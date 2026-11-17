import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  Mail, Lock, User, Eye, EyeOff, Building2,
  ArrowRight, ArrowLeft
} from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/context/ToastContext';
import { Button } from '@/components/ui/Button';
import { DEPARTMENTS } from '@/lib/constants';

export function SignupPage() {
  const { signUp } = useAuth();
  const { toast } = useToast();
  const navigate = useNavigate();

  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [department, setDepartment] = useState('Information Technology');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (password.length < 6) {
      setError('Password must be at least 6 characters');
      return;
    }

    setLoading(true);
    const { error: signUpError } = await signUp(
      email.trim().toLowerCase(),
      password,
      name.trim(),
      'student',
      department || 'Information Technology'
    );

    if (signUpError) {
      setError(signUpError);
      toast(signUpError, 'error');
      setLoading(false);
    } else {
      toast('Student account created successfully! Welcome to ClubHub.', 'success');
      setLoading(false);
      navigate('/dashboard', { replace: true });
    }
  };

  return (
    <div className="min-h-screen w-full bg-[#f8f9fa] dark:bg-[#0f172a] flex flex-col justify-between py-8 px-4 font-sans text-[#202122] dark:text-[#f3f4f6]">
      {/* Top Simple Utility Bar */}
      <div className="max-w-md w-full mx-auto flex items-center justify-between text-xs text-[#54595d] dark:text-[#9ca3af] mb-4">
        <Link
          to="/login"
          className="inline-flex items-center gap-1.5 text-[#0645ad] dark:text-[#6b9eff] hover:underline font-medium"
        >
          <ArrowLeft className="h-3.5 w-3.5" />
          <span>Back to Login</span>
        </Link>
        <span className="font-serif">Kongu Engineering College</span>
      </div>

      {/* Centered Clean Signup Box */}
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
            Create student account
          </h1>
          <p className="text-xs text-[#54595d] dark:text-[#9ca3af] mt-0.5">
            Register your institutional profile to join campus clubs and RSVP for events.
          </p>
        </div>

        <div className="p-6 space-y-4">
          {/* Error Notice */}
          {error && (
            <div className="p-3 bg-[#fee7e6] dark:bg-[#451214] border border-[#d33]/50 text-xs text-[#d33] dark:text-red-200 rounded-[2px]">
              <p className="font-bold">Registration Error</p>
              <p className="mt-0.5">{error}</p>
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-3.5">
            <div>
              <label className="block text-xs font-bold text-[#202122] dark:text-[#f3f4f6] mb-1">
                Full Official Name
              </label>
              <div className="relative">
                <User className="absolute left-2.5 top-1/2 -translate-y-1/2 h-4 w-4 text-[#72777d]" />
                <input
                  type="text"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="e.g. Arun Kumar"
                  className="w-full h-9 rounded-[2px] border border-[#a2a9b1] dark:border-[#374151] bg-white dark:bg-[#111827] pl-8 pr-3 text-xs text-[#202122] dark:text-white placeholder-[#72777d] focus:border-[#0645ad] focus:outline-none focus:ring-1 focus:ring-[#0645ad]"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold text-[#202122] dark:text-[#f3f4f6] mb-1">
                College Email Address
              </label>
              <div className="relative">
                <Mail className="absolute left-2.5 top-1/2 -translate-y-1/2 h-4 w-4 text-[#72777d]" />
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="student@college.edu"
                  className="w-full h-9 rounded-[2px] border border-[#a2a9b1] dark:border-[#374151] bg-white dark:bg-[#111827] pl-8 pr-3 text-xs text-[#202122] dark:text-white placeholder-[#72777d] focus:border-[#0645ad] focus:outline-none focus:ring-1 focus:ring-[#0645ad]"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold text-[#202122] dark:text-[#f3f4f6] mb-1">
                Academic Department
              </label>
              <div className="relative">
                <Building2 className="absolute left-2.5 top-1/2 -translate-y-1/2 h-4 w-4 text-[#72777d] pointer-events-none" />
                <select
                  value={department}
                  onChange={(e) => setDepartment(e.target.value)}
                  required
                  className="w-full h-9 rounded-[2px] border border-[#a2a9b1] dark:border-[#374151] bg-white dark:bg-[#111827] pl-8 pr-3 text-xs text-[#202122] dark:text-white focus:border-[#0645ad] focus:outline-none focus:ring-1 focus:ring-[#0645ad]"
                >
                  {DEPARTMENTS.map((dept) => (
                    <option key={dept} value={dept}>
                      {dept}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold text-[#202122] dark:text-[#f3f4f6] mb-1">
                Create Password
              </label>
              <div className="relative">
                <Lock className="absolute left-2.5 top-1/2 -translate-y-1/2 h-4 w-4 text-[#72777d]" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="At least 6 characters"
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
              className="w-full h-9 text-xs font-bold mt-2"
            >
              Register Student Profile <ArrowRight className="ml-1.5 h-3.5 w-3.5" />
            </Button>
          </form>

          {/* Institutional note */}
          <div className="p-2.5 rounded-[2px] bg-[#f8f9fa] dark:bg-[#1f2937] border border-[#a2a9b1] dark:border-[#374151] text-[11px] text-[#54595d] dark:text-[#9ca3af]">
            <strong className="text-[#202122] dark:text-[#f3f4f6]">Staff Notice:</strong> Faculty and club coordinator accounts are provisioned directly by Institutional Administration.
          </div>

          {/* Login Link */}
          <div className="pt-3 border-t border-[#a2a9b1]/60 dark:border-[#374151] flex items-center justify-between text-xs">
            <span className="text-[#54595d] dark:text-[#9ca3af]">Already registered?</span>
            <Link to="/login" className="font-semibold text-[#0645ad] dark:text-[#6b9eff] hover:underline">
              Sign In to Portal →
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
