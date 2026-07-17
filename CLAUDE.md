# CLAUDE.md - PromoHub Development Guidelines

This document provides essential context for AI assistants working on the PromoHub codebase.

## Project Overview

**PromoHub** is an all-in-one e-commerce platform for small-medium K-beauty/cosmetic companies. Starting with a **Promotion Calendar** as the core feature, it will scale to become a comprehensive e-commerce management platform.

**Target Users**: Brand managers and e-commerce teams at cosmetic companies who need to manage promotions across multiple Korean e-commerce channels.

**Core Philosophy**: Start simple with calendar, scale to full platform.

## Product Roadmap

| Phase | Module | Features |
|-------|--------|----------|
| **Phase 1** | Promotion Calendar | Monthly/weekly/daily views, promo CRUD, team sharing, channel filters, templates, conflict detection |
| **Phase 1** | Core Settings | Team management, channel setup, product/SKU management |
| **Phase 2** | Strategy | Monthly strategy planning, competitor monitoring, P&L simulation |
| **Phase 3** | Advanced | Price monitoring, channel expansion, marketing comms hub, AI agents |

**Current Focus**: Phase 1 - Promotion Calendar

## Technology Stack

| Layer | Technology | Reason |
|-------|------------|--------|
| **Monorepo** | Turborepo | Build cache, workspace management |
| **Frontend** | Next.js 14 (App Router) | SSR + API Routes integrated |
| **Styling** | Tailwind CSS | Rapid development |
| **Database** | Supabase (PostgreSQL) | Auth + DB + Realtime + Storage |
| **ORM** | Drizzle ORM | Type-safe, lightweight |
| **Auth** | Supabase Auth | Social login, team invitations |
| **Payments** | Toss Payments / Stripe | Korea = Toss, Global = Stripe |
| **Deploy** | Vercel | Next.js native |
| **Notifications** | Slack Webhook + Kakao Alimtalk | Korean business environment |
| **Language** | TypeScript (full-stack) | Type safety |

## Directory Structure

```
promohub/
├── apps/
│   ├── web/                           # Main Next.js web app
│   │   ├── src/
│   │   │   ├── app/                   # App Router
│   │   │   │   ├── (auth)/            # Login, signup
│   │   │   │   ├── (dashboard)/       # Main dashboard
│   │   │   │   │   ├── calendar/      # [Phase 1] Calendar views
│   │   │   │   │   ├── promotions/    # [Phase 1] Promo CRUD
│   │   │   │   │   ├── settings/      # Team, billing
│   │   │   │   │   ├── strategy/      # [Phase 2]
│   │   │   │   │   ├── competitors/   # [Phase 2]
│   │   │   │   │   ├── pnl/           # [Phase 2]
│   │   │   │   │   ├── channels/      # [Phase 3]
│   │   │   │   │   ├── pricing/       # [Phase 3]
│   │   │   │   │   └── comms/         # [Phase 3]
│   │   │   │   └── api/               # API routes, webhooks
│   │   │   ├── components/            # UI components
│   │   │   │   ├── layout/            # Sidebar, Header, MobileNav
│   │   │   │   ├── calendar/          # CalendarView, MonthView, WeekView, DayView
│   │   │   │   ├── promotions/        # PromoForm, PromoList, PromoStatusBadge
│   │   │   │   └── common/            # LoadingSpinner, EmptyState, ErrorBoundary
│   │   │   ├── hooks/                 # Custom hooks
│   │   │   └── lib/                   # Utilities, Supabase clients
│   │   │       └── supabase/          # Supabase client utilities
│   │   │           ├── client.ts      # Browser client (use in Client Components)
│   │   │           ├── server.ts      # Server client (use in Server Components/API)
│   │   │           └── middleware.ts  # Session refresh for Next.js middleware
│   │   ├── middleware.ts              # Auth middleware (protect routes)
│   │   └── package.json
│   └── landing/                       # Marketing site
├── packages/
│   ├── db/                            # Schema, migrations, queries
│   │   ├── schema/                    # SQL schema files
│   │   ├── migrations/                # Supabase migrations
│   │   ├── seed/                      # Seed data (channels, demo)
│   │   └── queries/                   # Reusable query functions
│   ├── types/                         # Shared TypeScript types
│   ├── ui/                            # Shared UI components
│   ├── utils/                         # Shared utilities (date, currency, validation)
│   └── config/                        # ESLint, TypeScript configs
├── turbo.json
├── package.json
└── docker-compose.yml
```

## Core Domain Entities

```
Promotion
├── id, title, description
├── channel_id → Channel (Oliveyoung, Coupang, Naver, Kakao, Musinsa)
├── team_id → Team
├── product_ids → Product[] (N:M via promo_products)
├── template_id → PromoTemplate (nullable)
├── status: planned | active | ended | cancelled
├── discount_type: percentage | bogo | coupon | gift | bundle
├── discount_value
├── start_date, end_date
├── memo
└── notifications

Channel: Oliveyoung, Coupang, Naver, Kakao, Musinsa, etc.
Product/SKU: Item management with SKU codes
Team: Multi-user collaboration with roles
PromoTemplate: Recurring promotion patterns (e.g., "Monthly Oliveyoung Sale")
```

## Development Commands

```bash
# Setup new project
npx create-turbo@latest promohub
cd promohub
npx create-next-app apps/web --typescript --tailwind --app --src-dir
npx supabase init

# Development
npm run dev                    # All apps
npm run dev --filter=web       # Web app only

# Database
npx supabase migration new <name>
npx supabase db push
npx supabase db reset          # Reset with migrations + seed

# Build & Deploy
npm run build
npm run lint
npm run typecheck

# Testing
npm run test
npm run test:e2e
```

## Git Conventions

### Branches
```
main           ← Production (auto-deploy)
└── develop    ← Integration
     ├── feat/calendar-view
     ├── feat/promo-crud
     ├── fix/date-timezone
     └── chore/setup-ci
```

### Commits
Format: `type(scope): message`

Examples:
- `feat(calendar): implement monthly view`
- `fix(promo): timezone bug on end date`
- `chore(db): add channel seed data`
- `refactor(ui): extract DateRangePicker component`

## Phase 1 Priority Features

Implementation priority for Phase 1:

1. **Calendar Component** - Month/week/day views with promotion cards
2. **Promotion CRUD** - Create, edit, delete promotions with forms
3. **Channel Filtering** - Filter calendar by sales channel
4. **Team Sharing** - Multi-user access with role-based permissions
5. **Template System** - Save and reuse recurring promotion patterns
6. **Conflict Detection** - Alert when promotions overlap on same channel/product

## Current Implementation Status

**Overall Completion: ~55% for Phase 1**

The codebase has completed the authentication foundation and is ready for API integration. Most features have working UI with demo data that needs to be replaced with real database calls.

### What's Complete

| Component | Status | Location |
|-----------|--------|----------|
| Database Schema | DONE | `supabase/migrations/` - All tables with RLS policies, using `gen_random_uuid()` |
| Calendar UI | DONE | `apps/web/src/components/calendar/` - Month/week/day views |
| Promotion Forms | DONE | `apps/web/src/components/promotions/PromotionForm.tsx` |
| Filter UI | DONE | `apps/web/src/components/filters/` - Channel/status filtering |
| Layout Components | DONE | `apps/web/src/components/layout/` - Sidebar, header, mobile nav |
| Type Definitions | DONE | `packages/types/` - Comprehensive TypeScript types |
| Validation Schemas | DONE | `packages/utils/src/validation.ts` - Zod schemas |
| Query Functions | DONE | `packages/db/queries/` - Ready for Supabase integration |
| Seed Data | DONE | `packages/db/seed/` and `supabase/seed.sql` |
| **Supabase Auth Clients** | DONE | `apps/web/src/lib/supabase/` - Browser, server, middleware clients |
| **Auth Middleware** | DONE | `apps/web/middleware.ts` - Route protection, session refresh |
| **Auth Callback Route** | DONE | `apps/web/src/app/api/auth/callback/route.ts` - OAuth/email confirmation |
| **Login/Signup Pages** | DONE | `apps/web/src/app/(auth)/` - Real forms with Supabase Auth |
| **UserMenu Component** | DONE | `apps/web/src/components/layout/UserMenu.tsx` - Real user data, logout |

### Authentication Implementation (Completed 2026-02-02)

**Files created:**
```
apps/web/
├── middleware.ts                           # Route protection (/calendar, /promotions, /settings, /products)
└── src/
    ├── app/
    │   ├── api/auth/callback/route.ts      # OAuth & email confirmation handler
    │   └── (auth)/
    │       ├── login/page.tsx              # Email/password login with Suspense
    │       └── signup/page.tsx             # Signup with email confirmation flow
    ├── lib/supabase/
    │   ├── client.ts                       # Browser client (createBrowserClient)
    │   ├── server.ts                       # Server client (createServerClient)
    │   ├── middleware.ts                   # Session refresh (updateSession)
    │   └── index.ts                        # Export index
    └── components/layout/
        └── UserMenu.tsx                    # Real user data display, working logout
```

**Environment variables updated:**
- Uses new Supabase key format: `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY` (replaces legacy `ANON_KEY`)

**Database migrations fixed:**
- All migrations updated to use `gen_random_uuid()` instead of deprecated `uuid_generate_v4()`

### What Needs Implementation (Priority Order)

#### Priority 1: HIGH - Replace Demo Data with API Calls (COMPLETED 2026-07-01)

| Issue | Location | Status |
|-------|----------|--------|
| Calendar uses static data | `apps/web/src/app/(dashboard)/calendar/page.tsx` | DONE - fetches `/api/calendar` per visible range |
| Promotions list uses static data | `apps/web/src/app/(dashboard)/promotions/page.tsx` | DONE - fetches `/api/promotions`, delete/duplicate wired |
| FilterProvider uses static channels | `apps/web/src/components/filters/FilterProvider.tsx` | DONE - fetches `/api/channels` (UUID-keyed) via `useChannelOptions` |
| API Routes are stubs | `apps/web/src/app/api/promotions/`, `api/calendar/`, `api/teams/` | DONE - auth + team scoping + Zod validation |
| Hardcoded Demo Team ID | `apps/web/src/app/(dashboard)/promotions/new/page.tsx` | DONE - uses `useTeam()` from TeamProvider |

**Critical DB fix (2026-07-01)**: `team_members` RLS policies were self-referential, causing
`infinite recursion detected in policy` (42P17) on every membership query. Fixed in
`supabase/migrations/20260701000000_fix_team_members_rls_recursion.sql` using SECURITY DEFINER
helpers `is_team_member()` / `is_team_admin()` and the `create_team_with_owner()` RPC
(used by `POST /api/teams`).

#### Priority 2: MEDIUM - Core Features

| Feature | Status | Action Required |
|---------|--------|-----------------|
| Team Management | Schema only | Create `apps/web/src/app/(dashboard)/settings/team/page.tsx` |
| Conflict Detection UI | Query ready | Add warning UI to `PromotionForm.tsx` using `checkPromotionConflicts` |
| Products Page | Missing | Create `apps/web/src/app/(dashboard)/products/page.tsx` |
| Template System UI | Schema only | Create template CRUD and selection in promotion form |

#### Priority 3: LOW - Polish

| Issue | Location | Action Required |
|-------|----------|-----------------|
| Inconsistent Channel IDs | FilterProvider vs Database | DONE (2026-07-01) - UUIDs used consistently, channels fetched from API |
| Missing Error Boundaries | `apps/web/src/components/common/` | Create `ErrorBoundary.tsx` |
| Incomplete Korean localization | Various UI files | Setup i18n library (next-intl recommended) |

### Channel ID Mapping Reference

The codebase currently has inconsistent channel identification:

| FilterProvider (slug) | Database (UUID) | Display Name |
|-----------------------|-----------------|--------------|
| `'oliveyoung'` | `'c1000000-0000-0000-0000-000000000001'` | Oliveyoung |
| `'coupang'` | `'c1000000-0000-0000-0000-000000000002'` | Coupang |
| `'naver'` | `'c1000000-0000-0000-0000-000000000003'` | Naver |
| `'kakao'` | `'c1000000-0000-0000-0000-000000000004'` | Kakao |
| `'musinsa'` | `'c1000000-0000-0000-0000-000000000005'` | Musinsa |

**Solution**: Fetch channels from API and use UUID consistently throughout the app.

### Implementation Checklist

When implementing features, ensure:

- [ ] **Auth**: Every page/API route verifies authentication
- [ ] **Team Scoping**: All queries include team_id from session
- [ ] **Validation**: All inputs validated with Zod schemas from `@promohub/utils`
- [ ] **Error Handling**: Proper error states and user feedback
- [ ] **Loading States**: Show loading indicators during data fetches
- [ ] **Type Safety**: Use types from `@promohub/types`

## API Routes (Next.js App Router)

```
# Auth (Supabase Auth - handled client-side, callback route for redirects)
GET    /api/auth/callback          # OAuth/email confirmation redirect handler  [DONE]

# Promotions
GET    /api/promotions             # List promotions (with filters)        [DONE]
POST   /api/promotions             # Create promotion (+conflict warning)  [DONE]
GET    /api/promotions/[id]        # Get promotion detail                  [DONE]
PATCH  /api/promotions/[id]        # Update promotion                      [DONE]
DELETE /api/promotions/[id]        # Delete promotion (owner/admin)        [DONE]

# Calendar
GET    /api/calendar               # Get promotions for date range         [DONE]

# Teams
GET    /api/teams                  # List user's teams                     [DONE]
POST   /api/teams                  # Create team (create_team_with_owner)  [DONE]
POST   /api/teams/[id]/invite      # Invite member                         [TODO]

# Channels & Products
GET    /api/channels               # List channels (system + custom)       [DONE]
POST   /api/channels               # Create custom channel                 [DONE]
GET    /api/products               # List products (+channel prices)       [DONE]
POST   /api/products               # Create product                        [DONE]

# Webhooks
POST   /api/webhooks/stripe        # Stripe payment webhooks               [Phase 2]
POST   /api/webhooks/slack         # Slack notifications                   [Phase 2]
```

**API Route Implementation Pattern:**
```typescript
// apps/web/src/app/api/promotions/route.ts
import { createServerClient } from '@/lib/supabase/server'
import { getPromotions, createPromotion } from '@promohub/db'
import { createPromotionSchema } from '@promohub/utils'

export async function GET(request: Request) {
  const supabase = await createServerClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 })
  }

  // Get user's team_id from team_members table
  const { data: membership } = await supabase
    .from('team_members')
    .select('team_id')
    .eq('user_id', user.id)
    .single()

  if (!membership) {
    return Response.json({ error: 'No team found' }, { status: 403 })
  }

  const promotions = await getPromotions(supabase, {
    teamId: membership.team_id
  })

  return Response.json(promotions)
}
```

## Environment Variables

```bash
# ============================================
# PUBLIC (safe to expose in browser)
# ============================================
NEXT_PUBLIC_SUPABASE_URL=              # Supabase project URL
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=  # Publishable key (sb_publishable_...)
NEXT_PUBLIC_APP_URL=                   # App domain for OAuth redirects

# ============================================
# SECRET (server-side only, NEVER expose)
# ============================================

# Supabase Secret Key (DANGER: bypasses RLS - use sparingly)
SUPABASE_SECRET_KEY=                   # Secret key (sb_secret_...)

# Payments (Phase 2)
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
TOSS_SECRET_KEY=
TOSS_CLIENT_KEY=

# Notifications (Phase 2)
SLACK_WEBHOOK_URL=
KAKAO_ALIMTALK_KEY=
KAKAO_ALIMTALK_SENDER=

# External APIs (Phase 2+)
COUPANG_ACCESS_KEY=
COUPANG_SECRET_KEY=
NAVER_CLIENT_ID=
NAVER_CLIENT_SECRET=
```

**For Local Development (Supabase CLI):**
```bash
# After running `supabase start`, these are auto-generated:
# NEXT_PUBLIC_SUPABASE_URL=http://127.0.0.1:54321
# NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=<from dashboard>
# SUPABASE_SECRET_KEY=<from dashboard>
#
# Get keys from Supabase Dashboard → Project Settings → API
```

**API Keys (2025 Update):**
- Supabase now uses `sb_publishable_...` and `sb_secret_...` keys
- Legacy `anon` and `service_role` JWT-based keys are deprecated for new projects
- Publishable key: Safe for browser, RLS enforced
- Secret key: Server-only, bypasses RLS

**Security Notes:**
- `NEXT_PUBLIC_*` are exposed to browser - only use for truly public values
- `SUPABASE_SECRET_KEY` bypasses ALL RLS - never use in API routes that handle user requests
- Use different values for development, staging, and production
- Rotate secrets regularly, especially after team member departures

## Code Conventions

### TypeScript
- Strict mode enabled
- Use `type` for object shapes, `interface` for extendable contracts
- Prefer named exports over default exports
- Use Zod for runtime validation

### Components
```tsx
// Prefer function components with explicit types
export function PromoCard({ promotion }: { promotion: Promotion }) {
  return <div>...</div>
}

// Use 'use client' directive only when needed
'use client'
```

### Database (Supabase)
- Use RLS (Row Level Security) for multi-tenant data isolation
- All tables must have `team_id` for team scoping
- Use `created_at` and `updated_at` timestamps

### File Naming
- Components: `PascalCase.tsx` (e.g., `PromoCard.tsx`)
- Hooks: `camelCase.ts` with `use` prefix (e.g., `usePromoCalendar.ts`)
- Utils: `camelCase.ts` (e.g., `date.ts`, `currency.ts`)

## Security (Multi-Tenant SaaS)

PromoHub is a B2B SaaS platform serving multiple companies. **Data isolation and security are critical** - one company must NEVER access another company's data.

### Multi-Tenant Data Isolation

**Row Level Security (RLS) is MANDATORY for all tables:**

```sql
-- Example: promotions table RLS policy
CREATE POLICY "Users can only access their team's promotions"
ON promotions
FOR ALL
USING (
  team_id IN (
    SELECT team_id FROM team_members
    WHERE user_id = auth.uid()
  )
);

-- NEVER bypass RLS - always use anon/authenticated client
-- Service role key should ONLY be used for admin operations
```

**Required RLS patterns:**
- Every table with user data MUST have `team_id` column
- Every query MUST be scoped by team membership
- Use Supabase `auth.uid()` in RLS policies, never trust client-side user IDs

### Authentication & Authorization

**Supabase Client Setup (Required Files):**

```typescript
// apps/web/src/lib/supabase/client.ts - Browser client
'use client'
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}

// apps/web/src/lib/supabase/server.ts - Server client
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'

export async function createClient() {
  const cookieStore = await cookies()

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll()
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value, options }) =>
            cookieStore.set(name, value, options)
          )
        },
      },
    }
  )
}
```

**Auth Middleware (apps/web/middleware.ts):**
```typescript
import { createServerClient } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  let response = NextResponse.next({ request })

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll()
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value }) =>
            request.cookies.set(name, value)
          )
          response = NextResponse.next({ request })
          cookiesToSet.forEach(({ name, value, options }) =>
            response.cookies.set(name, value, options)
          )
        },
      },
    }
  )

  const { data: { user } } = await supabase.auth.getUser()

  // Protect dashboard routes
  if (!user && request.nextUrl.pathname.startsWith('/calendar')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }
  if (!user && request.nextUrl.pathname.startsWith('/promotions')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }
  if (!user && request.nextUrl.pathname.startsWith('/settings')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  // Redirect logged-in users away from auth pages
  if (user && request.nextUrl.pathname.startsWith('/login')) {
    return NextResponse.redirect(new URL('/calendar', request.url))
  }

  return response
}

export const config = {
  matcher: ['/calendar/:path*', '/promotions/:path*', '/settings/:path*', '/login', '/signup'],
}
```

**Session verification in pages/API:**
```typescript
// Always verify session server-side
import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'

export async function getServerSession() {
  const supabase = await createClient()
  const { data: { user }, error } = await supabase.auth.getUser()

  if (error || !user) {
    redirect('/login')
  }
  return user
}

// Role-based access control
type Role = 'owner' | 'admin' | 'member' | 'viewer'

// Check permissions before sensitive operations
async function canEditPromotion(userId: string, promoId: string): Promise<boolean> {
  // Verify user belongs to the team AND has edit permissions
}
```

### API Security

```typescript
// All API routes must:
// 1. Verify authentication
// 2. Validate input with Zod
// 3. Check authorization (team membership + role)
// 4. Use parameterized queries (never string interpolation)

export async function POST(request: Request) {
  // 1. Auth check
  const session = await getServerSession()
  if (!session) return Response.json({ error: 'Unauthorized' }, { status: 401 })

  // 2. Input validation
  const body = await request.json()
  const parsed = createPromotionSchema.safeParse(body)
  if (!parsed.success) {
    return Response.json({ error: 'Invalid input' }, { status: 400 })
  }

  // 3. Authorization check
  const isMember = await isTeamMember(session.user.id, parsed.data.team_id)
  if (!isMember) return Response.json({ error: 'Forbidden' }, { status: 403 })

  // 4. Safe database operation (RLS will also enforce)
  const result = await supabase.from('promotions').insert(parsed.data)
}
```

### Input Validation & Sanitization

```typescript
// Use Zod schemas for ALL user inputs
import { z } from 'zod'

const promotionSchema = z.object({
  title: z.string().min(1).max(200).trim(),
  description: z.string().max(2000).optional(),
  discount_value: z.number().min(0).max(100),
  start_date: z.string().datetime(),
  end_date: z.string().datetime(),
  // Validate foreign keys exist and user has access
  channel_id: z.string().uuid(),
  team_id: z.string().uuid(),
})

// Sanitize HTML content to prevent XSS
// Use DOMPurify or similar for any rich text
```

### Secrets Management

```bash
# NEVER commit secrets to git
# .gitignore must include:
.env
.env.local
.env.*.local
*.pem
*.key

# Use environment variables for all secrets
# Rotate keys regularly
# Use different keys for dev/staging/production
```

**Secret handling rules:**
- `NEXT_PUBLIC_*` variables are exposed to browser - ONLY use for public values
- `SUPABASE_SERVICE_ROLE_KEY` bypasses RLS - use sparingly, never expose to client
- Store API keys for external services (Stripe, Kakao, etc.) server-side only

### OWASP Top 10 Checklist

| Vulnerability | Prevention |
|--------------|------------|
| **Injection** | Parameterized queries via Supabase client; Zod validation |
| **Broken Auth** | Supabase Auth; session verification on every request |
| **Sensitive Data Exposure** | HTTPS only; encrypt PII; minimal data in responses |
| **XXE** | Not applicable (JSON only) |
| **Broken Access Control** | RLS policies; authorization checks; team scoping |
| **Security Misconfiguration** | Environment-specific configs; security headers |
| **XSS** | React auto-escaping; CSP headers; sanitize rich text |
| **Insecure Deserialization** | Zod schema validation on all inputs |
| **Vulnerable Components** | Regular `npm audit`; Dependabot alerts |
| **Insufficient Logging** | Audit logs for sensitive operations |

### Security Headers (Next.js)

```typescript
// next.config.ts
const securityHeaders = [
  { key: 'X-DNS-Prefetch-Control', value: 'on' },
  { key: 'Strict-Transport-Security', value: 'max-age=63072000; includeSubDomains' },
  { key: 'X-Frame-Options', value: 'SAMEORIGIN' },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'Referrer-Policy', value: 'origin-when-cross-origin' },
  { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
]
```

### Audit Logging

```typescript
// Log sensitive operations for security audit
interface AuditLog {
  action: 'create' | 'update' | 'delete' | 'export' | 'invite' | 'role_change'
  entity_type: 'promotion' | 'team' | 'member' | 'product'
  entity_id: string
  user_id: string
  team_id: string
  timestamp: Date
  ip_address?: string
  changes?: Record<string, { old: unknown; new: unknown }>
}

// Log these events:
// - User login/logout
// - Team member added/removed
// - Role changes
// - Bulk data exports
// - Promotion create/update/delete
// - Settings changes
```

### Rate Limiting

```typescript
// Implement rate limiting for API routes
// Use Vercel's built-in or upstash/ratelimit

import { Ratelimit } from '@upstash/ratelimit'
import { Redis } from '@upstash/redis'

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, '10 s'), // 10 requests per 10 seconds
})

// Apply to sensitive endpoints (login, signup, password reset)
```

## Korean Language & Market

- UI supports Korean/English (i18n ready)
- Currency: Korean Won (원, 만, 억)
- Korean calendar events (Chuseok, Lunar New Year, Black Friday Korea, etc.)
- Korean e-commerce channels (Oliveyoung, Coupang, Naver, Kakao, Musinsa)
- Date format: `YYYY년 MM월 DD일` or `YYYY-MM-DD`
- Timezone: Asia/Seoul (KST, UTC+9)

## Notes for AI Assistants

### Security First (CRITICAL)
- **NEVER write code that bypasses RLS** - All queries must go through authenticated Supabase client
- **NEVER expose service role key** to client-side code
- **ALWAYS validate inputs** with Zod before database operations
- **ALWAYS check team membership** before returning data
- **NEVER log sensitive data** (passwords, tokens, PII)
- **NEVER trust client-side IDs** - verify ownership server-side

### Development Guidelines
1. **Phase 1 focus** - Prioritize calendar and promotion features; avoid AI agent complexity
2. **TypeScript first** - Full-stack TypeScript with strict mode; no `any` types
3. **Monorepo patterns** - Use `packages/` for shared code between apps
4. **Supabase patterns** - Use RLS for multi-tenant data; queries go in `packages/db/queries`
5. **Korean support** - All user-facing text should support Korean localization
6. **Simple solutions** - Start simple, add complexity only when needed
7. **Component reuse** - Check `packages/ui` before creating new components
8. **No premature optimization** - Make it work, make it right, then make it fast

### Security Review Checklist (Before Committing)
- [ ] All database queries use authenticated client (not service role)
- [ ] RLS policies exist for new tables
- [ ] Input validation with Zod on all API routes
- [ ] Authorization checks (team membership + role) on sensitive operations
- [ ] No secrets in code or logs
- [ ] Parameterized queries (no string interpolation for SQL)

## Future: AI Agent Integration (Phase 3)

When AI agents are added in Phase 3, they will be implemented as a separate Python service:

- **Framework**: FastAPI with async support
- **Orchestration**: LangChain + LangGraph for multi-agent coordination
- **Agents**: 21 specialized agents across 5 divisions (Strategy, Market Intelligence, Channel Management, Analytics, Operations)
- **Integration**: REST API endpoints for web app to communicate with agent service

Reference the `backend/` directory (if present) for existing agent patterns when Phase 3 development begins.

---

**Remember**: PromoHub is a fresh start. Focus on building a solid calendar-based promotion management system first. AI agents are a future enhancement, not the current priority.
