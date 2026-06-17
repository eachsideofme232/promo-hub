// Filter components barrel export

export { FilterProvider, useFilterContext, STATUSES } from './FilterProvider'
export type { FilterState, FilterContextValue, ChannelId } from './FilterProvider'

// Channel data now comes from ChannelProvider (single source of truth)
export { ChannelProvider, useChannels, useChannel } from '../providers/ChannelProvider'

export { ChannelFilter } from './ChannelFilter'
export { ChannelCheckbox } from './ChannelCheckbox'
export { StatusFilter } from './StatusFilter'
export { DateRangeFilter } from './DateRangeFilter'
export { FilterSidebar, MobileFilterButton } from './FilterSidebar'

export {
  useFilters,
  useStatus,
  useStatuses,
  useFilterSummary,
  usePromotionVisibility,
} from './useFilters'
