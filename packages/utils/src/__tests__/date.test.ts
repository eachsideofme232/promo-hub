import { describe, it, expect } from 'vitest'
import {
  formatDateKR,
  formatDateRange,
  getMonthDays,
  getWeekDays,
  toISODateString,
} from '../date'

describe('formatDateKR', () => {
  it('formats a Date in Korean style', () => {
    expect(formatDateKR(new Date(2026, 6, 17))).toBe('2026년 07월 17일')
  })

  it('parses and formats an ISO string', () => {
    expect(formatDateKR('2026-01-05')).toBe('2026년 01월 05일')
  })

  it('supports a custom format string', () => {
    expect(formatDateKR(new Date(2026, 6, 17), 'yyyy.MM.dd')).toBe('2026.07.17')
  })
})

describe('formatDateRange', () => {
  it('shortens the end date within the same month', () => {
    expect(formatDateRange('2026-07-01', '2026-07-15')).toBe('2026년 7월 1일 - 15일')
  })

  it('shows full dates across months', () => {
    expect(formatDateRange('2026-07-25', '2026-08-05')).toBe('2026년 7월 25일 - 2026년 8월 5일')
  })
})

describe('getMonthDays', () => {
  it('returns full weeks covering the month', () => {
    const days = getMonthDays(new Date(2026, 6, 1)) // July 2026
    expect(days.length % 7).toBe(0)
    expect(days.length).toBeGreaterThanOrEqual(28)
    // Every day of July must be present
    const julyDays = days.filter((d) => d.getMonth() === 6)
    expect(julyDays.length).toBe(31)
  })

  it('starts weeks on Sunday (ko locale)', () => {
    const days = getMonthDays(new Date(2026, 6, 1))
    expect(days[0].getDay()).toBe(0)
  })
})

describe('getWeekDays', () => {
  it('returns exactly 7 days containing the given date', () => {
    const target = new Date(2026, 6, 17)
    const days = getWeekDays(target)
    expect(days).toHaveLength(7)
    expect(days.some((d) => d.getDate() === 17 && d.getMonth() === 6)).toBe(true)
  })
})

describe('toISODateString', () => {
  it('formats as yyyy-MM-dd with zero padding', () => {
    expect(toISODateString(new Date(2026, 0, 5))).toBe('2026-01-05')
  })
})
