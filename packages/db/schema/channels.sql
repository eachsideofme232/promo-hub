-- Channels table schema
-- Run this in Supabase SQL editor or as a migration

-- Channels table (reference data)
CREATE TABLE IF NOT EXISTS channels (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(50) NOT NULL,
  slug VARCHAR(50) UNIQUE NOT NULL,
  logo_url TEXT,
  color VARCHAR(20) NOT NULL,
  is_active BOOLEAN NOT NULL DEFAULT true,

  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- No RLS needed for channels - it's reference data accessible to all
-- But we'll still enable it with a permissive policy

ALTER TABLE channels ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Channels are viewable by authenticated users"
  ON channels
  FOR SELECT
  TO authenticated
  USING (true);
