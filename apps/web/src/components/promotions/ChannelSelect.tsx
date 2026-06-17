'use client'

import { forwardRef } from 'react'

export interface ChannelOption {
  id: string
  name: string
  slug: string
  color: string
}

// Fallback Korean e-commerce channels (hex colors match supabase/seed.sql).
// In the app, channels are supplied from ChannelProvider via the `channels` prop;
// this list is only used when no channels are passed (e.g. standalone usage).
export const DEFAULT_CHANNELS: ChannelOption[] = [
  { id: 'oliveyoung', name: '올리브영', slug: 'oliveyoung', color: '#00A651' },
  { id: 'coupang', name: '쿠팡', slug: 'coupang', color: '#E31937' },
  { id: 'naver', name: '네이버', slug: 'naver', color: '#03C75A' },
  { id: 'kakao', name: '카카오', slug: 'kakao', color: '#FEE500' },
  { id: 'musinsa', name: '무신사', slug: 'musinsa', color: '#000000' },
  { id: 'ssg', name: 'SSG', slug: 'ssg', color: '#FF5252' },
  { id: 'lotteon', name: '롯데온', slug: 'lotteon', color: '#E60012' },
  { id: '11st', name: '11번가', slug: '11st', color: '#FF0050' },
]

interface ChannelSelectProps {
  value?: string
  onChange?: (value: string) => void
  channels?: ChannelOption[]
  error?: string
  disabled?: boolean
  placeholder?: string
  label?: string
  required?: boolean
}

export const ChannelSelect = forwardRef<HTMLSelectElement, ChannelSelectProps>(
  function ChannelSelect(
    {
      value,
      onChange,
      channels = DEFAULT_CHANNELS,
      error,
      disabled = false,
      placeholder = '채널 선택 (Select channel)',
      label = '판매 채널 (Channel)',
      required = false,
    },
    ref
  ) {
    const selectedChannel = channels.find((c) => c.id === value)

    return (
      <div className="space-y-1">
        {label && (
          <label className="block text-sm font-medium text-gray-700">
            {label}
            {required && <span className="text-red-500 ml-1">*</span>}
          </label>
        )}
        <div className="relative">
          {selectedChannel && (
            <span
              className="absolute left-3 top-1/2 -translate-y-1/2 w-3 h-3 rounded-full"
              style={{ backgroundColor: selectedChannel.color }}
            />
          )}
          <select
            ref={ref}
            value={value || ''}
            onChange={(e) => onChange?.(e.target.value)}
            disabled={disabled}
            className={`
              w-full px-4 py-2.5 border rounded-lg appearance-none
              focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent
              disabled:bg-gray-100 disabled:cursor-not-allowed
              ${selectedChannel ? 'pl-9' : ''}
              ${error ? 'border-red-500 focus:ring-red-500' : 'border-gray-300'}
            `}
          >
            <option value="">{placeholder}</option>
            {channels.map((channel) => (
              <option key={channel.id} value={channel.id}>
                {channel.name}
              </option>
            ))}
          </select>
          <div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none">
            <svg
              className="w-5 h-5 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 9l-7 7-7-7"
              />
            </svg>
          </div>
        </div>
        {error && <p className="text-sm text-red-500">{error}</p>}
      </div>
    )
  }
)
