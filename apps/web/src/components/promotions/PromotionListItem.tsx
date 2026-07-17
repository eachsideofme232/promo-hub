'use client'

import Link from 'next/link'
import { Calendar, Tag } from 'lucide-react'
import type { Promotion, DiscountType } from '@promohub/types'
import { PromotionStatusBadge } from './PromotionStatusBadge'
import { PromotionActions } from './PromotionActions'

interface Channel {
  id: string
  name: string
  color: string
}

interface PromotionListItemProps {
  promotion: Promotion
  channel: Channel | undefined
  isSelected?: boolean
  onSelect?: (id: string, selected: boolean) => void
  onDuplicate?: (id: string) => void
  onDelete?: (id: string) => void
}

const DISCOUNT_TYPE_LABELS: Record<DiscountType, string> = {
  percentage: '할인율',
  bogo: 'BOGO',
  coupon: '쿠폰',
  gift: '사은품',
  bundle: '번들',
}

function formatDateRange(startDate: string, endDate: string): string {
  const start = new Date(startDate)
  const end = new Date(endDate)

  const formatDate = (date: Date) => {
    const month = date.getMonth() + 1
    const day = date.getDate()
    return `${month}/${day}`
  }

  return `${formatDate(start)} ~ ${formatDate(end)}`
}

export function PromotionListItem({
  promotion,
  channel,
  isSelected = false,
  onSelect,
  onDuplicate,
  onDelete,
}: PromotionListItemProps) {
  const discountLabel = DISCOUNT_TYPE_LABELS[promotion.discountType]

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-4 hover:shadow-sm transition-shadow">
      <div className="flex items-start gap-3">
        {/* Checkbox */}
        {onSelect && (
          <input
            type="checkbox"
            checked={isSelected}
            onChange={(e) => onSelect(promotion.id, e.target.checked)}
            className="mt-1 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
          />
        )}

        {/* Main content */}
        <div className="flex-1 min-w-0">
          {/* Header row */}
          <div className="flex items-start justify-between gap-2">
            <Link
              href={`/promotions/${promotion.id}`}
              className="font-medium text-gray-900 hover:text-primary-600 line-clamp-1"
            >
              {promotion.title}
            </Link>
            <PromotionActions
              promotionId={promotion.id}
              onDuplicate={onDuplicate}
              onDelete={onDelete}
            />
          </div>

          {/* Channel and status */}
          <div className="flex items-center gap-2 mt-2">
            {channel && (
              <span className="flex items-center gap-1.5 text-sm text-gray-600">
                <span className="w-2 h-2 rounded-full" style={{ backgroundColor: channel.color }} />
                {channel.name}
              </span>
            )}
            <span className="text-gray-300">|</span>
            <PromotionStatusBadge status={promotion.status} />
          </div>

          {/* Date and discount */}
          <div className="flex items-center gap-4 mt-3 text-sm text-gray-500">
            <span className="flex items-center gap-1.5">
              <Calendar size={14} />
              {formatDateRange(promotion.startDate, promotion.endDate)}
            </span>
            <span className="flex items-center gap-1.5">
              <Tag size={14} />
              {discountLabel}: {promotion.discountValue}
            </span>
          </div>

          {/* Description preview */}
          {promotion.description && (
            <p className="mt-2 text-sm text-gray-500 line-clamp-2">
              {promotion.description}
            </p>
          )}
        </div>
      </div>
    </div>
  )
}
