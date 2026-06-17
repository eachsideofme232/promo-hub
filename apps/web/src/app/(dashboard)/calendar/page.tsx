'use client'

import { useState, useCallback, useMemo } from 'react'
import { CalendarView } from '@/components/calendar'
import { useFilters, useChannels } from '@/components/filters'
import type { CalendarPromotion } from '@promohub/types'

// Seed channel UUIDs (match supabase/seed.sql) so demo data lines up with the
// database-sourced channels until the calendar is wired to the API (Phase 3).
const CHANNEL_OLIVEYOUNG = 'c1000000-0000-0000-0000-000000000001'
const CHANNEL_COUPANG = 'c1000000-0000-0000-0000-000000000002'
const CHANNEL_NAVER = 'c1000000-0000-0000-0000-000000000003'
const CHANNEL_KAKAO = 'c1000000-0000-0000-0000-000000000004'
const CHANNEL_MUSINSA = 'c1000000-0000-0000-0000-000000000005'

// Demo promotions data
const DEMO_PROMOTIONS: CalendarPromotion[] = [
  {
    id: '1',
    title: '올리브영 2월 세일',
    status: 'active',
    channelId: CHANNEL_OLIVEYOUNG,
    channelName: '올리브영',
    channelColor: '#00A651',
    startDate: '2026-02-05',
    endDate: '2026-02-12',
    isStart: true,
    isEnd: true,
    isMultiDay: true,
  },
  {
    id: '2',
    title: '쿠팡 발렌타인 기획전',
    status: 'planned',
    channelId: CHANNEL_COUPANG,
    channelName: '쿠팡',
    channelColor: '#E31937',
    startDate: '2026-02-10',
    endDate: '2026-02-14',
    isStart: true,
    isEnd: true,
    isMultiDay: true,
  },
  {
    id: '3',
    title: '네이버 브랜드 위크',
    status: 'planned',
    channelId: CHANNEL_NAVER,
    channelName: '네이버',
    channelColor: '#03C75A',
    startDate: '2026-02-15',
    endDate: '2026-02-22',
    isStart: true,
    isEnd: true,
    isMultiDay: true,
  },
  {
    id: '4',
    title: '카카오 선물하기 프로모션',
    status: 'ended',
    channelId: CHANNEL_KAKAO,
    channelName: '카카오',
    channelColor: '#FEE500',
    startDate: '2026-02-01',
    endDate: '2026-02-07',
    isStart: true,
    isEnd: true,
    isMultiDay: true,
  },
  {
    id: '5',
    title: '무신사 브랜드데이',
    status: 'active',
    channelId: CHANNEL_MUSINSA,
    channelName: '무신사',
    channelColor: '#000000',
    startDate: '2026-02-08',
    endDate: '2026-02-20',
    isStart: true,
    isEnd: true,
    isMultiDay: true,
  },
  {
    id: '6',
    title: '올리브영 월말 정산 세일',
    status: 'planned',
    channelId: CHANNEL_OLIVEYOUNG,
    channelName: '올리브영',
    channelColor: '#00A651',
    startDate: '2026-02-25',
    endDate: '2026-02-28',
    isStart: true,
    isEnd: true,
    isMultiDay: true,
  },
]

export default function CalendarPage() {
  const [promotions] = useState<CalendarPromotion[]>(DEMO_PROMOTIONS)

  // Use filter context for channel and status filtering
  const { isChannelSelected, isStatusSelected } = useFilters()

  // Channel options sourced from the database via ChannelProvider
  const { channels } = useChannels()
  const channelOptions = useMemo(
    () => channels.map((channel) => ({
      id: channel.id,
      name: channel.name,
      color: channel.color,
    })),
    [channels]
  )

  // Filter promotions based on selected channels and statuses
  const filteredPromotions = useMemo(() => {
    return promotions.filter((promo) => {
      const channelMatch = isChannelSelected(promo.channelId)
      const statusMatch = isStatusSelected(promo.status)
      return channelMatch && statusMatch
    })
  }, [promotions, isChannelSelected, isStatusSelected])

  const handleAddPromotion = useCallback(() => {
    // TODO: Open promotion creation modal
    console.log('Add promotion clicked')
  }, [])

  const handlePromotionClick = useCallback((promotion: CalendarPromotion) => {
    // TODO: Open promotion detail modal
    console.log('Promotion clicked:', promotion)
  }, [])

  const handleDateClick = useCallback((date: Date) => {
    // TODO: Open promotion creation modal with pre-filled date
    console.log('Date clicked:', date)
  }, [])

  const handleDateRangeChange = useCallback((start: Date, end: Date) => {
    // TODO: Fetch promotions for the new date range
    console.log('Date range changed:', start, end)
  }, [])

  return (
    <CalendarView
      promotions={filteredPromotions}
      channels={channelOptions}
      initialView="month"
      onAddPromotion={handleAddPromotion}
      onPromotionClick={handlePromotionClick}
      onDateClick={handleDateClick}
      onDateRangeChange={handleDateRangeChange}
    />
  )
}
