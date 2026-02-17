'use client'

import { useCallback, useEffect, useState } from 'react'
import { useTranslations } from 'next-intl'
import { Plus, Loader2 } from 'lucide-react'
import { toast } from 'sonner'
import { useTeam } from '@/components/providers/TeamProvider'
import { ProductList, ProductForm } from '@/components/products'
import type { Product, Channel } from '@/components/products'
import type { ProductFormData } from '@promohub/utils'

export default function ProductsPage() {
  const t = useTranslations('products')
  const { teamId, isLoading: isTeamLoading } = useTeam()

  const [products, setProducts] = useState<Product[]>([])
  const [channels, setChannels] = useState<Channel[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editingProduct, setEditingProduct] = useState<Product | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  // Fetch products from API
  const fetchProducts = useCallback(async () => {
    try {
      const res = await fetch('/api/products')
      if (!res.ok) {
        throw new Error('Failed to fetch products')
      }
      const json = await res.json()
      setProducts(json.data ?? [])
    } catch {
      toast.error(t('loadError'))
    }
  }, [t])

  // Fetch channels from API (needed for form and list)
  const fetchChannels = useCallback(async () => {
    try {
      const res = await fetch('/api/channels')
      if (!res.ok) {
        throw new Error('Failed to fetch channels')
      }
      const json = await res.json()
      setChannels(json.data ?? [])
    } catch {
      // Channels are supplementary; products page still works without them
      console.warn('Failed to fetch channels')
    }
  }, [])

  // Load data when team is ready
  useEffect(() => {
    if (!isTeamLoading && teamId) {
      setIsLoading(true)
      Promise.all([fetchProducts(), fetchChannels()]).finally(() => {
        setIsLoading(false)
      })
    }
  }, [isTeamLoading, teamId, fetchProducts, fetchChannels])

  // Handle create product
  const handleCreate = async (data: ProductFormData) => {
    setIsSubmitting(true)
    try {
      const res = await fetch('/api/products', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      })

      if (!res.ok) {
        const errorJson = await res.json().catch(() => null)
        throw new Error(errorJson?.error ?? 'Failed to create product')
      }

      toast.success(t('createSuccess'))
      setShowForm(false)
      await fetchProducts()
    } catch (err) {
      toast.error(t('createError'))
      console.error('Product create error:', err)
    } finally {
      setIsSubmitting(false)
    }
  }

  // Handle update product
  const handleUpdate = async (data: ProductFormData) => {
    if (!editingProduct) return

    setIsSubmitting(true)
    try {
      const res = await fetch(`/api/products/${editingProduct.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      })

      if (!res.ok) {
        const errorJson = await res.json().catch(() => null)
        throw new Error(errorJson?.error ?? 'Failed to update product')
      }

      toast.success(t('updateSuccess'))
      setEditingProduct(null)
      setShowForm(false)
      await fetchProducts()
    } catch (err) {
      toast.error(t('updateError'))
      console.error('Product update error:', err)
    } finally {
      setIsSubmitting(false)
    }
  }

  // Handle delete product
  const handleDelete = async (product: Product) => {
    try {
      const res = await fetch(`/api/products/${product.id}`, {
        method: 'DELETE',
      })

      if (!res.ok) {
        throw new Error('Failed to delete product')
      }

      toast.success(t('deleteSuccess'))
      await fetchProducts()
    } catch (err) {
      toast.error(t('deleteError'))
      console.error('Product delete error:', err)
    }
  }

  // Handle form submission (routes to create or update)
  const handleSubmit = async (data: ProductFormData) => {
    if (editingProduct) {
      await handleUpdate(data)
    } else {
      await handleCreate(data)
    }
  }

  // Open form for editing
  const handleEditClick = (product: Product) => {
    setEditingProduct(product)
    setShowForm(true)
  }

  // Close form
  const handleFormCancel = () => {
    setShowForm(false)
    setEditingProduct(null)
  }

  // Loading state while team is loading
  if (isTeamLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-6 h-6 text-sky-500 animate-spin" />
      </div>
    )
  }

  return (
    <div className="p-6 max-w-6xl mx-auto">
      {/* Page header */}
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900">{t('title')}</h1>
        <button
          onClick={() => {
            setEditingProduct(null)
            setShowForm(true)
          }}
          className="inline-flex items-center gap-2 bg-sky-500 hover:bg-sky-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
        >
          <Plus className="w-4 h-4" />
          {t('addProduct')}
        </button>
      </div>

      {/* Stats summary */}
      {!isLoading && (
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-4">
            <p className="text-sm text-gray-500">{t('totalProducts')}</p>
            <p className="text-2xl font-bold text-gray-900">{products.length}</p>
          </div>
          <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-4">
            <p className="text-sm text-gray-500">{t('active')}</p>
            <p className="text-2xl font-bold text-gray-900">
              {products.filter((p) => p.isActive).length}
            </p>
          </div>
          <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-4">
            <p className="text-sm text-gray-500">{t('inactive')}</p>
            <p className="text-2xl font-bold text-gray-900">
              {products.filter((p) => !p.isActive).length}
            </p>
          </div>
        </div>
      )}

      {/* Product list */}
      {isLoading ? (
        <div className="flex items-center justify-center h-64">
          <Loader2 className="w-6 h-6 text-sky-500 animate-spin" />
        </div>
      ) : (
        <ProductList
          products={products}
          channels={channels}
          onEdit={handleEditClick}
          onDelete={handleDelete}
        />
      )}

      {/* Form slide-over */}
      {showForm && (
        <ProductForm
          product={editingProduct}
          channels={channels}
          onSubmit={handleSubmit}
          onCancel={handleFormCancel}
          isSubmitting={isSubmitting}
        />
      )}
    </div>
  )
}
