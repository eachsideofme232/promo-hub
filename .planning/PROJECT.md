# PromoHub — Trade Promotion Manager

## What This Is

An all-in-one Trade Promotion Management (TPM) SaaS for K-beauty and cosmetic companies. It replaces Excel spreadsheets with a unified platform where cross-functional teams (brand, sales, finance) can plan promotions on a calendar, track full P&L per promotion, and analyze ROI and volume uplift using the Simon-Kucher methodology. Multi-tenant SaaS designed for multiple brands.

## Core Value

Brand managers can see all promotions on a calendar, know exactly whether each promotion was profitable (full margin P&L), and make data-driven decisions about which promo mechanics to repeat or kill — across all Korean e-commerce channels.

## Requirements

### Validated

<!-- Shipped and confirmed valuable. -->

(None yet — ship to validate)

### Active

<!-- Current scope. Building toward these. -->

- [ ] Promotion calendar with month/week/day views across all channels
- [ ] Promotion CRUD with channel, product/SKU, discount mechanics, date ranges
- [ ] Channel management (Oliveyoung, Coupang, Naver, Kakao, Musinsa, custom)
- [ ] Product/SKU management with COGS tracking
- [ ] Full P&L per promotion (revenue, COGS, discount cost, subsidy cost, stock-up cost, cannibalization cost, net margin)
- [ ] Manual data entry for sales results and promotion costs (auto-pull in future phase)
- [ ] Baseline volume calculation from historical non-promo period averages
- [ ] Incremental volume calculation (competitor volume + category volume)
- [ ] ROI calculation: net profit impact / promotion investment (Simon-Kucher methodology)
- [ ] Volume uplift measurement vs baseline
- [ ] ROI vs Uplift 2x2 matrix visualization (quadrant analysis)
- [ ] Historical promotion library with outcomes — track what works over time
- [ ] Cross-functional team access with role-based views (brand, sales, finance)
- [ ] Multi-tenant architecture for SaaS (team/company isolation)
- [ ] Authentication and authorization

### Out of Scope

<!-- Explicit boundaries. Includes reasoning to prevent re-adding. -->

- Auto-pull from channel APIs (Oliveyoung, Coupang, etc.) — future phase, start with manual entry
- AI-powered forecasting/prediction — future phase after historical data accumulates
- Competitor monitoring/scraping — separate concern, not core TPM
- Slack/Kakao notifications — polish feature, not v1
- Payment/billing system — monetization comes after product-market fit
- Mobile native app — web-first, responsive design sufficient for v1

## Context

- Building on an existing PromoHub codebase that has calendar UI, auth, and database schema — but user wants a **fresh start** with cleaner architecture
- The existing codebase (mapped in `.planning/codebase/`) provides reference patterns but will not be the starting point
- Target market: small-to-medium K-beauty/cosmetic companies managing promotions across Korean e-commerce channels
- Cross-functional users: brand managers (plan promos), sales team (input results), finance (review P&L)
- Simon-Kucher's promotional effectiveness framework is the analytical backbone:
  - 5 volume effects: baseline, forward buying, cannibalization, competitor volume, category incremental
  - 3 hidden costs: subsidy cost, stock-up cost, cannibalization cost
  - ROI = net profit impact / promotion investment
  - Uplift = incremental volume vs baseline
  - 2x2 matrix: ROI (y-axis) vs Uplift (x-axis) for quadrant analysis
- Korean market context: KRW currency, Korean date formats, Korean channel names
- All channels: Oliveyoung, Coupang, Naver, Kakao, Musinsa, plus custom channels

## Constraints

- **Timeline**: 8-week sprint (Big 6 project #1, deadline end of Feb 2026)
- **Tech stack**: Next.js + TypeScript + Supabase + Tailwind (proven stack from existing codebase)
- **Fresh start**: New codebase, not extending existing PromoHub code
- **Manual-first**: Data entry is manual for v1; channel API integrations deferred
- **Multi-tenant**: Must be SaaS-ready from day one (RLS, team scoping)
- **Korean market**: UI must support Korean language and KRW currency

## Key Decisions

<!-- Decisions that constrain future work. Add throughout project lifecycle. -->

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Fresh start over extending existing code | Cleaner architecture for TPM-specific data models | — Pending |
| Simon-Kucher ROI methodology | Industry-standard framework trusted by consulting firms | — Pending |
| Manual data entry first | Faster to ship; channel APIs are complex and channel-specific | — Pending |
| Multi-tenant from day one | Avoid painful migration later; SaaS is the business model | — Pending |

---
*Last updated: 2026-02-17 after initialization*
