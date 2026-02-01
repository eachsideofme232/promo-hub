import { z } from 'zod'

// Common validation schemas

// Promotion validation
export const promotionSchema = z.object({
  title: z.string().min(1, '프로모션명을 입력해주세요').max(200, '200자 이내로 입력해주세요'),
  description: z.string().max(2000, '2000자 이내로 입력해주세요').optional(),
  channelId: z.string().uuid('올바른 채널을 선택해주세요'),
  teamId: z.string().uuid('올바른 팀을 선택해주세요'),
  templateId: z.string().uuid().optional(),
  discountType: z.enum(['percentage', 'bogo', 'coupon', 'gift', 'bundle'], {
    errorMap: () => ({ message: '할인 유형을 선택해주세요' }),
  }),
  discountValue: z.string().min(1, '할인 값을 입력해주세요').max(50),
  startDate: z.string().refine((val) => !isNaN(Date.parse(val)), {
    message: '올바른 날짜를 입력해주세요',
  }),
  endDate: z.string().refine((val) => !isNaN(Date.parse(val)), {
    message: '올바른 날짜를 입력해주세요',
  }),
  memo: z.string().max(1000, '1000자 이내로 입력해주세요').optional(),
}).refine(
  (data) => new Date(data.endDate) >= new Date(data.startDate),
  {
    message: '종료일은 시작일 이후여야 합니다',
    path: ['endDate'],
  }
)

export type PromotionFormData = z.infer<typeof promotionSchema>

// Team validation
export const teamSchema = z.object({
  name: z.string().min(1, '팀 이름을 입력해주세요').max(100, '100자 이내로 입력해주세요'),
  slug: z.string()
    .min(1, '슬러그를 입력해주세요')
    .max(50, '50자 이내로 입력해주세요')
    .regex(/^[a-z0-9-]+$/, '영문 소문자, 숫자, 하이픈만 사용할 수 있습니다'),
})

export type TeamFormData = z.infer<typeof teamSchema>

// Team invite validation
export const teamInviteSchema = z.object({
  email: z.string().email('올바른 이메일 주소를 입력해주세요'),
  role: z.enum(['admin', 'member', 'viewer'], {
    errorMap: () => ({ message: '권한을 선택해주세요' }),
  }),
})

export type TeamInviteFormData = z.infer<typeof teamInviteSchema>

// Helper function to safely parse with Zod
export function safeParse<T>(schema: z.ZodSchema<T>, data: unknown): {
  success: boolean
  data?: T
  errors?: Record<string, string>
} {
  const result = schema.safeParse(data)

  if (result.success) {
    return { success: true, data: result.data }
  }

  const errors: Record<string, string> = {}
  result.error.errors.forEach((err) => {
    const path = err.path.join('.')
    errors[path] = err.message
  })

  return { success: false, errors }
}
