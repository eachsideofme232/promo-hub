import { z } from 'zod'
import type { SupabaseClient } from '@supabase/supabase-js'

// Server-side promotion input schema.
// teamId is intentionally NOT accepted from the client - it is derived
// from the authenticated user's team membership.
const dateString = z
  .string()
  .regex(/^\d{4}-\d{2}-\d{2}$/, '올바른 날짜 형식이 아닙니다 (YYYY-MM-DD)')

export const promotionInputSchema = z
  .object({
    title: z.string().min(1, '프로모션명을 입력해주세요').max(200, '200자 이내로 입력해주세요').trim(),
    description: z.string().max(2000, '2000자 이내로 입력해주세요').optional().or(z.literal('')),
    channelId: z.string().uuid('올바른 채널을 선택해주세요'),
    templateId: z.string().uuid().optional(),
    status: z.enum(['planned', 'active', 'ended', 'cancelled']).optional(),
    discountType: z.enum(['percentage', 'bogo', 'coupon', 'gift', 'bundle'], {
      errorMap: () => ({ message: '할인 유형을 선택해주세요' }),
    }),
    discountValue: z.string().min(1, '할인 값을 입력해주세요').max(50),
    startDate: dateString,
    endDate: dateString,
    memo: z.string().max(1000, '1000자 이내로 입력해주세요').optional().or(z.literal('')),
  })
  .refine((data) => data.endDate >= data.startDate, {
    message: '종료일은 시작일 이후여야 합니다',
    path: ['endDate'],
  })

export const promotionUpdateSchema = z.object({
  title: z.string().min(1).max(200).trim().optional(),
  description: z.string().max(2000).optional().or(z.literal('')),
  channelId: z.string().uuid().optional(),
  templateId: z.string().uuid().nullable().optional(),
  status: z.enum(['planned', 'active', 'ended', 'cancelled']).optional(),
  discountType: z.enum(['percentage', 'bogo', 'coupon', 'gift', 'bundle']).optional(),
  discountValue: z.string().min(1).max(50).optional(),
  startDate: dateString.optional(),
  endDate: dateString.optional(),
  memo: z.string().max(1000).optional().or(z.literal('')),
})

export const PROMOTION_SELECT =
  '*, channels:channel_id (id, name, slug, color)'

interface ChannelJoin {
  id: string
  name: string
  slug: string
  color: string
}

export interface PromotionRow {
  id: string
  team_id: string
  channel_id: string
  template_id: string | null
  title: string
  description: string | null
  status: string
  discount_type: string
  discount_value: string
  start_date: string
  end_date: string
  memo: string | null
  created_at: string
  updated_at: string
  created_by: string | null
  channels: ChannelJoin | null
}

// Map a DB row (snake_case, with joined channel) to the camelCase API shape
export function mapPromotionResponse(row: PromotionRow) {
  return {
    id: row.id,
    teamId: row.team_id,
    channelId: row.channel_id,
    templateId: row.template_id ?? undefined,
    title: row.title,
    description: row.description ?? undefined,
    status: row.status,
    discountType: row.discount_type,
    discountValue: row.discount_value,
    startDate: row.start_date,
    endDate: row.end_date,
    memo: row.memo ?? undefined,
    createdAt: row.created_at,
    updatedAt: row.updated_at,
    createdBy: row.created_by ?? undefined,
    channel: row.channels
      ? {
          id: row.channels.id,
          name: row.channels.name,
          slug: row.channels.slug,
          color: row.channels.color,
        }
      : undefined,
  }
}

/**
 * Verify that a channel exists and is usable by the team
 * (system channel or the team's own custom channel).
 */
export async function isChannelAccessible(
  supabase: SupabaseClient,
  channelId: string,
  teamId: string
): Promise<boolean> {
  const { data } = await supabase
    .from('channels')
    .select('id, team_id')
    .eq('id', channelId)
    .single()

  if (!data) return false
  return data.team_id === null || data.team_id === teamId
}
