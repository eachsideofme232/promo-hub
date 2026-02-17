'use client'

import { useEffect } from 'react'
import { useTranslations } from 'next-intl'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { X } from 'lucide-react'
import type { Channel } from './ChannelList'

const channelFormSchema = z.object({
  name: z.string().min(1, '채널명을 입력해주세요').max(50, '채널명은 50자 이하여야 합니다'),
  slug: z.string().min(1, '슬러그를 입력해주세요').max(50, '슬러그는 50자 이하여야 합니다').regex(/^[a-z0-9-]+$/, '영문 소문자, 숫자, 하이픈만 사용 가능합니다'),
  color: z.string().regex(/^#[0-9A-Fa-f]{6}$/, '올바른 색상 코드를 입력해주세요'),
})

export type ChannelFormData = z.infer<typeof channelFormSchema>

interface ChannelFormProps {
  channel?: Channel | null
  onSubmit: (data: ChannelFormData) => Promise<void>
  onCancel: () => void
  isSubmitting?: boolean
}

// Generate slug from name: lowercase, replace spaces/special chars with hyphens
function generateSlug(name: string): string {
  return name
    .toLowerCase()
    .replace(/[가-힣]/g, '') // Remove Korean characters
    .replace(/[^a-z0-9\s-]/g, '') // Remove special chars except spaces and hyphens
    .replace(/\s+/g, '-') // Replace spaces with hyphens
    .replace(/-+/g, '-') // Remove consecutive hyphens
    .replace(/^-|-$/g, '') // Remove leading/trailing hyphens
}

// Default colors for new channels
const DEFAULT_COLORS = [
  '#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6',
  '#EC4899', '#06B6D4', '#84CC16', '#F97316', '#6366F1',
]

export function ChannelForm({ channel, onSubmit, onCancel, isSubmitting = false }: ChannelFormProps) {
  const t = useTranslations('channels')
  const isEditMode = !!channel

  const {
    register,
    handleSubmit,
    watch,
    setValue,
    formState: { errors },
  } = useForm<ChannelFormData>({
    resolver: zodResolver(channelFormSchema),
    defaultValues: {
      name: channel?.name ?? '',
      slug: channel?.slug ?? '',
      color: channel?.color ?? DEFAULT_COLORS[Math.floor(Math.random() * DEFAULT_COLORS.length)],
    },
  })

  // Auto-generate slug from name (only in create mode, and only if user hasn't manually edited slug)
  const nameValue = watch('name')
  const slugValue = watch('slug')

  useEffect(() => {
    if (!isEditMode && nameValue) {
      const generatedSlug = generateSlug(nameValue)
      // Only auto-update if the slug matches what would be auto-generated from the previous name
      // or if the slug is empty
      if (!slugValue || slugValue === generateSlug(nameValue.slice(0, -1)) || slugValue === generateSlug(nameValue)) {
        setValue('slug', generatedSlug)
      }
    }
  }, [nameValue, isEditMode, setValue, slugValue])

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-end bg-black/50">
      <div className="h-full w-full max-w-md bg-white shadow-xl flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">
            {isEditMode ? t('editChannel') : t('addChannel')}
          </h2>
          <button
            onClick={onCancel}
            className="p-1.5 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-md transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit(onSubmit)} className="flex-1 overflow-auto px-6 py-4 space-y-5">
          {/* Name field */}
          <div>
            <label htmlFor="channel-name" className="block text-sm font-medium text-gray-700 mb-1">
              {t('name')} <span className="text-red-500">*</span>
            </label>
            <input
              id="channel-name"
              type="text"
              {...register('name')}
              placeholder="My Custom Channel"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-sky-500 focus:border-sky-500 outline-none transition-colors"
              disabled={isSubmitting}
            />
            {errors.name && (
              <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>
            )}
          </div>

          {/* Slug field */}
          <div>
            <label htmlFor="channel-slug" className="block text-sm font-medium text-gray-700 mb-1">
              {t('slug')} <span className="text-red-500">*</span>
            </label>
            <input
              id="channel-slug"
              type="text"
              {...register('slug')}
              placeholder="my-custom-channel"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm font-mono focus:ring-2 focus:ring-sky-500 focus:border-sky-500 outline-none transition-colors"
              disabled={isSubmitting}
            />
            <p className="mt-1 text-xs text-gray-500">{t('slugHint')}</p>
            {errors.slug && (
              <p className="mt-1 text-sm text-red-600">{errors.slug.message}</p>
            )}
          </div>

          {/* Color field */}
          <div>
            <label htmlFor="channel-color" className="block text-sm font-medium text-gray-700 mb-1">
              {t('color')} <span className="text-red-500">*</span>
            </label>
            <div className="flex items-center gap-3">
              <input
                id="channel-color"
                type="color"
                {...register('color')}
                className="w-10 h-10 rounded-lg border border-gray-300 cursor-pointer p-0.5"
                disabled={isSubmitting}
              />
              <input
                type="text"
                value={watch('color')}
                onChange={(e) => setValue('color', e.target.value)}
                placeholder="#3B82F6"
                className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm font-mono focus:ring-2 focus:ring-sky-500 focus:border-sky-500 outline-none transition-colors"
                disabled={isSubmitting}
              />
            </div>
            {errors.color && (
              <p className="mt-1 text-sm text-red-600">{errors.color.message}</p>
            )}
          </div>

          {/* Quick color picker */}
          <div>
            <p className="text-xs text-gray-500 mb-2">빠른 색상 선택</p>
            <div className="flex flex-wrap gap-2">
              {DEFAULT_COLORS.map((color) => (
                <button
                  key={color}
                  type="button"
                  onClick={() => setValue('color', color)}
                  className="w-7 h-7 rounded-full border-2 transition-transform hover:scale-110"
                  style={{
                    backgroundColor: color,
                    borderColor: watch('color') === color ? '#1e293b' : 'transparent',
                  }}
                  title={color}
                  disabled={isSubmitting}
                />
              ))}
            </div>
          </div>
        </form>

        {/* Footer */}
        <div className="flex items-center justify-end gap-3 px-6 py-4 border-t border-gray-200 bg-gray-50">
          <button
            type="button"
            onClick={onCancel}
            disabled={isSubmitting}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50"
          >
            {t('cancel')}
          </button>
          <button
            type="button"
            disabled={isSubmitting}
            className="px-4 py-2 text-sm font-medium text-white bg-sky-500 rounded-lg hover:bg-sky-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            onClick={handleSubmit(onSubmit)}
          >
            {isSubmitting ? (
              <span className="flex items-center gap-2">
                <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                {t('save')}
              </span>
            ) : (
              isEditMode ? t('editChannel') : t('addChannel')
            )}
          </button>
        </div>
      </div>
    </div>
  )
}
