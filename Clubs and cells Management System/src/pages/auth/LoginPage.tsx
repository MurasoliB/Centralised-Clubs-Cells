import { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation, useSearchParams } from 'react-router-dom';
import {
  Mail, Lock, Eye, EyeOff,
  ArrowRight, ArrowLeft, LogOut, Info
} from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/context/ToastContext';
import { Button } from '@/components/ui/Button';
import { ROLE_LABELS } from '@/lib/constants';
import { supabase } from '@/lib/supabase';

export function LoginPage() {
  const { signIn, signOut, session, profile } = useAuth();
  const { toast } = useToast();
  const navigate = useNavigate();
  const location = useLocation();
  const [searchParams] = useSearchParams();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Pre-warm TCP/TLS connection to Supabase Auth so login is instantaneous
  useEffect(() => {
    supabase.auth.getSession().catch(() => {});
  }, []);

  // Pre-populate credentials if a role param is provided in URL (e.g. /login?role=student)
  useEffect(() => {
    const roleParam = searchParams.get('role');
    if (roleParam === 'student') {
      setEmail('student@college.edu');
      setPassword('Student@KEC2026');
    } else if (roleParam === 'coordinator' || roleParam === 'club_coordinator') {
      setEmail('coordinator@college.edu');
      setPassword('coord123456');
    } else if (roleParam === 'faculty' || roleParam === 'faculty_coordinator') {
      setEmail('faculty@college.edu');
      setPassword('faculty123456');
    } else if (roleParam === 'admin') {
      setEmail('admin@college.edu');
      setPassword('admin123456');
    }
  }, [searchParams]);

  const fillCredentials = (roleEmail: string, rolePass: string) => {
    setEmail(roleEmail);
    setPassword(rolePass);
    setError('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    const cleanEmail = email.trim().toLowerCase();

    // If currently already authenticated with this exact user, instant bypass
    if (session?.user?.email?.toLowerCase() === cleanEmail && profile) {
      toast('Welcome back to ClubHub!', 'success');
      const from = (location.state as any)?.from?.pathname;
      const destination = from && from !== '/login' ? from : '/dashboard';
      navigate(destination, { replace: true });
      return;
    }

    setLoading(true);

    const { error: signInError } = await signIn(cleanEmail, password);
    if (signInError) {
      setError(signInError);
      toast(signInError, 'error');
      setLoading(false);
    } else {
      toast('Signed in successfully!', 'success');
      setLoading(false);
      const from = (location.state as any)?.from?.pathname;
      const destination = from && from !== '/login' ? from : '/dashboard';
      navigate(destination, { replace: true });
    }
  };

  return (
    <div className="min-h-screen w-full bg-[#f8f9fa] dark:bg-[#0f172a] flex flex-col justify-between py-8 px-4 font-sans text-[#202122] dark:text-[#f3f4f6]">
      {/* Top Simple Utility Bar */}
      <div className="max-w-md w-full mx-auto flex items-center justify-between text-xs text-[#54595d] dark:text-[#9ca3af] mb-4">
        <Link
          to="/"
          className="inline-flex items-center gap-1.5 text-[#0645ad] dark:text-[#6b9eff] hover:underline font-medium"
        >
          <ArrowLeft className="h-3.5 w-3.5" />
          <span>Back to Home</span>
        </Link>
        <span className="font-serif">Kongu Engineering College</span>
      </div>

      {/* Centered Clean Login Box */}
      <div className="max-w-md w-full mx-auto bg-white dark:bg-[#111827] border border-[#a2a9b1] dark:border-[#374151] rounded-[2px] shadow-xs">
        {/* Box Header */}
        <div className="bg-[#eaecf0] dark:bg-[#1f2937] border-b border-[#a2a9b1] dark:border-[#374151] px-6 py-4">
          <div className="flex items-center gap-2 mb-1">
            <span className="font-serif text-lg font-bold text-[#202122] dark:text-[#f3f4f6]">ClubHub</span>
            <span className="text-[10px] font-bold px-1.5 py-0.5 rounded-[2px] bg-white dark:bg-[#111827] border border-[#a2a9b1] dark:border-[#374151] text-[#0645ad] dark:text-[#6b9eff]">
              KEC IT
            </span>
          </div>
          <h1 className="text-xl font-serif font-bold text-[#202122] dark:text-[#f3f4f6]">
            Log in
          </h1>
          <p className="text-xs text-[#54595d] dark:text-[#9ca3af] mt-0.5">
            Sign in with your institutional credentials to access the portal.
          </p>
        </div>

        <div className="p-6 space-y-5">
          {/* Active Session Notice */}
          {session && profile && (
            <div className="p-3 bg-[#eaf3ff] dark:bg-[#1e293b] border border-[#3366cc]/40 dark:border-blue-900 rounded-[2px] flex items-center justify-between gap-3 text-xs">
              <div className="min-w-0">
                <p className="font-bold text-[#202122] dark:text-white truncate">
                  Signed in as {profile.name}
                </p>
                <p className="text-[11px] text-[#54595d] dark:text-slate-400">
                  {ROLE_LABELS[profile.role] || profile.role}
                </p>
              </div>
              <div className="flex items-center gap-2 flex-shrink-0">
                <Link to="/dashboard">
                  <Button size="sm" className="text-xs h-7 px-2.5">
                    Dashboard →
                  </Button>
                </Link>
                <button
                  type="button"
                  onClick={async () => {
                    await signOut();
                    setEmail('');
                    setPassword('');
                    toast('Signed out successfully.', 'info');
                  }}
                  className="h-7 px-2 rounded-[2px] border border-[#a2a9b1] hover:bg-[#eaecf0] text-xs font-medium text-[#54595d]"
                  title="Sign out"
                >
                  <LogOut className="h-3.5 w-3.5" />
                </button>
              </div>
            </div>
          )}

          {/* Error Notice */}
          {error && (
            <div className="p-3 bg-[#fee7e6] dark:bg-[#451214] border border-[#d33]/50 text-xs text-[#d33] dark:text-red-200 rounded-[2px]">
              <p className="font-bold">Login Error</p>
              <p className="mt-0.5">{error}</p>
            </div>
          )}

          {/* Login Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-bold text-[#202122] dark:text-[#f3f4f6] mb-1">
                College Email
              </label>
              <div className="relative">
                <Mail className="absolute left-2.5 top-1/2 -translate-y-1/2 h-4 w-4 text-[#72777d]" />
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => {
                    setEmail(e.target.value);
                    if (error) setError('');
                  }}
                  placeholder="name@college.edu"
                  className="w-full h-9 rounded-[2px] border border-[#a2a9b1] dark:border-[#374151] bg-white dark:bg-[#111827] pl-8 pr-3 text-xs text-[#202122] dark:text-white placeholder-[#72777d] focus:border-[#0645ad] focus:outline-none focus:ring-1 focus:ring-[#0645ad]"
                />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between mb-1">
                <label className="text-xs font-bold text-[#202122] dark:text-[#f3f4f6]">
                  Password
                </label>
              </div>
              <div className="relative">
                <Lock className="absolute left-2.5 top-1/2 -translate-y-1/2 h-4 w-4 text-[#72777d]" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  required
                  value={password}
                  onChange={(e) => {
                    setPassword(e.target.value);
                    if (error) setError('');
                  }}
                  placeholder="••••••••"
                  className="w-full h-9 rounded-[2px] border border-[#a2a9b1] dark:border-[#374151] bg-white dark:bg-[#111827] pl-8 pr-9 text-xs text-[#202122] dark:text-white placeholder-[#72777d] focus:border-[#0645ad] focus:outline-none focus:ring-1 focus:ring-[#0645ad]"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-2.5 top-1/2 -translate-y-1/2 text-[#72777d] hover:text-[#202122] dark:hover:text-white"
                  title={showPassword ? 'Hide password' : 'Show password'}
                >
                  {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
            </div>

            <Button
              type="submit"
              loading={loading}
              className="w-full h-9 text-xs font-bold"
            >
              Sign In to Portal <ArrowRight className="ml-1.5 h-3.5 w-3.5" />
            </Button>
          </form>

          {/* Quick Demo Autofill Links */}
          <div className="pt-4 border-t border-[#a2a9b1]/60 dark:border-[#374151] space-y-2">
            <div className="flex items-center justify-between text-xs text-[#54595d] dark:text-[#9ca3af]">
              <span className="font-semibold flex items-center gap-1">
                <Info className="h-3 w-3 text-[#0645ad] dark:text-[#6b9eff]" /> Demo Accounts (1-click fill)
              </span>
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-1.5">
              <button
                type="button"
                onClick={() => fillCredentials('student@college.edu', 'Student@KEC2026')}
                className="px-2 py-1.5 text-xs font-medium rounded-[2px] bg-[#f8f9fa] dark:bg-[#1f2937] border border-[#a2a9b1] dark:border-[#374151] hover:bg-[#eaecf0] hover:text-[#0645ad] text-[#202122] dark:text-[#f3f4f6] transition-colors text-center"
              >
                🎓 Student
              </button>
              <button
                type="button"
                onClick={() => fillCredentials('coordinator@college.edu', 'coord123456')}
                className="px-2 py-1.5 text-xs font-medium rounded-[2px] bg-[#f8f9fa] dark:bg-[#1f2937] border border-[#a2a9b1] dark:border-[#374151] hover:bg-[#eaecf0] hover:text-[#0645ad] text-[#202122] dark:text-[#f3f4f6] transition-colors text-center"
              >
                ⚡ Lead
              </button>
              <button
                type="button"
                onClick={() => fillCredentials('faculty@college.edu', 'faculty123456')}
                className="px-2 py-1.5 text-xs font-medium rounded-[2px] bg-[#f8f9fa] dark:bg-[#1f2937] border border-[#a2a9b1] dark:border-[#374151] hover:bg-[#eaecf0] hover:text-[#0645ad] text-[#202122] dark:text-[#f3f4f6] transition-colors text-center"
              >
                👨‍🏫 Faculty
              </button>
              <button
                type="button"
                onClick={() => fillCredentials('admin@college.edu', 'admin123456')}
                className="px-2 py-1.5 text-xs font-medium rounded-[2px] bg-[#f8f9fa] dark:bg-[#1f2937] border border-[#a2a9b1] dark:border-[#374151] hover:bg-[#eaecf0] hover:text-[#0645ad] text-[#202122] dark:text-[#f3f4f6] transition-colors text-center"
              >
                🛡️ Admin
              </button>
            </div>
          </div>

          {/* Create Account Link */}
          <div className="pt-3 border-t border-[#a2a9b1]/60 dark:border-[#374151] flex items-center justify-between text-xs">
            <span className="text-[#54595d] dark:text-[#9ca3af]">New student?</span>
            <Link to="/signup" className="font-semibold text-[#0645ad] dark:text-[#6b9eff] hover:underline">
              Create Student Account →
            </Link>
          </div>
        </div>
      </div>

      {/* Footer Notice */}
      <div className="max-w-md w-full mx-auto text-center text-[11px] text-[#72777d] mt-4">
        <p>Kongu Engineering College Extracurricular Affairs Directory &bull; Academic Year 2026&ndash;2027</p>
      </div>
    </div>
  );
}
