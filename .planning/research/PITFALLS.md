# Pitfalls Research

**Domain:** Trade Promotion Management (TPM) SaaS for K-Beauty
**Researched:** 2026-02-17
**Confidence:** MEDIUM-HIGH (domain pitfalls well-documented in CPG industry; K-beauty/Korean channel specifics based on market knowledge + limited public TPM post-mortems)

## Critical Pitfalls

### Pitfall 1: Building P&L Without a Price Waterfall Foundation

**What goes wrong:**
Teams build a "promotion P&L" that is really just `revenue - discount = margin`. This misses the entire gross-to-net waterfall: off-invoice deductions, scan-backs, retailer fees, slotting fees, marketing allowances, and logistics costs. The resulting P&L shows promotions as profitable when they actually destroy margin. Nearly 60% of trade promotions fail to break even (industry-wide), and bad P&L models hide this truth.

**Why it happens:**
Developers model P&L as a simple subtraction because the price waterfall concept (List Price -> Invoice Price -> Pocket Price -> Pocket Margin) is a pricing/finance concept, not a software engineering concept. Without domain expertise, the data model captures "discount_value" and "revenue" but misses 5-8 deduction layers between them.

**How to avoid:**
Design the promotion P&L data model around the Simon-Kucher price waterfall from day one. Even if users manually enter data, the schema must have fields for: list price, on-invoice deductions (product discounts, promotional credits), invoice price, off-invoice deductions (rebates, marketing allowances, slotting fees, retailer-specific fees), pocket price, COGS, and pocket margin. Start with manual entry of these fields; don't try to auto-calculate everything initially.

Concrete schema requirement:
```
promotion_financials:
  list_price_per_unit
  on_invoice_discount        (percentage or fixed)
  invoice_price_per_unit     (calculated)
  retailer_fee               (OliveYoung commission, Coupang fees, etc.)
  marketing_allowance        (co-op marketing, display fees)
  logistics_cost             (shipping, fulfillment per channel)
  rebate_amount              (scan-back, volume rebate)
  pocket_price_per_unit      (calculated: invoice - all off-invoice)
  cogs_per_unit
  pocket_margin_per_unit     (calculated: pocket_price - cogs)
```

**Warning signs:**
- Your promotion form only has one "discount" field
- P&L report shows all promotions as profitable
- Finance team says "these numbers don't match our actuals"
- No distinction between "what we invoice" and "what we actually receive"

**Phase to address:**
Phase 1 (schema design). The waterfall columns can be nullable/optional at first, but the schema must accommodate them. Retrofitting a flat discount model into a waterfall model requires a database migration and complete UI rewrite of the P&L section.

---

### Pitfall 2: Wrong Baseline = Wrong ROI = Wrong Decisions

**What goes wrong:**
ROI is calculated as `(promoted_sales - regular_sales) / promo_cost`. But "regular_sales" (the baseline) is set incorrectly -- typically as a simple average of the prior 4 weeks. This ignores seasonality (Chuseok, Lunar New Year, summer peaks for K-beauty), underlying growth/decline trends, and the pre-promotion dip (consumers delay purchases anticipating a sale). The result: ROI is systematically overstated by 30-70%, and teams keep running unprofitable promotions believing they work.

**Why it happens:**
Accurate baseline modeling requires statistical decomposition (trend + seasonality + noise). For an MVP, nobody wants to build a time-series model. So developers use a naive average, or worse, let users self-report "expected sales without promo." Users always underestimate baseline to make their promotions look good.

**How to avoid:**
For Phase 1 (manual data entry), require users to input baseline explicitly and label it clearly as an estimate. Provide guidance text: "What would sales have been without this promotion, considering seasonal patterns?" Store the baseline methodology used (manual estimate, 4-week average, year-over-year, etc.) as metadata so it can be audited later. Do NOT auto-calculate ROI from a naive baseline without flagging the methodology.

For Phase 2+, implement at minimum a year-over-year comparison baseline (same period last year, adjusted for growth rate). This is far more accurate than trailing-average for seasonal K-beauty products.

Formula to implement correctly:
```
Incremental Volume = Promoted Volume - Baseline Volume - Forward Buy - Cannibalization + Halo
ROI = (Incremental Volume * Pocket Margin per Unit) / Total Trade Spend
```

**Warning signs:**
- All promotions show positive ROI (statistically impossible)
- ROI figures are 200-400% (unrealistic for K-beauty; typical good promotions are 120-180%)
- No field for "baseline methodology" in data model
- Users never edit the baseline number

**Phase to address:**
Phase 1 (data model must include baseline fields). Phase 2 (implement basic year-over-year baseline calculation). Phase 3 (advanced baseline modeling if data volume supports it).

---

### Pitfall 3: Ignoring Post-Promotion Effects in ROI

**What goes wrong:**
The system measures sales lift during the promotion period only. It ignores three critical post-promotion effects: (1) post-promotion decay/dip -- sales drop below baseline after the promo ends as consumers deplete stockpiled inventory; (2) cannibalization -- the promoted SKU steals sales from other SKUs in the same brand's portfolio; (3) forward buying -- retailers or consumers stock up during the promo, creating artificial lift followed by a demand hole. Without accounting for these, ROI is overstated by 40-70% (per CFO Pro Analytics research).

**Why it happens:**
These effects require tracking sales data beyond the promotion window (typically 4-8 weeks after), and they require product-level and category-level data. In an MVP focused on calendar + manual entry, the data to calculate these effects simply isn't being collected.

**How to avoid:**
In Phase 1, add an optional "post-promotion review" section to each promotion. Fields: post_promo_sales_week1, post_promo_sales_week2, estimated_cannibalization_pct, estimated_forward_buy_pct. Even manual estimates are better than ignoring these effects entirely.

In the data model, distinguish between:
- **Gross Lift**: Total sales during promo minus baseline
- **Net Incremental**: Gross Lift minus cannibalization minus forward-buy minus post-promo decay plus halo

Display both numbers. Never show only gross lift as "promotion performance."

**Warning signs:**
- Promotion detail view shows only "during promo" metrics
- No way to record what happened after a promotion ended
- Same product shows great ROI on promo after promo, but annual category sales are flat

**Phase to address:**
Phase 1 (add post-promotion review fields to schema). Phase 2 (build post-event analysis UI). Phase 3 (automate with data integration).

---

### Pitfall 4: Channel-Agnostic Data Model for Channel-Specific Reality

**What goes wrong:**
The system treats OliveYoung, Coupang, Naver, Kakao, and Musinsa as interchangeable "channels" with the same promotion mechanics. In reality, each Korean e-commerce channel has fundamentally different promotion structures: OliveYoung has specific commission tiers and "1+1" mechanics; Coupang has Rocket delivery cost implications; Naver has Smart Store fee structures and search ad costs; Musinsa has seasonal event fees. A generic "discount_type: percentage | bogo | coupon" enum cannot capture channel-specific promotion mechanics, fee structures, or performance metrics.

**Why it happens:**
Abstraction is a developer instinct. "A promotion is a promotion" feels clean. But K-beauty promotion management is where the abstractions leak -- every channel has different fee structures, different promotion types, different reporting metrics, and different settlement timelines.

**How to avoid:**
Use a hybrid model: a shared `promotions` table for common fields (title, dates, status, product) + a `channel_promotion_details` JSONB column or a set of channel-specific tables for channel-specific fields. At minimum, the schema needs:

- Channel-specific fee structure (commission rate, fixed fees, variable fees)
- Channel-specific promotion types (OliveYoung: 1+1, N+1, time-deal; Coupang: rocket-wow price, gold-box; Naver: smart-deal, live-commerce)
- Channel-specific settlement period (OliveYoung: ~30 days; Coupang: ~14 days; varies)
- Channel-specific metrics (Naver: search ranking impact; OliveYoung: category ranking; Coupang: Rocket badge effect)

JSONB is recommended for Phase 1 flexibility -- strict channel tables can come later when patterns stabilize.

**Warning signs:**
- Users request "custom fields" within weeks of launch
- Channel managers say "this doesn't capture how OliveYoung works"
- Fee calculations are wrong for specific channels
- The "promotion type" dropdown doesn't match what channels actually offer

**Phase to address:**
Phase 1 (schema design). Add JSONB `channel_config` and `channel_details` columns from the start. Populate with channel-specific schemas for the 5 Korean channels.

---

### Pitfall 5: Calendar Without Conflict Intelligence

**What goes wrong:**
The promotion calendar shows events on dates but doesn't detect or surface conflicts: same product on multiple channels with different prices (channel conflict), overlapping promotions cannibalizing each other, promotions scheduled during inventory shortages, or promotions conflicting with competitor pricing. The calendar becomes a display tool rather than a planning tool, no better than a shared Google Calendar.

**Why it happens:**
Building a calendar view is a solved UI problem. Building conflict detection requires business rules that intersect products, channels, dates, and inventory -- a graph of relationships that most developers underestimate. It's the difference between "display data" and "analyze data."

**How to avoid:**
Define conflict rules as first-class entities in the system. Start with the simplest, highest-value conflicts:

1. **Same-product, overlapping-date, different-channel price conflict**: If Product A is 20% off on OliveYoung and 30% off on Coupang during the same week, flag it. Channels monitor competitors and may penalize brands for price inconsistency.
2. **Same-channel, overlapping-date, same-category cannibalization**: Two promotions for similar products on the same channel at the same time.
3. **Date conflict with Korean retail calendar**: Promotions that collide with major events (OliveYoung's Mega Sale, Coupang's Wow Week) need to be flagged as either conflicts or opportunities.

Implement as a background check on promotion create/update, surfaced as warnings (not blockers).

**Warning signs:**
- Users maintain a separate spreadsheet to track conflicts
- Channel managers discover price inconsistencies after promotions go live
- Calendar shows 10+ overlapping promotions with no visual distinction of conflicts

**Phase to address:**
Phase 1 (basic same-product date overlap detection). Phase 2 (cross-channel price conflict detection, Korean retail calendar integration).

---

### Pitfall 6: Multi-Tenant Data Leakage Through Supabase RLS Gaps

**What goes wrong:**
In a multi-tenant B2B SaaS where Company A must never see Company B's promotion data, RLS policies have gaps: missing policies on new tables, policies that check `user_id` instead of `team_id` (allowing users who switch companies to see old data), or policies bypassed by API routes using the service_role key. One data leak in a promotion management tool (which contains pricing strategy, discount depths, product launch timing) would be catastrophic for customer trust.

**Why it happens:**
RLS is "opt-in per table" in Supabase. New tables default to NO RLS. Developers add tables (e.g., `promotion_financials`, `post_promotion_reviews`) and forget to add RLS policies. Additionally, complex queries with joins sometimes bypass RLS if the joined table lacks its own policy. Custom JWT claims for `team_id` are not set up, forcing expensive subqueries in every policy.

**How to avoid:**
1. Create a migration template that always includes `ALTER TABLE x ENABLE ROW LEVEL SECURITY` and a default-deny policy
2. Store `team_id` as a custom JWT claim via Supabase Auth hooks -- this makes every RLS policy a simple `team_id = (auth.jwt() -> 'team_id')` check instead of a subquery to `team_members`
3. Never use `service_role` key in API routes that handle user requests
4. Add a CI check: script that verifies every table has RLS enabled and at least one policy

**Warning signs:**
- Any table in the schema without `ENABLE ROW LEVEL SECURITY`
- API routes using `createClient()` with service_role key
- RLS policies that do subqueries to `team_members` (performance + correctness risk)
- No automated test for cross-tenant data isolation

**Phase to address:**
Phase 1 (foundational -- must be correct from the first migration). Every migration that creates a table must include RLS. Test with two test tenants from day one.

---

## Technical Debt Patterns

Shortcuts that seem reasonable but create long-term problems.

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Storing all financial values as floating point | Simple to implement | Rounding errors compound across hundreds of promotions; P&L totals don't reconcile | Never. Use integer cents or PostgreSQL `NUMERIC(12,2)` from day one |
| Single "discount_value" field instead of price waterfall | Faster form to build | Cannot compute accurate P&L; requires schema migration + data backfill + UI rewrite | Never for a TPM tool. This is the core domain |
| Hardcoded channel list in frontend | Faster development | Cannot add new channels without code deploy; inconsistent IDs between frontend and DB | Only in first 2 weeks of MVP; migrate to DB-driven within Phase 1 |
| Using localStorage for filter state | Quick UX win | Filters don't sync across devices; team members can't share views; breaks on logout | Acceptable for Phase 1 if URL params are planned for Phase 2 |
| Skipping audit logging on financial data changes | Less code to write | Cannot trace who changed a discount from 20% to 40%; compliance/trust issue for B2B | Never for financial fields. Log from Phase 1 |
| Naive date comparisons without timezone | Works in development | Promotions that start/end at midnight KST show on wrong dates for server-side rendering | Never. Use `Asia/Seoul` timezone consistently from day one |

## Integration Gotchas

Common mistakes when connecting to external services or handling Korean e-commerce channel specifics.

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| Supabase Auth + Next.js SSR | Using `getSession()` instead of `getUser()` for auth checks; session can be stale | Always use `supabase.auth.getUser()` which validates against the server; use middleware for session refresh |
| Korean Won currency handling | Using `number` type and dividing by 10000 for display | Store as integer (won), display with Korean formatting (만/억 units). Never store sub-won values -- KRW has no decimal places |
| Date handling across SSR/client | Server renders in UTC, client hydrates in KST, causing hydration mismatch on date boundaries | Store all dates as UTC in DB. Set server timezone to UTC. Convert to `Asia/Seoul` only at render time. Use `suppressHydrationWarning` on date elements or render dates client-side only |
| OliveYoung/Coupang fee structures | Hardcoding commission rates | Commission rates change quarterly. Store as config per channel per date range. Provide UI for users to update their contracted rates |
| Multi-channel promotion scheduling | Assuming channels share the same promotional calendar | Each channel has its own event calendar (OliveYoung Mega Sale, Coupang Wow Week, Naver Brand Day). Maintain a reference calendar of known channel events |
| Supabase RLS with joins | Assuming RLS on table A protects data when joining to table B | Each table needs its own RLS policy. A join `promotions JOIN products` requires RLS on BOTH tables |

## Performance Traps

Patterns that work at small scale but fail as usage grows.

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Loading all promotions for calendar view | Calendar loads slowly; browser memory spikes | Fetch only promotions within visible date range + 1 month buffer; paginate promotion list views | 500+ promotions per team (reached within 6-12 months for active K-beauty brand) |
| RLS policies with subqueries to `team_members` | Every query adds 2-5ms for the policy check; compounds with multiple tables | Use JWT custom claims for `team_id`; index `team_id` on all tables | 50+ concurrent users across tenants |
| Unindexed date range queries | Calendar view query time increases linearly | Add composite index on `(team_id, start_date, end_date)` and `(team_id, channel_id, start_date)` | 1000+ promotions per team |
| Fetching full promotion objects for calendar cells | Calendar loads 50+ full objects including financial data, notes, history | Create a `calendar_promotion_summary` view or DTO with only: id, title, channel, dates, status, color | 200+ promotions visible in month view |
| Computing P&L aggregations client-side | JavaScript freezes computing roll-ups across 100+ promotions | Use PostgreSQL aggregate queries or materialized views for P&L summaries | Monthly P&L report with 50+ promotions |

## Security Mistakes

Domain-specific security issues beyond general web security.

| Mistake | Risk | Prevention |
|---------|------|------------|
| Exposing competitor pricing data between tenants | Company A sees Company B's discount strategy; competitive intelligence leak; potential legal liability | RLS on every table; never use service_role in user-facing APIs; automated cross-tenant isolation tests |
| Financial data in client-side state without encryption | Promotion P&L data (margins, costs, discount depths) visible in browser DevTools | Minimize financial data sent to client; compute summaries server-side; never cache financial data in localStorage |
| Audit trail gaps on financial field changes | Cannot prove who authorized a discount change; problematic for B2B accountability | Implement `promotion_audit_log` table with trigger on UPDATE of any financial field; store old_value, new_value, changed_by, timestamp |
| Allowing bulk export without team scoping | A user exports "all promotions" and the query doesn't enforce team_id | All export endpoints must use the authenticated Supabase client (not service_role); verify team_id in export queries |
| Promotion URLs with predictable IDs | Attacker iterates promotion IDs to probe for data | Use UUIDs (already in schema); combine with RLS so even guessing a UUID returns 404 for wrong team |

## UX Pitfalls

Common user experience mistakes in this domain.

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| Forcing full P&L entry on every promotion | Users skip the form or enter garbage data; adoption drops | Progressive disclosure: require only title/channel/dates/discount to create. P&L fields are optional, surfaced in a "Financials" tab. Gradually encourage completion with a "completeness score" |
| Calendar as the only entry point | Brand managers who manage 50+ promotions/month need a list/table view for bulk operations | Provide both calendar view (planning/visualization) and table view (data entry/management). Table view with inline editing is critical for power users |
| Single-currency assumption | K-beauty brands selling on global channels (Shopee, Amazon) need multi-currency support | Design currency as a per-promotion field from the start (default: KRW). Even if Phase 1 is KRW-only, the schema should support it |
| No promotion templates for recurring events | "OliveYoung Monthly 1+1" happens every month with minor variations. Recreating from scratch each time is tedious | Implement "duplicate promotion" in Phase 1. Full template system (with variable fields) in Phase 2 |
| Conflict warnings that block instead of inform | Users get frustrated when the system prevents them from creating a promotion due to detected conflicts | Show conflicts as warnings with explanation, not as form validation errors. Let users acknowledge and proceed. Some "conflicts" are intentional strategy |
| Overwhelming P&L dashboards | Non-finance users (brand managers) are intimidated by waterfall charts and financial jargon | Provide two views: (1) Simple -- traffic light (green/yellow/red) ROI indicator per promotion; (2) Detailed -- full waterfall breakdown for finance team. Default to simple view |

## "Looks Done But Isn't" Checklist

Things that appear complete but are missing critical pieces.

- [ ] **Calendar View:** Often missing timezone handling -- promotions that span midnight KST show on wrong dates when server renders in UTC. Verify by checking a promotion ending at 2026-03-01 00:00 KST displays correctly
- [ ] **Promotion CRUD:** Often missing optimistic locking -- two team members editing the same promotion simultaneously will silently overwrite each other's changes. Verify with concurrent edit test
- [ ] **P&L Calculation:** Often missing the distinction between "planned" and "actual" financials. A promotion has estimated P&L (before) and actual P&L (after). Both must exist. Verify schema has `planned_*` and `actual_*` columns
- [ ] **ROI Display:** Often shows gross lift ROI without labeling the methodology. Users assume it's net incremental. Verify the UI clearly states "Estimated ROI (gross lift method)" or equivalent
- [ ] **Channel Filter:** Often filters promotions client-side from a full dataset instead of server-side. Works with 50 promotions, fails with 500. Verify by checking the API call includes channel filter parameters
- [ ] **Team Permissions:** Often checks "is user authenticated" but not "does user belong to this team" or "does user have edit permission." Verify a `viewer` role user cannot modify promotions
- [ ] **Export/Report:** Often exports currently visible data only, not all data matching the filter criteria. Verify export with pagination -- does it export all 200 promotions or just the 20 on screen?
- [ ] **Conflict Detection:** Often checks only exact date overlap, missing "adjacent promotions" (Promo A ends Monday, Promo B starts Tuesday on same product = consumers just wait). Verify with 1-day-gap test case
- [ ] **Settlement Tracking:** Often missing entirely. The promotion ran, but did we actually receive payment from the channel? Without settlement tracking, "actual P&L" is still theoretical

## Recovery Strategies

When pitfalls occur despite prevention, how to recover.

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Flat discount model (no waterfall) | HIGH | Schema migration adding waterfall columns; backfill historical data with estimates; rewrite P&L UI. 2-3 week effort minimum |
| Wrong baseline methodology baked in | MEDIUM | Add baseline_methodology column; re-calculate ROI for historical promotions with corrected baseline; update UI to show methodology. 1 week effort |
| Missing post-promotion tracking | MEDIUM | Add post-promo review tables; historical data cannot be recovered (those promotions are over). Going forward only. 1 week for schema + UI |
| Channel-agnostic data model | HIGH | Add JSONB channel details or channel-specific tables; migrate existing data; rewrite promotion forms for channel-specific fields. 2-3 weeks |
| No conflict detection | LOW | Can be added as an overlay without schema changes; query existing promotions for date/product/channel overlaps. 3-5 days |
| RLS gaps / data leakage | CRITICAL | Immediate: add missing RLS policies. Audit: review all access logs for cross-tenant queries. Communication: notify affected customers. Recovery time varies; trust damage may be permanent |
| Floating point currency | MEDIUM | Migrate column types; backfill with rounded values; audit calculations for cumulative rounding errors. 1 week with careful testing |

## Pitfall-to-Phase Mapping

How roadmap phases should address these pitfalls.

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| No price waterfall in P&L | Phase 1: Schema Design | Schema review: promotion_financials table has all waterfall columns (even if nullable) |
| Wrong baseline calculation | Phase 1: Data Model; Phase 2: Calculation Engine | Phase 1: baseline_value and baseline_methodology fields exist. Phase 2: YoY baseline auto-suggestion works |
| Missing post-promo effects | Phase 1: Schema; Phase 2: Post-Event Analysis UI | Schema has post_promotion_reviews table. Phase 2 UI allows entering post-promo sales data |
| Channel-agnostic model | Phase 1: Schema Design | Each channel has distinct promotion type options and fee structure fields in the creation form |
| Calendar without conflicts | Phase 1: Basic overlap; Phase 2: Cross-channel | Phase 1: creating overlapping same-product promo shows warning. Phase 2: cross-channel price difference flagged |
| Multi-tenant data leakage | Phase 1: Every Migration | CI script confirms all tables have RLS. Manual test: user from Team A cannot see Team B promotions |
| Floating point currency | Phase 1: Schema Design | All monetary columns use `NUMERIC` or `BIGINT` (cents), not `FLOAT` or `REAL` |
| Timezone bugs | Phase 1: First Calendar Implementation | Promotion spanning midnight KST renders correctly on calendar. Server + client show same date |
| No audit trail on financials | Phase 1: Core Tables | `promotion_audit_log` table exists with trigger on financial column changes |
| Planned vs Actual P&L gap | Phase 1: Schema; Phase 2: Post-Event | Schema has both planned and actual columns. Phase 2 UI has workflow for "close out promotion" with actual figures |

## Sources

- [Visualfabriq: Top 5 Mistakes in Trade Promotion Planning](https://visualfabriq.com/knowledge-hub/top-five-mistakes-in-trade-promotion-planning) -- MEDIUM confidence, industry vendor content
- [CFO Pro Analytics: How to Build a Trade Spend ROI Model](https://cfoproanalytics.com/cfo-wiki/cpg/how-to-build-a-trade-spend-roi-model-a-cfo-playbook-for-optimizing-cpg-promotions-profitability-growth/) -- MEDIUM-HIGH confidence, detailed methodology
- [Simon-Kucher: Navigating Pitfalls of Product Promotion](https://www.simon-kucher.com/en/insights/navigating-pitfalls-product-promotion) -- HIGH confidence, authoritative pricing consultancy
- [Simon-Kucher: Power Up the P&L with Trade Terms](https://www.simon-kucher.com/en/insights/power-pl-trade-terms-mitigate-cost-pressure) -- HIGH confidence
- [Confido Tech: Calculating True ROI of Trade Promotion](https://www.confidotech.com/blogs/calculating-the-true-roi-of-a-trade-promotion-methods-and-walkthrough) -- MEDIUM confidence, practitioner content
- [RevenueML: Guide to Price Waterfalls](https://revenueml.com/insights/articles/price-waterfalls) -- MEDIUM confidence, practical implementation guide
- [CPG Vision: Data Modeling for TPM/TPO](https://www.cpgvision.com/blog/trade-promotion-management-and-optimization) -- MEDIUM confidence, vendor content with technical depth
- [Supabase: Row Level Security Docs](https://supabase.com/docs/guides/database/postgres/row-level-security) -- HIGH confidence, official documentation
- [MakerKit: Supabase RLS Best Practices](https://makerkit.dev/blog/tutorials/supabase-rls-best-practices) -- MEDIUM confidence, community best practices
- [Vividly: 2026 Trade Promotion Success Guide](https://www.govividly.com/roi-advantage-trade-promotion-management) -- MEDIUM confidence, vendor with market data
- [Tredence: Promotion Effectiveness Uplift and Halo](https://www.tredence.com/blog/decoding-the-metrics-a-deep-dive-into-calculating-promotion-effectiveness) -- MEDIUM confidence, analytics practitioner
- [Next-intl: Reliable Date Formatting in Next.js](https://next-intl.dev/blog/date-formatting-nextjs) -- HIGH confidence, official library documentation

---
*Pitfalls research for: Trade Promotion Management SaaS (K-Beauty)*
*Researched: 2026-02-17*
