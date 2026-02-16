# Feature Research

**Domain:** Trade Promotion Management SaaS for K-beauty / Cosmetics SMBs
**Researched:** 2026-02-17
**Confidence:** MEDIUM (industry TPM features: HIGH; K-beauty-specific gap analysis: MEDIUM; competitor differentiation for Korean market: LOW -- no direct Korean-market TPM competitor found)

## Feature Landscape

### Table Stakes (Users Expect These)

Features users assume exist. Missing these = product feels incomplete.

| # | Feature | Why Expected | Complexity | Notes |
|---|---------|--------------|------------|-------|
| T1 | **Promotion Calendar (Month/Week/Day)** | Every brand manager's primary mental model is the calendar; this is the anchor UI for all TPM tools | MEDIUM | Must support drag-and-drop, color-coded by channel, filterable. Oliveyoung BigBang (Mar/Jun/Sep/Dec), Coupang Gold Box, Musinsa seasonal sales all need visual representation |
| T2 | **Promotion CRUD (Create/Read/Update/Delete)** | Core data entry; without it, no promotions exist in the system | MEDIUM | Fields: title, channel, products, discount type (percentage/BOGO/coupon/gift/bundle), dates, status (planned/active/ended/cancelled), memo. Must validate date ranges |
| T3 | **Channel Management** | K-beauty brands sell across 5+ channels simultaneously (Oliveyoung, Coupang, Naver, Kakao, Musinsa); each has distinct promo mechanics | LOW | Pre-seeded Korean channels. Each channel has its own promo types (e.g., Coupang: Gold Box, Time Sale, instant/downloadable coupons; OY: BigBang Sale, OliveDay 25-27th monthly) |
| T4 | **Product/SKU Management** | Promotions are always tied to specific products; P&L cannot be calculated without product cost data (COGS) | MEDIUM | Products with SKU codes, COGS, retail price, channel-specific pricing. Promo-product N:M relationship |
| T5 | **Multi-Channel Conflict Detection** | Overlapping promotions on the same product across channels erode margins; brand managers manually cross-check today | MEDIUM | Alert when same product is on promotion across multiple channels in overlapping dates. Visual indicator on calendar. Configurable severity (warning vs. block) |
| T6 | **Team Collaboration & Sharing** | Brand, sales, and finance teams all touch promotions; Excel files get emailed around with version conflicts | LOW | Multi-user access to same promotion data. Team-scoped data (multi-tenant). Real-time visibility into who changed what |
| T7 | **Role-Based Access Control** | Different team members have different responsibilities; finance approves budgets, brand managers create promos, viewers just read | MEDIUM | Roles: owner, admin, member, viewer. Controls who can create/edit/delete/approve promotions. Required for any B2B SaaS |
| T8 | **Basic Promotion Status Tracking** | Brand managers need to know where each promotion is in its lifecycle | LOW | Status flow: draft -> planned -> active -> ended/cancelled. Status badges on calendar and list views. Filter by status |
| T9 | **Promotion List View with Filters** | Calendar is great for time-based view, but list view is needed for bulk operations, searching, sorting | LOW | Filterable by channel, status, date range, product. Sortable. Searchable by title/description |
| T10 | **Data Export (CSV/Excel)** | Brand managers must share data with external stakeholders (retailers, finance teams) who do not use the system | LOW | Export promotions to CSV/Excel. Filtered export. Required for reporting to management in Korean corporate culture |
| T11 | **Korean Language Support** | Target users are Korean brand managers; English-only UI is a dealbreaker | MEDIUM | Full Korean UI (dates: YYYY년 MM월 DD일, currency: 원/만/억, KST timezone). Not full i18n initially -- Korean-first, English optional |
| T12 | **Authentication & Security** | Multi-tenant B2B SaaS with financial data; must protect company data | MEDIUM | Email/password + social login. Session management. Row-Level Security for multi-tenant isolation. Already partially implemented via Supabase Auth |

### Differentiators (Competitive Advantage)

Features that set PromoHub apart. K-beauty brand managers currently use Excel; these are the reasons they would pay for a dedicated tool.

| # | Feature | Value Proposition | Complexity | Notes |
|---|---------|-------------------|------------|-------|
| D1 | **Per-Promotion P&L Calculator** | The killer feature. No Excel template does this well. Full P&L per promotion: revenue, COGS, discount cost, subsidy from channel, stock-up cost (forward buying), cannibalization cost, net profit. Brand managers currently spend hours building one-off spreadsheets | HIGH | Must model: gross sales, COGS, discount amount, channel fees/subsidies, forward buying impact, cannibalization across own products. Needs product COGS data (depends on T4). Simon-Kucher methodology: ROI = net profit impact / promotion investment |
| D2 | **ROI / Uplift Analysis (Simon-Kucher 2x2 Matrix)** | Answers "was this promotion worth it?" -- the question every brand manager and their CFO asks. Most K-beauty SMBs cannot calculate this today | HIGH | ROI = net profit impact / promotion investment. Uplift = incremental volume vs. baseline. 2x2 quadrant: (1) High ROI + High Uplift = Winners, (2) High ROI + Low Uplift = Efficient niche, (3) Low ROI + High Uplift = Volume drivers (margin destroyers), (4) Low ROI + Low Uplift = Losers. Requires baseline volume estimation and post-event actual data entry |
| D3 | **Historical Promotion Library with Search** | "What did we run on Oliveyoung last September?" -- currently buried in email chains and old Excel files. Searchable archive of all past promotions with their P&L outcomes enables institutional knowledge | MEDIUM | Every completed promotion becomes a searchable record. Filter by channel, product, date, discount type, ROI outcome. Compare similar past promotions side-by-side. Powerful for planning next year's calendar |
| D4 | **Promotion Templates (Recurring Patterns)** | Oliveyoung BigBang happens 4x/year; Coupang Gold Box is recurring; monthly OliveDay is the 25th-27th every month. Templates eliminate re-entry of the same promotion structure | MEDIUM | Save any promotion as a template. Pre-built templates for known Korean channel events (OY BigBang Mar/Jun/Sep/Dec, OY OliveDay monthly, Coupang seasonal). One-click instantiation with date adjustment |
| D5 | **Channel-Specific Promotion Type Modeling** | Each Korean channel has unique promo mechanics (Coupang: Gold Box 24hr, Time Sale 4hr, instant/downloadable coupons; OY: BigBang Sale, member kits; Musinsa: seasonal sales). No generic TPM tool models these | MEDIUM | Channel-specific promo type dropdowns and fields. e.g., selecting "Coupang" shows Gold Box, Time Sale, Free Exposure options. Selecting "Oliveyoung" shows BigBang, OliveDay, Brand Coupon options. This domain knowledge is a moat |
| D6 | **Baseline Volume Estimation** | Foundation for all ROI/uplift math. Users enter baseline (regular sales without promotion) per product per channel. System can suggest baselines from historical data over time | MEDIUM | Manual entry first (user inputs expected baseline units/revenue). Later: auto-suggest from historical non-promotion periods. Critical dependency for D1, D2 |
| D7 | **Post-Event Analysis (PEA) Workflow** | Structured process: after promotion ends, enter actual results, system calculates ROI/uplift, generates comparison to plan. Turns ad-hoc analysis into a repeatable process | HIGH | Actual vs. planned comparison. Auto-calculate: lift %, incremental sales, CID (cost per incremental dollar), trade rate %. Feed results back into historical library (D3). Notification when promotion ends to prompt PEA entry |
| D8 | **Cross-Functional Dashboard** | Different views for different roles: brand manager sees calendar + upcoming promos; finance sees spend summary + ROI trends; sales sees channel performance. One platform, multiple lenses | MEDIUM | Role-aware default views. Brand dashboard: calendar + next 2 weeks of promos. Finance dashboard: total trade spend, ROI distribution, budget utilization. Executive dashboard: channel comparison, top/bottom promos by ROI |
| D9 | **Approval Workflow** | Promotions above a certain discount threshold or budget need finance/manager approval before execution. Prevents rogue discounting | MEDIUM | Configurable rules (e.g., >30% discount requires manager approval, >50M KRW budget requires director). Status transitions: draft -> pending approval -> approved/rejected -> active. Notification on approval request |
| D10 | **Korean E-Commerce Calendar Events** | Pre-loaded Korean retail calendar: Chuseok, Lunar New Year, Black Friday Korea, OY BigBang dates, 11/11 Singles Day, White Day (3/14), Pepero Day (11/11), summer/winter seasonal transitions | LOW | Built-in Korean retail event calendar overlay on promotion calendar. Helps brand managers plan around key dates. Updated annually. Unique domain knowledge that generic tools lack |
| D11 | **Promotion Scenario Simulation** | "What if we do 30% off vs. BOGO on this product at Oliveyoung?" -- test different promo mechanics before committing. Reduces guesswork | HIGH | What-if calculator: input discount type + value, see projected P&L impact based on historical data or manual assumptions. Compare up to 3 scenarios side-by-side. Depends on D1, D6 being populated |

### Anti-Features (Commonly Requested, Often Problematic)

Features that seem good but create problems for a Phase 1 K-beauty TPM product.

| # | Feature | Why Requested | Why Problematic | Alternative |
|---|---------|---------------|-----------------|-------------|
| A1 | **Real-Time Channel API Integration** | "Auto-pull sales data from Coupang/OY/Naver" | Each Korean channel has different (or no) public API. Coupang Rocket Growth has seller APIs but they change frequently. OY has no public brand API. Integration maintenance cost is enormous for a startup. Blocks launch on external dependencies | Manual data entry first. CSV import second. Channel APIs as Phase 3+ when revenue justifies maintenance cost. Design data model to be API-ready but do not build integrations yet |
| A2 | **AI-Powered Demand Forecasting** | Enterprise TPM tools market this heavily | Requires 2+ years of historical data to be meaningful. K-beauty SMBs starting fresh have no data. AI forecasting without data is snake oil. Massive engineering cost for questionable accuracy at SMB scale | Simple baseline estimation (manual + historical average). "Smart suggestions" based on same-period-last-year only after 12+ months of data accumulation |
| A3 | **Full ERP/Accounting Integration** | "Connect to our SAP/QuickBooks" | K-beauty SMBs (5-50 people) rarely use ERP. Those that do use Korean systems (Douzone, Wehago) with poor API support. Integration effort is disproportionate to user base that needs it | CSV/Excel export that accountants can import. API endpoints for future integration. Focus on being the source of truth for promotions, not replacing ERP |
| A4 | **Deduction Management & Claims Processing** | Core feature in enterprise TPM (Salesforce, TELUS) | This is a CPG-manufacturer-to-retailer reconciliation workflow. K-beauty brands selling on Korean e-commerce platforms do not process deductions the same way as US CPG companies selling to Walmart. Different commercial model | Track channel fees and subsidies as line items in per-promotion P&L. Do not build a full deduction management module |
| A5 | **In-Store Retail Execution Monitoring** | Enterprise TPM includes photo-based compliance checks | PromoHub targets e-commerce promotions, not in-store. Korean beauty is increasingly online-first. Adding offline retail execution doubles scope | Stay focused on e-commerce channel promotions. If offline becomes important, it is a separate product vertical |
| A6 | **Real-Time Collaborative Editing** | "Like Google Docs for promotions" | Massive technical complexity (CRDTs, WebSockets, conflict resolution). Promotions are not documents -- they are structured records with approval flows. Concurrent editing of the same promotion is an edge case | Optimistic locking: warn when two users edit same promotion simultaneously. Last-save-wins with change history. Real-time status updates via Supabase Realtime for calendar refresh |
| A7 | **Competitor Price Monitoring** | "Track what competitors are promoting" | Requires web scraping infrastructure, legal considerations, constant maintenance as sites change. Phase 2/3 feature at best | Manual competitor notes field on promotions. "Competitive context" section where users can paste screenshots or notes |
| A8 | **Multi-Currency / Multi-Region** | "Support USD, JPY for global expansion" | Adds complexity to every calculation, every display, every export. Target market is Korean domestic brands | KRW only. Korean date formats. Asia/Seoul timezone. Add multi-currency only when expanding to global K-beauty brands (Phase 3+) |

## Feature Dependencies

```
[T4 Product/SKU Management]
    |
    +--requires--> [T2 Promotion CRUD] (promotions reference products)
    |
    +--enables---> [D1 Per-Promotion P&L] (needs COGS from products)
                       |
                       +--enables---> [D2 ROI/Uplift Analysis] (needs P&L data)
                       |                   |
                       |                   +--enables---> [D7 Post-Event Analysis] (needs ROI framework)
                       |
                       +--requires--> [D6 Baseline Volume] (P&L needs baseline to calc incremental)

[T1 Promotion Calendar]
    |
    +--enhances--> [T5 Conflict Detection] (visual overlap indicators on calendar)
    |
    +--enhances--> [D10 Korean Calendar Events] (overlay on calendar)
    |
    +--enhanced-by--> [D4 Promotion Templates] (one-click create from template onto calendar)

[T6 Team Collaboration]
    |
    +--requires--> [T7 RBAC] (team sharing needs role permissions)
    |
    +--enables---> [D9 Approval Workflow] (needs team roles for approver assignment)

[T12 Authentication]
    |
    +--requires--> [T6 Team Collaboration] (auth needed before team features)

[D3 Historical Library]
    |
    +--requires--> [T2 Promotion CRUD] (completed promotions feed the library)
    |
    +--enhanced-by--> [D7 Post-Event Analysis] (PEA results enrich historical records)
    |
    +--enables---> [D11 Scenario Simulation] (uses historical data for projections)

[D1 P&L] --conflicts-with--> [A2 AI Forecasting]
    (Manual P&L is the honest v1; AI forecasting without data is misleading.
     Build P&L first, accumulate data, then layer AI)
```

### Dependency Notes

- **D1 (P&L) requires T4 (Products):** COGS data from product management is essential for margin calculations. Products must exist before P&L can be calculated.
- **D2 (ROI/Uplift) requires D1 (P&L) and D6 (Baseline):** Cannot calculate incremental profit without knowing both the full P&L and the baseline volume. This is the most complex dependency chain.
- **D7 (Post-Event Analysis) requires D2 (ROI/Uplift):** PEA is the workflow that captures actual results and feeds them into the ROI framework. Without the framework, PEA is just data entry.
- **D9 (Approval Workflow) requires T7 (RBAC):** Approval needs defined roles (who can approve) and team structure.
- **D11 (Scenario Simulation) requires D1 (P&L) + D3 (Historical Library):** Simulations are only as good as the P&L model and the historical data behind them. Build last.
- **A2 (AI Forecasting) conflicts with D1 (P&L) in sequencing:** Premature AI before manual data accumulation produces garbage outputs. P&L data collection for 12+ months must precede any AI features.

## MVP Definition

### Launch With (v1)

Minimum viable product -- replace the Excel spreadsheet for K-beauty brand managers.

- [x] **T1 Promotion Calendar** -- the anchor UI; brand managers think in calendars
- [x] **T2 Promotion CRUD** -- create and manage promotions with all key fields
- [x] **T3 Channel Management** -- pre-seeded Korean channels (OY, Coupang, Naver, Kakao, Musinsa)
- [x] **T4 Product/SKU Management** -- basic product list with COGS and pricing
- [x] **T5 Conflict Detection** -- visual warnings for overlapping promos (same product, same dates, different channels)
- [x] **T8 Basic Status Tracking** -- draft/planned/active/ended lifecycle
- [x] **T9 Promotion List + Filters** -- alternative to calendar for bulk viewing
- [x] **T11 Korean Language** -- Korean-first UI
- [x] **T12 Authentication** -- email/password login, multi-tenant team isolation
- [x] **D10 Korean Calendar Events** -- pre-loaded Korean retail calendar (low effort, high perceived value)

### Add After Validation (v1.x)

Features to add once core is working and first paying users provide feedback.

- [ ] **T6 Team Collaboration + T7 RBAC** -- trigger: when teams of 3+ are onboarding, role permissions become necessary
- [ ] **T10 Data Export** -- trigger: when users ask "can I share this with my boss?"
- [ ] **D1 Per-Promotion P&L** -- trigger: immediately after v1 launch; this is the primary differentiator that justifies paid tier
- [ ] **D6 Baseline Volume** -- trigger: concurrent with D1; users enter baselines as part of P&L workflow
- [ ] **D4 Promotion Templates** -- trigger: when users create their 3rd recurring promotion and complain about re-entry
- [ ] **D5 Channel-Specific Promo Types** -- trigger: when users request channel-specific fields; enriches the domain model
- [ ] **D3 Historical Library** -- trigger: after 3+ months of data accumulation; promotions auto-archive

### Future Consideration (v2+)

Features to defer until product-market fit is established.

- [ ] **D2 ROI/Uplift Analysis** -- defer until enough P&L data exists (3-6 months); the 2x2 matrix needs real numbers
- [ ] **D7 Post-Event Analysis** -- defer until ROI framework is solid; the workflow adds value only on top of working analytics
- [ ] **D9 Approval Workflow** -- defer until teams are large enough to need governance; most early users will be 1-3 person teams
- [ ] **D8 Cross-Functional Dashboard** -- defer until multiple roles are actively using the system
- [ ] **D11 Scenario Simulation** -- defer until historical data is rich enough; requires 12+ months of promotion data

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority | Phase |
|---------|------------|---------------------|----------|-------|
| T1 Promotion Calendar | HIGH | MEDIUM | P1 | v1 |
| T2 Promotion CRUD | HIGH | MEDIUM | P1 | v1 |
| T3 Channel Management | HIGH | LOW | P1 | v1 |
| T4 Product/SKU Mgmt | HIGH | MEDIUM | P1 | v1 |
| T5 Conflict Detection | HIGH | MEDIUM | P1 | v1 |
| T8 Status Tracking | MEDIUM | LOW | P1 | v1 |
| T9 List View + Filters | MEDIUM | LOW | P1 | v1 |
| T11 Korean Language | HIGH | MEDIUM | P1 | v1 |
| T12 Authentication | HIGH | MEDIUM | P1 | v1 (done) |
| D10 Korean Calendar | MEDIUM | LOW | P1 | v1 |
| D1 Per-Promotion P&L | HIGH | HIGH | P1 | v1.1 |
| D6 Baseline Volume | HIGH | MEDIUM | P1 | v1.1 |
| T6 Team Collaboration | MEDIUM | LOW | P2 | v1.x |
| T7 RBAC | MEDIUM | MEDIUM | P2 | v1.x |
| T10 Data Export | MEDIUM | LOW | P2 | v1.x |
| D4 Templates | MEDIUM | MEDIUM | P2 | v1.x |
| D5 Channel Promo Types | MEDIUM | MEDIUM | P2 | v1.x |
| D3 Historical Library | HIGH | MEDIUM | P2 | v1.x |
| D2 ROI/Uplift (2x2) | HIGH | HIGH | P2 | v2 |
| D7 Post-Event Analysis | HIGH | HIGH | P2 | v2 |
| D9 Approval Workflow | MEDIUM | MEDIUM | P3 | v2 |
| D8 Cross-Func Dashboard | MEDIUM | MEDIUM | P3 | v2 |
| D11 Scenario Simulation | MEDIUM | HIGH | P3 | v2+ |

**Priority key:**
- P1: Must have for launch (or immediately after)
- P2: Should have, add when possible
- P3: Nice to have, future consideration

## Competitor Feature Analysis

No direct Korean-market TPM competitor exists for K-beauty SMBs. The comparison below maps enterprise TPM features to PromoHub's approach.

| Feature | Enterprise TPM (Salesforce/TELUS/CPGvision) | UpClear (Mid-Market) | Excel (Current State for K-beauty) | PromoHub (Our Approach) |
|---------|----------------------------------------------|----------------------|-------------------------------------|------------------------|
| Promotion Calendar | Gantt-like, account-centric | Account calendar | Manual calendar sheets | Channel-centric calendar with Korean retail events overlay |
| P&L per Promotion | Full with ERP integration | Integrated with fund tracking | Manual spreadsheet (error-prone, no standardization) | Structured P&L form with COGS, discount, subsidy, stock-up, cannibalization costs. Manual entry, standardized format |
| ROI Measurement | AI-driven predictive + post-event | Prescriptive analytics | Ad-hoc calculation, often skipped | Simon-Kucher 2x2 matrix (ROI x Uplift). Manual actuals entry, automatic calculation |
| Channel Support | Generic retailer accounts (Walmart, Kroger focus) | Multi-market configurable | N/A | Pre-built Korean channel models (OY, Coupang, Naver, Kakao, Musinsa) with channel-specific promo types |
| Deduction Mgmt | Full claims/settlement workflow | Accrual tracking | N/A | Not building. Track as P&L line items only |
| Approval Workflow | Multi-level, ERP-connected | Basic approval | Email/chat-based | Simple configurable approval rules (Phase 2) |
| Team Size Target | 100+ users, enterprise | 10-50 users | 1-5 users | 2-20 users per team |
| Price Range | $50K-500K+/year | $20K-100K/year | Free | Target: $50-200/user/month |
| Korean Market Fit | None (US/EU focused) | None (global CPG) | Fully manual but familiar | Native Korean: language, channels, calendar, currency, promo mechanics |
| Implementation Time | 6-18 months | 3-6 months | Immediate | Self-serve, same day |

### Key Insight

PromoHub's competitive advantage is NOT feature parity with enterprise TPM. It is:
1. **Korean-market-native** -- pre-built for OY/Coupang/Naver/Kakao/Musinsa channel mechanics
2. **SMB-accessible** -- self-serve, affordable, no implementation project required
3. **P&L-first** -- structured promotion profitability that Excel cannot maintain consistently
4. **Calendar-anchored** -- the mental model K-beauty brand managers already use

Enterprise TPM tools are overkill for a 10-person cosmetics company. Excel is underkill. PromoHub fills the gap.

## Sources

### TPM Industry & Features
- [15 Best Trade Promotion Management Software 2026 - The Retail Exec](https://theretailexec.com/tools/best-trade-promotion-management-software/)
- [Aforza TPM Guide 2026](https://aforza.com/an-updated-guide-to-trade-promotion-management-software-for-consumer-goods-companies-2026/)
- [Capterra TPM Software](https://www.capterra.com/trade-promotion-management-software/)
- [Gartner Peer Insights - TPM](https://www.gartner.com/reviews/market/trade-promotion-management-and-optimization-for-the-consumer-goods-industry)
- [Salesforce Consumer Goods TPM](https://www.salesforce.com/consumer-goods/trade-promotion-management-software/)
- [TELUS TPM Guide](https://www.telus.com/agcg/en-us/blog-resources/what-is-trade-promotion-management)
- [UpClear - Calculate Promotional ROI](https://upclear.com/calculate-promotional-roi-start-5-key-building-blocks/)
- [CPGvision - Trade Promotion KPIs](https://www.cpgvision.com/blog/trade-promotion-kpis)

### ROI & Measurement Methodology
- [Simon-Kucher - How to Best Measure Promotional Effectiveness](https://www.simon-kucher.com/en/insights/how-best-measure-promotional-effectiveness-everything-you-need-know-calculating-promotion)
- [Visualfabriq - Trade Promotion ROI in CPG](https://visualfabriq.com/knowledge-hub/how-to-evaluate-trade-promotion-roi-in-the-cpg-industry)
- [Strategy& (PwC) - Seven Core Principles for Trade Promotion ROI](https://www.strategyand.pwc.com/gx/en/insights/archive/getting-post-event-analysis-right/strategyand-getting-post-event-analysis-right.pdf)
- [Confido - Calculating True ROI of Trade Promotion](https://www.confidotech.com/blogs/calculating-the-true-roi-of-a-trade-promotion-methods-and-walkthrough)

### Korean E-Commerce & K-Beauty Market
- [Creatrip - Olive Young Year-Round Sales Schedule](https://creatrip.com/en/news/14342)
- [Coupang Rocket Growth Seller Tools](https://sell.coupang.com/en-us)
- [Coupang Global Sellers - Free Exposure Promotion](https://globalsellers.coupang.com/en/seller-university/free-exposure-promotion/)
- [Coupang Global Sellers - Discount Coupons](https://globalsellers.coupang.com/en/seller-university/discount-coupons/)
- [Korea Shopping Sales Calendar - MyKoreaPicks](https://mykoreapicks.com/2025-korea-shopping-sales-calendar/)

### TPM Market Data
- [Business Research Insights - TPM Software Market (CAGR 9.62%)](https://www.businessresearchinsights.com/market-reports/trade-promotion-management-tpm-software-market-109449)
- [Trade Marketing Insider - TPM Strategies, Tools & Trends](https://trademarketinginsider.com/trade-promotion-management-strategies-tools-trends/)

---
*Feature research for: Trade Promotion Management SaaS (K-beauty / Cosmetics)*
*Researched: 2026-02-17*
