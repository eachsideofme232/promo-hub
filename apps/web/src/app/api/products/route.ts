import { createClient } from '@/lib/supabase/server'
import { NextRequest, NextResponse } from 'next/server'
import { productFormSchema } from '@promohub/utils'

// Helper: Map a product DB row (with nested channel prices) to camelCase response
function mapProductResponse(row: Record<string, unknown>) {
  const channelPricesRaw = row.product_channel_prices
  const channelPrices = Array.isArray(channelPricesRaw)
    ? channelPricesRaw.map((cp: Record<string, unknown>) => ({
        id: cp.id,
        channelId: cp.channel_id,
        sellingPrice: cp.selling_price,
        channelFeeRate: cp.channel_fee_rate,
        isActive: cp.is_active,
        notes: cp.notes,
      }))
    : []

  return {
    id: row.id,
    teamId: row.team_id,
    name: row.name,
    sku: row.sku,
    barcode: row.barcode,
    brand: row.brand,
    category: row.category,
    description: row.description,
    imageUrl: row.image_url,
    basePrice: row.base_price,
    costPrice: row.cost_price,
    isActive: row.is_active,
    createdAt: row.created_at,
    updatedAt: row.updated_at,
    channelPrices,
  }
}

// GET /api/products - List products with channel prices
export async function GET() {
  const supabase = await createClient()

  // 1. Verify authentication
  const { data: { user }, error: authError } = await supabase.auth.getUser()
  if (authError || !user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  // 2. Get team membership
  const { data: membership, error: teamError } = await supabase
    .from('team_members')
    .select('team_id')
    .eq('user_id', user.id)
    .limit(1)
    .single()

  if (teamError || !membership) {
    return NextResponse.json({ error: 'No team found' }, { status: 403 })
  }

  // 3. Fetch products with nested channel prices
  const { data, error } = await supabase
    .from('products')
    .select('*, product_channel_prices(id, channel_id, selling_price, channel_fee_rate, is_active, notes)')
    .eq('team_id', membership.team_id)
    .order('name')

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }

  // 4. Map to camelCase response
  const products = (data ?? []).map(mapProductResponse)

  return NextResponse.json({ data: products })
}

// POST /api/products - Create product with channel prices
export async function POST(request: NextRequest) {
  const supabase = await createClient()

  // 1. Verify authentication
  const { data: { user }, error: authError } = await supabase.auth.getUser()
  if (authError || !user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  // 2. Get team membership
  const { data: membership, error: teamError } = await supabase
    .from('team_members')
    .select('team_id, role')
    .eq('user_id', user.id)
    .limit(1)
    .single()

  if (teamError || !membership) {
    return NextResponse.json({ error: 'No team found' }, { status: 403 })
  }

  // 3. Validate request body
  let body: unknown
  try {
    body = await request.json()
  } catch {
    return NextResponse.json({ error: '올바른 JSON 형식이 아닙니다' }, { status: 400 })
  }

  const parsed = productFormSchema.safeParse(body)
  if (!parsed.success) {
    return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 })
  }

  // 4. Insert product with team scoping
  const { data: product, error: insertError } = await supabase
    .from('products')
    .insert({
      team_id: membership.team_id,
      name: parsed.data.name,
      sku: parsed.data.sku,
      barcode: parsed.data.barcode || null,
      brand: parsed.data.brand || null,
      category: parsed.data.category || null,
      description: parsed.data.description || null,
      image_url: parsed.data.imageUrl || null,
      base_price: parsed.data.basePrice,
      cost_price: parsed.data.costPrice ?? null,
    })
    .select()
    .single()

  if (insertError) {
    // Handle unique SKU constraint violation
    if (insertError.code === '23505') {
      return NextResponse.json(
        { error: '이미 사용 중인 SKU입니다' },
        { status: 409 }
      )
    }
    return NextResponse.json({ error: insertError.message }, { status: 500 })
  }

  // 5. Insert channel prices if provided (two-step insert)
  if (parsed.data.channelPrices && parsed.data.channelPrices.length > 0) {
    const channelPriceRows = parsed.data.channelPrices.map((cp) => ({
      product_id: product.id,
      channel_id: cp.channelId,
      selling_price: cp.sellingPrice,
      channel_fee_rate: cp.channelFeeRate ?? null,
      is_active: cp.isActive,
    }))

    const { error: cpError } = await supabase
      .from('product_channel_prices')
      .insert(channelPriceRows)

    if (cpError) {
      console.warn('Warning: Failed to insert channel prices for product', product.id, cpError.message)
    }
  }

  // 6. Re-fetch complete product with channel prices
  const { data: fullProduct, error: fetchError } = await supabase
    .from('products')
    .select('*, product_channel_prices(id, channel_id, selling_price, channel_fee_rate, is_active, notes)')
    .eq('id', product.id)
    .single()

  if (fetchError) {
    // Product was created but re-fetch failed; return basic product data
    return NextResponse.json({ data: mapProductResponse(product) }, { status: 201 })
  }

  return NextResponse.json({ data: mapProductResponse(fullProduct) }, { status: 201 })
}
