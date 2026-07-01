'use client'

import Link from 'next/link'
import { ArrowLeft, Loader2 } from 'lucide-react'
import { PromotionForm } from '@/components/promotions'
import { useTeam } from '@/components/providers/TeamProvider'

export default function NewPromotionPage() {
  const { teamId, isLoading, error } = useTeam()

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
              새 프로모션 생성
            </h1>
            <p className="text-sm text-gray-500">
              Create a new promotion
            </p>
          </div>
        </div>
      </header>

      {/* Form Content */}
      <div className="flex-1 p-6 overflow-auto bg-gray-50">
        <div className="max-w-2xl mx-auto">
          {isLoading ? (
            <div className="flex items-center justify-center py-24">
              <Loader2 size={32} className="animate-spin text-primary-600" />
            </div>
          ) : !teamId ? (
            <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-sm text-red-600">
                {error?.message || '팀 정보를 불러오지 못했습니다. 다시 로그인해 주세요.'}
              </p>
            </div>
          ) : (
            <>
              <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
                <PromotionForm mode="create" teamId={teamId} />
              </div>

              {/* Help Text */}
              <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <h3 className="text-sm font-medium text-blue-800 mb-2">
                  프로모션 작성 가이드 (Guide)
                </h3>
                <ul className="text-sm text-blue-700 space-y-1">
                  <li>
                    * 프로모션명은 채널명과 주요 내용을 포함하면 관리가 쉽습니다.
                  </li>
                  <li>
                    * 할인 값은 유형에 맞게 입력하세요 (예: 30%, 5000원, 1+1).
                  </li>
                  <li>
                    * 메모에는 담당자 정보나 특이사항을 기록하세요.
                  </li>
                </ul>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
