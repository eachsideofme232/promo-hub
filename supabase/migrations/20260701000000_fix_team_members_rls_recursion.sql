-- Fix infinite recursion in team_members RLS policies.
--
-- The original policies on team_members referenced team_members in their own
-- USING clause, which Postgres rejects at query time with
-- "infinite recursion detected in policy for relation team_members" (42P17).
-- That error broke every query that touched team membership (i.e. all of them).
--
-- Fix: SECURITY DEFINER helper functions that bypass RLS for the membership
-- lookup, plus a bootstrap RPC for creating a team with its first owner
-- (a brand-new team has no members, so no INSERT policy could otherwise pass).

-- Helper: is the current user a member of the given team?
CREATE OR REPLACE FUNCTION public.is_team_member(check_team_id UUID)
RETURNS BOOLEAN
LANGUAGE sql
SECURITY DEFINER
SET search_path = public
STABLE
AS $$
  SELECT EXISTS (
    SELECT 1 FROM team_members
    WHERE team_id = check_team_id
      AND user_id = auth.uid()
  );
$$;

-- Helper: is the current user an owner/admin of the given team?
CREATE OR REPLACE FUNCTION public.is_team_admin(check_team_id UUID)
RETURNS BOOLEAN
LANGUAGE sql
SECURITY DEFINER
SET search_path = public
STABLE
AS $$
  SELECT EXISTS (
    SELECT 1 FROM team_members
    WHERE team_id = check_team_id
      AND user_id = auth.uid()
      AND role IN ('owner', 'admin')
  );
$$;

REVOKE ALL ON FUNCTION public.is_team_member(UUID) FROM PUBLIC;
REVOKE ALL ON FUNCTION public.is_team_admin(UUID) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION public.is_team_member(UUID) TO authenticated;
GRANT EXECUTE ON FUNCTION public.is_team_admin(UUID) TO authenticated;

-- Replace the recursive team_members policies
DROP POLICY IF EXISTS "Users can view members of their teams" ON team_members;
DROP POLICY IF EXISTS "Team owners/admins can manage members" ON team_members;

CREATE POLICY "Users can view own membership or team members"
  ON team_members
  FOR SELECT
  USING (
    user_id = auth.uid()
    OR public.is_team_member(team_id)
  );

CREATE POLICY "Team owners/admins can insert members"
  ON team_members
  FOR INSERT
  WITH CHECK (public.is_team_admin(team_id));

CREATE POLICY "Team owners/admins can update members"
  ON team_members
  FOR UPDATE
  USING (public.is_team_admin(team_id));

CREATE POLICY "Team owners/admins can delete members"
  ON team_members
  FOR DELETE
  USING (public.is_team_admin(team_id));

-- Bootstrap RPC: create a team and register the caller as its owner.
CREATE OR REPLACE FUNCTION public.create_team_with_owner(team_name TEXT, team_slug TEXT)
RETURNS teams
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  new_team teams;
BEGIN
  IF auth.uid() IS NULL THEN
    RAISE EXCEPTION 'Not authenticated';
  END IF;

  INSERT INTO teams (name, slug)
  VALUES (team_name, team_slug)
  RETURNING * INTO new_team;

  INSERT INTO team_members (team_id, user_id, role)
  VALUES (new_team.id, auth.uid(), 'owner');

  RETURN new_team;
END;
$$;

REVOKE ALL ON FUNCTION public.create_team_with_owner(TEXT, TEXT) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION public.create_team_with_owner(TEXT, TEXT) TO authenticated;
