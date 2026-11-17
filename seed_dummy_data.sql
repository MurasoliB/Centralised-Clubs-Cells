-- ========================================================
-- MASTER SEED DUMMY DATA FOR CLUBS & CELLS MANAGEMENT
-- ========================================================

-- 1. CLUBS & CELLS (ORGANIZATIONS)
INSERT INTO public.organizations (name, short_name, type, category, description, status) VALUES
('Coding Club', 'CC', 'club', 'Technical', 'Competitive programming, open-source projects, and national hackathons', 'active'),
('Design Tribe', 'DT', 'club', 'Technical', 'UI/UX prototyping, graphic design, and human-centered design thinking', 'active'),
('Robotics Club', 'RAC', 'club', 'Technical', 'Autonomous combat robotics, IoT systems, and drone mechanics', 'active'),
('Institution''s Innovation Council', 'IIC', 'cell', 'Innovation', 'Student patents, ideation funding, and government incubation initiatives', 'active'),
('Entrepreneurship Development Cell', 'EDC', 'cell', 'Entrepreneurship', 'Startup pitch contests, angel networking, and venture mentorship', 'active'),
('Women Development Cell', 'WDC', 'cell', 'Empowerment', 'Leadership development, safety awareness, and technical empowerment', 'active')
ON CONFLICT DO NOTHING;

-- 2. STUDENT ACADEMIC PROFILE (Linked to student@college.edu)
INSERT INTO public.students (user_id, register_number, department, year, section, skills, interests, bio)
SELECT 
  id, 
  '25ITR121', 
  'Information Technology', 
  2, 
  'B', 
  ARRAY['React', 'TypeScript', 'PostgreSQL', 'Tailwind CSS'], 
  ARRAY['Web Development', 'Hackathons', 'Design Thinking'], 
  'Second-year IT undergraduate passionate about full-stack engineering and cloud architecture.'
FROM public.profiles 
WHERE email = 'student@college.edu'
ON CONFLICT (user_id) DO NOTHING;

-- 3. CLUB MEMBERSHIPS
INSERT INTO public.memberships (student_id, organization_id, role, status)
SELECT 
  p.id, 
  o.id, 
  'core_member', 
  'approved'
FROM public.profiles p
CROSS JOIN public.organizations o
WHERE p.email = 'student@college.edu' AND o.short_name IN ('CC', 'DT')
ON CONFLICT DO NOTHING;

-- 4. CAMPUS EVENTS
INSERT INTO public.events (organization_id, title, description, event_type, location, start_date, end_date, maximum_participants, status) VALUES
((SELECT id FROM public.organizations WHERE short_name = 'CC' LIMIT 1), 'HackSphere 2026: 24-Hour Hackathon', 'Inter-collegiate 24-hour coding sprint solving industry problem statements.', 'competition', 'CC-3 Computing Laboratory', NOW() + INTERVAL '4 days', NOW() + INTERVAL '5 days', 120, 'upcoming'),
((SELECT id FROM public.organizations WHERE short_name = 'DT' LIMIT 1), 'DesignSprint: UI/UX Prototyping Workshop', 'Hands-on Figma component systems and responsive design thinking sprints.', 'workshop', 'Mechanical Audio Visual Hall', NOW() + INTERVAL '7 days', NOW() + INTERVAL '7 days 4 hours', 80, 'upcoming'),
((SELECT id FROM public.organizations WHERE short_name = 'IIC' LIMIT 1), 'Startup Pitch Challenge 2026', 'Annual seed-funding pitch challenge judged by venture capitalists.', 'competition', 'Convention Center Auditorium', NOW() + INTERVAL '12 days', NOW() + INTERVAL '12 days 6 hours', 250, 'upcoming'),
((SELECT id FROM public.organizations WHERE short_name = 'RAC' LIMIT 1), 'RoboWars: Combat League 2026', 'Robot combat tournament and autonomous maze solver championship.', 'competition', 'Indoor Sports Complex', NOW() + INTERVAL '15 days', NOW() + INTERVAL '16 days', 150, 'upcoming'),
((SELECT id FROM public.organizations WHERE short_name = 'EDC' LIMIT 1), 'Founder Talk: From Campus to Series A', 'Fireside chat with alumni unicorn startup founders.', 'seminar', 'IT Seminar Hall', NOW() + INTERVAL '18 days', NOW() + INTERVAL '18 days 2 hours', 180, 'upcoming')
ON CONFLICT DO NOTHING;

-- 5. EVENT REGISTRATIONS
INSERT INTO public.event_registrations (event_id, student_id, participation_status)
SELECT 
  e.id, 
  p.id, 
  'registered'
FROM public.events e
CROSS JOIN public.profiles p
WHERE p.email = 'student@college.edu' AND e.title LIKE 'HackSphere%'
ON CONFLICT DO NOTHING;

-- 6. ATTENDANCE & ON-DUTY LOGS
INSERT INTO public.attendance (event_id, student_id, status, marked_at)
SELECT 
  e.id, 
  p.id, 
  'present', 
  NOW()
FROM public.events e
CROSS JOIN public.profiles p
WHERE p.email = 'student@college.edu' AND e.title LIKE 'HackSphere%'
ON CONFLICT DO NOTHING;

-- 7. CLUB ANNOUNCEMENTS
INSERT INTO public.announcements (organization_id, title, content, priority, target_audience) VALUES
((SELECT id FROM public.organizations WHERE short_name = 'CC' LIMIT 1), 'HackSphere 2026 Registrations Open!', 'All students are invited to register in teams of 2 to 4. Grand cash prizes of ₹50,000 to be won.', 'high', 'all'),
((SELECT id FROM public.organizations WHERE short_name = 'DT' LIMIT 1), 'DesignSprint Venue Update', 'Please note that the workshop has been moved to Mech Audio Visual Hall due to increased capacity.', 'medium', 'members'),
((SELECT id FROM public.organizations WHERE short_name = 'IIC' LIMIT 1), 'Patenting Grant Applications Open', 'Submit your initial project abstracts for college-funded patent assistance before the 25th.', 'high', 'all');

-- 8. STUDENT ACHIEVEMENTS
INSERT INTO public.achievements (student_id, organization_id, title, description, type, level, status)
SELECT 
  p.id, 
  o.id, 
  '1st Place - Smart India Hackathon Internal Round', 
  'Secured first place for developing the Centralised Clubs and Cell Management System.', 
  'competition', 
  'college', 
  'approved'
FROM public.profiles p
CROSS JOIN public.organizations o
WHERE p.email = 'student@college.edu' AND o.short_name = 'CC'
LIMIT 1
ON CONFLICT DO NOTHING;
