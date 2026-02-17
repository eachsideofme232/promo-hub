import { createClient } from '@/lib/supabase/server'
import { NextRequest, NextResponse } from 'next/server'
import { z } from 'zod'

const updateChannelSchema = z.object({
  name: z.string().min(1, '채널명을 입력해주세요').max(50, '채널명은 50자 이하여야 합니다').trim().optional(),
  slug: z.string().min(1).max(50).regex(/^[a-z0-9-]+$/, '슬러그는 영문 소문자, 숫자, 하이픈만 사용 가능합니다').trim().optional(),
  color: z.string().regex(/^#[0-9A-Fa-f]{6}$/, '올바른 색상 코드를 입력해주세요').optional(),
  isActive: z.boolean().optional(),
  promoTypes: z.array(z.string()).optional(),
})

// Helper: Verify auth and get team membership
async function getAuthContext(supabase: Awaited<ReturnType<typeof createClient>>) {
  const { data: { user }, error: authError } = await supabase.auth.getUser()
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

  return { user, membership }
}

// Helper: Verify the channel exists and is editable by this team
async function verifyChannelOwnership(
  supabase: Awaited<ReturnType<typeof createClient>>,
  channelId: string,
  teamId: string
) {
  const { data: existing, error } = await supabase
    .from('channels')
    .select('team_id')
    .eq('id', channelId)
    .single()

  if (error || !existing) {
    return { error: NextResponse.json({ error: '채널을 찾을 수 없습니다' }, { status: 404 }) }
  }

  if (existing.team_id === null) {
    return { error: NextResponse.json({ error: '시스템 채널은 수정할 수 없습니다' }, { status: 403 }) }
  }

  if (existing.team_id !== teamId) {
    return { error: NextResponse.json({ error: '접근 권한이 없습니다' }, { status: 403 }) }
  }

  return { existing }
}

// PATCH /api/channels/[id] - Update a custom channel
export async function PATCH(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params
  const supabase = await createClient()

  // 1. Verify authentication and team membership
  const auth = await getAuthContext(supabase)
  if ('error' in auth && auth.error) return auth.error
  const { membership } = auth as { membership: { team_id: string; role: string }; user: unknown }

  // 2. Verify channel ownership (not a system channel, belongs to this team)
  const ownership = await verifyChannelOwnership(supabase, id, membership.team_id)
  if ('error' in ownership && ownership.error) return ownership.error

  // 3. Validate request body
  let body: unknown
  try {
    body = await request.json()
  } catch {
    return NextResponse.json({ error: '올바른 JSON 형식이 아닙니다' }, { status: 400 })
  }

  const parsed = updateChannelSchema.safeParse(body)
  if (!parsed.success) {
    return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 })
  }

  // 4. Map camelCase input to snake_case for DB
  const updateData: Record<string, unknown> = {}
  if (parsed.data.name !== undefined) updateData.name = parsed.data.name
  if (parsed.data.slug !== undefined) updateData.slug = parsed.data.slug
  if (parsed.data.color !== undefined) updateData.color = parsed.data.color
  if (parsed.data.isActive !== undefined) updateData.is_active = parsed.data.isActive
  if (parsed.data.promoTypes !== undefined) updateData.promo_types = parsed.data.promoTypes

  if (Object.keys(updateData).length === 0) {
    return NextResponse.json({ error: '수정할 항목이 없습니다' }, { status: 400 })
  }

  // 5. Update the channel
  const { data, error } = await supabase
    .from('channels')
    .update(updateData)
    .eq('id', id)
    .select()
    .single()

  if (error) {
    if (error.code === '23505') {
      return NextResponse.json(
        { error: '이미 사용 중인 슬러그입니다' },
        { status: 409 }
      )
    }
    return NextResponse.json({ error: error.message }, { status: 500 })
  }

  // 6. Return updated channel
  const channel = {
    id: data.id,
    name: data.name,
    slug: data.slug,
    logoUrl: data.logo_url,
    color: data.color,
    isActive: data.is_active,
    isSystem: false,
    teamId: data.team_id,
    promoTypes: data.promo_types ?? [],
    createdAt: data.created_at,
  }

  return NextResponse.json({ data: channel })
}

// DELETE /api/channels/[id] - Delete a custom channel
export async function DELETE(
  _request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params
  const supabase = await createClient()

  // 1. Verify authentication and team membership
  const auth = await getAuthContext(supabase)
  if ('error' in auth && auth.error) return auth.error
  const { membership } = auth as { membership: { team_id: string; role: string }; user: unknown }

  // 2. Verify channel ownership (not a system channel, belongs to this team)
  const ownership = await verifyChannelOwnership(supabase, id, membership.team_id)
  if ('error' in ownership && ownership.error) return ownership.error

  // 3. Delete the channel
  const { error } = await supabase
    .from('channels')
    .delete()
    .eq('id', id)

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }

  // 4. Return 204 No Content
  return new NextResponse(null, { status: 204 })
}
