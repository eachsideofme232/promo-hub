# Roadmap: PromoHub -- Trade Promotion Manager

## Overview

PromoHub replaces Excel spreadsheets for K-beauty brand managers by delivering a calendar-first promotion management platform with full P&L analysis. The roadmap progresses from foundation (auth, multi-tenant, Korean locale) through the core calendar experience, then layers in the P&L engine and ROI analysis that differentiate PromoHub from spreadsheets. Eight phases deliver all 30 v1 requirements, with each phase producing a coherent, verifiable capability.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Foundation** - Auth, multi-tenant isolation, Korean locale, and channel setup ✓ 2026-02-18
- [ ] **Phase 2: Products & Channels** - Product/SKU management with COGS and channel-specific pricing
- [ ] **Phase 3: Calendar Views** - Month/week/day calendar with filtering and Korean retail events
- [ ] **Phase 4: Promotion CRUD & Lifecycle** - Create, edit, delete promotions with full status tracking
- [ ] **Phase 5: Templates & Conflict Detection** - Reusable promotion templates and overlap warnings
- [ ] **Phase 6: P&L Engine** - Per-promotion financial entry and Simon-Kucher calculation engine
- [ ] **Phase 7: ROI Analysis & Visualization** - ROI/uplift calculations and 2x2 quadrant matrix
- [ ] **Phase 8: Team Management & Export** - Team invitations, role-based permissions, data export

## Phase Details

### Phase 1: Foundation
**Goal**: Users can securely access PromoHub with team-scoped data isolation and a Korean-native interface
**Depends on**: Nothing (first phase)
**Requirements**: TEAM-01, TEAM-02, LOC-01, LOC-02, PROD-03
**Success Criteria** (what must be TRUE):
  1. User can sign up and log in with email/password and reach the dashboard
  2. User data is completely isolated -- one team cannot see another team's data (RLS enforced)
  3. UI displays Korean dates (YYYY-MM-DD), Korean Won currency (1,000 / 1만 / 1억), and KST timezone throughout
  4. Pre-seeded Korean e-commerce channels (OliveYoung, Coupang, Naver, Kakao, Musinsa) appear in the system with Korean names and channel-specific promo types
  5. User can add custom channels beyond the pre-seeded Korean ones
**Plans**: 3 plans

Plans:
- [ ] 01-01-PLAN.md — Database migrations (auto-team trigger, channel schema extension) + next-intl Korean localization + TeamProvider context
- [ ] 01-02-PLAN.md — Channel API routes (CRUD with auth/validation) + channel management page UI
- [ ] 01-03-PLAN.md — Gap closure: Wire Korean Won currency formatting into Phase 1 UI + fix ChannelForm anti-pattern

### Phase 2: Products & Channels
**Goal**: Users can manage their product catalog with pricing data needed for promotion planning and P&L analysis
**Depends on**: Phase 1
**Requirements**: PROD-01, PROD-02
**Success Criteria** (what must be TRUE):
  1. User can create/edit/delete products with SKU codes, COGS, and retail price
  2. User can set different pricing per channel for the same product (e.g., OliveYoung price vs Coupang price)
  3. Product data persists across sessions and is scoped to the user's team
**Plans**: TBD

Plans:
- [ ] 02-01: TBD

### Phase 3: Calendar Views
**Goal**: Users can visually see all their promotions across channels on a calendar and find what they need through filtering
**Depends on**: Phase 1
**Requirements**: PLAN-01, PLAN-02, PLAN-03, PLAN-06, PLAN-07, PLAN-11
**Success Criteria** (what must be TRUE):
  1. User can view promotions on a monthly calendar with channel color coding (distinct colors per channel)
  2. User can switch between monthly, weekly, and daily calendar views
  3. User can view promotions in a filterable/sortable list view as an alternative to the calendar
  4. User can filter promotions by channel, status, date range, and product -- and filters apply across both calendar and list views
  5. User can see Korean retail calendar events overlaid on the calendar (Chuseok, Lunar New Year, OliveYoung BigBang, etc.)
**Plans**: TBD

Plans:
- [ ] 03-01: TBD
- [ ] 03-02: TBD

### Phase 4: Promotion CRUD & Lifecycle
**Goal**: Users can create and manage promotions with all required business data and track them through their lifecycle
**Depends on**: Phase 2, Phase 3
**Requirements**: PLAN-04, PLAN-05, PLAN-08
**Success Criteria** (what must be TRUE):
  1. User can create a promotion with title, channel, products, discount type (percentage/BOGO/coupon/gift/bundle), date range, status, and memo
  2. User can edit any field of an existing promotion and delete promotions they created
  3. User can move a promotion through its lifecycle: draft -> planned -> active -> ended/cancelled, and the status is visually reflected on the calendar and list views
**Plans**: TBD

Plans:
- [ ] 04-01: TBD
- [ ] 04-02: TBD

### Phase 5: Templates & Conflict Detection
**Goal**: Users can reuse recurring promotion patterns and get warned about scheduling conflicts
**Depends on**: Phase 4
**Requirements**: PLAN-09, PLAN-10, PROD-04
**Success Criteria** (what must be TRUE):
  1. User can save any promotion as a reusable template
  2. User can create a new promotion from a template with adjusted dates (other fields pre-filled from template)
  3. User receives a visual warning when creating or editing a promotion that overlaps with another promotion on the same product across channels
**Plans**: TBD

Plans:
- [ ] 05-01: TBD

### Phase 6: P&L Engine
**Goal**: Users can enter full financial data per promotion and the system calculates profitability using the Simon-Kucher price waterfall methodology
**Depends on**: Phase 4
**Requirements**: FIN-01, FIN-02, FIN-03, FIN-04, FIN-08
**Success Criteria** (what must be TRUE):
  1. User can enter full P&L data for a promotion: revenue, COGS, discount cost, channel subsidy, stock-up cost, and cannibalization cost
  2. System automatically calculates net profit and margin per promotion using the price waterfall methodology (no manual calculation needed)
  3. User can enter baseline volume from historical non-promo period averages with a methodology label (manual estimate / 4-week avg / YoY)
  4. System calculates incremental volume (actual minus baseline) and displays it alongside the P&L
  5. All financial calculations use decimal precision -- no floating-point rounding errors for KRW amounts
**Plans**: TBD

Plans:
- [ ] 06-01: TBD
- [ ] 06-02: TBD

### Phase 7: ROI Analysis & Visualization
**Goal**: Users can evaluate promotion effectiveness using ROI and uplift metrics and visually classify promotions into strategic quadrants
**Depends on**: Phase 6
**Requirements**: FIN-05, FIN-06, FIN-07
**Success Criteria** (what must be TRUE):
  1. System calculates ROI (net profit impact / promotion investment) for each promotion with P&L data entered
  2. System calculates volume uplift percentage vs baseline for each promotion
  3. User can view an ROI vs Uplift 2x2 matrix that classifies promotions into four quadrants: Star, Efficient Niche, Volume Trap, and Value Destroyer -- with Korean labels
  4. User can identify at a glance which promotions to repeat and which to kill based on quadrant placement
**Plans**: TBD

Plans:
- [ ] 07-01: TBD

### Phase 8: Team Management & Export
**Goal**: Users can collaborate with their team through invitations and role-based access, and export data for external reporting
**Depends on**: Phase 4
**Requirements**: TEAM-03, TEAM-04, TEAM-05
**Success Criteria** (what must be TRUE):
  1. User can invite team members by email with an assigned role (owner, admin, member, viewer)
  2. Permissions enforce what each role can do -- viewers cannot create/edit/delete, members cannot manage team settings, only owners/admins can invite
  3. User can export promotions and P&L data to CSV or Excel for external reporting and management presentations
**Plans**: TBD

Plans:
- [ ] 08-01: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8

Note: Phases 2 and 3 both depend only on Phase 1 and could execute in parallel. Phase 4 depends on both 2 and 3. Phase 8 depends on Phase 4 and could execute in parallel with Phases 5-7.

| Phase | Plans Complete | Status | Completed |
|-------|---------------|--------|-----------|
| 1. Foundation | 3/3 | ✓ Complete | 2026-02-18 |
| 2. Products & Channels | 0/1 | Not started | - |
| 3. Calendar Views | 0/2 | Not started | - |
| 4. Promotion CRUD & Lifecycle | 0/2 | Not started | - |
| 5. Templates & Conflict Detection | 0/1 | Not started | - |
| 6. P&L Engine | 0/2 | Not started | - |
| 7. ROI Analysis & Visualization | 0/1 | Not started | - |
| 8. Team Management & Export | 0/1 | Not started | - |
