# Phase 2: Products & Channels - Research

**Researched:** 2026-02-18
**Domain:** Product/SKU management, channel-specific pricing, CRUD API patterns, form handling with dynamic arrays
**Confidence:** HIGH

## Summary

Phase 2 builds on the Phase 1 foundation (auth, teams, channels, localization) to deliver product catalog management with channel-specific pricing. The requirements are straightforward CRUD: PROD-01 (product management with SKU, COGS, retail price) and PROD-02 (channel-specific pricing per product). The existing codebase already has significant scaffolding -- the `products` table migration exists with RLS policies, query functions in `packages/db/queries/products.ts` are fully implemented, Zod validation schemas for products exist in `packages/utils/src/validation.ts`, and seed data includes 8 demo products. What's missing is the **UI** (no products page exists), the **API routes** (no `/api/products` endpoint), and the **channel-specific pricing table** (the current schema only has `base_price` and `cost_price` on products, with no per-channel pricing mechanism).

The critical architectural decision for Phase 2 is how to model channel-specific pricing. The existing `promo_products` junction table stores per-promotion pricing (`promo_price`), but there is no table for the base channel pricing that PROD-02 requires (e.g., "this product's retail price on OliveYoung is 28,000 KRW, but on Coupang it's 25,000 KRW"). This requires a **new `product_channel_prices` junction table** linking products to channels with pricing fields. This is a standard many-to-many pattern in Supabase/PostgreSQL.

For the UI, the established patterns from Phase 1 (channels page with ChannelList + ChannelForm slide-over panel, react-hook-form + zod, next-intl for Korean strings, toast notifications via sonner, FormattedWon for currency display) should be replicated exactly. The products page will additionally need `useFieldArray` from react-hook-form to manage the dynamic list of channel prices per product.

**Primary recommendation:** Create a `product_channel_prices` junction table via migration, build Product API routes (GET/POST/PATCH/DELETE) following the Channel API route pattern established in Phase 1, build a products page with a table list + slide-over form, and integrate channel-specific pricing as a dynamic field array within the product form.

## Standard Stack

### Core (Phase 2 Specific -- No New Dependencies)

Phase 2 requires **zero new npm dependencies**. Everything needed is already installed from Phase 1:

| Library | Version | Purpose | Already Installed |
|---------|---------|---------|-------------------|
| `react-hook-form` | 7.71.x | Product form management | Yes (Phase 1) |
| `@hookform/resolvers` | 5.2.x | Zod-to-RHF bridge | Yes (Phase 1) |
| `zod` | 3.23.x | Product validation schemas | Yes (existing) |
| `next-intl` | 4.8.x | Korean i18n strings | Yes (Phase 1) |
| `sonner` | 2.0.x | Toast notifications | Yes (Phase 1) |
| `lucide-react` | 0.400.x | Icons for product UI | Yes (existing) |
| `@supabase/ssr` | 0.5.x | Server-side Supabase client | Yes (existing) |
| `date-fns` | 3.6.x | Date formatting | Yes (existing) |

### Supporting (Already Available)

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `@promohub/utils` | workspace | `formatWon()`, `formatKoreanNumber()` | Currency display in product prices |
| `FormattedWon` component | N/A | Korean Won display | Price columns in product list |
| `useTeam` hook | N/A | Team context for API scoping | Every product API call |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Junction table (`product_channel_prices`) | JSONB column on `products` | JSONB is simpler but loses referential integrity, can't JOIN with channels, harder to query "all prices for a channel". Junction table is the correct relational pattern. |
| `useFieldArray` for channel prices | Manual `useState` array management | Manual state works but loses RHF validation, dirty tracking, and error handling per field. `useFieldArray` is the standard RHF pattern for dynamic lists. |
| Slide-over panel form | Full-page form at `/products/new` | Slide-over is established Phase 1 pattern (channels). Consistency is more valuable than routing-based forms at this stage. |
| Single form with embedded channel prices | Separate "manage prices" page per product | Single form is simpler UX. Users see product + all channel prices in one view. Separate page adds navigation complexity for a simple data entry task. |

### Installation

```bash
# No new packages needed. Phase 2 uses only existing dependencies.
```

## Architecture Patterns

### Recommended Project Structure (New Files for Phase 2)

```
apps/web/src/
├── app/
│   ├── (dashboard)/
│   │   └── products/
│   │       └── page.tsx                # NEW - Product list page
│   └── api/
│       └── products/
│           ├── route.ts                # NEW - GET (list) + POST (create)
│           └── [id]/
│               └── route.ts            # NEW - GET (single) + PATCH + DELETE
├── components/
│   └── products/
│       ├── ProductList.tsx             # NEW - Product table with channel prices
│       ├── ProductForm.tsx             # NEW - Slide-over form with channel pricing
│       └── index.ts                    # NEW - Barrel export
supabase/
└── migrations/
    └── 20240101000009_create_product_channel_prices.sql  # NEW - Channel pricing junction table
packages/
├── db/queries/products.ts              # UPDATE - Add channel price queries
└── utils/src/validation.ts             # UPDATE - Add channel price validation schema
apps/web/messages/ko.json               # UPDATE - Add products i18n strings
```

### Pattern 1: Channel-Specific Pricing Junction Table

**What:** A junction table `product_channel_prices` links products to channels with pricing fields. Each row represents "this product costs X on this channel."

**When to use:** PROD-02 requirement -- different pricing per channel for the same product.

**Why junction table over JSONB:** Referential integrity (FK to both products and channels), query-ability (find all products sold on OliveYoung), indexability, and RLS can be applied to the junction table itself.

**Confidence:** HIGH -- standard relational many-to-many pattern verified via Supabase docs.

```sql
-- Source: Standard PostgreSQL many-to-many pattern + Supabase RLS docs
-- File: supabase/migrations/20240101000009_create_product_channel_prices.sql

CREATE TABLE IF NOT EXISTS product_channel_prices (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  channel_id UUID NOT NULL REFERENCES channels(id) ON DELETE CASCADE,

  -- Pricing (in KRW, stored as integer for accuracy)
  selling_price INTEGER NOT NULL,         -- Retail/selling price on this channel
  channel_fee_rate NUMERIC(5,2),          -- Channel commission rate (e.g., 30.00 for 30%)

  -- Metadata
  is_active BOOLEAN NOT NULL DEFAULT true,
  notes TEXT,

  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

  -- One price per product per channel
  UNIQUE(product_id, channel_id)
);

-- Indexes
CREATE INDEX idx_product_channel_prices_product_id ON product_channel_prices(product_id);
CREATE INDEX idx_product_channel_prices_channel_id ON product_channel_prices(channel_id);

-- RLS (inherits access from products table -- same team scoping)
ALTER TABLE product_channel_prices ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view channel prices for their team's products"
  ON product_channel_prices FOR SELECT TO authenticated
  USING (
    product_id IN (
      SELECT id FROM products
      WHERE team_id IN (
        SELECT team_id FROM team_members
        WHERE user_id = auth.uid()
      )
    )
  );

CREATE POLICY "Team members can manage channel prices"
  ON product_channel_prices FOR ALL TO authenticated
  USING (
    product_id IN (
      SELECT id FROM products
      WHERE team_id IN (
        SELECT team_id FROM team_members
        WHERE user_id = auth.uid()
        AND role IN ('owner', 'admin', 'member')
      )
    )
  );

-- Auto-update updated_at
CREATE TRIGGER product_channel_prices_updated_at
  BEFORE UPDATE ON product_channel_prices
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();
```

**Column decisions:**
- `selling_price INTEGER NOT NULL` -- KRW stored as integer (no floating point). This is the price the consumer pays on that channel.
- `channel_fee_rate NUMERIC(5,2)` -- Optional. The commission percentage the channel takes. Useful for P&L calculations in Phase 6. Stored as decimal (e.g., 30.00 = 30%). `NUMERIC(5,2)` allows up to 999.99%.
- `is_active BOOLEAN` -- Whether this product is currently listed on this channel.
- `notes TEXT` -- Free-form notes (e.g., "Only during promotions", "Exclusive to rocket delivery").

**What's NOT included (deferred):**
- `min_price` / `max_price` (price monitoring, Phase 3+)
- `url` (channel product listing URL, not needed for v1)
- `channel_sku` (channel-specific SKU code, could add later if needed)

### Pattern 2: Product API Routes (Following Channel API Pattern)

**What:** REST API routes for product CRUD, following the exact pattern established by the Channel API in Phase 1.

**When to use:** All product operations from the frontend.

**Confidence:** HIGH -- identical pattern to working Channel API routes.

```typescript
// apps/web/src/app/api/products/route.ts
// Source: Phase 1 Channel API pattern (apps/web/src/app/api/channels/route.ts)
import { createClient } from '@/lib/supabase/server'
import { NextRequest, NextResponse } from 'next/server'
import { z } from 'zod'

const createProductSchema = z.object({
  name: z.string().min(1).max(200).trim(),
  sku: z.string().min(1).max(50).trim(),
  barcode: z.string().max(50).trim().optional(),
  brand: z.string().max(100).trim().optional(),
  category: z.string().max(100).trim().optional(),
  description: z.string().max(2000).optional(),
  basePrice: z.number().int().min(0),
  costPrice: z.number().int().min(0).optional(),
  channelPrices: z.array(z.object({
    channelId: z.string().uuid(),
    sellingPrice: z.number().int().min(0),
    channelFeeRate: z.number().min(0).max(100).optional(),
    isActive: z.boolean().optional(),
  })).optional().default([]),
})

export async function GET() {
  const supabase = await createClient()

  // 1. Auth check
  const { data: { user }, error: authError } = await supabase.auth.getUser()
  if (authError || !user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  // 2. Team membership
  const { data: membership } = await supabase
    .from('team_members')
    .select('team_id')
    .eq('user_id', user.id)
    .limit(1)
    .single()

  if (!membership) {
    return NextResponse.json({ error: 'No team found' }, { status: 403 })
  }

  // 3. Fetch products with channel prices
  const { data, error } = await supabase
    .from('products')
    .select(`
      *,
      product_channel_prices(
        id, channel_id, selling_price, channel_fee_rate, is_active, notes
      )
    `)
    .eq('team_id', membership.team_id)
    .order('name')

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }

  // 4. Map snake_case to camelCase
  const products = (data ?? []).map(mapProductResponse)
  return NextResponse.json({ data: products })
}
```

**Key pattern notes:**
- Supabase auto-detects the foreign key relationship between `products` and `product_channel_prices` for nested selects
- Channel prices are embedded in the product response (no separate API call needed)
- The create endpoint handles product + channel prices in a single request (insert product, then insert channel prices with the new product ID)

### Pattern 3: Product Form with Dynamic Channel Prices (useFieldArray)

**What:** Product creation/edit form with a dynamic list of channel-specific prices using `useFieldArray` from react-hook-form.

**When to use:** ProductForm component for create and edit.

**Confidence:** HIGH -- `useFieldArray` is the standard react-hook-form pattern for dynamic lists. Verified via Context7 docs.

```typescript
// Source: Context7 react-hook-form docs (useFieldArray)
// apps/web/src/components/products/ProductForm.tsx (key excerpt)

import { useForm, useFieldArray } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'

// Form type includes channel prices array
type ProductFormValues = {
  name: string
  sku: string
  basePrice: number
  costPrice?: number
  // ... other fields
  channelPrices: {
    channelId: string
    sellingPrice: number
    channelFeeRate?: number
    isActive: boolean
  }[]
}

function ProductForm({ channels, product, onSubmit }) {
  const { control, register, handleSubmit } = useForm<ProductFormValues>({
    resolver: zodResolver(productFormSchema),
    defaultValues: {
      // ... product defaults
      channelPrices: product?.channelPrices ?? [],
    },
  })

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'channelPrices',
  })

  // Channels not yet added to this product
  const availableChannels = channels.filter(
    ch => !fields.some(f => f.channelId === ch.id)
  )

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* ... product fields ... */}

      {/* Channel Prices Section */}
      <h3>채널별 판매가</h3>
      {fields.map((field, index) => (
        <div key={field.id}>
          {/* Channel name (read-only display) */}
          <span>{channels.find(c => c.id === field.channelId)?.name}</span>

          {/* Selling price */}
          <input
            {...register(`channelPrices.${index}.sellingPrice`, { valueAsNumber: true })}
            type="number"
          />

          {/* Channel fee rate */}
          <input
            {...register(`channelPrices.${index}.channelFeeRate`, { valueAsNumber: true })}
            type="number"
            step="0.01"
          />

          {/* Remove button */}
          <button type="button" onClick={() => remove(index)}>삭제</button>
        </div>
      ))}

      {/* Add channel price button */}
      {availableChannels.length > 0 && (
        <button type="button" onClick={() => {/* show channel picker */}}>
          채널 추가
        </button>
      )}
    </form>
  )
}
```

**Key UX decisions:**
- Channel prices are managed inline within the product form (not a separate page)
- Users add channels one at a time from a dropdown of available channels
- Each channel price row shows: channel name (color dot), selling price input, fee rate input, remove button
- The form fetches the channel list from the existing `/api/channels` endpoint
- `IMPORTANT: Use field.id as key, not index` -- per react-hook-form docs

### Pattern 4: Product List with Expandable Channel Prices

**What:** Table-based product list showing core product info (name, SKU, base price, COGS) with expandable rows to show per-channel pricing.

**When to use:** Main products page.

```
Desktop Layout:
┌──────────────┬────────┬──────────┬──────────┬───────────┬────────┐
│ 상품명        │ SKU    │ 소비자가  │ 원가     │ 채널 수    │ 관리   │
├──────────────┼────────┼──────────┼──────────┼───────────┼────────┤
│ 비타민C 세럼  │ BK-001 │ 45,000원 │ 12,000원 │ 3개 채널  │ ✏️ 🗑️ │
│  └─ 올리브영  │        │ 42,000원 │ 30%      │           │        │
│  └─ 쿠팡     │        │ 39,000원 │ 25%      │           │        │
│  └─ 네이버   │        │ 44,000원 │ 15%      │           │        │
├──────────────┼────────┼──────────┼──────────┼───────────┼────────┤
│ 수분 크림     │ BK-002 │ 38,000원 │ 10,000원 │ 2개 채널  │ ✏️ 🗑️ │
└──────────────┴────────┴──────────┴──────────┴───────────┴────────┘
```

**Why expandable rows:** The primary view shows product-level data. Channel pricing is important but secondary. Showing all prices for all channels in the main row would create too many columns (8+ channels). Expandable/collapsible rows keep the list scannable while allowing drill-down.

### Anti-Patterns to Avoid

- **Storing prices as floats:** KRW has no decimals. Use `INTEGER` for all KRW amounts. The existing codebase correctly uses `INTEGER` for `base_price` and `cost_price`. Continue this pattern for `selling_price`.

- **Channel fee rate as integer:** Unlike KRW amounts, commission rates need decimal precision (e.g., 12.5%). Use `NUMERIC(5,2)` not `INTEGER` for `channel_fee_rate`.

- **Separate API calls for product + channel prices:** Don't fetch product data and then make N additional calls for each channel price. Use Supabase's nested select (`products(*, product_channel_prices(*))`) to get everything in one query.

- **Duplicate validation schemas:** The existing `productSchema` in `packages/utils/src/validation.ts` needs updating (currently requires `teamId` in the schema, which should come from auth context, not from the form). Don't create a second schema -- update the existing one.

- **Forgetting to pass `valueAsNumber: true`:** react-hook-form registers inputs as strings by default. All price and rate inputs must use `{ valueAsNumber: true }` to avoid sending "45000" (string) instead of 45000 (number) to the API.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Dynamic form field arrays | Manual `useState` + `map` for channel prices | `useFieldArray` from react-hook-form | Handles add/remove/reorder with proper key management, validation per-item, and dirty state tracking. Manual approach loses all of this. |
| Currency display in product list | Inline number formatting | `<FormattedWon>` component | Already built in Phase 1. Handles both compact (15만원) and full (150,000원) formats. |
| Korean i18n strings | Hardcoded Korean text in components | `useTranslations('products')` from next-intl | Established pattern. All Phase 1 pages use this. |
| Product validation | Inline checks in API routes | Zod schemas from `@promohub/utils` | Existing `productSchema` covers most fields. Extend it for channel prices. |
| Auth + team context in API | Custom auth middleware | Phase 1 helper pattern (`getAuthContext`) | Already implemented in `apps/web/src/app/api/channels/[id]/route.ts`. Reuse for products. |
| Toast notifications | Custom notification system | `toast.success()` / `toast.error()` from sonner | Already installed and used in channels page. |

**Key insight:** Phase 2 is primarily about applying Phase 1 patterns to a new domain (products instead of channels). The architecture, libraries, and UI patterns are all established. The only net-new concept is the channel-pricing junction table and the `useFieldArray` pattern for the form.

## Common Pitfalls

### Pitfall 1: Product Creation Requires Two-Step Insert (Product + Channel Prices)

**What goes wrong:** Inserting a product with channel prices in a single Supabase call fails because `product_channel_prices` needs the product `id` as a foreign key, but the product doesn't exist yet.

**Why it happens:** Supabase's `.insert()` doesn't support nested inserts (inserting a parent and children in one call). You must insert the product first, get its ID, then insert channel prices.

**How to avoid:**
1. Insert the product first with `.insert().select().single()` to get the new `id`
2. Then bulk-insert channel prices with that `product_id`
3. If channel price insertion fails, you have an orphaned product (but it's still valid -- just has no channel prices)
4. Consider wrapping in a Supabase RPC function if atomicity is critical (for v1, two sequential inserts are acceptable)

**Warning signs:** Channel prices silently fail to save while the product itself appears saved. The product shows "0 channels" even though the user added prices.

### Pitfall 2: Existing `productSchema` in validation.ts Has teamId as Required Field

**What goes wrong:** The form tries to validate `teamId` from user input, but `teamId` should come from the auth context (TeamProvider), not from the form.

**Why it happens:** The existing schema was written with the assumption that `teamId` would be part of the form data. In the Phase 1 pattern, `teamId` is injected server-side from the user's team membership.

**How to avoid:**
1. Create a separate `productFormSchema` (client-side, without `teamId`) and `createProductApiSchema` (server-side, with `teamId` injected)
2. Or: make `teamId` optional in the form schema and require it in the API schema
3. Follow the channel pattern: the channel form doesn't include `teamId` -- it's injected by the API route

**Warning signs:** Form validation fails immediately because `teamId` is undefined.

### Pitfall 3: Channel Prices Form Doesn't Know Available Channels

**What goes wrong:** The product form can't show a "add channel" dropdown because it doesn't have the channel list.

**Why it happens:** The ProductForm component needs the channel list to (a) show channel names next to prices and (b) offer an "add channel" picker. This data must be fetched before the form renders.

**How to avoid:**
1. The products page fetches channels from `/api/channels` on mount (same as the channels page does)
2. Pass the channel list as a prop to `ProductForm`
3. Or: create a `useChannels` hook that fetches and caches the channel list

**Warning signs:** Product form shows channel UUIDs instead of names, or the "add channel" dropdown is empty.

### Pitfall 4: NUMERIC(5,2) vs INTEGER Confusion for Fee Rates

**What goes wrong:** Channel fee rates are stored as integers (e.g., 30 for 30%), but the P&L engine in Phase 6 expects decimals (0.30). Or: fee rates with decimals (12.5%) are truncated to integers (12%).

**Why it happens:** The existing codebase uses `INTEGER` for all monetary amounts (correct for KRW). Developers might apply the same pattern to percentage rates.

**How to avoid:**
1. Use `NUMERIC(5,2)` for `channel_fee_rate` in the migration
2. Store as percentage points (30.00 = 30%), not as decimals (0.30)
3. Document the convention in the schema comment
4. Use `z.number().min(0).max(100)` in Zod validation (not `.int()`)
5. In the form, use `step="0.01"` on the input

**Warning signs:** Fee rates like 12.5% appear as 12% or 13% in the database.

### Pitfall 5: Supabase Nested Select Returns Different Shape for Empty Relations

**What goes wrong:** When a product has no channel prices, `product_channel_prices` in the nested select returns `[]` (empty array). But when building the response mapper, developers might not handle this case, causing undefined errors.

**Why it happens:** Supabase returns `[]` for empty relations in nested selects, which is correct but can trip up TypeScript code that destructures without checking.

**How to avoid:**
1. Always default to `[]`: `const channelPrices = row.product_channel_prices ?? []`
2. Type the response correctly: `product_channel_prices: ChannelPriceRow[] | null`
3. The mapper function should handle both null and empty array

**Warning signs:** Products without channel prices cause TypeScript errors or show "undefined" in the UI.

## Code Examples

### Migration: Create product_channel_prices Table

```sql
-- Source: Standard PostgreSQL many-to-many + Supabase RLS patterns
-- File: supabase/migrations/20240101000009_create_product_channel_prices.sql

CREATE TABLE IF NOT EXISTS product_channel_prices (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  channel_id UUID NOT NULL REFERENCES channels(id) ON DELETE CASCADE,
  selling_price INTEGER NOT NULL,                   -- KRW retail price on this channel
  channel_fee_rate NUMERIC(5,2),                    -- Commission % (e.g., 30.00 = 30%)
  is_active BOOLEAN NOT NULL DEFAULT true,
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(product_id, channel_id)
);

CREATE INDEX idx_pcp_product_id ON product_channel_prices(product_id);
CREATE INDEX idx_pcp_channel_id ON product_channel_prices(channel_id);

ALTER TABLE product_channel_prices ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their team's product channel prices"
  ON product_channel_prices FOR SELECT TO authenticated
  USING (
    product_id IN (
      SELECT id FROM products WHERE team_id IN (
        SELECT team_id FROM team_members WHERE user_id = auth.uid()
      )
    )
  );

CREATE POLICY "Team members can insert product channel prices"
  ON product_channel_prices FOR INSERT TO authenticated
  WITH CHECK (
    product_id IN (
      SELECT id FROM products WHERE team_id IN (
        SELECT team_id FROM team_members
        WHERE user_id = auth.uid() AND role IN ('owner', 'admin', 'member')
      )
    )
  );

CREATE POLICY "Team members can update product channel prices"
  ON product_channel_prices FOR UPDATE TO authenticated
  USING (
    product_id IN (
      SELECT id FROM products WHERE team_id IN (
        SELECT team_id FROM team_members
        WHERE user_id = auth.uid() AND role IN ('owner', 'admin', 'member')
      )
    )
  );

CREATE POLICY "Admins can delete product channel prices"
  ON product_channel_prices FOR DELETE TO authenticated
  USING (
    product_id IN (
      SELECT id FROM products WHERE team_id IN (
        SELECT team_id FROM team_members
        WHERE user_id = auth.uid() AND role IN ('owner', 'admin')
      )
    )
  );

CREATE TRIGGER product_channel_prices_updated_at
  BEFORE UPDATE ON product_channel_prices
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();
```

### Supabase Nested Select for Products with Channel Prices

```typescript
// Source: Context7 Supabase docs (joins-and-nesting, select with relations)
// Fetches products with their channel prices in a single query

const { data, error } = await supabase
  .from('products')
  .select(`
    *,
    product_channel_prices(
      id,
      channel_id,
      selling_price,
      channel_fee_rate,
      is_active,
      notes
    )
  `)
  .eq('team_id', teamId)
  .order('name')
```

### Product + Channel Prices Two-Step Insert

```typescript
// Source: Context7 Supabase JS docs (insert operations)
// Insert product first, then channel prices

// Step 1: Insert product
const { data: product, error: productError } = await supabase
  .from('products')
  .insert({
    team_id: teamId,
    name: parsed.data.name,
    sku: parsed.data.sku,
    base_price: parsed.data.basePrice,
    cost_price: parsed.data.costPrice ?? null,
    // ... other fields
  })
  .select()
  .single()

if (productError) {
  return NextResponse.json({ error: productError.message }, { status: 500 })
}

// Step 2: Insert channel prices (if any)
if (parsed.data.channelPrices.length > 0) {
  const channelPriceRows = parsed.data.channelPrices.map(cp => ({
    product_id: product.id,
    channel_id: cp.channelId,
    selling_price: cp.sellingPrice,
    channel_fee_rate: cp.channelFeeRate ?? null,
    is_active: cp.isActive ?? true,
  }))

  const { error: priceError } = await supabase
    .from('product_channel_prices')
    .insert(channelPriceRows)

  if (priceError) {
    // Product was created but prices failed. Log warning, don't delete product.
    console.error('Channel price insert failed:', priceError.message)
  }
}
```

### Upsert Pattern for Updating Channel Prices

```typescript
// Source: Context7 Supabase JS docs (upsert operations)
// When editing a product, channel prices may be added, updated, or removed

// Step 1: Delete existing channel prices for this product
await supabase
  .from('product_channel_prices')
  .delete()
  .eq('product_id', productId)

// Step 2: Insert the new set of channel prices
if (channelPrices.length > 0) {
  await supabase
    .from('product_channel_prices')
    .insert(channelPrices.map(cp => ({
      product_id: productId,
      channel_id: cp.channelId,
      selling_price: cp.sellingPrice,
      channel_fee_rate: cp.channelFeeRate ?? null,
      is_active: cp.isActive ?? true,
    })))
}

// Alternative: Use upsert with onConflict
await supabase
  .from('product_channel_prices')
  .upsert(
    channelPrices.map(cp => ({
      product_id: productId,
      channel_id: cp.channelId,
      selling_price: cp.sellingPrice,
      channel_fee_rate: cp.channelFeeRate ?? null,
    })),
    { onConflict: 'product_id,channel_id' }
  )
```

### Zod Schema for Product with Channel Prices

```typescript
// Extends existing productSchema from packages/utils/src/validation.ts

// Client-side form schema (no teamId -- injected server-side)
export const productFormSchema = z.object({
  name: z.string().min(1, '상품명을 입력해주세요').max(200, '200자 이내로 입력해주세요'),
  sku: z.string().min(1, 'SKU 코드를 입력해주세요').max(50, '50자 이내로 입력해주세요'),
  barcode: z.string().max(50).optional().or(z.literal('')),
  brand: z.string().max(100).optional().or(z.literal('')),
  category: z.string().max(100).optional().or(z.literal('')),
  description: z.string().max(2000).optional().or(z.literal('')),
  basePrice: z.number().int().min(0, '0 이상의 금액을 입력해주세요'),
  costPrice: z.number().int().min(0, '0 이상의 금액을 입력해주세요').optional(),
  imageUrl: z.string().url('올바른 URL을 입력해주세요').optional().or(z.literal('')),
  channelPrices: z.array(z.object({
    channelId: z.string().uuid(),
    sellingPrice: z.number().int().min(0, '0 이상의 금액을 입력해주세요'),
    channelFeeRate: z.number().min(0).max(100, '수수료율은 100% 이하여야 합니다').optional(),
    isActive: z.boolean().default(true),
  })).default([]),
})

export type ProductFormData = z.infer<typeof productFormSchema>
```

### Korean i18n Strings for Products

```json
{
  "products": {
    "title": "상품 관리",
    "addProduct": "상품 추가",
    "editProduct": "상품 수정",
    "deleteProduct": "상품 삭제",
    "name": "상품명",
    "sku": "SKU 코드",
    "barcode": "바코드",
    "brand": "브랜드",
    "category": "카테고리",
    "description": "설명",
    "basePrice": "소비자가",
    "costPrice": "원가 (COGS)",
    "channelPrices": "채널별 판매가",
    "sellingPrice": "판매가",
    "channelFeeRate": "수수료율",
    "addChannelPrice": "채널 추가",
    "selectChannel": "채널 선택",
    "noProducts": "등록된 상품이 없습니다",
    "channelCount": "{count}개 채널",
    "confirmDelete": "이 상품을 삭제하시겠습니까?",
    "confirmDeleteDesc": "삭제된 상품은 복구할 수 없습니다. 관련된 채널별 가격도 함께 삭제됩니다.",
    "createSuccess": "상품이 추가되었습니다",
    "updateSuccess": "상품이 수정되었습니다",
    "deleteSuccess": "상품이 삭제되었습니다",
    "createError": "상품 추가에 실패했습니다",
    "updateError": "상품 수정에 실패했습니다",
    "deleteError": "상품 삭제에 실패했습니다",
    "loadError": "상품 목록을 불러오지 못했습니다",
    "save": "저장",
    "cancel": "취소",
    "active": "활성",
    "inactive": "비활성",
    "status": "상태",
    "actions": "관리",
    "search": "상품 검색",
    "filter": "필터",
    "allBrands": "전체 브랜드",
    "allCategories": "전체 카테고리",
    "totalProducts": "전체 상품",
    "activeProducts": "활성 상품",
    "avgPrice": "평균 판매가"
  }
}
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `uuid_generate_v4()` | `gen_random_uuid()` | PostgreSQL 13+ | Already updated in all existing migrations. New migration must also use `gen_random_uuid()`. |
| Separate SELECT + FOR ALL RLS | Separate SELECT + INSERT + UPDATE + DELETE policies | Supabase best practice | The existing `promo_products` uses a single `FOR ALL` policy. The product RLS correctly uses separate per-operation policies. New `product_channel_prices` should follow the per-operation pattern for clearer security. |
| Manual form state (`useState`) | react-hook-form + zod resolver | Phase 1 adoption | All Phase 1 forms use RHF. Phase 2 must follow this pattern. |
| Hardcoded Korean strings | next-intl `useTranslations()` | Phase 1 adoption | All user-facing strings must use the i18n pattern. |

**Deprecated/outdated in existing code:**
- The `packages/db/queries/products.ts` has its own `Product` interface and `ProductRow` interface. These are separate from `@promohub/types`. For consistency, the types should eventually be unified, but for Phase 2 the pragmatic approach is to extend `packages/db/queries/products.ts` with channel price support and use those types in the API routes. Unification can happen in a future cleanup.
- The existing `productSchema` in `validation.ts` includes `teamId` as a required field. This needs to be split into form-side and server-side schemas.

## Open Questions

1. **Should the product form support image upload?**
   - What we know: The products table has an `image_url` column. The seed data leaves it NULL. No Supabase Storage bucket is configured.
   - What's unclear: Is image upload a Phase 2 requirement or can it be deferred?
   - Recommendation: Defer image upload. Accept `image_url` as a text input (paste a URL) for now. Setting up Supabase Storage for file uploads is scope creep for a product catalog feature. Add a placeholder image when `image_url` is null.

2. **Should channel fee rates be required or optional?**
   - What we know: Channel fee rates are needed for P&L calculations in Phase 6. Not all users may know their channel's commission rate when first entering products.
   - What's unclear: Will missing fee rates cause problems in Phase 6?
   - Recommendation: Make `channel_fee_rate` optional (nullable). Users can fill it in later. Phase 6 P&L calculations should handle missing rates gracefully (show "N/A" or prompt user to fill in).

3. **Product bulk import from Excel/CSV?**
   - What we know: The existing validation.ts has a `productBulkImportSchema` for up to 1000 products. K-beauty companies may have hundreds of SKUs.
   - What's unclear: Is bulk import a Phase 2 requirement?
   - Recommendation: Defer bulk import. Manual single-product entry is the v1 requirement (aligned with "manual data entry first" decision). Bulk import can be added as a Phase 2.1 insertion if needed.

4. **Seed data for product_channel_prices?**
   - What we know: The seed data has 8 products but no channel pricing data. The existing `promo_products` seed has per-promotion prices but not per-channel base prices.
   - What's unclear: Should the seed file be updated with channel pricing for the demo products?
   - Recommendation: Yes, add seed data for `product_channel_prices`. It helps during development and demo. Assign 3-5 channels per demo product with realistic K-beauty price points.

## Sources

### Primary (HIGH confidence)
- Context7 `/supabase/supabase` -- Many-to-many junction table patterns, RLS policies for join tables, nested select queries
- Context7 `/supabase/supabase-js` -- Insert, upsert, select with relations, update operations
- Context7 `/react-hook-form/documentation` -- `useFieldArray` API, Zod resolver integration, dynamic form arrays
- Existing codebase analysis:
  - `supabase/migrations/20240101000003_create_products.sql` -- Current products schema
  - `packages/db/queries/products.ts` -- Existing product CRUD queries
  - `packages/utils/src/validation.ts` -- Existing product validation schema
  - `apps/web/src/app/api/channels/route.ts` -- Phase 1 API route pattern
  - `apps/web/src/app/api/channels/[id]/route.ts` -- Phase 1 helper functions pattern
  - `apps/web/src/app/(dashboard)/channels/page.tsx` -- Phase 1 page pattern
  - `apps/web/src/components/channels/` -- Phase 1 component patterns (ChannelList, ChannelForm)

### Secondary (MEDIUM confidence)
- [Supabase Joins & Nesting docs](https://supabase.com/docs/guides/database/joins-and-nesting) -- Automatic join detection for foreign keys
- [Supabase RLS Performance docs](https://supabase.com/docs/guides/database/postgres/row-level-security) -- IN operator pattern for team-scoped policies

### Tertiary (LOW confidence)
- None. All findings verified against primary or secondary sources.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- Zero new dependencies. All libraries already installed and patterns established in Phase 1.
- Architecture: HIGH -- Junction table for channel pricing is a standard relational pattern. Supabase nested selects verified in Context7. API route pattern is copy of working Phase 1 code.
- Pitfalls: HIGH -- Two-step insert requirement verified against Supabase JS docs (no nested insert support). NUMERIC vs INTEGER for rates is a known PostgreSQL pattern. Schema split (form vs API) is directly observed in existing code.
- UI patterns: HIGH -- Product page follows exact same structure as channels page. `useFieldArray` verified in Context7 react-hook-form docs.

**Research date:** 2026-02-18
**Valid until:** 2026-03-18 (stable domain, 30-day validity)
