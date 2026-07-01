import { NextRequest, NextResponse } from 'next/server'
import { getTeamContext } from '@/lib/api/auth'
import {
  promotionUpdateSchema,
  mapPromotionResponse,
  isChannelAccessible,
  PROMOTION_SELECT,
  type PromotionRow,
} from '@/lib/api/promotions'

// GET /api/promotions/[id] - Get a single promotion
export async function GET(
  _request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params
  const { context, error } = await getTeamContext()
  if (error) return error
  const { supabase, teamId } = context

  const { data, error: queryError } = await supabase
    .from('promotions')
    .select(PROMOTION_SELECT)
    .eq('id', id)
    .eq('team_id', teamId)
    .single()

  if (queryError || !data) {
    return NextResponse.json({ error: '프로모션을 찾을 수 없습니다' }, { status: 404 })
  }

  return NextResponse.json({ data: mapPromotionResponse(data as unknown as PromotionRow) })
}

// PATCH /api/promotions/[id] - Update a promotion
export async function PATCH(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params
  const { context, error } = await getTeamContext()
  if (error) return error
  const { supabase, teamId, role } = context

  if (role === 'viewer') {
    return NextResponse.json({ error: '프로모션을 수정할 권한이 없습니다' }, { status: 403 })
  }

  let body: unknown
  try {
    body = await request.json()
  } catch {
    return NextResponse.json({ error: '올바른 JSON 형식이 아닙니다' }, { status: 400 })
  }

  const parsed = promotionUpdateSchema.safeParse(body)
  if (!parsed.success) {
    return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 })
  }

  const input = parsed.data

  // Fetch the existing promotion (team-scoped) to validate date ordering
  const { data: existing, error: fetchError } = await supabase
    .from('promotions')
    .select('id, start_date, end_date')
    .eq('id', id)
    .eq('team_id', teamId)
    .single()

  if (fetchError || !existing) {
    return NextResponse.json({ error: '프로모션을 찾을 수 없습니다' }, { status: 404 })
  }

  const newStart = input.startDate ?? existing.start_date
  const newEnd = input.endDate ?? existing.end_date
  if (newEnd < newStart) {
    return NextResponse.json({ error: '종료일은 시작일 이후여야 합니다' }, { status: 400 })
  }

  if (input.channelId && !(await isChannelAccessible(supabase, input.channelId, teamId))) {
    return NextResponse.json({ error: '사용할 수 없는 채널입니다' }, { status: 400 })
  }

  const updateData: Record<string, unknown> = {}
  if (input.title !== undefined) updateData.title = input.title
  if (input.description !== undefined) updateData.description = input.description || null
  if (input.channelId !== undefined) updateData.channel_id = input.channelId
  if (input.templateId !== undefined) updateData.template_id = input.templateId
  if (input.status !== undefined) updateData.status = input.status
  if (input.discountType !== undefined) updateData.discount_type = input.discountType
  if (input.discountValue !== undefined) updateData.discount_value = input.discountValue
  if (input.startDate !== undefined) updateData.start_date = input.startDate
  if (input.endDate !== undefined) updateData.end_date = input.endDate
  if (input.memo !== undefined) updateData.memo = input.memo || null

  if (Object.keys(updateData).length === 0) {
    return NextResponse.json({ error: '수정할 내용이 없습니다' }, { status: 400 })
  }

  const { data, error: updateError } = await supabase
    .from('promotions')
    .update(updateData)
    .eq('id', id)
    .eq('team_id', teamId)
    .select(PROMOTION_SELECT)
    .single()

  if (updateError) {
    return NextResponse.json({ error: updateError.message }, { status: 500 })
  }

  return NextResponse.json({ data: mapPromotionResponse(data as unknown as PromotionRow) })
}

// DELETE /api/promotions/[id] - Delete a promotion (owner/admin only, per RLS)
export async function DELETE(
  _request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params
  const { context, error } = await getTeamContext()
  if (error) return error
  const { supabase, teamId, role } = context

  if (role !== 'owner' && role !== 'admin') {
    return NextResponse.json({ error: '프로모션을 삭제할 권한이 없습니다' }, { status: 403 })
  }

  const { data: existing } = await supabase
    .from('promotions')
    .select('id')
    .eq('id', id)
    .eq('team_id', teamId)
    .single()

  if (!existing) {
    return NextResponse.json({ error: '프로모션을 찾을 수 없습니다' }, { status: 404 })
  }

  const { error: deleteError } = await supabase
    .from('promotions')
    .delete()
    .eq('id', id)
    .eq('team_id', teamId)

  if (deleteError) {
    return NextResponse.json({ error: deleteError.message }, { status: 500 })
  }

  return NextResponse.json({ success: true })
}
