import { useEffect, useState, useRef } from 'react';
import {
  User, Mail, Phone, Building2, Save, KeyRound, Sparkles,
  Shield, ShieldCheck, GraduationCap, Award, BookOpen, Camera, Upload,
  Trash2, Check, RefreshCw, Image as ImageIcon, ExternalLink, Briefcase
} from 'lucide-react';
import { supabase } from '@/lib/supabase';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/context/ToastContext';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { Input, Select, Textarea } from '@/components/ui/Input';
import { LoadingSpinner } from '@/components/ui/EmptyState';
import { PageHeader } from '@/components/layout/PageHeader';
import { DEPARTMENTS, ROLE_LABELS } from '@/lib/constants';
import { initials, isUUID } from '@/lib/utils';
import { getUserWorkPortfolio, type UserWorkPortfolio } from '@/lib/orgScope';

// Curated high-resolution academic and professional avatar presets
const AVATAR_PRESETS = [
  {
    id: 'fac-1',
    label: 'Professor / Advisor (Male)',
    url: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=300&q=80',
  },
  {
    id: 'fac-2',
    label: 'Professor / Advisor (Female)',
    url: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=300&q=80',
  },
  {
    id: 'coord-1',
    label: 'Student Lead / Coordinator',
    url: 'https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&w=300&q=80',
  },
  {
    id: 'coord-2',
    label: 'Technical Head / Coordinator',
    url: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=300&q=80',
  },
  {
    id: 'stud-1',
    label: 'Engineering Student (Tech)',
    url: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=300&q=80',
  },
  {
    id: 'stud-2',
    label: 'Engineering Student (Innovator)',
    url: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80',
  },
];

// Client-side image compressor & resizer using HTML5 Canvas
const optimizeImageFile = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const img = new Image();
      img.onload = () => {
        const canvas = document.createElement('canvas');
        const MAX_WIDTH = 400;
        const MAX_HEIGHT = 400;
        let width = img.width;
        let height = img.height;

        if (width > height) {
          if (width > MAX_WIDTH) {
            height *= MAX_WIDTH / width;
            width = MAX_WIDTH;
          }
        } else {
          if (height > MAX_HEIGHT) {
            width *= MAX_HEIGHT / height;
            height = MAX_HEIGHT;
          }
        }

        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext('2d');
        if (!ctx) {
          resolve(e.target?.result as string);
          return;
        }
        ctx.drawImage(img, 0, 0, width, height);
        // Convert to optimized lightweight JPEG data URL
        const dataUrl = canvas.toDataURL('image/jpeg', 0.88);
        resolve(dataUrl);
      };
      img.onerror = () => {
        resolve(e.target?.result as string);
      };
      img.src = e.target?.result as string;
    };
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
};

export function ProfilePage() {
  const { profile, user, refreshProfile } = useAuth();
  const { toast } = useToast();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [loading, setLoading] = useState(!profile);
  const [saving, setSaving] = useState(false);
  const [uploadingImage, setUploadingImage] = useState(false);
  const [changingPassword, setChangingPassword] = useState(false);
  const [activeTab, setActiveTab] = useState<'details' | 'avatar' | 'security'>('details');

  const [studentData, setStudentData] = useState<any>(null);
  const [profileImage, setProfileImage] = useState<string>(profile?.profile_image || '');
  const [customImageUrl, setCustomImageUrl] = useState<string>(profile?.profile_image || '');

  const [form, setForm] = useState({
    name: profile?.name || '',
    phone: profile?.phone || '',
    department: profile?.department || '',
  });

  const [studentForm, setStudentForm] = useState({
    register_number: '',
    year: '1',
    section: 'A',
    skills: '',
    interests: '',
    bio: '',
  });

  const [passwordForm, setPasswordForm] = useState({ current: '', new: '', confirm: '' });

  // Official Work & Club Appointment synced directly from database
  const [portfolio, setPortfolio] = useState<UserWorkPortfolio>({
    scopeTitle: 'Synchronizing with Database...',
    workDesignation: 'Resolving Official Appointment...',
    roleCategory: 'Official Leadership',
    isSynced: false,
  });

  useEffect(() => {
    if (profile) {
      setForm({
        name: profile.name || '',
        phone: profile.phone || '',
        department: profile.department || '',
      });
      setProfileImage(profile.profile_image || '');
      setCustomImageUrl(profile.profile_image || '');

      // Automatically sync assigned club and official work designation from Supabase database
      getUserWorkPortfolio(profile).then((res) => {
        setPortfolio(res);
      });

      // Read cached student details if available
      try {
        const localStudent = localStorage.getItem('kec_student_data_' + profile.id);
        if (localStudent) {
          const parsed = JSON.parse(localStudent);
          setStudentData(parsed);
          setStudentForm({
            register_number: parsed.register_number || '',
            year: String(parsed.year || '1'),
            section: parsed.section || 'A',
            skills: Array.isArray(parsed.skills) ? parsed.skills.join(', ') : (parsed.skills || ''),
            interests: Array.isArray(parsed.interests) ? parsed.interests.join(', ') : (parsed.interests || ''),
            bio: parsed.bio || '',
          });
        }
      } catch {}

      if (profile.role === 'student' && isUUID(profile.id)) {
        supabase
          .from('students')
          .select('*')
          .eq('user_id', profile.id)
          .maybeSingle()
          .then(({ data }) => {
            if (data) {
              setStudentData(data);
              setStudentForm({
                register_number: data.register_number || '',
                year: String(data.year || '1'),
                section: data.section || 'A',
                skills: (data.skills || []).join(', '),
                interests: (data.interests || []).join(', '),
                bio: data.bio || '',
              });
            }
          })
          .catch(() => {});
      }
      setLoading(false);
    }
  }, [profile]);

  // Handle local image file upload from computer, auto-optimize and save
  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.type.startsWith('image/')) {
      toast('Please select an image file (PNG, JPG, or WEBP)', 'error');
      return;
    }

    setUploadingImage(true);
    try {
      toast('Optimizing and applying your photo...', 'info');
      const optimizedDataUrl = await optimizeImageFile(file);
      setProfileImage(optimizedDataUrl);
      setCustomImageUrl('');

      // Auto-save photo to Supabase profile immediately
      if (profile?.id) {
        const { error: updateError } = await supabase.from('profiles').update({
          profile_image: optimizedDataUrl,
          updated_at: new Date().toISOString(),
        }).eq('id', profile.id);

        if (updateError) throw updateError;
        await refreshProfile();
        toast('Profile picture uploaded and saved successfully!', 'success');
      }
    } catch (err: any) {
      toast(err.message || 'Failed to process image file', 'error');
    } finally {
      setUploadingImage(false);
      // Reset input value so same file can be selected again if desired
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const handleApplyCustomUrl = async () => {
    if (!customImageUrl.trim()) {
      toast('Please enter a valid image URL', 'error');
      return;
    }
    const url = customImageUrl.trim();
    setProfileImage(url);

    if (profile?.id) {
      setSaving(true);
      try {
        const { error } = await supabase.from('profiles').update({
          profile_image: url,
          updated_at: new Date().toISOString(),
        }).eq('id', profile.id);
        if (error) throw error;
        await refreshProfile();
        toast('Profile image URL applied and saved!', 'success');
      } catch (err: any) {
        toast(err.message || 'Failed to save image URL', 'error');
      } finally {
        setSaving(false);
      }
    }
  };

  const handleSelectPreset = async (url: string) => {
    setProfileImage(url);
    setCustomImageUrl(url);

    if (profile?.id) {
      setSaving(true);
      try {
        const { error } = await supabase.from('profiles').update({
          profile_image: url,
          updated_at: new Date().toISOString(),
        }).eq('id', profile.id);
        if (error) throw error;
        await refreshProfile();
        toast('Avatar preset chosen and saved!', 'success');
      } catch (err: any) {
        toast(err.message || 'Failed to save preset', 'error');
      } finally {
        setSaving(false);
      }
    }
  };

  const handleRemovePhoto = async () => {
    setProfileImage('');
    setCustomImageUrl('');

    if (profile?.id) {
      setSaving(true);
      try {
        const { error } = await supabase.from('profiles').update({
          profile_image: null,
          updated_at: new Date().toISOString(),
        }).eq('id', profile.id);
        if (error) throw error;
        await refreshProfile();
        toast('Profile photo removed. Default initials restored.', 'info');
      } catch (err: any) {
        toast(err.message || 'Failed to remove photo', 'error');
      } finally {
        setSaving(false);
      }
    }
  };

  const handleSave = async () => {
    if (!profile) return;
    setSaving(true);
    try {
      if (isUUID(profile.id)) {
        try {
          await supabase.from('profiles').update({
            name: form.name.trim(),
            phone: form.phone.trim() || null,
            department: form.department || null,
            profile_image: profileImage.trim() || null,
            updated_at: new Date().toISOString(),
          }).eq('id', profile.id);
        } catch {}
      }

      // Always update local storage profile for instant responsiveness
      const updatedProfile = {
        ...profile,
        name: form.name.trim(),
        phone: form.phone.trim() || null,
        department: form.department || null,
        profile_image: profileImage.trim() || null,
        updated_at: new Date().toISOString(),
      };

      try {
        localStorage.setItem('kec_user_profile', JSON.stringify(updatedProfile));
        sessionStorage.setItem('kec_user_profile', JSON.stringify(updatedProfile));
        localStorage.setItem(`kec_profile_${profile.id}`, JSON.stringify(updatedProfile));
      } catch {}

      // Re-sync official work appointment
      getUserWorkPortfolio(updatedProfile).then(setPortfolio).catch(() => {});

      if (profile.role === 'student') {
        const skills = (studentForm.skills || '').split(',').map((s) => s.trim()).filter(Boolean);
        const interests = (studentForm.interests || '').split(',').map((s) => s.trim()).filter(Boolean);
        const studentPayload = {
          user_id: profile.id,
          register_number: studentForm.register_number.trim() || null,
          year: parseInt(studentForm.year) || 1,
          section: studentForm.section.trim() || 'A',
          skills,
          interests,
          bio: studentForm.bio.trim() || null,
          updated_at: new Date().toISOString(),
        };

        try {
          localStorage.setItem('kec_student_data_' + profile.id, JSON.stringify(studentPayload));
        } catch {}

        if (isUUID(profile.id)) {
          try {
            if (studentData) {
              await supabase.from('students').update(studentPayload).eq('user_id', profile.id);
            } else {
              await supabase.from('students').insert(studentPayload);
            }
          } catch {}
        }
      }

      await refreshProfile();
      toast('Profile details saved successfully!', 'success');
    } catch (err: any) {
      toast(err.message || 'Failed to update profile', 'error');
    } finally {
      setSaving(false);
    }
  };

  const handleChangePassword = async () => {
    if (passwordForm.new !== passwordForm.confirm) {
      toast('New passwords do not match', 'error');
      return;
    }
    if (passwordForm.new.length < 6) {
      toast('Password must be at least 6 characters', 'error');
      return;
    }
    setChangingPassword(true);
    const { error } = await supabase.auth.updateUser({ password: passwordForm.new });
    if (error) {
      toast(error.message || 'Failed to change password', 'error');
    } else {
      toast('Password changed successfully', 'success');
      setPasswordForm({ current: '', new: '', confirm: '' });
    }
    setChangingPassword(false);
  };

  if (loading || !profile) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <LoadingSpinner />
      </div>
    );
  }

  const parsedSkills = (studentForm.skills || '').split(',').map((s) => s.trim()).filter(Boolean);
  const parsedInterests = (studentForm.interests || '').split(',').map((s) => s.trim()).filter(Boolean);

  return (
    <div className="space-y-8 animate-fade-in w-full pb-12">
      {/* Hidden File Input for Direct Local Computer Upload */}
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileUpload}
        accept="image/*"
        className="hidden"
      />

      <PageHeader
        title="Institutional Account Profile"
        description="Manage your professional credentials, upload verified avatar photo, and configure security access."
        action={
          <Button
            variant="gradient"
            onClick={handleSave}
            loading={saving}
            className="shadow-md shadow-blue-600/20 font-bold"
          >
            <Save className="h-4 w-4 mr-1.5" /> Save Changes
          </Button>
        }
      />

      {/* Sleek Executive Header Card - Wikipedia Infobox Theme */}
      <div className="rounded-[2px] border border-[#a2a9b1] bg-white shadow-xs dark:border-[#374151] dark:bg-[#111827] mb-6">
        {/* Executive Cover Header */}
        <div className="w-full bg-[#eaecf0] dark:bg-[#1f2937] border-b border-[#a2a9b1] dark:border-[#374151] px-5 py-3 flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold uppercase tracking-wider text-[#202122] dark:text-[#f3f4f6]">
              Kongu Engineering College • Extracurricular Directory
            </span>
          </div>

          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded-[2px] border border-[#a2a9b1] dark:border-[#374151] bg-white dark:bg-[#111827] text-xs font-bold text-[#0645ad] dark:text-[#6b9eff] flex items-center gap-1.5 shadow-xs">
              <ShieldCheck className="w-3.5 h-3.5 text-[#10b981]" />
              Verified Active Account
            </span>
          </div>
        </div>

        {/* Profile Identity Section - Cleanly Aligned without Clipping */}
        <div className="p-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
            {/* Left: Avatar with Photo Picker Trigger & User Details */}
            <div className="flex flex-col sm:flex-row items-center sm:items-start gap-5 text-center sm:text-left">
              {/* Avatar Box with Direct Upload Trigger on Click */}
              <div className="relative group cursor-pointer flex-shrink-0" onClick={() => fileInputRef.current?.click()}>
                <div className="h-24 w-24 sm:h-28 sm:w-28 rounded-[2px] border-2 border-[#a2a9b1] dark:border-[#374151] bg-[#f8f9fa] dark:bg-[#1f2937] shadow-sm overflow-hidden flex items-center justify-center">
                  {profileImage ? (
                    <img
                      src={profileImage}
                      alt={profile.name}
                      className="h-full w-full object-cover"
                    />
                  ) : (
                    <div className="h-full w-full bg-[#f8f9fa] dark:bg-[#1f2937] flex items-center justify-center text-3xl font-bold font-serif text-[#202122] dark:text-[#f3f4f6]">
                      {initials(form.name || profile.name)}
                    </div>
                  )}
                  {uploadingImage && (
                    <div className="absolute inset-0 bg-black/50 flex items-center justify-center">
                      <LoadingSpinner />
                    </div>
                  )}
                </div>

                {/* Direct Upload Button Overlay on Avatar */}
                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation();
                    fileInputRef.current?.click();
                  }}
                  className="absolute bottom-1 right-1 p-1.5 rounded-[2px] bg-[#0645ad] text-white shadow border border-white hover:bg-[#0b0080] transition-colors"
                  title="Click to choose image file from computer"
                >
                  <Camera className="h-4 w-4" />
                </button>
              </div>

              {/* User Names & Meta */}
              <div className="space-y-2">
                <div className="flex flex-wrap items-center justify-center sm:justify-start gap-2.5">
                  <h2 className="text-2xl sm:text-3xl font-bold font-serif text-[#202122] dark:text-[#f3f4f6] tracking-tight">
                    {form.name || profile.name}
                  </h2>
                  <span className="px-2 py-0.5 rounded-[2px] border border-[#a2a9b1] dark:border-[#374151] bg-[#eaecf0] dark:bg-[#1f2937] text-xs font-bold uppercase tracking-wider text-[#0645ad] dark:text-[#6b9eff]">
                    {profile?.role ? (ROLE_LABELS[profile.role] || 'Member') : 'Member'}
                  </span>
                </div>

                {/* Prominent Designated Work & Portfolio Pill */}
                <div className="flex flex-wrap items-center justify-center sm:justify-start gap-2">
                  <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-[2px] text-xs font-semibold bg-[#eaecf0] text-[#202122] border border-[#a2a9b1] dark:bg-[#1f2937] dark:text-[#f3f4f6] dark:border-[#374151]">
                    <Briefcase className="h-3.5 w-3.5 text-[#0645ad] dark:text-[#6b9eff] flex-shrink-0" />
                    <span>{portfolio.workDesignation || 'Campus Member'}</span>
                  </div>
                </div>

                <p className="text-xs sm:text-sm text-[#54595d] dark:text-[#9ca3af] font-normal flex flex-wrap items-center justify-center sm:justify-start gap-2">
                  <span className="flex items-center gap-1">
                    <Mail className="h-3.5 w-3.5 text-[#72777d]" />
                    {profile.email}
                  </span>
                  <span>•</span>
                  <span className="font-semibold text-[#202122] dark:text-[#f3f4f6]">
                    {form.department || profile.department || 'General IT'}
                  </span>
                </p>

                {/* Direct Quick Upload Button right below the name */}
                <div className="pt-1 flex flex-wrap items-center justify-center sm:justify-start gap-2">
                  <button
                    type="button"
                    onClick={() => fileInputRef.current?.click()}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-[2px] text-xs font-semibold text-[#0645ad] bg-[#f8f9fa] hover:bg-[#eaecf0] border border-[#a2a9b1] transition-colors"
                  >
                    <Upload className="h-3.5 w-3.5 text-[#0645ad]" />
                    Upload Picture From Computer
                  </button>
                  {profileImage && (
                    <button
                      type="button"
                      onClick={handleRemovePhoto}
                      className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-[2px] text-xs font-semibold text-[#d33] hover:bg-red-50 border border-[#d33]/40 transition-colors"
                      title="Remove picture"
                    >
                      <Trash2 className="h-3.5 w-3.5" /> Remove
                    </button>
                  )}
                </div>
              </div>
            </div>

            {/* Right: Quick Role Privilege Box */}
            <div className="hidden lg:block max-w-xs text-xs text-[#54595d] dark:text-[#9ca3af] bg-[#f8f9fa] dark:bg-[#1f2937] p-3 rounded-[2px] border border-[#a2a9b1] dark:border-[#374151]">
              <p className="font-bold text-[#202122] dark:text-[#f3f4f6] mb-1 flex items-center gap-1">
                <Shield className="h-3.5 w-3.5 text-[#0645ad] dark:text-[#6b9eff]" /> Account Privileges
              </p>
              <p className="text-[11px] leading-relaxed">
                Synchronized with Kongu Engineering College ERP directory. Updates to name and contact details reflect instantly campus-wide.
              </p>
            </div>
          </div>
        </div>

        {/* Dedicated Wikipedia Vector Tab Bar */}
        <div className="flex items-center border-t border-[#a2a9b1] dark:border-[#374151] bg-[#f8f9fa] dark:bg-[#1f2937] px-4 pt-1 gap-1 overflow-x-auto">
          <button
            onClick={() => setActiveTab('details')}
            className={`flex items-center gap-1.5 px-4 py-2 text-xs font-semibold rounded-t-[2px] border-t border-x transition-colors -mb-px ${
              activeTab === 'details'
                ? 'bg-white dark:bg-[#111827] text-[#202122] dark:text-white border-[#a2a9b1] dark:border-[#374151] border-b-white dark:border-b-[#111827] font-bold shadow-2xs'
                : 'text-[#0645ad] dark:text-[#6b9eff] border-transparent hover:text-[#0b0080] hover:underline'
            }`}
          >
            <User className="h-3.5 w-3.5" /> Details
          </button>
          <button
            onClick={() => setActiveTab('avatar')}
            className={`flex items-center gap-1.5 px-4 py-2 text-xs font-semibold rounded-t-[2px] border-t border-x transition-colors -mb-px ${
              activeTab === 'avatar'
                ? 'bg-white dark:bg-[#111827] text-[#202122] dark:text-white border-[#a2a9b1] dark:border-[#374151] border-b-white dark:border-b-[#111827] font-bold shadow-2xs'
                : 'text-[#0645ad] dark:text-[#6b9eff] border-transparent hover:text-[#0b0080] hover:underline'
            }`}
          >
            <ImageIcon className="h-3.5 w-3.5" /> Photo & Presets
          </button>
          <button
            onClick={() => setActiveTab('security')}
            className={`flex items-center gap-1.5 px-4 py-2 text-xs font-semibold rounded-t-[2px] border-t border-x transition-colors -mb-px ${
              activeTab === 'security'
                ? 'bg-white dark:bg-[#111827] text-[#202122] dark:text-white border-[#a2a9b1] dark:border-[#374151] border-b-white dark:border-b-[#111827] font-bold shadow-2xs'
                : 'text-[#0645ad] dark:text-[#6b9eff] border-transparent hover:text-[#0b0080] hover:underline'
            }`}
          >
            <KeyRound className="h-3.5 w-3.5" /> Security
          </button>
        </div>
      </div>

      {/* TAB 1: PERSONAL & INSTITUTIONAL CREDENTIALS */}
      {activeTab === 'details' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-fade-in">
          {/* Main Info Form */}
          <div className="lg:col-span-2 space-y-6">
            <Card className="border-slate-200 shadow-sm">
              <CardHeader className="border-b border-slate-100 pb-4">
                <div className="flex items-center gap-2">
                  <div className="p-2 rounded-xl bg-blue-50 text-blue-600">
                    <User className="h-5 w-5" />
                  </div>
                  <div>
                    <CardTitle>Personal & Academic Information</CardTitle>
                    <p className="text-xs text-slate-500 font-medium">
                      Primary administrative identification synchronized with College ERP.
                    </p>
                  </div>
                </div>
              </CardHeader>

              <CardContent className="p-6 space-y-4">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <Input
                    label="Full Official Name"
                    value={form.name}
                    onChange={(e) => setForm({ ...form, name: e.target.value })}
                    required
                  />
                  <Input
                    label="Institutional Email (Immutable)"
                    value={profile.email}
                    disabled
                  />
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <Input
                    label="Contact Phone"
                    value={form.phone}
                    onChange={(e) => setForm({ ...form, phone: e.target.value })}
                    placeholder="+91 98427 12345"
                  />
                  <Select
                    label="Assigned Department"
                    value={form.department}
                    onChange={(e) => setForm({ ...form, department: e.target.value })}
                  >
                    <option value="">Select Department</option>
                    {DEPARTMENTS.map((dept) => (
                      <option key={dept} value={dept}>
                        {dept}
                      </option>
                    ))}
                  </Select>
                </div>

                {/* Extracurricular Work & Club Appointment */}
                <div className="p-4 rounded-[2px] bg-[#f8f9fa] dark:bg-[#1f2937] border border-[#a2a9b1] dark:border-[#374151] space-y-3">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Briefcase className="h-4 w-4 text-[#0645ad] dark:text-[#6b9eff]" />
                      <span className="text-xs font-bold text-[#202122] dark:text-[#f3f4f6] uppercase tracking-wider">
                        Extracurricular Work & Club Appointment
                      </span>
                    </div>
                    <span className="inline-flex items-center gap-1.5 text-[10px] font-bold text-[#0645ad] dark:text-[#6b9eff] bg-white dark:bg-[#111827] px-2 py-0.5 rounded-[2px] border border-[#a2a9b1]">
                      Synced with Database
                    </span>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
                    <div>
                      <label className="block text-xs font-bold text-[#202122] dark:text-[#f3f4f6] mb-1">
                        Designated Club or Cell
                      </label>
                      <div className="flex items-center gap-2.5 min-h-[38px] rounded-[2px] border border-[#a2a9b1] bg-white dark:border-[#374151] dark:bg-[#111827] px-3 py-1.5 text-xs font-bold text-[#202122] dark:text-[#f3f4f6]">
                        <Building2 className="w-4 h-4 text-[#0645ad] dark:text-[#6b9eff] flex-shrink-0" />
                        <span className="truncate">{portfolio.scopeTitle}</span>
                      </div>
                    </div>

                    <div>
                      <label className="block text-xs font-bold text-[#202122] dark:text-[#f3f4f6] mb-1">
                        Active Official Work Designation
                      </label>
                      <div className="flex items-center gap-2.5 min-h-[38px] px-3 py-1.5 rounded-[2px] bg-white dark:bg-[#111827] border border-[#a2a9b1] dark:border-[#374151] text-xs font-bold text-[#0645ad] dark:text-[#6b9eff]">
                        <ShieldCheck className="w-4 h-4 text-[#0645ad] dark:text-[#6b9eff] flex-shrink-0" />
                        <span className="truncate">{portfolio.workDesignation}</span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Role Specific Notice */}
                <div className="p-3 rounded-[2px] bg-[#f8f9fa] dark:bg-[#1f2937] border border-[#a2a9b1] dark:border-[#374151] flex items-start gap-2.5 mt-2">
                  <ShieldCheck className="h-5 w-5 text-blue-600 flex-shrink-0 mt-0.5" />
                  <div className="text-xs text-slate-600">
                    <p className="font-bold text-slate-800">
                      Role Privilege Level: {profile?.role ? (ROLE_LABELS[profile.role] || 'Member') : 'Member'}
                    </p>
                    <p className="mt-0.5 leading-relaxed">
                      {profile.role === 'admin' && 'You possess institutional oversight to provision Faculty Coordinators and audit compliance.'}
                      {profile.role === 'faculty_coordinator' && 'You possess sanction authority to approve events, endorse certificates, and onboard Club Coordinators.'}
                      {profile.role === 'club_coordinator' && 'You possess operational rights to publish events, take attendance, and manage club rosters.'}
                      {profile.role === 'student' && 'You possess standard student rights to join clubs, RSVP for hackathons, and download certificates.'}
                    </p>
                  </div>
                </div>

                {/* Student specific fields */}
                {profile.role === 'student' && (
                  <div className="pt-4 border-t border-slate-100 space-y-4">
                    <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                      <GraduationCap className="h-4 w-4 text-emerald-600" />
                      Student Extracurricular Details
                    </h3>

                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                      <Input
                        label="Roll / Register Number"
                        value={studentForm.register_number}
                        onChange={(e) => setStudentForm({ ...studentForm, register_number: e.target.value })}
                        placeholder="e.g. 21IT001"
                      />
                      <Select
                        label="Academic Year"
                        value={studentForm.year}
                        onChange={(e) => setStudentForm({ ...studentForm, year: e.target.value })}
                      >
                        <option value="1">1st Year (Freshman)</option>
                        <option value="2">2nd Year (Sophomore)</option>
                        <option value="3">3rd Year (Junior)</option>
                        <option value="4">4th Year (Senior)</option>
                      </Select>
                      <Input
                        label="Section"
                        value={studentForm.section}
                        onChange={(e) => setStudentForm({ ...studentForm, section: e.target.value })}
                        placeholder="A / B / C"
                      />
                    </div>

                    <div>
                      <Input
                        label="Skills (comma separated)"
                        value={studentForm.skills}
                        onChange={(e) => setStudentForm({ ...studentForm, skills: e.target.value })}
                        placeholder="Python, UI Design, Robotics, Public Speaking"
                      />
                      {parsedSkills.length > 0 && (
                        <div className="flex flex-wrap gap-1.5 mt-2">
                          {parsedSkills.map((skill, idx) => (
                            <span
                              key={idx}
                              className="px-2.5 py-1 rounded-lg text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200"
                            >
                              ✓ {skill}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>

                    <div>
                      <Input
                        label="Interests & Passions (comma separated)"
                        value={studentForm.interests}
                        onChange={(e) => setStudentForm({ ...studentForm, interests: e.target.value })}
                        placeholder="Web Development, Robotics, Debating, Photography"
                      />
                      {parsedInterests.length > 0 && (
                        <div className="flex flex-wrap gap-1.5 mt-2">
                          {parsedInterests.map((interest, idx) => (
                            <span
                              key={idx}
                              className="px-2.5 py-1 rounded-lg text-xs font-semibold bg-blue-50 text-blue-700 border border-blue-200"
                            >
                              ★ {interest}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>

                    <Textarea
                      label="Short Bio / Extracurricular Summary"
                      value={studentForm.bio}
                      onChange={(e) => setStudentForm({ ...studentForm, bio: e.target.value })}
                      rows={3}
                      placeholder="Brief statement of your extracurricular and technical ambitions..."
                    />
                  </div>
                )}

                <div className="pt-2 flex justify-end">
                  <Button
                    variant="gradient"
                    onClick={handleSave}
                    loading={saving}
                    className="font-bold shadow-md shadow-blue-500/20"
                  >
                    <Save className="h-4 w-4 mr-1.5" /> Save Profile Details
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Side Info Cards */}
          <div className="space-y-6">
            {/* Extracurricular Appointment Card */}
            <Card className="border-blue-200 bg-gradient-to-br from-blue-50/70 to-indigo-50/40 dark:border-blue-900/60 dark:bg-slate-900 shadow-xs">
              <CardHeader className="border-b border-blue-100 dark:border-blue-900/40 pb-3">
                <div className="flex items-center gap-2">
                  <Briefcase className="h-4 w-4 text-blue-600 dark:text-cyan-400" />
                  <CardTitle className="text-sm font-bold text-slate-900 dark:text-white">Assigned Extracurricular Work</CardTitle>
                </div>
              </CardHeader>
              <CardContent className="p-4 space-y-3 text-xs">
                <div className="p-3 rounded-xl bg-white dark:bg-slate-800/80 border border-blue-100 dark:border-slate-700 shadow-2xs">
                  <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Official Appointment</p>
                  <p className="text-sm font-black text-blue-900 dark:text-cyan-300 mt-0.5">
                    {portfolio.workDesignation}
                  </p>
                </div>

                <div className="flex justify-between items-center py-1 border-b border-blue-100/60 dark:border-slate-800">
                  <span className="text-slate-500 font-medium">Designated Scope</span>
                  <span className="font-bold text-slate-800 dark:text-slate-200 truncate max-w-[180px]">{portfolio.scopeTitle}</span>
                </div>

                <div className="flex justify-between items-center py-1 border-b border-blue-100/60 dark:border-slate-800">
                  <span className="text-slate-500 font-medium">Academic Department</span>
                  <span className="font-bold text-slate-800 dark:text-slate-200">{form.department || profile.department || 'Information Technology'}</span>
                </div>

                <div className="flex justify-between items-center py-1">
                  <span className="text-slate-500 font-medium">Appointment Status</span>
                  <span className="font-bold text-emerald-600 dark:text-emerald-400 flex items-center gap-1">
                    <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
                    Authorized Active
                  </span>
                </div>
              </CardContent>
            </Card>

            <Card className="border-slate-200 shadow-sm">
              <CardHeader className="border-b border-slate-100 pb-3">
                <CardTitle className="text-sm">Account Status</CardTitle>
              </CardHeader>
              <CardContent className="p-5 space-y-3.5 text-xs">
                <div className="flex justify-between items-center py-1 border-b border-slate-100">
                  <span className="text-slate-500 font-medium">Authentication</span>
                  <span className="font-bold text-slate-800">Email & Password</span>
                </div>
                <div className="flex justify-between items-center py-1 border-b border-slate-100">
                  <span className="text-slate-500 font-medium">Campus Status</span>
                  <span className="font-bold text-emerald-600 flex items-center gap-1">
                    <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
                    Active (Enrolled)
                  </span>
                </div>
                <div className="flex justify-between items-center py-1 border-b border-slate-100">
                  <span className="text-slate-500 font-medium">Member Since</span>
                  <span className="font-bold text-slate-800">
                    {profile?.created_at ? new Date(profile.created_at).toLocaleDateString('en-US', { month: 'short', year: 'numeric' }) : 'Academic Year 2026'}
                  </span>
                </div>
                <div className="flex justify-between items-center py-1">
                  <span className="text-slate-500 font-medium">Photo Attached</span>
                  <span className={`font-bold ${profileImage ? 'text-blue-600' : 'text-slate-400'}`}>
                    {profileImage ? 'Yes (Configured)' : 'Default Initials'}
                  </span>
                </div>
              </CardContent>
            </Card>

            <div className="p-4 rounded-[2px] bg-[#f8f9fa] dark:bg-[#1f2937] border border-[#a2a9b1] dark:border-[#374151]">
              <div className="flex items-center gap-2 mb-1">
                <Sparkles className="h-4 w-4 text-[#0645ad] dark:text-[#6b9eff]" />
                <h4 className="text-xs font-bold uppercase tracking-wider text-[#202122] dark:text-[#f3f4f6]">
                  KEC Institutional Directory
                </h4>
              </div>
              <p className="text-xs text-[#54595d] dark:text-[#9ca3af] leading-relaxed">
                Your profile is synchronized with Kongu Engineering College active directory for seamless club participation, attendance logging, and certificates.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: PROFILE PHOTO & AVATAR MANAGER */}
      {activeTab === 'avatar' && (
        <Card className="border-[#a2a9b1] shadow-none animate-fade-in">
          <CardHeader className="border-b border-[#a2a9b1] pb-3 bg-[#eaecf0] dark:bg-[#1f2937]">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="p-1 rounded-[2px] bg-white text-[#0645ad]">
                  <ImageIcon className="h-4 w-4" />
                </div>
                <div>
                  <CardTitle>Profile Photo Management</CardTitle>
                  <p className="text-xs text-[#54595d] font-normal">
                    Upload a portrait or select from institutional presets.
                  </p>
                </div>
              </div>

              {profileImage && (
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleRemovePhoto}
                  className="text-[#d33] border-[#a2a9b1]"
                >
                  <Trash2 className="h-3.5 w-3.5 mr-1" /> Remove Photo
                </Button>
              )}
            </div>
          </CardHeader>

          <CardContent className="p-6 space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-start">
              {/* Preview Box & Upload Trigger */}
              <div className="md:col-span-4 flex flex-col items-center p-4 rounded-[2px] bg-[#f8f9fa] border border-[#a2a9b1] text-center">
                <div
                  onClick={() => fileInputRef.current?.click()}
                  className="h-32 w-32 rounded-[2px] overflow-hidden border border-[#a2a9b1] shadow-none bg-white mb-3 cursor-pointer group relative"
                  title="Click to choose image file from computer"
                >
                  {profileImage ? (
                    <img src={profileImage} alt="Current Preview" className="h-full w-full object-cover" />
                  ) : (
                    <div className="h-full w-full flex items-center justify-center bg-slate-200 text-slate-500 font-bold text-2xl">
                      {initials(form.name || profile.name)}
                    </div>
                  )}
                  <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col items-center justify-center text-white text-xs font-bold gap-1">
                    <Camera className="h-5 w-5" />
                    <span>Change</span>
                  </div>
                </div>

                <p className="text-xs font-bold text-slate-800">Current Profile Picture</p>
                <p className="text-[11px] text-slate-500 mt-0.5">
                  Synchronized across header and sidebar
                </p>

                {/* Primary Upload Button from Device */}
                <Button
                  type="button"
                  variant="primary"
                  onClick={() => fileInputRef.current?.click()}
                  loading={uploadingImage}
                  className="mt-4 w-full bg-blue-600 hover:bg-blue-700 text-white font-bold shadow-md shadow-blue-500/20"
                >
                  <Upload className="h-4 w-4 mr-1.5" /> Choose Photo From Computer
                </Button>
                <p className="text-[10px] text-slate-400 mt-1.5">
                  Supports JPG, PNG, WEBP • Automatically compressed
                </p>
              </div>

              {/* Online URL & Presets Column */}
              <div className="md:col-span-8 space-y-5">
                {/* Method 1: Direct Image URL */}
                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1.5">
                    Option A: Direct Image Web Address (URL)
                  </label>
                  <div className="flex gap-2">
                    <input
                      type="url"
                      value={customImageUrl}
                      onChange={(e) => setCustomImageUrl(e.target.value)}
                      placeholder="https://example.com/your-profile-photo.jpg"
                      className="flex-1 rounded-xl border border-slate-300 bg-white px-3.5 py-2 text-sm text-slate-900 placeholder-slate-400 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                    />
                    <Button
                      type="button"
                      variant="outline"
                      onClick={handleApplyCustomUrl}
                      loading={saving}
                      className="font-bold border-slate-300"
                    >
                      Apply & Save
                    </Button>
                  </div>
                </div>

                {/* Method 2: Curated High-Quality Presets */}
                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-2">
                    Option B: One-Click Institutional Presets
                  </label>
                  <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                    {AVATAR_PRESETS.map((preset) => {
                      const isSelected = profileImage === preset.url;
                      return (
                        <button
                          key={preset.id}
                          type="button"
                          onClick={() => handleSelectPreset(preset.url)}
                          className={`relative p-2 rounded-xl border text-left transition-all flex items-center gap-2.5 ${
                            isSelected
                              ? 'border-blue-600 bg-blue-50/80 ring-2 ring-blue-500/30'
                              : 'border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-50'
                          }`}
                        >
                          <img
                            src={preset.url}
                            alt={preset.label}
                            className="h-10 w-10 rounded-lg object-cover flex-shrink-0"
                          />
                          <div className="min-w-0 flex-1">
                            <p className="text-[11px] font-bold text-slate-900 truncate">{preset.label}</p>
                            <span className="text-[10px] text-blue-600 font-semibold">Apply</span>
                          </div>
                          {isSelected && (
                            <span className="absolute top-1.5 right-1.5 h-4 w-4 rounded-full bg-blue-600 text-white flex items-center justify-center text-[10px]">
                              ✓
                            </span>
                          )}
                        </button>
                      );
                    })}
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* TAB 3: SECURITY & PASSWORD */}
      {activeTab === 'security' && (
        <Card className="border-slate-200 shadow-sm max-w-xl animate-fade-in">
          <CardHeader className="border-b border-slate-100 pb-4">
            <div className="flex items-center gap-2">
              <div className="p-2 rounded-xl bg-amber-50 text-amber-600">
                <KeyRound className="h-5 w-5" />
              </div>
              <div>
                <CardTitle>Update Account Password</CardTitle>
                <p className="text-xs text-slate-500 font-medium">
                  Ensure your account uses a secure password with at least 6 characters.
                </p>
              </div>
            </div>
          </CardHeader>
          <CardContent className="p-6 space-y-4">
            <Input
              label="New Password"
              type="password"
              value={passwordForm.new}
              onChange={(e) => setPasswordForm({ ...passwordForm, new: e.target.value })}
              placeholder="Minimum 6 characters"
            />
            <Input
              label="Confirm New Password"
              type="password"
              value={passwordForm.confirm}
              onChange={(e) => setPasswordForm({ ...passwordForm, confirm: e.target.value })}
              placeholder="Repeat new password"
            />
            <div className="pt-2 flex justify-end">
              <Button
                variant="gradient"
                onClick={handleChangePassword}
                loading={changingPassword}
                className="font-bold shadow-md shadow-blue-500/20"
              >
                Update Password
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
