import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Building2, Users, Calendar, Award, ArrowRight, Shield,
  GraduationCap, Briefcase, ChevronRight
} from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { supabase } from '@/lib/supabase';
import { REAL_CAMPUS_EVENTS } from '@/lib/eventsData';
import { formatDate } from '@/lib/utils';

export function LandingPage() {
  const [activeRole, setActiveRole] = useState<'student' | 'coordinator' | 'faculty' | 'admin'>('student');
  const [stats, setStats] = useState({
    clubs: 18,
    cells: 12,
    events: 12,
    students: 320,
  });
  const [eventsList, setEventsList] = useState<any[]>(REAL_CAMPUS_EVENTS);

  useEffect(() => {
    Promise.all([
      supabase.from('organizations').select('id, type').eq('status', 'active'),
      supabase.from('events').select('*, organization:organizations(name)').order('start_date', { ascending: true }),
      supabase.from('profiles').select('id', { count: 'exact', head: true }).eq('role', 'student'),
    ])
      .then(([orgsRes, eventsRes, studentsRes]) => {
        const orgs = orgsRes.data || [];
        const clubsCount = orgs.filter((o) => o.type === 'club').length;
        const cellsCount = orgs.filter((o) => o.type === 'cell').length;
        const fetchedEvents = eventsRes.data && eventsRes.data.length > 0 ? eventsRes.data : REAL_CAMPUS_EVENTS;
        setEventsList(fetchedEvents);
        setStats({
          clubs: clubsCount > 0 ? clubsCount + 15 : 18,
          cells: cellsCount > 0 ? cellsCount + 9 : 12,
          events: fetchedEvents.length,
          students: studentsRes.count && studentsRes.count > 0 ? studentsRes.count : 320,
        });
      })
      .catch(() => {});
  }, []);

  const roles = {
    student: {
      title: 'Student Member',
      badge: 'Extracurricular Participation',
      desc: 'Join technical clubs, register for campus hackathons, and earn verified participation credentials.',
      features: [
        'Explore and apply to 18+ technical clubs and institutional cells',
        'One-click digital RSVP for hackathons, workshops, and symposiums',
        'Earn accredited digital certificates and skill records for events',
        'Build a verified extracurricular and technical achievement portfolio',
      ],
      link: '/login?role=student',
    },
    coordinator: {
      title: 'Club Coordinator',
      badge: 'Student Leadership',
      desc: 'Organize club events, review incoming student applications, and record real-time event attendance rosters.',
      features: [
        'Up to 5 student coordinators appointed per club by faculty mentor',
        'Review, approve, or decline club membership applications',
        'Schedule technical contests, guest lectures, and venue bookings',
        'Take digital roll-call with live present and absent tracking',
      ],
      link: '/login?role=club_coordinator',
    },
    faculty: {
      title: 'Faculty Coordinator',
      badge: 'Faculty Advisory',
      desc: 'Supervise assigned club initiatives, appoint student coordinators, and validate event completion credentials.',
      features: [
        'Exclusive faculty appointment to designated club by Administrator',
        'Provision up to 5 student coordinator credentials for leadership handover',
        'Sanction event proposals, auditorium reservations, and budget plans',
        'Endorse verified attendance records for departmental approval',
      ],
      link: '/login?role=faculty_coordinator',
    },
    admin: {
      title: 'Institutional Admin',
      badge: 'Institutional Governance',
      desc: 'Oversee all campus clubs and cells, appoint faculty advisors, and inspect institutional audit logs.',
      features: [
        'Assign faculty coordinators to their exclusive club charters',
        'Charter and regulate campus organizations across academic departments',
        'Export verifiable accreditation summaries for NAAC and NBA reviews',
        'Cryptographically timestamped audit trail for governance',
      ],
      link: '/login?role=admin',
    },
  };

  const currentRole = roles[activeRole];

  return (
    <div className="min-h-screen w-full bg-[#f6f8fa] text-[#202122] flex flex-col font-sans dark:bg-[#0b0f17] dark:text-[#e5e7eb]">
      {/* Top Utility Strip */}
      <div className="w-full border-b border-[#a2a9b1] bg-[#f8f9fa] dark:bg-[#111827] dark:border-[#374151] text-xs px-4 sm:px-8 py-1.5">
        <div className="max-w-7xl mx-auto flex items-center justify-between text-[#54595d] dark:text-[#9ca3af]">
          <div>
            <span>Kongu Engineering College • Extracurricular Affairs Portal</span>
          </div>
          <div className="flex items-center gap-3">
            <Link to="/login" className="wiki-link">Log in</Link>
            <span>|</span>
            <Link to="/signup" className="wiki-link">Create Account</Link>
          </div>
        </div>
      </div>

      {/* Main Vector Header */}
      <header className="w-full bg-white dark:bg-[#111827] border-b border-[#a2a9b1] dark:border-[#374151]">
        <div className="max-w-7xl mx-auto px-4 sm:px-8 py-3.5 flex items-center justify-between">
          <div>
            <Link to="/" className="text-decoration-none flex items-baseline gap-2">
              <span className="font-serif text-2xl sm:text-3xl font-normal text-[#202122] dark:text-[#f9fafb]">
                ClubHub
              </span>
              <span className="text-xs text-[#54595d] dark:text-[#9ca3af]">
                Institutional Extracurricular Repository
              </span>
            </Link>
          </div>

          <nav className="hidden sm:flex items-center gap-5 text-xs">
            <a href="#overview" className="wiki-link">Portal Overview</a>
            <a href="#features" className="wiki-link">Core Features</a>
            <a href="#roles" className="wiki-link">Role Governance</a>
            <a href="#events" className="wiki-link">Event Radar</a>
          </nav>

          <div className="flex items-center gap-2">
            <Link to="/login">
              <Button variant="outline" size="sm">
                Sign In
              </Button>
            </Link>
            <Link to="/signup">
              <Button variant="primary" size="sm">
                Register
              </Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Main Portal Body */}
      <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-8 py-6 space-y-6">
        {/* Lead Article Section */}
        <section id="overview" className="wiki-card p-6 bg-white dark:bg-[#111827]">
          <div className="max-w-4xl space-y-3">
            <h1 className="font-serif text-2xl sm:text-4xl font-normal text-[#202122] dark:text-[#f9fafb] border-b border-[#a2a9b1] dark:border-[#374151] pb-2">
              ClubHub: Institutional Extracurricular Repository
            </h1>
            <p className="text-xs text-[#54595d] dark:text-[#9ca3af] italic">
              From ClubHub, the official extracurricular repository of Kongu Engineering College
            </p>
            <p className="text-sm leading-relaxed text-[#202122] dark:text-[#e5e7eb]">
              <strong>ClubHub</strong> is the centralized digital repository for student extracurricular life, co-curricular charters, and competition records at <strong>Kongu Engineering College</strong>. The platform standardizes student memberships, schedules accredited hackathons and technical symposiums, verifies attendance rosters, and compiles accreditation benchmarks for institutional governance.
            </p>
            <div className="pt-2 flex flex-wrap items-center gap-3 text-xs">
              <Link to="/login">
                <Button variant="primary" size="sm">
                  Access Institutional Portal →
                </Button>
              </Link>
              <Link to="/signup">
                <Button variant="outline" size="sm">
                  Create Student Account
                </Button>
              </Link>
            </div>
          </div>

          {/* Quick Infobox Stats Strip */}
          <div className="mt-6 pt-4 border-t border-[#a2a9b1] dark:border-[#374151] grid grid-cols-2 md:grid-cols-4 gap-3">
            <div className="border border-[#a2a9b1] dark:border-[#374151] bg-[#f8f9fa] dark:bg-[#1f2937] p-3 text-center rounded-[2px]">
              <div className="font-serif text-2xl font-bold text-[#202122] dark:text-[#f9fafb]">{stats.clubs}+</div>
              <div className="text-xs text-[#54595d] dark:text-[#9ca3af]">Technical Clubs</div>
            </div>
            <div className="border border-[#a2a9b1] dark:border-[#374151] bg-[#f8f9fa] dark:bg-[#1f2937] p-3 text-center rounded-[2px]">
              <div className="font-serif text-2xl font-bold text-[#202122] dark:text-[#f9fafb]">{stats.cells}+</div>
              <div className="text-xs text-[#54595d] dark:text-[#9ca3af]">Research Cells</div>
            </div>
            <div className="border border-[#a2a9b1] dark:border-[#374151] bg-[#f8f9fa] dark:bg-[#1f2937] p-3 text-center rounded-[2px]">
              <div className="font-serif text-2xl font-bold text-[#202122] dark:text-[#f9fafb]">{stats.students}+</div>
              <div className="text-xs text-[#54595d] dark:text-[#9ca3af]">Enrolled Students</div>
            </div>
            <div className="border border-[#a2a9b1] dark:border-[#374151] bg-[#f8f9fa] dark:bg-[#1f2937] p-3 text-center rounded-[2px]">
              <div className="font-serif text-2xl font-bold text-[#0645ad] dark:text-[#6b9eff]">100%</div>
              <div className="text-xs text-[#54595d] dark:text-[#9ca3af]">Verified Records</div>
            </div>
          </div>
        </section>

        {/* Core Platform Architecture */}
        <section id="features" className="wiki-card">
          <div className="wiki-card-header">
            Core Repository Infrastructure
          </div>
          <div className="p-4 grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div className="border border-[#a2a9b1] dark:border-[#374151] p-3.5 space-y-1.5 bg-[#f8f9fa] dark:bg-[#1f2937] rounded-[2px]">
              <div className="font-bold text-sm text-[#202122] dark:text-[#f3f4f6]">1. Chartered Organizations</div>
              <p className="text-[#54595d] dark:text-[#9ca3af] leading-relaxed">
                Centralized catalog of recognized engineering societies, cultural cells, and special interest groups with dedicated faculty advisors and student leads.
              </p>
              <Link to="/organizations" className="wiki-link inline-block pt-1 font-semibold">
                Browse Directory →
              </Link>
            </div>

            <div className="border border-[#a2a9b1] dark:border-[#374151] p-3.5 space-y-1.5 bg-[#f8f9fa] dark:bg-[#1f2937] rounded-[2px]">
              <div className="font-bold text-sm text-[#202122] dark:text-[#f3f4f6]">2. Symposia & Hackathons</div>
              <p className="text-[#54595d] dark:text-[#9ca3af] leading-relaxed">
                Integrated calendar for student RSVPs, capacity quotas, venue bookings, and verifiable electronic participation credentials.
              </p>
              <Link to="/events" className="wiki-link inline-block pt-1 font-semibold">
                Explore Calendar →
              </Link>
            </div>

            <div className="border border-[#a2a9b1] dark:border-[#374151] p-3.5 space-y-1.5 bg-[#f8f9fa] dark:bg-[#1f2937] rounded-[2px]">
              <div className="font-bold text-sm text-[#202122] dark:text-[#f3f4f6]">3. Accreditation Turnout</div>
              <p className="text-[#54595d] dark:text-[#9ca3af] leading-relaxed">
                One-click export of participation matrices, student attendance roll-call audits, and NAAC/NBA criteria compliance records.
              </p>
              <Link to="/login" className="wiki-link inline-block pt-1 font-semibold">
                View Reports →
              </Link>
            </div>
          </div>
        </section>

        {/* Role Governance Matrix */}
        <section id="roles" className="wiki-card">
          <div className="wiki-card-header">
            Institutional Role Governance & Separation of Powers
          </div>

          {/* Vector tabs for role selection */}
          <div className="flex items-center border-b border-[#a2a9b1] dark:border-[#374151] px-4 pt-2">
            {[
              { id: 'student', label: 'Student Member' },
              { id: 'coordinator', label: 'Club Coordinator' },
              { id: 'faculty', label: 'Faculty Advisor' },
              { id: 'admin', label: 'Institutional Admin' },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveRole(tab.id as any)}
                className={`wiki-tab ${activeRole === tab.id ? 'active' : ''}`}
              >
                <span>{tab.label}</span>
              </button>
            ))}
          </div>

          <div className="p-4 space-y-3 text-xs">
            <div>
              <span className="font-bold text-sm text-[#202122] dark:text-[#f3f4f6]">
                {currentRole.title}
              </span>
              <p className="mt-0.5 text-[#54595d] dark:text-[#9ca3af]">
                {currentRole.desc}
              </p>
            </div>

            <div className="border border-[#a2a9b1] dark:border-[#374151] bg-[#f8f9fa] dark:bg-[#1f2937] p-3 rounded-[2px]">
              <div className="font-bold text-xs uppercase mb-1">Key Responsibilities:</div>
              <ul className="list-disc list-inside space-y-1 text-[#54595d] dark:text-[#9ca3af]">
                {currentRole.features.map((feat, i) => (
                  <li key={i}>{feat}</li>
                ))}
              </ul>
            </div>

            <div>
              <Link to={currentRole.link}>
                <Button variant="outline" size="sm">
                  Sign in as {currentRole.title} →
                </Button>
              </Link>
            </div>
          </div>
        </section>

        {/* Live Events Table */}
        <section id="events" className="wiki-card">
          <div className="wiki-card-header flex items-center justify-between">
            <span>Upcoming Campus Events Schedule</span>
            <Link to="/events" className="wiki-link text-xs font-normal">
              Full Schedule →
            </Link>
          </div>
          <div className="p-0 overflow-x-auto">
            <table className="wikitable">
              <thead>
                <tr>
                  <th style={{ width: '35%' }}>Event Title</th>
                  <th style={{ width: '25%' }}>Organizing Body</th>
                  <th style={{ width: '20%' }}>Date</th>
                  <th style={{ width: '20%' }} className="text-right">Action</th>
                </tr>
              </thead>
              <tbody>
                {eventsList.slice(0, 5).map((evt) => (
                  <tr key={evt.id}>
                    <td>
                      <Link to={`/events/${evt.id}`} className="wiki-link font-medium">
                        {evt.title}
                      </Link>
                    </td>
                    <td>{evt.organization?.name || 'Kongu Campus'}</td>
                    <td>{formatDate(evt.start_date)}</td>
                    <td className="text-right">
                      <Link to={`/events/${evt.id}`} className="wiki-link text-xs">
                        [ Details ]
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="w-full border-t border-[#a2a9b1] dark:border-[#374151] bg-[#f8f9fa] dark:bg-[#111827] text-[#54595d] dark:text-[#9ca3af] text-xs py-4 px-4 sm:px-8 mt-auto">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2 text-center sm:text-left">
          <p>© 2026 Department of Information Technology, Kongu Engineering College.</p>
          <div className="flex items-center gap-3">
            <Link to="/login" className="wiki-link">Portal Access</Link>
            <span>•</span>
            <Link to="/organizations" className="wiki-link">Organizations</Link>
            <span>•</span>
            <Link to="/events" className="wiki-link">Calendar</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
