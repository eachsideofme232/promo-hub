# External Integrations

**Analysis Date:** 2026-02-17

## APIs & External Services

**Korean E-commerce Channels (Demo only - NOT integrated):**
- Oliveyoung - Korean beauty retailer
  - Channel ID: `c1000000-0000-0000-0000-000000000001`
  - Status: Schema only, demo data in `supabase/seed.sql`
- Coupang - Korean marketplace
  - Channel ID: `c1000000-0000-0000-0000-000000000002`
  - Status: Schema only
- Naver - Korean search/commerce platform
  - Channel ID: `c1000000-0000-0000-0000-000000000003`
  - Status: Schema only
- Kakao - Korean messenger/commerce
  - Channel ID: `c1000000-0000-0000-0000-000000000004`
  - Status: Schema only
- Musinsa - Fashion/beauty platform
  - Channel ID: `c1000000-0000-0000-0000-000000000005`
  - Status: Schema only

**Status:** Channels stored in database (`public.channels` table), no live API connections yet. Phase 2-3 feature to add connector integrations via environment variables.

## Data Storage

**Database:**
- Supabase (PostgreSQL 17)
  - Cloud: `NEXT_PUBLIC_SUPABASE_URL` (project URL)
  - Local: `http://127.0.0.1:54321` (via Docker + Supabase CLI)
  - Client: `@supabase/supabase-js` 2.45.0
  - Connection pooler: Disabled locally (available for Supabase Cloud Pro)

**File Storage:**
- Supabase Storage (S3-compatible)
  - Status: Schema configured, not yet used
  - Config: `supabase/config.toml` - File size limit 50MiB
  - Buckets: Can be configured in `[storage.buckets.*]` section
  - Purpose: Future use for promotion images, product photos, templates

**Caching:**
- None detected - Supabase Realtime available but not actively cached

## Authentication & Identity

**Auth Provider:**
- Supabase Auth (managed authentication service)
  - Implementation: OAuth2 + email/password flows
  - Signup enabled: Yes (email confirmation optional)
  - Social providers: Configurable in `supabase/config.toml` (Apple, Google, GitHub, etc. - currently disabled)

**Client Implementation:**
- Browser client: `apps/web/src/lib/supabase/client.ts`
  - Uses `createBrowserClient` from `@supabase/ssr`
  - Constructor: `NEXT_PUBLIC_SUPABASE_URL` + `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY`
- Server client: `apps/web/src/lib/supabase/server.ts`
  - Uses `createServerClient` from `@supabase/ssr`
  - Handles cookie-based session management
  - Constructor: `NEXT_PUBLIC_SUPABASE_URL` + `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY`
- Middleware: `apps/web/src/lib/supabase/middleware.ts`
  - Session refresh utility for Next.js middleware

**Auth Routes:**
- `/api/auth/callback` - OAuth and email confirmation handler
  - File: `apps/web/src/app/api/auth/callback/route.ts`
  - Exchanges authorization code for session
  - Redirects to `/calendar` on success, `/login?error=auth_callback_error` on failure
- `/login` - Email/password login page
  - File: `apps/web/src/app/(auth)/login/page.tsx`
  - Uses Supabase email/password auth
- `/signup` - Email registration with confirmation
  - File: `apps/web/src/app/(auth)/signup/page.tsx`
  - Email confirmation flow via Inbucket (local) or SendGrid SMTP (production)

**Session Management:**
- JWT tokens stored in secure httpOnly cookies
- Token expiry: 3600 seconds (1 hour)
- Refresh token rotation: Enabled
- Reuse interval: 10 seconds (allows rapid refreshes)

## Monitoring & Observability

**Error Tracking:**
- Not detected

**Logs:**
- Console logging (default - no structured logging library)
- Supabase Analytics available but not configured
  - Port: 54327 (local)
  - Backend: PostgreSQL analytics engine

**Development Utilities:**
- Supabase Studio - Web UI for database inspection
  - Local: `http://127.0.0.1:54323`
- Inbucket - Email testing interface
  - Local: `http://127.0.0.1:54324`
  - Tests email sending without actually sending

## CI/CD & Deployment

**Hosting:**
- Vercel - Next.js platform
  - Config: `apps/web/vercel.json`
  - Auto-deploys from `master` branch
  - Environment variables set via Vercel Dashboard

**CI Pipeline:**
- Not detected (no GitHub Actions, no CI config in `.github/workflows/`)
- Turborepo has lint and typecheck tasks configured in `turbo.json`

**Build Process:**
```bash
npm run build        # Turbo builds all apps
npm run lint         # Turbo lints all apps
npm run typecheck    # Turbo typechecks all apps
```

**Database Migrations:**
- Supabase CLI managed:
  ```bash
  npx supabase link --project-ref YOUR_PROJECT_REF
  npx supabase db push                          # Apply migrations
  npx supabase db reset                         # Reset and seed
  ```

## Environment Configuration

**Required Environment Variables (apps/web/.env.local):**
- `NEXT_PUBLIC_SUPABASE_URL` - Supabase project URL (e.g., `https://your-project.supabase.co`)
- `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY` - Publishable key with `sb_publishable_` prefix

**Optional Environment Variables (for future phases):**
- `SUPABASE_SECRET_KEY` - Service role key for server-side admin operations (bypass RLS)
- `STRIPE_SECRET_KEY` - Stripe payment processing (Phase 2)
- `STRIPE_WEBHOOK_SECRET` - Stripe webhook verification
- `TOSS_SECRET_KEY` - Toss Payments (Korean payment gateway, Phase 2)
- `TOSS_CLIENT_KEY` - Toss Payments client key
- `SLACK_WEBHOOK_URL` - Slack notifications (Phase 2)
- `KAKAO_ALIMTALK_KEY` - Kakao AlimTalk messaging (Phase 2)
- `KAKAO_ALIMTALK_SENDER` - Kakao AlimTalk sender ID
- `COUPANG_ACCESS_KEY` - Coupang API integration (Phase 3)
- `COUPANG_SECRET_KEY` - Coupang API secret
- `NAVER_CLIENT_ID` - Naver API credentials (Phase 3)
- `NAVER_CLIENT_SECRET` - Naver API secret

**Secrets Location:**
- Development: `.env.local` (git-ignored, never committed)
- Production: Vercel Environment Variables (set via Vercel Dashboard)

## Webhooks & Callbacks

**Incoming:**
- OAuth redirect callback: `/api/auth/callback`
  - Handles Google OAuth, GitHub OAuth, etc. (configurable providers)
  - Verifies authorization code with Supabase Auth
- Email confirmation callback: `/api/auth/callback`
  - Handles email verification tokens from Supabase Auth

**Outgoing:**
- Stripe webhooks (stub): `/api/webhooks/stripe`
  - File: `apps/web/src/app/api/webhooks/stripe/route.ts`
  - Status: Placeholder - expects `stripe-signature` header
  - Purpose: Payment events (Phase 2)
- Slack webhooks (planned): Notification integration
  - Configuration: `SLACK_WEBHOOK_URL` environment variable
  - Status: Not implemented

## Multi-Tenant Data Isolation

**Row Level Security (RLS):**
- All tables with user/team data have RLS policies enabled
- Every table includes `team_id` column for scoping
- Policies use `auth.uid()` to verify user team membership
- Service role key (if used) can bypass RLS - restricted to server-side only

**Team-Based Access:**
- Users belong to teams via `team_members` table
- All queries must include `team_id` from authenticated session
- No cross-team data visibility at database level

## Integration Status Summary

| Service | Status | Phase | Implementation |
|---------|--------|-------|-----------------|
| Supabase Auth | Active | 1 | `@supabase/ssr` clients, middleware |
| Supabase Database | Active | 1 | PostgreSQL via `@supabase/supabase-js` |
| Supabase Storage | Schema Only | 2-3 | Configured, not yet used |
| Supabase Realtime | Available | 2+ | Configured, not yet used |
| Vercel | Active | 1 | Deployment platform |
| Stripe | Stub Only | 2 | `/api/webhooks/stripe` placeholder |
| Toss Payments | Not Started | 2 | Environment variable ready |
| Slack | Not Started | 2 | Environment variable ready |
| Kakao AlimTalk | Not Started | 2 | Environment variable ready |
| E-commerce APIs | Not Started | 3 | Channels schema ready |

---

*Integration audit: 2026-02-17*
