'use client'

import { useState, useCallback, useMemo } from 'react'
import Link from 'next/link'
import { Plus } from 'lucide-react'
import type { Promotion } from '@promohub/types'
import { PromotionList } from '@/components/promotions'
import { useChannels } from '@/components/filters'

// Seed channel UUIDs (match supabase/seed.sql) so demo data lines up with the
// database-sourced channels until promotions are wired to the API (Phase 4).
const CHANNEL_OLIVEYOUNG = 'c1000000-0000-0000-0000-000000000001'
const CHANNEL_COUPANG = 'c1000000-0000-0000-0000-000000000002'
const CHANNEL_NAVER = 'c1000000-0000-0000-0000-000000000003'
const CHANNEL_KAKAO = 'c1000000-0000-0000-0000-000000000004'
const CHANNEL_MUSINSA = 'c1000000-0000-0000-0000-000000000005'

// Demo promotions data - will be replaced with API calls
const DEMO_PROMOTIONS: Promotion[] = [
  {
    id: '1',
    teamId: 'team-1',
    channelId: CHANNEL_OLIVEYOUNG,
    title: '올리브영 2월 뷰티 페스타',
    description: '2월 한 달간 진행하는 대규모 뷰티 프로모션',
    status: 'active',
    discountType: 'percentage',
    discountValue: '30%',
    startDate: '2026-02-01',
    endDate: '2026-02-14',
    createdAt: '2026-01-15T09:00:00Z',
    updatedAt: '2026-01-20T14:30:00Z',
  },
  {
    id: '2',
    teamId: 'team-1',
    channelId: CHANNEL_COUPANG,
    title: '쿠팡 발렌타인 기획전',
    description: '발렌타인데이 특별 기획전 쿠폰 할인',
    status: 'planned',
    discountType: 'coupon',
    discountValue: '5,000원',
    startDate: '2026-02-10',
    endDate: '2026-02-14',
    createdAt: '2026-01-18T10:00:00Z',
    updatedAt: '2026-01-18T10:00:00Z',
  },
  {
    id: '3',
    teamId: 'team-1',
    channelId: CHANNEL_NAVER,
    title: '네이버 브랜드 위크',
    description: '네이버 쇼핑 브랜드 위크 1+1 프로모션',
    status: 'planned',
    discountType: 'bogo',
    discountValue: '1+1',
    startDate: '2026-02-15',
    endDate: '2026-02-22',
    createdAt: '2026-01-20T11:00:00Z',
    updatedAt: '2026-01-20T11:00:00Z',
  },
  {
    id: '4',
    teamId: 'team-1',
    channelId: CHANNEL_KAKAO,
    title: '카카오 선물하기 기획전',
    description: '카카오 선물하기 단독 기획전',
    status: 'planned',
    discountType: 'gift',
    discountValue: '미니어처 증정',
    startDate: '2026-02-20',
    endDate: '2026-02-28',
    createdAt: '2026-01-22T09:00:00Z',
    updatedAt: '2026-01-22T09:00:00Z',
  },
  {
    id: '5',
    teamId: 'team-1',
    channelId: CHANNEL_MUSINSA,
    title: '무신사 뷰티 페스티벌',
    description: '무신사 뷰티 카테고리 론칭 기념 페스티벌',
    status: 'planned',
    discountType: 'bundle',
    discountValue: '세트 20% 할인',
    startDate: '2026-03-01',
    endDate: '2026-03-15',
    createdAt: '2026-01-25T10:00:00Z',
    updatedAt: '2026-01-25T10:00:00Z',
  },
  {
    id: '6',
    teamId: 'team-1',
    channelId: CHANNEL_OLIVEYOUNG,
    title: '올리브영 1월 세일',
    description: '1월 할인 행사 종료',
    status: 'ended',
    discountType: 'percentage',
    discountValue: '25%',
    startDate: '2026-01-01',
    endDate: '2026-01-15',
    createdAt: '2025-12-20T09:00:00Z',
    updatedAt: '2026-01-16T09:00:00Z',
  },
  {
    id: '7',
    teamId: 'team-1',
    channelId: CHANNEL_COUPANG,
    title: '쿠팡 신년 행사 (취소)',
    description: '일정 변경으로 취소됨',
    status: 'cancelled',
    discountType: 'coupon',
    discountValue: '10,000원',
    startDate: '2026-01-05',
    endDate: '2026-01-10',
    createdAt: '2025-12-28T11:00:00Z',
    updatedAt: '2026-01-03T14:00:00Z',
  },
]

export default function PromotionsPage() {
  const [promotions, setPromotions] = useState<Promotion[]>(DEMO_PROMOTIONS)

  // Channels sourced from the database via ChannelProvider (single source of truth)
  const { channels } = useChannels()
  const channelOptions = useMemo(
    () => channels.map((ch) => ({ id: ch.id, name: ch.name, color: ch.color })),
    [channels]
  )
  const channelNameMap = useMemo(
    () => Object.fromEntries(channels.map((ch) => [ch.id, ch.name])),
    [channels]
  )

  const handleDuplicate = useCallback((id: string) => {
    const originalPromotion = promotions.find((p) => p.id === id)
    if (!originalPromotion) return

    const newPromotion: Promotion = {
      ...originalPromotion,
      id: `${Date.now()}`,
      title: `${originalPromotion.title} (복사본)`,
      status: 'planned',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    }

    setPromotions((prev) => [newPromotion, ...prev])
  }, [promotions])

  const handleDelete = useCallback((id: string) => {
    setPromotions((prev) => prev.filter((p) => p.id !== id))
  }, [])

  const handleBulkDelete = useCallback((ids: string[]) => {
    setPromotions((prev) => prev.filter((p) => !ids.includes(p.id)))
  }, [])

  const handleBulkExport = useCallback((ids: string[]) => {
    const selectedPromotions = promotions.filter((p) => ids.includes(p.id))
    const csvContent = generateCSV(selectedPromotions, channelNameMap)
    downloadCSV(csvContent, 'promotions-export.csv')
  }, [promotions, channelNameMap])

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
        <PromotionList
          promotions={promotions}
          channels={channelOptions}
          onDuplicate={handleDuplicate}
          onDelete={handleDelete}
          onBulkDelete={handleBulkDelete}
          onBulkExport={handleBulkExport}
        />
      </div>
    </div>
  )
}

// Helper functions for CSV export
function generateCSV(
  promotions: Promotion[],
  channelMap: Record<string, string>
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
    channelMap[promo.channelId] || promo.channelId,
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
