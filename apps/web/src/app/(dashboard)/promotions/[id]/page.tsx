import Link from 'next/link'
import { ArrowLeft } from 'lucide-react'

export default function PromotionDetailPage({ params }: { params: { id: string } }) {
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
            <h1 className="text-2xl font-bold text-gray-900">프로모션 상세</h1>
            <p className="text-sm text-gray-500">ID: {params.id}</p>
          </div>
        </div>
      </header>

      {/* Content */}
      <div className="flex-1 p-6 overflow-auto">
        <div className="max-w-2xl mx-auto bg-white rounded-lg border border-gray-200 p-8">
          <div className="text-center text-gray-500">
            <p>프로모션 상세 페이지는 Phase 1에서 구현 예정입니다.</p>
            <p className="mt-2 text-sm">Supabase 연동 후 실제 데이터를 표시합니다.</p>
          </div>
        </div>
      </div>
    </div>
  )
}
