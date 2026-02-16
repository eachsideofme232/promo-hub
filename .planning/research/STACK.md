# Stack Research

**Domain:** Trade Promotion Management (TPM) SaaS for K-beauty/cosmetic companies
**Researched:** 2026-02-17
**Confidence:** HIGH (core stack) / MEDIUM (supporting libraries)

## Context: Existing Codebase vs. Recommended Stack

The existing PromoHub codebase uses Next.js 14.2, React 18, Tailwind CSS v3, Zod v3, date-fns v3, Recharts v2, and Supabase. This research recommends upgrade targets for a greenfield rebuild or major version bump. Each recommendation includes migration notes where relevant.

---

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended | Confidence |
|------------|---------|---------|-----------------|------------|
| **Next.js** | 16.1.x (latest 16.1.6) | Full-stack React framework | Stable Turbopack file system caching for dev, App Router is mature and production-proven. Major perf improvements over 14.x. Server Components reduce JS sent to client -- critical for dashboard-heavy TPM app. | HIGH |
| **React** | 19.x | UI library | Next.js 16 requires React 19. Server Components, Actions, and `use()` hook are stable. Concurrent features improve perceived performance for data-heavy calendar/table views. | HIGH |
| **TypeScript** | 5.7.x | Type safety | Full-stack type safety is non-negotiable for a multi-entity domain (Promotion, Channel, Product, Team). Strict mode prevents entire categories of bugs in financial calculations. | HIGH |
| **Supabase** (PostgreSQL) | supabase-js 2.95.x, @supabase/ssr 0.8.x | Database + Auth + Realtime + Storage | All-in-one BaaS eliminates separate auth/db/storage setup. RLS provides multi-tenant data isolation at the database level -- critical for B2B SaaS. Realtime subscriptions enable live calendar updates across team members. Korean market has no regulatory issues with Supabase hosting. | HIGH |
| **Drizzle ORM** | 0.45.x (drizzle-kit 0.31.x) | Type-safe ORM | Zero dependencies, ~7.4kb gzipped. SQL-like query API gives fine-grained control for complex TPM queries (P&L aggregations, conflict detection, date range queries). Works with Supabase's connection pooler. Better for complex queries than Supabase client's query builder alone. | HIGH |
| **Tailwind CSS** | 4.1.x (latest 4.1.18) | Styling | 5x faster full builds, 100x faster incremental. CSS-first config with @theme replaces tailwind.config.js. Zero-config content detection. Major upgrade from v3 currently in the codebase. | HIGH |
| **Turborepo** | 2.8.x (latest 2.8.9) | Monorepo build system | Existing monorepo structure (apps/web, packages/*) requires Turborepo. Remote caching speeds CI. Already configured in the codebase. | HIGH |

### UI Component System

| Technology | Version | Purpose | Why Recommended | Confidence |
|------------|---------|---------|-----------------|------------|
| **shadcn/ui** | latest (not versioned, copy-paste) | UI component library | Not a dependency -- components are copied into codebase and owned by you. Built on Radix UI primitives (already partially in codebase). Full Tailwind v4 + React 19 support. Visual project builder via `npx shadcn create`. RTL support. Actively maintained by Vercel. | HIGH |
| **Radix UI** | latest | Accessible primitives | Already partially adopted (@radix-ui/react-dialog, etc.). shadcn/ui is built on top of Radix. Unstyled, accessible, composable. | HIGH |
| **Lucide React** | latest | Icons | Already in codebase. Tree-shakable, consistent with shadcn/ui ecosystem. | HIGH |

### Calendar & Scheduling (Domain-Critical)

| Technology | Version | Purpose | Why Recommended | Confidence |
|------------|---------|---------|-----------------|------------|
| **@fullcalendar/react** | 6.1.20 | Calendar component | 1M+ npm downloads/week vs. react-big-calendar's 500K. Month/week/day views out of box. Drag-and-drop event scheduling. Event resizing. Extensive plugin architecture for timeline/resource views. Built-in localization (Korean supported). Premium plugins available for Gantt-style timeline (useful for multi-channel promo planning). | MEDIUM |

**Note on existing calendar:** The codebase has custom calendar components in `apps/web/src/components/calendar/`. Evaluate whether migrating to FullCalendar saves enough development time vs. continuing the custom implementation. For a TPM product, the investment in FullCalendar pays off when you need drag-to-reschedule, multi-resource views (one row per channel), and conflict visualization.

### Data Fetching & State

| Technology | Version | Purpose | Why Recommended | Confidence |
|------------|---------|---------|-----------------|------------|
| **@tanstack/react-query** | 5.90.x | Server state management | Automatic caching, background refetching, optimistic updates. Critical for TPM where multiple team members edit promotions simultaneously. Stale-while-revalidate pattern prevents data loss. Devtools for debugging cache. | HIGH |
| **nuqs** | 2.8.x | URL state management | 6kb gzipped. Type-safe URL query state for calendar filters (date range, channel, status). Used by Supabase, Vercel, Sentry. Shareable URLs for filtered calendar views -- essential for team collaboration ("look at this week's OliveYoung promos"). | MEDIUM |
| **Zustand** | 4.5.x (already in codebase) | Client state | Already adopted. Minimal boilerplate. Use only for truly client-side state (UI preferences, sidebar state). Do NOT use for server data -- that belongs in TanStack Query. | HIGH |

### Forms & Validation

| Technology | Version | Purpose | Why Recommended | Confidence |
|------------|---------|---------|-----------------|------------|
| **Zod** | 3.24.x (stay on v3) | Schema validation | v3 is stable and battle-tested. v4 exists (v4.1.13) with 14x faster parsing, but @hookform/resolvers only recently added v4 support (5.2.2) and ecosystem compatibility is still settling. For an 8-week sprint, v3 is the safer choice. Upgrade to v4 in Phase 2. | HIGH |
| **react-hook-form** | 7.71.x | Form management | Uncontrolled form architecture minimizes re-renders -- important for complex promo creation forms with many fields (title, dates, channel, products, discount type/value, P&L inputs). Native Zod integration via @hookform/resolvers. | HIGH |
| **@hookform/resolvers** | 5.2.x | Zod-to-RHF bridge | Connects Zod schemas to react-hook-form. Supports both Zod v3 and v4 -- enables future migration. | HIGH |

### Data Visualization (P&L, ROI, Analytics)

| Technology | Version | Purpose | Why Recommended | Confidence |
|------------|---------|---------|-----------------|------------|
| **Recharts** | 3.7.0 | Charts & graphs | Already in codebase (v2). v3 is a major rewrite with better performance. Best for TPM dashboards: bar charts (promo spend by channel), line charts (ROI trends), pie charts (discount type distribution). Simpler API than Visx. Performance ceiling at ~5000 data points is fine for promo analytics (typically dozens, not thousands of data points per view). | HIGH |

### Data Tables

| Technology | Version | Purpose | Why Recommended | Confidence |
|------------|---------|---------|-----------------|------------|
| **@tanstack/react-table** | 8.21.x | Headless table | Server-side sorting, filtering, pagination. Needed for promotion lists, product catalogs, P&L breakdowns. Headless design works with shadcn/ui table components. Type-safe column definitions. | HIGH |

### Financial Calculations

| Technology | Version | Purpose | Why Recommended | Confidence |
|------------|---------|---------|-----------------|------------|
| **decimal.js** | 10.5.x | Arbitrary-precision math | JavaScript floating-point arithmetic is unsuitable for financial calculations (0.1 + 0.2 !== 0.3). TPM requires precise discount calculations, COGS, subsidy amounts, and P&L rollups in KRW (no decimal places, but large numbers up to billions). decimal.js handles this correctly. Prefer over big.js because TPM needs percentage calculations and rounding modes. | MEDIUM |

### Date & Time

| Technology | Version | Purpose | Why Recommended | Confidence |
|------------|---------|---------|-----------------|------------|
| **date-fns** | 4.1.0 | Date manipulation | Already in codebase (v3). v4 is tree-shakable ESM. Promotion date ranges, calendar navigation, date formatting (Korean: YYYY년 MM월 DD일). Use with @date-fns/tz for timezone-safe operations (Asia/Seoul KST). | HIGH |
| **@date-fns/tz** | latest | Timezone support | TPM promotions operate in KST (UTC+9). All date comparisons, conflict detection, and calendar rendering must be timezone-aware. Critical to avoid the "promotion starts a day early" bug common in UTC-stored, locally-displayed dates. | HIGH |

### Internationalization

| Technology | Version | Purpose | Why Recommended | Confidence |
|------------|---------|---------|-----------------|------------|
| **next-intl** | 4.8.x | i18n | Next.js-native. Works with App Router + Server Components. ICU message syntax for Korean pluralization and number formatting. Korean Won formatting (1,000원, 1만원, 1억원). ESM-only in v4. | HIGH |

### Toast & Notifications

| Technology | Version | Purpose | Why Recommended | Confidence |
|------------|---------|---------|-----------------|------------|
| **Sonner** | 2.0.x | Toast notifications | Integrated with shadcn/ui. No hooks or setup required. Used by OpenAI, Adobe. Accessible (ARIA, keyboard nav). Lightweight. For TPM: "Promotion saved", "Conflict detected", "Team member invited" feedback. | HIGH |

### Excel Export

| Technology | Version | Purpose | Why Recommended | Confidence |
|------------|---------|---------|-----------------|------------|
| **SheetJS (xlsx)** | latest | Excel import/export | K-beauty brand managers live in Excel. Export promotion calendars, P&L reports, and ROI analyses to .xlsx. Import historical promotion data from Excel. SheetJS is the de facto standard for browser-side Excel in JS. | MEDIUM |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| **Turbopack** | Dev server bundler | Comes with Next.js 16. Stable file system caching. Replaces Webpack for dev. |
| **ESLint** | Linting | Already configured. Upgrade to ESLint 9 flat config when Next.js officially supports it. |
| **Prettier** | Formatting | Standard config. Use prettier-plugin-tailwindcss for class sorting. |
| **Supabase CLI** | Local DB | Local development with `supabase start`. Migrations, type generation, seeding. |
| **Drizzle Kit** | Schema management | `drizzle-kit generate` for migrations, `drizzle-kit push` for schema sync. Complements Supabase migrations. |

---

## Installation

```bash
# Core framework (upgrade from existing)
npm install next@16 react@19 react-dom@19

# Tailwind CSS v4 (breaking change from v3)
npm install tailwindcss@4 @tailwindcss/postcss

# Database & Auth
npm install @supabase/supabase-js@latest @supabase/ssr@latest
npm install drizzle-orm postgres
npm install -D drizzle-kit

# UI Components (shadcn/ui is copy-paste, not installed)
npx shadcn@latest init
# Then add components: npx shadcn@latest add button dialog dropdown-menu ...

# Data fetching & state
npm install @tanstack/react-query @tanstack/react-query-devtools
npm install nuqs

# Forms & validation (keep Zod v3 for now)
npm install react-hook-form @hookform/resolvers
# zod is already installed

# Calendar
npm install @fullcalendar/react @fullcalendar/core @fullcalendar/daygrid @fullcalendar/timegrid @fullcalendar/interaction

# Tables
npm install @tanstack/react-table

# Charts (upgrade from v2)
npm install recharts@3

# Financial
npm install decimal.js

# Dates (upgrade from v3)
npm install date-fns@4 @date-fns/tz

# i18n
npm install next-intl

# Notifications
npm install sonner

# Excel
npm install xlsx

# Dev dependencies
npm install -D @types/node @types/react @types/react-dom
npm install -D prettier prettier-plugin-tailwindcss
```

---

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| **Supabase** | PlanetScale + Clerk + Uploadthing | If you need MySQL or Supabase's free tier limits become a bottleneck. Not recommended for this project -- Supabase covers auth+db+realtime+storage in one. |
| **Drizzle ORM** | Prisma | If team is already proficient with Prisma. Prisma is heavier (generates client), slower cold starts in serverless. Drizzle is lighter and closer to SQL. |
| **Tailwind CSS v4** | Stay on v3 | If upgrade effort is too risky for the 8-week sprint. v3 works fine. But v4 is significantly faster and shadcn/ui fully supports it. |
| **FullCalendar** | Custom calendar (current) | If your calendar needs are truly unique. FullCalendar saves weeks of dev time for standard calendar interactions. |
| **Recharts** | Visx (Airbnb) | If you need highly custom chart designs or >5000 data points per chart. Overkill for TPM dashboards. |
| **date-fns** | dayjs | If bundle size is the top priority. dayjs is smaller but less tree-shakable. date-fns v4 is already tree-shakable ESM. |
| **Zod v3** | Zod v4 | After ecosystem stabilizes (mid-2026). v4 is 14x faster parsing but @hookform/resolvers integration is new. |
| **decimal.js** | big.js | If you only need basic addition/subtraction. TPM needs percentage calculations and rounding, so decimal.js is better. |
| **next-intl** | next-i18next | Never. next-i18next is for Pages Router. next-intl is the standard for App Router. |
| **SheetJS** | ExcelJS | If you need server-side Excel generation (e.g., scheduled reports via Supabase Edge Functions). SheetJS works both client and server. |

---

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| **Moment.js** | Deprecated, not tree-shakable, mutable API, 72kb gzipped | date-fns v4 |
| **Redux / Redux Toolkit** | Massive boilerplate for what TPM needs. Server state belongs in TanStack Query, not Redux. | TanStack Query + Zustand |
| **Prisma** | Generates heavy client (~2MB), slow serverless cold starts, schema-first approach conflicts with Supabase's migration system | Drizzle ORM |
| **CSS Modules / Styled Components** | Slower, more boilerplate, no utility-class ecosystem. The industry has moved to Tailwind. | Tailwind CSS v4 |
| **Material UI (MUI)** | Opinionated design system that fights customization. Large bundle. Not aligned with the modern shadcn/ui pattern. | shadcn/ui + Radix |
| **tRPC** | Overkill when using Supabase client directly + Next.js API routes. Adds a layer of abstraction with minimal benefit here. | Next.js API Routes + Supabase client |
| **NextAuth.js (Auth.js)** | Unnecessary when Supabase Auth handles everything (email/password, OAuth, session management, RLS integration). Adding NextAuth creates auth-state duplication. | Supabase Auth |
| **Firebase** | Google ecosystem lock-in. No true PostgreSQL. RLS is weaker than Supabase's Postgres RLS. Real-time is different paradigm. | Supabase |
| **react-big-calendar** | Fewer features than FullCalendar. No built-in drag-and-drop. Requires manual implementation for basics. Half the downloads. | @fullcalendar/react |
| **Formik** | Legacy form library. Slower re-renders (controlled components). react-hook-form is the modern standard. | react-hook-form |
| **JavaScript floating-point** | `0.1 + 0.2 !== 0.3`. Unacceptable for KRW financial calculations in P&L, discount amounts, and subsidy tracking. | decimal.js |

---

## Stack Patterns by Variant

**If starting Phase 1 only (Calendar + CRUD):**
- Skip: FullCalendar premium plugins, @tanstack/react-table, decimal.js, SheetJS
- Add later when Phase 2 (P&L, analytics) begins
- Rationale: Reduce initial bundle and complexity

**If targeting mobile-responsive dashboard:**
- Add: `@fullcalendar/list` plugin for mobile list view
- Use: shadcn/ui responsive patterns (sheet for mobile nav, drawer for forms)
- Rationale: Brand managers check promotions on mobile between meetings

**If multi-language from day 1:**
- Setup next-intl immediately with ko/en message files
- Use ICU MessageFormat for all user-facing strings
- Rationale: Retro-fitting i18n is painful; setting up the structure early is cheap

---

## Version Compatibility

| Package A | Compatible With | Notes |
|-----------|-----------------|-------|
| next@16.1.x | react@19.x, react-dom@19.x | Next.js 16 requires React 19. Cannot use React 18. |
| tailwindcss@4.1.x | postcss@8.x, @tailwindcss/postcss | v4 uses CSS-first config (@theme). tailwind.config.js is deprecated. |
| @supabase/ssr@0.8.x | @supabase/supabase-js@2.95.x | Must use matching major versions. SSR package handles cookie-based auth. |
| drizzle-orm@0.45.x | postgres@3.x | Use `postgres` driver (not `pg`). Works with Supabase connection pooler. |
| zod@3.24.x | @hookform/resolvers@5.2.x | Resolvers auto-detect Zod v3 vs v4 at runtime. |
| react-hook-form@7.71.x | @hookform/resolvers@5.2.x | Stable combination. |
| @tanstack/react-query@5.90.x | react@19.x | TanStack Query v5 supports React 19. |
| @fullcalendar/react@6.1.x | react@19.x | FullCalendar v6 supports React 18+. Verify React 19 compatibility before adopting. |
| recharts@3.7.x | react@19.x | Recharts v3 supports React 18+. |
| next-intl@4.8.x | next@16.x, react@19.x | v4 is ESM-only. Requires React 17+. |
| shadcn/ui | tailwindcss@4.x, react@19.x | Full compatibility with both confirmed. |

---

## Migration Notes (From Current Codebase)

### Breaking Changes to Plan For

1. **Next.js 14 -> 16**: React 18 -> 19 is required. `useFormState` renamed to `useActionState`. Some caching behavior changes. Turbopack is now default.
2. **Tailwind CSS v3 -> v4**: `tailwind.config.js` replaced by CSS `@theme` directive. `@apply` still works but CSS-first approach is preferred. Class name changes for some utilities. Run `npx @tailwindcss/upgrade` for automated migration.
3. **Recharts v2 -> v3**: API changes for chart components. Check migration guide.
4. **date-fns v3 -> v4**: ESM-only. Import paths may change.
5. **Zod v3**: Stay on v3 for now. Plan v4 migration for Phase 2.

### New Additions (Not in Current Codebase)

- TanStack Query (replaces manual fetch + useState patterns)
- react-hook-form + @hookform/resolvers (proper form management)
- nuqs (URL state for calendar filters)
- Drizzle ORM (type-safe queries, complements Supabase client)
- next-intl (i18n for Korean/English)
- decimal.js (financial math)
- Sonner (toast notifications)
- @tanstack/react-table (data tables)
- FullCalendar (calendar component, if replacing custom implementation)

---

## Sources

- [Next.js 16.1 release blog](https://nextjs.org/blog/next-16-1) -- Version confirmed via official blog, HIGH confidence
- [Next.js GitHub releases](https://github.com/vercel/next.js/releases) -- v16.1.6 latest, HIGH confidence
- [Tailwind CSS v4.0 announcement](https://tailwindcss.com/blog/tailwindcss-v4) -- v4.1.18 on npm, HIGH confidence
- [Tailwind CSS npm](https://www.npmjs.com/package/tailwindcss) -- Version verified, HIGH confidence
- [Supabase SSR npm](https://www.npmjs.com/package/@supabase/ssr) -- v0.8.0, HIGH confidence
- [@supabase/supabase-js npm](https://www.npmjs.com/package/@supabase/supabase-js) -- v2.95.3, HIGH confidence
- [Drizzle ORM + Supabase docs](https://orm.drizzle.team/) -- v0.45.1 via Context7, HIGH confidence
- [drizzle-orm npm](https://www.npmjs.com/package/drizzle-orm) -- Version verified, HIGH confidence
- [Zod v4 release notes](https://zod.dev/v4) -- v4.1.13 available but v3.24.x recommended for stability, Context7 verified, HIGH confidence
- [@tanstack/react-query npm](https://www.npmjs.com/package/@tanstack/react-query) -- v5.90.21, HIGH confidence
- [@tanstack/react-table npm](https://www.npmjs.com/package/@tanstack/react-table) -- v8.21.3, HIGH confidence
- [nuqs npm](https://www.npmjs.com/package/nuqs) -- v2.8.8, HIGH confidence
- [react-hook-form npm](https://www.npmjs.com/package/react-hook-form) -- v7.71.1, HIGH confidence
- [@hookform/resolvers npm](https://www.npmjs.com/package/@hookform/resolvers) -- v5.2.2, HIGH confidence
- [Recharts npm](https://www.npmjs.com/package/recharts) -- v3.7.0, HIGH confidence
- [@fullcalendar/react npm](https://www.npmjs.com/package/@fullcalendar/react) -- v6.1.20, HIGH confidence
- [date-fns npm](https://www.npmjs.com/package/date-fns) -- v4.1.0, HIGH confidence
- [next-intl npm](https://www.npmjs.com/package/next-intl) -- v4.8.3, HIGH confidence
- [Sonner npm](https://www.npmjs.com/package/sonner) -- v2.0.7, HIGH confidence
- [Turborepo npm](https://www.npmjs.com/package/turbo) -- v2.8.9, HIGH confidence
- [shadcn/ui changelog](https://ui.shadcn.com/docs/changelog) -- Tailwind v4 + React 19 support confirmed, HIGH confidence
- [FullCalendar vs react-big-calendar comparison](https://bryntum.com/blog/react-fullcalendar-vs-big-calendar/) -- MEDIUM confidence (third-party comparison)
- [Recharts vs Visx comparison](https://embeddable.com/blog/react-chart-libraries) -- MEDIUM confidence (third-party comparison)
- [decimal.js vs big.js comparison](https://npm-compare.com/big.js,bignumber.js,decimal.js,decimal.js-light) -- MEDIUM confidence (community comparison)
- [Gartner TPM market review](https://www.gartner.com/reviews/market/trade-promotion-management-and-optimization-for-the-consumer-goods-industry) -- Market context, MEDIUM confidence

---
*Stack research for: Trade Promotion Management SaaS (K-beauty)*
*Researched: 2026-02-17*
