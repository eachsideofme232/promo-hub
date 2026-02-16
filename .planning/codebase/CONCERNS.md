# Codebase Concerns

**Analysis Date:** 2026-02-17

## Incomplete API Integration (CRITICAL)

**Issue:** All core API routes are stubbed with TODO comments. Calendar and promotions pages use static demo data instead of real database queries.

**Files:**
- `apps/web/src/app/api/promotions/route.ts` - GET/POST not implemented
- `apps/web/src/app/api/calendar/route.ts` - Calendar endpoint stub
- `apps/web/src/app/api/teams/route.ts` - Team endpoints stub
- `apps/web/src/app/(dashboard)/calendar/page.tsx:9-88` - DEMO_PROMOTIONS hard-coded
- `apps/web/src/app/(dashboard)/promotions/page.tsx:10-109` - DEMO_PROMOTIONS hard-coded

**Impact:**
- Calendar/promotions pages will not reflect real database changes
- Creating/editing promotions via forms does not persist to database
- No authentication verification on API routes
- Team isolation not enforced

**Fix approach:**
1. Connect calendar/promotions pages to `getPromotions()` from `@promohub/db`
2. Implement full API routes: GET/POST /promotions, GET /calendar, GET /teams, GET /channels, GET /products
3. Add Supabase client initialization and session verification to all routes
4. Replace demo data with actual Supabase queries

---

## Channel ID Inconsistency

**Issue:** Two representations of channels exist - filter system uses string slugs ('oliveyoung') while database uses UUIDs (c1000000-0000-0000-0000-000000000001).

**Files:**
- `apps/web/src/components/filters/FilterProvider.tsx:14-20` - String IDs: 'oliveyoung', 'coupang', etc.
- `supabase/migrations/20240101000001_create_channels.sql` - Database uses UUID primary keys
- `apps/web/src/app/(dashboard)/calendar/page.tsx:91-95` - Maps CHANNELS to channelOptions

**Impact:**
- Frontend filters won't match database channel_id values
- Promotions filtered by channel cannot query correctly
- If channels table is populated with real UUIDs, all filter logic breaks
- Mapping layer needed or inconsistent IDs stored

**Fix approach:**
1. Fetch channels from database API endpoint (`GET /api/channels`)
2. Use database UUIDs consistently throughout the frontend
3. Remove hard-coded CHANNELS from FilterProvider
4. Update all filter comparisons to use UUIDs

---

## Hardcoded Team ID

**Issue:** Demo team ID hard-coded in promotion creation pages. No mechanism to get actual team from authenticated session.

**Files:**
- `apps/web/src/app/(dashboard)/promotions/new/page.tsx:8` - `DEMO_TEAM_ID = '00000000-0000-0000-0000-000000000001'`
- `apps/web/src/app/(dashboard)/promotions/[id]/page.tsx:10` - Same hard-coded team ID
- `apps/web/src/components/layout/UserMenu.tsx:137-139` - Mock team data instead of fetching

**Impact:**
- All created promotions will have the same demo team_id regardless of logged-in user
- Multi-team support is not functional
- Team membership verification not implemented
- Users cannot create separate teams

**Fix approach:**
1. Extract team_id from user's active team in session (via GET /api/teams)
2. Create context/hook to provide current team to all dashboard pages
3. Implement actual team switching in UserMenu component
4. Query user's team memberships from database on mount

---

## Missing Authorization Checks

**Issue:** API endpoints and database queries lack team membership verification. User context not extracted from Supabase session.

**Files:**
- `apps/web/src/app/api/promotions/route.ts` - No auth, no team check
- `apps/web/src/app/api/teams/route.ts` - No auth
- `apps/web/src/app/api/calendar/route.ts` - No auth
- All API route files need Supabase client and `getUser()` call

**Impact:**
- RLS policies exist but are not triggered because API routes could return all data
- No per-team data isolation at application layer
- User ID from session not verified server-side
- Service role key could accidentally be exposed

**Fix approach:**
1. Add to every API route: `const { data: { user } } = await supabase.auth.getUser()`
2. Return 401 if no user present
3. Fetch user's team_id from team_members table
4. Return 403 if user not member of requested team
5. Never use service role key in API routes - only anon/authenticated

---

## Incomplete Mobile Navigation

**Issue:** Mobile navigation has placeholder/incomplete implementation with mock data and TODO for logout.

**Files:**
- `apps/web/src/components/layout/MobileNav.tsx:254-256` - TODO: Implement logout
- `apps/web/src/components/layout/MobileNav.tsx:63-69` - Mock user data instead of real session

**Impact:**
- Mobile users cannot logout properly
- Mobile nav doesn't display real user information
- Could cause issues on mobile production

**Fix approach:**
1. Connect MobileNav to real user session from Supabase
2. Implement logout by calling `supabase.auth.signOut()`
3. Handle sign-out errors appropriately
4. Show actual user email/name from session

---

## Unimplemented Interactive Features

**Issue:** Calendar and promotions pages have click handlers that log to console instead of performing actions.

**Files:**
- `apps/web/src/components/layout/Header.tsx:63` - Global search not implemented
- `apps/web/src/app/(dashboard)/calendar/page.tsx:113-130` - All calendar interactions log only
- Date range changes don't fetch new promotions

**Impact:**
- Users cannot interact with calendar meaningfully
- Cannot create promotions from calendar
- Cannot open promotion details
- Date filtering doesn't update data

**Fix approach:**
1. Implement promotion modal/drawer for creation and detail views
2. Connect calendar clicks to open modal with pre-filled date
3. Connect date range changes to fetch new promotions from API
4. Implement global search across promotions
5. Add navigation to promotion detail pages

---

## Test Coverage Gap

**Issue:** No unit, integration, or E2E tests present for core features.

**Files:**
- No `.test.ts`, `.spec.ts` files in `apps/web/src/` or `packages/`
- No test configuration (Jest/Vitest) in package.json

**Impact:**
- Regressions cannot be detected
- Calendar component date logic untested
- Filter logic untested
- API changes break without notification
- Form validation not verified
- Database migrations not validated

**Risk:** High - Phase 1 focuses on calendar functionality which is completely untested.

**Fix approach:**
1. Set up Vitest or Jest in monorepo
2. Add integration tests for API routes with Supabase
3. Add component tests for calendar views (MonthView, WeekView, DayView)
4. Add tests for filter logic (FilterProvider)
5. Add tests for form validation (PromotionForm)

---

## Fragment Risk in MonthView

**Issue:** Calendar day rendering uses array index as key in map. Day promotions regenerated unnecessarily.

**Files:**
- `apps/web/src/components/calendar/MonthView.tsx:99` - `key={index}` instead of `key={dateKey}`
- `apps/web/src/components/calendar/MonthView.tsx:48-68` - Full promotion map recalculated on every render

**Impact:**
- React can't properly identify which days changed
- Animations/focus may be lost when promotions update
- Performance degradation with large promotion lists
- Potential state confusion if day cells have internal state

**Fix approach:**
1. Change key from `index` to `dateKey` (already formatted as 'yyyy-MM-dd')
2. Consider memoizing individual day cells as separate components
3. Profile rendering performance with 100+ promotions

---

## Form Submission Type Safety Issue

**Issue:** PromotionForm passes raw form data instead of validated data to API.

**Files:**
- `apps/web/src/components/promotions/PromotionForm.tsx:111-136` - Form data passed unvalidated to API

**Details:**
- Form validates with Zod before submit but then passes raw `formData` object
- Validated `result` data is not used for submission
- API cannot trust incoming data
- Mismatch between validation and submission

**Impact:**
- API must re-validate all data (validation done twice)
- Inconsistency between client validation and server
- Form errors may not catch all issues before submission

**Fix approach:**
1. Use validated data from `result.data` for submission, not raw `formData`
2. Ensure API route also validates with same Zod schema
3. Make validation a single source of truth

---

## Error Boundary Missing

**Issue:** No error boundary component exists for graceful error handling in components.

**Files:**
- `apps/web/src/components/common/` - Empty directory, no ErrorBoundary
- All pages could crash without recovery UI

**Impact:**
- Entire page crashes if any component errors
- No fallback UI for users
- Poor error visibility for debugging
- Production users see blank pages

**Fix approach:**
1. Create `apps/web/src/components/common/ErrorBoundary.tsx`
2. Wrap dashboard pages with error boundary
3. Show error message + retry button
4. Log errors for debugging

---

## Channel Color Type Mismatch

**Issue:** Channel colors stored as hex strings, but CalendarPromotion expects optional color field. Inconsistent color handling.

**Files:**
- `apps/web/src/components/filters/FilterProvider.tsx:15` - String colors: '#9ACD32', '#E31837'
- `apps/web/src/components/calendar/CalendarView.tsx:26` - `color?: string` optional
- Channel table has color column but used inconsistently

**Impact:**
- Promotion cards may not display with correct channel colors
- Color field sometimes undefined, sometimes populated
- Hard to maintain color consistency across app

**Fix approach:**
1. Fetch channels with colors from database
2. Map promotion's channelId to color lookup
3. Always pass color to calendar components
4. Use channel colors from database, not from static FilterProvider

---

## Date String Parsing Fragility

**Issue:** ISO date strings parsed inconsistently. Start/end dates split on 'T' without timezone handling.

**Files:**
- `apps/web/src/components/promotions/PromotionForm.tsx:62-63` - `split('T')[0]` for date parsing
- `supabase/migrations/20240101000005_create_promotions.sql:15-16` - Dates stored as DATE type, not TIMESTAMPTZ

**Details:**
- Form assumes ISO format with 'T' separator
- No timezone handling
- Date comparison in calendar assumes local time
- Different date formats in different places

**Impact:**
- Promotions from other timezones may show on wrong dates
- Edge cases at day boundaries
- Date validation doesn't account for timezone

**Fix approach:**
1. Use date-fns for all date parsing: `parse(dateString, 'yyyy-MM-dd', new Date())`
2. Store all dates with consistent timezone (Asia/Seoul for Korean market)
3. Add timezone field to promotions table or document assumption
4. Use consistent date formatting throughout app

---

## Global Search Not Implemented

**Issue:** Search input in header exists but has no functionality.

**Files:**
- `apps/web/src/components/layout/Header.tsx:63` - TODO: Implement global search
- No search API endpoint exists

**Impact:**
- Users expect search to work
- No way to find specific promotions beyond filters
- Scales poorly as promotion count grows

**Fix approach:**
1. Create `GET /api/search` endpoint
2. Implement full-text search in Supabase
3. Debounce search input in header
4. Show dropdown results

---

## Vulnerable Team Context Access

**Issue:** No way to verify user can access specific team. All operations assume current team without validation.

**Files:**
- Team ID passed as parameter to pages without verification
- API routes don't check if user is member of requested team

**Impact:**
- Users could potentially access other teams' data if team ID is guessed
- No protection against team ID enumeration
- SQL injection if team IDs not validated

**Fix approach:**
1. Store current active team in session/context (not URL)
2. Verify team membership in middleware before allowing access
3. Return 403 if user not member of team

---

## Pagination Not Used in Promotions

**Issue:** `getPromotions()` query function supports pagination, but frontend always fetches with default limit.

**Files:**
- `packages/db/queries/promotions.ts:50-79` - Pagination params available
- `apps/web/src/app/(dashboard)/promotions/page.tsx` - Loads all promotions at once
- No pagination controls in UI

**Impact:**
- Large teams with many promotions will load slowly
- Network waterfall if pagination not implemented
- All promotions fetched even if only showing 10

**Fix approach:**
1. Add pagination controls to promotions list
2. Use page parameter in API query
3. Show results per page in UI
4. Implement "Load More" or pagination buttons

---

## Type Mismatch in Calendar Components

**Issue:** Calendar promotion types have inconsistent field names (channelId vs channel_id, etc.).

**Files:**
- `packages/types/src/promotion.ts` - camelCase in Promotion type
- `packages/db/queries/promotions.ts:10-27` - PromotionRow has snake_case
- Conversion handled in `toPromotion()` but error-prone

**Impact:**
- Easy to pass wrong field names to components
- Component bugs if type conversion missed
- Database schema and types can drift

**Fix approach:**
1. Ensure all database rows converted consistently
2. Add types test to verify conversion works
3. Document camelCase/snake_case boundary

---

## Unvalidated URL Parameters

**Issue:** Promotion ID from URL used directly without validation in [id] routes.

**Files:**
- `apps/web/src/app/(dashboard)/promotions/[id]/page.tsx` - ID from URL not validated
- Could fetch non-existent promotion, displaying empty form

**Impact:**
- Bad UX with invalid IDs (blank forms)
- No error handling or 404
- Should verify ID format (UUID)

**Fix approach:**
1. Validate UUID format with Zod
2. Fetch promotion and handle not-found case
3. Show 404 page or redirect if missing

---

## Session Refresh Timing

**Issue:** Auth middleware refreshes session on every request. No caching of session state.

**Files:**
- `apps/web/middleware.ts` - Calls updateSession on all requests
- `apps/web/src/lib/supabase/middleware.ts` - Refreshes token on each request

**Impact:**
- Extra database round-trip on every page change
- Could slow down navigation
- Potential race conditions with concurrent requests

**Fix approach:**
1. Check if session is still valid before refreshing
2. Only refresh if token close to expiration
3. Cache session in memory temporarily

---

## Missing Input Sanitization

**Issue:** Form inputs (title, description, memo) not sanitized before storage or display.

**Files:**
- `apps/web/src/components/promotions/PromotionForm.tsx` - Text inputs not sanitized
- Could allow XSS or data corruption

**Impact:**
- SQL injection if ORM bypass occurs
- XSS if data rendered without React escaping
- Special characters could break CSV exports

**Fix approach:**
1. Ensure Zod validates string formats
2. Use React's automatic HTML escaping in display
3. Sanitize for CSV export if needed

---

## No Conflict Detection UI

**Issue:** Database query `checkPromotionConflicts()` exists but not called or displayed in UI.

**Files:**
- `packages/db/queries/promotions.ts` - Has conflict detection function
- `apps/web/src/components/promotions/PromotionForm.tsx` - No conflict checking

**Impact:**
- Users can create overlapping promotions on same channel/product
- No warning when scheduling conflicts
- One of Phase 1's priority features incomplete

**Fix approach:**
1. Call `checkPromotionConflicts()` before form submission
2. Display warning if conflicts found
3. Allow user to proceed or cancel
4. Document conflict detection rules

---

## Logging Inconsistency

**Issue:** No structured logging framework. Errors logged to console without context.

**Files:**
- `apps/web/src/components/layout/Header.tsx:64` - console.log for unimplemented features
- `apps/web/src/app/(dashboard)/calendar/page.tsx:114-130` - console.log for interactions

**Impact:**
- Cannot track errors in production
- No audit trail for sensitive operations
- Debugging requires manual log tailing

**Fix approach:**
1. Set up Vercel logs or similar
2. Create logger utility for structured logs
3. Log auth events, data mutations, errors
4. Remove console.log statements from production

---

## Timezone Assumptions

**Issue:** Application assumes all dates are in browser timezone. No explicit timezone handling.

**Files:**
- `apps/web/src/components/calendar/` - Uses local Date objects
- Database migrations don't specify timezone assumptions

**Impact:**
- Multi-timezone team coordination will show wrong dates
- Promotions may appear on wrong dates for different users
- Korean market (UTC+9) not explicitly set

**Fix approach:**
1. Document timezone assumption: Asia/Seoul (KST)
2. Convert all display dates to KST
3. Store dates with timezone in database
4. Use date-fns/tz for timezone-aware operations

---

## Dependency Audit Needed

**Issue:** No recent audit of dependencies for security vulnerabilities.

**Files:**
- `apps/web/package.json` - Multiple packages with unknown vulnerability status
- Dependencies: @supabase/*, @radix-ui/*, recharts, zod, date-fns, etc.

**Impact:**
- Known security vulnerabilities could exist in dependencies
- Could allow supply chain attacks
- Compliance/audit requirements

**Fix approach:**
1. Run `npm audit` regularly
2. Set up Dependabot alerts
3. Pin minor/patch versions
4. Regular security reviews (quarterly)

---

*Concerns audit: 2026-02-17*
