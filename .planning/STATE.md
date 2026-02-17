# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-02-17)

**Core value:** Brand managers can see all promotions on a calendar, know exactly whether each promotion was profitable (full margin P&L), and make data-driven decisions about which promo mechanics to repeat or kill -- across all Korean e-commerce channels.
**Current focus:** Phase 2: Products & Channels

## Current Position

Phase: 2 of 8 (Products & Channels)
Plan: 2 of 2 in current phase (COMPLETE)
Status: Phase Complete
Last activity: 2026-02-18 -- Completed 02-02-PLAN.md (product UI: ProductList, ProductForm, products page with CRUD)

Progress: [▓▓▓▓░░░░░░] 25%

## Performance Metrics

**Velocity:**
- Total plans completed: 5
- Average duration: 4 min
- Total execution time: 0.32 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 01-foundation | 3 | 13 min | 4 min |
| 02-products-channels | 2 | 6 min | 3 min |

**Recent Trend:**
- Last 5 plans: 01-02 (5 min), 01-03 (3 min), 02-01 (4 min), 02-02 (2 min)
- Trend: Stable/improving

*Updated after each plan completion*

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- Fresh start over extending existing code (cleaner architecture for TPM data models)
- Simon-Kucher ROI methodology (industry-standard framework)
- Manual data entry first (faster to ship; channel APIs deferred)
- Multi-tenant from day one (avoid painful migration later)
- SECURITY DEFINER with EXCEPTION handler for signup trigger (never block registration)
- Separate RLS policies for system channels (team_id IS NULL) vs custom channels
- next-intl without i18n routing (single Korean locale, no [locale] path segments)
- TeamProvider wraps inside FilterProvider in dashboard layout
- Helper functions for auth context and channel ownership in API routes (reduce duplication)
- Channel API maps snake_case DB to camelCase response; isSystem derived from team_id === null
- Channel form uses slide-over panel; auto-slug generation strips Korean chars
- FormattedWon component uses compact prop to switch between formatWon and formatKoreanNumber
- workspace:* changed to * for npm workspace compatibility
- productFormSchema excludes teamId (injected server-side from team membership)
- channelPrices uses delete-then-insert on PATCH (simpler than diffing, atomic)
- productSchema kept as alias for backward compatibility with productBulkImportSchema
- Product API follows channel API helper pattern (getAuthContext, verifyProductOwnership)
- ProductFormInput bridge type for react-hook-form with zodResolver (input type != Zod output type)
- Set-based expansion tracking for expandable table rows (O(1) toggle)
- Product CRUD page follows exact channels page pattern (useCallback, useTeam, toast, slide-over)

### Pending Todos

None yet.

### Blockers/Concerns

- Research flagged: existing codebase has ~55% of Phase 1 UI done but this is a fresh start -- reference only, not reuse
- Research flagged: Simon-Kucher terminology needs validation with Korean brand managers during Phase 6

## Session Continuity

Last session: 2026-02-18
Stopped at: Completed 02-02-PLAN.md (product UI: ProductList, ProductForm, products page with full CRUD). Phase 02 complete. Phase 03 next.
Resume file: None
