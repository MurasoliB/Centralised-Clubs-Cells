import { useState, useEffect } from 'react';
import { NavLink, useNavigate, useLocation, Link } from 'react-router-dom';
import {
  Menu, X, LogOut, Bell, Moon, Sun,
  User, ExternalLink
} from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import { useTheme } from '@/context/ThemeContext';
import { getNavItems } from '@/lib/constants';
import { cn, initials } from '@/lib/utils';
import { supabase } from '@/lib/supabase';
import { cache } from '@/lib/cache';
import { ErrorBoundary } from '@/components/ui/ErrorBoundary';

export function AppLayout({ children }: { children: React.ReactNode }) {
  const { profile, signOut } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [unreadNotifications, setUnreadNotifications] = useState(0);

  // Nav items for the current role
  const allNavItems = profile ? getNavItems(profile.role) : [];
  const horizontalNavItems = allNavItems.filter(
    (item) => !['/notifications', '/profile', '/settings'].includes(item.path)
  );

  useEffect(() => {
    setMobileMenuOpen(false);
  }, [location.pathname]);

  // Gentle notifications polling
  useEffect(() => {
    if (!profile?.id) return;
    const fetchUnread = () => {
      supabase
        .from('notifications')
        .select('id', { count: 'exact', head: true })
        .eq('user_id', profile.id)
        .eq('is_read', false)
        .then(({ count }) => {
          setUnreadNotifications(count || 0);
        });
    };

    fetchUnread();
    const interval = setInterval(fetchUnread, 60000);
    return () => clearInterval(interval);
  }, [profile?.id]);

  // Silent pre-warming for zero-latency route switching
  useEffect(() => {
    if (!profile) return;
    const prewarmTimer = setTimeout(async () => {
      try {
        if (!cache.has('organizations_list')) {
          const [orgsRes, membersRes, eventsRes] = await Promise.all([
            supabase.from('organizations').select('*').order('name'),
            supabase.from('memberships').select('organization_id').eq('status', 'approved'),
            supabase.from('events').select('organization_id'),
          ]);
          if (orgsRes.data) {
            const memberMap: Record<string, number> = {};
            (membersRes.data || []).forEach((m) => { memberMap[m.organization_id] = (memberMap[m.organization_id] || 0) + 1; });
            const eventMap: Record<string, number> = {};
            (eventsRes.data || []).forEach((e) => { eventMap[e.organization_id] = (eventMap[e.organization_id] || 0) + 1; });
            const fullOrgs = orgsRes.data.map((org) => ({
              ...org,
              memberCount: memberMap[org.id] || 0,
              eventCount: eventMap[org.id] || 0,
            }));
            cache.set('organizations_list', fullOrgs);
          }
        }

        if (!cache.has('events_list')) {
          const [eventsRes, regsRes] = await Promise.all([
            supabase.from('events').select('*, organization:organizations(name, type, short_name)').order('start_date', { ascending: true }),
            supabase.from('event_registrations').select('event_id').neq('participation_status', 'cancelled'),
          ]);
          if (eventsRes.data) {
            const regMap: Record<string, number> = {};
            (regsRes.data || []).forEach((r) => { regMap[r.event_id] = (regMap[r.event_id] || 0) + 1; });
            const fullEvents = eventsRes.data.map((e) => ({
              ...e,
              registrationCount: regMap[e.id] || 0,
            }));
            cache.set('events_list', fullEvents);
          }
        }

        if (!cache.has('announcements_list')) {
          const { data: annData } = await supabase
            .from('announcements')
            .select('*, organization:organizations(name, type)')
            .order('publish_date', { ascending: false });
          if (annData) cache.set('announcements_list', annData);
        }

        const achKey = `achievements_${profile.id || 'all'}`;
        if (!cache.has(achKey)) {
          let achQuery = supabase
            .from('achievements')
            .select('*, student:profiles!achievements_student_id_fkey(name, department), organization:organizations(name)')
            .order('achievement_date', { ascending: false });
          if (profile.role === 'student') {
            achQuery = achQuery.eq('student_id', profile.id);
          }
          const { data: achData } = await achQuery;
          if (achData) cache.set(achKey, achData);
        }

        if (profile.role === 'student') {
          const memKey = `memberships_${profile.id}`;
          if (!cache.has(memKey)) {
            const { data: memData } = await supabase
              .from('memberships')
              .select('*, organization:organizations(*)')
              .eq('student_id', profile.id)
              .order('created_at', { ascending: false });
            if (memData) cache.set(memKey, { my: memData, pending: [], all: [] });
          }
        }
      } catch {}
    }, 50);

    return () => clearTimeout(prewarmTimer);
  }, [profile?.id]);

  const handleSignOut = async () => {
    await signOut();
    navigate('/login');
  };

  const getRoleDisplayName = (role?: string) => {
    switch (role) {
      case 'admin':
        return 'Administrator';
      case 'faculty_coordinator':
        return 'Faculty Advisor';
      case 'club_coordinator':
        return 'Student Coordinator';
      default:
        return 'Student Member';
    }
  };

  return (
    <div className="min-h-screen w-full bg-[#f6f8fa] text-[#202122] dark:bg-[#0b0f17] dark:text-[#e5e7eb] flex flex-col font-sans">
      {/* Top Utility Bar (Classic Wikipedia User Tools Strip) */}
      <div className="w-full border-b border-[#a2a9b1] dark:border-[#374151] bg-[#f8f9fa] dark:bg-[#111827] text-xs px-4 sm:px-8 py-1.5">
        <div className="max-w-7xl mx-auto flex items-center justify-between text-[#54595d] dark:text-[#9ca3af]">
          {/* Institution Notice */}
          <div className="flex items-center gap-2">
            <span className="font-semibold text-[#202122] dark:text-[#f3f4f6]">Kongu Engineering College</span>
            <span className="text-[#a2a9b1] dark:text-[#4b5563]">•</span>
            <span>Department of Information Technology</span>
          </div>

          {/* User Utility Links (Wikipedia Vector Personal Tools) */}
          <div className="flex items-center gap-3">
            {profile && (
              <>
                <Link
                  to="/profile"
                  className="wiki-link flex items-center gap-1 font-medium"
                  title="View user profile"
                >
                  <User className="h-3.5 w-3.5 inline" />
                  <span>{profile.name}</span>
                  <span className="text-[11px] text-[#54595d] dark:text-[#9ca3af]">
                    ({getRoleDisplayName(profile.role)})
                  </span>
                </Link>
                <span className="text-[#a2a9b1] dark:text-[#4b5563]">|</span>
              </>
            )}

            <Link
              to="/notifications"
              className="wiki-link flex items-center gap-1 font-medium"
              title="View notifications"
            >
              <Bell className="h-3.5 w-3.5 inline" />
              <span>Alerts</span>
              {unreadNotifications > 0 && (
                <span className="bg-[#cc0000] text-white text-[10px] px-1 font-bold rounded-[2px] leading-tight">
                  {unreadNotifications}
                </span>
              )}
            </Link>

            <span className="text-[#a2a9b1] dark:text-[#4b5563]">|</span>

            <button
              onClick={toggleTheme}
              className="wiki-link flex items-center gap-1 cursor-pointer font-medium"
              title={theme === 'light' ? 'Switch to Dark Mode' : 'Switch to Light Mode'}
            >
              {theme === 'light' ? <Moon className="h-3.5 w-3.5 inline" /> : <Sun className="h-3.5 w-3.5 inline" />}
              <span>{theme === 'light' ? 'Dark theme' : 'Light theme'}</span>
            </button>

            <span className="text-[#a2a9b1] dark:text-[#4b5563]">|</span>

            <button
              onClick={handleSignOut}
              className="wiki-link flex items-center gap-1 cursor-pointer font-medium text-[#d33] dark:text-[#f87171]"
              title="Sign Out"
            >
              <LogOut className="h-3.5 w-3.5 inline" />
              <span>Log out</span>
            </button>
          </div>
        </div>
      </div>

      {/* Main Header / Banner */}
      <header className="w-full bg-white dark:bg-[#111827] border-b border-[#a2a9b1] dark:border-[#374151]">
        <div className="max-w-7xl mx-auto px-4 sm:px-8 py-3.5 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Link to="/dashboard" className="flex items-baseline gap-2 group text-decoration-none">
              <span className="font-serif text-2xl sm:text-3xl font-normal tracking-tight text-[#202122] dark:text-[#f9fafb]">
                ClubHub
              </span>
              <span className="text-xs sm:text-sm font-sans text-[#54595d] dark:text-[#9ca3af] tracking-normal">
                Extracurricular Affairs Repository
              </span>
            </Link>
          </div>

          {/* Mobile hamburger menu toggle */}
          <div className="lg:hidden">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-1.5 border border-[#a2a9b1] rounded-[2px] text-[#202122] dark:text-[#e5e7eb] bg-[#f8f9fa] dark:bg-[#1f2937]"
              aria-label="Toggle menu"
            >
              {mobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            </button>
          </div>
        </div>

        {/* Vector Tabs Row - Aligned with Wikipedia page tabs */}
        <div className="max-w-7xl mx-auto px-4 sm:px-8 -mb-[1px] flex items-center justify-between overflow-x-auto">
          <nav className="flex items-end gap-1" role="tablist">
            {horizontalNavItems.map((item) => {
              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  className={({ isActive }) =>
                    cn(
                      'inline-flex items-center gap-1.5 px-3 sm:px-4 py-2 text-xs sm:text-[13px] border border-b-0 border-[#a2a9b1] dark:border-[#374151] font-medium transition-colors whitespace-nowrap',
                      isActive
                        ? 'bg-white dark:bg-[#111827] text-[#202122] dark:text-[#f9fafb] font-bold border-t-2 border-t-[#0645ad] dark:border-t-[#6b9eff] -mb-px z-10'
                        : 'bg-[#f8f9fa] dark:bg-[#1f2937] text-[#0645ad] dark:text-[#6b9eff] hover:bg-white dark:hover:bg-[#111827] hover:underline'
                    )
                  }
                >
                  <span>{item.label}</span>
                </NavLink>
              );
            })}
          </nav>
        </div>

        {/* Mobile Navigation Dropdown */}
        {mobileMenuOpen && (
          <div className="lg:hidden border-t border-[#a2a9b1] dark:border-[#374151] bg-[#f8f9fa] dark:bg-[#1f2937] p-3">
            <div className="grid grid-cols-2 gap-1 text-xs">
              {allNavItems.map((item) => (
                <NavLink
                  key={item.path}
                  to={item.path}
                  onClick={() => setMobileMenuOpen(false)}
                  className={({ isActive }) =>
                    cn(
                      'px-2 py-1.5 border border-[#a2a9b1] dark:border-[#374151] rounded-[2px]',
                      isActive
                        ? 'bg-white dark:bg-[#111827] font-bold text-[#202122] dark:text-[#f9fafb] border-l-2 border-l-[#0645ad]'
                        : 'bg-white dark:bg-[#111827] text-[#0645ad] dark:text-[#6b9eff] hover:underline'
                    )
                  }
                >
                  {item.label}
                </NavLink>
              ))}
            </div>
          </div>
        )}
      </header>

      {/* Main Content Area - Boxed & Strictly Aligned */}
      <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-8 py-5 sm:py-6">
        <div className="bg-white dark:bg-[#111827] border border-[#a2a9b1] dark:border-[#374151] p-4 sm:p-6 shadow-sm min-h-[500px]">
          <ErrorBoundary fallbackTitle="Page Content Recovery">
            {children}
          </ErrorBoundary>
        </div>
      </main>

      {/* Classic Wikipedia Vector Footer */}
      <footer className="w-full border-t border-[#a2a9b1] dark:border-[#374151] bg-[#f8f9fa] dark:bg-[#111827] text-[#54595d] dark:text-[#9ca3af] text-xs py-5 px-4 sm:px-8 mt-auto">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3 text-center sm:text-left">
          <div>
            <p>This repository portal is managed by the Department of Information Technology, Kongu Engineering College.</p>
            <p className="mt-0.5 text-[11px] text-[#72777d]">Records, leadership assignments, and participation audits are subject to Institutional Guidelines.</p>
          </div>
          <div className="flex items-center gap-3">
            <span className="wiki-link cursor-pointer">Privacy policy</span>
            <span>•</span>
            <span className="wiki-link cursor-pointer">About ClubHub</span>
            <span>•</span>
            <span className="wiki-link cursor-pointer">Disclaimers</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
