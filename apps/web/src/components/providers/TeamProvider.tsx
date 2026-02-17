'use client'

import { createContext, useContext, useEffect, useState, type ReactNode } from 'react'
import { createClient } from '@/lib/supabase/client'

interface Team {
  id: string
  name: string
  slug: string
  logoUrl: string | null
  createdAt: string
  updatedAt: string
}

interface TeamContextValue {
  team: Team | null
  teamId: string | null
  isLoading: boolean
  error: Error | null
}

const TeamContext = createContext<TeamContextValue>({
  team: null,
  teamId: null,
  isLoading: true,
  error: null,
})

export function TeamProvider({ children }: { children: ReactNode }) {
  const [team, setTeam] = useState<Team | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    async function fetchTeam() {
      try {
        const supabase = createClient()
        const { data: { user } } = await supabase.auth.getUser()
        if (!user) {
          setIsLoading(false)
          return
        }

        const { data, error: queryError } = await supabase
          .from('team_members')
          .select('team_id, teams(id, name, slug, logo_url, created_at, updated_at)')
          .eq('user_id', user.id)
          .limit(1)
          .single()

        if (queryError) {
          setError(new Error(queryError.message))
        } else if (data?.teams) {
          const t = data.teams as unknown as Record<string, unknown>
          setTeam({
            id: t.id as string,
            name: t.name as string,
            slug: t.slug as string,
            logoUrl: t.logo_url as string | null,
            createdAt: t.created_at as string,
            updatedAt: t.updated_at as string,
          })
        }
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Failed to fetch team'))
      } finally {
        setIsLoading(false)
      }
    }
    fetchTeam()
  }, [])

  return (
    <TeamContext.Provider value={{ team, teamId: team?.id ?? null, isLoading, error }}>
      {children}
    </TeamContext.Provider>
  )
}

export function useTeam() {
  const context = useContext(TeamContext)
  if (context === undefined) {
    throw new Error('useTeam must be used within a TeamProvider')
  }
  return context
}
