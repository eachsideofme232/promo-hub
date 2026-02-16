# Architecture

**Analysis Date:** 2026-02-17

## Pattern Overview

**Overall:** Next.js App Router with Turborepo monorepo structure. Multi-tenant SaaS using Supabase for authentication, database, and Row Level Security (RLS) for data isolation.

**Key Characteristics:**
- Server-side rendering (SSR) with Next.js 14 App Router
- Client components for interactive features (filters, forms, calendar views)
- Monorepo with shared packages for types, utilities, database queries, and UI components
- Multi-tenant architecture with team-based data scoping
- Supabase integration with RLS policies for secure multi-tenant isolation
- Zustand for client-side state management (filters)
- Context API for filter state management across pages

## Layers

**Presentation (Frontend):**
- Purpose: User interface and client-side interactions
- Location: `apps/web/src/app` (pages), `apps/web/src/components` (reusable UI)
- Contains: Page components (App Router), layout components, interactive filters, calendar views, forms
- Depends on: Shared types (`@promohub/types`), utilities (`@promohub/utils`), Supabase client
- Used by: End users accessing the web application

**API Layer:**
- Purpose: Server-side endpoints for data operations and webhooks
- Location: `apps/web/src/app/api`
- Contains: Route handlers for promotions, calendar, teams, channels, auth callbacks, webhooks
- Depends on: Supabase server client, database queries (`@promohub/db`), validation schemas (`@promohub/utils`)
- Used by: Frontend pages and external services (webhooks)

**Database Query Layer:**
- Purpose: Typed, reusable database query functions with type conversion
- Location: `packages/db/queries`
- Contains: Query functions for promotions, calendar, teams, channels, products
- Depends on: Supabase client, shared types (`@promohub/types`)
- Used by: API routes and server-side pages

**Data Layer:**
- Purpose: Supabase PostgreSQL database with Row Level Security
- Location: `supabase/migrations/`, `supabase/seed.sql`
- Contains: Table schemas, RLS policies, indexes, triggers
- Depends on: PostgreSQL, Supabase Auth
- Used by: Query layer via Supabase client

**Shared Packages:**
- Purpose: Reusable code across applications and layers
- Location: `packages/`
- Contains: TypeScript types, validation schemas, utilities, UI components, database configuration
- Depends on: External libraries (Zod, date-fns, Radix UI, Tailwind)
- Used by: Frontend, API routes, database queries

## Data Flow

**Promotion List Display:**

1. User navigates to `/promotions` (client browser)
2. Middleware verifies authentication via Supabase session
3. Dashboard layout renders with FilterProvider (client component wrapping context)
4. Page component (`PromotionsPage`) initializes with demo data (in-memory state)
5. FilterProvider manages URL-based filter state (channels, statuses, date range)
6. PromotionList component renders filtered promotions
7. (Future) API route `/api/promotions` called with filter params
8. (Future) Query function `getPromotions()` executes with team scoping
9. (Future) Supabase RLS policies enforce team data isolation

**Calendar View Display:**

1. User navigates to `/calendar` (client browser)
2. Middleware authentication check
3. Dashboard layout renders with FilterProvider
4. Calendar page component receives filter context
5. CalendarView component accepts filtered promotions and displays in month/week/day format
6. Navigation handlers update date range and trigger re-renders
7. (Future) useEffect observes filter changes and refetches from API

**Authentication Flow:**

1. User accesses protected route (e.g., `/calendar`)
2. Middleware calls `updateSession()` from Supabase client
3. If no valid session, redirects to `/login`
4. Login page uses Supabase Auth (email/password or OAuth)
5. On successful auth, `auth.callback` route processes OAuth redirect
6. Session stored in secure HTTP-only cookies
7. Supabase client automatically includes session in all requests
8. RLS policies verify user's team membership before returning data

**State Management:**

- **Client-side filters:** Zustand store in `FilterProvider` context (URL-synced, persistent)
- **Page state:** React useState for promotions list, form inputs
- **Server session:** Supabase Auth session in cookies (managed by middleware)
- **Database state:** PostgreSQL tables with Supabase as interface

## Key Abstractions

**Supabase Client Factory:**
- Purpose: Create authenticated database clients (browser or server)
- Examples: `apps/web/src/lib/supabase/client.ts`, `apps/web/src/lib/supabase/server.ts`
- Pattern: Factory functions returning configured Supabase clients with proper authentication context

**Query Functions:**
- Purpose: Type-safe, reusable database operations with result conversion
- Examples: `packages/db/queries/promotions.ts`, `packages/db/queries/calendar.ts`
- Pattern: Async functions accepting Supabase client + params, returning `{ data, error }` result objects. Input/output type conversion (camelCase ↔ snake_case) handled here.

**Validation Schemas:**
- Purpose: Runtime input validation and type inference
- Examples: `promotionSchema`, `teamInviteSchema` in `packages/utils/src/validation.ts`
- Pattern: Zod schemas defining input requirements. Used in API routes and forms. SafeParse helper returns typed data or structured errors.

**Filter Context (FilterProvider):**
- Purpose: Centralized filter state management with URL synchronization
- Location: `apps/web/src/components/filters/FilterProvider.tsx`
- Pattern: React Context providing filter state + action functions. Updates reflected in URL search params for bookmarkable, shareable filter states.

**Layout Composition:**
- Purpose: Consistent dashboard structure across pages
- Location: `apps/web/src/app/(dashboard)/layout.tsx`
- Pattern: Root layout renders sidebar, header, and optional filter sidebar. Detects which routes should show filters via `FILTER_ENABLED_PATHS` constant.

## Entry Points

**Web Application:**
- Location: `apps/web/src/app/layout.tsx`
- Triggers: Browser loads `https://app.promohub.com/`
- Responsibilities: Set metadata, fonts, global styles. Render root children.

**Authentication Pages:**
- Location: `apps/web/src/app/(auth)/login/page.tsx`, `apps/web/src/app/(auth)/signup/page.tsx`
- Triggers: User navigates to `/login` or `/signup` OR middleware redirects from protected route
- Responsibilities: Render login/signup forms, call Supabase Auth, redirect to dashboard on success

**Dashboard Pages:**
- Location: `apps/web/src/app/(dashboard)/calendar/page.tsx`, `apps/web/src/app/(dashboard)/promotions/page.tsx`, etc.
- Triggers: Authenticated user navigates to `/calendar`, `/promotions`, `/settings`
- Responsibilities: Fetch data (currently demo), render page-specific content within dashboard layout

**API Routes:**
- Location: `apps/web/src/app/api/promotions/route.ts`, `apps/web/src/app/api/auth/callback/route.ts`, etc.
- Triggers: Frontend fetch requests, external webhooks
- Responsibilities: Verify authentication, validate input, execute database queries, return JSON responses

**Middleware:**
- Location: `apps/web/middleware.ts`
- Triggers: Every request matching `matcher` config
- Responsibilities: Refresh Supabase session, redirect unauthenticated users to login, prevent authenticated users from accessing auth pages

## Error Handling

**Strategy:** Layered error handling with specific error types and user-friendly messages.

**Patterns:**

- **Query functions:** Return `{ data, error }` tuples. Errors captured from Supabase client. Caller decides how to handle (throw, log, display to user).

  ```typescript
  const { data, error } = await getPromotions(supabase, params)
  if (error) {
    console.error('Failed to fetch promotions:', error)
    return Response.json({ error: 'Failed to fetch' }, { status: 500 })
  }
  ```

- **API routes:** Validate input with Zod. Return error response with appropriate status code if validation fails. Catch database errors and return 500 with generic message (don't expose internal errors).

  ```typescript
  const parsed = promotionSchema.safeParse(body)
  if (!parsed.success) {
    return Response.json({ error: 'Invalid input', errors: parsed.error.flatten() }, { status: 400 })
  }
  ```

- **Client-side:** Form components show validation errors from Zod schema. Async operations display loading states and error toasts (when toast library added).

- **Middleware:** Errors in session refresh caught and user redirected to login gracefully.

## Cross-Cutting Concerns

**Logging:** Console-based for now. Structured logs should include user ID, action, team ID, timestamp. (Future: integration with observability platform)

**Validation:** Zod schemas in `packages/utils/src/validation.ts` used at API route entry points. Frontend forms validate before submission.

**Authentication:** Supabase Auth handles user login/signup. Middleware refreshes session on every request. Authenticated routes verified server-side in API routes and protected pages.

**Authorization (Data Isolation):** Supabase RLS policies enforce team-based data access. All queries include `team_id` filter from user's session. API routes verify team membership before returning user data. No client-side IDs trusted.

**Multi-Tenancy:** Every data table has `team_id` column. RLS policies check `team_id IN (SELECT team_id FROM team_members WHERE user_id = auth.uid())`. All API queries require `teamId` parameter.

---

*Architecture analysis: 2026-02-17*
