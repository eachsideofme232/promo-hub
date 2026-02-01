import Link from 'next/link'
import { Users, CreditCard, Bell, Shield } from 'lucide-react'

const settingsItems = [
  {
    href: '/settings/team',
    icon: Users,
    title: '팀 관리',
    description: '팀원 초대 및 권한 관리',
  },
  {
    href: '/settings/billing',
    icon: CreditCard,
    title: '결제 및 구독',
    description: '요금제 및 결제 수단 관리',
  },
  {
    href: '#',
    icon: Bell,
    title: '알림 설정',
    description: '이메일 및 슬랙 알림 설정',
    disabled: true,
  },
  {
    href: '#',
    icon: Shield,
    title: '보안',
    description: '비밀번호 및 2FA 설정',
    disabled: true,
  },
]

export default function SettingsPage() {
  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <h1 className="text-2xl font-bold text-gray-900">설정</h1>
        <p className="text-sm text-gray-500">계정 및 팀 설정을 관리하세요</p>
      </header>

      {/* Settings grid */}
      <div className="flex-1 p-6 overflow-auto">
        <div className="max-w-3xl mx-auto grid grid-cols-2 gap-4">
          {settingsItems.map((item) => {
            const Icon = item.icon
            return (
              <Link
                key={item.href}
                href={item.disabled ? '#' : item.href}
                className={`p-6 bg-white rounded-lg border border-gray-200 transition-colors ${
                  item.disabled
                    ? 'opacity-50 cursor-not-allowed'
                    : 'hover:border-primary-300 hover:shadow-sm'
                }`}
              >
                <Icon className="w-8 h-8 text-primary-600 mb-3" />
                <h3 className="font-semibold text-gray-900">{item.title}</h3>
                <p className="text-sm text-gray-500 mt-1">{item.description}</p>
                {item.disabled && (
                  <span className="inline-block mt-2 text-xs text-gray-400">Coming soon</span>
                )}
              </Link>
            )
          })}
        </div>
      </div>
    </div>
  )
}
