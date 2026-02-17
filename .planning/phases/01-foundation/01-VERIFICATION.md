---
phase: 01-foundation
verified: 2026-02-17T15:18:06Z
status: passed
score: 5/5 must-haves verified
re_verification:
  previous_status: gaps_found
  previous_score: 4/5
  gaps_closed:
    - "UI displays Korean Won currency (formatWon/formatKoreanNumber) wired into channels page via FormattedWon component"
  gaps_remaining: []
  regressions: []
human_verification:
  - test: "Sign up with a new email and confirm the auto-team creation"
    expected: "After email confirmation user lands on /calendar. A team row exists in the teams table with name ending in '의 팀' and a team_members row with role='owner'"
    why_human: "Cannot verify PostgreSQL trigger execution without a live Supabase instance"
  - test: "Visit /channels as an authenticated user"
    expected: "Pre-seeded Korean channels (올리브영, 쿠팡, 네이버, 카카오, 무신사) appear with Korean names, color swatches, promo type tags, and a lock icon labeled '기본 채널'. Edit and delete buttons are absent for system channels."
    why_human: "Visual layout and Korean text rendering require browser confirmation"
  - test: "Create a custom channel with name, slug, and color"
    expected: "Channel appears in the list with '사용자 채널' badge and edit/delete buttons. Toast shows '채널이 추가되었습니다'. Attempting to access the channel API without auth returns 401."
    why_human: "End-to-end flow requires live Supabase auth session"
---

# Phase 1: Foundation Verification Report

**Phase Goal:** Users can securely access PromoHub with team-scoped data isolation and a Korean-native interface
**Verified:** 2026-02-17T15:18:06Z
**Status:** passed
**Re-verification:** Yes — after gap closure (LOC-01 currency wiring)

## Re-Verification Summary

Previous status: `gaps_found` (4/5, 2026-02-17T14:57:16Z)
Current status: `passed` (5/5)

Commits that closed the gap:
- `a928f18` — `feat(01-03): create FormattedWon component and wire currency into channels page`
- `a4dd362` — `fix(01-03): remove broken form attribute from ChannelForm submit button`

Gap closed: `packages/utils/src/currency.ts` is now wired into a Phase 1 UI via `apps/web/src/components/common/FormattedWon.tsx`, which is rendered on the channels page stats summary.

Anti-pattern fixed: `apps/web/src/components/channels/ChannelForm.tsx` submit button no longer carries broken `form="channel-form-submit"` attribute referencing a non-existent form id.

No regressions detected across previously passing truths 1, 2, 4, and 5.

---

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|---------|
| 1 | User can sign up and log in with email/password and reach the dashboard | VERIFIED | Login calls `supabase.auth.signInWithPassword`, signup calls `supabase.auth.signUp`. Middleware redirects `/calendar`, `/promotions`, `/settings`, `/products`, `/channels` to `/login` if no user. Auth callback at `/api/auth/callback/route.ts` exchanges code for session. No regression. |
| 2 | User data is completely isolated — one team cannot see another team's data (RLS enforced) | VERIFIED | Migration `20240101000008` drops permissive channel policy and creates 5 granular RLS policies separating `team_id IS NULL` (system, visible to all) from `team_id IS NOT NULL` (custom, team-scoped). Auto-team trigger creates isolated team + `team_members` row on signup. All API routes query `team_members` before returning data. No regression. |
| 3 | UI displays Korean dates (YYYY-MM-DD), Korean Won currency (1,000 / 1만 / 1억), and KST timezone throughout | VERIFIED | Dates: calendar uses `format(date, 'yyyy년 M월 d일', { locale: ko })`. KST: `i18n/request.ts` sets `timeZone: 'Asia/Seoul'`. Currency: `FormattedWon` component imports `formatWon` and `formatKoreanNumber` from `@promohub/utils`. Channels page renders `<FormattedWon value={0} />` in the monthly budget stat card. Full wiring chain confirmed. |
| 4 | Pre-seeded Korean e-commerce channels (OliveYoung, Coupang, Naver, Kakao, Musinsa) appear in the system with Korean names and channel-specific promo types | VERIFIED | `supabase/seed.sql` inserts 8 channels (올리브영, 쿠팡, 네이버, 카카오, 무신사, SSG, 롯데ON, 11번가) with Korean names and channel-specific `promo_types` JSONB. GET `/api/channels` returns them with `isSystem: true`. `ChannelList.tsx` renders promo type tags and system badge. No regression. |
| 5 | User can add custom channels beyond the pre-seeded Korean ones | VERIFIED | POST `/api/channels` validates with Zod, inserts with `team_id: membership.team_id`. PATCH and DELETE block system channels (returns 403 "시스템 채널은 수정할 수 없습니다"). Full CRUD wired through channels page via `fetch('/api/channels')` with `useTeam()` gating. No regression. |

**Score:** 5/5 truths verified

---

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `supabase/migrations/20240101000007_auto_create_team.sql` | Auto-team creation trigger | VERIFIED | `SECURITY DEFINER`, `handle_new_user()` function, `on_auth_user_created` trigger, EXCEPTION handler. Present on disk. |
| `supabase/migrations/20240101000008_channel_team_id_promo_types.sql` | Channel schema with team_id and promo_types | VERIFIED | Adds `team_id UUID REFERENCES teams(id)`, `promo_types JSONB`, 5 granular RLS policies. Present on disk. |
| `apps/web/src/i18n/request.ts` | next-intl config for Korean locale | VERIFIED | Returns `locale: 'ko'`, `timeZone: 'Asia/Seoul'`. |
| `apps/web/messages/ko.json` | Korean UI message catalog | VERIFIED | 8 namespaces: common, auth, channels, dashboard, nav, team, errors, validation — all values in Korean. `dashboard` namespace added in gap closure. |
| `apps/web/src/components/providers/TeamProvider.tsx` | Team context provider and useTeam hook | VERIFIED | Exports `TeamProvider` and `useTeam`. Queries `team_members` with Supabase join. |
| `apps/web/next.config.mjs` | next-intl plugin wrapping | VERIFIED | Uses `createNextIntlPlugin()` wrapping `nextConfig`. |
| `apps/web/src/app/layout.tsx` | Async root layout with NextIntlClientProvider and Toaster | VERIFIED | Calls `getLocale()` and `getMessages()`, wraps with `NextIntlClientProvider`. |
| `apps/web/src/app/(dashboard)/layout.tsx` | TeamProvider wired into dashboard layout | VERIFIED | Imports and renders `TeamProvider` inside `FilterProvider`. |
| `apps/web/middleware.ts` | Auth middleware protecting routes | VERIFIED | Protects `/calendar`, `/promotions`, `/settings`, `/products`, `/channels`. |
| `apps/web/src/app/api/channels/route.ts` | GET and POST channel endpoints | VERIFIED | GET returns system + team channels with `isSystem` flag. POST validates with Zod, inserts with `team_id`. |
| `apps/web/src/app/api/channels/[id]/route.ts` | PATCH and DELETE channel endpoints | VERIFIED | System channel protection (403), team ownership verification, Zod validation. |
| `apps/web/src/app/(dashboard)/channels/page.tsx` | Channel management page | VERIFIED | Uses `useTeam()`, fetches on mount, handles create/edit/delete with toast feedback, renders stats summary with `FormattedWon`. |
| `apps/web/src/components/channels/ChannelList.tsx` | Channel list component | VERIFIED | Color swatches, promo type tags, system badge with lock icon, edit/delete buttons (disabled for system channels). |
| `apps/web/src/components/channels/ChannelForm.tsx` | Channel form with validation | VERIFIED | `react-hook-form` + `zodResolver`, auto-slug generation, Korean error messages, slide-over panel. Broken form attribute fixed. |
| `apps/web/src/components/common/FormattedWon.tsx` | Korean Won currency display component | VERIFIED | Imports `formatWon` and `formatKoreanNumber` from `@promohub/utils`. Renders `<span>` with formatted value. Wired into channels page stats summary. |
| `packages/utils/src/currency.ts` | Korean Won currency utilities | VERIFIED | `formatWon`, `formatKoreanNumber` implemented and exported via `packages/utils/src/index.ts`. `@promohub/utils` declared in `apps/web/package.json`. |

---

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `apps/web/src/app/layout.tsx` | `apps/web/src/i18n/request.ts` | `NextIntlClientProvider` wrapping body | WIRED | `getMessages()` called, children wrapped |
| `apps/web/src/app/(dashboard)/layout.tsx` | `apps/web/src/components/providers/TeamProvider.tsx` | `TeamProvider` wrapping dashboard content | WIRED | Imports and renders `TeamProvider` |
| `supabase/migrations/20240101000007_auto_create_team.sql` | teams + team_members tables | `INSERT INTO public.teams` | WIRED | Inserts team then member via trigger |
| `apps/web/src/app/(dashboard)/channels/page.tsx` | `/api/channels` | `fetch('/api/channels')` in `useEffect` | WIRED | Fetches on mount when `teamId` is ready |
| `apps/web/src/app/api/channels/route.ts` | `supabase.from('channels')` | Supabase client query | WIRED | Queries with `.or('team_id.is.null,team_id.eq.${membership.team_id}')` |
| `apps/web/src/components/channels/ChannelForm.tsx` | `/api/channels` via POST | `fetch` in channels page `handleCreate` | WIRED | Page submits via POST with JSON body |
| `apps/web/src/components/common/FormattedWon.tsx` | `packages/utils/src/currency.ts` | `import { formatWon, formatKoreanNumber } from '@promohub/utils'` | WIRED | Both functions imported and called. `@promohub/utils: "*"` in apps/web/package.json. Package exports via `src/index.ts`. |
| `apps/web/src/app/(dashboard)/channels/page.tsx` | `FormattedWon` | `import { FormattedWon } from '@/components/common/FormattedWon'` | WIRED | Rendered at line 177 as `<FormattedWon value={0} />` in monthly budget stat card |

---

### Requirements Coverage

| Requirement | Status | Blocking Issue |
|-------------|--------|----------------|
| TEAM-01: User can sign up and log in with email/password | SATISFIED | Login/signup pages call Supabase Auth, middleware protects routes |
| TEAM-02: User data isolated per team (multi-tenant with RLS) | SATISFIED | Auto-team trigger + 5 RLS policies on channels + team_members scoping in all API routes |
| LOC-01: UI displays in Korean (dates, currency in KRW, KST timezone) | SATISFIED | Dates verified, timezone verified, KRW currency now wired via FormattedWon on channels page |
| LOC-02: All Korean e-commerce channels pre-seeded with Korean names and promo types | SATISFIED | seed.sql has 8 channels with Korean names + promo_types JSONB |
| PROD-03: User can manage channels (pre-seeded Korean channels + custom) | SATISFIED | Full CRUD via /api/channels + channels page, system channels protected from edit/delete |

---

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| _(none)_ | — | — | — | All previously flagged anti-patterns resolved |

Previously flagged:
- `ChannelForm.tsx` broken `form="channel-form-submit"` attribute — FIXED in commit `a4dd362`. Submit button is now `type="button"` with `onClick={handleSubmit(onSubmit)}`.
- `currency.ts` orphaned utilities — FIXED in commit `a928f18`. `FormattedWon` component created and wired into channels page.

---

### Human Verification Required

#### 1. Auto-Team Creation on Signup

**Test:** Sign up with a new email address via `/signup`
**Expected:** After email confirmation, user is redirected to `/calendar`. In Supabase dashboard, a row exists in `teams` with `name` ending in `의 팀` and a corresponding row in `team_members` with `user_id` matching the new user and `role = 'owner'`
**Why human:** Cannot verify PostgreSQL trigger execution without a running Supabase instance connected to a live database

#### 2. Korean Channels Visible on /channels Page

**Test:** Log in and navigate to `/channels`
**Expected:** Pre-seeded channels appear with Korean names (올리브영, 쿠팡, 네이버, 카카오, 무신사 minimum). Each shows a color swatch, slug, promo type tags, and a lock icon labeled `기본 채널`. Edit and delete buttons are absent for system channels. Stats row shows "월 예산" card with "0원" rendered by `FormattedWon`.
**Why human:** Visual rendering with Korean characters requires browser confirmation

#### 3. Custom Channel CRUD Flow

**Test:** Create a new channel with a custom name, slug (e.g., `my-channel`), and color. Then edit it. Then delete it.
**Expected:** Each operation shows a Korean toast message (채널이 추가되었습니다, 채널이 수정되었습니다, 채널이 삭제되었습니다). The custom channel shows `사용자 채널` badge with edit/delete buttons. Pre-seeded channels remain unchanged.
**Why human:** End-to-end flow requires live Supabase auth session and database

---

### Gap Closure Verification Detail

**LOC-01 Currency — CLOSED**

The gap required at least one Phase 1 UI surface to render Korean Won using `formatWon` or `formatKoreanNumber`.

Wiring chain confirmed:
1. `packages/utils/src/currency.ts` — `formatWon(value: number): string` returns `${KR_NUMBER_FORMATTER.format(value)}원`
2. `packages/utils/src/index.ts` — `export * from './currency'` makes both functions available as `@promohub/utils`
3. `apps/web/package.json` — `"@promohub/utils": "*"` declares the workspace dependency
4. `apps/web/src/components/common/FormattedWon.tsx` — imports `formatWon` and `formatKoreanNumber`, exposes a `<FormattedWon value={number} compact={boolean} />` component
5. `apps/web/src/app/(dashboard)/channels/page.tsx` line 9 — `import { FormattedWon } from '@/components/common/FormattedWon'`
6. `apps/web/src/app/(dashboard)/channels/page.tsx` line 177 — `<FormattedWon value={0} />` renders in the "월 예산" stat card

All six links in the chain are present and substantive. The gap is closed.

---

_Verified: 2026-02-17T15:18:06Z_
_Verifier: Claude (gsd-verifier)_
