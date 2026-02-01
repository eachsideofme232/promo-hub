// Calendar queries
// TODO: Implement with Supabase

import type { SupabaseClient } from '@supabase/supabase-js'

export interface GetCalendarPromotionsParams {
  teamId: string
  startDate: string
  endDate: string
  channelIds?: string[]
}

export async function getCalendarPromotions(
  supabase: SupabaseClient,
  params: GetCalendarPromotionsParams
) {
  // TODO: Implement query with RLS
  // Query promotions that overlap with the given date range
  // const { data, error } = await supabase
  //   .from('promotions')
  //   .select('*')
  //   .eq('team_id', params.teamId)
  //   .lte('start_date', params.endDate)
  //   .gte('end_date', params.startDate)

  return { data: [], error: null }
}
