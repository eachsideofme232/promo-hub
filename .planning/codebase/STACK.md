# Technology Stack

**Analysis Date:** 2026-02-17

## Languages

**Primary:**
- TypeScript 5.7.0 - Full-stack type safety across monorepo (strict mode enabled)
- JavaScript (JSX/TSX) - React components, Next.js app router

**Secondary:**
- SQL - PostgreSQL migrations and seed data in `supabase/migrations/` and `supabase/seed.sql`

## Runtime

**Environment:**
- Node.js 18+ (specified in `package.json` engines)
- Browser (React 18.3.0+)

**Package Manager:**
- npm 10.9.0
- Lockfile: `package-lock.json` (present)

## Frameworks

**Core:**
- Next.js 14.2.0 - App Router, SSR, API routes, middleware
- React 18.3.0 - UI components and state management

**Monorepo Management:**
- Turborepo 2.3.0 - Workspace orchestration, build caching
  - Config: `turbo.json`
  - Workspaces: `apps/` (web, landing) and `packages/` (db, types, ui, utils, config)

**UI & Styling:**
- Tailwind CSS 3.4.0 - Utility-first CSS framework
  - Config: `apps/web/tailwind.config.ts`
  - Extended theme: Primary colors (sky blue palette), terminal color overrides, custom animations
- Radix UI - Headless component primitives
  - `@radix-ui/react-dialog` 1.1.0
  - `@radix-ui/react-dropdown-menu` 2.1.0
  - `@radix-ui/react-tabs` 1.1.0
  - `@radix-ui/react-tooltip` 1.1.0
  - `@radix-ui/react-scroll-area` 1.1.0
  - `@radix-ui/react-select` 2.1.0
  - `@radix-ui/react-popover` 1.1.0
- Lucide React 0.400.0 - Icon library
- class-variance-authority 0.7.0 - Component variant patterns
- clsx 2.1.0 - Conditional CSS class management
- tailwind-merge 2.3.0 - Merge Tailwind classes without conflicts

**Validation & Type Safety:**
- Zod 3.23.0 - Runtime schema validation (`packages/utils/src/validation.ts`)
- TypeScript strict mode - No implicit any, null checks enforced

**Data & Date Handling:**
- date-fns 3.6.0 - Date manipulation and formatting (calendars, date ranges)
- Recharts 2.12.0 - Charts and data visualization (for Phase 2 P&L simulation)

**State Management:**
- Zustand 4.5.0 - Lightweight client-side state (FilterProvider context)

**Linting & Code Quality:**
- ESLint 8.0.0
  - Config: `apps/web/.eslintrc.json`
  - Extends: `eslint-config-next` (Next.js recommended rules)
- PostCSS 8.4.0 - CSS transformation
- Autoprefixer 10.4.0 - Vendor prefixes

**Build & Development:**
- Next.js 14.2.0 built-in:
  - Dev server with hot reload
  - TypeScript support
  - ESLint integration

## Key Dependencies

**Critical:**
- `@supabase/supabase-js` 2.45.0 - Database client, auth, realtime
- `@supabase/ssr` 0.5.0 - Server-side rendering utilities for Supabase auth
- Next.js middleware and auth callback handling

**Database:**
- PostgreSQL 17 (Supabase-hosted or local via Docker)
  - Version specified in `supabase/config.toml`: `major_version = 17`

**Infrastructure:**
- Supabase - Managed PostgreSQL with auth, realtime, storage
- Vercel - Next.js deployment platform (configured in `vercel.json`)

## Configuration

**Environment:**
- `.env.local` (development) - Contains `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY`
- Environment-specific secrets:
  - `NEXT_PUBLIC_*` - Safe for browser, exposed to client
  - `SUPABASE_SECRET_KEY` - Server-only, bypasses RLS (development only)
  - `STRIPE_SECRET_KEY`, `TOSS_SECRET_KEY`, etc. - For Phase 2+ features

**Build:**
- `next.config.mjs` - Configures React strict mode, transpiles monorepo packages (`@promohub/types`, `@promohub/ui`, `@promohub/utils`)
- `tsconfig.base.json` - Base TypeScript config for monorepo (ES2022 target, strict mode, module resolution bundler)
- `tsconfig.json` - Per-app overrides in `apps/web/` and `apps/landing/`
- `turbo.json` - Task pipelines, cache configuration, output specifications

**Database:**
- `supabase/config.toml` - Local development config:
  - API port: 54321
  - Database port: 54322
  - Studio port: 54323
  - Inbucket (email testing): 54324
  - Storage: S3-compatible, enabled with 50MiB file size limit
  - Auth: Email signup enabled, JWT expiry 3600s, refresh token rotation enabled
  - Realtime: Enabled
  - Edge Runtime: Deno v2 support
- `supabase/migrations/` - Schema files (using `gen_random_uuid()` instead of deprecated `uuid_generate_v4()`)
- `supabase/seed.sql` - Demo data for channels, teams, products, promotions

## Platform Requirements

**Development:**
- Node.js 18.0.0+
- npm 10.9.0+
- Docker (optional, for local Supabase)
- Supabase CLI (for local development and migrations)

**Production:**
- Vercel (Next.js deployment platform)
  - Configured in `apps/web/vercel.json`
  - Auto-deploys from `master` branch
- Supabase Cloud (PostgreSQL, auth, realtime, storage)

**Browser Support:**
- Modern browsers (ES2022 target, React 18 concurrent features)
- Chrome DevTools support via Supabase Edge Runtime inspector (port 8083)

## Workspace Structure

```
promohub/
├── apps/
│   ├── web/                    # Main Next.js app (port 3000)
│   │   └── src/
│   │       ├── app/            # App Router pages
│   │       ├── components/     # React components
│   │       ├── lib/supabase/   # Supabase clients (browser, server, middleware)
│   │       └── ...
│   └── landing/                # Marketing site (port 3001)
├── packages/
│   ├── db/                     # Database queries, seed utilities
│   ├── types/                  # Shared TypeScript types
│   ├── ui/                     # Shared Radix/Tailwind components
│   ├── utils/                  # Utilities (validation, date, currency)
│   └── config/                 # ESLint, TypeScript configs
├── supabase/
│   ├── migrations/             # SQL migration files
│   ├── seed.sql                # Demo data
│   └── config.toml             # Local dev configuration
└── turbo.json                  # Monorepo task definitions
```

---

*Stack analysis: 2026-02-17*
