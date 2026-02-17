-- Channel schema extension: team_id for custom channels, promo_types for channel-specific promotion types

-- Add team_id column (nullable: NULL = system/pre-seeded channel, non-NULL = custom team channel)
ALTER TABLE channels ADD COLUMN team_id UUID REFERENCES teams(id) ON DELETE CASCADE;

-- Add promo_types column (JSONB array of supported promotion types per channel)
ALTER TABLE channels ADD COLUMN promo_types JSONB DEFAULT '[]'::jsonb;

-- Drop the existing permissive RLS policy
DROP POLICY "Channels are viewable by authenticated users" ON channels;

-- Create granular RLS policies for system vs custom channels

-- System channels (team_id IS NULL) visible to all authenticated users
CREATE POLICY "System channels visible to all authenticated users"
  ON channels FOR SELECT TO authenticated
  USING (team_id IS NULL);

-- Custom channels visible only to their team members
CREATE POLICY "Custom channels visible to team members"
  ON channels FOR SELECT TO authenticated
  USING (
    team_id IN (
      SELECT tm.team_id FROM team_members tm
      WHERE tm.user_id = auth.uid()
    )
  );

-- Team members (owner/admin/member) can create custom channels
CREATE POLICY "Team members can create custom channels"
  ON channels FOR INSERT TO authenticated
  WITH CHECK (
    team_id IS NOT NULL AND
    team_id IN (
      SELECT tm.team_id FROM team_members tm
      WHERE tm.user_id = auth.uid()
      AND tm.role IN ('owner', 'admin', 'member')
    )
  );

-- Team members (owner/admin/member) can update their custom channels
CREATE POLICY "Team members can update their custom channels"
  ON channels FOR UPDATE TO authenticated
  USING (
    team_id IS NOT NULL AND
    team_id IN (
      SELECT tm.team_id FROM team_members tm
      WHERE tm.user_id = auth.uid()
      AND tm.role IN ('owner', 'admin', 'member')
    )
  );

-- Only admins and owners can delete custom channels
CREATE POLICY "Admins can delete their custom channels"
  ON channels FOR DELETE TO authenticated
  USING (
    team_id IS NOT NULL AND
    team_id IN (
      SELECT tm.team_id FROM team_members tm
      WHERE tm.user_id = auth.uid()
      AND tm.role IN ('owner', 'admin')
    )
  );

-- Index for team_id lookups on custom channels
CREATE INDEX idx_channels_team_id ON channels(team_id) WHERE team_id IS NOT NULL;
