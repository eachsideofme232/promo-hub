'use client'

import { useState } from 'react'
import { ChevronDown, ChevronUp } from 'lucide-react'
import { ChannelCheckbox } from './ChannelCheckbox'
import { useFilterContext, type ChannelId } from './FilterProvider'

interface ChannelFilterProps {
  defaultExpanded?: boolean
}

export function ChannelFilter({ defaultExpanded = true }: ChannelFilterProps) {
  const [isExpanded, setIsExpanded] = useState(defaultExpanded)
  const {
    channels,
    availableChannels,
    channelsLoading,
    toggleChannel,
    selectAllChannels,
    deselectAllChannels,
    isChannelSelected,
  } = useFilterContext()

  const selectedCount = channels.length
  const totalCount = availableChannels.length
  const allSelected = selectedCount === totalCount
  const noneSelected = selectedCount === 0

  return (
    <div className="border-b border-gray-200 pb-4">
      {/* Header */}
      <button
        type="button"
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full flex items-center justify-between py-2 text-left"
        aria-expanded={isExpanded}
        aria-controls="channel-filter-content"
      >
        <div className="flex items-center gap-2">
          <h3 className="text-sm font-semibold text-gray-900">채널</h3>
          <span className="text-xs text-gray-500">
            ({selectedCount}/{totalCount})
          </span>
        </div>
        {isExpanded ? (
          <ChevronUp size={16} className="text-gray-400" />
        ) : (
          <ChevronDown size={16} className="text-gray-400" />
        )}
      </button>

      {/* Content */}
      {isExpanded && (
        <div id="channel-filter-content" className="mt-2 space-y-1">
          {/* Select All / Deselect All buttons */}
          <div className="flex gap-2 mb-3">
            <button
              type="button"
              onClick={selectAllChannels}
              disabled={allSelected}
              className={`
                flex-1 px-3 py-1.5 text-xs font-medium rounded-md
                transition-colors duration-150
                ${
                  allSelected
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }
              `}
            >
              전체 선택
            </button>
            <button
              type="button"
              onClick={deselectAllChannels}
              disabled={noneSelected}
              className={`
                flex-1 px-3 py-1.5 text-xs font-medium rounded-md
                transition-colors duration-150
                ${
                  noneSelected
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }
              `}
            >
              전체 해제
            </button>
          </div>

          {/* Channel checkboxes */}
          <div className="space-y-1">
            {channelsLoading ? (
              <p className="px-2 py-1.5 text-xs text-gray-400">채널 불러오는 중...</p>
            ) : availableChannels.length === 0 ? (
              <p className="px-2 py-1.5 text-xs text-gray-400">사용 가능한 채널이 없습니다</p>
            ) : (
              availableChannels.map((channel) => (
                <ChannelCheckbox
                  key={channel.id}
                  id={channel.id}
                  name={channel.name}
                  nameEn={channel.slug}
                  color={channel.color}
                  checked={isChannelSelected(channel.id)}
                  onChange={toggleChannel as (id: ChannelId) => void}
                />
              ))
            )}
          </div>
        </div>
      )}
    </div>
  )
}
