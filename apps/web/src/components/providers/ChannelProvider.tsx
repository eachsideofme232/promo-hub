'use client'

import {
  createContext,
  useContext,
  useEffect,
  useState,
  useCallback,
  useMemo,
  type ReactNode,
} from 'react'
import type { Channel } from '@promohub/types'

interface ChannelContextValue {
  /** Active channels (system + team custom) sourced from the database via /api/channels */
  channels: Channel[]
  isLoading: boolean
  error: Error | null
  /** Look up a single channel by its database UUID */
  getChannel: (id: string) => Channel | undefined
  /** Re-fetch channels (e.g. after creating a custom channel) */
  refetch: () => Promise<void>
}

const ChannelContext = createContext<ChannelContextValue | null>(null)

/**
 * Provides the single source of truth for channels across the app.
 *
 * Channels are fetched from the database (`GET /api/channels`) and keyed by
 * their UUID, replacing the previously hard-coded slug-based channel lists.
 * This keeps filters, the calendar, and forms consistent with the database
 * and with team-specific custom channels.
 */
export function ChannelProvider({ children }: { children: ReactNode }) {
  const [channels, setChannels] = useState<Channel[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  const fetchChannels = useCallback(async () => {
    setIsLoading(true)
    setError(null)
    try {
      const res = await fetch('/api/channels')
      if (!res.ok) {
        throw new Error(`Failed to load channels (${res.status})`)
      }
      const json = (await res.json()) as { data?: Channel[] }
      // Only expose active channels for filtering/selection
      setChannels((json.data ?? []).filter((c) => c.isActive))
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to load channels'))
      setChannels([])
    } finally {
      setIsLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchChannels()
  }, [fetchChannels])

  const getChannel = useCallback(
    (id: string) => channels.find((c) => c.id === id),
    [channels]
  )

  const value = useMemo<ChannelContextValue>(
    () => ({ channels, isLoading, error, getChannel, refetch: fetchChannels }),
    [channels, isLoading, error, getChannel, fetchChannels]
  )

  return <ChannelContext.Provider value={value}>{children}</ChannelContext.Provider>
}

/**
 * Access the channels context. Returns the active channel list plus helpers.
 * Must be used within a {@link ChannelProvider}.
 */
export function useChannels(): ChannelContextValue {
  const ctx = useContext(ChannelContext)
  if (!ctx) {
    throw new Error('useChannels must be used within a ChannelProvider')
  }
  return ctx
}

/**
 * Convenience hook to look up a single channel by its UUID.
 */
export function useChannel(channelId: string | null | undefined): Channel | undefined {
  const { getChannel } = useChannels()
  return channelId ? getChannel(channelId) : undefined
}
