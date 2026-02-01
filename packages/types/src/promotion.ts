// Promotion types

export type PromotionStatus = 'planned' | 'active' | 'ended' | 'cancelled'

export type DiscountType = 'percentage' | 'bogo' | 'coupon' | 'gift' | 'bundle'

export interface Promotion {
  id: string
  teamId: string
  channelId: string
  templateId?: string

  title: string
  description?: string

  status: PromotionStatus
  discountType: DiscountType
  discountValue: string

  startDate: string // ISO date string
  endDate: string   // ISO date string

  memo?: string

  createdAt: string
  updatedAt: string
  createdBy?: string
}

export interface CreatePromotionInput {
  teamId: string
  channelId: string
  templateId?: string
  title: string
  description?: string
  discountType: DiscountType
  discountValue: string
  startDate: string
  endDate: string
  memo?: string
}

export interface UpdatePromotionInput {
  title?: string
  description?: string
  status?: PromotionStatus
  discountType?: DiscountType
  discountValue?: string
  startDate?: string
  endDate?: string
  memo?: string
}

export interface PromotionFilters {
  channelIds?: string[]
  status?: PromotionStatus
  startDate?: string
  endDate?: string
  search?: string
}
