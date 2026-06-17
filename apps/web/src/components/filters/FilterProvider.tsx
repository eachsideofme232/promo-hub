'use client'

import {
  createContext,
  useContext,
  useCallback,
  useMemo,
  type ReactNode,
} from 'react'
import { useRouter, useSearchParams, usePathname } from 'next/navigation'
import type { PromotionStatus } from '@promohub/types'
import { useChannels } from '../providers/ChannelProvider'

// Channel IDs are database UUIDs sourced from ChannelProvider (single source of truth).
export type ChannelId = string

export const STATUSES: { id: PromotionStatus; name: string; nameEn: string }[] = [
  { id: 'planned', name: '예정', nameEn: 'Planned' },
  { id: 'active', name: '진행중', nameEn: 'Active' },
  { id: 'ended', name: '종료', nameEn: 'Ended' },
  { id: 'cancelled', name: '취소', nameEn: 'Cancelled' },
]

export interface FilterState {
  channels: ChannelId[]
  statuses: PromotionStatus[]
  startDate: string | null
  endDate: string | null
}

export interface FilterContextValue extends FilterState {
  // Channel filters
  toggleChannel: (channelId: ChannelId) => void
  setChannels: (channelIds: ChannelId[]) => void
  selectAllChannels: () => void
  deselectAllChannels: () => void
  isChannelSelected: (channelId: ChannelId) => boolean

  // Status filters
  toggleStatus: (status: PromotionStatus) => void
  setStatuses: (statuses: PromotionStatus[]) => void
  selectAllStatuses: () => void
  deselectAllStatuses: () => void
  isStatusSelected: (status: PromotionStatus) => boolean

  // Date range filters
  setDateRange: (startDate: string | null, endDate: string | null) => void
  clearDateRange: () => void

  // Reset all filters
  resetFilters: () => void

  // Check if any filters are active
  hasActiveFilters: boolean
}

const FilterContext = createContext<FilterContextValue | null>(null)

// URL param keys
const PARAM_CHANNELS = 'channels'
const PARAM_STATUSES = 'statuses'
const PARAM_START_DATE = 'startDate'
const PARAM_END_DATE = 'endDate'

function parseChannelsFromUrl(
  params: URLSearchParams,
  availableChannelIds: ChannelId[]
): ChannelId[] {
  const channelsParam = params.get(PARAM_CHANNELS)
  if (!channelsParam) {
    // Default: all available channels selected
    return availableChannelIds
  }
  const channelIds = channelsParam.split(',').filter(Boolean)
  // Keep only IDs that correspond to a real channel
  return channelIds.filter((id) => availableChannelIds.includes(id))
}

function parseStatusesFromUrl(params: URLSearchParams): PromotionStatus[] {
  const statusesParam = params.get(PARAM_STATUSES)
  if (!statusesParam) {
    // Default: all statuses selected
    return STATUSES.map((s) => s.id)
  }
  const statusIds = statusesParam.split(',').filter(Boolean)
  return statusIds.filter((id): id is PromotionStatus =>
    STATUSES.some((s) => s.id === id)
  )
}

interface FilterProviderProps {
  children: ReactNode
}

export function FilterProvider({ children }: FilterProviderProps) {
  const router = useRouter()
  const pathname = usePathname()
  const searchParams = useSearchParams()
  const { channels: availableChannels } = useChannels()

  const availableChannelIds = useMemo(
    () => availableChannels.map((c) => c.id),
    [availableChannels]
  )

  // Parse filter state from URL
  const filterState = useMemo<FilterState>(() => {
    return {
      channels: parseChannelsFromUrl(searchParams, availableChannelIds),
      statuses: parseStatusesFromUrl(searchParams),
      startDate: searchParams.get(PARAM_START_DATE),
      endDate: searchParams.get(PARAM_END_DATE),
    }
  }, [searchParams, availableChannelIds])

  // Update URL with new filter values
  const updateUrl = useCallback(
    (updates: Partial<FilterState>) => {
      const params = new URLSearchParams(searchParams.toString())

      if (updates.channels !== undefined) {
        if (
          updates.channels.length === availableChannelIds.length ||
          updates.channels.length === 0
        ) {
          // Remove param if all or none selected (use default)
          params.delete(PARAM_CHANNELS)
        } else {
          params.set(PARAM_CHANNELS, updates.channels.join(','))
        }
      }

      if (updates.statuses !== undefined) {
        if (
          updates.statuses.length === STATUSES.length ||
          updates.statuses.length === 0
        ) {
          params.delete(PARAM_STATUSES)
        } else {
          params.set(PARAM_STATUSES, updates.statuses.join(','))
        }
      }

      if (updates.startDate !== undefined) {
        if (updates.startDate) {
          params.set(PARAM_START_DATE, updates.startDate)
        } else {
          params.delete(PARAM_START_DATE)
        }
      }

      if (updates.endDate !== undefined) {
        if (updates.endDate) {
          params.set(PARAM_END_DATE, updates.endDate)
        } else {
          params.delete(PARAM_END_DATE)
        }
      }

      const queryString = params.toString()
      const newUrl = queryString ? `${pathname}?${queryString}` : pathname
      router.push(newUrl, { scroll: false })
    },
    [pathname, router, searchParams, availableChannelIds]
  )

  // Channel filter actions
  const toggleChannel = useCallback(
    (channelId: ChannelId) => {
      const newChannels = filterState.channels.includes(channelId)
        ? filterState.channels.filter((id) => id !== channelId)
        : [...filterState.channels, channelId]
      updateUrl({ channels: newChannels })
    },
    [filterState.channels, updateUrl]
  )

  const setChannels = useCallback(
    (channelIds: ChannelId[]) => {
      updateUrl({ channels: channelIds })
    },
    [updateUrl]
  )

  const selectAllChannels = useCallback(() => {
    updateUrl({ channels: availableChannelIds })
  }, [updateUrl, availableChannelIds])

  const deselectAllChannels = useCallback(() => {
    updateUrl({ channels: [] })
  }, [updateUrl])

  const isChannelSelected = useCallback(
    (channelId: ChannelId) => filterState.channels.includes(channelId),
    [filterState.channels]
  )

  // Status filter actions
  const toggleStatus = useCallback(
    (status: PromotionStatus) => {
      const newStatuses = filterState.statuses.includes(status)
        ? filterState.statuses.filter((s) => s !== status)
        : [...filterState.statuses, status]
      updateUrl({ statuses: newStatuses })
    },
    [filterState.statuses, updateUrl]
  )

  const setStatuses = useCallback(
    (statuses: PromotionStatus[]) => {
      updateUrl({ statuses })
    },
    [updateUrl]
  )

  const selectAllStatuses = useCallback(() => {
    updateUrl({ statuses: STATUSES.map((s) => s.id) })
  }, [updateUrl])

  const deselectAllStatuses = useCallback(() => {
    updateUrl({ statuses: [] })
  }, [updateUrl])

  const isStatusSelected = useCallback(
    (status: PromotionStatus) => filterState.statuses.includes(status),
    [filterState.statuses]
  )

  // Date range actions
  const setDateRange = useCallback(
    (startDate: string | null, endDate: string | null) => {
      updateUrl({ startDate, endDate })
    },
    [updateUrl]
  )

  const clearDateRange = useCallback(() => {
    updateUrl({ startDate: null, endDate: null })
  }, [updateUrl])

  // Reset all filters
  const resetFilters = useCallback(() => {
    router.push(pathname, { scroll: false })
  }, [pathname, router])

  // Check if any filters are active (not default)
  const hasActiveFilters = useMemo(() => {
    const hasChannelFilter =
      filterState.channels.length > 0 &&
      filterState.channels.length < availableChannelIds.length
    const hasStatusFilter =
      filterState.statuses.length > 0 &&
      filterState.statuses.length < STATUSES.length
    const hasDateFilter = !!filterState.startDate || !!filterState.endDate

    return hasChannelFilter || hasStatusFilter || hasDateFilter
  }, [filterState, availableChannelIds])

  const contextValue = useMemo<FilterContextValue>(
    () => ({
      ...filterState,
      toggleChannel,
      setChannels,
      selectAllChannels,
      deselectAllChannels,
      isChannelSelected,
      toggleStatus,
      setStatuses,
      selectAllStatuses,
      deselectAllStatuses,
      isStatusSelected,
      setDateRange,
      clearDateRange,
      resetFilters,
      hasActiveFilters,
    }),
    [
      filterState,
      toggleChannel,
      setChannels,
      selectAllChannels,
      deselectAllChannels,
      isChannelSelected,
      toggleStatus,
      setStatuses,
      selectAllStatuses,
      deselectAllStatuses,
      isStatusSelected,
      setDateRange,
      clearDateRange,
      resetFilters,
      hasActiveFilters,
    ]
  )

  return (
    <FilterContext.Provider value={contextValue}>
      {children}
    </FilterContext.Provider>
  )
}

export function useFilterContext(): FilterContextValue {
  const context = useContext(FilterContext)
  if (!context) {
    throw new Error('useFilterContext must be used within a FilterProvider')
  }
  return context
}
