import {
  format,
  parseISO,
  startOfMonth,
  endOfMonth,
  startOfWeek,
  endOfWeek,
  eachDayOfInterval,
  isSameMonth,
  isSameDay,
  isToday,
  addMonths,
  subMonths,
  addWeeks,
  subWeeks,
} from 'date-fns'
import { ko } from 'date-fns/locale'

// Korean date formatting
export function formatDateKR(date: Date | string, formatStr = 'yyyy년 MM월 dd일'): string {
  const dateObj = typeof date === 'string' ? parseISO(date) : date
  return format(dateObj, formatStr, { locale: ko })
}

export function formatDateRange(startDate: Date | string, endDate: Date | string): string {
  const start = typeof startDate === 'string' ? parseISO(startDate) : startDate
  const end = typeof endDate === 'string' ? parseISO(endDate) : endDate

  if (isSameMonth(start, end)) {
    return `${format(start, 'yyyy년 M월 d일', { locale: ko })} - ${format(end, 'd일', { locale: ko })}`
  }

  return `${format(start, 'yyyy년 M월 d일', { locale: ko })} - ${format(end, 'yyyy년 M월 d일', { locale: ko })}`
}

// Calendar utilities
export function getMonthDays(date: Date): Date[] {
  const start = startOfWeek(startOfMonth(date), { locale: ko })
  const end = endOfWeek(endOfMonth(date), { locale: ko })
  return eachDayOfInterval({ start, end })
}

export function getWeekDays(date: Date): Date[] {
  const start = startOfWeek(date, { locale: ko })
  const end = endOfWeek(date, { locale: ko })
  return eachDayOfInterval({ start, end })
}

// Navigation
export { addMonths, subMonths, addWeeks, subWeeks }

// Comparison
export { isSameMonth, isSameDay, isToday }

// ISO date string helpers
export function toISODateString(date: Date): string {
  return format(date, 'yyyy-MM-dd')
}

export { parseISO }
