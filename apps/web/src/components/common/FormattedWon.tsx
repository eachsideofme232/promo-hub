'use client'

import { formatWon, formatKoreanNumber } from '@promohub/utils'

interface FormattedWonProps {
  value: number
  compact?: boolean
}

/**
 * Reusable Korean Won currency display component.
 *
 * @param value - The numeric amount to format
 * @param compact - When true, uses Korean units (만, 억). Default: false
 *
 * @example
 * <FormattedWon value={150000} />          // "150,000원"
 * <FormattedWon value={150000} compact />  // "15만원"
 */
export function FormattedWon({ value, compact = false }: FormattedWonProps) {
  const formatted = compact
    ? `${formatKoreanNumber(value)}원`
    : formatWon(value)

  return <span>{formatted}</span>
}
