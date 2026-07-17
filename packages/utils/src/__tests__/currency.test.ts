import { describe, it, expect } from 'vitest'
import {
  formatNumber,
  formatKRW,
  formatWon,
  formatKoreanNumber,
  formatPercent,
  parseKRW,
} from '../currency'

describe('formatNumber', () => {
  it('groups digits with commas', () => {
    expect(formatNumber(1234567)).toBe('1,234,567')
    expect(formatNumber(0)).toBe('0')
  })
})

describe('formatKRW / formatWon', () => {
  it('prefixes with ₩', () => {
    expect(formatKRW(49000)).toBe('₩49,000')
  })

  it('suffixes with 원', () => {
    expect(formatWon(49000)).toBe('49,000원')
  })
})

describe('formatKoreanNumber', () => {
  it('formats 억 units', () => {
    expect(formatKoreanNumber(100000000)).toBe('1억')
    expect(formatKoreanNumber(250000000)).toBe('2.5억')
  })

  it('formats 만 units', () => {
    expect(formatKoreanNumber(10000)).toBe('1만')
    expect(formatKoreanNumber(35000)).toBe('3.5만')
  })

  it('formats below 만 with plain grouping', () => {
    expect(formatKoreanNumber(9999)).toBe('9,999')
  })
})

describe('formatPercent', () => {
  it('appends a percent sign', () => {
    expect(formatPercent(20)).toBe('20%')
  })
})

describe('parseKRW', () => {
  it('parses ₩-prefixed strings', () => {
    expect(parseKRW('₩49,000')).toBe(49000)
  })

  it('parses 원-suffixed strings', () => {
    expect(parseKRW('49,000원')).toBe(49000)
  })

  it('returns 0 for unparseable input', () => {
    expect(parseKRW('abc')).toBe(0)
  })

  it('round-trips with formatKRW', () => {
    expect(parseKRW(formatKRW(1234567))).toBe(1234567)
  })
})
