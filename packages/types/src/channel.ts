// Channel types

export interface Channel {
  id: string
  name: string
  slug: string
  logoUrl?: string
  color: string
  isActive: boolean
  createdAt: string
  teamId?: string | null
  promoTypes?: string[]
  /** true when teamId is null (system/pre-seeded channel) */
  isSystem?: boolean
}

// Input types for channel CRUD operations
export interface CreateChannelInput {
  name: string
  slug: string
  color: string
  promoTypes?: string[]
}

export interface UpdateChannelInput {
  name?: string
  slug?: string
  color?: string
  isActive?: boolean
  promoTypes?: string[]
}

// Predefined Korean e-commerce channels
export type ChannelSlug =
  | 'oliveyoung'
  | 'coupang'
  | 'naver'
  | 'kakao'
  | 'musinsa'
  | 'ssg'
  | 'lotteon'
  | '11st'
