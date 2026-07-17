'use client'

import { useState, useCallback, useEffect, useMemo } from 'react'
import Link from 'next/link'
import { Plus, Loader2 } from 'lucide-react'
import { toast } from 'sonner'
import type { Promotion } from '@promohub/types'
import { PromotionList } from '@/components/promotions'
import { useFilters } from '@/components/filters'

async function readErrorMessage(response: Response, fallback: string) {
  const payload = await response.json().catch(() => ({}))
  return typeof payload.error === 'string' ? payload.error : fallback
}

export default function PromotionsPage() {
  const [promotions, setPromotions] = useState<Promotion[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const { availableChannels } = useFilters()

  const channels = useMemo(
    () =>
      availableChannels.map((channel) => ({
        id: channel.id,
        name: channel.name,
        color: channel.color,
      })),
    [availableChannels]
  )

  const channelNameById = useMemo(() => {
    const map = new Map<string, string>()
    for (const channel of availableChannels) {
      map.set(channel.id, channel.name)
    }
    return map
  }, [availableChannels])

  const fetchPromotions = useCallback(async () => {
    setError(null)
    try {
      const response = await fetch('/api/promotions?limit=100')
      if (!response.ok) {
        throw new Error(await readErrorMessage(response, '프로모션을 불러오지 못했습니다'))
      }
      const payload = await response.json()
      setPromotions(payload.data ?? [])
    } catch (err) {
      setError(err instanceof Error ? err.message : '프로모션을 불러오지 못했습니다')
    } finally {
      setIsLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchPromotions()
  }, [fetchPromotions])

  const handleDuplicate = useCallback(
    async (id: string) => {
      const original = promotions.find((p) => p.id === id)
      if (!original) return

      try {
        const response = await fetch('/api/promotions', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            title: `${original.title} (복사본)`,
            description: original.description ?? '',
            channelId: original.channelId,
            status: 'planned',
            discountType: original.discountType,
            discountValue: original.discountValue,
            startDate: original.startDate,
            endDate: original.endDate,
            memo: original.memo ?? '',
          }),
        })
        if (!response.ok) {
          throw new Error(await readErrorMessage(response, '복제에 실패했습니다'))
        }
        toast.success('프로모션이 복제되었습니다')
        await fetchPromotions()
      } catch (err) {
        toast.error(err instanceof Error ? err.message : '복제에 실패했습니다')
      }
    },
    [promotions, fetchPromotions]
  )

  const handleDelete = useCallback(
    async (id: string) => {
      try {
        const response = await fetch(`/api/promotions/${id}`, { method: 'DELETE' })
        if (!response.ok) {
          throw new Error(await readErrorMessage(response, '삭제에 실패했습니다'))
        }
        toast.success('프로모션이 삭제되었습니다')
        setPromotions((prev) => prev.filter((p) => p.id !== id))
      } catch (err) {
        toast.error(err instanceof Error ? err.message : '삭제에 실패했습니다')
      }
    },
    []
  )

  const handleBulkDelete = useCallback(
    async (ids: string[]) => {
      const results = await Promise.allSettled(
        ids.map((id) => fetch(`/api/promotions/${id}`, { method: 'DELETE' }))
      )
      const failed = results.filter(
        (r) => r.status === 'rejected' || !r.value.ok
      ).length

      if (failed > 0) {
        toast.error(`${failed}건 삭제에 실패했습니다`)
      } else {
        toast.success(`${ids.length}건이 삭제되었습니다`)
      }
      await fetchPromotions()
    },
    [fetchPromotions]
  )

  const handleBulkExport = useCallback(
    (ids: string[]) => {
      const selectedPromotions = promotions.filter((p) => ids.includes(p.id))
      const csvContent = generateCSV(selectedPromotions, channelNameById)
      downloadCSV(csvContent, 'promotions-export.csv')
    },
    [promotions, channelNameById]
  )

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">프로모션 관리</h1>
            <p className="text-sm text-gray-500">
              모든 프로모션을 한 곳에서 관리하세요
            </p>
          </div>

          <Link
            href="/promotions/new"
            className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            <Plus size={20} />
            새 프로모션
          </Link>
        </div>
      </header>

      {/* Content */}
      <div className="flex-1 p-6 overflow-auto bg-gray-50">
        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-sm text-red-600">{error}</p>
          </div>
        )}
        {isLoading ? (
          <div className="flex items-center justify-center py-24">
            <Loader2 size={32} className="animate-spin text-primary-600" />
          </div>
        ) : (
          <PromotionList
            promotions={promotions}
            channels={channels}
            onDuplicate={handleDuplicate}
            onDelete={handleDelete}
            onBulkDelete={handleBulkDelete}
            onBulkExport={handleBulkExport}
          />
        )}
      </div>
    </div>
  )
}

// Helper functions for CSV export
function generateCSV(
  promotions: Promotion[],
  channelNameById: Map<string, string>
): string {
  const headers = [
    '제목',
    '채널',
    '상태',
    '할인 유형',
    '할인 값',
    '시작일',
    '종료일',
    '설명',
  ]

  const statusMap: Record<string, string> = {
    planned: '예정',
    active: '진행중',
    ended: '종료',
    cancelled: '취소',
  }

  const discountTypeMap: Record<string, string> = {
    percentage: '할인율',
    bogo: 'BOGO',
    coupon: '쿠폰',
    gift: '사은품',
    bundle: '번들',
  }

  const rows = promotions.map((promo) => [
    promo.title,
    channelNameById.get(promo.channelId) || promo.channelId,
    statusMap[promo.status] || promo.status,
    discountTypeMap[promo.discountType] || promo.discountType,
    promo.discountValue,
    promo.startDate,
    promo.endDate,
    promo.description || '',
  ])

  const escapeCSV = (value: string) => {
    if (value.includes(',') || value.includes('"') || value.includes('\n')) {
      return `"${value.replace(/"/g, '""')}"`
    }
    return value
  }

  const csvRows = [
    headers.join(','),
    ...rows.map((row) => row.map(escapeCSV).join(',')),
  ]

  return '\uFEFF' + csvRows.join('\n') // Add BOM for Excel Korean support
}

function downloadCSV(content: string, filename: string): void {
  const blob = new Blob([content], { type: 'text/csv;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}
