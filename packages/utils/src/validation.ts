import { z } from 'zod'

// Common validation schemas

// Password validation helper
const passwordSchema = z
  .string()
  .min(8, '비밀번호는 8자 이상이어야 합니다')
  .max(100, '비밀번호는 100자 이하여야 합니다')
  .regex(/[A-Z]/, '대문자를 1자 이상 포함해야 합니다')
  .regex(/[a-z]/, '소문자를 1자 이상 포함해야 합니다')
  .regex(/[0-9]/, '숫자를 1자 이상 포함해야 합니다')

// Email validation helper
const emailSchema = z
  .string()
  .email('올바른 이메일 주소를 입력해주세요')
  .max(255, '이메일은 255자 이하여야 합니다')

// ============================================
// Auth Validation Schemas
// ============================================

// Login
export const loginSchema = z.object({
  email: emailSchema,
  password: z.string().min(1, '비밀번호를 입력해주세요'),
})

export type LoginFormData = z.infer<typeof loginSchema>

// Signup
export const signupSchema = z.object({
  email: emailSchema,
  password: passwordSchema,
  confirmPassword: z.string(),
  name: z.string().min(1, '이름을 입력해주세요').max(100, '100자 이내로 입력해주세요'),
  agreeToTerms: z.boolean().refine((val) => val === true, {
    message: '이용약관에 동의해주세요',
  }),
}).refine((data) => data.password === data.confirmPassword, {
  message: '비밀번호가 일치하지 않습니다',
  path: ['confirmPassword'],
})

export type SignupFormData = z.infer<typeof signupSchema>

// Password reset request
export const passwordResetRequestSchema = z.object({
  email: emailSchema,
})

export type PasswordResetRequestFormData = z.infer<typeof passwordResetRequestSchema>

// Password reset (with token)
export const passwordResetSchema = z.object({
  token: z.string().min(1, '유효하지 않은 토큰입니다'),
  password: passwordSchema,
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: '비밀번호가 일치하지 않습니다',
  path: ['confirmPassword'],
})

export type PasswordResetFormData = z.infer<typeof passwordResetSchema>

// Password update (authenticated user)
export const passwordUpdateSchema = z.object({
  currentPassword: z.string().min(1, '현재 비밀번호를 입력해주세요'),
  newPassword: passwordSchema,
  confirmPassword: z.string(),
}).refine((data) => data.newPassword === data.confirmPassword, {
  message: '비밀번호가 일치하지 않습니다',
  path: ['confirmPassword'],
}).refine((data) => data.currentPassword !== data.newPassword, {
  message: '새 비밀번호는 현재 비밀번호와 달라야 합니다',
  path: ['newPassword'],
})

export type PasswordUpdateFormData = z.infer<typeof passwordUpdateSchema>

// ============================================
// User Profile Validation Schemas
// ============================================

export const userProfileSchema = z.object({
  name: z.string().min(1, '이름을 입력해주세요').max(100, '100자 이내로 입력해주세요').optional(),
  phone: z.string().regex(/^01[0-9]-?[0-9]{4}-?[0-9]{4}$/, '올바른 전화번호 형식이 아닙니다').optional().or(z.literal('')),
  locale: z.enum(['ko', 'en'], {
    errorMap: () => ({ message: '언어를 선택해주세요' }),
  }).optional(),
  timezone: z.string().optional(),
})

export type UserProfileFormData = z.infer<typeof userProfileSchema>

export const userPreferencesSchema = z.object({
  emailNotifications: z.boolean().optional(),
  pushNotifications: z.boolean().optional(),
  weekStartsOn: z.union([z.literal(0), z.literal(1)]).optional(),
  defaultCalendarView: z.enum(['month', 'week', 'day']).optional(),
  theme: z.enum(['light', 'dark', 'system']).optional(),
})

export type UserPreferencesFormData = z.infer<typeof userPreferencesSchema>

// ============================================
// Settings Validation Schemas
// ============================================

// Notification settings
export const notificationSettingsSchema = z.object({
  emailEnabled: z.boolean().optional(),
  slackEnabled: z.boolean().optional(),
  kakaoEnabled: z.boolean().optional(),
  promotionReminders: z.boolean().optional(),
  reminderDaysBefore: z.number().min(1, '1일 이상이어야 합니다').max(30, '30일 이하여야 합니다').optional(),
  dailyDigest: z.boolean().optional(),
  digestTime: z.string().regex(/^([01]?[0-9]|2[0-3]):[0-5][0-9]$/, '올바른 시간 형식이 아닙니다 (HH:mm)').optional(),
  conflictAlerts: z.boolean().optional(),
  teamUpdates: z.boolean().optional(),
})

export type NotificationSettingsFormData = z.infer<typeof notificationSettingsSchema>

// Team settings
export const teamSettingsSchema = z.object({
  defaultCurrency: z.enum(['KRW', 'USD'], {
    errorMap: () => ({ message: '통화를 선택해주세요' }),
  }).optional(),
  fiscalYearStart: z.number().min(1, '1월 이상이어야 합니다').max(12, '12월 이하여야 합니다').optional(),
})

export type TeamSettingsFormData = z.infer<typeof teamSettingsSchema>

// Channel preference
export const channelPreferenceSchema = z.object({
  channelId: z.string().uuid('올바른 채널을 선택해주세요'),
  isActive: z.boolean().optional(),
  displayOrder: z.number().min(0).optional(),
  color: z.string().regex(/^#[0-9A-Fa-f]{6}$/, '올바른 색상 코드가 아닙니다 (#RRGGBB)').optional(),
})

export type ChannelPreferenceFormData = z.infer<typeof channelPreferenceSchema>

// API key creation
export const apiKeyCreateSchema = z.object({
  name: z.string().min(1, 'API 키 이름을 입력해주세요').max(100, '100자 이내로 입력해주세요'),
  permissions: z.array(z.enum(['read', 'write', 'admin'])).min(1, '최소 1개의 권한을 선택해주세요'),
  expiresAt: z.string().refine((val) => !val || !isNaN(Date.parse(val)), {
    message: '올바른 날짜를 입력해주세요',
  }).optional(),
})

export type ApiKeyCreateFormData = z.infer<typeof apiKeyCreateSchema>

// ============================================
// Promotion Validation Schema
// ============================================

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

// ============================================
// Product Validation Schemas
// ============================================

// Channel price schema for a single channel price entry
export const channelPriceSchema = z.object({
  channelId: z.string().uuid('올바른 채널을 선택해주세요'),
  sellingPrice: z.number().int('정수 금액을 입력해주세요').min(0, '0 이상의 금액을 입력해주세요'),
  channelFeeRate: z.number().min(0, '0 이상의 수수료율을 입력해주세요').max(100, '수수료율은 100% 이하여야 합니다').optional(),
  isActive: z.boolean().default(true),
})

export type ChannelPriceFormData = z.infer<typeof channelPriceSchema>

// Product form schema (client-side, NO teamId -- injected server-side)
export const productFormSchema = z.object({
  name: z.string().min(1, '상품명을 입력해주세요').max(200, '200자 이내로 입력해주세요').trim(),
  sku: z.string().min(1, 'SKU 코드를 입력해주세요').max(50, '50자 이내로 입력해주세요').trim(),
  barcode: z.string().max(50, '50자 이내로 입력해주세요').trim().optional().or(z.literal('')),
  brand: z.string().max(100, '100자 이내로 입력해주세요').trim().optional().or(z.literal('')),
  category: z.string().max(100, '100자 이내로 입력해주세요').trim().optional().or(z.literal('')),
  description: z.string().max(2000, '2000자 이내로 입력해주세요').optional().or(z.literal('')),
  basePrice: z.number().int('정수 금액을 입력해주세요').min(0, '0 이상의 금액을 입력해주세요'),
  costPrice: z.number().int('정수 금액을 입력해주세요').min(0, '0 이상의 금액을 입력해주세요').optional(),
  imageUrl: z.string().url('올바른 URL을 입력해주세요').optional().or(z.literal('')),
  channelPrices: z.array(channelPriceSchema).default([]),
})

export type ProductFormData = z.infer<typeof productFormSchema>

// Backward compatibility alias (referenced by productBulkImportSchema)
export const productSchema = productFormSchema

// Product bulk import
export const productBulkImportSchema = z.object({
  products: z.array(productSchema).min(1, '최소 1개의 상품을 입력해주세요').max(1000, '한 번에 1000개까지만 등록할 수 있습니다'),
  skipDuplicates: z.boolean().optional(),
})

export type ProductBulkImportFormData = z.infer<typeof productBulkImportSchema>

// ============================================
// Calendar Filter Schemas
// ============================================

export const calendarFilterSchema = z.object({
  channels: z.array(z.string().uuid()).optional(),
  status: z.array(z.enum(['planned', 'active', 'ended', 'cancelled'])).optional(),
  startDate: z.string().refine((val) => !isNaN(Date.parse(val)), {
    message: '올바른 날짜를 입력해주세요',
  }),
  endDate: z.string().refine((val) => !isNaN(Date.parse(val)), {
    message: '올바른 날짜를 입력해주세요',
  }),
}).refine(
  (data) => new Date(data.endDate) >= new Date(data.startDate),
  {
    message: '종료일은 시작일 이후여야 합니다',
    path: ['endDate'],
  }
)

export type CalendarFilterFormData = z.infer<typeof calendarFilterSchema>

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
