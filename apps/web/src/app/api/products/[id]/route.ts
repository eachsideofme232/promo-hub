import { createClient } from '@/lib/supabase/server'
import { NextRequest, NextResponse } from 'next/server'
import { z } from 'zod'
import { channelPriceSchema } from '@promohub/utils'

// Update schema: all fields optional, plus isActive toggle
const updateProductSchema = z.object({
  name: z.string().min(1, '상품명을 입력해주세요').max(200, '200자 이내로 입력해주세요').trim().optional(),
  sku: z.string().min(1, 'SKU 코드를 입력해주세요').max(50, '50자 이내로 입력해주세요').trim().optional(),
  barcode: z.string().max(50, '50자 이내로 입력해주세요').trim().optional().or(z.literal('')),
  brand: z.string().max(100, '100자 이내로 입력해주세요').trim().optional().or(z.literal('')),
  category: z.string().max(100, '100자 이내로 입력해주세요').trim().optional().or(z.literal('')),
  description: z.string().max(2000, '2000자 이내로 입력해주세요').optional().or(z.literal('')),
  basePrice: z.number().int('정수 금액을 입력해주세요').min(0, '0 이상의 금액을 입력해주세요').optional(),
  costPrice: z.number().int('정수 금액을 입력해주세요').min(0, '0 이상의 금액을 입력해주세요').optional(),
  imageUrl: z.string().url('올바른 URL을 입력해주세요').optional().or(z.literal('')),
  isActive: z.boolean().optional(),
  channelPrices: z.array(channelPriceSchema).optional(),
})

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

// Helper: Verify auth and get team membership
async function getAuthContext(supabase: Awaited<ReturnType<typeof createClient>>) {
  const { data: { user }, error: authError } = await supabase.auth.getUser()
  if (authError || !user) {
    return { error: NextResponse.json({ error: 'Unauthorized' }, { status: 401 }) }
  }

  const { data: membership, error: teamError } = await supabase
    .from('team_members')
    .select('team_id, role')
    .eq('user_id', user.id)
    .limit(1)
    .single()

  if (teamError || !membership) {
    return { error: NextResponse.json({ error: 'No team found' }, { status: 403 }) }
  }

  return { user, membership }
}

// Helper: Verify the product exists and belongs to this team
async function verifyProductOwnership(
  supabase: Awaited<ReturnType<typeof createClient>>,
  productId: string,
  teamId: string
) {
  const { data: existing, error } = await supabase
    .from('products')
    .select('team_id')
    .eq('id', productId)
    .single()

  if (error || !existing) {
    return { error: NextResponse.json({ error: '상품을 찾을 수 없습니다' }, { status: 404 }) }
  }

  if (existing.team_id !== teamId) {
    return { error: NextResponse.json({ error: '접근 권한이 없습니다' }, { status: 403 }) }
  }

  return { existing }
}

// GET /api/products/[id] - Get single product with channel prices
export async function GET(
  _request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params
  const supabase = await createClient()

  // 1. Verify authentication and team membership
  const auth = await getAuthContext(supabase)
  if ('error' in auth && auth.error) return auth.error
  const { membership } = auth as { membership: { team_id: string; role: string }; user: unknown }

  // 2. Verify product ownership
  const ownership = await verifyProductOwnership(supabase, id, membership.team_id)
  if ('error' in ownership && ownership.error) return ownership.error

  // 3. Fetch product with channel prices
  const { data, error } = await supabase
    .from('products')
    .select('*, product_channel_prices(id, channel_id, selling_price, channel_fee_rate, is_active, notes)')
    .eq('id', id)
    .single()

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }

  return NextResponse.json({ data: mapProductResponse(data) })
}

// PATCH /api/products/[id] - Update product and channel prices
export async function PATCH(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params
  const supabase = await createClient()

  // 1. Verify authentication and team membership
  const auth = await getAuthContext(supabase)
  if ('error' in auth && auth.error) return auth.error
  const { membership } = auth as { membership: { team_id: string; role: string }; user: unknown }

  // 2. Verify product ownership
  const ownership = await verifyProductOwnership(supabase, id, membership.team_id)
  if ('error' in ownership && ownership.error) return ownership.error

  // 3. Validate request body
  let body: unknown
  try {
    body = await request.json()
  } catch {
    return NextResponse.json({ error: '올바른 JSON 형식이 아닙니다' }, { status: 400 })
  }

  const parsed = updateProductSchema.safeParse(body)
  if (!parsed.success) {
    return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 })
  }

  // 4. Map camelCase input to snake_case for DB (product fields only)
  const updateData: Record<string, unknown> = {}
  if (parsed.data.name !== undefined) updateData.name = parsed.data.name
  if (parsed.data.sku !== undefined) updateData.sku = parsed.data.sku
  if (parsed.data.barcode !== undefined) updateData.barcode = parsed.data.barcode || null
  if (parsed.data.brand !== undefined) updateData.brand = parsed.data.brand || null
  if (parsed.data.category !== undefined) updateData.category = parsed.data.category || null
  if (parsed.data.description !== undefined) updateData.description = parsed.data.description || null
  if (parsed.data.basePrice !== undefined) updateData.base_price = parsed.data.basePrice
  if (parsed.data.costPrice !== undefined) updateData.cost_price = parsed.data.costPrice
  if (parsed.data.imageUrl !== undefined) updateData.image_url = parsed.data.imageUrl || null
  if (parsed.data.isActive !== undefined) updateData.is_active = parsed.data.isActive

  const hasProductUpdates = Object.keys(updateData).length > 0
  const hasChannelPriceUpdates = parsed.data.channelPrices !== undefined

  if (!hasProductUpdates && !hasChannelPriceUpdates) {
    return NextResponse.json({ error: '수정할 항목이 없습니다' }, { status: 400 })
  }

  // 5. Update product fields if any
  if (hasProductUpdates) {
    const { error: updateError } = await supabase
      .from('products')
      .update(updateData)
      .eq('id', id)

    if (updateError) {
      if (updateError.code === '23505') {
        return NextResponse.json(
          { error: '이미 사용 중인 SKU입니다' },
          { status: 409 }
        )
      }
      return NextResponse.json({ error: updateError.message }, { status: 500 })
    }
  }

  // 6. Handle channel prices update (delete-then-insert strategy)
  if (hasChannelPriceUpdates && parsed.data.channelPrices) {
    // Delete all existing channel prices for this product
    const { error: deleteError } = await supabase
      .from('product_channel_prices')
      .delete()
      .eq('product_id', id)

    if (deleteError) {
      console.warn('Warning: Failed to delete existing channel prices', deleteError.message)
    }

    // Insert new channel prices
    if (parsed.data.channelPrices.length > 0) {
      const channelPriceRows = parsed.data.channelPrices.map((cp) => ({
        product_id: id,
        channel_id: cp.channelId,
        selling_price: cp.sellingPrice,
        channel_fee_rate: cp.channelFeeRate ?? null,
        is_active: cp.isActive,
      }))

      const { error: insertError } = await supabase
        .from('product_channel_prices')
        .insert(channelPriceRows)

      if (insertError) {
        console.warn('Warning: Failed to insert new channel prices', insertError.message)
      }
    }
  }

  // 7. Re-fetch and return updated product with channel prices
  const { data: fullProduct, error: fetchError } = await supabase
    .from('products')
    .select('*, product_channel_prices(id, channel_id, selling_price, channel_fee_rate, is_active, notes)')
    .eq('id', id)
    .single()

  if (fetchError) {
    return NextResponse.json({ error: fetchError.message }, { status: 500 })
  }

  return NextResponse.json({ data: mapProductResponse(fullProduct) })
}

// DELETE /api/products/[id] - Delete product (CASCADE handles channel prices)
export async function DELETE(
  _request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params
  const supabase = await createClient()

  // 1. Verify authentication and team membership
  const auth = await getAuthContext(supabase)
  if ('error' in auth && auth.error) return auth.error
  const { membership } = auth as { membership: { team_id: string; role: string }; user: unknown }

  // 2. Verify product ownership
  const ownership = await verifyProductOwnership(supabase, id, membership.team_id)
  if ('error' in ownership && ownership.error) return ownership.error

  // 3. Delete the product (CASCADE will handle channel prices)
  const { error } = await supabase
    .from('products')
    .delete()
    .eq('id', id)

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }

  return NextResponse.json({ success: true })
}
