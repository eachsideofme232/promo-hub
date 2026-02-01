// Calendar types

import type { Promotion } from './promotion'

export type CalendarView = 'month' | 'week' | 'day'

export interface CalendarDay {
  date: string // ISO date string YYYY-MM-DD
  dayOfMonth: number
  isToday: boolean
  isCurrentMonth: boolean
  promotions: CalendarPromotion[]
}

export interface CalendarPromotion extends Pick<Promotion, 'id' | 'title' | 'status'> {
  channelId: string
  channelName: string
  channelColor: string
  startDate: string
  endDate: string
  isStart: boolean
  isEnd: boolean
  isMultiDay: boolean
}

export interface CalendarRange {
  start: string // ISO date string
  end: string   // ISO date string
}

export interface CalendarFilters {
  channels?: string[]
  status?: Promotion['status'][]
}
