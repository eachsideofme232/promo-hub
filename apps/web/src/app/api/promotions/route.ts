import { NextRequest, NextResponse } from 'next/server'
import { getTeamContext } from '@/lib/api/auth'
import {
  promotionInputSchema,
  mapPromotionResponse,
  isChannelAccessible,
  PROMOTION_SELECT,
  type PromotionRow,
} from '@/lib/api/promotions'

const VALID_STATUSES = ['planned', 'active', 'ended', 'cancelled']
const UUID_REGEX = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i

// GET /api/promotions - List the team's promotions with optional filters
export async function GET(request: NextRequest) {
  const { context, error } = await getTeamContext()
  if (error) return error
  const { supabase, teamId } = context

  const searchParams = request.nextUrl.searchParams
  const page = Math.max(1, parseInt(searchParams.get('page') ?? '1', 10) || 1)
  const limit = Math.min(100, Math.max(1, parseInt(searchParams.get('limit') ?? '50', 10) || 50))
  const offset = (page - 1) * limit

  const search = searchParams.get('search')?.trim()
  const statuses = searchParams
    .get('statuses')
    ?.split(',')
    .filter((s) => VALID_STATUSES.includes(s))
  const channelIds = searchParams
    .get('channels')
    ?.split(',')
    .filter((id) => UUID_REGEX.test(id))
  const startDate = searchParams.get('start')
  const endDate = searchParams.get('end')

  let query = supabase
    .from('promotions')
    .select(PROMOTION_SELECT, { count: 'exact' })
    .eq('team_id', teamId)
    .order('start_date', { ascending: false })
    .range(offset, offset + limit - 1)

  if (statuses && statuses.length > 0) {
    query = query.in('status', statuses)
  }
  if (channelIds && channelIds.length > 0) {
    query = query.in('channel_id', channelIds)
  }
  if (search) {
    query = query.ilike('title', `%${search}%`)
  }
  // Overlap semantics: promotion intersects [start, end]
  if (startDate) {
    query = query.gte('end_date', startDate)
  }
  if (endDate) {
    query = query.lte('start_date', endDate)
  }

  const { data, error: queryError, count } = await query

  if (queryError) {
    return NextResponse.json({ error: queryError.message }, { status: 500 })
  }

  return NextResponse.json({
    data: ((data ?? []) as unknown as PromotionRow[]).map(mapPromotionResponse),
    pagination: { page, limit, total: count ?? 0 },
  })
}

// POST /api/promotions - Create a promotion for the caller's team
export async function POST(request: NextRequest) {
  const { context, error } = await getTeamContext()
  if (error) return error
  const { supabase, teamId, userId, role } = context

  if (role === 'viewer') {
    return NextResponse.json({ error: '프로모션을 생성할 권한이 없습니다' }, { status: 403 })
  }

  let body: unknown
  try {
    body = await request.json()
  } catch {
    return NextResponse.json({ error: '올바른 JSON 형식이 아닙니다' }, { status: 400 })
  }

  const parsed = promotionInputSchema.safeParse(body)
  if (!parsed.success) {
    return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 })
  }

  const input = parsed.data

  if (!(await isChannelAccessible(supabase, input.channelId, teamId))) {
    return NextResponse.json({ error: '사용할 수 없는 채널입니다' }, { status: 400 })
  }

  const { data, error: insertError } = await supabase
    .from('promotions')
    .insert({
      team_id: teamId,
      channel_id: input.channelId,
      template_id: input.templateId ?? null,
      title: input.title,
      description: input.description || null,
      status: input.status ?? 'planned',
      discount_type: input.discountType,
      discount_value: input.discountValue,
      start_date: input.startDate,
      end_date: input.endDate,
      memo: input.memo || null,
      created_by: userId,
    })
    .select(PROMOTION_SELECT)
    .single()

  if (insertError) {
    return NextResponse.json({ error: insertError.message }, { status: 500 })
  }

  // Non-blocking conflict detection: same channel, overlapping dates
  const { data: conflicts } = await supabase
    .from('promotions')
    .select('id, title, start_date, end_date')
    .eq('team_id', teamId)
    .eq('channel_id', input.channelId)
    .neq('id', (data as unknown as PromotionRow).id)
    .neq('status', 'cancelled')
    .lte('start_date', input.endDate)
    .gte('end_date', input.startDate)

  return NextResponse.json(
    {
      data: mapPromotionResponse(data as unknown as PromotionRow),
      conflicts: (conflicts ?? []).map((c) => ({
        id: c.id,
        title: c.title,
        startDate: c.start_date,
        endDate: c.end_date,
      })),
    },
    { status: 201 }
  )
}
