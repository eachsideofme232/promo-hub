# Codebase Structure

**Analysis Date:** 2026-02-17

## Directory Layout

```
promohub/ (root)
├── apps/
│   ├── web/                           # Main Next.js web application
│   │   ├── src/
│   │   │   ├── app/                   # Next.js App Router
│   │   │   │   ├── layout.tsx         # Root layout (fonts, metadata, styles)
│   │   │   │   ├── page.tsx           # Home page (redirects to /calendar)
│   │   │   │   ├── (auth)/            # Auth routes (login, signup)
│   │   │   │   │   ├── layout.tsx
│   │   │   │   │   ├── login/page.tsx
│   │   │   │   │   └── signup/page.tsx
│   │   │   │   ├── (dashboard)/       # Protected dashboard routes
│   │   │   │   │   ├── layout.tsx     # Dashboard layout with sidebar, header, filters
│   │   │   │   │   ├── page.tsx       # Dashboard home (redirect to /calendar)
│   │   │   │   │   ├── calendar/      # [Phase 1] Promotion calendar
│   │   │   │   │   │   └── page.tsx
│   │   │   │   │   ├── promotions/    # [Phase 1] Promotion management
│   │   │   │   │   │   ├── page.tsx   # List promotions
│   │   │   │   │   │   ├── new/page.tsx       # Create promotion
│   │   │   │   │   │   └── [id]/page.tsx      # Edit promotion detail
│   │   │   │   │   ├── products/      # [Phase 2+] Product management
│   │   │   │   │   ├── settings/      # Team settings
│   │   │   │   │   │   ├── page.tsx   # Settings home
│   │   │   │   │   │   ├── team/page.tsx      # Team management
│   │   │   │   │   │   └── billing/page.tsx   # Billing (Phase 2)
│   │   │   │   │   ├── strategy/      # [Phase 2] Strategy planning
│   │   │   │   │   └── competitors/   # [Phase 2] Competitor monitoring
│   │   │   │   └── api/               # API routes (Next.js server functions)
│   │   │   │       ├── auth/
│   │   │   │       │   └── callback/route.ts  # OAuth/email confirmation handler
│   │   │   │       ├── promotions/route.ts    # GET/POST promotions
│   │   │   │       ├── calendar/route.ts      # GET calendar events
│   │   │   │       ├── teams/route.ts         # Team APIs
│   │   │   │       └── webhooks/stripe/route.ts
│   │   │   ├── components/            # Reusable React components
│   │   │   │   ├── layout/            # Layout components
│   │   │   │   │   ├── Sidebar.tsx
│   │   │   │   │   ├── Header.tsx
│   │   │   │   │   ├── MobileNav.tsx
│   │   │   │   │   ├── UserMenu.tsx
│   │   │   │   │   ├── PageHeader.tsx
│   │   │   │   │   ├── Breadcrumb.tsx
│   │   │   │   │   └── index.ts
│   │   │   │   ├── calendar/          # Calendar-specific components
│   │   │   │   │   ├── CalendarView.tsx       # Main calendar container
│   │   │   │   │   ├── MonthView.tsx          # Month grid display
│   │   │   │   │   ├── WeekView.tsx           # Week grid display
│   │   │   │   │   ├── DayView.tsx            # Day detail view
│   │   │   │   │   ├── CalendarHeader.tsx     # Navigation + view switcher
│   │   │   │   │   ├── PromotionCard.tsx      # Individual promotion card
│   │   │   │   │   ├── ChannelFilter.tsx
│   │   │   │   │   └── index.ts
│   │   │   │   ├── filters/           # Filter components + context
│   │   │   │   │   ├── FilterProvider.tsx     # Context provider with URL sync
│   │   │   │   │   ├── FilterSidebar.tsx      # Desktop filter sidebar
│   │   │   │   │   ├── ChannelFilter.tsx      # Channel checkbox group
│   │   │   │   │   ├── StatusFilter.tsx       # Status filter
│   │   │   │   │   ├── DateRangeFilter.tsx    # Date range picker
│   │   │   │   │   ├── useFilters.ts          # Custom hook for filter context
│   │   │   │   │   └── index.ts
│   │   │   │   ├── promotions/        # Promotion list + form components
│   │   │   │   │   ├── PromotionForm.tsx      # Create/edit form
│   │   │   │   │   ├── PromotionList.tsx      # Table/list view
│   │   │   │   │   ├── PromotionStatusBadge.tsx
│   │   │   │   │   ├── BulkActions.tsx
│   │   │   │   │   └── index.ts
│   │   │   │   ├── dashboard/         # Dashboard-specific components
│   │   │   │   │   ├── TerminalLayout.tsx
│   │   │   │   │   ├── AgentChat.tsx
│   │   │   │   │   ├── LiveMetrics.tsx
│   │   │   │   │   ├── AlertsPanel.tsx
│   │   │   │   │   ├── ChannelStatus.tsx
│   │   │   │   │   └── TitleBar.tsx
│   │   │   │   └── common/            # Shared utility components
│   │   │   │       ├── LoadingSpinner.tsx
│   │   │   │       ├── EmptyState.tsx
│   │   │   │       └── ErrorBoundary.tsx (planned)
│   │   │   ├── lib/                   # Client + server utilities
│   │   │   │   └── supabase/          # Supabase client initialization
│   │   │   │       ├── client.ts      # createClient() for browser (use in Client Components)
│   │   │   │       ├── server.ts      # createClient() for server (use in Server Components/API)
│   │   │   │       └── middleware.ts  # updateSession() for session refresh
│   │   │   ├── styles/
│   │   │   │   └── globals.css        # Tailwind + global styles
│   │   │   └── hooks/                 # Custom React hooks (planned)
│   │   ├── middleware.ts              # Next.js middleware (auth protection, session refresh)
│   │   ├── next.config.js
│   │   ├── tsconfig.json
│   │   ├── tailwind.config.ts
│   │   └── package.json
│   └── landing/                       # Marketing site (Phase 2+)
│       ├── src/
│       │   ├── app/
│       │   └── components/
│       └── package.json
├── packages/                          # Shared code across apps
│   ├── types/                         # Shared TypeScript interfaces
│   │   ├── src/
│   │   │   ├── index.ts               # Export all types
│   │   │   ├── promotion.ts           # Promotion, PromotionStatus, DiscountType, PromotionFilters
│   │   │   ├── channel.ts             # Channel interface
│   │   │   ├── team.ts                # Team, TeamMember, TeamRole
│   │   │   ├── user.ts                # User, UserProfile
│   │   │   ├── calendar.ts            # CalendarView, CalendarPromotion
│   │   │   ├── product.ts             # Product, SKU
│   │   │   └── settings.ts            # Settings, Preferences
│   │   ├── package.json
│   │   └── tsconfig.json
│   ├── utils/                         # Shared utility functions + validation
│   │   ├── src/
│   │   │   ├── index.ts               # Export all utilities
│   │   │   ├── validation.ts          # Zod schemas for all forms (promotionSchema, teamSchema, etc.)
│   │   │   ├── date.ts                # Date formatting, timezone helpers
│   │   │   └── currency.ts            # Currency formatting (KRW, USD)
│   │   ├── package.json
│   │   └── tsconfig.json
│   ├── db/                            # Database layer (Supabase queries + seed data)
│   │   ├── src/
│   │   │   └── index.ts
│   │   ├── queries/                   # Reusable query functions
│   │   │   ├── index.ts               # Export all queries
│   │   │   ├── promotions.ts          # getPromotions, createPromotion, updatePromotion, deletePromotion
│   │   │   ├── calendar.ts            # getCalendarEvents, getConflictingPromotions
│   │   │   ├── teams.ts               # getTeams, getTeamMembers, createTeam, inviteTeamMember
│   │   │   ├── channels.ts            # getChannels, getChannelsForTeam
│   │   │   └── products.ts            # getProducts, createProduct, bulkImportProducts
│   │   ├── seed/                      # Initial seed data scripts
│   │   │   ├── index.ts               # Main seed entry
│   │   │   ├── channels.ts            # Korean e-commerce channels (Oliveyoung, Coupang, etc.)
│   │   │   └── demo.ts                # Demo promotions for testing
│   │   ├── package.json
│   │   └── tsconfig.json
│   ├── ui/                            # Shared UI components (Radix UI based)
│   │   ├── src/
│   │   │   ├── index.ts
│   │   │   └── utils/cn.ts            # classname utility for Tailwind
│   │   ├── package.json
│   │   └── tsconfig.json
│   └── config/                        # Shared configuration files
│       ├── eslint-config/
│       ├── tsconfig/                  # Base TypeScript config
│       └── package.json
├── supabase/                          # Supabase configuration + migrations
│   ├── config.toml                    # Supabase local dev config
│   ├── migrations/                    # SQL migrations (executed in order)
│   │   ├── 20240101000000_init_extensions.sql        # Functions (update_updated_at trigger)
│   │   ├── 20240101000001_create_channels.sql        # Channels table + RLS
│   │   ├── 20240101000002_create_teams.sql           # Teams + team_members tables + RLS
│   │   ├── 20240101000003_create_products.sql        # Products table + RLS
│   │   ├── 20240101000004_create_promo_templates.sql # PromoTemplate table + RLS
│   │   ├── 20240101000005_create_promotions.sql      # Promotions table + RLS + indexes
│   │   └── 20240101000006_create_promo_products.sql  # Promo_products junction table
│   └── seed.sql                       # Seed data (channels, demo team, demo promotions)
├── turbo.json                         # Turborepo configuration (caching, tasks)
├── tsconfig.base.json                 # Base TypeScript config (path aliases)
├── package.json                       # Root workspace config
├── docker-compose.yml                 # Local Supabase development environment
└── .planning/
    └── codebase/                      # GSD codebase documentation
        ├── ARCHITECTURE.md
        └── STRUCTURE.md
```

## Directory Purposes

**`apps/web/src/app`:**
- Purpose: Next.js App Router pages and API routes
- Contains: Page components (`.tsx`), layout components, API endpoints
- Key files: All pages follow Next.js routing conventions. Grouped by route segment (auth, dashboard)

**`apps/web/src/components`:**
- Purpose: Reusable React components organized by feature
- Contains: Layout, calendar, filters, promotions, dashboard components
- Key files: Index files in each subdirectory export components for clean imports

**`apps/web/src/lib/supabase`:**
- Purpose: Supabase client initialization and middleware utilities
- Contains: Browser client, server client, session refresh middleware
- Key files: `client.ts` (browser), `server.ts` (server), `middleware.ts` (refresh)

**`packages/types`:**
- Purpose: Shared TypeScript type definitions across all apps
- Contains: Interfaces for Promotion, Team, User, Channel, Calendar, Product, Settings
- Key files: `index.ts` exports all types. Organized by domain (promotion.ts, team.ts, etc.)

**`packages/utils`:**
- Purpose: Shared utility functions and validation schemas
- Contains: Zod validation schemas, date/currency formatting helpers
- Key files: `validation.ts` contains all Zod schemas. `date.ts` and `currency.ts` for formatting.

**`packages/db`:**
- Purpose: Database query layer and seed data
- Contains: Query functions (typed wrappers around Supabase queries), seed scripts
- Key files: `queries/index.ts` exports all query functions. `seed/index.ts` runs seed initialization.

**`supabase/migrations`:**
- Purpose: SQL migrations defining database schema and RLS policies
- Contains: Table definitions, indexes, Row Level Security policies, triggers
- Key files: Numbered in execution order. Each file creates tables + RLS for a domain (channels, teams, promotions, etc.)

**`supabase/seed.sql`:**
- Purpose: Initial data load for local development and demo
- Contains: Channel definitions, demo team, demo promotions
- Key files: Single SQL file run after migrations

## Key File Locations

**Entry Points:**
- `apps/web/src/app/layout.tsx` - Root layout, fonts, metadata, global styles
- `apps/web/src/app/page.tsx` - Home page (redirects to dashboard)
- `apps/web/middleware.ts` - Auth middleware, session refresh, route protection

**Configuration:**
- `turbo.json` - Turborepo task definitions and caching
- `tsconfig.base.json` - Shared TypeScript config with path aliases (`@promohub/*`)
- `apps/web/next.config.js` - Next.js config
- `apps/web/tailwind.config.ts` - Tailwind CSS config
- `supabase/config.toml` - Supabase local development config

**Core Logic:**
- `apps/web/src/app/(dashboard)/layout.tsx` - Dashboard layout composition (sidebar, header, filters)
- `apps/web/src/components/filters/FilterProvider.tsx` - Filter state + URL sync
- `apps/web/src/components/calendar/CalendarView.tsx` - Calendar UI container
- `packages/db/queries/promotions.ts` - Promotion CRUD query functions
- `packages/utils/src/validation.ts` - All Zod validation schemas

**Testing:**
- Not yet implemented. Tests should follow Next.js conventions:
  - Unit tests: `*.test.ts` or `*.test.tsx` files alongside source
  - Integration tests: `__tests__/` directories
  - E2E tests: Playwright (when added)

## Naming Conventions

**Files:**
- Components: `PascalCase.tsx` (e.g., `CalendarView.tsx`, `PromotionForm.tsx`)
- Utilities: `camelCase.ts` (e.g., `validation.ts`, `date.ts`)
- Pages: `page.tsx` (Next.js convention)
- Hooks: `camelCase.ts` with `use` prefix (e.g., `useFilters.ts`)
- API routes: `route.ts` (Next.js convention)

**Directories:**
- Feature grouping: `kebab-case` (e.g., `filter-sidebar`, `promo-templates`)
- Grouped routes: parentheses for organization without URL impact (e.g., `(auth)`, `(dashboard)`)
- Dynamic routes: Square brackets (e.g., `[id]`)

**Functions & Variables:**
- Functions: `camelCase` (e.g., `getPromotions()`, `toggleChannel()`)
- Types/Interfaces: `PascalCase` (e.g., `Promotion`, `FilterState`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `DEMO_PROMOTIONS`, `CHANNELS`, `FILTER_ENABLED_PATHS`)
- HTML/CSS classes: `kebab-case` (Tailwind convention)

## Where to Add New Code

**New Feature (e.g., new page like Templates):**
1. Create page file: `apps/web/src/app/(dashboard)/templates/page.tsx`
2. Create components: `apps/web/src/components/templates/*.tsx` (TemplateList.tsx, TemplateForm.tsx, etc.)
3. Create type: Add interface to `packages/types/src/promotion.ts` (or new file if large domain)
4. Create validation: Add schema to `packages/utils/src/validation.ts`
5. Create queries: Add query functions to `packages/db/queries/templates.ts` (if new domain)
6. Create API routes: `apps/web/src/app/api/templates/route.ts`
7. Create migrations: `supabase/migrations/20240101000NNN_create_templates.sql`

**New Component:**
- Reusable UI component: `packages/ui/src/` (if truly generic)
- Feature-specific component: `apps/web/src/components/{feature}/` (e.g., `promotions/PromotionCard.tsx`)
- Always include TypeScript types in component props interface

**New Utility Function:**
- Validation schema: `packages/utils/src/validation.ts`
- Date utility: `packages/utils/src/date.ts`
- Currency formatter: `packages/utils/src/currency.ts`
- Other utilities: New file in `packages/utils/src/` if domain-specific

**New API Route:**
- Location: `apps/web/src/app/api/{resource}/route.ts`
- Pattern: Verify auth, validate input with Zod, call query functions, return JSON
- Always include error handling and appropriate HTTP status codes

**New Database Table:**
1. Create migration: `supabase/migrations/20240101000NNN_create_{table}.sql`
2. Add RLS policies in same migration
3. Create query functions: `packages/db/queries/{table}.ts`
4. Add types: `packages/types/src/{domain}.ts`

## Special Directories

**`apps/web/.next`:**
- Purpose: Next.js build output
- Generated: Yes (by `npm run build`)
- Committed: No (.gitignore)

**`node_modules`:**
- Purpose: Installed npm dependencies
- Generated: Yes (by `npm install`)
- Committed: No (.gitignore)

**`.turbo`:**
- Purpose: Turborepo cache
- Generated: Yes (by turbo)
- Committed: No (.gitignore)

**`.planning/codebase`:**
- Purpose: GSD codebase documentation (ARCHITECTURE.md, STRUCTURE.md, CONVENTIONS.md, TESTING.md, CONCERNS.md)
- Generated: No (written by GSD mapping command)
- Committed: Yes (documents for future Claude instances)

**`supabase/migrations`:**
- Purpose: Version-controlled SQL migrations
- Generated: No (manually written)
- Committed: Yes (schema version control)

---

*Structure analysis: 2026-02-17*
