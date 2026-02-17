---
phase: 01-foundation
plan: 01
subsystem: database, i18n, auth
tags: [supabase, postgresql, trigger, rls, next-intl, react-context, korean-localization]

# Dependency graph
requires: []
provides:
  - Auto-team creation trigger on auth.users signup
  - Channel schema with team_id (system vs custom channels) and promo_types JSONB
  - Five granular RLS policies for channels (system/custom separation)
  - next-intl Korean localization infrastructure (ko.json, request config, provider)
  - TeamProvider context with useTeam hook for dashboard components
  - Sonner toast notification system
  - react-hook-form + @hookform/resolvers for form management
affects: [01-02, channel-api, channel-ui, promotion-crud, team-management]

# Tech tracking
tech-stack:
  added: [next-intl 4.8.3, react-hook-form 7.71.1, "@hookform/resolvers 5.2.x", sonner 2.0.7]
  patterns: [auto-team-on-signup trigger, system-vs-custom RLS, TeamProvider context, next-intl without routing]

key-files:
  created:
    - supabase/migrations/20240101000007_auto_create_team.sql
    - supabase/migrations/20240101000008_channel_team_id_promo_types.sql
    - apps/web/src/i18n/request.ts
    - apps/web/messages/ko.json
    - apps/web/src/components/providers/TeamProvider.tsx
  modified:
    - supabase/seed.sql
    - apps/web/next.config.mjs
    - apps/web/src/app/layout.tsx
    - apps/web/src/app/(dashboard)/layout.tsx
    - apps/web/middleware.ts
    - packages/types/src/channel.ts
    - apps/web/package.json

key-decisions:
  - "Use SECURITY DEFINER with EXCEPTION handler for signup trigger to never block registration"
  - "Separate RLS policies for system channels (team_id IS NULL) vs custom channels (team_id IS NOT NULL)"
  - "next-intl without i18n routing (single Korean locale, no [locale] path segments)"
  - "TeamProvider wraps inside FilterProvider in dashboard layout"

patterns-established:
  - "Auto-team creation: PostgreSQL trigger on auth.users creates team + membership automatically"
  - "System vs custom channels: team_id NULL = system (visible to all), non-NULL = custom (team-scoped)"
  - "Korean localization: next-intl getRequestConfig with ko.json message catalog"
  - "Team context: useTeam() hook provides teamId to all dashboard client components"

# Metrics
duration: 5min
completed: 2026-02-17
---

# Phase 1 Plan 01: Foundation Pillars Summary

**Auto-team creation trigger, channel schema extension with system/custom RLS, next-intl Korean localization, and TeamProvider context for dashboard**

## Performance

- **Duration:** 5 min
- **Started:** 2026-02-17T14:39:57Z
- **Completed:** 2026-02-17T14:44:28Z
- **Tasks:** 3
- **Files modified:** 13

## Accomplishments
- Auto-team creation trigger on auth.users ensures new signups immediately have a team and owner membership
- Channel schema extended with team_id (nullable FK) and promo_types (JSONB) with 5 granular RLS policies replacing the single permissive one
- next-intl configured for Korean-only locale with comprehensive ko.json (7 namespaces: common, auth, channels, nav, team, errors, validation)
- TeamProvider context provides useTeam() hook for all dashboard components to access current team
- Root layout upgraded to async Server Component with NextIntlClientProvider and Toaster
- Build passes cleanly with all changes

## Task Commits

Each task was committed atomically:

1. **Task 1: Create database migrations for auto-team trigger and channel schema extension** - `4909e99` (feat)
2. **Task 2: Set up next-intl for Korean-only localization** - `f6d6535` (feat)
3. **Task 3: Create TeamProvider context and wire into dashboard layout** - `374235c` (feat)

## Files Created/Modified
- `supabase/migrations/20240101000007_auto_create_team.sql` - Auto-team creation trigger with SECURITY DEFINER and exception handling
- `supabase/migrations/20240101000008_channel_team_id_promo_types.sql` - Channel team_id, promo_types columns, 5 RLS policies, partial index
- `supabase/seed.sql` - Updated channel INSERT with promo_types JSONB per channel
- `packages/types/src/channel.ts` - Added teamId, promoTypes, isSystem, CreateChannelInput, UpdateChannelInput
- `apps/web/next.config.mjs` - Wrapped with createNextIntlPlugin
- `apps/web/src/i18n/request.ts` - next-intl config returning Korean locale with Asia/Seoul timezone
- `apps/web/messages/ko.json` - Comprehensive Korean UI string catalog (7 namespaces)
- `apps/web/src/app/layout.tsx` - Async Server Component with NextIntlClientProvider and Toaster
- `apps/web/src/app/(dashboard)/layout.tsx` - TeamProvider wrapping, channels route title
- `apps/web/middleware.ts` - /channels added to protected routes
- `apps/web/src/components/providers/TeamProvider.tsx` - Team context with useTeam hook
- `apps/web/package.json` - Added next-intl, react-hook-form, @hookform/resolvers, sonner
- `package-lock.json` - Updated lockfile

## Decisions Made
- Used `SECURITY DEFINER` with `SET search_path = public` and EXCEPTION handler for the auto-team trigger to never block user signup even on failure
- Created separate RLS policies for system channels (team_id IS NULL, visible to all) vs custom channels (team_id IS NOT NULL, team-scoped) instead of a combined policy
- Configured next-intl without i18n routing (single locale) since PromoHub is Korean-first
- TeamProvider placed inside FilterProvider in dashboard layout wrapping order

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed Supabase join query type assertion in TeamProvider**
- **Found during:** Task 3 (TeamProvider context)
- **Issue:** `data.teams as Record<string, unknown>` failed TypeScript strict check because Supabase returns join results as array type, not Record
- **Fix:** Changed to `data.teams as unknown as Record<string, unknown>` (double assertion via unknown)
- **Files modified:** `apps/web/src/components/providers/TeamProvider.tsx`
- **Verification:** `npx next build` passes cleanly
- **Committed in:** 374235c (Task 3 commit)

---

**Total deviations:** 1 auto-fixed (1 bug fix)
**Impact on plan:** Minor type assertion fix required for TypeScript strict mode compliance. No scope creep.

## Issues Encountered
None - all tasks executed cleanly with only the type assertion fix noted above.

## User Setup Required
None - no external service configuration required. Migrations will apply when Supabase is set up.

## Next Phase Readiness
- Database migrations ready for auto-team creation and channel schema extension
- next-intl infrastructure ready for all UI components to use Korean strings via useTranslations()
- TeamProvider ready for API routes and components to access current team context
- Channel API routes (Plan 02) can now query channels with team_id scoping and RLS
- All foundation pillars in place for channel management UI and API implementation

## Self-Check: PASSED

- All 6 key files verified present on disk
- All 3 task commits verified in git log (4909e99, f6d6535, 374235c)
- Build passes cleanly (`npx next build` succeeds)

---
*Phase: 01-foundation*
*Completed: 2026-02-17*
