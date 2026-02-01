'use client'

import Link from 'next/link'
import { Plus, Search, Filter, Calendar, Tag } from 'lucide-react'

const CHANNELS = [
  { id: 'oliveyoung', name: '올리브영', color: 'bg-green-500' },
  { id: 'coupang', name: '쿠팡', color: 'bg-red-500' },
  { id: 'naver', name: '네이버', color: 'bg-green-600' },
  { id: 'kakao', name: '카카오', color: 'bg-yellow-500' },
  { id: 'musinsa', name: '무신사', color: 'bg-black' },
]

const STATUS_LABELS = {
  planned: { label: '예정', color: 'bg-blue-100 text-blue-700' },
  active: { label: '진행중', color: 'bg-green-100 text-green-700' },
  ended: { label: '종료', color: 'bg-gray-100 text-gray-700' },
  cancelled: { label: '취소', color: 'bg-red-100 text-red-700' },
}

// Demo promotions
const DEMO_PROMOTIONS = [
  {
    id: '1',
    title: '올리브영 2월 뷰티 페스타',
    channel: 'oliveyoung',
    status: 'active',
    startDate: '2026-02-01',
    endDate: '2026-02-14',
    discountType: '할인율',
    discountValue: '30%',
  },
  {
    id: '2',
    title: '쿠팡 발렌타인 기획전',
    channel: 'coupang',
    status: 'planned',
    startDate: '2026-02-10',
    endDate: '2026-02-14',
    discountType: '쿠폰',
    discountValue: '5,000원',
  },
  {
    id: '3',
    title: '네이버 브랜드 위크',
    channel: 'naver',
    status: 'planned',
    startDate: '2026-02-15',
    endDate: '2026-02-22',
    discountType: 'BOGO',
    discountValue: '1+1',
  },
]

export default function PromotionsPage() {
  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">프로모션 관리</h1>
            <p className="text-sm text-gray-500">모든 프로모션을 한 곳에서 관리하세요</p>
          </div>

          <Link
            href="/promotions/new"
            className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            <Plus size={20} />
            새 프로모션
          </Link>
        </div>

        {/* Search and filters */}
        <div className="flex items-center gap-4 mt-4">
          <div className="flex-1 relative">
            <Search size={20} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              placeholder="프로모션 검색..."
              className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>

          <button className="flex items-center gap-2 px-4 py-2 border border-gray-200 rounded-lg hover:bg-gray-50">
            <Filter size={18} />
            필터
          </button>
        </div>
      </header>

      {/* Promotion list */}
      <div className="flex-1 p-6 overflow-auto">
        <div className="bg-white rounded-lg border border-gray-200">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  프로모션
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  채널
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  기간
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  할인
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  상태
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  작업
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {DEMO_PROMOTIONS.map(promo => {
                const channel = CHANNELS.find(c => c.id === promo.channel)
                const status = STATUS_LABELS[promo.status as keyof typeof STATUS_LABELS]

                return (
                  <tr key={promo.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4">
                      <Link href={`/promotions/${promo.id}`} className="font-medium text-gray-900 hover:text-primary-600">
                        {promo.title}
                      </Link>
                    </td>
                    <td className="px-6 py-4">
                      <span className="flex items-center gap-2">
                        <span className={`w-2 h-2 rounded-full ${channel?.color}`} />
                        {channel?.name}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-600">
                      <span className="flex items-center gap-1">
                        <Calendar size={14} />
                        {promo.startDate} ~ {promo.endDate}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className="flex items-center gap-1 text-sm">
                        <Tag size={14} className="text-gray-400" />
                        {promo.discountType}: {promo.discountValue}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${status.color}`}>
                        {status.label}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <Link
                        href={`/promotions/${promo.id}`}
                        className="text-primary-600 hover:text-primary-700 text-sm font-medium"
                      >
                        편집
                      </Link>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
