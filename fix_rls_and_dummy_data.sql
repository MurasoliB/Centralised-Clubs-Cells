-- ====================================================================
-- KONGU ENGINEERING COLLEGE (KEC) - CLUBS & CELLS MANAGEMENT SYSTEM
-- MASTER RLS UNBLOCK & DUMMY DATA SYNC SCRIPT
-- ====================================================================

-- 1. UNBLOCK ROW LEVEL SECURITY (RLS) POLICIES FOR FRONTEND CLIENT
-- This allows both authenticated and anonymous institutional connections to select, insert, and update
DO $$
DECLARE
  tbl text;
BEGIN
  FOR tbl IN SELECT tablename FROM pg_tables WHERE schemaname = 'public' LOOP
    EXECUTE format('ALTER TABLE public.%I DISABLE ROW LEVEL SECURITY;', tbl);
  END LOOP;
END $$;

-- 2. INSERT CORE INSTITUTIONAL PROFILES
INSERT INTO public.profiles (id, email, name, role, department, is_active, created_at, updated_at) VALUES
('a1b2c3d4-0001-4000-8000-000000000001', 'student@college.edu', 'Praveen Kumar', 'student', 'Information Technology', true, now(), now()),
('a1b2c3d4-0002-4000-8000-000000000002', 'coordinator@college.edu', 'Ananya Sharma', 'club_coordinator', 'Information Technology', true, now(), now()),
('a1b2c3d4-0003-4000-8000-000000000003', 'faculty@college.edu', 'Dr. S. K. Sakthivel', 'faculty_coordinator', 'Information Technology', true, now(), now()),
('a1b2c3d4-0004-4000-8000-000000000004', 'admin@college.edu', 'Dr. Rajesh Kumar', 'admin', 'Administration', true, now(), now()),
('423f05db-e3bc-4b3c-8cf2-29fc30f54ff3', 'vigneshm@gmail.com', 'VIGNESH M', 'student', 'Information Technology', true, now(), now()),
('e57a8a0b-1934-406a-810a-3c24b94f6e0b', 'balajimurasoli@gmail.com', 'MURASOLI B', 'student', 'Information Technology', true, now(), now()),
('cb0980cf-c3a5-420a-9d22-19e487102604', 'sahana@gmail.com', 'SAHANA S', 'student', 'Information Technology', true, now(), now()),
('c0678fc7-60a6-42d8-8255-7dae37a34aa6', 'sarankarthik@gmail.com', 'SARAN KARTHIK S', 'student', 'Information Technology', true, now(), now()),
('a1b2c3d4-0005-4000-8000-000000000005', 'sharan@gmail.com', 'SHARAN V', 'student', 'Information Technology', true, now(), now())
ON CONFLICT (id) DO UPDATE SET 
  name = EXCLUDED.name,
  role = EXCLUDED.role,
  department = EXCLUDED.department,
  updated_at = now();

-- 3. INSERT RECOGNIZED CAMPUS ORGANIZATIONS
INSERT INTO public.organizations (id, name, short_name, type, category, department, description, status, faculty_coordinator_id, student_coordinator_id) VALUES
('45283f33-e7a2-4938-bfc6-08ea848e0d61', 'Coding Club', 'CC', 'club', 'Technical', 'Computer Science', 'A community for competitive programming, open source hackathons, and software engineering sprints.', 'active', 'a1b2c3d4-0003-4000-8000-000000000003', 'a1b2c3d4-0002-4000-8000-000000000002'),
('32cfeb41-1570-4151-8725-191f4e48b983', 'Robotics Cell', 'RC', 'cell', 'Technical', 'Electronics', 'Autonomous combat rovers, IoT edge controllers, and national hardware robotics leagues.', 'active', 'a1b2c3d4-0003-4000-8000-000000000003', 'a1b2c3d4-0002-4000-8000-000000000002'),
('21ad11f0-1dda-4cbe-a10f-683dbe0d417e', 'Cultural Club', 'CUL', 'club', 'Cultural', 'Civil', 'Classical arts, Carnatic music, inter-collegiate fine arts, and annual cultural celebrations.', 'active', 'a1b2c3d4-0003-4000-8000-000000000003', 'a1b2c3d4-0002-4000-8000-000000000002'),
('c07fb697-55d1-4167-abb6-78f653542c85', 'Entrepreneurship Cell', 'ECELL', 'cell', 'Professional', 'Information Technology', 'Student startups, angel pitching, patent ideation grants, and corporate incubation.', 'active', 'a1b2c3d4-0003-4000-8000-000000000003', 'a1b2c3d4-0002-4000-8000-000000000002'),
('3253a0c6-a0aa-4610-85ab-b29997900f89', 'Sports Club', 'SC', 'club', 'Sports', 'Mechanical', 'Athletic excellence, intra-college badminton, cricket championships, and annual sports track meets.', 'active', 'a1b2c3d4-0003-4000-8000-000000000003', 'a1b2c3d4-0002-4000-8000-000000000002'),
('7f81b17a-59b1-41e7-8149-8b839bb9b740', 'Design Tribe', 'DT', 'club', 'Technical', 'Information Technology', 'UI/UX design systems, Figma component prototyping, and human-centered design sprints.', 'active', 'a1b2c3d4-0003-4000-8000-000000000003', 'a1b2c3d4-0002-4000-8000-000000000002')
ON CONFLICT (id) DO UPDATE SET 
  name = EXCLUDED.name,
  type = EXCLUDED.type,
  description = EXCLUDED.description,
  status = EXCLUDED.status;

-- 4. INSERT STUDENTS RECORD
INSERT INTO public.students (user_id, register_number, department, year, section, skills, interests, bio) VALUES
('a1b2c3d4-0001-4000-8000-000000000001', '25ITR101', 'Information Technology', 2, 'A', ARRAY['TypeScript', 'React', 'Node.js'], ARRAY['Web Dev', 'Hackathons'], 'IT undergraduate passionate about full-stack engineering.'),
('423f05db-e3bc-4b3c-8cf2-29fc30f54ff3', '25ITR121', 'Information Technology', 2, 'B', ARRAY['React', 'PostgreSQL', 'Tailwind CSS'], ARRAY['System Design', 'Cloud Apps'], 'Student researcher and developer for ClubHub.')
ON CONFLICT (user_id) DO UPDATE SET 
  register_number = EXCLUDED.register_number,
  skills = EXCLUDED.skills,
  interests = EXCLUDED.interests;

-- 5. INSERT CAMPUS EVENTS
INSERT INTO public.events (id, organization_id, title, description, event_type, location, start_date, end_date, maximum_participants, status) VALUES
('b1c2d3e4-1001-4000-8000-000000000001', '45283f33-e7a2-4938-bfc6-08ea848e0d61', 'HackSphere 2026: 24-Hour Hackathon', 'Inter-collegiate 24-hour hackathon solving real-world problem statements.', 'competition', 'CC-3 Computing Laboratory', now() + interval '3 days', now() + interval '4 days', 120, 'upcoming'),
('b1c2d3e4-1002-4000-8000-000000000002', '7f81b17a-59b1-41e7-8149-8b839bb9b740', 'DesignSprint: UI/UX Prototyping Workshop', 'Hands-on Figma component systems and interactive UX sprints.', 'workshop', 'Mechanical Audio Visual Hall', now() + interval '6 days', now() + interval '6 days 4 hours', 80, 'upcoming'),
('b1c2d3e4-1003-4000-8000-000000000003', 'c07fb697-55d1-4167-abb6-78f653542c85', 'Startup Pitch Challenge 2026', 'Collegiate entrepreneurship pitch round with venture mentorship.', 'competition', 'Convention Center Auditorium', now() + interval '10 days', now() + interval '10 days 6 hours', 200, 'upcoming'),
('b1c2d3e4-1004-4000-8000-000000000004', '32cfeb41-1570-4151-8725-191f4e48b983', 'RoboWars 2026: Combat Tournament', 'Autonomous rover navigation and combat robot championship.', 'competition', 'Indoor Sports Complex', now() + interval '14 days', now() + interval '15 days', 150, 'upcoming')
ON CONFLICT (id) DO UPDATE SET title = EXCLUDED.title, status = EXCLUDED.status;

-- 6. INSERT MEMBERSHIPS
INSERT INTO public.memberships (id, student_id, organization_id, role, status) VALUES
('c1d2e3f4-2001-4000-8000-000000000001', 'a1b2c3d4-0001-4000-8000-000000000001', '45283f33-e7a2-4938-bfc6-08ea848e0d61', 'core_member', 'approved'),
('c1d2e3f4-2002-4000-8000-000000000002', '423f05db-e3bc-4b3c-8cf2-29fc30f54ff3', '45283f33-e7a2-4938-bfc6-08ea848e0d61', 'member', 'approved'),
('c1d2e3f4-2003-4000-8000-000000000003', '423f05db-e3bc-4b3c-8cf2-29fc30f54ff3', '7f81b17a-59b1-41e7-8149-8b839bb9b740', 'member', 'approved')
ON CONFLICT (student_id, organization_id) DO NOTHING;

-- 7. INSERT EVENT REGISTRATIONS
INSERT INTO public.event_registrations (event_id, student_id, participation_status) VALUES
('b1c2d3e4-1001-4000-8000-000000000001', 'a1b2c3d4-0001-4000-8000-000000000001', 'registered'),
('b1c2d3e4-1001-4000-8000-000000000001', '423f05db-e3bc-4b3c-8cf2-29fc30f54ff3', 'registered')
ON CONFLICT (event_id, student_id) DO NOTHING;
