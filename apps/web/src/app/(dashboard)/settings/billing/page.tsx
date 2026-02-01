import Link from 'next/link'
import { ArrowLeft, Check, CreditCard } from 'lucide-react'

const PLANS = [
  {
    id: 'free',
    name: 'Free',
    price: '₩0',
    period: '영구 무료',
    features: [
      '프로모션 10개',
      '팀원 2명',
      '기본 캘린더',
      '커뮤니티 지원',
    ],
    current: false,
  },
  {
    id: 'pro',
    name: 'Pro',
    price: '₩49,000',
    period: '월',
    features: [
      '프로모션 무제한',
      '팀원 10명',
      '고급 캘린더 + 분석',
      '채널 연동 (5개)',
      '우선 지원',
    ],
    current: true,
    recommended: true,
  },
  {
    id: 'enterprise',
    name: 'Enterprise',
    price: '문의',
    period: '',
    features: [
      '모든 Pro 기능',
      '팀원 무제한',
      '채널 무제한 연동',
      'API 액세스',
      '전담 지원',
      'SLA 보장',
    ],
    current: false,
  },
]

export default function BillingSettingsPage() {
  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center gap-4">
          <Link href="/settings" className="p-2 hover:bg-gray-100 rounded-lg">
            <ArrowLeft size={20} />
          </Link>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">결제 및 구독</h1>
            <p className="text-sm text-gray-500">요금제 및 결제 정보를 관리하세요</p>
          </div>
        </div>
      </header>

      {/* Content */}
      <div className="flex-1 p-6 overflow-auto">
        <div className="max-w-5xl mx-auto">
          {/* Current plan info */}
          <div className="bg-primary-50 border border-primary-200 rounded-lg p-6 mb-8">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-primary-600 font-medium">현재 요금제</p>
                <h2 className="text-2xl font-bold text-primary-900">Pro</h2>
                <p className="text-sm text-primary-700 mt-1">다음 결제일: 2026년 3월 1일</p>
              </div>
              <button className="px-4 py-2 border border-primary-300 text-primary-700 rounded-lg hover:bg-primary-100 transition-colors">
                결제 수단 관리
              </button>
            </div>
          </div>

          {/* Plans */}
          <h3 className="text-lg font-semibold text-gray-900 mb-4">요금제 비교</h3>
          <div className="grid grid-cols-3 gap-6">
            {PLANS.map((plan) => (
              <div
                key={plan.id}
                className={`bg-white rounded-lg border-2 p-6 ${
                  plan.current
                    ? 'border-primary-500 ring-1 ring-primary-500'
                    : 'border-gray-200'
                }`}
              >
                {plan.recommended && (
                  <span className="inline-block px-2 py-1 bg-primary-100 text-primary-700 text-xs font-medium rounded mb-4">
                    추천
                  </span>
                )}
                <h4 className="text-xl font-bold text-gray-900">{plan.name}</h4>
                <div className="mt-2 mb-4">
                  <span className="text-3xl font-bold text-gray-900">{plan.price}</span>
                  {plan.period && (
                    <span className="text-gray-500 ml-1">/ {plan.period}</span>
                  )}
                </div>
                <ul className="space-y-3">
                  {plan.features.map((feature, i) => (
                    <li key={i} className="flex items-center gap-2 text-sm text-gray-600">
                      <Check size={16} className="text-green-500" />
                      {feature}
                    </li>
                  ))}
                </ul>
                <button
                  className={`w-full mt-6 py-2 rounded-lg font-medium transition-colors ${
                    plan.current
                      ? 'bg-gray-100 text-gray-500 cursor-not-allowed'
                      : 'bg-primary-600 text-white hover:bg-primary-700'
                  }`}
                  disabled={plan.current}
                >
                  {plan.current ? '현재 요금제' : plan.id === 'enterprise' ? '문의하기' : '업그레이드'}
                </button>
              </div>
            ))}
          </div>

          {/* Payment method */}
          <div className="bg-white rounded-lg border border-gray-200 mt-8 p-6">
            <h3 className="font-semibold text-gray-900 mb-4">결제 수단</h3>
            <div className="flex items-center gap-4 p-4 bg-gray-50 rounded-lg">
              <CreditCard className="w-8 h-8 text-gray-400" />
              <div>
                <p className="font-medium text-gray-900">•••• •••• •••• 4242</p>
                <p className="text-sm text-gray-500">만료: 12/28</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
