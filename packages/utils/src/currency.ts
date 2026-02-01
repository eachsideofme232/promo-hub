// Korean currency formatting utilities

const KR_NUMBER_FORMATTER = new Intl.NumberFormat('ko-KR')

// Format number with Korean number grouping
export function formatNumber(value: number): string {
  return KR_NUMBER_FORMATTER.format(value)
}

// Format as Korean Won
export function formatKRW(value: number): string {
  return `₩${KR_NUMBER_FORMATTER.format(value)}`
}

// Format as Korean Won with 원 suffix
export function formatWon(value: number): string {
  return `${KR_NUMBER_FORMATTER.format(value)}원`
}

// Format large numbers with Korean units (만, 억)
export function formatKoreanNumber(value: number): string {
  if (value >= 100000000) {
    const eok = value / 100000000
    return `${formatDecimal(eok)}억`
  }
  if (value >= 10000) {
    const man = value / 10000
    return `${formatDecimal(man)}만`
  }
  return KR_NUMBER_FORMATTER.format(value)
}

// Format with decimal places if needed
function formatDecimal(value: number): string {
  if (Number.isInteger(value)) {
    return value.toString()
  }
  return value.toFixed(1)
}

// Format percentage
export function formatPercent(value: number): string {
  return `${value}%`
}

// Parse Korean currency string back to number
export function parseKRW(value: string): number {
  const cleaned = value.replace(/[₩,원\s]/g, '')
  return parseInt(cleaned, 10) || 0
}
