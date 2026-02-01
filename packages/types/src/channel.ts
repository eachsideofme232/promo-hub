// Channel types

export interface Channel {
  id: string
  name: string
  slug: string
  logoUrl?: string
  color: string
  isActive: boolean
  createdAt: string
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
