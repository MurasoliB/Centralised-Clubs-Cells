import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  CheckCircle2, Clock, AlertCircle, Plus, UserPlus, Users, Building2,
  Calendar, Award, Megaphone, FileText, ArrowRight, Shield, Check,
  Sparkles, ExternalLink, Filter
} from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/context/ToastContext';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { Modal } from '@/components/ui/Modal';
import { Input, Select } from '@/components/ui/Input';
import { PageHeader } from '@/components/layout/PageHeader';
import { DEPARTMENTS } from '@/lib/constants';
import { supabase } from '@/lib/supabase';
import { cache } from '@/lib/cache';
import { createFacultyAccount, createCoordinatorAccount } from '@/lib/authHelpers';

interface ClubTask {
  id: string;
  title: string;
  description: string;
  role: 'student' | 'club_coordinator' | 'faculty_coordinator' | 'admin';
  category: string;
  priority: 'High' | 'Medium' | 'Routine';
  actionLabel: string;
  actionUrl?: string;
  openModal?: 'create_faculty' | 'create_coordinator';
  color: string;
}

export function TasksPage() {
  const { profile } = useAuth();
  const { toast } = useToast();
  const navigate = useNavigate();

  const [activeRoleView, setActiveRoleView] = useState<string>(profile?.role || 'student');
  const [completedTaskIds, setCompletedTaskIds] = useState<Record<string, boolean>>({});

  // Modals state
  const [facultyModalOpen, setFacultyModalOpen] = useState(false);
  const [coordModalOpen, setCoordModalOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  // Forms
  const [facultyForm, setFacultyForm] = useState({
    name: '',
    email: '',
    department: 'Information Technology',
    phone: '',
    password: 'Faculty@KEC2026',
  });

  const [coordForm, setCoordForm] = useState({
    name: '',
    email: '',
    organizationId: '',
    department: 'Information Technology',
    phone: '',
    password: 'Coord@KEC2026',
  });

  const cachedOrgs = cache.get<any[]>('organizations_list') || [];
  const [orgs, setOrgs] = useState<any[]>(cachedOrgs);

  useEffect(() => {
    if (profile?.role === 'student') {
      navigate('/dashboard', { replace: true });
      return;
    }
    if (profile?.role) {
      setActiveRoleView(profile.role);
    }
    // Load organizations for coordinator assignment
    if (!cachedOrgs.length) {
      supabase.from('organizations').select('id, name, type').eq('status', 'active').then(({ data }) => {
        setOrgs(data || []);
      });
    }

    // Load completed tasks from localStorage
    const saved = localStorage.getItem(`kec_tasks_${profile?.id}`);
    if (saved) {
      try {
        setCompletedTaskIds(JSON.parse(saved));
      } catch {}
    }
  }, [profile?.id, profile?.role, navigate]);

  const toggleTask = (taskId: string) => {
    const updated = { ...completedTaskIds, [taskId]: !completedTaskIds[taskId] };
    setCompletedTaskIds(updated);
    if (profile?.id) {
      localStorage.setItem(`kec_tasks_${profile?.id}`, JSON.stringify(updated));
    }
    if (!completedTaskIds[taskId]) {
      toast('Task marked as completed! 🎉', 'success');
    }
  };

  const handleCreateFaculty = async (e: React.FormEvent) => {
    e.preventDefault();
    if (profile?.role !== 'admin') {
      toast('Only Institutional Administrator is authorized to create Faculty Coordinator profiles', 'error');
      return;
    }
    setSubmitting(true);
    try {
      await createFacultyAccount({
        name: facultyForm.name,
        email: facultyForm.email,
        department: facultyForm.department,
        phone: facultyForm.phone,
        password: facultyForm.password,
        role: 'faculty_coordinator',
      });
      toast(`Faculty Coordinator account created for ${facultyForm.name}! Credentials: ${facultyForm.email} / ${facultyForm.password}`, 'success');
      setFacultyModalOpen(false);
      setFacultyForm({ name: '', email: '', department: 'Information Technology', phone: '', password: 'Faculty@KEC2026' });
    } catch (err: any) {
      toast(err.message || 'Failed to create Faculty profile', 'error');
    } finally {
      setSubmitting(false);
    }
  };

  const handleCreateCoordinator = async (e: React.FormEvent) => {
    e.preventDefault();
    if (profile?.role !== 'faculty_coordinator') {
      toast('Only Faculty Coordinators are authorized to create Club Coordinators', 'error');
      return;
    }
    setSubmitting(true);
    try {
      await createCoordinatorAccount({
        name: coordForm.name,
        email: coordForm.email,
        organizationId: coordForm.organizationId,
        department: coordForm.department,
        phone: coordForm.phone,
        password: coordForm.password,
        role: 'club_coordinator',
      });
      toast(`Club Coordinator account created for ${coordForm.name}! Credentials: ${coordForm.email} / ${coordForm.password}`, 'success');
      setCoordModalOpen(false);
      setCoordForm({ name: '', email: '', organizationId: '', department: 'Information Technology', phone: '', password: 'Coord@KEC2026' });
    } catch (err: any) {
      toast(err.message || 'Failed to create Coordinator profile', 'error');
    } finally {
      setSubmitting(false);
    }
  };

  // The 4 distinct reliable tasks for each role
  const allTasks: ClubTask[] = [
    // STUDENT TASKS
    {
      id: 'task_std_1',
      title: 'Complete Student Academic Profile & Skills',
      description: 'Fill in your register number, department, year, key technical skills, and extracurricular interests for official college records.',
      role: 'student',
      category: 'Profile',
      priority: 'High',
      actionLabel: 'Update Profile',
      actionUrl: '/profile',
      color: 'emerald',
    },
    {
      id: 'task_std_2',
      title: 'Apply for Club or Special Interest Cell Membership',
      description: 'Explore active technical, cultural, sports, and professional bodies and submit an enrollment request.',
      role: 'student',
      category: 'Memberships',
      priority: 'High',
      actionLabel: 'Browse Clubs',
      actionUrl: '/organizations',
      color: 'emerald',
    },
    {
      id: 'task_std_3',
      title: 'RSVP for Flagship Hackathon / Workshop',
      description: 'Register for upcoming events like HackKEC 2026 or RoboWars to reserve your seat and qualify for certificates.',
      role: 'student',
      category: 'Events',
      priority: 'Medium',
      actionLabel: 'View Events',
      actionUrl: '/events',
      color: 'emerald',
    },
    {
      id: 'task_std_4',
      title: 'Submit Verified Accolade or Certificate',
      description: 'Upload tournament victories, certifications, or paper presentations to the college verified honor roll.',
      role: 'student',
      category: 'Accreditation',
      priority: 'Routine',
      actionLabel: 'Add Achievement',
      actionUrl: '/achievements',
      color: 'emerald',
    },

    // CLUB COORDINATOR TASKS
    {
      id: 'task_coord_1',
      title: 'Review & Authenticate Student Membership Requests',
      description: 'Inspect pending student applications to your assigned club and approve or decline them with 1-click feedback.',
      role: 'club_coordinator',
      category: 'Memberships',
      priority: 'High',
      actionLabel: 'Review Requests',
      actionUrl: '/memberships',
      color: 'amber',
    },
    {
      id: 'task_coord_2',
      title: 'Schedule & Publish Upcoming Flagship Event',
      description: 'Announce inter-college hackathons, symposia, or bootcamps with venue, date, time, and participant capacity.',
      role: 'club_coordinator',
      category: 'Events',
      priority: 'High',
      actionLabel: 'Schedule Event',
      actionUrl: '/events',
      color: 'amber',
    },
    {
      id: 'task_coord_3',
      title: 'Record Live Attendance for Completed Event',
      description: 'Mark student presence (Present, Absent, Late) so attendees can receive verified digital certificates.',
      role: 'club_coordinator',
      category: 'Attendance',
      priority: 'High',
      actionLabel: 'Take Attendance',
      actionUrl: '/attendance',
      color: 'amber',
    },
    {
      id: 'task_coord_4',
      title: 'Broadcast Official Club Notice to Members',
      description: 'Publish important semester schedule changes or audition press releases to the campus notice board.',
      role: 'club_coordinator',
      category: 'Announcements',
      priority: 'Routine',
      actionLabel: 'Post Notice',
      actionUrl: '/announcements',
      color: 'amber',
    },

    // FACULTY COORDINATOR TASKS
    {
      id: 'task_fac_1',
      title: 'Create & Onboard Club Coordinator Profile',
      description: 'Authorized privilege: Generate official club coordinator login credentials for student leaders and assign them to their club.',
      role: 'faculty_coordinator',
      category: 'Governance',
      priority: 'High',
      actionLabel: '+ Create Coordinator Account',
      openModal: 'create_coordinator',
      color: 'blue',
    },
    {
      id: 'task_fac_2',
      title: 'Validate Club Event Proposals & Logistics',
      description: 'Review event dates, hall allocations, and guest speaker approvals before public broadcast.',
      role: 'faculty_coordinator',
      category: 'Supervision',
      priority: 'High',
      actionLabel: 'Review Events',
      actionUrl: '/events',
      color: 'blue',
    },
    {
      id: 'task_fac_3',
      title: 'Audit Student Attendance & Certificate Issuance',
      description: 'Verify attendance records submitted by student coordinators before event certificates are issued.',
      role: 'faculty_coordinator',
      category: 'Attendance',
      priority: 'High',
      actionLabel: 'Inspect Attendance',
      actionUrl: '/attendance',
      color: 'blue',
    },
    {
      id: 'task_fac_4',
      title: 'Review Club Operational Performance Metrics',
      description: 'Inspect membership strength, event turnout ratios, and semester achievements for DSP/NAAC compliance.',
      role: 'faculty_coordinator',
      category: 'Analytics',
      priority: 'Medium',
      actionLabel: 'View Reports',
      actionUrl: '/reports',
      color: 'blue',
    },

    // INSTITUTIONAL ADMIN TASKS
    {
      id: 'task_adm_1',
      title: 'Create & Assign Faculty Coordinator Profile',
      description: 'Exclusive administrative privilege: Create verified Faculty Coordinator accounts and assign department jurisdictions.',
      role: 'admin',
      category: 'Onboarding',
      priority: 'High',
      actionLabel: '+ Create Faculty Account',
      openModal: 'create_faculty',
      color: 'cyan',
    },
    {
      id: 'task_adm_2',
      title: 'Audit Institutional Clubs & Cells Directory',
      description: 'Oversee charter statuses, update faculty coordinators, and activate newly formed student bodies.',
      role: 'admin',
      category: 'Directory',
      priority: 'High',
      actionLabel: 'Manage Organizations',
      actionUrl: '/organizations',
      color: 'cyan',
    },
    {
      id: 'task_adm_3',
      title: 'Inspect Security Logs & Audit Trail',
      description: 'Examine cryptographic timestamped records of every administrative action, user modification, and role update.',
      role: 'admin',
      category: 'Security',
      priority: 'High',
      actionLabel: 'View Audit Logs',
      actionUrl: '/audit-logs',
      color: 'cyan',
    },
    {
      id: 'task_adm_4',
      title: 'Export Institutional NAAC / NBA Accreditation Reports',
      description: 'Generate multi-department participation registries and CSV matrices for university inspections.',
      role: 'admin',
      category: 'Reporting',
      priority: 'Medium',
      actionLabel: 'Export Reports',
      actionUrl: '/reports',
      color: 'cyan',
    },
  ];

  // Filter tasks based on active selected role view
  const currentTasks = allTasks.filter((t) => t.role === activeRoleView);
  const completedCount = currentTasks.filter((t) => completedTaskIds[t.id]).length;
  const progressPercent = Math.round((completedCount / currentTasks.length) * 100) || 0;

  const handleAction = (task: ClubTask) => {
    if (task.openModal === 'create_faculty') {
      setFacultyModalOpen(true);
    } else if (task.openModal === 'create_coordinator') {
      setCoordModalOpen(true);
    } else if (task.actionUrl) {
      navigate(task.actionUrl);
    }
  };

  const roleHeaders: Record<string, { title: string; desc: string }> = {
    club_coordinator: {
      title: 'Club Coordinator Operational Tasks',
      desc: 'Review student membership requests, publish flagship club events, and log live attendance.',
    },
    faculty_coordinator: {
      title: 'Faculty Advisory Tasks & Governance',
      desc: 'Create official student club coordinators, validate event proposals, and audit student attendance.',
    },
    admin: {
      title: 'Institutional Administration Tasks',
      desc: 'Onboard Faculty Advisors, oversee club charters, inspect audit logs, and export accreditation reports.',
    },
  };

  const headerInfo = roleHeaders[profile?.role || 'club_coordinator'] || roleHeaders.club_coordinator;

  return (
    <div className="space-y-8 animate-fade-in font-sans">
      <PageHeader
        title={headerInfo.title}
        description={headerInfo.desc}
        badge={
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-blue-100 text-blue-700 border border-blue-200">
            <Sparkles className="w-3.5 h-3.5" />
            Reliable Action Matrix
          </span>
        }
        action={
          <div className="flex gap-2">
            {profile?.role === 'admin' && (
              <Button variant="gradient" size="sm" onClick={() => setFacultyModalOpen(true)} className="shadow-md shadow-blue-600/20 font-bold">
                <UserPlus className="h-4 w-4 mr-1.5" /> + Create Faculty Account
              </Button>
            )}
            {profile?.role === 'faculty_coordinator' && (
              <Button variant="emerald" size="sm" onClick={() => setCoordModalOpen(true)} className="shadow-md shadow-emerald-500/20 font-bold">
                <UserPlus className="h-4 w-4 mr-1.5" /> + Create Coordinator Account
              </Button>
            )}
          </div>
        }
      />

      {/* Role Governance Banner */}
      <div className="p-4 rounded-2xl bg-gradient-to-r from-blue-50/70 to-slate-50 border border-blue-100 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="flex items-center gap-2.5">
          <Shield className="h-4 w-4 text-blue-600 flex-shrink-0" />
          <span className="text-xs font-bold text-slate-800">
            Role Jurisdictions: <span className="text-blue-700 font-extrabold uppercase">{profile?.role ? profile.role.replace('_', ' ') : 'COORDINATOR'}</span>
          </span>
        </div>
        <p className="text-xs text-slate-500 font-medium">
          Admin creates Faculty Advisors • Faculty Advisors create Club Coordinators
        </p>
      </div>

      {/* Progress Summary Card */}
      <div className="p-6 rounded-3xl bg-white border border-slate-200 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h3 className="text-lg font-black text-slate-900 flex items-center gap-2">
            <span>Role Milestone Checklist</span>
            <span className="text-xs px-2.5 py-0.5 rounded-full font-bold bg-slate-100 text-slate-700">
              {completedCount} of {currentTasks.length} Done
            </span>
          </h3>
          <p className="text-xs text-slate-500 font-medium mt-1">
            Track your key club responsibilities. Click on any action button to immediately jump to the relevant module.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="w-36 h-3 rounded-full bg-slate-100 overflow-hidden">
            <div
              className="h-full rounded-full bg-gradient-to-r from-blue-500 to-emerald-500 transition-all duration-500"
              style={{ width: `${progressPercent}%` }}
            />
          </div>
          <span className="text-sm font-black text-slate-800">{progressPercent}%</span>
        </div>
      </div>

      {/* Tasks List */}
      <div className="space-y-4">
        {currentTasks.map((task, idx) => {
          const isDone = Boolean(completedTaskIds[task.id]);

          return (
            <div
              key={task.id}
              className={`p-6 rounded-3xl border-2 transition-all duration-200 bg-white shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-5 ${
                isDone
                  ? 'border-emerald-200 bg-emerald-50/20'
                  : 'border-slate-200 hover:border-blue-300 hover:shadow-md'
              }`}
            >
              <div className="flex items-start gap-4">
                {/* Checkbox */}
                <button
                  type="button"
                  onClick={() => toggleTask(task.id)}
                  className={`mt-1 flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-lg border-2 transition-all ${
                    isDone
                      ? 'border-emerald-500 bg-emerald-500 text-white shadow-sm'
                      : 'border-slate-300 bg-white hover:border-slate-400'
                  }`}
                  title={isDone ? 'Mark as incomplete' : 'Mark as complete'}
                >
                  {isDone && <Check className="h-4 w-4 stroke-[3]" />}
                </button>

                <div className="space-y-1.5">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="text-xs font-black text-slate-400">
                      TASK 0{idx + 1}
                    </span>
                    <Badge className="bg-slate-100 text-slate-700 text-[10px] font-bold">
                      {task.category}
                    </Badge>
                    <span
                      className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                        task.priority === 'High'
                          ? 'bg-rose-100 text-rose-700'
                          : 'bg-blue-100 text-blue-700'
                      }`}
                    >
                      {task.priority} Priority
                    </span>
                  </div>

                  <h4
                    className={`text-base font-bold text-slate-900 ${
                      isDone ? 'line-through text-slate-400' : ''
                    }`}
                  >
                    {task.title}
                  </h4>
                  <p className="text-xs sm:text-sm text-slate-600 font-medium leading-relaxed max-w-3xl">
                    {task.description}
                  </p>
                </div>
              </div>

              {/* Direct Action Button */}
              <div className="flex-shrink-0 flex items-center gap-2 pl-10 md:pl-0">
                <Button
                  variant={isDone ? 'outline' : 'gradient'}
                  size="sm"
                  onClick={() => handleAction(task)}
                  className="font-bold shadow-sm whitespace-nowrap text-xs"
                >
                  {task.actionLabel} <ArrowRight className="ml-1.5 h-3.5 w-3.5" />
                </Button>
              </div>
            </div>
          );
        })}
      </div>

      {/* CREATE FACULTY MODAL (Admin Only) */}
      <Modal
        open={facultyModalOpen}
        onClose={() => setFacultyModalOpen(false)}
        title="Create Faculty Coordinator Profile"
        description="Only Administrators can create Faculty accounts. This generates instant access credentials for faculty advisors."
      >
        <form onSubmit={handleCreateFaculty} className="space-y-4 pt-2">
          <Input
            label="Faculty Full Name"
            required
            value={facultyForm.name}
            onChange={(e) => setFacultyForm({ ...facultyForm, name: e.target.value })}
            placeholder="Dr. S. Kumar Ph.D"
          />
          <Input
            label="Official College Email"
            type="email"
            required
            value={facultyForm.email}
            onChange={(e) => setFacultyForm({ ...facultyForm, email: e.target.value })}
            placeholder="kumar.faculty@kongu.edu"
          />
          <Select
            label="Department"
            value={facultyForm.department}
            onChange={(e) => setFacultyForm({ ...facultyForm, department: e.target.value })}
            options={DEPARTMENTS.map((d) => ({ value: d, label: d }))}
          />
          <Input
            label="Contact Phone"
            value={facultyForm.phone}
            onChange={(e) => setFacultyForm({ ...facultyForm, phone: e.target.value })}
            placeholder="+91 98427 12345"
          />
          <Input
            label="Initial Account Password"
            required
            value={facultyForm.password}
            onChange={(e) => setFacultyForm({ ...facultyForm, password: e.target.value })}
            placeholder="Faculty@KEC2026"
          />

          <div className="p-3 rounded-xl bg-cyan-50 border border-cyan-200 text-xs text-cyan-900 font-semibold">
            Institutional Rule: This profile will be assigned the <strong>faculty_coordinator</strong> role with rights to create Club Coordinators.
          </div>

          <div className="flex justify-end gap-3 pt-3 border-t border-slate-200">
            <Button variant="outline" type="button" onClick={() => setFacultyModalOpen(false)}>
              Cancel
            </Button>
            <Button variant="gradient" type="submit" loading={submitting}>
              Create Faculty Account
            </Button>
          </div>
        </form>
      </Modal>

      {/* CREATE CLUB COORDINATOR MODAL (Faculty Coordinator or Admin) */}
      <Modal
        open={coordModalOpen}
        onClose={() => setCoordModalOpen(false)}
        title="Create Club Coordinator Profile"
        description="Faculty Coordinators & Admins can create student/staff coordinator accounts and assign them to clubs."
      >
        <form onSubmit={handleCreateCoordinator} className="space-y-4 pt-2">
          <Input
            label="Coordinator Name"
            required
            value={coordForm.name}
            onChange={(e) => setCoordForm({ ...coordForm, name: e.target.value })}
            placeholder="e.g. Anandha Kumar"
          />
          <Input
            label="Coordinator Email"
            type="email"
            required
            value={coordForm.email}
            onChange={(e) => setCoordForm({ ...coordForm, email: e.target.value })}
            placeholder="coord.hackers@college.edu"
          />
          <Select
            label="Assigned Club or Cell"
            required
            value={coordForm.organizationId}
            onChange={(e) => setCoordForm({ ...coordForm, organizationId: e.target.value })}
            options={orgs.map((o) => ({ value: o.id, label: `${o.name} (${o.type.toUpperCase()})` }))}
            placeholder="Select Organization to Lead"
          />
          <Select
            label="Department"
            value={coordForm.department}
            onChange={(e) => setCoordForm({ ...coordForm, department: e.target.value })}
            options={DEPARTMENTS.map((d) => ({ value: d, label: d }))}
          />
          <Input
            label="Initial Account Password"
            required
            value={coordForm.password}
            onChange={(e) => setCoordForm({ ...coordForm, password: e.target.value })}
            placeholder="Coord@KEC2026"
          />

          <div className="p-3 rounded-xl bg-blue-50 border border-blue-200 text-xs text-blue-900 font-semibold">
            Faculty Privilege: This account will receive <strong>club_coordinator</strong> credentials to take attendance and manage memberships for the selected organization.
          </div>

          <div className="flex justify-end gap-3 pt-3 border-t border-slate-200">
            <Button variant="outline" type="button" onClick={() => setCoordModalOpen(false)}>
              Cancel
            </Button>
            <Button variant="gradient" type="submit" loading={submitting}>
              Create Coordinator Account
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
}

