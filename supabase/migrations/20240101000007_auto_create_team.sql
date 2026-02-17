-- Auto-create team on user signup
-- When a user signs up via Supabase Auth, this trigger automatically creates
-- a personal team and adds the user as owner, eliminating the "create your first team" step.

-- Function to handle new user registration
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  new_team_id UUID;
  team_name TEXT;
  team_slug TEXT;
BEGIN
  -- Generate team name from user metadata or email
  team_name := COALESCE(
    NEW.raw_user_meta_data->>'name',
    split_part(NEW.email, '@', 1)
  ) || '의 팀';

  -- Generate unique slug from user UUID (first 8 chars)
  team_slug := 'team-' || substr(NEW.id::text, 1, 8);

  -- Create the team
  INSERT INTO public.teams (name, slug)
  VALUES (team_name, team_slug)
  RETURNING id INTO new_team_id;

  -- Add user as owner
  INSERT INTO public.team_members (team_id, user_id, role)
  VALUES (new_team_id, NEW.id, 'owner');

  RETURN NEW;
EXCEPTION
  WHEN OTHERS THEN
    -- Log error but don't block signup
    RAISE WARNING 'Failed to create team for user %: %', NEW.id, SQLERRM;
    RETURN NEW;
END;
$$;

-- Create trigger on auth.users insert
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW
  EXECUTE FUNCTION public.handle_new_user();
