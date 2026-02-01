'use client'

import Link from 'next/link'
import { ArrowLeft } from 'lucide-react'

const CHANNELS = [
  { id: 'oliveyoung', name: '올리브영' },
  { id: 'coupang', name: '쿠팡' },
  { id: 'naver', name: '네이버' },
  { id: 'kakao', name: '카카오' },
  { id: 'musinsa', name: '무신사' },
]

const DISCOUNT_TYPES = [
  { id: 'percentage', name: '할인율 (%)' },
  { id: 'bogo', name: 'BOGO (1+1, 2+1 등)' },
  { id: 'coupon', name: '쿠폰' },
  { id: 'gift', name: '사은품' },
  { id: 'bundle', name: '번들' },
]

export default function NewPromotionPage() {
  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center gap-4">
          <Link
            href="/promotions"
            className="p-2 hover:bg-gray-100 rounded-lg"
          >
            <ArrowLeft size={20} />
          </Link>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">새 프로모션 등록</h1>
            <p className="text-sm text-gray-500">프로모션 정보를 입력하세요</p>
          </div>
        </div>
      </header>

      {/* Form */}
      <div className="flex-1 p-6 overflow-auto">
        <div className="max-w-2xl mx-auto bg-white rounded-lg border border-gray-200 p-6">
          <form className="space-y-6">
            {/* Title */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                프로모션명 *
              </label>
              <input
                type="text"
                placeholder="예: 올리브영 2월 뷰티 페스타"
                className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>

            {/* Channel */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                채널 *
              </label>
              <select className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500">
                <option value="">채널을 선택하세요</option>
                {CHANNELS.map(channel => (
                  <option key={channel.id} value={channel.id}>
                    {channel.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Date range */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  시작일 *
                </label>
                <input
                  type="date"
                  className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  종료일 *
                </label>
                <input
                  type="date"
                  className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>
            </div>

            {/* Discount type */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  할인 유형 *
                </label>
                <select className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500">
                  <option value="">유형을 선택하세요</option>
                  {DISCOUNT_TYPES.map(type => (
                    <option key={type.id} value={type.id}>
                      {type.name}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  할인 값 *
                </label>
                <input
                  type="text"
                  placeholder="예: 30% 또는 5,000원"
                  className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>
            </div>

            {/* Description */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                설명
              </label>
              <textarea
                rows={4}
                placeholder="프로모션에 대한 상세 설명을 입력하세요"
                className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>

            {/* Memo */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                내부 메모
              </label>
              <textarea
                rows={2}
                placeholder="팀 내부용 메모"
                className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>

            {/* Actions */}
            <div className="flex items-center justify-end gap-4 pt-4 border-t border-gray-200">
              <Link
                href="/promotions"
                className="px-4 py-2 text-gray-600 hover:text-gray-800"
              >
                취소
              </Link>
              <button
                type="submit"
                className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
              >
                저장
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}
