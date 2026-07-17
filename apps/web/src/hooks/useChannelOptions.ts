'use client'

import { useEffect, useState } from 'react'

export interface ChannelOption {
  id: string
  name: string
  slug: string
  color: string
  isSystem: boolean
  isActive: boolean
}

interface ChannelApiRow {
  id: string
  name: string
  slug: string
  color: string | null
  isSystem: boolean
  isActive: boolean
}

/**
 * Fetch the team's available channels (system + custom) from the API.
 * Channel ids are database UUIDs - use them consistently for filtering,
 * promotion forms, and display.
 */
export function useChannelOptions() {
  const [channels, setChannels] = useState<ChannelOption[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false

    async function fetchChannels() {
      try {
        const response = await fetch('/api/channels')
        if (!response.ok) {
          const data = await response.json().catch(() => ({}))
          throw new Error(
            typeof data.error === 'string' ? data.error : '채널을 불러오지 못했습니다'
          )
        }
        const { data } = (await response.json()) as { data: ChannelApiRow[] }
        if (!cancelled) {
          setChannels(
            (data ?? [])
              .filter((ch) => ch.isActive !== false)
              .map((ch) => ({
                id: ch.id,
                name: ch.name,
                slug: ch.slug,
                color: ch.color || '#888888',
                isSystem: ch.isSystem,
                isActive: ch.isActive,
              }))
          )
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : '채널을 불러오지 못했습니다')
        }
      } finally {
        if (!cancelled) {
          setIsLoading(false)
        }
      }
    }

    fetchChannels()
    return () => {
      cancelled = true
    }
  }, [])

  return { channels, isLoading, error }
}
