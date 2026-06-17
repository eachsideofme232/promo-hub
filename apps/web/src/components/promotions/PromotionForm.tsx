'use client'

import { useState, useCallback, FormEvent } from 'react'
import { useRouter } from 'next/navigation'
import { Loader2, Save, X } from 'lucide-react'
import type { Promotion, DiscountType } from '@promohub/types'
import { promotionSchema, safeParse } from '@promohub/utils'
import { ChannelSelect, type ChannelOption } from './ChannelSelect'
import { DiscountTypeSelect } from './DiscountTypeSelect'
import { DateRangeInput } from './DateRangeInput'
import { useChannels } from '../providers/ChannelProvider'

interface PromotionFormData {
  title: string
  description: string
  channelId: string
  discountType: DiscountType | ''
  discountValue: string
  startDate: string
  endDate: string
  memo: string
}

interface PromotionFormProps {
  mode: 'create' | 'edit'
  promotion?: Promotion
  teamId: string
  onSubmit?: (data: PromotionFormData) => Promise<void>
  onCancel?: () => void
  isLoading?: boolean
}

const initialFormData: PromotionFormData = {
  title: '',
  description: '',
  channelId: '',
  discountType: '',
  discountValue: '',
  startDate: '',
  endDate: '',
  memo: '',
}

export function PromotionForm({
  mode,
  promotion,
  teamId,
  onSubmit,
  onCancel,
  isLoading = false,
}: PromotionFormProps) {
  const router = useRouter()

  // Channels sourced from the database via ChannelProvider (single source of truth)
  const { channels } = useChannels()
  const channelOptions: ChannelOption[] = channels.map((ch) => ({
    id: ch.id,
    name: ch.name,
    slug: ch.slug,
    color: ch.color,
  }))

  // Initialize form data from promotion if editing
  const [formData, setFormData] = useState<PromotionFormData>(() => {
    if (promotion) {
      return {
        title: promotion.title,
        description: promotion.description || '',
        channelId: promotion.channelId,
        discountType: promotion.discountType,
        discountValue: promotion.discountValue,
        startDate: promotion.startDate.split('T')[0], // Handle ISO date strings
        endDate: promotion.endDate.split('T')[0],
        memo: promotion.memo || '',
      }
    }
    return initialFormData
  })

  const [errors, setErrors] = useState<Record<string, string>>({})
  const [submitting, setSubmitting] = useState(false)

  // Update form field
  const updateField = useCallback(
    <K extends keyof PromotionFormData>(field: K, value: PromotionFormData[K]) => {
      setFormData((prev) => ({ ...prev, [field]: value }))
      // Clear error when field is updated
      if (errors[field]) {
        setErrors((prev) => {
          const next = { ...prev }
          delete next[field]
          return next
        })
      }
    },
    [errors]
  )

  // Handle form submission
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()

    // Validate form data
    const dataToValidate = {
      ...formData,
      teamId,
      discountType: formData.discountType || undefined,
    }

    const result = safeParse(promotionSchema, dataToValidate)

    if (!result.success) {
      setErrors(result.errors || {})
      return
    }

    setSubmitting(true)
    setErrors({})

    try {
      if (onSubmit) {
        await onSubmit(formData)
      } else {
        // Default API submission
        const endpoint =
          mode === 'create'
            ? '/api/promotions'
            : `/api/promotions/${promotion?.id}`

        const response = await fetch(endpoint, {
          method: mode === 'create' ? 'POST' : 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            ...formData,
            teamId,
          }),
        })

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}))
          throw new Error(errorData.message || '저장에 실패했습니다')
        }

        router.push('/promotions')
        router.refresh()
      }
    } catch (error) {
      setErrors({
        submit:
          error instanceof Error
            ? error.message
            : '저장 중 오류가 발생했습니다 (An error occurred)',
      })
    } finally {
      setSubmitting(false)
    }
  }

  // Handle cancel
  const handleCancel = () => {
    if (onCancel) {
      onCancel()
    } else {
      router.back()
    }
  }

  const isDisabled = isLoading || submitting

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Title */}
      <div className="space-y-1">
        <label
          htmlFor="title"
          className="block text-sm font-medium text-gray-700"
        >
          프로모션명 (Title)
          <span className="text-red-500 ml-1">*</span>
        </label>
        <input
          id="title"
          type="text"
          value={formData.title}
          onChange={(e) => updateField('title', e.target.value)}
          disabled={isDisabled}
          placeholder="예: 올리브영 2월 뷰티 페스타"
          className={`
            w-full px-4 py-2.5 border rounded-lg
            focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent
            disabled:bg-gray-100 disabled:cursor-not-allowed
            ${errors.title ? 'border-red-500 focus:ring-red-500' : 'border-gray-300'}
          `}
        />
        {errors.title && <p className="text-sm text-red-500">{errors.title}</p>}
      </div>

      {/* Description */}
      <div className="space-y-1">
        <label
          htmlFor="description"
          className="block text-sm font-medium text-gray-700"
        >
          설명 (Description)
        </label>
        <textarea
          id="description"
          value={formData.description}
          onChange={(e) => updateField('description', e.target.value)}
          disabled={isDisabled}
          placeholder="프로모션에 대한 상세 설명을 입력하세요"
          rows={3}
          className={`
            w-full px-4 py-2.5 border rounded-lg resize-none
            focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent
            disabled:bg-gray-100 disabled:cursor-not-allowed
            ${errors.description ? 'border-red-500 focus:ring-red-500' : 'border-gray-300'}
          `}
        />
        {errors.description && (
          <p className="text-sm text-red-500">{errors.description}</p>
        )}
      </div>

      {/* Channel */}
      <ChannelSelect
        value={formData.channelId}
        onChange={(value) => updateField('channelId', value)}
        channels={channelOptions.length > 0 ? channelOptions : undefined}
        error={errors.channelId}
        disabled={isDisabled}
        required
      />

      {/* Discount Type and Value */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <DiscountTypeSelect
          value={formData.discountType as DiscountType | undefined}
          onChange={(value) => updateField('discountType', value)}
          error={errors.discountType}
          disabled={isDisabled}
          required
        />

        <div className="space-y-1">
          <label
            htmlFor="discountValue"
            className="block text-sm font-medium text-gray-700"
          >
            할인 값 (Discount Value)
            <span className="text-red-500 ml-1">*</span>
          </label>
          <input
            id="discountValue"
            type="text"
            value={formData.discountValue}
            onChange={(e) => updateField('discountValue', e.target.value)}
            disabled={isDisabled}
            placeholder="예: 30%, 5000원, 1+1"
            className={`
              w-full px-4 py-2.5 border rounded-lg
              focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent
              disabled:bg-gray-100 disabled:cursor-not-allowed
              ${errors.discountValue ? 'border-red-500 focus:ring-red-500' : 'border-gray-300'}
            `}
          />
          {errors.discountValue && (
            <p className="text-sm text-red-500">{errors.discountValue}</p>
          )}
        </div>
      </div>

      {/* Date Range */}
      <DateRangeInput
        startDate={formData.startDate}
        endDate={formData.endDate}
        onStartDateChange={(value) => updateField('startDate', value)}
        onEndDateChange={(value) => updateField('endDate', value)}
        startError={errors.startDate}
        endError={errors.endDate}
        disabled={isDisabled}
        required
      />

      {/* Memo */}
      <div className="space-y-1">
        <label
          htmlFor="memo"
          className="block text-sm font-medium text-gray-700"
        >
          메모 (Memo)
        </label>
        <textarea
          id="memo"
          value={formData.memo}
          onChange={(e) => updateField('memo', e.target.value)}
          disabled={isDisabled}
          placeholder="내부 참고용 메모를 입력하세요"
          rows={2}
          className={`
            w-full px-4 py-2.5 border rounded-lg resize-none
            focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent
            disabled:bg-gray-100 disabled:cursor-not-allowed
            ${errors.memo ? 'border-red-500 focus:ring-red-500' : 'border-gray-300'}
          `}
        />
        {errors.memo && <p className="text-sm text-red-500">{errors.memo}</p>}
      </div>

      {/* Submit Error */}
      {errors.submit && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-600">{errors.submit}</p>
        </div>
      )}

      {/* Actions */}
      <div className="flex items-center justify-end gap-3 pt-4 border-t border-gray-200">
        <button
          type="button"
          onClick={handleCancel}
          disabled={isDisabled}
          className="flex items-center gap-2 px-4 py-2.5 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <X size={18} />
          취소 (Cancel)
        </button>
        <button
          type="submit"
          disabled={isDisabled}
          className="flex items-center gap-2 px-6 py-2.5 text-white bg-primary-600 rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {submitting ? (
            <>
              <Loader2 size={18} className="animate-spin" />
              저장 중...
            </>
          ) : (
            <>
              <Save size={18} />
              {mode === 'create' ? '생성 (Create)' : '저장 (Save)'}
            </>
          )}
        </button>
      </div>
    </form>
  )
}
