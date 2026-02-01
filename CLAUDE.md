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

## API Routes (Next.js App Router)

```
# Auth
POST   /api/auth/[...nextauth]     # NextAuth.js handlers

# Promotions
GET    /api/promotions             # List promotions (with filters)
POST   /api/promotions             # Create promotion
GET    /api/promotions/[id]        # Get promotion detail
PATCH  /api/promotions/[id]        # Update promotion
DELETE /api/promotions/[id]        # Delete promotion

# Calendar
GET    /api/calendar               # Get promotions for date range

# Teams
GET    /api/teams                  # List user's teams
POST   /api/teams                  # Create team
POST   /api/teams/[id]/invite      # Invite member

# Channels & Products
GET    /api/channels               # List channels
GET    /api/products               # List products

# Webhooks
POST   /api/webhooks/stripe        # Stripe payment webhooks
POST   /api/webhooks/slack         # Slack notifications
```

## Environment Variables

```bash
# ============================================
# PUBLIC (safe to expose in browser)
# ============================================
NEXT_PUBLIC_SUPABASE_URL=          # Supabase project URL
NEXT_PUBLIC_SUPABASE_ANON_KEY=     # Anon key (RLS enforced)
NEXT_PUBLIC_APP_URL=               # App domain for OAuth redirects

# ============================================
# SECRET (server-side only, NEVER expose)
# ============================================

# Supabase Admin (DANGER: bypasses RLS - use sparingly)
SUPABASE_SERVICE_ROLE_KEY=

# Auth
NEXTAUTH_SECRET=                   # Random 32+ char string
NEXTAUTH_URL=

# Payments
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
TOSS_SECRET_KEY=
TOSS_CLIENT_KEY=

# Notifications
SLACK_WEBHOOK_URL=
KAKAO_ALIMTALK_KEY=
KAKAO_ALIMTALK_SENDER=

# External APIs (Phase 2+)
COUPANG_ACCESS_KEY=
COUPANG_SECRET_KEY=
NAVER_CLIENT_ID=
NAVER_CLIENT_SECRET=
```

**Security Notes:**
- `NEXT_PUBLIC_*` are exposed to browser - only use for truly public values
- `SUPABASE_SERVICE_ROLE_KEY` bypasses ALL RLS - never use in API routes that handle user requests
- Generate `NEXTAUTH_SECRET` with: `openssl rand -base64 32`
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

```typescript
// Always verify session server-side
import { createServerClient } from '@supabase/ssr'

export async function getServerSession() {
  const supabase = createServerClient(/* config */)
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
