import { createClient } from '@/lib/supabase/server'
import { NextRequest, NextResponse } from 'next/server'
import { z } from 'zod'

const createChannelSchema = z.object({
  name: z.string().min(1, '채널명을 입력해주세요').max(50, '채널명은 50자 이하여야 합니다').trim(),
  slug: z.string().min(1).max(50).regex(/^[a-z0-9-]+$/, '슬러그는 영문 소문자, 숫자, 하이픈만 사용 가능합니다').trim(),
  color: z.string().regex(/^#[0-9A-Fa-f]{6}$/, '올바른 색상 코드를 입력해주세요'),
  promoTypes: z.array(z.string()).optional().default([]),
})

// GET /api/channels - List all channels (system + team custom)
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

  // 3. Fetch system channels (team_id IS NULL) and team's custom channels
  const { data, error } = await supabase
    .from('channels')
    .select('*')
    .or(`team_id.is.null,team_id.eq.${membership.team_id}`)
    .order('name')

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }

  // 4. Map to response with isSystem flag
  const channels = (data ?? []).map((ch) => ({
    id: ch.id,
    name: ch.name,
    slug: ch.slug,
    logoUrl: ch.logo_url,
    color: ch.color,
    isActive: ch.is_active,
    isSystem: ch.team_id === null,
    teamId: ch.team_id,
    promoTypes: ch.promo_types ?? [],
    createdAt: ch.created_at,
  }))

  return NextResponse.json({ data: channels })
}

// POST /api/channels - Create a custom channel
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

  const parsed = createChannelSchema.safeParse(body)
  if (!parsed.success) {
    return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 })
  }

  // 4. Insert custom channel with team scoping
  const { data, error } = await supabase
    .from('channels')
    .insert({
      name: parsed.data.name,
      slug: parsed.data.slug,
      color: parsed.data.color,
      promo_types: parsed.data.promoTypes,
      team_id: membership.team_id,
      is_active: true,
    })
    .select()
    .single()

  if (error) {
    // Handle unique constraint violation on slug
    if (error.code === '23505') {
      return NextResponse.json(
        { error: '이미 사용 중인 슬러그입니다' },
        { status: 409 }
      )
    }
    return NextResponse.json({ error: error.message }, { status: 500 })
  }

  // 5. Return created channel with isSystem flag
  const channel = {
    id: data.id,
    name: data.name,
    slug: data.slug,
    logoUrl: data.logo_url,
    color: data.color,
    isActive: data.is_active,
    isSystem: false,
    teamId: data.team_id,
    promoTypes: data.promo_types ?? [],
    createdAt: data.created_at,
  }

  return NextResponse.json({ data: channel }, { status: 201 })
}
