/*
# Centralized Clubs & Cells Management System - Schema

## Overview
Creates the complete database schema for a college clubs & cells management platform.
Multi-user, role-based application with Supabase email/password auth. Roles: admin,
faculty_coordinator, club_coordinator, student.

## Tables Created
1. profiles — extends auth.users with role, name, phone, department, profile_image, is_active
2. students — student-specific data (register_number, year, section, skills, interests, bio)
3. organizations — clubs and cells with coordinators, category, status
4. memberships — student membership in an organization with status workflow
5. events — events run by an organization with registration capacity
6. event_registrations — student registration for an event (unique per event/student)
7. attendance — attendance record per event/student with status
8. achievements — student achievements with certificate/image, verification
9. announcements — organization announcements with target audience
10. notifications — per-user notifications with read state
11. audit_logs — administrative action audit trail

## Security
- RLS enabled on every table.
- Policies scoped TO authenticated with ownership/role-based predicates.
- Helper functions is_admin(), is_coordinator_of(), is_member_of() defined after all tables.
- Auto-create profile on signup via trigger on auth.users.

## Structure
Tables are created first (with RLS enabled but no policies), then helper functions
(which reference those tables), then all policies (which reference the functions).
*/

-- ============================================================
-- TABLES (all created first, RLS enabled, no policies yet)
-- ============================================================

CREATE TABLE IF NOT EXISTS public.profiles (
  id uuid PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  name text NOT NULL,
  email text NOT NULL,
  role text NOT NULL DEFAULT 'student' CHECK (role IN ('admin','faculty_coordinator','club_coordinator','student')),
  phone text,
  department text,
  profile_image text,
  is_active boolean NOT NULL DEFAULT true,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.students (
  user_id uuid PRIMARY KEY REFERENCES public.profiles(id) ON DELETE CASCADE,
  register_number text UNIQUE,
  department text,
  year integer,
  section text,
  skills text[] DEFAULT '{}',
  interests text[] DEFAULT '{}',
  bio text,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.organizations (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  short_name text,
  type text NOT NULL CHECK (type IN ('club','cell')),
  description text,
  category text,
  logo text,
  cover_image text,
  department text,
  faculty_coordinator_id uuid REFERENCES public.profiles(id) ON DELETE SET NULL,
  student_coordinator_id uuid REFERENCES public.profiles(id) ON DELETE SET NULL,
  contact_email text,
  contact_phone text,
  status text NOT NULL DEFAULT 'active' CHECK (status IN ('active','inactive')),
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.memberships (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  student_id uuid NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  organization_id uuid NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
  role text NOT NULL DEFAULT 'member' CHECK (role IN ('member','core_member','secretary','treasurer','president','vice_president')),
  status text NOT NULL DEFAULT 'pending' CHECK (status IN ('pending','approved','rejected','suspended','left')),
  applied_at timestamptz NOT NULL DEFAULT now(),
  approved_at timestamptz,
  approved_by uuid REFERENCES public.profiles(id) ON DELETE SET NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (student_id, organization_id)
);

CREATE TABLE IF NOT EXISTS public.events (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
  title text NOT NULL,
  description text,
  event_type text DEFAULT 'workshop' CHECK (event_type IN ('workshop','seminar','competition','cultural','technical','social','meeting','other')),
  location text,
  start_date timestamptz,
  end_date timestamptz,
  registration_deadline timestamptz,
  maximum_participants integer,
  banner text,
  status text NOT NULL DEFAULT 'upcoming' CHECK (status IN ('upcoming','ongoing','completed','cancelled')),
  instructions text,
  created_by uuid REFERENCES public.profiles(id) ON DELETE SET NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.event_registrations (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  event_id uuid NOT NULL REFERENCES public.events(id) ON DELETE CASCADE,
  student_id uuid NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  registration_date timestamptz NOT NULL DEFAULT now(),
  participation_status text NOT NULL DEFAULT 'registered' CHECK (participation_status IN ('registered','attended','absent','cancelled')),
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (event_id, student_id)
);

CREATE TABLE IF NOT EXISTS public.attendance (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  event_id uuid NOT NULL REFERENCES public.events(id) ON DELETE CASCADE,
  student_id uuid NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  status text NOT NULL DEFAULT 'absent' CHECK (status IN ('present','absent','late','excused')),
  marked_by uuid REFERENCES public.profiles(id) ON DELETE SET NULL,
  marked_at timestamptz NOT NULL DEFAULT now(),
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (event_id, student_id)
);

CREATE TABLE IF NOT EXISTS public.achievements (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  student_id uuid NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  organization_id uuid REFERENCES public.organizations(id) ON DELETE SET NULL,
  title text NOT NULL,
  description text,
  type text DEFAULT 'competition' CHECK (type IN ('competition','project','certification','workshop','paper_presentation','sports','cultural','other')),
  level text CHECK (level IN ('college','state','national','international')),
  position text,
  achievement_date date,
  certificate text,
  image text,
  verified boolean NOT NULL DEFAULT false,
  verified_by uuid REFERENCES public.profiles(id) ON DELETE SET NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.announcements (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
  title text NOT NULL,
  content text NOT NULL,
  created_by uuid REFERENCES public.profiles(id) ON DELETE SET NULL,
  target_audience text NOT NULL DEFAULT 'all' CHECK (target_audience IN ('all','members','coordinators')),
  publish_date timestamptz NOT NULL DEFAULT now(),
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.notifications (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  title text NOT NULL,
  message text NOT NULL,
  type text NOT NULL DEFAULT 'info' CHECK (type IN ('info','success','warning','error','membership','event','attendance','achievement','announcement')),
  is_read boolean NOT NULL DEFAULT false,
  related_id uuid,
  related_type text,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.audit_logs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES public.profiles(id) ON DELETE SET NULL,
  action text NOT NULL,
  entity_type text,
  entity_id uuid,
  details jsonb,
  created_at timestamptz NOT NULL DEFAULT now()
);

-- ============================================================
-- ENABLE RLS ON ALL TABLES
-- ============================================================

ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.students ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.organizations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.memberships ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.events ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.event_registrations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.attendance ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.achievements ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.announcements ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.audit_logs ENABLE ROW LEVEL SECURITY;

-- ============================================================
-- HELPER FUNCTIONS (after all tables exist)
-- ============================================================

CREATE OR REPLACE FUNCTION public.is_admin()
RETURNS boolean
LANGUAGE sql
SECURITY DEFINER
SET search_path = public
AS $$
  SELECT EXISTS (
    SELECT 1 FROM public.profiles
    WHERE id = auth.uid() AND role = 'admin' AND is_active = true
  );
$$;

CREATE OR REPLACE FUNCTION public.is_coordinator_of(org_id uuid)
RETURNS boolean
LANGUAGE sql
SECURITY DEFINER
SET search_path = public
AS $$
  SELECT EXISTS (
    SELECT 1 FROM public.organizations o
    WHERE o.id = org_id
    AND (o.faculty_coordinator_id = auth.uid() OR o.student_coordinator_id = auth.uid())
  );
$$;

CREATE OR REPLACE FUNCTION public.is_member_of(org_id uuid)
RETURNS boolean
LANGUAGE sql
SECURITY DEFINER
SET search_path = public
AS $$
  SELECT EXISTS (
    SELECT 1 FROM public.memberships m
    WHERE m.organization_id = org_id
    AND m.student_id = auth.uid()
    AND m.status = 'approved'
  );
$$;

-- ============================================================
-- POLICIES: PROFILES
-- ============================================================

DROP POLICY IF EXISTS "profiles_select_all_authenticated" ON public.profiles;
CREATE POLICY "profiles_select_all_authenticated"
ON public.profiles FOR SELECT
TO authenticated USING (true);

DROP POLICY IF EXISTS "profiles_insert_self" ON public.profiles;
CREATE POLICY "profiles_insert_self"
ON public.profiles FOR INSERT
TO authenticated WITH CHECK (auth.uid() = id);

DROP POLICY IF EXISTS "profiles_update_self_or_admin" ON public.profiles;
CREATE POLICY "profiles_update_self_or_admin"
ON public.profiles FOR UPDATE
TO authenticated
USING (auth.uid() = id OR public.is_admin())
WITH CHECK (auth.uid() = id OR public.is_admin());

DROP POLICY IF EXISTS "profiles_delete_admin" ON public.profiles;
CREATE POLICY "profiles_delete_admin"
ON public.profiles FOR DELETE
TO authenticated USING (public.is_admin());

-- ============================================================
-- POLICIES: STUDENTS
-- ============================================================

DROP POLICY IF EXISTS "students_select_authenticated" ON public.students;
CREATE POLICY "students_select_authenticated"
ON public.students FOR SELECT
TO authenticated USING (true);

DROP POLICY IF EXISTS "students_insert_self_or_admin" ON public.students;
CREATE POLICY "students_insert_self_or_admin"
ON public.students FOR INSERT
TO authenticated
WITH CHECK (auth.uid() = user_id OR public.is_admin());

DROP POLICY IF EXISTS "students_update_self_or_admin" ON public.students;
CREATE POLICY "students_update_self_or_admin"
ON public.students FOR UPDATE
TO authenticated
USING (auth.uid() = user_id OR public.is_admin())
WITH CHECK (auth.uid() = user_id OR public.is_admin());

DROP POLICY IF EXISTS "students_delete_admin" ON public.students;
CREATE POLICY "students_delete_admin"
ON public.students FOR DELETE
TO authenticated USING (public.is_admin());

-- ============================================================
-- POLICIES: ORGANIZATIONS
-- ============================================================

DROP POLICY IF EXISTS "orgs_select_authenticated" ON public.organizations;
CREATE POLICY "orgs_select_authenticated"
ON public.organizations FOR SELECT
TO authenticated USING (true);

DROP POLICY IF EXISTS "orgs_insert_admin" ON public.organizations;
CREATE POLICY "orgs_insert_admin"
ON public.organizations FOR INSERT
TO authenticated WITH CHECK (public.is_admin());

DROP POLICY IF EXISTS "orgs_update_admin_or_coordinator" ON public.organizations;
CREATE POLICY "orgs_update_admin_or_coordinator"
ON public.organizations FOR UPDATE
TO authenticated
USING (public.is_admin() OR public.is_coordinator_of(id))
WITH CHECK (public.is_admin() OR public.is_coordinator_of(id));

DROP POLICY IF EXISTS "orgs_delete_admin" ON public.organizations;
CREATE POLICY "orgs_delete_admin"
ON public.organizations FOR DELETE
TO authenticated USING (public.is_admin());

-- ============================================================
-- POLICIES: MEMBERSHIPS
-- ============================================================

DROP POLICY IF EXISTS "memberships_select_authenticated" ON public.memberships;
CREATE POLICY "memberships_select_authenticated"
ON public.memberships FOR SELECT
TO authenticated USING (true);

DROP POLICY IF EXISTS "memberships_insert_self" ON public.memberships;
CREATE POLICY "memberships_insert_self"
ON public.memberships FOR INSERT
TO authenticated
WITH CHECK (auth.uid() = student_id);

DROP POLICY IF EXISTS "memberships_update_self_or_coordinator_or_admin" ON public.memberships;
CREATE POLICY "memberships_update_self_or_coordinator_or_admin"
ON public.memberships FOR UPDATE
TO authenticated
USING (
  auth.uid() = student_id
  OR public.is_admin()
  OR public.is_coordinator_of(organization_id)
)
WITH CHECK (
  auth.uid() = student_id
  OR public.is_admin()
  OR public.is_coordinator_of(organization_id)
);

DROP POLICY IF EXISTS "memberships_delete_admin_or_coordinator" ON public.memberships;
CREATE POLICY "memberships_delete_admin_or_coordinator"
ON public.memberships FOR DELETE
TO authenticated
USING (public.is_admin() OR public.is_coordinator_of(organization_id));

-- ============================================================
-- POLICIES: EVENTS
-- ============================================================

DROP POLICY IF EXISTS "events_select_authenticated" ON public.events;
CREATE POLICY "events_select_authenticated"
ON public.events FOR SELECT
TO authenticated USING (true);

DROP POLICY IF EXISTS "events_insert_coordinator_or_admin" ON public.events;
CREATE POLICY "events_insert_coordinator_or_admin"
ON public.events FOR INSERT
TO authenticated
WITH CHECK (
  public.is_admin()
  OR public.is_coordinator_of(organization_id)
);

DROP POLICY IF EXISTS "events_update_coordinator_or_admin" ON public.events;
CREATE POLICY "events_update_coordinator_or_admin"
ON public.events FOR UPDATE
TO authenticated
USING (
  public.is_admin()
  OR public.is_coordinator_of(organization_id)
)
WITH CHECK (
  public.is_admin()
  OR public.is_coordinator_of(organization_id)
);

DROP POLICY IF EXISTS "events_delete_coordinator_or_admin" ON public.events;
CREATE POLICY "events_delete_coordinator_or_admin"
ON public.events FOR DELETE
TO authenticated
USING (public.is_admin() OR public.is_coordinator_of(organization_id));

-- ============================================================
-- POLICIES: EVENT REGISTRATIONS
-- ============================================================

DROP POLICY IF EXISTS "registrations_select_authenticated" ON public.event_registrations;
CREATE POLICY "registrations_select_authenticated"
ON public.event_registrations FOR SELECT
TO authenticated USING (true);

DROP POLICY IF EXISTS "registrations_insert_self" ON public.event_registrations;
CREATE POLICY "registrations_insert_self"
ON public.event_registrations FOR INSERT
TO authenticated
WITH CHECK (auth.uid() = student_id);

DROP POLICY IF EXISTS "registrations_update_self_or_coordinator_or_admin" ON public.event_registrations;
CREATE POLICY "registrations_update_self_or_coordinator_or_admin"
ON public.event_registrations FOR UPDATE
TO authenticated
USING (
  auth.uid() = student_id
  OR public.is_admin()
  OR EXISTS (
    SELECT 1 FROM public.events e
    WHERE e.id = event_id AND public.is_coordinator_of(e.organization_id)
  )
)
WITH CHECK (
  auth.uid() = student_id
  OR public.is_admin()
  OR EXISTS (
    SELECT 1 FROM public.events e
    WHERE e.id = event_id AND public.is_coordinator_of(e.organization_id)
  )
);

DROP POLICY IF EXISTS "registrations_delete_self_or_coordinator_or_admin" ON public.event_registrations;
CREATE POLICY "registrations_delete_self_or_coordinator_or_admin"
ON public.event_registrations FOR DELETE
TO authenticated
USING (
  auth.uid() = student_id
  OR public.is_admin()
  OR EXISTS (
    SELECT 1 FROM public.events e
    WHERE e.id = event_id AND public.is_coordinator_of(e.organization_id)
  )
);

-- ============================================================
-- POLICIES: ATTENDANCE
-- ============================================================

DROP POLICY IF EXISTS "attendance_select_authenticated" ON public.attendance;
CREATE POLICY "attendance_select_authenticated"
ON public.attendance FOR SELECT
TO authenticated USING (true);

DROP POLICY IF EXISTS "attendance_insert_coordinator_or_admin" ON public.attendance;
CREATE POLICY "attendance_insert_coordinator_or_admin"
ON public.attendance FOR INSERT
TO authenticated
WITH CHECK (
  public.is_admin()
  OR EXISTS (
    SELECT 1 FROM public.events e
    WHERE e.id = event_id AND public.is_coordinator_of(e.organization_id)
  )
);

DROP POLICY IF EXISTS "attendance_update_coordinator_or_admin" ON public.attendance;
CREATE POLICY "attendance_update_coordinator_or_admin"
ON public.attendance FOR UPDATE
TO authenticated
USING (
  public.is_admin()
  OR EXISTS (
    SELECT 1 FROM public.events e
    WHERE e.id = event_id AND public.is_coordinator_of(e.organization_id)
  )
)
WITH CHECK (
  public.is_admin()
  OR EXISTS (
    SELECT 1 FROM public.events e
    WHERE e.id = event_id AND public.is_coordinator_of(e.organization_id)
  )
);

DROP POLICY IF EXISTS "attendance_delete_coordinator_or_admin" ON public.attendance;
CREATE POLICY "attendance_delete_coordinator_or_admin"
ON public.attendance FOR DELETE
TO authenticated
USING (public.is_admin() OR EXISTS (
  SELECT 1 FROM public.events e
  WHERE e.id = event_id AND public.is_coordinator_of(e.organization_id)
));

-- ============================================================
-- POLICIES: ACHIEVEMENTS
-- ============================================================

DROP POLICY IF EXISTS "achievements_select_authenticated" ON public.achievements;
CREATE POLICY "achievements_select_authenticated"
ON public.achievements FOR SELECT
TO authenticated USING (true);

DROP POLICY IF EXISTS "achievements_insert_coordinator_or_admin_or_self" ON public.achievements;
CREATE POLICY "achievements_insert_coordinator_or_admin_or_self"
ON public.achievements FOR INSERT
TO authenticated
WITH CHECK (
  auth.uid() = student_id
  OR public.is_admin()
  OR (organization_id IS NOT NULL AND public.is_coordinator_of(organization_id))
);

DROP POLICY IF EXISTS "achievements_update_coordinator_or_admin_or_self" ON public.achievements;
CREATE POLICY "achievements_update_coordinator_or_admin_or_self"
ON public.achievements FOR UPDATE
TO authenticated
USING (
  auth.uid() = student_id
  OR public.is_admin()
  OR (organization_id IS NOT NULL AND public.is_coordinator_of(organization_id))
)
WITH CHECK (
  auth.uid() = student_id
  OR public.is_admin()
  OR (organization_id IS NOT NULL AND public.is_coordinator_of(organization_id))
);

DROP POLICY IF EXISTS "achievements_delete_admin_or_coordinator_or_self" ON public.achievements;
CREATE POLICY "achievements_delete_admin_or_coordinator_or_self"
ON public.achievements FOR DELETE
TO authenticated
USING (
  auth.uid() = student_id
  OR public.is_admin()
  OR (organization_id IS NOT NULL AND public.is_coordinator_of(organization_id))
);

-- ============================================================
-- POLICIES: ANNOUNCEMENTS
-- ============================================================

DROP POLICY IF EXISTS "announcements_select_authenticated" ON public.announcements;
CREATE POLICY "announcements_select_authenticated"
ON public.announcements FOR SELECT
TO authenticated USING (true);

DROP POLICY IF EXISTS "announcements_insert_coordinator_or_admin" ON public.announcements;
CREATE POLICY "announcements_insert_coordinator_or_admin"
ON public.announcements FOR INSERT
TO authenticated
WITH CHECK (
  public.is_admin()
  OR public.is_coordinator_of(organization_id)
);

DROP POLICY IF EXISTS "announcements_update_coordinator_or_admin" ON public.announcements;
CREATE POLICY "announcements_update_coordinator_or_admin"
ON public.announcements FOR UPDATE
TO authenticated
USING (public.is_admin() OR public.is_coordinator_of(organization_id))
WITH CHECK (public.is_admin() OR public.is_coordinator_of(organization_id));

DROP POLICY IF EXISTS "announcements_delete_coordinator_or_admin" ON public.announcements;
CREATE POLICY "announcements_delete_coordinator_or_admin"
ON public.announcements FOR DELETE
TO authenticated
USING (public.is_admin() OR public.is_coordinator_of(organization_id));

-- ============================================================
-- POLICIES: NOTIFICATIONS
-- ============================================================

DROP POLICY IF EXISTS "notifications_select_self_or_admin" ON public.notifications;
CREATE POLICY "notifications_select_self_or_admin"
ON public.notifications FOR SELECT
TO authenticated
USING (auth.uid() = user_id OR public.is_admin());

DROP POLICY IF EXISTS "notifications_insert_admin_or_system" ON public.notifications;
CREATE POLICY "notifications_insert_admin_or_system"
ON public.notifications FOR INSERT
TO authenticated
WITH CHECK (auth.uid() = user_id OR public.is_admin());

DROP POLICY IF EXISTS "notifications_update_self_or_admin" ON public.notifications;
CREATE POLICY "notifications_update_self_or_admin"
ON public.notifications FOR UPDATE
TO authenticated
USING (auth.uid() = user_id OR public.is_admin())
WITH CHECK (auth.uid() = user_id OR public.is_admin());

DROP POLICY IF EXISTS "notifications_delete_self_or_admin" ON public.notifications;
CREATE POLICY "notifications_delete_self_or_admin"
ON public.notifications FOR DELETE
TO authenticated
USING (auth.uid() = user_id OR public.is_admin());

-- ============================================================
-- POLICIES: AUDIT LOGS
-- ============================================================

DROP POLICY IF EXISTS "audit_logs_select_admin" ON public.audit_logs;
CREATE POLICY "audit_logs_select_admin"
ON public.audit_logs FOR SELECT
TO authenticated USING (public.is_admin());

DROP POLICY IF EXISTS "audit_logs_insert_authenticated" ON public.audit_logs;
CREATE POLICY "audit_logs_insert_authenticated"
ON public.audit_logs FOR INSERT
TO authenticated WITH CHECK (true);

-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_profiles_role ON public.profiles(role);
CREATE INDEX IF NOT EXISTS idx_students_department ON public.students(department);
CREATE INDEX IF NOT EXISTS idx_organizations_type ON public.organizations(type);
CREATE INDEX IF NOT EXISTS idx_organizations_status ON public.organizations(status);
CREATE INDEX IF NOT EXISTS idx_memberships_student ON public.memberships(student_id);
CREATE INDEX IF NOT EXISTS idx_memberships_org ON public.memberships(organization_id);
CREATE INDEX IF NOT EXISTS idx_memberships_status ON public.memberships(status);
CREATE INDEX IF NOT EXISTS idx_events_org ON public.events(organization_id);
CREATE INDEX IF NOT EXISTS idx_events_status ON public.events(status);
CREATE INDEX IF NOT EXISTS idx_events_start_date ON public.events(start_date);
CREATE INDEX IF NOT EXISTS idx_registrations_event ON public.event_registrations(event_id);
CREATE INDEX IF NOT EXISTS idx_registrations_student ON public.event_registrations(student_id);
CREATE INDEX IF NOT EXISTS idx_attendance_event ON public.attendance(event_id);
CREATE INDEX IF NOT EXISTS idx_attendance_student ON public.attendance(student_id);
CREATE INDEX IF NOT EXISTS idx_achievements_student ON public.achievements(student_id);
CREATE INDEX IF NOT EXISTS idx_achievements_org ON public.achievements(organization_id);
CREATE INDEX IF NOT EXISTS idx_announcements_org ON public.announcements(organization_id);
CREATE INDEX IF NOT EXISTS idx_notifications_user ON public.notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_read ON public.notifications(is_read);
CREATE INDEX IF NOT EXISTS idx_audit_logs_user ON public.audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created ON public.audit_logs(created_at);

-- ============================================================
-- UPDATED_AT TRIGGER
-- ============================================================

CREATE OR REPLACE FUNCTION public.handle_updated_at()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS profiles_updated_at ON public.profiles;
CREATE TRIGGER profiles_updated_at BEFORE UPDATE ON public.profiles
  FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

DROP TRIGGER IF EXISTS students_updated_at ON public.students;
CREATE TRIGGER students_updated_at BEFORE UPDATE ON public.students
  FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

DROP TRIGGER IF EXISTS organizations_updated_at ON public.organizations;
CREATE TRIGGER organizations_updated_at BEFORE UPDATE ON public.organizations
  FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

DROP TRIGGER IF EXISTS memberships_updated_at ON public.memberships;
CREATE TRIGGER memberships_updated_at BEFORE UPDATE ON public.memberships
  FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

DROP TRIGGER IF EXISTS events_updated_at ON public.events;
CREATE TRIGGER events_updated_at BEFORE UPDATE ON public.events
  FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

DROP TRIGGER IF EXISTS registrations_updated_at ON public.event_registrations;
CREATE TRIGGER registrations_updated_at BEFORE UPDATE ON public.event_registrations
  FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

DROP TRIGGER IF EXISTS attendance_updated_at ON public.attendance;
CREATE TRIGGER attendance_updated_at BEFORE UPDATE ON public.attendance
  FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

DROP TRIGGER IF EXISTS achievements_updated_at ON public.achievements;
CREATE TRIGGER achievements_updated_at BEFORE UPDATE ON public.achievements
  FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

DROP TRIGGER IF EXISTS announcements_updated_at ON public.announcements;
CREATE TRIGGER announcements_updated_at BEFORE UPDATE ON public.announcements
  FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

-- ============================================================
-- AUTO-CREATE PROFILE ON SIGNUP
-- ============================================================

CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  INSERT INTO public.profiles (id, name, email, role)
  VALUES (
    NEW.id,
    COALESCE(NEW.raw_user_meta_data->>'name', split_part(NEW.email,'@',1)),
    NEW.email,
    COALESCE(NEW.raw_user_meta_data->>'role','student')
  );
  RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();