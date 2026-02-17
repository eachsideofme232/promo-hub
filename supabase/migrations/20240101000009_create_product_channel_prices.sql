-- Product Channel Prices junction table
-- Stores channel-specific pricing for products (e.g., different selling price on OliveYoung vs Coupang)
CREATE TABLE IF NOT EXISTS product_channel_prices (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  channel_id UUID NOT NULL REFERENCES channels(id) ON DELETE CASCADE,

  -- Pricing (KRW, integer for accuracy)
  selling_price INTEGER NOT NULL,
  channel_fee_rate NUMERIC(5,2),  -- percentage, e.g. 30.00 = 30%

  is_active BOOLEAN NOT NULL DEFAULT true,
  notes TEXT,

  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

  -- Each product can only have one price per channel
  UNIQUE(product_id, channel_id)
);

-- Indexes
CREATE INDEX idx_product_channel_prices_product_id ON product_channel_prices(product_id);
CREATE INDEX idx_product_channel_prices_channel_id ON product_channel_prices(channel_id);

-- Row Level Security
ALTER TABLE product_channel_prices ENABLE ROW LEVEL SECURITY;

-- SELECT: authenticated users can view prices for their team's products
CREATE POLICY "Users can view their team's product channel prices"
  ON product_channel_prices
  FOR SELECT
  USING (
    product_id IN (
      SELECT id FROM products
      WHERE team_id IN (
        SELECT team_id FROM team_members
        WHERE user_id = auth.uid()
      )
    )
  );

-- INSERT: team members (owner/admin/member) can insert
CREATE POLICY "Team members can insert product channel prices"
  ON product_channel_prices
  FOR INSERT
  WITH CHECK (
    product_id IN (
      SELECT id FROM products
      WHERE team_id IN (
        SELECT team_id FROM team_members
        WHERE user_id = auth.uid()
        AND role IN ('owner', 'admin', 'member')
      )
    )
  );

-- UPDATE: team members (owner/admin/member) can update
CREATE POLICY "Team members can update product channel prices"
  ON product_channel_prices
  FOR UPDATE
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

-- DELETE: admins (owner/admin) can delete
CREATE POLICY "Admins can delete product channel prices"
  ON product_channel_prices
  FOR DELETE
  USING (
    product_id IN (
      SELECT id FROM products
      WHERE team_id IN (
        SELECT team_id FROM team_members
        WHERE user_id = auth.uid()
        AND role IN ('owner', 'admin')
      )
    )
  );

-- Trigger to update updated_at
CREATE TRIGGER product_channel_prices_updated_at
  BEFORE UPDATE ON product_channel_prices
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();
