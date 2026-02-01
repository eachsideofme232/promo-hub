-- Promotions table schema
-- Run this in Supabase SQL editor or as a migration

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Promotions table
CREATE TABLE IF NOT EXISTS promotions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  team_id UUID NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
  channel_id UUID NOT NULL REFERENCES channels(id),
  template_id UUID REFERENCES promo_templates(id),

  title VARCHAR(200) NOT NULL,
  description TEXT,

  status VARCHAR(20) NOT NULL DEFAULT 'planned' CHECK (status IN ('planned', 'active', 'ended', 'cancelled')),
  discount_type VARCHAR(20) NOT NULL CHECK (discount_type IN ('percentage', 'bogo', 'coupon', 'gift', 'bundle')),
  discount_value VARCHAR(50) NOT NULL,

  start_date DATE NOT NULL,
  end_date DATE NOT NULL,

  memo TEXT,

  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_by UUID REFERENCES auth.users(id),

  CONSTRAINT valid_date_range CHECK (end_date >= start_date)
);

-- Indexes
CREATE INDEX idx_promotions_team_id ON promotions(team_id);
CREATE INDEX idx_promotions_channel_id ON promotions(channel_id);
CREATE INDEX idx_promotions_status ON promotions(status);
CREATE INDEX idx_promotions_date_range ON promotions(start_date, end_date);

-- Row Level Security
ALTER TABLE promotions ENABLE ROW LEVEL SECURITY;

-- RLS Policy: Users can only access promotions from their teams
CREATE POLICY "Users can view their team's promotions"
  ON promotions
  FOR SELECT
  USING (
    team_id IN (
      SELECT team_id FROM team_members
      WHERE user_id = auth.uid()
    )
  );

CREATE POLICY "Users can insert promotions to their teams"
  ON promotions
  FOR INSERT
  WITH CHECK (
    team_id IN (
      SELECT team_id FROM team_members
      WHERE user_id = auth.uid()
      AND role IN ('owner', 'admin', 'member')
    )
  );

CREATE POLICY "Users can update their team's promotions"
  ON promotions
  FOR UPDATE
  USING (
    team_id IN (
      SELECT team_id FROM team_members
      WHERE user_id = auth.uid()
      AND role IN ('owner', 'admin', 'member')
    )
  );

CREATE POLICY "Admins can delete their team's promotions"
  ON promotions
  FOR DELETE
  USING (
    team_id IN (
      SELECT team_id FROM team_members
      WHERE user_id = auth.uid()
      AND role IN ('owner', 'admin')
    )
  );

-- Trigger to update updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER promotions_updated_at
  BEFORE UPDATE ON promotions
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();
