# Phase 1: Foundation - Research

**Researched:** 2026-02-17
**Domain:** Authentication, multi-tenant isolation (RLS), Korean localization, channel management
**Confidence:** HIGH

## Summary

Phase 1 delivers the security and localization foundation that every subsequent phase depends on. The existing codebase has roughly 55% of the work done -- Supabase Auth clients, middleware, login/signup pages, database migrations with RLS policies, seed data, and utility functions for Korean dates/currency are all implemented. However, the current code has critical gaps: API routes are stubs, team creation is not automated on signup, channel IDs are inconsistent (slugs vs UUIDs), and there is no i18n framework for systematic Korean localization.

The key architectural decision for Phase 1 is **auto-creating a personal team on signup** via a PostgreSQL trigger, so new users immediately land in a team-scoped dashboard without a manual "create team" step. This is the standard Supabase multi-tenant pattern and avoids the "empty state after signup" anti-pattern.

For Korean localization, the recommended approach is **next-intl without i18n routing** (single locale setup). Since PromoHub is Korean-first, there is no need for `[locale]` path segments. The existing `packages/utils/src/date.ts` and `packages/utils/src/currency.ts` already handle Korean date/currency formatting correctly and should be preserved as the primary formatting layer, with next-intl providing the message catalog and server component integration.

**Primary recommendation:** Wire up the existing Supabase Auth + RLS foundation to real API routes, add auto-team-creation on signup, set up next-intl for Korean UI strings, and build a channels management page. Most of the heavy lifting (migrations, types, queries, auth clients) is already done.

## Standard Stack

### Core (Phase 1 Specific)

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| `@supabase/ssr` | 0.5.x (existing) | SSR auth cookie handling | Already implemented. Manages session cookies across browser, server, and middleware contexts. |
| `@supabase/supabase-js` | 2.45.x (existing) | Supabase client | Already implemented. Provides auth, database queries, RLS integration. |
| `next-intl` | 4.8.x | Korean i18n messages | Standard for Next.js App Router i18n. Works without routing (single locale). Server Component support. |
| `zod` | 3.23.x (existing) | Validation schemas | Already implemented with Korean error messages. Used for all API input validation. |
| `date-fns` | 3.6.x (existing) | Date formatting | Already implemented with Korean locale. `formatDateKR()` and `formatDateRange()` work correctly. |
| `react-hook-form` | 7.71.x (NEW) | Form management | Uncontrolled forms minimize re-renders. Zod integration via `@hookform/resolvers`. |
| `@hookform/resolvers` | 5.2.x (NEW) | Zod-to-RHF bridge | Connects existing Zod schemas to react-hook-form. |
| `sonner` | 2.0.x (NEW) | Toast notifications | Lightweight. "Team created", "Channel added", "Login failed" feedback. |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `nuqs` | 2.8.x (NEW, optional) | URL state management | Shareable filter URLs. Could defer to Phase 3 (Calendar Views). |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| next-intl (single locale) | Hardcoded Korean strings | Hardcoded strings work now but make future English support painful. next-intl setup cost is low. |
| next-intl | next-i18next | next-i18next is Pages Router only. Not compatible with App Router. |
| react-hook-form | Current manual state | Manual `useState` per field works for simple forms but scales poorly for channel management CRUD. |
| Auto-team via trigger | Manual team creation page | Trigger removes onboarding friction. Users reach dashboard immediately after signup. |

### Installation (Phase 1 additions only)

```bash
# i18n
npm install next-intl

# Forms (upgrade from manual useState)
npm install react-hook-form @hookform/resolvers

# Toast notifications
npm install sonner
```

## Architecture Patterns

### Recommended Structure Changes for Phase 1

```
apps/web/src/
├── app/
│   ├── (auth)/
│   │   ├── login/page.tsx          # EXISTS - works
│   │   └── signup/page.tsx         # EXISTS - works
│   ├── (dashboard)/
│   │   ├── layout.tsx              # EXISTS - needs team context provider
│   │   ├── calendar/page.tsx       # EXISTS - needs API connection (Phase 3)
│   │   ├── promotions/page.tsx     # EXISTS - needs API connection (Phase 4)
│   │   ├── channels/page.tsx       # NEW - channel management CRUD
│   │   └── settings/
│   │       └── page.tsx            # EXISTS - scaffold
│   └── api/
│       ├── auth/callback/route.ts  # EXISTS - works
│       ├── channels/route.ts       # NEW - GET/POST channels
│       ├── channels/[id]/route.ts  # NEW - PATCH/DELETE channel
│       └── teams/route.ts          # EXISTS (stub) - needs implementation
├── components/
│   ├── channels/                   # NEW
│   │   ├── ChannelList.tsx         # Channel management table
│   │   ├── ChannelForm.tsx         # Add/edit channel form
│   │   └── ChannelCard.tsx         # Channel display card
│   └── providers/                  # NEW
│       └── TeamProvider.tsx        # Current team context
├── hooks/
│   └── useTeam.ts                  # NEW - current team hook
├── i18n/
│   └── request.ts                  # NEW - next-intl config
└── messages/
    └── ko.json                     # NEW - Korean UI strings
```

### Pattern 1: Auto-Create Team on Signup (PostgreSQL Trigger)

**What:** When a user signs up via Supabase Auth, a PostgreSQL trigger automatically creates a personal team and adds the user as owner. This eliminates the "create your first team" step from onboarding.

**When to use:** Every new user signup.

**Why:** Standard Supabase multi-tenant pattern. Prevents the "empty dashboard" problem where a user signs up but cannot do anything because they have no team.

**Confidence:** HIGH -- verified via Supabase official docs and community patterns.

```sql
-- Source: Supabase docs (managing-user-data) + community patterns
-- Migration: supabase/migrations/XXXXXXX_auto_create_team.sql

CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
DECLARE
  new_team_id UUID;
BEGIN
  -- Create a personal team for the new user
  INSERT INTO public.teams (name, slug)
  VALUES (
    COALESCE(NEW.raw_user_meta_data->>'name', split_part(NEW.email, '@', 1)) || '의 팀',
    'team-' || substr(NEW.id::text, 1, 8)
  )
  RETURNING id INTO new_team_id;

  -- Add user as owner of their team
  INSERT INTO public.team_members (team_id, user_id, role)
  VALUES (new_team_id, NEW.id, 'owner');

  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger on auth.users insert
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW
  EXECUTE FUNCTION public.handle_new_user();
```

**Critical notes:**
- `SECURITY DEFINER` is required because the trigger runs as the postgres role, not the user
- The trigger must not fail or it blocks signup entirely. Test thoroughly.
- Team slug uses first 8 chars of user UUID for uniqueness

### Pattern 2: Team Context Provider

**What:** A React context that provides the current user's active team to all dashboard components. Fetched once on dashboard layout mount, cached for the session.

**When to use:** Every dashboard page needs `teamId` for scoped queries.

```typescript
// apps/web/src/components/providers/TeamProvider.tsx
'use client'

import { createContext, useContext, useEffect, useState } from 'react'
import { createClient } from '@/lib/supabase/client'
import type { Team } from '@promohub/types'

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

export function TeamProvider({ children }: { children: React.ReactNode }) {
  const [team, setTeam] = useState<Team | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    async function fetchTeam() {
      const supabase = createClient()
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) return

      // Get user's first team (auto-created on signup)
      const { data, error } = await supabase
        .from('team_members')
        .select('team_id, teams(*)')
        .eq('user_id', user.id)
        .limit(1)
        .single()

      if (error) {
        setError(error)
      } else if (data) {
        setTeam(data.teams as unknown as Team)
      }
      setIsLoading(false)
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
  return useContext(TeamContext)
}
```

### Pattern 3: next-intl Without Routing (Korean-Only Setup)

**What:** Use next-intl for Korean UI strings without `[locale]` path segments. Single locale configuration that always returns `'ko'`.

**When to use:** Every user-facing string in the app.

**Why:** Korean-only for v1 (explicitly stated in requirements). The "without i18n routing" setup is the simplest next-intl configuration. It requires no changes to the existing App Router structure (no `[locale]` directory).

**Confidence:** HIGH -- verified via next-intl official docs ("App Router setup without i18n routing").

```typescript
// apps/web/src/i18n/request.ts
// Source: https://next-intl.dev/docs/getting-started/app-router/without-i18n-routing
import { getRequestConfig } from 'next-intl/server'

export default getRequestConfig(async () => ({
  locale: 'ko',
  messages: (await import('../../messages/ko.json')).default,
  timeZone: 'Asia/Seoul',
  now: new Date(),
  formats: {
    dateTime: {
      short: { day: 'numeric', month: 'short', year: 'numeric' },
      long: { day: 'numeric', month: 'long', year: 'numeric', weekday: 'long' },
    },
    number: {
      currency: { style: 'currency', currency: 'KRW', maximumFractionDigits: 0 },
    },
  },
}))
```

```json
// apps/web/messages/ko.json (partial example)
{
  "common": {
    "save": "저장",
    "cancel": "취소",
    "delete": "삭제",
    "edit": "수정",
    "create": "생성",
    "loading": "로딩 중...",
    "error": "오류가 발생했습니다",
    "confirm": "확인",
    "back": "뒤로"
  },
  "auth": {
    "login": "로그인",
    "signup": "회원가입",
    "logout": "로그아웃",
    "email": "이메일",
    "password": "비밀번호",
    "passwordConfirm": "비밀번호 확인",
    "loginError": "이메일 또는 비밀번호가 올바르지 않습니다.",
    "signupSuccess": "회원가입이 완료되었습니다",
    "checkEmail": "{email}로 인증 링크를 보냈습니다."
  },
  "channels": {
    "title": "채널 관리",
    "addChannel": "채널 추가",
    "editChannel": "채널 수정",
    "deleteChannel": "채널 삭제",
    "name": "채널명",
    "slug": "슬러그",
    "color": "색상",
    "active": "활성",
    "inactive": "비활성",
    "preseeded": "기본 채널",
    "custom": "사용자 채널",
    "confirmDelete": "이 채널을 삭제하시겠습니까?"
  },
  "nav": {
    "calendar": "캘린더",
    "promotions": "프로모션",
    "channels": "채널",
    "products": "상품",
    "settings": "설정"
  }
}
```

### Pattern 4: Channel Management with Pre-seeded + Custom

**What:** Channels table contains both pre-seeded Korean e-commerce channels (system-level, read-only) and custom channels (team-scoped, editable). The `channels` table needs a `team_id` column (nullable) to distinguish: `NULL` = system channel, non-NULL = custom channel.

**When to use:** Phase 1 requirement PROD-03: "User can manage channels (pre-seeded Korean channels + custom)."

**Schema change needed:**

```sql
-- Add team_id to channels for custom channel support
ALTER TABLE channels ADD COLUMN team_id UUID REFERENCES teams(id) ON DELETE CASCADE;

-- Update RLS: system channels (team_id IS NULL) visible to all,
-- custom channels visible only to their team
DROP POLICY "Channels are viewable by authenticated users" ON channels;

CREATE POLICY "System channels visible to all authenticated users"
  ON channels FOR SELECT TO authenticated
  USING (team_id IS NULL);

CREATE POLICY "Custom channels visible to team members"
  ON channels FOR SELECT TO authenticated
  USING (
    team_id IN (
      SELECT tm.team_id FROM team_members tm
      WHERE tm.user_id = auth.uid()
    )
  );

CREATE POLICY "Team members can create custom channels"
  ON channels FOR INSERT TO authenticated
  WITH CHECK (
    team_id IS NOT NULL AND
    team_id IN (
      SELECT tm.team_id FROM team_members tm
      WHERE tm.user_id = auth.uid()
      AND tm.role IN ('owner', 'admin', 'member')
    )
  );

CREATE POLICY "Team members can update their custom channels"
  ON channels FOR UPDATE TO authenticated
  USING (
    team_id IS NOT NULL AND
    team_id IN (
      SELECT tm.team_id FROM team_members tm
      WHERE tm.user_id = auth.uid()
      AND tm.role IN ('owner', 'admin', 'member')
    )
  );

CREATE POLICY "Admins can delete their custom channels"
  ON channels FOR DELETE TO authenticated
  USING (
    team_id IS NOT NULL AND
    team_id IN (
      SELECT tm.team_id FROM team_members tm
      WHERE tm.user_id = auth.uid()
      AND tm.role IN ('owner', 'admin')
    )
  );
```

**Confidence:** HIGH -- straightforward RLS extension. Existing seed data has `team_id = NULL` which makes them system channels automatically.

### Pattern 5: API Route with Auth + Team Scoping

**What:** Standard pattern for all Phase 1 API routes. Verify auth, get team, execute query, return response.

**When to use:** Every API route.

```typescript
// Source: Existing code pattern from CLAUDE.md + @supabase/ssr Context7 docs
import { createClient } from '@/lib/supabase/server'
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const supabase = await createClient()

  // 1. Verify authentication
  const { data: { user }, error: authError } = await supabase.auth.getUser()
  if (authError || !user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  // 2. Get user's team (RLS handles scoping, but we need team_id for custom queries)
  const { data: membership, error: teamError } = await supabase
    .from('team_members')
    .select('team_id')
    .eq('user_id', user.id)
    .limit(1)
    .single()

  if (teamError || !membership) {
    return NextResponse.json({ error: 'No team found' }, { status: 403 })
  }

  // 3. Execute team-scoped query (RLS also enforces this)
  const { data, error } = await supabase
    .from('channels')
    .select('*')
    .or(`team_id.is.null,team_id.eq.${membership.team_id}`)
    .order('name')

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }

  return NextResponse.json({ data })
}
```

### Anti-Patterns to Avoid

- **Channel ID slug vs UUID confusion:** The FilterProvider uses string slugs (`'oliveyoung'`) while the database uses UUIDs. Phase 1 must unify to UUIDs. Fetch channels from the API and use database IDs consistently.

- **Hardcoded team ID:** The current `DEMO_TEAM_ID = '00000000-...'` pattern in promotion pages must be replaced with the TeamProvider context.

- **Service role key in API routes:** Never use `SUPABASE_SECRET_KEY` in routes that handle user requests. Always use the anon/publishable key with authenticated session cookies. RLS enforces isolation.

- **Skipping middleware session refresh:** The `updateSession()` call in middleware is mandatory. Without it, server components cannot read the user's session from cookies. The existing middleware implementation is correct.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Korean date formatting | Custom formatters | `packages/utils/src/date.ts` (existing) | Already implemented with date-fns and ko locale. Correct YYYY-MM-DD format. |
| Korean currency formatting | Custom KRW formatter | `packages/utils/src/currency.ts` (existing) | Already implements won/man/eok formatting. Handles the 1,000 / 1만 / 1억 breakpoints. |
| Auth session management | Custom JWT handling | `@supabase/ssr` (existing) | Cookie-based session with automatic refresh. Already implemented in middleware, server, and browser clients. |
| Multi-tenant isolation | Application-layer WHERE clauses | Supabase RLS policies (existing) | Already implemented in all migrations. Defense-in-depth at database layer. |
| Form validation messages | Custom error strings | Zod schemas in `packages/utils/src/validation.ts` (existing) | Already has Korean error messages for all form fields. |
| UI component primitives | Custom buttons/dialogs | Radix UI (existing) + shadcn/ui (recommended) | Radix already partially adopted. shadcn/ui provides pre-built Tailwind components. |
| Toast notifications | Custom notification system | Sonner | 2kb, no setup, works with shadcn/ui. |

**Key insight:** Phase 1 is primarily about *wiring existing pieces together*, not building new ones. The database schema, RLS policies, auth clients, types, validation, and date/currency utils are all done. The work is connecting them to real API routes and building the channel management UI.

## Common Pitfalls

### Pitfall 1: Signup Trigger Failure Blocks Registration

**What goes wrong:** The `handle_new_user()` trigger fails (e.g., unique slug collision, null email), which rolls back the entire `auth.users` INSERT, preventing the user from signing up.
**Why it happens:** Triggers run in the same transaction as the INSERT. Any error cascades.
**How to avoid:**
1. Use `COALESCE` for all nullable fields (email could theoretically be null for phone auth)
2. Generate slug from UUID (guaranteed unique) not from username (could collide)
3. Test the trigger with edge cases: very long emails, special characters, null metadata
4. Add exception handling in the PL/pgSQL function
**Warning signs:** Users report "signup failed" with no clear error message.

### Pitfall 2: Channel UUID vs Slug Mismatch

**What goes wrong:** Frontend filters send channel slugs (`'oliveyoung'`) but API/database expects UUIDs (`'c1000000-...'`). Filters silently fail to match anything.
**Why it happens:** The existing `FilterProvider.tsx` defines channels as static objects with slug IDs. The database uses UUID primary keys.
**How to avoid:**
1. Fetch channels from API on app load (not hardcoded)
2. Use channel UUID as the canonical identifier everywhere
3. Keep slug only for URL-friendly display and lookup
4. Update FilterProvider to accept dynamic channels from API
**Warning signs:** Filters show channels but selecting them shows no promotions.

### Pitfall 3: next-intl Plugin Configuration Missing

**What goes wrong:** Server components throw "unable to find next-intl configuration" error at runtime.
**Why it happens:** next-intl requires a Next.js plugin in `next.config.ts` and a `i18n/request.ts` config file. Missing either causes the error.
**How to avoid:**
1. Add `createNextIntlPlugin` to `next.config.ts`
2. Create `src/i18n/request.ts` with `getRequestConfig`
3. Wrap root layout with `NextIntlClientProvider`
**Warning signs:** Build succeeds but pages crash at runtime with "Cannot read properties of undefined (reading 'messages')".

### Pitfall 4: RLS Policy on Channels Breaks After team_id Addition

**What goes wrong:** After adding `team_id` to channels table, the existing seed data (which has `team_id = NULL`) becomes invisible because the new RLS policy only checks team membership.
**Why it happens:** `WHERE team_id IN (SELECT team_id FROM team_members WHERE ...)` returns false when `team_id IS NULL`.
**How to avoid:**
1. Use separate policies for system channels (`team_id IS NULL`) and custom channels
2. Test that pre-seeded channels are still visible after migration
3. Seed data migration must run before RLS policy changes
**Warning signs:** After migration, the channels list is empty for all users.

### Pitfall 5: Missing `await` on `cookies()` in Next.js 14+

**What goes wrong:** Server components or API routes fail with "cookies() should be awaited" error.
**Why it happens:** In Next.js 14+, `cookies()` from `next/headers` returns a Promise. The existing codebase correctly uses `await cookies()` but new code might forget.
**How to avoid:** Always `const cookieStore = await cookies()` in server components and API routes.
**Warning signs:** Build warnings about unawaited promises, runtime errors in server components.

### Pitfall 6: Team Context Not Available During SSR

**What goes wrong:** Server components try to read team context but it's only available after client-side hydration.
**Why it happens:** TeamProvider uses `useEffect` (client-only). Server components render before client hydration.
**How to avoid:**
1. For server components that need team_id, query Supabase directly using the server client
2. Use TeamProvider only for client components
3. Consider passing team_id from server layout to client components via props
**Warning signs:** Hydration mismatch errors, "team is null" in server-rendered content.

## Code Examples

### Auto-Team Creation Migration (Complete)

```sql
-- Source: Supabase official docs + verified community patterns
-- File: supabase/migrations/XXXXXXX_auto_create_team.sql

-- Function to handle new user registration
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  new_team_id UUID;
  team_name TEXT;
  team_slug TEXT;
BEGIN
  -- Generate team name from user metadata or email
  team_name := COALESCE(
    NEW.raw_user_meta_data->>'name',
    split_part(NEW.email, '@', 1)
  ) || '의 팀';

  -- Generate unique slug from user UUID
  team_slug := 'team-' || substr(NEW.id::text, 1, 8);

  -- Create the team
  INSERT INTO public.teams (name, slug)
  VALUES (team_name, team_slug)
  RETURNING id INTO new_team_id;

  -- Add user as owner
  INSERT INTO public.team_members (team_id, user_id, role)
  VALUES (new_team_id, NEW.id, 'owner');

  RETURN NEW;
EXCEPTION
  WHEN OTHERS THEN
    -- Log error but don't block signup
    RAISE WARNING 'Failed to create team for user %: %', NEW.id, SQLERRM;
    RETURN NEW;
END;
$$;

-- Create trigger
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW
  EXECUTE FUNCTION public.handle_new_user();
```

### next-intl Configuration for Next.js (Complete)

```typescript
// apps/web/next.config.ts
// Source: https://next-intl.dev/docs/getting-started/app-router/without-i18n-routing
import createNextIntlPlugin from 'next-intl/plugin'

const withNextIntl = createNextIntlPlugin()

/** @type {import('next').NextConfig} */
const nextConfig = {
  // existing config...
}

export default withNextIntl(nextConfig)
```

```typescript
// apps/web/src/i18n/request.ts
import { getRequestConfig } from 'next-intl/server'

export default getRequestConfig(async () => ({
  locale: 'ko',
  messages: (await import('../../messages/ko.json')).default,
  timeZone: 'Asia/Seoul',
  now: new Date(),
}))
```

```tsx
// apps/web/src/app/layout.tsx (root layout update)
import { NextIntlClientProvider } from 'next-intl'
import { getLocale, getMessages } from 'next-intl/server'

export default async function RootLayout({ children }: { children: React.ReactNode }) {
  const locale = await getLocale()
  const messages = await getMessages()

  return (
    <html lang={locale}>
      <body>
        <NextIntlClientProvider messages={messages}>
          {children}
        </NextIntlClientProvider>
      </body>
    </html>
  )
}
```

### Channel API Route (Complete)

```typescript
// apps/web/src/app/api/channels/route.ts
import { createClient } from '@/lib/supabase/server'
import { NextRequest, NextResponse } from 'next/server'
import { z } from 'zod'

const createChannelSchema = z.object({
  name: z.string().min(1).max(50),
  slug: z.string().min(1).max(50).regex(/^[a-z0-9-]+$/),
  color: z.string().regex(/^#[0-9A-Fa-f]{6}$/),
})

// GET /api/channels - List all channels (system + team custom)
export async function GET() {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  const { data: membership } = await supabase
    .from('team_members')
    .select('team_id')
    .eq('user_id', user.id)
    .limit(1)
    .single()

  if (!membership) {
    return NextResponse.json({ error: 'No team found' }, { status: 403 })
  }

  // Fetch system channels (team_id IS NULL) and team's custom channels
  const { data, error } = await supabase
    .from('channels')
    .select('*')
    .or(`team_id.is.null,team_id.eq.${membership.team_id}`)
    .order('name')

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }

  return NextResponse.json({ data })
}

// POST /api/channels - Create a custom channel
export async function POST(request: NextRequest) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  const { data: membership } = await supabase
    .from('team_members')
    .select('team_id, role')
    .eq('user_id', user.id)
    .limit(1)
    .single()

  if (!membership) {
    return NextResponse.json({ error: 'No team found' }, { status: 403 })
  }

  const body = await request.json()
  const parsed = createChannelSchema.safeParse(body)
  if (!parsed.success) {
    return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 })
  }

  const { data, error } = await supabase
    .from('channels')
    .insert({
      ...parsed.data,
      team_id: membership.team_id,
      is_active: true,
    })
    .select()
    .single()

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }

  return NextResponse.json({ data }, { status: 201 })
}
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `uuid_generate_v4()` | `gen_random_uuid()` | PostgreSQL 13+ | Already updated in all migrations. No action needed. |
| `SUPABASE_ANON_KEY` | `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY` | Supabase 2025 | Already updated in existing client code. |
| `getSession()` for auth checks | `getUser()` for auth checks | Supabase SSR best practice | `getUser()` validates the JWT server-side. `getSession()` only reads the local token. Existing code correctly uses `getUser()`. |
| Pages Router middleware | App Router middleware | Next.js 13+ | Existing middleware uses App Router pattern correctly. |
| tailwind.config.js | CSS @theme directive | Tailwind v4 | Not yet migrated. Existing v3 config works. Can defer to later phase. |

**Deprecated/outdated in existing code:**
- `CookieOptions` type import from `@supabase/ssr`: Still works but may be removed in future versions. The existing server.ts and middleware.ts use it correctly.

## Open Questions

1. **Team switching UI for multi-team users**
   - What we know: The auto-team trigger creates one team per user. Later, users may be invited to other teams.
   - What's unclear: Should Phase 1 include a team switcher in the dashboard? Or defer to Phase 8 (Team Management)?
   - Recommendation: Defer team switching to Phase 8. Phase 1 assumes one team per user. The TeamProvider fetches the first (and only) team. This is sufficient for launch.

2. **Channel promo types per channel**
   - What we know: Requirement LOC-02 says "channel-specific promo types." Current schema has a single `discount_type` enum on promotions.
   - What's unclear: Does each channel need its own list of supported promo types? (e.g., OliveYoung supports BigBang, Coupang supports RocketDeal)
   - Recommendation: Add a `promo_types` JSONB column to channels table storing an array of supported promo type slugs per channel. Pre-seed Korean channels with their specific types. Defer enforcement to Phase 4 (Promotion CRUD). For Phase 1, just store the data.

3. **Supabase project setup state**
   - What we know: Migrations exist locally. `.env.example` lists required variables.
   - What's unclear: Is a Supabase project already created and linked? Are environment variables configured?
   - Recommendation: Phase 1 Plan 01 should include Supabase project setup verification as the first task.

4. **next-intl version compatibility with Next.js 14.2**
   - What we know: The codebase uses Next.js 14.2. next-intl 4.x supports Next.js 13+.
   - What's unclear: Are there any specific 14.2 incompatibilities with next-intl 4.8.x?
   - Recommendation: LOW risk. next-intl 4.x explicitly supports Next.js 14. If issues arise, fall back to next-intl 3.x which has identical API for single-locale setup.

## Sources

### Primary (HIGH confidence)
- Context7 `/supabase/ssr` -- SSR client setup, middleware pattern, cookie handling, session refresh flow
- Context7 `/amannn/next-intl` -- App Router setup, `getRequestConfig`, single-locale without routing, server component translations
- Context7 `/websites/supabase` -- RLS policies with `auth.jwt()`, `SECURITY DEFINER` function for team membership, performance optimization with `select` wrapper
- Existing codebase analysis -- All files in `apps/web/src/lib/supabase/`, `supabase/migrations/`, `packages/types/`, `packages/utils/`, `packages/db/queries/`

### Secondary (MEDIUM confidence)
- [Supabase Managing User Data docs](https://supabase.com/docs/guides/auth/managing-user-data) -- Trigger pattern for auto-creating user data on signup
- [Supabase Triggers docs](https://supabase.com/docs/guides/database/postgres/triggers) -- PostgreSQL trigger syntax and SECURITY DEFINER usage
- [next-intl "App Router without i18n routing" docs](https://next-intl.dev/docs/getting-started/app-router/without-i18n-routing) -- Single-locale setup guide
- [Supabase RLS docs](https://supabase.com/docs/guides/database/postgres/row-level-security) -- RLS policy patterns, auth.jwt() usage
- [Supabase Discussion #306](https://github.com/orgs/supabase/discussions/306) -- Community patterns for signup triggers

### Tertiary (LOW confidence)
- Stack research from `.planning/research/STACK.md` -- Version numbers for recommended libraries (verified via npm where possible)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- Supabase Auth, RLS, and next-intl are well-documented. Existing code is 55% complete.
- Architecture: HIGH -- Multi-tenant RLS pattern is standard Supabase. Auto-team trigger is documented community pattern.
- Pitfalls: HIGH -- Channel UUID mismatch is directly observed in codebase. Trigger failure risk is documented in Supabase docs.
- Korean localization: HIGH -- `packages/utils` already handles dates and currency correctly. next-intl single-locale setup is documented.
- Channel management: MEDIUM -- Custom channel RLS extension is straightforward but the `promo_types` JSONB pattern needs validation during implementation.

**Research date:** 2026-02-17
**Valid until:** 2026-03-17 (stable domain, 30-day validity)
