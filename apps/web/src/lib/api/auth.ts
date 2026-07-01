import { NextResponse } from 'next/server'
import { createClient } from '@/lib/supabase/server'

export type TeamRole = 'owner' | 'admin' | 'member' | 'viewer'

export interface TeamContext {
  supabase: Awaited<ReturnType<typeof createClient>>
  userId: string
  teamId: string
  role: TeamRole
}

/**
 * Verify authentication and resolve the caller's team membership.
 * Returns either a ready-to-use context or an error response.
 */
export async function getTeamContext(): Promise<
  | { context: TeamContext; error?: never }
  | { context?: never; error: NextResponse }
> {
  const supabase = await createClient()

  const {
    data: { user },
    error: authError,
  } = await supabase.auth.getUser()

  if (authError || !user) {
    return { error: NextResponse.json({ error: 'Unauthorized' }, { status: 401 }) }
  }

  const { data: membership, error: teamError } = await supabase
    .from('team_members')
    .select('team_id, role')
    .eq('user_id', user.id)
    .limit(1)
    .single()

  if (teamError || !membership) {
    return { error: NextResponse.json({ error: 'No team found' }, { status: 403 }) }
  }

  return {
    context: {
      supabase,
      userId: user.id,
      teamId: membership.team_id,
      role: membership.role as TeamRole,
    },
  }
}
