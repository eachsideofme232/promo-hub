'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { ArrowLeft, Loader2 } from 'lucide-react'
import type { Promotion } from '@promohub/types'
import { PromotionForm } from '@/components/promotions'

interface PageProps {
  params: { id: string }
}

export default function EditPromotionPage({ params }: PageProps) {
  const promotionId = params.id
  const [promotion, setPromotion] = useState<Promotion | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Fetch promotion data
  useEffect(() => {
    let cancelled = false

    const fetchPromotion = async () => {
      setLoading(true)
      setError(null)

      try {
        const response = await fetch(`/api/promotions/${promotionId}`)
        const payload = await response.json().catch(() => ({}))

        if (!response.ok) {
          throw new Error(
            typeof payload.error === 'string'
              ? payload.error
              : '프로모션을 불러오는데 실패했습니다 (Failed to load promotion)'
          )
        }

        if (!cancelled) {
          setPromotion(payload.data ?? null)
        }
      } catch (err) {
        if (!cancelled) {
          setError(
            err instanceof Error
              ? err.message
              : '프로모션을 불러오는데 실패했습니다 (Failed to load promotion)'
          )
        }
      } finally {
        if (!cancelled) {
          setLoading(false)
        }
      }
    }

    fetchPromotion()
    return () => {
      cancelled = true
    }
  }, [promotionId])

  if (loading) {
    return (
      <div className="h-full flex flex-col">
        <header className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center gap-4">
            <Link
              href="/promotions"
              className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
              aria-label="Back to promotions"
            >
              <ArrowLeft size={20} />
            </Link>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                프로모션 수정
              </h1>
              <p className="text-sm text-gray-500">Loading...</p>
            </div>
          </div>
        </header>
        <div className="flex-1 flex items-center justify-center">
          <Loader2 size={32} className="animate-spin text-primary-600" />
        </div>
      </div>
    )
  }

  if (error || !promotion) {
    return (
      <div className="h-full flex flex-col">
        <header className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center gap-4">
            <Link
              href="/promotions"
              className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
              aria-label="Back to promotions"
            >
              <ArrowLeft size={20} />
            </Link>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">오류</h1>
              <p className="text-sm text-gray-500">Error</p>
            </div>
          </div>
        </header>
        <div className="flex-1 flex items-center justify-center p-6">
          <div className="max-w-md text-center">
            <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-600">{error || '프로모션을 찾을 수 없습니다'}</p>
            </div>
            <Link
              href="/promotions"
              className="inline-block mt-4 text-primary-600 hover:text-primary-700"
            >
              프로모션 목록으로 돌아가기
            </Link>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center gap-4">
          <Link
            href="/promotions"
            className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
            aria-label="Back to promotions"
          >
            <ArrowLeft size={20} />
          </Link>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              프로모션 수정
            </h1>
            <p className="text-sm text-gray-500">
              Edit promotion: {promotion.title}
            </p>
          </div>
        </div>
      </header>

      {/* Form Content */}
      <div className="flex-1 p-6 overflow-auto bg-gray-50">
        <div className="max-w-2xl mx-auto">
          <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
            <PromotionForm
              mode="edit"
              promotion={promotion}
              teamId={promotion.teamId}
            />
          </div>

          {/* Metadata */}
          <div className="mt-6 p-4 bg-gray-100 border border-gray-200 rounded-lg">
            <h3 className="text-sm font-medium text-gray-700 mb-2">
              프로모션 정보 (Info)
            </h3>
            <div className="text-xs text-gray-500 space-y-1">
              <p>ID: {promotion.id}</p>
              <p>
                생성일: {new Date(promotion.createdAt).toLocaleDateString('ko-KR')}
              </p>
              <p>
                수정일: {new Date(promotion.updatedAt).toLocaleDateString('ko-KR')}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
