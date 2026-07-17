'use client'

import { useState, useCallback, useEffect, useMemo } from 'react'
import { useRouter } from 'next/navigation'
import {
  format,
  startOfMonth,
  endOfMonth,
  startOfWeek,
  endOfWeek,
} from 'date-fns'
import { CalendarView } from '@/components/calendar'
import { useFilters } from '@/components/filters'
import type { CalendarPromotion } from '@promohub/types'

function getInitialRange() {
  const now = new Date()
  return {
    start: format(startOfWeek(startOfMonth(now), { weekStartsOn: 0 }), 'yyyy-MM-dd'),
    end: format(endOfWeek(endOfMonth(now), { weekStartsOn: 0 }), 'yyyy-MM-dd'),
  }
}

export default function CalendarPage() {
  const router = useRouter()
  const [promotions, setPromotions] = useState<CalendarPromotion[]>([])
  const [range, setRange] = useState(getInitialRange)
  const [error, setError] = useState<string | null>(null)

  const { availableChannels, isChannelSelected, isStatusSelected } = useFilters()

  // Fetch promotions for the visible date range
  useEffect(() => {
    let cancelled = false

    async function fetchPromotions() {
      setError(null)
      try {
        const response = await fetch(
          `/api/calendar?start=${range.start}&end=${range.end}`
        )
        const payload = await response.json().catch(() => ({}))
        if (!response.ok) {
          throw new Error(
            typeof payload.error === 'string'
              ? payload.error
              : '프로모션을 불러오지 못했습니다'
          )
        }
        if (!cancelled) {
          setPromotions(payload.data ?? [])
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : '프로모션을 불러오지 못했습니다')
        }
      }
    }

    fetchPromotions()
    return () => {
      cancelled = true
    }
  }, [range])

  const channelOptions = useMemo(
    () =>
      availableChannels.map((channel) => ({
        id: channel.id,
        name: channel.name,
        color: channel.color,
      })),
    [availableChannels]
  )

  // Apply channel and status filters
  const filteredPromotions = useMemo(() => {
    return promotions.filter((promo) => {
      return isChannelSelected(promo.channelId) && isStatusSelected(promo.status)
    })
  }, [promotions, isChannelSelected, isStatusSelected])

  const handleAddPromotion = useCallback(() => {
    router.push('/promotions/new')
  }, [router])

  const handlePromotionClick = useCallback(
    (promotion: CalendarPromotion) => {
      router.push(`/promotions/${promotion.id}`)
    },
    [router]
  )

  const handleDateClick = useCallback(() => {
    router.push('/promotions/new')
  }, [router])

  const handleDateRangeChange = useCallback((start: Date, end: Date) => {
    setRange({
      start: format(start, 'yyyy-MM-dd'),
      end: format(end, 'yyyy-MM-dd'),
    })
  }, [])

  return (
    <div className="h-full flex flex-col">
      {error && (
        <div className="m-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-600">{error}</p>
        </div>
      )}
      <div className="flex-1 min-h-0">
        <CalendarView
          promotions={filteredPromotions}
          channels={channelOptions}
          initialView="month"
          onAddPromotion={handleAddPromotion}
          onPromotionClick={handlePromotionClick}
          onDateClick={handleDateClick}
          onDateRangeChange={handleDateRangeChange}
        />
      </div>
    </div>
  )
}
