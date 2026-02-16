# Project Research Summary

**Project:** PromoHub - Trade Promotion Management SaaS for K-Beauty
**Domain:** B2B SaaS, Trade Promotion Management, E-commerce Analytics
**Researched:** 2026-02-17
**Confidence:** HIGH

## Executive Summary

PromoHub is a Trade Promotion Management (TPM) platform designed specifically for small-medium K-beauty and cosmetics companies managing promotions across Korean e-commerce channels (OliveYoung, Coupang, Naver, Kakao, Musinsa). The target users are brand managers and e-commerce teams at 5-50 person companies who currently manage promotions in Excel spreadsheets with no standardized P&L analysis or ROI tracking. Research shows TPM is a mature enterprise software category with established best practices (Simon-Kucher P&L methodology, price waterfall models), but no Korean-market-native solution exists for SMBs at an accessible price point.

The recommended approach is to build a calendar-first promotion management platform that progressively enhances from basic CRUD to sophisticated P&L analysis. Start with replacing the Excel spreadsheet (Phase 1: calendar + promotion CRUD + conflict detection), then add the killer differentiator (Phase 2: per-promotion P&L calculator with Simon-Kucher methodology), and finally scale to analytics and automation (Phase 3+). The existing codebase already has strong foundations: Turborepo monorepo structure, Supabase Auth implemented, core UI components built, RLS-protected database schema with proper UUID defaults. Approximately 55% of Phase 1 is complete but needs API integration to replace demo data.

Key risks are **premature complexity** (building AI/forecasting before data exists), **wrong financial model** (missing the price waterfall foundation that makes P&L accurate), and **channel abstraction** (treating all Korean channels the same when each has unique mechanics). These are mitigated by: deferring AI to Phase 3+, implementing the full price waterfall schema from Phase 1 even if fields are nullable initially, and using JSONB channel-specific configs from the start.

## Key Findings

### Recommended Stack

PromoHub's existing stack is fundamentally sound and aligned with industry best practices for 2026. The codebase uses Next.js 14.2, React 18, Tailwind CSS v3, Supabase, and Turborepo. Research recommends upgrading to Next.js 16 (React 19 required, Turbopack default), Tailwind CSS v4 (5x faster builds, CSS-first config), and adding critical missing pieces: TanStack Query for server state, react-hook-form for complex forms, next-intl for Korean/English i18n, and decimal.js for financial calculations.

**Core technologies with high confidence:**
- **Next.js 16 + React 19:** App Router is production-proven; Turbopack file system caching delivers major dev performance improvements; Server Components reduce JS sent to client (critical for data-heavy TPM dashboards)
- **Supabase (PostgreSQL + Auth + RLS):** All-in-one BaaS eliminates separate auth/db setup; RLS provides multi-tenant isolation at database level (non-negotiable for B2B SaaS with competitive pricing data); Realtime enables live calendar collaboration
- **Tailwind CSS v4:** Already in codebase as v3; v4 upgrade delivers 5x faster builds and CSS-first config; fully compatible with shadcn/ui
- **TanStack Query v5 (NEW):** Replaces manual fetch + useState patterns; critical for multi-user promotion editing with optimistic updates and cache invalidation
- **decimal.js (NEW):** JavaScript floating-point math is unsuitable for financial calculations (0.1 + 0.2 !== 0.3); TPM requires precise KRW calculations for discount amounts, COGS, P&L rollups
- **next-intl v4 (NEW):** Korean-first UI with ICU message format for Korean Won formatting (1,000원, 1만원, 1억원) and date formatting (YYYY년 MM월 DD일)

**Migration considerations:** Tailwind v3 → v4 requires running `npx @tailwindcss/upgrade`. Zod should stay on v3 (v4 exists but ecosystem compatibility is new). FullCalendar is recommended over the custom calendar implementation for drag-drop scheduling and multi-channel timeline views (saves 2-3 weeks of dev time).

### Expected Features

Research identified 12 table stakes features, 11 competitive differentiators, and 8 anti-features to avoid.

**Must have (table stakes) — users expect these:**
- **Promotion Calendar** (month/week/day views): Primary UI; brand managers think in calendars; must support drag-drop, color-coded by channel, filterable
- **Promotion CRUD:** Core data entry with fields for title, channel, products, discount type (percentage/BOGO/coupon/gift/bundle), dates, status, memo
- **Channel Management:** Pre-seeded Korean channels (OliveYoung, Coupang, Naver, Kakao, Musinsa) with distinct promo mechanics per channel
- **Product/SKU Management:** Promotions tied to products; P&L requires product COGS data
- **Multi-Channel Conflict Detection:** Alert when same product has overlapping promotions across channels (erodes margins)
- **Team Collaboration & RBAC:** Multi-tenant B2B SaaS requires team-scoped data and role-based permissions (owner/admin/member/viewer)
- **Korean Language Support:** Full Korean UI (dates, currency, timezone KST); English-only is a dealbreaker for target market
- **Data Export (CSV/Excel):** Required for reporting to management in Korean corporate culture

**Should have (competitive differentiators) — these justify paid tier:**
- **Per-Promotion P&L Calculator:** The killer feature. Full Simon-Kucher methodology: revenue, COGS, discount cost, channel subsidies, stock-up cost, cannibalization cost, net profit. No Excel template does this well. Brand managers currently spend hours on one-off spreadsheets.
- **ROI/Uplift Analysis (2x2 Matrix):** Answers "was this promotion worth it?" — classifies promotions into quadrants (Star, Volume Trap, Niche Win, Value Destroyer) with action recommendations. Most K-beauty SMBs cannot calculate this today.
- **Historical Promotion Library:** Searchable archive of all past promotions with P&L outcomes; answers "What did we run on OliveYoung last September?" Currently buried in email chains.
- **Promotion Templates:** OliveYoung BigBang happens 4x/year; templates eliminate re-entry. Pre-built templates for known Korean channel events.
- **Channel-Specific Promotion Types:** OliveYoung (BigBang, OliveDay 25-27th monthly), Coupang (Gold Box, Time Sale), Musinsa (seasonal sales). Generic TPM tools don't model these — this is domain knowledge moat.
- **Baseline Volume Estimation:** Foundation for ROI/uplift math. Users enter baseline (regular sales without promotion); system suggests from historical data over time.

**Defer (anti-features — v2+ or never):**
- **Real-Time Channel API Integration:** Each Korean channel has different (or no) public API; integration maintenance cost is enormous; blocks launch on external dependencies. Solution: manual entry first, CSV import second, APIs as Phase 3+ when revenue justifies cost.
- **AI-Powered Demand Forecasting:** Requires 2+ years of historical data; K-beauty SMBs starting fresh have no data; massive engineering cost for questionable accuracy. Solution: simple baseline estimation first, accumulate 12+ months data before considering AI.
- **Full ERP/Accounting Integration:** K-beauty SMBs (5-50 people) rarely use ERP; those that do use Korean systems (Douzone, Wehago) with poor API support. Solution: CSV/Excel export that accountants can import.
- **Real-Time Collaborative Editing:** Massive technical complexity (CRDTs, WebSockets); promotions are structured records with approval flows, not documents. Solution: optimistic locking with change history.

### Architecture Approach

The research confirms the existing Turborepo monorepo structure is appropriate. The recommended architecture follows a three-layer pattern: Presentation (calendar, P&L worksheet, analytics dashboards) → Application (promotion service, P&L engine, reporting service) → Data (Supabase with RLS-enforced multi-tenancy). The P&L engine should be implemented as **pure TypeScript functions** in `lib/pnl/` that run client-side for instant recalculation, not as API-only server logic.

**Major components and responsibilities:**
1. **Promotion Calendar UI:** Visual scheduling with drag-drop, channel-colored cards, conflict overlay. Communicates with Promo Service + Channel Service. Status: UI done, needs API connection.
2. **P&L Engine (Pure Calculation Module):** Implements Simon-Kucher methodology as pure functions: 5 volume effects (baseline, forward-buying, cannibalization, competitor, category incremental) + 3 hidden costs (subsidy, stock-up, cannibalization) + direct costs → ROI, Uplift, Quadrant classification. Lives in `lib/pnl/`, used by both UI (instant feedback) and API (validation). Status: Not built yet.
3. **ROI/Uplift Evaluation Matrix:** 2x2 quadrant classifier (Star/Volume Trap/Niche Win/Value Destroyer) with Korean labels and action recommendations. Status: Schema supports it, logic not implemented.
4. **Team-Scoped Data via RLS:** Every query automatically filtered by authenticated user's team membership through PostgreSQL RLS. Never manually filter by team_id in application code. Status: RLS policies complete and correct in existing migrations.
5. **Analytics Aggregation (Phase 2):** Aggregate pre-computed P&L results from `promo_pnl` table (not recalculating on the fly). Scatter plot dashboard, waterfall summaries, channel comparisons. Status: Deferred to Phase 2.

**Key architectural patterns:**
- **P&L as pure functions:** Client-side calculation for instant feedback; same logic server-side for validation. No database calls in calculation engine.
- **Planned vs. Actual P&L:** Store both pre-event plan and post-event actual financials (schema has `is_plan` boolean). Critical for post-event analysis.
- **JSONB for channel-specific data:** Each Korean channel has unique fee structures and promo types; use JSONB `channel_config` and `channel_details` columns for flexibility without rigid channel tables.

### Critical Pitfalls

Research identified 6 critical pitfalls that have high impact and occur frequently in TPM implementations:

1. **Building P&L Without Price Waterfall Foundation:** Most failed TPM tools model P&L as `revenue - discount = margin`, missing 5-8 deduction layers (retailer fees, slotting fees, marketing allowances, logistics). 60% of trade promotions fail to break even industry-wide; bad P&L models hide this. **Prevention:** Design schema around Simon-Kucher price waterfall from Phase 1 (list_price, on_invoice_discount, invoice_price, retailer_fee, marketing_allowance, logistics_cost, pocket_price, COGS, pocket_margin). Even if fields are nullable initially, the structure must exist.

2. **Wrong Baseline = Wrong ROI = Wrong Decisions:** ROI is `(promoted_sales - regular_sales) / promo_cost`, but "regular_sales" baseline is set incorrectly (naive 4-week average ignoring seasonality). Result: ROI overstated by 30-70%; teams run unprofitable promotions believing they work. **Prevention:** Require users to input baseline explicitly with methodology label (manual estimate / 4-week avg / YoY). Phase 2: implement year-over-year baseline suggestion. Store baseline_methodology as metadata for audit.

3. **Ignoring Post-Promotion Effects:** Measuring lift during promo only, ignoring post-promo dip (consumers deplete stockpiled inventory), cannibalization, and forward buying. ROI overstated by 40-70%. **Prevention:** Phase 1 schema includes `post_promotion_review` fields. Phase 2 UI workflow prompts for post-promo actuals 4 weeks after promotion ends. Distinguish "Gross Lift" vs. "Net Incremental."

4. **Channel-Agnostic Data Model:** Treating OliveYoung, Coupang, Naver as interchangeable "channels" when each has fundamentally different promotion mechanics, fee structures, settlement timelines. **Prevention:** JSONB `channel_details` column from Phase 1. Pre-populate channel-specific promotion types and fee structures for 5 Korean channels.

5. **Calendar Without Conflict Intelligence:** Calendar displays events but doesn't detect conflicts (same product, different prices across channels; overlapping promos cannibalizing each other). **Prevention:** Phase 1 implements basic same-product date overlap detection as warnings (not blockers). Phase 2 adds cross-channel price conflict detection.

6. **Multi-Tenant Data Leakage Through RLS Gaps:** New tables default to NO RLS in Supabase; missing RLS policies or policies checking `user_id` instead of `team_id` allow data leaks. One leak in pricing strategy data = catastrophic loss of customer trust. **Prevention:** Every migration template includes `ENABLE ROW LEVEL SECURITY` and default-deny policy. Store `team_id` as JWT custom claim. CI script verifies all tables have RLS. Never use service_role key in user-facing APIs.

## Implications for Roadmap

Based on research findings, the recommended phase structure prioritizes replacing Excel first, then layering sophisticated P&L analysis, then analytics:

### Phase 1A: Calendar + CRUD Foundation (Replace Excel)
**Rationale:** The existing codebase is 55% complete for Phase 1A. Calendar UI, promotion forms, filters, and layout components are built but use demo data. This phase connects them to real APIs and makes the product minimally viable as an Excel replacement.

**Delivers:**
- Working promotion calendar (month/week/day views) with real data from Supabase
- Promotion CRUD with channel selection, product linking, status tracking
- Channel filtering (fetch channels from DB, not hardcoded)
- Basic conflict detection (same product, overlapping dates)
- Products page for COGS/pricing management
- Team management basics (invite, roles)
- Korean language UI (already in progress)
- Data export to CSV/Excel

**Addresses features:** T1 Promotion Calendar, T2 Promotion CRUD, T3 Channel Management, T4 Product/SKU Management, T5 Conflict Detection, T8 Status Tracking, T9 List View + Filters, T11 Korean Language, T12 Authentication (done)

**Avoids pitfalls:** RLS gaps (already implemented correctly), channel-agnostic model (add JSONB channel_details now), calendar without conflicts (basic detection)

**Technical work:**
- Replace `DEMO_PROMOTIONS` with API calls using TanStack Query
- Implement `/api/promotions`, `/api/calendar`, `/api/products`, `/api/channels` routes
- Connect FilterProvider to real channel data
- Build Products CRUD page
- Add Korean calendar events overlay (OliveYoung BigBang, Chuseok, etc.)
- Implement promotion templates (duplicate feature minimum)

**Stack additions:** TanStack Query, react-hook-form, next-intl

**Duration estimate:** 2-3 weeks (most UI already built)

**Research flag:** NO — standard CRUD patterns, well-documented

---

### Phase 1B: P&L Engine (The Differentiator)
**Rationale:** This is the killer feature that justifies paid tier and differentiates from Excel. Research shows Simon-Kucher P&L methodology is well-documented and can be implemented as pure TypeScript functions. Building this immediately after Phase 1A validates product-market fit: do users actually enter P&L data?

**Delivers:**
- Per-promotion P&L worksheet UI with volume decomposition (5 effects), cost breakdown, waterfall visualization
- P&L calculation engine implementing Simon-Kucher methodology
- ROI and Uplift calculations with quadrant classification (Star/Volume Trap/Niche Win/Value Destroyer)
- Planned vs. Actual P&L (pre-event estimates, post-event actuals)
- Baseline volume estimation fields
- P&L results displayed on promotion detail view

**Addresses features:** D1 Per-Promotion P&L, D6 Baseline Volume, D2 ROI/Uplift Analysis (partial — calculation logic, not dashboard yet)

**Avoids pitfalls:** Price waterfall foundation (schema has all waterfall columns), wrong baseline (explicit methodology field), planned vs. actual gap (schema supports both)

**Technical work:**
- Create `promo_pnl` table migration with full price waterfall schema
- Implement `lib/pnl/calculator.ts` with Simon-Kucher formulas
- Build P&L worksheet UI components (`VolumeDecomposition`, `CostBreakdown`, `PnlWaterfall`, `RoiResult`, `QuadrantBadge`)
- Create `/api/promotions/[id]/pnl` routes (GET, POST, PATCH)
- Add quadrant badge to promotion cards on calendar
- Korean/English labels for quadrants

**Stack additions:** decimal.js (financial math), Recharts v3 (P&L waterfall chart)

**Duration estimate:** 2 weeks (calculation logic is complex but well-specified)

**Research flag:** MEDIUM — Simon-Kucher methodology is documented, but translating to Korean business context needs validation with target users during implementation

---

### Phase 2A: Post-Event Analysis Workflow
**Rationale:** P&L calculation alone doesn't close the loop. Brand managers need a structured process to enter actual results after promotions end, compare to plan, and feed results into historical library. This completes the "plan → execute → analyze → learn" cycle.

**Delivers:**
- Post-promotion review workflow (notification when promo ends, form for actual results)
- Planned vs. Actual comparison view (side-by-side waterfall charts)
- Post-promotion sales tracking (4-8 weeks after promo to capture decay/stock-up effects)
- Actual ROI/Uplift with quadrant re-classification
- Results auto-feed into historical promotion library

**Addresses features:** D7 Post-Event Analysis, D3 Historical Library (enhanced)

**Avoids pitfalls:** Ignoring post-promotion effects (post-promo review captures these), missing post-promo tracking

**Technical work:**
- `post_promotion_reviews` table (or extend `promo_pnl` with post-promo fields)
- Notification system (Supabase Edge Function cron job checks for ended promotions)
- Post-event analysis UI with actuals form
- Comparison view: planned waterfall vs. actual waterfall
- Historical library search/filter enhancements

**Stack additions:** Potentially Supabase Edge Functions for notifications (or defer to manual workflow)

**Duration estimate:** 1.5 weeks

**Research flag:** LOW — workflow design, not technical complexity

---

### Phase 2B: Analytics Dashboards
**Rationale:** Once users have 10+ promotions with P&L data entered (Phase 1B + 2A), build analytics to aggregate insights. Building dashboards before data exists teaches nothing about real UX needs.

**Delivers:**
- ROI/Uplift scatter plot dashboard (each promotion as a dot, quadrants color-coded)
- Aggregated P&L waterfall (total across all promotions for a period)
- Channel performance comparison (ROI by channel bar chart)
- Trend analysis (performance over time line chart)
- Quadrant distribution (% of promotions in each quadrant)
- Role-aware dashboards (brand manager view vs. finance view vs. executive view)

**Addresses features:** D2 ROI/Uplift Analysis (full dashboard), D8 Cross-Functional Dashboard

**Avoids pitfalls:** Building analytics before P&L data exists (deferred until Phase 2B)

**Technical work:**
- `/api/analytics` aggregation queries (SUM/AVG ROI, quadrant counts, waterfall totals)
- Scatter plot component (Recharts)
- Aggregated waterfall component
- Channel comparison charts
- Period-over-period filters (YoY, MoM)
- Export analytics to PDF/Excel

**Stack additions:** Already have Recharts; may add @tanstack/react-table for analytics data tables

**Duration estimate:** 2 weeks

**Research flag:** LOW — standard dashboard patterns

---

### Phase 3: Automation & Scale
**Rationale:** After product-market fit is established (Phases 1-2), add features that reduce manual work and support larger teams.

**Delivers:**
- Advanced promotion templates (with variable fields, not just duplication)
- Scenario simulation ("what if we do 30% off vs. BOGO?")
- Approval workflow (promotions >30% discount require manager approval)
- Bulk import/export (CSV upload for historical data migration)
- Advanced conflict detection (price parity across channels, inventory-aware scheduling)
- Realtime calendar collaboration (Supabase Realtime subscriptions, live updates)
- AI suggestions (deferred until 12+ months of data; suggest optimal discount depth based on historical ROI)

**Addresses features:** D4 Templates (advanced), D11 Scenario Simulation, D9 Approval Workflow, A2 AI Forecasting (mitigated — only after sufficient data)

**Duration estimate:** 3-4 weeks (multiple sub-features)

**Research flag:** HIGH for AI suggestions (need to research Korean-market demand forecasting models), LOW for others

---

### Phase Ordering Rationale

**Why Phase 1A before 1B:**
P&L is meaningless without promotions to calculate P&L for. Calendar + CRUD must work first. Phase 1A also delivers immediate value (Excel replacement) while Phase 1B adds the differentiator.

**Why Phase 1B before Phase 2:**
Post-event analysis and analytics both depend on having the P&L calculation engine working. Building dashboards before P&L data exists is premature. Phase 1B validates whether users actually enter P&L data (critical product risk).

**Why Phase 2A before 2B:**
Post-event analysis feeds data into analytics. Building trend dashboards before users have a workflow to enter actual results produces empty charts. The workflow comes first.

**Why Phase 3 deferred:**
Templates, scenarios, and approval workflows are "nice to have" that optimize an already-working system. They should not block launch. AI suggestions require 12+ months of data accumulation; building them in Phase 1-2 would be premature and deliver garbage outputs.

**Dependency chain validated by research:**
- Products (Phase 1A) → P&L (Phase 1B): P&L needs product COGS data
- P&L calculation (Phase 1B) → Post-event analysis (Phase 2A): Actual P&L uses same calculation engine as planned
- Post-event analysis (Phase 2A) → Analytics (Phase 2B): Dashboards aggregate actual results
- Historical library (Phase 2A) → Scenario simulation (Phase 3): Simulations use historical ROI data

### Research Flags

**Phases needing deeper research during planning:**
- **Phase 1B (P&L Engine):** MEDIUM — Simon-Kucher methodology is well-documented for global CPG, but validating field terminology and calculation assumptions with Korean K-beauty brand managers during implementation is recommended. Korean Won handling (no decimal places, 만/억 display) needs testing.
- **Phase 3 (AI Suggestions):** HIGH — If AI forecasting is added, will need research on demand forecasting models suitable for K-beauty seasonality (Chuseok, seasonal product cycles). Defer this research until Phase 3 kickoff.

**Phases with standard patterns (skip research-phase):**
- **Phase 1A (Calendar + CRUD):** Standard Next.js CRUD patterns, TanStack Query for data fetching, react-hook-form for complex forms. All well-documented.
- **Phase 2A (Post-Event Analysis):** Workflow design, not technical complexity. Standard form + comparison UI.
- **Phase 2B (Analytics Dashboards):** Standard aggregation queries + Recharts visualizations. Well-trodden path.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| **Stack** | HIGH | Next.js 16, React 19, Supabase, Tailwind v4 all have official docs and verified version compatibility. TanStack Query, react-hook-form, decimal.js are industry-standard choices for their respective purposes. |
| **Features** | MEDIUM-HIGH | Industry TPM features (calendar, P&L, ROI) are well-documented via Simon-Kucher, Salesforce, UpClear sources. K-beauty-specific features (channel mechanics, Korean calendar events) based on market knowledge + limited public competitor data. No direct Korean-market TPM competitor found for validation. |
| **Architecture** | HIGH | Simon-Kucher methodology for P&L is publicly documented with formulas. Supabase multi-tenant RLS patterns are official best practices. P&L-as-pure-functions pattern is validated by research and existing implementations. |
| **Pitfalls** | MEDIUM-HIGH | Domain pitfalls (wrong baseline, missing post-promo effects, price waterfall) are well-documented in CPG industry sources (CFO Pro Analytics, Simon-Kucher, Visualfabriq). Korean channel-specific pitfalls are based on market knowledge + inference. Limited TPM post-mortem case studies available. |

**Overall confidence:** HIGH

The core recommendation (calendar-first TPM with Simon-Kucher P&L methodology) is strongly supported by research. The stack choices are mainstream 2026 best practices with high confidence. The main uncertainty is Korean-market-specific validation (channel fee structures, brand manager workflows, terminology) which should be addressed through user testing during Phase 1-2 implementation, not as a blocker to starting.

### Gaps to Address

**Korean channel fee structures and promo mechanics:**
Research identified the general pattern (each channel has different mechanics) but did not find authoritative public sources for OliveYoung commission rates, Coupang Rocket Growth fee structures, Musinsa seller fees, or Naver Smart Store fee tiers. **How to handle:** Start with JSONB channel_config that users can customize. Pre-populate based on available public data (Coupang Global Sellers docs) and update based on beta user feedback. Plan to interview 2-3 K-beauty brand managers during Phase 1B for validation.

**Baseline calculation methodology for Korean seasonal products:**
Year-over-year baseline works for products with stable demand, but K-beauty has strong seasonal patterns (summer sunscreen, winter moisturizer) plus promotional calendars (Chuseok, Lunar New Year). Naive YoY may miss these. **How to handle:** Phase 1 uses manual baseline entry with guidance text. Phase 2 implements basic YoY. Defer advanced seasonal decomposition to Phase 3 when enough data exists to tune models. Document baseline methodology used per promotion for audit.

**Excel import/export format expectations:**
Research confirmed K-beauty brand managers "live in Excel" but did not find standardized promotion planning Excel templates used in the industry. **How to handle:** Build CSV export first (Phase 1A). Interview early users about their current Excel format. Build import to match their format in Phase 2/3 rather than forcing them to adapt.

**Settlement tracking integration:**
Pitfalls research noted that "actual P&L" is theoretical until channel payment is received, and settlement timelines vary by channel. This feature is not in current roadmap. **How to handle:** Phase 1-2 P&L is cash-based (assumes payment). Add `settlement_tracking` table in Phase 3 if users request it. Not a blocker for launch.

## Sources

### Primary (HIGH confidence)
- **Stack research:** Next.js 16.1 release blog, Tailwind CSS v4 announcement, Supabase SSR docs, npm package pages for version verification (all OFFICIAL sources)
- **Architecture research:** Simon-Kucher "How to best measure promotional effectiveness" (authoritative pricing consultancy), Supabase RLS docs (OFFICIAL), Salesforce Trailhead TPM module (enterprise vendor training)
- **Pitfalls research:** Simon-Kucher "Navigating pitfalls of product promotion" (authoritative), CFO Pro Analytics "How to build trade spend ROI model" (detailed methodology), Supabase RLS best practices (OFFICIAL)

### Secondary (MEDIUM confidence)
- **Features research:** 15 Best TPM Software 2026 (The Retail Exec), Aforza TPM Guide, Gartner Peer Insights TPM reviews, UpClear promotional ROI guide, CPGvision trade promotion KPIs
- **Stack research:** FullCalendar vs react-big-calendar comparison (third-party), decimal.js vs big.js comparison (npm-compare), Recharts vs Visx comparison (embeddable.com)
- **Korean market research:** Creatrip Olive Young sales schedule, Coupang Global Sellers documentation, MyKoreaPicks Korea shopping calendar

### Tertiary (LOW confidence)
- **Features research:** Business Research Insights TPM market data (CAGR claims — unverified), Trade Marketing Insider trends (vendor content)
- **Architecture research:** AntStack Supabase RLS multi-tenant article (community blog, not official)

**Research methodology:**
All four research files (STACK.md, FEATURES.md, ARCHITECTURE.md, PITFALLS.md) were synthesized. Confidence levels were assigned based on source authority (official docs > authoritative consultancy > vendor content > community blogs). Korean-market-specific findings have MEDIUM confidence due to sparse public TPM documentation for Korean e-commerce; these will be validated through user interviews during implementation.

---
*Research completed: 2026-02-17*
*Ready for roadmap: YES*
*Estimated total duration: Phase 1A (3 weeks) + Phase 1B (2 weeks) + Phase 2A (1.5 weeks) + Phase 2B (2 weeks) = 8.5 weeks to full Phase 2 completion, fitting within the 8-week Big 6 sprint with tight execution*
