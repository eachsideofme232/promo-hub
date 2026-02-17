'use client'

import { useState } from 'react'
import { useTranslations } from 'next-intl'
import { Pencil, Trash2, ChevronDown, ChevronRight } from 'lucide-react'
import { FormattedWon } from '@/components/common/FormattedWon'

export interface ChannelPrice {
  id: string
  channelId: string
  sellingPrice: number
  channelFeeRate: number | null
  isActive: boolean
  notes: string | null
}

export interface Product {
  id: string
  teamId: string
  name: string
  sku: string | null
  barcode: string | null
  brand: string | null
  category: string | null
  description: string | null
  imageUrl: string | null
  basePrice: number | null
  costPrice: number | null
  isActive: boolean
  createdAt: string
  updatedAt: string
  channelPrices: ChannelPrice[]
}

export interface Channel {
  id: string
  name: string
  color: string
  isSystem: boolean
}

interface ProductListProps {
  products: Product[]
  channels: Channel[]
  onEdit: (product: Product) => void
  onDelete: (product: Product) => void
}

export function ProductList({ products, channels, onEdit, onDelete }: ProductListProps) {
  const t = useTranslations('products')
  const [expandedIds, setExpandedIds] = useState<Set<string>>(new Set())
  const [deletingProduct, setDeletingProduct] = useState<Product | null>(null)

  const toggleExpand = (productId: string) => {
    setExpandedIds((prev) => {
      const next = new Set(prev)
      if (next.has(productId)) {
        next.delete(productId)
      } else {
        next.add(productId)
      }
      return next
    })
  }

  const getChannelName = (channelId: string) => {
    return channels.find((ch) => ch.id === channelId)?.name ?? channelId
  }

  const getChannelColor = (channelId: string) => {
    return channels.find((ch) => ch.id === channelId)?.color ?? '#94a3b8'
  }

  const handleDeleteClick = (product: Product) => {
    setDeletingProduct(product)
  }

  const handleDeleteConfirm = () => {
    if (deletingProduct) {
      onDelete(deletingProduct)
      setDeletingProduct(null)
    }
  }

  const handleDeleteCancel = () => {
    setDeletingProduct(null)
  }

  if (products.length === 0) {
    return (
      <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-12 text-center">
        <p className="text-gray-500">{t('noProducts')}</p>
      </div>
    )
  }

  return (
    <>
      {/* Desktop table */}
      <div className="hidden lg:block bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-200 bg-gray-50">
              <th className="w-8 px-3 py-3" />
              <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                {t('name')}
              </th>
              <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                {t('sku')}
              </th>
              <th className="text-right px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                {t('basePrice')}
              </th>
              <th className="text-right px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                {t('costPrice')}
              </th>
              <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                {t('channelCount')}
              </th>
              <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                {t('status')}
              </th>
              <th className="text-right px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                {t('actions')}
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {products.map((product) => {
              const isExpanded = expandedIds.has(product.id)
              return (
                <tr key={product.id} className="group">
                  <td colSpan={8} className="p-0">
                    <div>
                      {/* Main row */}
                      <div className="flex items-center hover:bg-gray-50 transition-colors">
                        <div className="w-8 px-3 py-4 flex items-center justify-center">
                          {product.channelPrices.length > 0 && (
                            <button
                              onClick={() => toggleExpand(product.id)}
                              className="p-0.5 text-gray-400 hover:text-gray-600 rounded"
                            >
                              {isExpanded ? (
                                <ChevronDown className="w-4 h-4" />
                              ) : (
                                <ChevronRight className="w-4 h-4" />
                              )}
                            </button>
                          )}
                        </div>
                        <div className="flex-1 px-6 py-4">
                          <span className="font-medium text-gray-900">{product.name}</span>
                        </div>
                        <div className="px-6 py-4">
                          <code className="text-sm text-gray-600 bg-gray-100 px-2 py-0.5 rounded">
                            {product.sku ?? '-'}
                          </code>
                        </div>
                        <div className="px-6 py-4 text-right text-sm text-gray-900">
                          {product.basePrice != null ? (
                            <FormattedWon value={product.basePrice} />
                          ) : (
                            <span className="text-gray-400">-</span>
                          )}
                        </div>
                        <div className="px-6 py-4 text-right text-sm text-gray-900">
                          {product.costPrice != null ? (
                            <FormattedWon value={product.costPrice} />
                          ) : (
                            <span className="text-gray-400">-</span>
                          )}
                        </div>
                        <div className="px-6 py-4">
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-sky-100 text-sky-700">
                            {product.channelPrices.length}개 채널
                          </span>
                        </div>
                        <div className="px-6 py-4">
                          {product.isActive ? (
                            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-700">
                              {t('active')}
                            </span>
                          ) : (
                            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-600">
                              {t('inactive')}
                            </span>
                          )}
                        </div>
                        <div className="px-6 py-4 text-right">
                          <div className="flex items-center justify-end gap-2">
                            <button
                              onClick={() => onEdit(product)}
                              className="p-1.5 text-gray-500 hover:text-sky-600 hover:bg-sky-50 rounded-md transition-colors"
                              title={t('editProduct')}
                            >
                              <Pencil className="w-4 h-4" />
                            </button>
                            <button
                              onClick={() => handleDeleteClick(product)}
                              className="p-1.5 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-md transition-colors"
                              title={t('deleteProduct')}
                            >
                              <Trash2 className="w-4 h-4" />
                            </button>
                          </div>
                        </div>
                      </div>

                      {/* Expanded channel prices */}
                      {isExpanded && product.channelPrices.length > 0 && (
                        <div className="bg-gray-50 border-t border-gray-100 px-12 py-3">
                          <p className="text-xs font-medium text-gray-500 uppercase mb-2">
                            {t('channelPrices')}
                          </p>
                          <div className="space-y-1.5">
                            {product.channelPrices.map((cp) => (
                              <div
                                key={cp.id}
                                className="flex items-center gap-3 text-sm"
                              >
                                <span
                                  className="w-3 h-3 rounded-full flex-shrink-0"
                                  style={{ backgroundColor: getChannelColor(cp.channelId) }}
                                />
                                <span className="text-gray-700 w-24">
                                  {getChannelName(cp.channelId)}
                                </span>
                                <span className="text-gray-900 font-medium">
                                  <FormattedWon value={cp.sellingPrice} />
                                </span>
                                <span className="text-gray-500 text-xs">
                                  {cp.channelFeeRate != null
                                    ? `${cp.channelFeeRate.toFixed(2)}%`
                                    : '-'}
                                </span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>

      {/* Mobile card layout */}
      <div className="lg:hidden space-y-3">
        {products.map((product) => {
          const isExpanded = expandedIds.has(product.id)
          return (
            <div
              key={product.id}
              className="bg-white rounded-lg border border-gray-200 shadow-sm p-4"
            >
              <div className="flex items-start justify-between">
                <div>
                  <div className="font-medium text-gray-900">{product.name}</div>
                  {product.sku && (
                    <code className="text-xs text-gray-500 bg-gray-100 px-1.5 py-0.5 rounded mt-1 inline-block">
                      {product.sku}
                    </code>
                  )}
                </div>
                <div>
                  {product.isActive ? (
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-700">
                      {t('active')}
                    </span>
                  ) : (
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-600">
                      {t('inactive')}
                    </span>
                  )}
                </div>
              </div>

              <div className="mt-3 grid grid-cols-2 gap-2 text-sm">
                <div>
                  <span className="text-gray-500">{t('basePrice')}: </span>
                  <span className="text-gray-900 font-medium">
                    {product.basePrice != null ? (
                      <FormattedWon value={product.basePrice} />
                    ) : (
                      '-'
                    )}
                  </span>
                </div>
                <div>
                  <span className="text-gray-500">{t('costPrice')}: </span>
                  <span className="text-gray-900 font-medium">
                    {product.costPrice != null ? (
                      <FormattedWon value={product.costPrice} />
                    ) : (
                      '-'
                    )}
                  </span>
                </div>
              </div>

              {/* Channel count badge + expand toggle */}
              {product.channelPrices.length > 0 && (
                <button
                  onClick={() => toggleExpand(product.id)}
                  className="mt-2 flex items-center gap-1 text-sm text-sky-600 hover:text-sky-700"
                >
                  <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-sky-100 text-sky-700">
                    {product.channelPrices.length}개 채널
                  </span>
                  {isExpanded ? (
                    <ChevronDown className="w-3.5 h-3.5" />
                  ) : (
                    <ChevronRight className="w-3.5 h-3.5" />
                  )}
                </button>
              )}

              {/* Expanded channel prices for mobile */}
              {isExpanded && product.channelPrices.length > 0 && (
                <div className="mt-2 bg-gray-50 rounded-md p-3 space-y-1.5">
                  {product.channelPrices.map((cp) => (
                    <div key={cp.id} className="flex items-center justify-between text-sm">
                      <div className="flex items-center gap-2">
                        <span
                          className="w-3 h-3 rounded-full flex-shrink-0"
                          style={{ backgroundColor: getChannelColor(cp.channelId) }}
                        />
                        <span className="text-gray-700">{getChannelName(cp.channelId)}</span>
                      </div>
                      <div className="flex items-center gap-3">
                        <span className="text-gray-900 font-medium">
                          <FormattedWon value={cp.sellingPrice} />
                        </span>
                        <span className="text-gray-500 text-xs">
                          {cp.channelFeeRate != null
                            ? `${cp.channelFeeRate.toFixed(2)}%`
                            : '-'}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* Actions */}
              <div className="mt-3 flex items-center justify-end gap-2 pt-2 border-t border-gray-100">
                <button
                  onClick={() => onEdit(product)}
                  className="p-1.5 text-gray-500 hover:text-sky-600 hover:bg-sky-50 rounded-md transition-colors"
                  title={t('editProduct')}
                >
                  <Pencil className="w-4 h-4" />
                </button>
                <button
                  onClick={() => handleDeleteClick(product)}
                  className="p-1.5 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-md transition-colors"
                  title={t('deleteProduct')}
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          )
        })}
      </div>

      {/* Delete confirmation dialog */}
      {deletingProduct && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
          <div className="bg-white rounded-lg shadow-lg p-6 max-w-sm mx-4 w-full">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              {t('deleteProduct')}
            </h3>
            <p className="text-sm text-gray-600 mb-1">{t('confirmDelete')}</p>
            <p className="text-sm text-gray-500 mb-6">{t('confirmDeleteDesc')}</p>
            <div className="flex justify-end gap-3">
              <button
                onClick={handleDeleteCancel}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
              >
                {t('cancel')}
              </button>
              <button
                onClick={handleDeleteConfirm}
                className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700 transition-colors"
              >
                {t('deleteProduct')}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  )
}
