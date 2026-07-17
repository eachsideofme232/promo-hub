import { NextRequest, NextResponse } from 'next/server'
import { getTeamContext } from '@/lib/api/auth'
import { PROMOTION_SELECT, type PromotionRow } from '@/lib/api/promotions'

const DATE_REGEX = /^\d{4}-\d{2}-\d{2}$/
const VALID_STATUSES = ['planned', 'active', 'ended', 'cancelled']
const UUID_REGEX = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i

// GET /api/calendar?start=YYYY-MM-DD&end=YYYY-MM-DD - Promotions for a date range,
// shaped for the calendar UI (CalendarPromotion)
export async function GET(request: NextRequest) {
  const { context, error } = await getTeamContext()
  if (error) return error
  const { supabase, teamId } = context

  const searchParams = request.nextUrl.searchParams
  const startDate = searchParams.get('start')
  const endDate = searchParams.get('end')

  if (!startDate || !endDate || !DATE_REGEX.test(startDate) || !DATE_REGEX.test(endDate)) {
    return NextResponse.json(
      { error: 'start와 end 파라미터가 필요합니다 (YYYY-MM-DD)' },
      { status: 400 }
    )
  }
  if (endDate < startDate) {
    return NextResponse.json({ error: '종료일은 시작일 이후여야 합니다' }, { status: 400 })
  }

  const channelIds = searchParams
    .get('channels')
    ?.split(',')
    .filter((id) => UUID_REGEX.test(id))
  const statuses = searchParams
    .get('statuses')
    ?.split(',')
    .filter((s) => VALID_STATUSES.includes(s))

  // Overlap: promo.start <= range.end AND promo.end >= range.start
  let query = supabase
    .from('promotions')
    .select(PROMOTION_SELECT)
    .eq('team_id', teamId)
    .lte('start_date', endDate)
    .gte('end_date', startDate)
    .order('start_date', { ascending: true })

  if (channelIds && channelIds.length > 0) {
    query = query.in('channel_id', channelIds)
  }
  if (statuses && statuses.length > 0) {
    query = query.in('status', statuses)
  }

  const { data, error: queryError } = await query

  if (queryError) {
    return NextResponse.json({ error: queryError.message }, { status: 500 })
  }

  const promotions = ((data ?? []) as unknown as PromotionRow[]).map((row) => ({
    id: row.id,
    title: row.title,
    status: row.status,
    channelId: row.channel_id,
    channelName: row.channels?.name ?? '',
    channelColor: row.channels?.color ?? '#888888',
    channelSlug: row.channels?.slug ?? '',
    startDate: row.start_date,
    endDate: row.end_date,
    isStart: true,
    isEnd: true,
    isMultiDay: row.start_date !== row.end_date,
  }))

  return NextResponse.json({ data: promotions })
}
