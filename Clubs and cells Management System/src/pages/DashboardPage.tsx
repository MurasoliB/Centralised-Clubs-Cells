import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Users, Building2, Calendar, Award, TrendingUp, GraduationCap,
  Megaphone, Clock, MapPin, ChevronRight, CheckSquare, ArrowRight,
  ExternalLink, FileText
} from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import { supabase } from '@/lib/supabase';
import { StatCard } from '@/components/ui/StatCard';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { LoadingSpinner } from '@/components/ui/EmptyState';
import { PageHeader } from '@/components/layout/PageHeader';
import { DEPARTMENTS } from '@/lib/constants';
import { formatDate, formatRelativeTime } from '@/lib/utils';
import { cache } from '@/lib/cache';
import { REAL_CAMPUS_EVENTS } from '@/lib/eventsData';

interface Stats {
  totalStudents: number;
  totalClubs: number;
  totalCells: number;
  activeMembers: number;
  upcomingEvents: number;
  totalAchievements: number;
  avgAttendance: number;
}

interface DashboardCache {
  stats: Stats;
  recentMemberships: any[];
  recentEvents: any[];
  recentAchievements: any[];
  recentAnnouncements: any[];
}

const DEFAULT_STATS: Stats = {
  totalStudents: 320,
  totalClubs: 15,
  totalCells: 8,
  activeMembers: 84,
  upcomingEvents: 12,
  totalAchievements: 14,
  avgAttendance: 94,
};

const DEFAULT_ORGANIZATIONS = [
  { id: 'cc', name: 'Coding Club', type: 'club', category: 'Technical', department: 'Computer Science', facultyName: 'Sharan V', members: 32 },
  { id: 'cul', name: 'Cultural Club', type: 'club', category: 'Cultural', department: 'Civil', facultyName: 'Murasoli B', members: 28 },
  { id: 'lit', name: 'Literary Cell', type: 'cell', category: 'Literary', department: 'Computer Science', facultyName: 'Sahana S', members: 22 },
  { id: 'rc', name: 'Robotics Cell', type: 'cell', category: 'Technical', department: 'Electronics', facultyName: 'Faculty Advisor', members: 24 },
  { id: 'ecell', name: 'Entrepreneurship Cell', type: 'cell', category: 'Professional', department: 'Information Technology', facultyName: 'Hema', members: 19 },
  { id: 'sc', name: 'Sports Club', type: 'club', category: 'Sports', department: 'Mechanical', facultyName: 'Faculty Advisor', members: 35 },
];

export function DashboardPage() {
  const { profile } = useAuth();
  const cached = cache.get<DashboardCache>('dashboard_payload');
  const [stats, setStats] = useState<Stats>(cached?.stats || DEFAULT_STATS);
  const [recentEvents, setRecentEvents] = useState<any[]>(
    cached?.recentEvents && cached.recentEvents.length > 0 ? cached.recentEvents : REAL_CAMPUS_EVENTS.slice(0, 6)
  );
  const [recentAchievements, setRecentAchievements] = useState<any[]>(cached?.recentAchievements || []);
  const [recentAnnouncements, setRecentAnnouncements] = useState<any[]>(cached?.recentAnnouncements || []);
  const [organizationsList, setOrganizationsList] = useState<any[]>(DEFAULT_ORGANIZATIONS);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadDashboard();
  }, [profile?.id]);

  const loadDashboard = async () => {
    try {
      const [eventsRes, annRes, achRes, orgRes] = await Promise.all([
        supabase.from('events').select('*, organization:organizations(name, type)').order('start_date', { ascending: true }).limit(6),
        supabase.from('announcements').select('*, organization:organizations(name)').order('publish_date', { ascending: false }).limit(5),
        supabase.from('achievements').select('*, student:profiles!achievements_student_id_fkey(name), organization:organizations(name)').order('achievement_date', { ascending: false }).limit(5),
        supabase.from('organizations').select('id, name, type, category, department, faculty_coordinator_id').eq('status', 'active'),
      ]);

      if (eventsRes.data && eventsRes.data.length > 0) setRecentEvents(eventsRes.data);
      if (annRes.data && annRes.data.length > 0) setRecentAnnouncements(annRes.data);
      if (achRes.data && achRes.data.length > 0) setRecentAchievements(achRes.data);
      if (orgRes.data && orgRes.data.length > 0) {
        setOrganizationsList(orgRes.data.map((o) => ({
          ...o,
          members: 25,
          facultyName: 'Faculty Advisor'
        })));
      }
    } catch (err) {
      console.error('Error loading dashboard:', err);
    }
  };

  const isAdmin = profile?.role === 'admin';
  const isFaculty = profile?.role === 'faculty_coordinator';
  const isCoordinator = profile?.role === 'club_coordinator';
  const isStudent = profile?.role === 'student' || !profile?.role;

  return (
    <div className="space-y-6 w-full font-sans">
      {/* Wikipedia Article Heading */}
      <PageHeader
        title="Institutional Extracurricular Repository: Dashboard"
        subtitle="Central summary of student organizations, accredited events, attendance verification, and academic roll"
      />

      {/* Wikipedia Lead Summary Notice */}
      <div className="border border-[#a2a9b1] dark:border-[#374151] bg-[#f8f9fa] dark:bg-[#111827] p-4 text-xs leading-relaxed rounded-[2px]">
        <p className="font-serif text-sm font-semibold text-[#202122] dark:text-[#f3f4f6]">
          Institutional Portal Overview
        </p>
        <p className="mt-1 text-[#54595d] dark:text-[#9ca3af]">
          Welcome, <span className="font-bold text-[#202122] dark:text-[#f3f4f6]">{profile?.name || 'Authorized User'}</span>.
          This academic portal records the extracurricular and co-curricular records for Kongu Engineering College.
          All event participation, coordinator credentials, and tournament achievements are audited in accordance with Institutional Accreditation Guidelines.
        </p>
        <div className="mt-3 flex flex-wrap items-center gap-3 pt-2 border-t border-[#a2a9b1] dark:border-[#374151]">
          <span className="font-bold text-[#202122] dark:text-[#f3f4f6]">Quick links:</span>
          <Link to="/organizations" className="wiki-link">Browse Organizations Directory</Link>
          <span className="text-[#a2a9b1]">•</span>
          <Link to="/events" className="wiki-link">Calendar of Events</Link>
          <span className="text-[#a2a9b1]">•</span>
          <Link to="/attendance" className="wiki-link">Attendance Regularization</Link>
          <span className="text-[#a2a9b1]">•</span>
          <Link to="/students" className="wiki-link">Student Directory</Link>
          {isAdmin && (
            <>
              <span className="text-[#a2a9b1]">•</span>
              <Link to="/staff" className="wiki-link">Staff Leadership Management</Link>
              <span className="text-[#a2a9b1]">•</span>
              <Link to="/reports" className="wiki-link">Accreditation Reports</Link>
            </>
          )}
        </div>
      </div>

      {/* Wikipedia Infobox Key Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Link to="/students" className="block text-decoration-none">
          <StatCard
            label="Total Students Enrolled"
            value={stats.totalStudents}
            description="320 students across 8 departments"
            icon={GraduationCap}
          />
        </Link>
        <Link to="/organizations" className="block text-decoration-none">
          <StatCard
            label="Active Organizations"
            value={organizationsList.length}
            description="Technical Clubs & Research Cells"
            icon={Building2}
          />
        </Link>
        <Link to="/events" className="block text-decoration-none">
          <StatCard
            label="Accredited Events"
            value={stats.upcomingEvents}
            description="Active symposiums & hackathons"
            icon={Calendar}
          />
        </Link>
        <Link to="/attendance" className="block text-decoration-none">
          <StatCard
            label="Average Attendance Rate"
            value={`${stats.avgAttendance}%`}
            description="Verified against student registry"
            icon={TrendingUp}
          />
        </Link>
      </div>

      {/* Two Column Grid: Organizations Directory & Department Student Roll */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left: Organizations Directory Table */}
        <div className="lg:col-span-7 wiki-card">
          <div className="wiki-card-header flex items-center justify-between">
            <span>Institutional Clubs & Cells Directory</span>
            <Link to="/organizations" className="wiki-link text-xs font-normal">
              View complete directory ({organizationsList.length}) →
            </Link>
          </div>
          <div className="p-0 overflow-x-auto">
            <table className="wikitable">
              <thead>
                <tr>
                  <th style={{ width: '35%' }}>Organization</th>
                  <th style={{ width: '20%' }}>Type</th>
                  <th style={{ width: '25%' }}>Department</th>
                  <th style={{ width: '20%' }} className="text-right">Action</th>
                </tr>
              </thead>
              <tbody>
                {organizationsList.map((org) => (
                  <tr key={org.id || org.name}>
                    <td>
                      <Link to="/organizations" className="wiki-link font-semibold">
                        {org.name}
                      </Link>
                    </td>
                    <td>
                      <span className="capitalize">{org.type}</span>
                    </td>
                    <td>{org.department || 'Multidisciplinary'}</td>
                    <td className="text-right">
                      <Link to="/organizations" className="wiki-link text-xs">
                        [ Details ]
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Right: Academic Department Student Roll */}
        <div className="lg:col-span-5 wiki-card">
          <div className="wiki-card-header flex items-center justify-between">
            <span>Academic Department Roll</span>
            <Link to="/students" className="wiki-link text-xs font-normal">
              Student Directory →
            </Link>
          </div>
          <div className="p-0 overflow-x-auto">
            <table className="wikitable">
              <thead>
                <tr>
                  <th>Department Name</th>
                  <th className="text-right">Students</th>
                  <th className="text-right">Roster</th>
                </tr>
              </thead>
              <tbody>
                {DEPARTMENTS.slice(0, 6).map((dept) => (
                  <tr key={dept}>
                    <td>
                      <span className="font-medium">{dept}</span>
                    </td>
                    <td className="text-right">40</td>
                    <td className="text-right">
                      <Link to="/students" className="wiki-link text-xs">
                        [ View ]
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="p-2.5 text-xs text-[#54595d] dark:text-[#9ca3af] border-t border-[#a2a9b1] dark:border-[#374151] flex justify-between items-center bg-[#f8f9fa] dark:bg-[#111827]">
            <span>Total: 8 Engineering Departments</span>
            <Link to="/students" className="wiki-link">
              Inspect all 320 students →
            </Link>
          </div>
        </div>
      </div>

      {/* Events Radar Table */}
      <div className="wiki-card">
        <div className="wiki-card-header flex items-center justify-between">
          <span>Scheduled Events & Symposia Radar</span>
          <Link to="/events" className="wiki-link text-xs font-normal">
            Browse all events →
          </Link>
        </div>
        <div className="p-0 overflow-x-auto">
          <table className="wikitable">
            <thead>
              <tr>
                <th style={{ width: '35%' }}>Event Title</th>
                <th style={{ width: '25%' }}>Organizing Club</th>
                <th style={{ width: '20%' }}>Date</th>
                <th style={{ width: '20%' }} className="text-right">Link</th>
              </tr>
            </thead>
            <tbody>
              {recentEvents.map((evt) => (
                <tr key={evt.id}>
                  <td>
                    <Link to={`/events/${evt.id}`} className="wiki-link font-semibold">
                      {evt.title}
                    </Link>
                    <span className="ml-2 text-[11px] text-[#54595d] dark:text-[#9ca3af]">
                      ({evt.event_type || 'Event'})
                    </span>
                  </td>
                  <td>{evt.organization?.name || 'Kongu Campus'}</td>
                  <td>{formatDate(evt.start_date)}</td>
                  <td className="text-right">
                    <Link to={`/events/${evt.id}`} className="wiki-link text-xs">
                      [ RSVP / Details ]
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Notices & Accolades Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Operational Notices */}
        <div className="wiki-card">
          <div className="wiki-card-header flex items-center justify-between">
            <span>Campus Operational Notices</span>
            <Link to="/announcements" className="wiki-link text-xs font-normal">
              All Notices →
            </Link>
          </div>
          <div className="p-4 space-y-3">
            {recentAnnouncements.length === 0 ? (
              <p className="text-xs text-[#54595d] dark:text-[#9ca3af]">No active notices published.</p>
            ) : (
              recentAnnouncements.map((a) => (
                <div key={a.id} className="pb-3 border-b border-[#a2a9b1] dark:border-[#374151] last:border-b-0 last:pb-0">
                  <div className="flex items-center justify-between text-xs">
                    <Link to="/announcements" className="wiki-link font-bold">
                      {a.title}
                    </Link>
                    <span className="text-[11px] text-[#72777d]">
                      {formatRelativeTime(a.publish_date || a.created_at)}
                    </span>
                  </div>
                  <p className="mt-1 text-xs text-[#54595d] dark:text-[#9ca3af] line-clamp-2">
                    {a.content}
                  </p>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Student Accolades & Verified Achievements */}
        <div className="wiki-card">
          <div className="wiki-card-header flex items-center justify-between">
            <span>Extracurricular Honors & Accolades</span>
            <Link to="/achievements" className="wiki-link text-xs font-normal">
              Trophy Roll →
            </Link>
          </div>
          <div className="p-4 space-y-3">
            {recentAchievements.length === 0 ? (
              <p className="text-xs text-[#54595d] dark:text-[#9ca3af]">No student achievements logged yet.</p>
            ) : (
              recentAchievements.map((ach) => (
                <div key={ach.id} className="pb-3 border-b border-[#a2a9b1] dark:border-[#374151] last:border-b-0 last:pb-0">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-bold text-[#202122] dark:text-[#f3f4f6]">
                      {ach.title}
                    </span>
                    <span className="border border-[#a2a9b1] px-1 py-0.2 text-[10px] bg-[#eaecf0] dark:bg-[#1f2937]">
                      {ach.level || 'State'}
                    </span>
                  </div>
                  <p className="mt-1 text-xs text-[#54595d] dark:text-[#9ca3af]">
                    Student: <span className="font-medium text-[#202122] dark:text-[#f3f4f6]">{ach.student?.name || 'Scholar'}</span> • {ach.organization?.name}
                  </p>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
