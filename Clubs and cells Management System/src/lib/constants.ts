import {
  LayoutDashboard, Users, Building2, Calendar, Award, Bell, FileBarChart,
  Settings, User, LogOut, Briefcase, Megaphone, GraduationCap, ClipboardCheck,
  Ticket, Shield,
} from 'lucide-react';
import type { UserRole } from '@/types/database';

export interface NavItem {
  label: string;
  path: string;
  icon: typeof LayoutDashboard;
}

export const ROLE_LABELS: Record<UserRole, string> = {
  admin: 'Administrator',
  faculty_coordinator: 'Faculty Coordinator',
  club_coordinator: 'Club/Cell Coordinator',
  student: 'Student',
};

export const MEMBERSHIP_STATUS_STYLES: Record<string, string> = {
  pending: 'bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-300',
  approved: 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300',
  rejected: 'bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300',
  suspended: 'bg-orange-100 text-orange-800 dark:bg-orange-900/40 dark:text-orange-300',
  left: 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400',
};

export const EVENT_STATUS_STYLES: Record<string, string> = {
  upcoming: 'bg-blue-100 text-blue-800 dark:bg-blue-900/40 dark:text-blue-300',
  ongoing: 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300',
  completed: 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400',
  cancelled: 'bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300',
};

export const ATTENDANCE_STATUS_STYLES: Record<string, string> = {
  present: 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300',
  absent: 'bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300',
  late: 'bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-300',
  excused: 'bg-blue-100 text-blue-800 dark:bg-blue-900/40 dark:text-blue-300',
};

export const ORG_STATUS_STYLES: Record<string, string> = {
  active: 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300',
  inactive: 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400',
};

export const DEPARTMENTS = [
  'Computer Science',
  'Electronics',
  'Mechanical',
  'Civil',
  'Information Technology',
  'Electrical',
  'Chemical',
  'Biotechnology',
];

export const EVENT_TYPES = [
  'workshop', 'seminar', 'competition', 'cultural', 'technical', 'social', 'meeting', 'other',
];

export const ACHIEVEMENT_TYPES = [
  'competition', 'project', 'certification', 'workshop', 'paper_presentation', 'sports', 'cultural', 'other',
];

export const ACHIEVEMENT_LEVELS = ['college', 'state', 'national', 'international'];

export const NAV_ITEMS: NavItem[] = [
  { label: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
  { label: 'Students', path: '/students', icon: GraduationCap, },
  { label: 'Organizations', path: '/organizations', icon: Building2 },
  { label: 'Events', path: '/events', icon: Calendar },
  { label: 'Achievements', path: '/achievements', icon: Award },
  { label: 'Announcements', path: '/announcements', icon: Megaphone },
  { label: 'Notifications', path: '/notifications', icon: Bell },
  { label: 'Reports', path: '/reports', icon: FileBarChart },
  { label: 'Profile', path: '/profile', icon: User },
  { label: 'Settings', path: '/settings', icon: Settings },
];

export const ADMIN_NAV_ITEMS: NavItem[] = [
  { label: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
  { label: 'Clubs & Cells', path: '/organizations', icon: Building2 },
  { label: 'Events', path: '/events', icon: Calendar },
  { label: 'Faculty Staff', path: '/staff', icon: Users },
  { label: 'Memberships', path: '/memberships', icon: Briefcase },
  { label: 'Attendance', path: '/attendance', icon: ClipboardCheck },
  { label: 'Achievements', path: '/achievements', icon: Award },
  { label: 'Announcements', path: '/announcements', icon: Megaphone },
  { label: 'Reports', path: '/reports', icon: FileBarChart },
  { label: 'Students', path: '/students', icon: GraduationCap },
  { label: 'Audit Logs', path: '/audit-logs', icon: Shield },
  { label: 'Notifications', path: '/notifications', icon: Bell },
  { label: 'Profile', path: '/profile', icon: User },
  { label: 'Settings', path: '/settings', icon: Settings },
];

export const FACULTY_NAV_ITEMS: NavItem[] = [
  { label: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
  { label: 'Clubs & Cells', path: '/organizations', icon: Building2 },
  { label: 'Events', path: '/events', icon: Calendar },
  { label: 'Coordinators', path: '/staff', icon: Users },
  { label: 'Attendance Audit', path: '/attendance', icon: ClipboardCheck },
  { label: 'Reports', path: '/reports', icon: FileBarChart },
  { label: 'Announcements', path: '/announcements', icon: Megaphone },
  { label: 'Students', path: '/students', icon: GraduationCap },
  { label: 'Notifications', path: '/notifications', icon: Bell },
  { label: 'Profile', path: '/profile', icon: User },
  { label: 'Settings', path: '/settings', icon: Settings },
];

export const STUDENT_NAV_ITEMS: NavItem[] = [
  { label: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
  { label: 'Clubs & Cells', path: '/organizations', icon: Building2 },
  { label: 'My Memberships', path: '/memberships', icon: Briefcase },
  { label: 'Events', path: '/events', icon: Calendar },
  { label: 'My Achievements', path: '/achievements', icon: Award },
  { label: 'Announcements', path: '/announcements', icon: Megaphone },
  { label: 'Notifications', path: '/notifications', icon: Bell },
  { label: 'Profile', path: '/profile', icon: User },
];

export const COORDINATOR_NAV_ITEMS: NavItem[] = [
  { label: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
  { label: 'Clubs & Cells', path: '/organizations', icon: Building2 },
  { label: 'Events', path: '/events', icon: Calendar },
  { label: 'Memberships', path: '/memberships', icon: Ticket },
  { label: 'Attendance', path: '/attendance', icon: ClipboardCheck },
  { label: 'Achievements', path: '/achievements', icon: Award },
  { label: 'Announcements', path: '/announcements', icon: Megaphone },
  { label: 'Reports', path: '/reports', icon: FileBarChart },
  { label: 'Students', path: '/students', icon: GraduationCap },
  { label: 'Notifications', path: '/notifications', icon: Bell },
  { label: 'Profile', path: '/profile', icon: User },
];

export function getNavItems(role: UserRole): NavItem[] {
  switch (role) {
    case 'admin': return ADMIN_NAV_ITEMS;
    case 'faculty_coordinator': return FACULTY_NAV_ITEMS;
    case 'club_coordinator': return COORDINATOR_NAV_ITEMS;
    case 'student': return STUDENT_NAV_ITEMS;
    default: return NAV_ITEMS;
  }
}
