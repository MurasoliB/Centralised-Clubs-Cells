import { useAuth } from '@/context/AuthContext';
import { useTheme } from '@/context/ThemeContext';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { PageHeader } from '@/components/layout/PageHeader';
import { ROLE_LABELS } from '@/lib/constants';
import {
  Moon, Sun, Bell, Shield, User, Sparkles, CheckCircle2,
  Lock, KeyRound, Monitor, Smartphone, Globe
} from 'lucide-react';
import { initials } from '@/lib/utils';

export function SettingsPage() {
  const { profile } = useAuth();
  const { theme, toggleTheme } = useTheme();

  return (
    <div className="space-y-8 animate-fade-in w-full pb-12">
      <PageHeader
        title="Preferences & Settings"
        description="Configure your interface theme, notification protocols, and account security."
      />

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Left Column: Account Profile Overview */}
        <div className="md:col-span-1 space-y-6">
          <div className="p-6 rounded-3xl bg-gradient-to-br from-blue-600 to-indigo-700 text-white shadow-xl shadow-blue-500/10">
            <div className="flex items-center gap-4 mb-4">
              <div className="h-16 w-16 rounded-2xl bg-white/20 flex items-center justify-center text-2xl font-bold border border-white/20 shadow-md">
                {profile ? initials(profile.name) : 'U'}
              </div>
              <div>
                <h3 className="font-bold text-lg leading-tight">{profile?.name}</h3>
                <p className="text-xs text-blue-200 mt-0.5">{profile?.email}</p>
                <span className="inline-block mt-2 px-2.5 py-0.5 rounded-full text-[10px] font-extrabold uppercase bg-white/20 tracking-wider">
                  {profile ? ROLE_LABELS[profile.role] : 'Member'}
                </span>
              </div>
            </div>
            <div className="pt-4 border-t border-white/20 text-xs text-blue-100 space-y-1.5">
              <div className="flex justify-between">
                <span>Account Status:</span>
                <span className="font-semibold text-emerald-300">Active</span>
              </div>
              <div className="flex justify-between">
                <span>Department:</span>
                <span className="font-semibold text-white">{profile?.department || 'KEC'}</span>
              </div>
            </div>
          </div>

          <div className="p-6 rounded-3xl bg-slate-50 dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 space-y-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">Institutional Access</h4>
            <div className="space-y-2 text-xs text-slate-600 dark:text-slate-400">
              <p className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-500" /> Single Sign-On Ready
              </p>
              <p className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-500" /> Event Attendance Tracking
              </p>
              <p className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-500" /> Verified Certificate Issuance
              </p>
            </div>
          </div>
        </div>

        {/* Right Column: Appearance & Security Settings */}
        <div className="md:col-span-2 space-y-6">
          {/* Appearance Card */}
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2.5">
                <div className="p-2 rounded-xl bg-blue-500/10 text-blue-600 dark:text-blue-400">
                  <Sun className="h-5 w-5" />
                </div>
                <div>
                  <CardTitle>Interface Appearance</CardTitle>
                  <p className="text-xs text-slate-400">Personalize lighting mode to suit your study environment</p>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/40 border border-slate-200/60 dark:border-slate-800">
                <div className="space-y-1">
                  <p className="text-sm font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
                    {theme === 'dark' ? <Moon className="w-4 h-4 text-indigo-400" /> : <Sun className="w-4 h-4 text-amber-500" />}
                    Theme Mode: <span className="capitalize">{theme} Mode</span>
                  </p>
                  <p className="text-xs text-slate-500 dark:text-slate-400">
                    {theme === 'dark'
                      ? 'Dark mode is optimized to reduce eye strain during late night coding and work.'
                      : 'Light mode offers clear contrast with vivid vibrant brand colors.'}
                  </p>
                </div>
                <Button
                  variant="gradient"
                  onClick={toggleTheme}
                  className="flex-shrink-0 shadow-md shadow-blue-500/20"
                >
                  {theme === 'light' ? (
                    <>
                      <Moon className="h-4 w-4 mr-2" /> Switch to Dark
                    </>
                  ) : (
                    <>
                      <Sun className="h-4 w-4 mr-2" /> Switch to Light
                    </>
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Security Protocols */}
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2.5">
                <div className="p-2 rounded-xl bg-emerald-500/10 text-emerald-600 dark:text-emerald-400">
                  <Shield className="h-5 w-5" />
                </div>
                <div>
                  <CardTitle>Security & Data Governance</CardTitle>
                  <p className="text-xs text-slate-400">Row Level Security (RLS) encrypted database</p>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-start gap-3 p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/40 border border-slate-200/60 dark:border-slate-800">
                  <Lock className="w-5 h-5 text-indigo-500 flex-shrink-0 mt-0.5" />
                  <div>
                    <h5 className="text-sm font-bold text-slate-900 dark:text-slate-100">Session Authentication</h5>
                    <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                      Your identity token is securely verified through Supabase Auth using cryptographically signed JWTs with automatic refresh.
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3 p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/40 border border-slate-200/60 dark:border-slate-800">
                  <Globe className="w-5 h-5 text-blue-500 flex-shrink-0 mt-0.5" />
                  <div>
                    <h5 className="text-sm font-bold text-slate-900 dark:text-slate-100">Device Responsiveness</h5>
                    <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                      Full-screen fluid layout engine automatically optimizes cards, charts, and grids for ultra-wide laptop displays and mobile touchscreens alike.
                    </p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
