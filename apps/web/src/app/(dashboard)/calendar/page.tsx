'use client'

import { useState } from 'react'
import { ChevronLeft, ChevronRight, Plus, Filter } from 'lucide-react'

const CHANNELS = [
  { id: 'oliveyoung', name: '올리브영', color: 'bg-green-500' },
  { id: 'coupang', name: '쿠팡', color: 'bg-red-500' },
  { id: 'naver', name: '네이버', color: 'bg-green-600' },
  { id: 'kakao', name: '카카오', color: 'bg-yellow-500' },
  { id: 'musinsa', name: '무신사', color: 'bg-black' },
]

const DAYS = ['일', '월', '화', '수', '목', '금', '토']

// Demo promotions data
const DEMO_PROMOTIONS = [
  { id: 1, title: '올리브영 2월 세일', channel: 'oliveyoung', startDay: 5, endDay: 12 },
  { id: 2, title: '쿠팡 발렌타인 기획전', channel: 'coupang', startDay: 10, endDay: 14 },
  { id: 3, title: '네이버 브랜드 위크', channel: 'naver', startDay: 15, endDay: 22 },
]

export default function CalendarPage() {
  const [currentDate, setCurrentDate] = useState(new Date())
  const [selectedChannels, setSelectedChannels] = useState<string[]>(CHANNELS.map(c => c.id))
  const [view, setView] = useState<'month' | 'week'>('month')

  const year = currentDate.getFullYear()
  const month = currentDate.getMonth()

  // Get first day of month and total days
  const firstDayOfMonth = new Date(year, month, 1).getDay()
  const daysInMonth = new Date(year, month + 1, 0).getDate()

  // Generate calendar days
  const calendarDays = []
  for (let i = 0; i < firstDayOfMonth; i++) {
    calendarDays.push(null)
  }
  for (let i = 1; i <= daysInMonth; i++) {
    calendarDays.push(i)
  }

  const navigateMonth = (direction: 'prev' | 'next') => {
    setCurrentDate(new Date(year, month + (direction === 'next' ? 1 : -1), 1))
  }

  const toggleChannel = (channelId: string) => {
    setSelectedChannels(prev =>
      prev.includes(channelId)
        ? prev.filter(id => id !== channelId)
        : [...prev, channelId]
    )
  }

  const getPromotionsForDay = (day: number) => {
    return DEMO_PROMOTIONS.filter(
      p => selectedChannels.includes(p.channel) && day >= p.startDay && day <= p.endDay
    )
  }

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">프로모션 캘린더</h1>
            <p className="text-sm text-gray-500">채널별 프로모션 일정을 관리하세요</p>
          </div>

          <div className="flex items-center gap-4">
            {/* View toggle */}
            <div className="flex bg-gray-100 rounded-lg p-1">
              <button
                onClick={() => setView('month')}
                className={`px-3 py-1 rounded text-sm ${
                  view === 'month' ? 'bg-white shadow' : 'text-gray-600'
                }`}
              >
                월간
              </button>
              <button
                onClick={() => setView('week')}
                className={`px-3 py-1 rounded text-sm ${
                  view === 'week' ? 'bg-white shadow' : 'text-gray-600'
                }`}
              >
                주간
              </button>
            </div>

            {/* Add promotion button */}
            <button className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
              <Plus size={20} />
              프로모션 추가
            </button>
          </div>
        </div>

        {/* Month navigation and filters */}
        <div className="flex items-center justify-between mt-4">
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigateMonth('prev')}
              className="p-2 hover:bg-gray-100 rounded-lg"
            >
              <ChevronLeft size={20} />
            </button>
            <h2 className="text-lg font-semibold text-gray-900 min-w-[140px] text-center">
              {year}년 {month + 1}월
            </h2>
            <button
              onClick={() => navigateMonth('next')}
              className="p-2 hover:bg-gray-100 rounded-lg"
            >
              <ChevronRight size={20} />
            </button>
            <button
              onClick={() => setCurrentDate(new Date())}
              className="px-3 py-1 text-sm text-gray-600 hover:bg-gray-100 rounded"
            >
              오늘
            </button>
          </div>

          {/* Channel filters */}
          <div className="flex items-center gap-2">
            <Filter size={16} className="text-gray-400" />
            {CHANNELS.map(channel => (
              <button
                key={channel.id}
                onClick={() => toggleChannel(channel.id)}
                className={`flex items-center gap-2 px-3 py-1 rounded-full text-sm border transition-colors ${
                  selectedChannels.includes(channel.id)
                    ? 'border-gray-300 bg-white'
                    : 'border-transparent bg-gray-100 text-gray-400'
                }`}
              >
                <span className={`w-2 h-2 rounded-full ${channel.color}`} />
                {channel.name}
              </button>
            ))}
          </div>
        </div>
      </header>

      {/* Calendar Grid */}
      <div className="flex-1 p-6 overflow-auto">
        <div className="bg-white rounded-lg border border-gray-200 h-full">
          {/* Day headers */}
          <div className="grid grid-cols-7 border-b border-gray-200">
            {DAYS.map((day, i) => (
              <div
                key={day}
                className={`p-3 text-center text-sm font-medium ${
                  i === 0 ? 'text-red-500' : i === 6 ? 'text-blue-500' : 'text-gray-600'
                }`}
              >
                {day}
              </div>
            ))}
          </div>

          {/* Calendar days */}
          <div className="grid grid-cols-7 flex-1">
            {calendarDays.map((day, index) => {
              const isToday = day === new Date().getDate() &&
                month === new Date().getMonth() &&
                year === new Date().getFullYear()
              const promotions = day ? getPromotionsForDay(day) : []

              return (
                <div
                  key={index}
                  className={`min-h-[100px] border-b border-r border-gray-100 p-2 ${
                    !day ? 'bg-gray-50' : ''
                  }`}
                >
                  {day && (
                    <>
                      <span
                        className={`inline-flex items-center justify-center w-7 h-7 text-sm ${
                          isToday
                            ? 'bg-primary-600 text-white rounded-full'
                            : index % 7 === 0
                            ? 'text-red-500'
                            : index % 7 === 6
                            ? 'text-blue-500'
                            : 'text-gray-700'
                        }`}
                      >
                        {day}
                      </span>
                      <div className="mt-1 space-y-1">
                        {promotions.slice(0, 3).map(promo => {
                          const channel = CHANNELS.find(c => c.id === promo.channel)
                          return (
                            <div
                              key={promo.id}
                              className={`text-xs px-2 py-1 rounded truncate text-white ${channel?.color}`}
                            >
                              {promo.title}
                            </div>
                          )
                        })}
                        {promotions.length > 3 && (
                          <div className="text-xs text-gray-500 px-2">
                            +{promotions.length - 3}개 더보기
                          </div>
                        )}
                      </div>
                    </>
                  )}
                </div>
              )
            })}
          </div>
        </div>
      </div>
    </div>
  )
}
