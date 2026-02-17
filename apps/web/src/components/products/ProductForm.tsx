'use client'

import { useEffect, useState } from 'react'
import { useTranslations } from 'next-intl'
import { useForm, useFieldArray } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { X, Trash2, Plus } from 'lucide-react'
import { productFormSchema, type ProductFormData } from '@promohub/utils'
import type { Product, Channel } from './ProductList'

// Form input type (before Zod defaults are applied)
// This aligns with what the user actually types in the form
type ProductFormInput = {
  name: string
  sku: string
  barcode?: string
  brand?: string
  category?: string
  description?: string
  basePrice: number
  costPrice?: number
  imageUrl?: string
  channelPrices: {
    channelId: string
    sellingPrice: number
    channelFeeRate?: number
    isActive: boolean
  }[]
}

interface ProductFormProps {
  product: Product | null
  channels: Channel[]
  onSubmit: (data: ProductFormData) => void
  onCancel: () => void
  isSubmitting: boolean
}

export function ProductForm({ product, channels, onSubmit, onCancel, isSubmitting }: ProductFormProps) {
  const t = useTranslations('products')
  const isEditMode = !!product

  const {
    register,
    handleSubmit,
    control,
    formState: { errors },
  } = useForm<ProductFormInput>({
    resolver: zodResolver(productFormSchema) as never,
    defaultValues: {
      name: product?.name ?? '',
      sku: product?.sku ?? '',
      barcode: product?.barcode ?? '',
      brand: product?.brand ?? '',
      category: product?.category ?? '',
      description: product?.description ?? '',
      basePrice: product?.basePrice ?? 0,
      costPrice: product?.costPrice ?? undefined,
      imageUrl: product?.imageUrl ?? '',
      channelPrices: product?.channelPrices?.map((cp) => ({
        channelId: cp.channelId,
        sellingPrice: cp.sellingPrice,
        channelFeeRate: cp.channelFeeRate ?? undefined,
        isActive: cp.isActive,
      })) ?? [],
    },
  })

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'channelPrices',
  })

  // Channels not yet added to the field array
  const availableChannels = channels.filter(
    (ch) => !fields.some((f) => f.channelId === ch.id)
  )

  const [showChannelSelect, setShowChannelSelect] = useState(false)

  const handleAddChannel = (channel: Channel) => {
    append({
      channelId: channel.id,
      sellingPrice: 0,
      channelFeeRate: undefined,
      isActive: true,
    })
    setShowChannelSelect(false)
  }

  const getChannelName = (channelId: string) => {
    return channels.find((ch) => ch.id === channelId)?.name ?? channelId
  }

  const getChannelColor = (channelId: string) => {
    return channels.find((ch) => ch.id === channelId)?.color ?? '#94a3b8'
  }

  // Bridge between form input type and the validated output type
  const handleFormSubmit = (data: ProductFormInput) => {
    // After zodResolver validates, the data matches ProductFormData shape
    onSubmit(data as unknown as ProductFormData)
  }

  // Close channel select dropdown when clicking outside
  useEffect(() => {
    if (!showChannelSelect) return
    const handleClick = () => setShowChannelSelect(false)
    document.addEventListener('click', handleClick)
    return () => document.removeEventListener('click', handleClick)
  }, [showChannelSelect])

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-end bg-black/50">
      <div className="h-full w-full max-w-lg bg-white shadow-xl flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">
            {isEditMode ? t('editProduct') : t('addProduct')}
          </h2>
          <button
            onClick={onCancel}
            className="p-1.5 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-md transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form */}
        <form
          onSubmit={handleSubmit(handleFormSubmit)}
          className="flex-1 overflow-auto px-6 py-4 space-y-5"
        >
          {/* Product name */}
          <div>
            <label htmlFor="product-name" className="block text-sm font-medium text-gray-700 mb-1">
              {t('name')} <span className="text-red-500">*</span>
            </label>
            <input
              id="product-name"
              type="text"
              {...register('name')}
              placeholder="상품명을 입력하세요"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-sky-500 focus:border-sky-500 outline-none transition-colors"
              disabled={isSubmitting}
            />
            {errors.name && (
              <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>
            )}
          </div>

          {/* SKU */}
          <div>
            <label htmlFor="product-sku" className="block text-sm font-medium text-gray-700 mb-1">
              {t('sku')} <span className="text-red-500">*</span>
            </label>
            <input
              id="product-sku"
              type="text"
              {...register('sku')}
              placeholder="SKU-001"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm font-mono focus:ring-2 focus:ring-sky-500 focus:border-sky-500 outline-none transition-colors"
              disabled={isSubmitting}
            />
            {errors.sku && (
              <p className="mt-1 text-sm text-red-600">{errors.sku.message}</p>
            )}
          </div>

          {/* Barcode */}
          <div>
            <label htmlFor="product-barcode" className="block text-sm font-medium text-gray-700 mb-1">
              {t('barcode')}
            </label>
            <input
              id="product-barcode"
              type="text"
              {...register('barcode')}
              placeholder="8801234567890"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm font-mono focus:ring-2 focus:ring-sky-500 focus:border-sky-500 outline-none transition-colors"
              disabled={isSubmitting}
            />
            {errors.barcode && (
              <p className="mt-1 text-sm text-red-600">{errors.barcode.message}</p>
            )}
          </div>

          {/* Brand & Category row */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label htmlFor="product-brand" className="block text-sm font-medium text-gray-700 mb-1">
                {t('brand')}
              </label>
              <input
                id="product-brand"
                type="text"
                {...register('brand')}
                placeholder="브랜드명"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-sky-500 focus:border-sky-500 outline-none transition-colors"
                disabled={isSubmitting}
              />
              {errors.brand && (
                <p className="mt-1 text-sm text-red-600">{errors.brand.message}</p>
              )}
            </div>
            <div>
              <label htmlFor="product-category" className="block text-sm font-medium text-gray-700 mb-1">
                {t('category')}
              </label>
              <input
                id="product-category"
                type="text"
                {...register('category')}
                placeholder="카테고리"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-sky-500 focus:border-sky-500 outline-none transition-colors"
                disabled={isSubmitting}
              />
              {errors.category && (
                <p className="mt-1 text-sm text-red-600">{errors.category.message}</p>
              )}
            </div>
          </div>

          {/* Base Price & Cost Price row */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label htmlFor="product-basePrice" className="block text-sm font-medium text-gray-700 mb-1">
                {t('basePrice')} (원) <span className="text-red-500">*</span>
              </label>
              <input
                id="product-basePrice"
                type="number"
                {...register('basePrice', { valueAsNumber: true })}
                placeholder="0"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-sky-500 focus:border-sky-500 outline-none transition-colors"
                disabled={isSubmitting}
              />
              {errors.basePrice && (
                <p className="mt-1 text-sm text-red-600">{errors.basePrice.message}</p>
              )}
            </div>
            <div>
              <label htmlFor="product-costPrice" className="block text-sm font-medium text-gray-700 mb-1">
                {t('costPrice')} (COGS)
              </label>
              <input
                id="product-costPrice"
                type="number"
                {...register('costPrice', { valueAsNumber: true })}
                placeholder="0"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-sky-500 focus:border-sky-500 outline-none transition-colors"
                disabled={isSubmitting}
              />
              {errors.costPrice && (
                <p className="mt-1 text-sm text-red-600">{errors.costPrice.message}</p>
              )}
            </div>
          </div>

          {/* Description */}
          <div>
            <label htmlFor="product-description" className="block text-sm font-medium text-gray-700 mb-1">
              {t('description')}
            </label>
            <textarea
              id="product-description"
              {...register('description')}
              placeholder="상품 설명을 입력하세요"
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-sky-500 focus:border-sky-500 outline-none transition-colors resize-none"
              disabled={isSubmitting}
            />
            {errors.description && (
              <p className="mt-1 text-sm text-red-600">{errors.description.message}</p>
            )}
          </div>

          {/* Image URL */}
          <div>
            <label htmlFor="product-imageUrl" className="block text-sm font-medium text-gray-700 mb-1">
              이미지 URL
            </label>
            <input
              id="product-imageUrl"
              type="text"
              {...register('imageUrl')}
              placeholder="https://example.com/image.jpg"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-sky-500 focus:border-sky-500 outline-none transition-colors"
              disabled={isSubmitting}
            />
            {errors.imageUrl && (
              <p className="mt-1 text-sm text-red-600">{errors.imageUrl.message}</p>
            )}
          </div>

          {/* Channel Prices Section */}
          <div className="border-t border-gray-200 pt-5">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-semibold text-gray-900">
                {t('channelPrices')}
              </h3>
              {availableChannels.length > 0 && (
                <div className="relative">
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation()
                      setShowChannelSelect(!showChannelSelect)
                    }}
                    className="inline-flex items-center gap-1 text-sm text-sky-600 hover:text-sky-700 font-medium"
                    disabled={isSubmitting}
                  >
                    <Plus className="w-4 h-4" />
                    {t('addChannelPrice')}
                  </button>
                  {showChannelSelect && (
                    <div
                      className="absolute right-0 top-8 z-10 w-56 bg-white rounded-lg border border-gray-200 shadow-lg py-1"
                      onClick={(e) => e.stopPropagation()}
                    >
                      <p className="px-3 py-1.5 text-xs text-gray-500 font-medium uppercase">
                        {t('selectChannel')}
                      </p>
                      {availableChannels.map((ch) => (
                        <button
                          key={ch.id}
                          type="button"
                          onClick={() => handleAddChannel(ch)}
                          className="w-full flex items-center gap-2 px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
                        >
                          <span
                            className="w-3 h-3 rounded-full flex-shrink-0"
                            style={{ backgroundColor: ch.color }}
                          />
                          {ch.name}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Channel price rows */}
            {fields.length === 0 ? (
              <p className="text-sm text-gray-400 text-center py-4">
                채널별 가격을 추가하세요
              </p>
            ) : (
              <div className="space-y-3">
                {fields.map((field, index) => (
                  <div
                    key={field.id}
                    className="bg-gray-50 rounded-lg p-3 border border-gray-200"
                  >
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <span
                          className="w-3 h-3 rounded-full flex-shrink-0"
                          style={{ backgroundColor: getChannelColor(field.channelId) }}
                        />
                        <span className="text-sm font-medium text-gray-700">
                          {getChannelName(field.channelId)}
                        </span>
                      </div>
                      <button
                        type="button"
                        onClick={() => remove(index)}
                        className="p-1 text-gray-400 hover:text-red-500 rounded transition-colors"
                        disabled={isSubmitting}
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <label className="block text-xs text-gray-500 mb-1">
                          {t('sellingPrice')}
                        </label>
                        <input
                          type="number"
                          {...register(`channelPrices.${index}.sellingPrice`, {
                            valueAsNumber: true,
                          })}
                          placeholder="판매가"
                          className="w-full px-2.5 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-sky-500 focus:border-sky-500 outline-none transition-colors"
                          disabled={isSubmitting}
                        />
                        {errors.channelPrices?.[index]?.sellingPrice && (
                          <p className="mt-0.5 text-xs text-red-600">
                            {errors.channelPrices[index].sellingPrice?.message}
                          </p>
                        )}
                      </div>
                      <div>
                        <label className="block text-xs text-gray-500 mb-1">
                          {t('channelFeeRate')} (%)
                        </label>
                        <input
                          type="number"
                          step="0.01"
                          {...register(`channelPrices.${index}.channelFeeRate`, {
                            valueAsNumber: true,
                          })}
                          placeholder="수수료율 (%)"
                          className="w-full px-2.5 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-sky-500 focus:border-sky-500 outline-none transition-colors"
                          disabled={isSubmitting}
                        />
                        {errors.channelPrices?.[index]?.channelFeeRate && (
                          <p className="mt-0.5 text-xs text-red-600">
                            {errors.channelPrices[index].channelFeeRate?.message}
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
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
            onClick={handleSubmit(handleFormSubmit)}
          >
            {isSubmitting ? (
              <span className="flex items-center gap-2">
                <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                {t('save')}
              </span>
            ) : (
              isEditMode ? t('editProduct') : t('addProduct')
            )}
          </button>
        </div>
      </div>
    </div>
  )
}
