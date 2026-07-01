'use client'

import Link from 'next/link'
import { Calendar, Tag } from 'lucide-react'
import type { Promotion, DiscountType } from '@promohub/types'
import { PromotionStatusBadge } from './PromotionStatusBadge'
import { PromotionActionButtons } from './PromotionActions'
import { SortableHeader, type SortConfig, type SortField } from './PromotionSort'

interface Channel {
  id: string
  name: string
  color: string
}

interface PromotionTableProps {
  promotions: Promotion[]
  channels: Channel[]
  selectedIds: Set<string>
  onSelectAll: (selected: boolean) => void
  onSelectOne: (id: string, selected: boolean) => void
  sortConfig: SortConfig
  onSort: (field: SortField) => void
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
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    return `${year}-${month}-${day}`
  }

  return `${formatDate(start)} ~ ${formatDate(end)}`
}

export function PromotionTable({
  promotions,
  channels,
  selectedIds,
  onSelectAll,
  onSelectOne,
  sortConfig,
  onSort,
  onDuplicate,
  onDelete,
}: PromotionTableProps) {
  const allSelected =
    promotions.length > 0 && promotions.every((p) => selectedIds.has(p.id))
  const someSelected = promotions.some((p) => selectedIds.has(p.id))

  const getChannel = (channelId: string) =>
    channels.find((c) => c.id === channelId)

  return (
    <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-200 bg-gray-50">
              {/* Checkbox column */}
              <th className="px-4 py-3 text-left w-12">
                <input
                  type="checkbox"
                  checked={allSelected}
                  ref={(el) => {
                    if (el) {
                      el.indeterminate = someSelected && !allSelected
                    }
                  }}
                  onChange={(e) => onSelectAll(e.target.checked)}
                  className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                />
              </th>
              {/* Title column */}
              <th className="px-4 py-3 text-left">
                <SortableHeader
                  field="title"
                  label="프로모션"
                  sortConfig={sortConfig}
                  onSort={onSort}
                />
              </th>
              {/* Channel column */}
              <th className="px-4 py-3 text-left">
                <SortableHeader
                  field="channel"
                  label="채널"
                  sortConfig={sortConfig}
                  onSort={onSort}
                />
              </th>
              {/* Date column */}
              <th className="px-4 py-3 text-left">
                <SortableHeader
                  field="startDate"
                  label="기간"
                  sortConfig={sortConfig}
                  onSort={onSort}
                />
              </th>
              {/* Discount column */}
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                할인
              </th>
              {/* Status column */}
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                상태
              </th>
              {/* Actions column */}
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                작업
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {promotions.map((promotion) => {
              const channel = getChannel(promotion.channelId)
              const isSelected = selectedIds.has(promotion.id)

              return (
                <tr
                  key={promotion.id}
                  className={`hover:bg-gray-50 transition-colors ${
                    isSelected ? 'bg-primary-50' : ''
                  }`}
                >
                  {/* Checkbox */}
                  <td className="px-4 py-4">
                    <input
                      type="checkbox"
                      checked={isSelected}
                      onChange={(e) =>
                        onSelectOne(promotion.id, e.target.checked)
                      }
                      className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                    />
                  </td>
                  {/* Title */}
                  <td className="px-4 py-4">
                    <Link
                      href={`/promotions/${promotion.id}`}
                      className="font-medium text-gray-900 hover:text-primary-600"
                    >
                      {promotion.title}
                    </Link>
                    {promotion.description && (
                      <p className="text-sm text-gray-500 mt-0.5 line-clamp-1">
                        {promotion.description}
                      </p>
                    )}
                  </td>
                  {/* Channel */}
                  <td className="px-4 py-4">
                    {channel && (
                      <span className="flex items-center gap-2">
                        <span
                          className="w-2 h-2 rounded-full"
                          style={{ backgroundColor: channel.color }}
                        />
                        <span className="text-sm text-gray-700">
                          {channel.name}
                        </span>
                      </span>
                    )}
                  </td>
                  {/* Date range */}
                  <td className="px-4 py-4">
                    <span className="flex items-center gap-1.5 text-sm text-gray-600">
                      <Calendar size={14} className="text-gray-400" />
                      {formatDateRange(promotion.startDate, promotion.endDate)}
                    </span>
                  </td>
                  {/* Discount */}
                  <td className="px-4 py-4">
                    <span className="flex items-center gap-1.5 text-sm">
                      <Tag size={14} className="text-gray-400" />
                      <span className="text-gray-600">
                        {DISCOUNT_TYPE_LABELS[promotion.discountType]}:
                      </span>
                      <span className="font-medium text-gray-900">
                        {promotion.discountValue}
                      </span>
                    </span>
                  </td>
                  {/* Status */}
                  <td className="px-4 py-4">
                    <PromotionStatusBadge status={promotion.status} />
                  </td>
                  {/* Actions */}
                  <td className="px-4 py-4">
                    <div className="flex justify-end">
                      <PromotionActionButtons
                        promotionId={promotion.id}
                        onDuplicate={onDuplicate}
                        onDelete={onDelete}
                      />
                    </div>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}
