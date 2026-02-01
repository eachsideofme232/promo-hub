export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-primary-50 to-white">
      {/* Hero section */}
      <div className="max-w-4xl mx-auto px-4 py-32 text-center">
        <span className="inline-block px-4 py-2 bg-primary-100 text-primary-700 rounded-full text-sm font-medium mb-6">
          Coming Soon
        </span>
        <h1 className="text-5xl font-bold text-gray-900 mb-6">
          PromoHub
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          K-beauty 브랜드를 위한 올인원 프로모션 관리 플랫폼.
          <br />
          올리브영, 쿠팡, 네이버 등 모든 채널을 한 곳에서.
        </p>

        {/* Email signup */}
        <div className="max-w-md mx-auto">
          <form className="flex gap-2">
            <input
              type="email"
              placeholder="이메일 주소"
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
            <button
              type="submit"
              className="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium"
            >
              알림 신청
            </button>
          </form>
          <p className="text-sm text-gray-500 mt-3">
            출시 알림을 받아보세요. 스팸 없음을 약속드립니다.
          </p>
        </div>

        {/* Features preview */}
        <div className="mt-24 grid grid-cols-3 gap-8 text-left">
          <div className="p-6 bg-white rounded-xl shadow-sm border border-gray-100">
            <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center text-primary-600 mb-4">
              📅
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">프로모션 캘린더</h3>
            <p className="text-sm text-gray-600">
              월간, 주간, 일간 뷰로 모든 프로모션 일정을 한눈에
            </p>
          </div>
          <div className="p-6 bg-white rounded-xl shadow-sm border border-gray-100">
            <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center text-primary-600 mb-4">
              🏪
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">채널 통합</h3>
            <p className="text-sm text-gray-600">
              올리브영, 쿠팡, 네이버, 카카오, 무신사 채널 관리
            </p>
          </div>
          <div className="p-6 bg-white rounded-xl shadow-sm border border-gray-100">
            <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center text-primary-600 mb-4">
              👥
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">팀 협업</h3>
            <p className="text-sm text-gray-600">
              팀원과 실시간으로 프로모션 계획을 공유하고 관리
            </p>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t border-gray-200 py-8 mt-24">
        <div className="max-w-4xl mx-auto px-4 text-center text-sm text-gray-500">
          © 2026 PromoHub. All rights reserved.
        </div>
      </footer>
    </div>
  )
}
