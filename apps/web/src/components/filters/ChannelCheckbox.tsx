'use client'

import { Check } from 'lucide-react'
import type { ChannelId } from './FilterProvider'

interface ChannelCheckboxProps {
  id: ChannelId
  name: string
  nameEn?: string
  color: string
  checked: boolean
  onChange: (channelId: ChannelId) => void
  disabled?: boolean
}

export function ChannelCheckbox({
  id,
  name,
  nameEn,
  color,
  checked,
  onChange,
  disabled = false,
}: ChannelCheckboxProps) {
  const handleClick = () => {
    if (!disabled) {
      onChange(id)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if ((e.key === 'Enter' || e.key === ' ') && !disabled) {
      e.preventDefault()
      onChange(id)
    }
  }

  // Determine if color is dark (for text contrast)
  const isDarkColor = isColorDark(color)
  const checkColor = isDarkColor ? '#FFFFFF' : '#000000'

  return (
    <div
      role="checkbox"
      aria-checked={checked}
      aria-disabled={disabled}
      aria-label={`${name} (${nameEn})`}
      tabIndex={disabled ? -1 : 0}
      onClick={handleClick}
      onKeyDown={handleKeyDown}
      className={`
        flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer
        transition-all duration-150 select-none
        ${disabled ? 'opacity-50 cursor-not-allowed' : 'hover:bg-gray-50'}
        ${checked ? 'bg-gray-50' : ''}
      `}
    >
      {/* Checkbox indicator with brand color */}
      <div
        className={`
          relative w-5 h-5 rounded border-2 flex items-center justify-center
          transition-all duration-150
          ${checked ? '' : 'border-gray-300'}
        `}
        style={{
          backgroundColor: checked ? color : 'transparent',
          borderColor: checked ? color : undefined,
        }}
      >
        {checked && <Check size={14} color={checkColor} strokeWidth={3} />}
      </div>

      {/* Channel color indicator dot */}
      <span
        className="w-3 h-3 rounded-full flex-shrink-0"
        style={{ backgroundColor: color }}
        aria-hidden="true"
      />

      {/* Channel name */}
      <div className="flex-1 min-w-0">
        <span className="text-sm font-medium text-gray-900">{name}</span>
        {nameEn && <span className="text-xs text-gray-500 ml-1">({nameEn})</span>}
      </div>
    </div>
  )
}

/**
 * Determine if a hex color is dark based on luminance
 */
function isColorDark(hexColor: string): boolean {
  // Remove # if present
  const hex = hexColor.replace('#', '')

  // Parse RGB values
  const r = parseInt(hex.substring(0, 2), 16)
  const g = parseInt(hex.substring(2, 4), 16)
  const b = parseInt(hex.substring(4, 6), 16)

  // Calculate relative luminance using sRGB
  const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255

  return luminance < 0.5
}
