'use client'

import { useMemo } from 'react'
import { useFilterContext, STATUSES, type ChannelId } from './FilterProvider'
import { useChannels } from '../providers/ChannelProvider'
import type { PromotionStatus } from '@promohub/types'

/**
 * Custom hook for accessing and updating filter state.
 * This hook provides a simplified interface to the FilterContext.
 */
export function useFilters() {
  const context = useFilterContext()

  return context
}

/**
 * Hook to get status information by ID
 */
export function useStatus(statusId: PromotionStatus) {
  return useMemo(() => STATUSES.find((s) => s.id === statusId), [statusId])
}

/**
 * Hook to get all available statuses
 */
export function useStatuses() {
  return STATUSES
}

/**
 * Hook to get a summary of active filters for display
 */
export function useFilterSummary() {
  const { channels, statuses, startDate, endDate, hasActiveFilters } =
    useFilterContext()
  const { channels: availableChannels } = useChannels()

  return useMemo(() => {
    const parts: string[] = []

    // Channel summary
    if (channels.length === 0) {
      parts.push('채널 없음')
    } else if (channels.length < availableChannels.length) {
      const selectedNames = channels
        .map((id) => availableChannels.find((c) => c.id === id)?.name)
        .filter(Boolean)
      if (selectedNames.length <= 2) {
        parts.push(selectedNames.join(', '))
      } else {
        parts.push(`${selectedNames[0]} 외 ${selectedNames.length - 1}개`)
      }
    }

    // Status summary
    if (statuses.length === 0) {
      parts.push('상태 없음')
    } else if (statuses.length < STATUSES.length) {
      const selectedNames = statuses
        .map((id) => STATUSES.find((s) => s.id === id)?.name)
        .filter(Boolean)
      if (selectedNames.length <= 2) {
        parts.push(selectedNames.join(', '))
      } else {
        parts.push(`${selectedNames[0]} 외 ${selectedNames.length - 1}개`)
      }
    }

    // Date range summary
    if (startDate && endDate) {
      parts.push(`${startDate} ~ ${endDate}`)
    } else if (startDate) {
      parts.push(`${startDate} 부터`)
    } else if (endDate) {
      parts.push(`${endDate} 까지`)
    }

    return {
      summary: parts.join(' | ') || '전체',
      hasActiveFilters,
      channelCount: channels.length,
      statusCount: statuses.length,
      totalChannels: availableChannels.length,
      totalStatuses: STATUSES.length,
    }
  }, [channels, statuses, startDate, endDate, hasActiveFilters, availableChannels])
}

/**
 * Hook to check if a promotion should be visible based on current filters
 */
export function usePromotionVisibility() {
  const { channels, statuses, startDate, endDate } = useFilterContext()

  return useMemo(() => {
    return (promotion: {
      channelId: string
      status: PromotionStatus
      startDate: string
      endDate: string
    }): boolean => {
      // Check channel filter
      if (channels.length > 0 && !channels.includes(promotion.channelId as ChannelId)) {
        return false
      }

      // Check status filter
      if (statuses.length > 0 && !statuses.includes(promotion.status)) {
        return false
      }

      // Check date range filter
      if (startDate && promotion.endDate < startDate) {
        return false
      }
      if (endDate && promotion.startDate > endDate) {
        return false
      }

      return true
    }
  }, [channels, statuses, startDate, endDate])
}
