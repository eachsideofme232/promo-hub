import { NextRequest, NextResponse } from 'next/server'
import { createClient } from '@/lib/supabase/server'
import { teamSchema } from '@promohub/utils'

interface TeamRow {
  id: string
  name: string
  slug: string
  logo_url: string | null
  created_at: string
  updated_at: string
}

// GET /api/teams - List the caller's teams with their role
export async function GET() {
  const supabase = await createClient()

  const {
    data: { user },
    error: authError,
  } = await supabase.auth.getUser()
  if (authError || !user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  const { data, error } = await supabase
    .from('team_members')
    .select('role, teams(id, name, slug, logo_url, created_at, updated_at)')
    .eq('user_id', user.id)

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }

  const teams = (data ?? [])
    .filter((row) => row.teams)
    .map((row) => {
      const team = row.teams as unknown as TeamRow
      return {
        id: team.id,
        name: team.name,
        slug: team.slug,
        logoUrl: team.logo_url,
        role: row.role,
        createdAt: team.created_at,
        updatedAt: team.updated_at,
      }
    })

  return NextResponse.json({ data: teams })
}

// POST /api/teams - Create a team and add the caller as owner
// Uses the create_team_with_owner RPC (SECURITY DEFINER) because a brand-new
// team has no members yet, so direct team_members INSERT would be blocked by RLS.
export async function POST(request: NextRequest) {
  const supabase = await createClient()

  const {
    data: { user },
    error: authError,
  } = await supabase.auth.getUser()
  if (authError || !user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  let body: unknown
  try {
    body = await request.json()
  } catch {
    return NextResponse.json({ error: '올바른 JSON 형식이 아닙니다' }, { status: 400 })
  }

  const parsed = teamSchema.safeParse(body)
  if (!parsed.success) {
    return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 })
  }

  const { data, error } = await supabase.rpc('create_team_with_owner', {
    team_name: parsed.data.name,
    team_slug: parsed.data.slug,
  })

  if (error) {
    if (error.code === '23505') {
      return NextResponse.json({ error: '이미 사용 중인 슬러그입니다' }, { status: 409 })
    }
    return NextResponse.json({ error: error.message }, { status: 500 })
  }

  const team = data as TeamRow
  return NextResponse.json(
    {
      data: {
        id: team.id,
        name: team.name,
        slug: team.slug,
        logoUrl: team.logo_url,
        role: 'owner',
        createdAt: team.created_at,
        updatedAt: team.updated_at,
      },
    },
    { status: 201 }
  )
}
