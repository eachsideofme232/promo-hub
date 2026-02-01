// Promotion queries
// TODO: Implement with Supabase

import type { SupabaseClient } from '@supabase/supabase-js'

export interface GetPromotionsParams {
  teamId: string
  channelIds?: string[]
  status?: 'planned' | 'active' | 'ended' | 'cancelled'
  page?: number
  limit?: number
}

export async function getPromotions(
  supabase: SupabaseClient,
  params: GetPromotionsParams
) {
  // TODO: Implement query with RLS
  // const { data, error } = await supabase
  //   .from('promotions')
  //   .select('*')
  //   .eq('team_id', params.teamId)
  //   .order('start_date', { ascending: false })

  return { data: [], error: null }
}

export async function getPromotionById(
  supabase: SupabaseClient,
  id: string
) {
  // TODO: Implement query with RLS
  return { data: null, error: null }
}

export async function createPromotion(
  supabase: SupabaseClient,
  promotion: unknown
) {
  // TODO: Implement mutation with RLS
  return { data: null, error: null }
}

export async function updatePromotion(
  supabase: SupabaseClient,
  id: string,
  updates: unknown
) {
  // TODO: Implement mutation with RLS
  return { data: null, error: null }
}

export async function deletePromotion(
  supabase: SupabaseClient,
  id: string
) {
  // TODO: Implement mutation with RLS
  return { data: null, error: null }
}
