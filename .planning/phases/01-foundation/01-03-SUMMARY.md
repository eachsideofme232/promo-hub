---
phase: 01-foundation
plan: 03
subsystem: ui
tags: [currency, korean-won, next-intl, react-component, gap-closure]

# Dependency graph
requires:
  - phase: 01-foundation/02
    provides: Channel management page and API routes
provides:
  - FormattedWon reusable Korean Won currency component
  - Currency formatting pipeline proven end-to-end (utils -> component -> page)
  - Dashboard i18n namespace with Korean channel stats strings
  - Fixed ChannelForm submit button HTML
affects: [promotions, calendar, dashboard]

# Tech tracking
tech-stack:
  added: ["@promohub/utils workspace dependency in apps/web"]
  patterns: ["FormattedWon wraps formatWon/formatKoreanNumber for consistent currency display"]

key-files:
  created:
    - apps/web/src/components/common/FormattedWon.tsx
  modified:
    - apps/web/src/app/(dashboard)/channels/page.tsx
    - apps/web/messages/ko.json
    - apps/web/package.json
    - apps/web/src/components/channels/ChannelForm.tsx

key-decisions:
  - "FormattedWon uses compact prop to switch between formatWon (default) and formatKoreanNumber"
  - "workspace:* changed to * for npm workspace compatibility (plan said workspace:* but project uses npm)"

patterns-established:
  - "FormattedWon component: use <FormattedWon value={n} /> for standard display, add compact prop for Korean units"
  - "Dashboard i18n namespace: use useTranslations('dashboard') for cross-page dashboard strings"

# Metrics
duration: 3min
completed: 2026-02-18
---

# Phase 1 Plan 3: Gap Closure Summary

**FormattedWon component wiring Korean Won currency from @promohub/utils into channels page, plus ChannelForm submit button fix**

## Performance

- **Duration:** 3 min
- **Started:** 2026-02-17T15:11:40Z
- **Completed:** 2026-02-17T15:15:34Z
- **Tasks:** 2
- **Files modified:** 6

## Accomplishments
- Created reusable `FormattedWon` component that imports `formatWon`/`formatKoreanNumber` from `@promohub/utils`
- Wired currency display into channels page via stats summary row showing Korean Won formatting
- Closed LOC-01 verification gap: Korean Won currency formatting now exercised in Phase 1 UI
- Fixed ChannelForm submit button HTML anti-pattern (broken `form` attribute removed)

## Task Commits

Each task was committed atomically:

1. **Task 1: Create FormattedWon component and wire currency display** - `a928f18` (feat)
2. **Task 2: Fix ChannelForm submit button form attribute** - `a4dd362` (fix)

## Files Created/Modified
- `apps/web/src/components/common/FormattedWon.tsx` - Reusable Korean Won currency display component
- `apps/web/src/app/(dashboard)/channels/page.tsx` - Added stats summary with FormattedWon and dashboard translations
- `apps/web/messages/ko.json` - Added dashboard i18n namespace with channel stats strings
- `apps/web/package.json` - Added @promohub/utils workspace dependency
- `package-lock.json` - Updated lockfile for workspace dependency
- `apps/web/src/components/channels/ChannelForm.tsx` - Removed broken form attribute, changed button type

## Decisions Made
- Used `*` instead of `workspace:*` for npm workspace dependency (plan specified `workspace:*` but project uses npm which does not support that protocol)
- FormattedWon compact mode appends "원" to formatKoreanNumber output for consistency (e.g., "15만원")

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Changed workspace:* to * for npm compatibility**
- **Found during:** Task 1 (adding @promohub/utils dependency)
- **Issue:** Plan specified `"@promohub/utils": "workspace:*"` but the project uses npm workspaces (packageManager: npm@10.9.0), which does not support the `workspace:` protocol (that is pnpm/yarn-specific)
- **Fix:** Used `"@promohub/utils": "*"` which is the correct npm workspace syntax
- **Files modified:** apps/web/package.json
- **Verification:** `npm install` succeeds, build passes
- **Committed in:** a928f18 (Task 1 commit)

---

**Total deviations:** 1 auto-fixed (1 blocking)
**Impact on plan:** Trivial syntax fix for package manager compatibility. No scope creep.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- All Phase 1 verification criteria now satisfiable including LOC-01 currency requirement
- FormattedWon component ready for reuse across promotions, calendar, and dashboard pages
- Foundation phase (01) fully complete with all 3 plans executed

## Self-Check: PASSED

- FOUND: apps/web/src/components/common/FormattedWon.tsx
- FOUND: .planning/phases/01-foundation/01-03-SUMMARY.md
- FOUND: a928f18 (Task 1 commit)
- FOUND: a4dd362 (Task 2 commit)

---
*Phase: 01-foundation*
*Completed: 2026-02-18*
