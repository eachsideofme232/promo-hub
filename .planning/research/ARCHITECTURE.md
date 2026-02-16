# Architecture Research

**Domain:** Trade Promotion Management (TPM) SaaS for K-Beauty
**Researched:** 2026-02-17
**Confidence:** HIGH (domain patterns well-established; Simon-Kucher methodology documented publicly; Supabase multi-tenant patterns verified via official docs)

## Standard Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                             │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐             │
│  │  Promotion    │  │  P&L         │  │  Analytics    │             │
│  │  Calendar     │  │  Calculator  │  │  Dashboard    │             │
│  └──────┬───────┘  └──────┬───────┘  └───────┬───────┘             │
│         │                 │                   │                     │
├─────────┴─────────────────┴───────────────────┴─────────────────────┤
│                      APPLICATION LAYER                              │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐             │
│  │  Promo        │  │  P&L         │  │  Reporting    │             │
│  │  Service      │  │  Engine      │  │  Service      │             │
│  └──────┬───────┘  └──────┬───────┘  └───────┬───────┘             │
│         │                 │                   │                     │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐             │
│  │  Team/Auth    │  │  Product     │  │  Channel      │             │
│  │  Service      │  │  Service     │  │  Service      │             │
│  └──────┬───────┘  └──────┬───────┘  └───────┬───────┘             │
│         │                 │                   │                     │
├─────────┴─────────────────┴───────────────────┴─────────────────────┤
│                      DATA LAYER                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Supabase (PostgreSQL + Auth + RLS + Realtime)               │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │   │
│  │  │promotions│  │promo_pnl │  │products  │  │teams     │    │   │
│  │  │promo_    │  │pnl_cost_ │  │promo_    │  │team_     │    │   │
│  │  │products  │  │items     │  │          │  │members   │    │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Communicates With |
|-----------|----------------|-------------------|
| **Promotion Calendar** | Visual scheduling of promotions on month/week/day views. Channel-colored cards. Drag-drop date changes. Conflict detection overlay. | Promo Service, Channel Service |
| **Promotion CRUD** | Create/read/update/delete promotions. Status lifecycle (planned -> active -> ended). Attach products. Apply templates. | Promo Service, Product Service, P&L Engine |
| **P&L Calculator UI** | Per-promotion financial worksheet. Volume decomposition inputs. Cost line items. ROI/Uplift result display. Waterfall chart. | P&L Engine |
| **P&L Engine** | Core calculation logic. Simon-Kucher 5 volume effects + 3 hidden costs. ROI and Uplift computation. Evaluation matrix quadrant classification. | Promotion data, Product data (cost/price) |
| **Analytics Dashboard** | Aggregated views: ROI by channel, by product, by period. Quadrant scatter plot. P&L waterfall summaries. Post-event vs. plan comparison. | Reporting Service, P&L Engine |
| **Team/Auth Service** | Authentication, team creation, member invitations, role management. Session handling. RLS context provider (auth.uid). | Supabase Auth, team_members table |
| **Product Service** | Product/SKU catalog. Base price and cost price management. Product-promotion linkage. | products table, promo_products table |
| **Channel Service** | Reference data for K-beauty e-commerce channels. Channel colors, filtering, display order. | channels table |
| **Reporting Service** | Query aggregation for dashboards. Period-over-period comparisons. Export to CSV/Excel. | All data tables via read queries |

## Recommended Project Structure

The existing Turborepo monorepo is the right foundation. Below is the target structure that extends what already exists.

```
promohub/
├── apps/
│   └── web/
│       └── src/
│           ├── app/
│           │   ├── (auth)/                      # Login, signup (DONE)
│           │   ├── (dashboard)/
│           │   │   ├── calendar/                # Calendar views (DONE - needs API)
│           │   │   ├── promotions/              # Promo CRUD (DONE - needs API)
│           │   │   │   ├── [id]/
│           │   │   │   │   └── pnl/             # Per-promotion P&L worksheet (NEW)
│           │   │   │   └── new/
│           │   │   ├── products/                # Product catalog (NEW)
│           │   │   ├── analytics/               # Dashboards & reports (NEW - Phase 2)
│           │   │   │   ├── overview/            # Summary dashboard
│           │   │   │   ├── roi-matrix/          # Quadrant scatter plot
│           │   │   │   └── waterfall/           # P&L waterfall view
│           │   │   └── settings/                # Team, billing (DONE - scaffold)
│           │   └── api/
│           │       ├── promotions/              # Promotion CRUD API (STUB)
│           │       ├── promotions/[id]/pnl/     # P&L data API (NEW)
│           │       ├── calendar/                # Calendar query API (STUB)
│           │       ├── products/                # Products API (NEW)
│           │       ├── channels/                # Channels API (NEW)
│           │       ├── teams/                   # Teams API (STUB)
│           │       └── analytics/               # Aggregation API (NEW - Phase 2)
│           ├── components/
│           │   ├── calendar/                    # Calendar components (DONE)
│           │   ├── promotions/                  # Promotion components (DONE)
│           │   ├── pnl/                         # P&L worksheet components (NEW)
│           │   │   ├── VolumeDecomposition.tsx   # 5 volume effect inputs
│           │   │   ├── CostBreakdown.tsx         # Direct + hidden costs
│           │   │   ├── PnlWaterfall.tsx          # Waterfall visualization
│           │   │   ├── RoiResult.tsx             # ROI calculation result
│           │   │   └── QuadrantBadge.tsx         # ROI/Uplift quadrant label
│           │   ├── analytics/                   # Dashboard charts (NEW - Phase 2)
│           │   ├── products/                    # Product components (NEW)
│           │   ├── filters/                     # Filter components (DONE)
│           │   └── layout/                      # Layout components (DONE)
│           ├── hooks/
│           │   ├── usePromotion.ts               # Promotion CRUD hooks (NEW)
│           │   ├── usePnl.ts                     # P&L calculation hook (NEW)
│           │   └── useCalendar.ts                # Calendar data hook (NEW)
│           └── lib/
│               ├── supabase/                    # Supabase clients (DONE)
│               └── pnl/                         # P&L calculation engine (NEW)
│                   ├── calculator.ts             # Core P&L math
│                   ├── volume-effects.ts         # 5 volume effect decomposition
│                   ├── hidden-costs.ts           # 3 hidden cost calculations
│                   ├── roi.ts                    # ROI & Uplift formulas
│                   └── quadrant.ts               # Evaluation matrix classifier
├── packages/
│   ├── db/
│   │   ├── queries/                             # Query functions (DONE - needs expansion)
│   │   │   ├── promotions.ts
│   │   │   ├── pnl.ts                           # P&L data queries (NEW)
│   │   │   ├── products.ts
│   │   │   ├── calendar.ts
│   │   │   ├── channels.ts
│   │   │   ├── teams.ts
│   │   │   └── analytics.ts                     # Aggregation queries (NEW)
│   │   └── seed/
│   ├── types/
│   │   └── src/
│   │       ├── promotion.ts                     # (DONE - needs P&L fields)
│   │       ├── pnl.ts                           # P&L types (NEW)
│   │       ├── product.ts                       # (DONE)
│   │       ├── team.ts                          # (DONE)
│   │       ├── channel.ts                       # (DONE)
│   │       └── analytics.ts                     # Analytics types (NEW)
│   ├── ui/                                      # Shared UI (DONE)
│   └── utils/
│       └── src/
│           ├── validation.ts                    # Zod schemas (DONE - needs P&L)
│           ├── date.ts                          # (DONE)
│           └── currency.ts                      # (DONE)
└── supabase/
    └── migrations/                              # (DONE - needs P&L tables)
```

### Structure Rationale

- **`lib/pnl/`** in the web app (not in `packages/`): The P&L engine runs client-side for instant recalculation as users change inputs. It is pure TypeScript math with no server dependencies. Keeping it in `lib/` makes it available to both React components and API routes. If a second app needs it later, extract to `packages/pnl/`.
- **`components/pnl/`** separate from `components/promotions/`**: The P&L worksheet is a distinct UI concern from promotion CRUD. Users navigate from a promotion detail to its P&L. Separating prevents the promotions folder from growing unwieldy.
- **`analytics/` is Phase 2 only**: The analytics dashboard aggregates P&L data across promotions. It depends on having real P&L data entered first. Deferring prevents building dashboards over empty data.

## Architectural Patterns

### Pattern 1: P&L Engine as Pure Calculation Module

**What:** The P&L engine is a set of pure TypeScript functions (no side effects, no database calls) that take structured inputs and return calculated results. It lives in `lib/pnl/` and is used by both UI components (for instant feedback) and API routes (for persistence/validation).

**When to use:** Any time financial calculations are needed -- creating a P&L, recalculating on input change, generating analytics summaries.

**Trade-offs:**
- Pro: Instant client-side recalculation without server round-trips
- Pro: Testable in isolation with unit tests
- Pro: Same logic used server-side for validation
- Con: Complex formulas must be kept in sync if ever duplicated

**Example:**

```typescript
// lib/pnl/calculator.ts

export interface PnlInput {
  // Volume decomposition (Simon-Kucher 5 effects)
  baselineVolume: number        // Units sold without promotion
  forwardBuyingVolume: number   // Stock-up volume (causes post-promo dip)
  cannibalizationVolume: number // Volume stolen from own other products
  competitorVolume: number      // Volume taken from competitors
  categoryIncrementalVolume: number // Genuinely new category demand

  // Pricing
  regularPrice: number          // KRW per unit (normal selling price)
  promoPrice: number            // KRW per unit (during promotion)
  costOfGoods: number           // KRW per unit (COGS)

  // Direct promotion costs
  slotFees: number              // Channel listing/slot fees (KRW)
  displayCosts: number          // In-store/online display costs (KRW)
  sampleCosts: number           // Sample/gift costs (KRW)
  otherDirectCosts: number      // Other direct costs (KRW)
}

export interface PnlResult {
  // Volume analysis
  totalPromoVolume: number
  incrementalVolume: number     // competitor + category incremental only
  subsidizedVolume: number      // baseline + forward buying + cannibalization

  // Revenue
  grossRevenue: number          // totalPromoVolume * promoPrice
  baselineRevenue: number       // what baseline would have earned at regular price
  revenueAtRegularPrice: number // totalPromoVolume * regularPrice

  // Three hidden costs (Simon-Kucher)
  costOfSubsidy: number         // baseline * (regularPrice - promoPrice)
  costOfStockUp: number         // forwardBuying * (regularPrice - promoPrice)
  costOfCannibalization: number // cannibalization * (regularPrice - promoPrice)
  totalHiddenCosts: number

  // Direct costs
  totalDirectCosts: number      // slot + display + sample + other

  // P&L
  totalCOGS: number             // totalPromoVolume * costOfGoods
  grossProfit: number           // grossRevenue - totalCOGS
  netProfit: number             // grossProfit - totalDirectCosts - totalHiddenCosts

  // ROI & evaluation
  totalPromotionInvestment: number // totalDirectCosts + totalHiddenCosts
  roi: number                   // netProfit / totalPromotionInvestment
  uplift: number                // incrementalVolume / baselineVolume
  quadrant: 'star' | 'volume-trap' | 'niche-win' | 'value-destroyer'
}

export function calculatePnl(input: PnlInput): PnlResult {
  const totalPromoVolume =
    input.baselineVolume +
    input.forwardBuyingVolume +
    input.cannibalizationVolume +
    input.competitorVolume +
    input.categoryIncrementalVolume

  const incrementalVolume =
    input.competitorVolume + input.categoryIncrementalVolume

  const priceDelta = input.regularPrice - input.promoPrice

  // Simon-Kucher 3 hidden costs
  const costOfSubsidy = input.baselineVolume * priceDelta
  const costOfStockUp = input.forwardBuyingVolume * priceDelta
  const costOfCannibalization = input.cannibalizationVolume * priceDelta
  const totalHiddenCosts =
    costOfSubsidy + costOfStockUp + costOfCannibalization

  const totalDirectCosts =
    input.slotFees + input.displayCosts + input.sampleCosts + input.otherDirectCosts

  const grossRevenue = totalPromoVolume * input.promoPrice
  const totalCOGS = totalPromoVolume * input.costOfGoods
  const grossProfit = grossRevenue - totalCOGS
  const netProfit = grossProfit - totalDirectCosts - totalHiddenCosts

  const totalPromotionInvestment = totalDirectCosts + totalHiddenCosts
  const roi = totalPromotionInvestment > 0
    ? netProfit / totalPromotionInvestment
    : 0
  const uplift = input.baselineVolume > 0
    ? incrementalVolume / input.baselineVolume
    : 0

  return {
    totalPromoVolume,
    incrementalVolume,
    subsidizedVolume: input.baselineVolume + input.forwardBuyingVolume + input.cannibalizationVolume,
    grossRevenue,
    baselineRevenue: input.baselineVolume * input.regularPrice,
    revenueAtRegularPrice: totalPromoVolume * input.regularPrice,
    costOfSubsidy,
    costOfStockUp,
    costOfCannibalization,
    totalHiddenCosts,
    totalDirectCosts,
    totalCOGS,
    grossProfit,
    netProfit,
    totalPromotionInvestment,
    roi,
    uplift,
    quadrant: classifyQuadrant(roi, uplift),
  }
}
```

### Pattern 2: ROI/Uplift Evaluation Matrix (Quadrant Classifier)

**What:** Every promotion is plotted on a 2x2 matrix with ROI on the Y-axis and Volume Uplift on the X-axis. The quadrant determines the action recommendation. This is the core Simon-Kucher framework for separating "winning" promotions from "value-destroying" ones.

**When to use:** After P&L calculation completes. Displayed on promotion detail, used for analytics aggregation, and drives the scatter plot dashboard.

**Trade-offs:**
- Pro: Simple, actionable classification
- Pro: Immediately tells users whether a promotion is worth repeating
- Con: Thresholds (what counts as "high" ROI) need calibration per team/industry

**Example:**

```typescript
// lib/pnl/quadrant.ts

export type Quadrant = 'star' | 'volume-trap' | 'niche-win' | 'value-destroyer'

export interface QuadrantThresholds {
  roiBreakeven: number   // Default: 0 (positive ROI = good)
  upliftMinimum: number  // Default: 0.1 (10% volume uplift = meaningful)
}

const DEFAULT_THRESHOLDS: QuadrantThresholds = {
  roiBreakeven: 0,
  upliftMinimum: 0.1,
}

/**
 * Classify promotion into ROI/Uplift quadrant:
 *
 *         High ROI
 *            |
 *  Niche Win | Star
 *  ----------+----------
 *  Value     | Volume
 *  Destroyer | Trap
 *            |
 *         Low ROI
 *     Low Uplift   High Uplift
 */
export function classifyQuadrant(
  roi: number,
  uplift: number,
  thresholds: QuadrantThresholds = DEFAULT_THRESHOLDS
): Quadrant {
  const highRoi = roi > thresholds.roiBreakeven
  const highUplift = uplift > thresholds.upliftMinimum

  if (highRoi && highUplift) return 'star'
  if (highRoi && !highUplift) return 'niche-win'
  if (!highRoi && highUplift) return 'volume-trap'
  return 'value-destroyer'
}

// Action recommendations per quadrant
export const QUADRANT_ACTIONS: Record<Quadrant, {
  label: string
  labelKo: string
  color: string
  action: string
  actionKo: string
}> = {
  'star': {
    label: 'Star',
    labelKo: '스타',
    color: '#22c55e', // green
    action: 'Scale and repeat',
    actionKo: '확대 반복 실행',
  },
  'niche-win': {
    label: 'Niche Win',
    labelKo: '틈새 수익',
    color: '#3b82f6', // blue
    action: 'Increase activation to boost volume',
    actionKo: '볼륨 확대를 위한 활성화 강화',
  },
  'volume-trap': {
    label: 'Volume Trap',
    labelKo: '볼륨 함정',
    color: '#f59e0b', // amber
    action: 'Reduce discount depth or frequency',
    actionKo: '할인율 또는 빈도 축소',
  },
  'value-destroyer': {
    label: 'Value Destroyer',
    labelKo: '가치 파괴',
    color: '#ef4444', // red
    action: 'Eliminate or fundamentally restructure',
    actionKo: '제거 또는 근본적 구조 변경',
  },
}
```

### Pattern 3: Team-Scoped Data Access via RLS

**What:** Every data query is automatically filtered by the authenticated user's team membership through PostgreSQL Row Level Security. The application never manually filters by team_id in queries -- RLS handles it at the database layer.

**When to use:** Every database read/write operation.

**Trade-offs:**
- Pro: Defense-in-depth -- even if application code has a bug, data cannot leak
- Pro: Queries are simpler (no WHERE team_id = ... in every query)
- Con: RLS subqueries on team_members add overhead; must index properly
- Con: Debugging query issues requires understanding RLS policies

**Implementation note:** The existing migrations already implement this pattern correctly. Every table that holds tenant data has RLS enabled with policies checking `auth.uid()` against `team_members`. The `channels` table is the exception (reference data viewable by all authenticated users), which is correct.

## Data Flow

### Core Data Flow: Promotion Lifecycle

```
[User creates promotion]
    |
    v
[PromotionForm] ──validate──> [Zod schema] ──valid──> [API Route POST /api/promotions]
    |                                                        |
    |                                              [Auth check: getUser()]
    |                                              [RLS: auto-scopes to team]
    |                                                        |
    |                                              [Supabase INSERT promotions]
    |                                                        |
    v                                                        v
[Calendar updates] <──────── [Revalidate / Refetch] <──── [201 Created]
```

### P&L Calculation Flow

```
[User opens promotion P&L]
    |
    v
[Fetch promotion + products + existing P&L data]
    |
    v
[PnlWorksheet component]
    |
    ├── [VolumeDecomposition] ── user inputs 5 volume effects
    │         |
    │         v
    ├── [CostBreakdown] ── user inputs direct costs
    │         |
    │         v
    └── [calculatePnl()] ── pure function, runs on every input change
              |
              ├──> [PnlWaterfall] ── visual P&L waterfall chart
              ├──> [RoiResult] ── ROI %, Uplift %, Quadrant badge
              └──> [Save] ── POST /api/promotions/[id]/pnl ── persists to promo_pnl table
```

### Analytics Aggregation Flow (Phase 2)

```
[Analytics Dashboard]
    |
    v
[GET /api/analytics?period=...&channel=...]
    |
    v
[Aggregate promo_pnl data via SQL]
    |
    ├── SUM/AVG ROI by channel
    ├── Quadrant distribution (% Star / Trap / etc)
    ├── P&L waterfall (total across promotions)
    └── Period-over-period comparison
    |
    v
[Dashboard renders charts]
    ├── [ScatterPlot] ── ROI vs Uplift (each dot = one promotion)
    ├── [WaterfallChart] ── Aggregated P&L
    ├── [BarChart] ── ROI by channel
    └── [TrendLine] ── Performance over time
```

### Key Data Flows

1. **Promotion -> P&L:** A promotion is the parent entity. Each promotion has zero or one P&L record. P&L is calculated from manual inputs (volume effects, costs) combined with product data (prices, COGS). The P&L result is stored for analytics but can always be recalculated from inputs.

2. **P&L -> Analytics:** Analytics dashboards aggregate across stored P&L results. They do NOT recalculate -- they query pre-computed ROI, Uplift, and financial totals from the `promo_pnl` table. This makes dashboard queries fast.

3. **Team -> Everything:** The team_id is the universal scoping key. Every promotion, product, P&L record, and template belongs to exactly one team. RLS policies enforce this boundary at the database level. A user accesses data through their team_members entry.

4. **Channel -> Promotion:** Channels are reference data shared across all teams. Each promotion belongs to exactly one channel (Oliveyoung, Coupang, etc.). Channel is used for filtering, color-coding, and analytics grouping.

## Scaling Considerations

| Scale | Architecture Adjustments |
|-------|--------------------------|
| 0-100 teams (launch) | Current architecture is fine. Supabase free/pro tier. All queries direct to PostgreSQL. Client-side P&L calculation. No caching needed. |
| 100-1K teams | Add database indexes on (team_id, start_date) composite. Consider Supabase connection pooling (PgBouncer). Pre-compute analytics summaries nightly via Supabase Edge Functions or cron. |
| 1K-10K teams | RLS subquery performance becomes a concern. Move team_id into JWT custom claims to avoid subquery on every request. Add Redis/Upstash for analytics caching. Consider read replicas for dashboard queries. |
| 10K+ teams | Evaluate schema-per-tenant for largest customers. Separate analytics into its own service/database. This is far beyond Phase 1-2 scope. |

### Scaling Priorities

1. **First bottleneck: RLS subquery performance.** Every query joins against `team_members` to check access. At scale, this is the first thing to optimize. Solution: store `team_id` in JWT custom claims (Supabase supports this) so RLS can check `auth.jwt()->'team_id'` instead of running a subquery.

2. **Second bottleneck: Analytics query performance.** Aggregating P&L data across hundreds of promotions with SUM/AVG/GROUP BY will slow down as data grows. Solution: materialized views or nightly summary tables that pre-compute totals per channel, per period.

## Anti-Patterns

### Anti-Pattern 1: Calculating P&L Server-Side Only

**What people do:** Put all P&L calculation in API routes; UI sends inputs, waits for server response to show results.
**Why it's wrong:** Users need instant feedback as they adjust volume estimates. Round-trip latency (even 200ms) makes the P&L worksheet feel sluggish and discourages experimentation.
**Do this instead:** Run the P&L engine as pure functions on the client. Recalculate on every input change. Only hit the server to persist the final result.

### Anti-Pattern 2: Storing Only P&L Results, Not Inputs

**What people do:** Calculate ROI/Uplift and store only the final numbers, discarding the volume decomposition and cost inputs.
**Why it's wrong:** Users cannot review what assumptions went into the calculation. Post-event analysis requires comparing planned inputs vs. actual inputs. Audit trail is lost.
**Do this instead:** Store the full PnlInput alongside the PnlResult. The `promo_pnl` table should have columns for every input field AND every calculated field.

### Anti-Pattern 3: Embedding Team Filtering in Application Code

**What people do:** Write `WHERE team_id = $1` manually in every query function instead of relying on RLS.
**Why it's wrong:** Creates a single-point-of-failure in application code. If any developer forgets the filter, data leaks across tenants. RLS is defense-in-depth that cannot be bypassed by application bugs.
**Do this instead:** The existing RLS policies are correct -- keep them. Application queries should NOT include team_id filters; let RLS handle it. The only exception is when creating a record (you must set team_id on INSERT).

### Anti-Pattern 4: Building Analytics Before P&L Data Exists

**What people do:** Build elaborate dashboards and charts in Phase 1, then struggle because there is no real data to display.
**Why it's wrong:** Dashboards over demo data teach nothing about real UX needs. Users cannot evaluate chart usefulness without their own data.
**Do this instead:** Build Promotion Calendar and P&L worksheet first. Once users have entered 10+ promotions with P&L data, build analytics dashboards in Phase 2 informed by real data patterns.

### Anti-Pattern 5: Over-Complicating Volume Decomposition for Manual Entry

**What people do:** Require users to input all 5 volume effects for every promotion, even for simple "planned" promotions that have not happened yet.
**Why it's wrong:** Most K-beauty brand managers plan promotions without syndicated data. Requiring all 5 volume inputs upfront creates friction and abandonment.
**Do this instead:** Make P&L optional on promotion creation. Allow partial input (just baseline + discount). Progressively unlock full volume decomposition for post-event analysis. Default forward-buying, cannibalization, and competitor volumes to 0 with clear "estimated" labels.

## Integration Points

### External Services

| Service | Integration Pattern | Notes |
|---------|---------------------|-------|
| **Supabase Auth** | SSR client via `@supabase/ssr` | DONE. Browser + server + middleware clients implemented. |
| **Supabase Database** | Direct PostgreSQL via Supabase client | RLS enforces tenant isolation. No ORM needed yet (Drizzle deferred). |
| **Supabase Realtime** | WebSocket subscription (Phase 2) | For multi-user calendar collaboration. Not needed for MVP. |
| **Vercel** | Next.js deployment | Edge middleware for auth. Static generation for marketing pages. |
| **Toss Payments** | Server-side webhook (Phase 3) | Billing for SaaS subscription. Not relevant to TPM architecture. |

### Internal Boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| **Calendar UI <-> Promo Service** | React Query / SWR fetching API routes | Calendar reads promotions by date range. Mutations invalidate calendar cache. |
| **Promotion Detail <-> P&L Engine** | Direct function import (same app) | P&L engine is a lib, not a service. Imported directly by components and API routes. |
| **P&L Engine <-> Database** | API routes only | P&L inputs are persisted via API routes. Engine itself has no database dependency. |
| **Analytics <-> P&L Data** | SQL aggregation queries | Analytics reads from `promo_pnl` table. Never calls the P&L engine directly. Uses pre-stored results. |
| **`packages/types` <-> All apps** | TypeScript imports | Shared type definitions. No runtime boundary. Build-time dependency only. |
| **`packages/utils` <-> All apps** | TypeScript imports | Validation schemas (Zod) and utility functions. No runtime boundary. |

## Database Schema Extensions for P&L

The existing schema handles promotions, products, teams, and channels. The P&L engine requires two new tables.

### New Table: `promo_pnl`

```sql
CREATE TABLE IF NOT EXISTS promo_pnl (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  promotion_id UUID NOT NULL REFERENCES promotions(id) ON DELETE CASCADE,
  team_id UUID NOT NULL REFERENCES teams(id) ON DELETE CASCADE,

  -- Volume decomposition (Simon-Kucher 5 effects)
  baseline_volume INTEGER NOT NULL DEFAULT 0,
  forward_buying_volume INTEGER NOT NULL DEFAULT 0,
  cannibalization_volume INTEGER NOT NULL DEFAULT 0,
  competitor_volume INTEGER NOT NULL DEFAULT 0,
  category_incremental_volume INTEGER NOT NULL DEFAULT 0,

  -- Pricing
  regular_price INTEGER NOT NULL,    -- KRW per unit
  promo_price INTEGER NOT NULL,      -- KRW per unit
  cost_of_goods INTEGER NOT NULL,    -- KRW per unit

  -- Direct costs (KRW)
  slot_fees INTEGER NOT NULL DEFAULT 0,
  display_costs INTEGER NOT NULL DEFAULT 0,
  sample_costs INTEGER NOT NULL DEFAULT 0,
  other_direct_costs INTEGER NOT NULL DEFAULT 0,

  -- Calculated results (stored for fast analytics queries)
  total_promo_volume INTEGER,
  incremental_volume INTEGER,
  gross_revenue BIGINT,
  total_hidden_costs BIGINT,
  total_direct_costs BIGINT,
  total_cogs BIGINT,
  gross_profit BIGINT,
  net_profit BIGINT,
  roi NUMERIC(10, 4),
  uplift NUMERIC(10, 4),
  quadrant VARCHAR(20) CHECK (quadrant IN ('star', 'volume-trap', 'niche-win', 'value-destroyer')),

  -- Metadata
  is_plan BOOLEAN NOT NULL DEFAULT true,  -- true = pre-event plan, false = post-event actual
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_by UUID REFERENCES auth.users(id),

  UNIQUE(promotion_id, is_plan)  -- One plan + one actual per promotion
);
```

### RBAC Permissions Matrix

The existing 4-role system (owner, admin, member, viewer) is appropriate. Here is how it maps to TPM operations:

| Action | Owner | Admin | Member | Viewer |
|--------|-------|-------|--------|--------|
| View calendar | Yes | Yes | Yes | Yes |
| View promotions | Yes | Yes | Yes | Yes |
| Create promotion | Yes | Yes | Yes | No |
| Edit promotion | Yes | Yes | Yes (own) | No |
| Delete promotion | Yes | Yes | No | No |
| View P&L | Yes | Yes | Yes | Yes |
| Edit P&L inputs | Yes | Yes | Yes | No |
| View analytics | Yes | Yes | Yes | Yes |
| Export data | Yes | Yes | Yes | No |
| Manage team members | Yes | Yes | No | No |
| Change team settings | Yes | Yes | No | No |
| Delete team | Yes | No | No | No |
| Manage billing | Yes | No | No | No |

**Note:** "Member" maps to brand managers / e-commerce teams who create and manage their own promotions. "Viewer" maps to executives or finance who need read-only access to the calendar and P&L data.

## Suggested Build Order

Based on component dependencies:

```
Phase 1A: Foundation (Calendar + CRUD)
├── Connect existing Calendar UI to real API
├── Connect existing Promotion CRUD to real API
├── Connect existing Filters to real channel data
├── Products page (needed before P&L)
└── Team management basics

Phase 1B: P&L Engine
├── promo_pnl database migration
├── P&L calculation engine (lib/pnl/)
├── P&L worksheet UI (components/pnl/)
├── Per-promotion P&L page
└── Quadrant badge on promotion cards

Phase 2: Analytics & Reporting
├── Analytics aggregation queries
├── ROI/Uplift scatter plot dashboard
├── P&L waterfall summary
├── Channel comparison charts
└── Post-event vs. plan comparison

Phase 3: Scale & Automation
├── Template system (auto-generate from past promos)
├── Conflict detection (same channel + overlapping dates)
├── Notifications (Slack/Kakao)
├── Bulk import/export
└── AI suggestions (Phase 3+)
```

**Dependency chain:** Products must exist before P&L (need base_price, cost_price). P&L must exist before Analytics (need data to aggregate). Calendar + CRUD must work before anything else (core value proposition).

## Sources

- [Simon-Kucher: How to best measure promotional effectiveness](https://www.simon-kucher.com/en/insights/how-best-measure-promotional-effectiveness-everything-you-need-know-calculating-promotion) -- 5 volume effects, 3 hidden costs, ROI formula (HIGH confidence)
- [Simon-Kucher: Promotion effectiveness in MENA](https://www.simon-kucher.com/en/insights/promotion-effectiveness-mena-how-fix-30-percent-value-destroying-promotions) -- Quadrant evaluation matrix, value-destroyer classification (HIGH confidence)
- [Salesforce Trailhead: Promotion KPIs in TPM](https://trailhead.salesforce.com/content/learn/modules/promotions-setup-in-trade-promotion-management/explore-promotions-kpis) -- P&L waterfall structure, baseline/incremental volume (HIGH confidence)
- [UpClear: Calculate Promotional ROI - 5 Building Blocks](https://upclear.com/calculate-promotional-roi-start-5-key-building-blocks/) -- Base demand, spending categories, financial reconciliation (MEDIUM confidence)
- [Supabase: Row Level Security docs](https://supabase.com/docs/guides/database/postgres/row-level-security) -- RLS patterns for multi-tenant SaaS (HIGH confidence)
- [AntStack: Multi-Tenant Applications with RLS on Supabase](https://www.antstack.com/blog/multi-tenant-applications-with-rls-on-supabase-postgress/) -- Shared tables with tenant_id pattern (MEDIUM confidence)
- [CPGvision: Key Trade Promotion KPIs](https://www.cpgvision.com/blog/trade-promotion-kpis) -- Post-event analysis KPIs, lift factors (MEDIUM confidence)
- [Visualfabriq: Trade promotion ROI in CPG](https://visualfabriq.com/knowledge-hub/how-to-evaluate-trade-promotion-roi-in-the-cpg-industry) -- ROI evaluation framework (MEDIUM confidence)
- [Wikipedia: Trade promotion management](https://en.wikipedia.org/wiki/Trade_promotion_management) -- Domain overview, industry spend benchmarks (HIGH confidence)

---
*Architecture research for: Trade Promotion Management SaaS (PromoHub)*
*Researched: 2026-02-17*
