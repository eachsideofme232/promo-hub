# Requirements: PromoHub -- Trade Promotion Manager

**Defined:** 2026-02-17
**Core Value:** Brand managers can see all promotions on a calendar, know exactly whether each promotion was profitable (full margin P&L), and make data-driven decisions about which promo mechanics to repeat or kill -- across all Korean e-commerce channels.

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### Promotion Planning

- [ ] **PLAN-01**: User can view promotions on a monthly calendar with channel color coding
- [ ] **PLAN-02**: User can view promotions on a weekly calendar
- [ ] **PLAN-03**: User can view promotions on a daily calendar
- [ ] **PLAN-04**: User can create a promotion with title, channel, products, discount type, dates, status, and memo
- [ ] **PLAN-05**: User can edit and delete their promotions
- [ ] **PLAN-06**: User can view promotions in a filterable/sortable list view
- [ ] **PLAN-07**: User can filter promotions by channel, status, date range, and product
- [ ] **PLAN-08**: User can track promotion status through lifecycle (draft -> planned -> active -> ended/cancelled)
- [ ] **PLAN-09**: User can save a promotion as a reusable template
- [ ] **PLAN-10**: User can create a promotion from a template with date adjustment
- [ ] **PLAN-11**: User can see Korean retail calendar events overlaid on the calendar (Chuseok, Lunar New Year, OY BigBang, etc.)

### Products & Channels

- [ ] **PROD-01**: User can manage products with SKU codes, COGS, and retail price
- [ ] **PROD-02**: User can set channel-specific pricing per product
- [ ] **PROD-03**: User can manage channels (pre-seeded Korean channels + custom)
- [ ] **PROD-04**: User receives visual warnings when promotions overlap on the same product across channels

### Financial Analysis

- [ ] **FIN-01**: User can enter full P&L per promotion (revenue, COGS, discount cost, channel subsidy, stock-up cost, cannibalization cost)
- [ ] **FIN-02**: System calculates net profit/margin per promotion using price waterfall methodology
- [ ] **FIN-03**: User can enter baseline volume from historical non-promo period averages
- [ ] **FIN-04**: System calculates incremental volume (actual - baseline)
- [ ] **FIN-05**: System calculates ROI (net profit impact / promotion investment)
- [ ] **FIN-06**: System calculates volume uplift percentage vs baseline
- [ ] **FIN-07**: User can view ROI vs Uplift 2x2 matrix visualization (Star / Efficient Niche / Volume Trap / Value Destroyer quadrants)
- [ ] **FIN-08**: All financial calculations use decimal precision (no floating-point errors for KRW)

### Team & Access

- [ ] **TEAM-01**: User can sign up and log in with email/password
- [ ] **TEAM-02**: User data is isolated per team (multi-tenant with RLS)
- [ ] **TEAM-03**: User can invite team members with assigned roles (owner, admin, member, viewer)
- [ ] **TEAM-04**: Permissions enforce what each role can do (create/edit/delete/view)
- [ ] **TEAM-05**: User can export promotions and P&L data to CSV/Excel

### Localization

- [ ] **LOC-01**: UI displays in Korean (dates, currency in KRW with won/man/eok, KST timezone)
- [ ] **LOC-02**: All Korean e-commerce channels pre-seeded with Korean names and promo types

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Post-Event Analysis

- **PEA-01**: User can enter actual sales results after a promotion ends
- **PEA-02**: System compares planned vs actual P&L with variance analysis
- **PEA-03**: System generates post-event analysis report

### Advanced Features

- **ADV-01**: User can search and browse historical promotion library with outcomes
- **ADV-02**: User can compare similar past promotions side-by-side
- **ADV-03**: User can simulate what-if scenarios (compare promo mechanics before committing)
- **ADV-04**: Cross-functional dashboards (brand, finance, executive views)
- **ADV-05**: Approval workflow with configurable discount/budget thresholds
- **ADV-06**: Channel-specific promotion type modeling (Coupang Gold Box, OY BigBang, etc.)

### Notifications & Integration

- **INT-01**: Slack/Kakao notifications for promotion status changes
- **INT-02**: Channel API integration for auto-pulling sales data

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| Real-time channel API integration | Each Korean channel has different/no public API; blocks launch on external dependencies |
| AI-powered demand forecasting | Requires 2+ years historical data; meaningless without accumulated data |
| Full ERP/accounting integration | K-beauty SMBs rarely use ERP; CSV export sufficient |
| Deduction management & claims | Different commercial model than US CPG; track as P&L line items only |
| In-store retail execution monitoring | E-commerce focused; offline is separate product vertical |
| Real-time collaborative editing | Massive CRDT complexity; optimistic locking sufficient |
| Competitor price monitoring | Requires scraping infrastructure; manual notes field instead |
| Multi-currency/multi-region | KRW only for v1; add when expanding globally |
| Mobile native app | Web-first, responsive design sufficient |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| PLAN-01 | Phase 3: Calendar Views | Pending |
| PLAN-02 | Phase 3: Calendar Views | Pending |
| PLAN-03 | Phase 3: Calendar Views | Pending |
| PLAN-04 | Phase 4: Promotion CRUD & Lifecycle | Pending |
| PLAN-05 | Phase 4: Promotion CRUD & Lifecycle | Pending |
| PLAN-06 | Phase 3: Calendar Views | Pending |
| PLAN-07 | Phase 3: Calendar Views | Pending |
| PLAN-08 | Phase 4: Promotion CRUD & Lifecycle | Pending |
| PLAN-09 | Phase 5: Templates & Conflict Detection | Pending |
| PLAN-10 | Phase 5: Templates & Conflict Detection | Pending |
| PLAN-11 | Phase 3: Calendar Views | Pending |
| PROD-01 | Phase 2: Products & Channels | Pending |
| PROD-02 | Phase 2: Products & Channels | Pending |
| PROD-03 | Phase 1: Foundation | Pending |
| PROD-04 | Phase 5: Templates & Conflict Detection | Pending |
| FIN-01 | Phase 6: P&L Engine | Pending |
| FIN-02 | Phase 6: P&L Engine | Pending |
| FIN-03 | Phase 6: P&L Engine | Pending |
| FIN-04 | Phase 6: P&L Engine | Pending |
| FIN-05 | Phase 7: ROI Analysis & Visualization | Pending |
| FIN-06 | Phase 7: ROI Analysis & Visualization | Pending |
| FIN-07 | Phase 7: ROI Analysis & Visualization | Pending |
| FIN-08 | Phase 6: P&L Engine | Pending |
| TEAM-01 | Phase 1: Foundation | Pending |
| TEAM-02 | Phase 1: Foundation | Pending |
| TEAM-03 | Phase 8: Team Management & Export | Pending |
| TEAM-04 | Phase 8: Team Management & Export | Pending |
| TEAM-05 | Phase 8: Team Management & Export | Pending |
| LOC-01 | Phase 1: Foundation | Pending |
| LOC-02 | Phase 1: Foundation | Pending |

**Coverage:**
- v1 requirements: 30 total
- Mapped to phases: 30
- Unmapped: 0

---
*Requirements defined: 2026-02-17*
*Last updated: 2026-02-17 after roadmap creation*
