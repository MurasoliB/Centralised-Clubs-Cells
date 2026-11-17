import { useEffect, useState } from 'react';
import { Plus, Award, Download, Check } from 'lucide-react';
import { supabase } from '@/lib/supabase';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/context/ToastContext';
import { Button } from '@/components/ui/Button';
import { Modal } from '@/components/ui/Modal';
import { Input, Select, Textarea } from '@/components/ui/Input';
import { SearchBar } from '@/components/ui/SearchBar';
import { EmptyState, LoadingSpinner } from '@/components/ui/EmptyState';
import { PageHeader } from '@/components/layout/PageHeader';
import { ACHIEVEMENT_TYPES, ACHIEVEMENT_LEVELS } from '@/lib/constants';
import { formatDate, exportToCsv } from '@/lib/utils';
import { cache } from '@/lib/cache';

export function AchievementsPage() {
  const { profile } = useAuth();
  const { toast } = useToast();
  const cacheKey = `achievements_${profile?.id || 'all'}`;
  const cachedAchievements = cache.get<any[]>(cacheKey);
  const [achievements, setAchievements] = useState<any[]>(cachedAchievements || []);
  const [loading, setLoading] = useState(!cachedAchievements);
  const [search, setSearch] = useState('');
  const [typeFilter, setTypeFilter] = useState('');
  const [levelFilter, setLevelFilter] = useState('');
  const [modalOpen, setModalOpen] = useState(false);
  const [creating, setCreating] = useState(false);
  const [myOrgs, setMyOrgs] = useState<any[]>([]);
  const [newAchievement, setNewAchievement] = useState({
    title: '', description: '', type: 'competition', level: 'college',
    organization_id: '', event_name: '', position: '', achievement_date: '',
    certificate_url: '',
  });

  const isAdmin = profile?.role === 'admin';
  const isCoordinator = profile?.role === 'faculty_coordinator' || profile?.role === 'club_coordinator';
  const isStudent = profile?.role === 'student';
  const canCreate = Boolean(profile);

  useEffect(() => {
    loadAchievements();
    loadOrgs();
  }, [profile?.id]);

  const loadOrgs = async () => {
    const { data } = await supabase.from('organizations').select('id, name').eq('status', 'active');
    setMyOrgs(data || []);
  };

  const loadAchievements = async () => {
    if (!cache.has(cacheKey)) {
      setLoading(true);
    }
    try {
      let query = supabase
        .from('achievements')
        .select('*, student:profiles!achievements_student_id_fkey(name, department), organization:organizations(name)')
        .order('achievement_date', { ascending: false });

      if (isStudent && profile) {
        query = query.eq('student_id', profile.id);
      }

      const { data, error } = await query;
      if (error) throw error;
      const list = data || [];
      setAchievements(list);
      cache.set(cacheKey, list);
    } catch {
      toast('Failed to load achievements', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async () => {
    if (!newAchievement.title || !newAchievement.achievement_date) {
      toast('Please provide at least a title and achievement date', 'error');
      return;
    }

    setCreating(true);
    try {
      const { error } = await supabase.from('achievements').insert({
        student_id: profile?.id,
        title: newAchievement.title,
        description: newAchievement.description,
        type: newAchievement.type,
        level: newAchievement.level,
        organization_id: newAchievement.organization_id || null,
        event_name: newAchievement.event_name,
        position: newAchievement.position,
        achievement_date: newAchievement.achievement_date,
        certificate_url: newAchievement.certificate_url,
        verified: isAdmin || isCoordinator,
        verified_by: (isAdmin || isCoordinator) ? profile?.id : null,
        verified_at: (isAdmin || isCoordinator) ? new Date().toISOString() : null,
      });

      if (error) throw error;
      toast('Achievement recorded successfully', 'success');
      setModalOpen(false);
      setNewAchievement({
        title: '', description: '', type: 'competition', level: 'college',
        organization_id: '', event_name: '', position: '', achievement_date: '',
        certificate_url: '',
      });
      loadAchievements();
    } catch (err: any) {
      toast(err.message || 'Failed to submit achievement', 'error');
    } finally {
      setCreating(false);
    }
  };

  const verifyAchievement = async (id: string) => {
    try {
      const { error } = await supabase
        .from('achievements')
        .update({
          verified: true,
          verified_by: profile?.id,
          verified_at: new Date().toISOString(),
        })
        .eq('id', id);

      if (error) throw error;
      toast('Achievement verified successfully', 'success');
      loadAchievements();
    } catch {
      toast('Failed to verify achievement', 'error');
    }
  };

  const handleExport = () => {
    exportToCsv('campus_extracurricular_honors.csv', achievements.map((a) => ({
      title: a.title,
      student: a.student?.name,
      department: a.student?.department,
      organization: a.organization?.name,
      level: a.level,
      position: a.position,
      date: a.achievement_date,
      verified: a.verified ? 'Yes' : 'No',
    })));
    toast('Honors roll exported to CSV', 'success');
  };

  const filteredAchievements = achievements.filter((a) => {
    if (typeFilter && a.type !== typeFilter) return false;
    if (levelFilter && a.level !== levelFilter) return false;
    if (search.trim()) {
      const q = search.toLowerCase();
      return (
        a.title?.toLowerCase().includes(q) ||
        a.student?.name?.toLowerCase().includes(q) ||
        a.organization?.name?.toLowerCase().includes(q)
      );
    }
    return true;
  });

  return (
    <div className="space-y-6 font-sans w-full">
      <PageHeader
        title="Extracurricular Honors & Trophy Roll"
        subtitle="Institutional registry of tournament medals, competitive hackathon laurels, and verified credentials"
        action={
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm" onClick={handleExport}>
              <Download className="h-3.5 w-3.5 mr-1" /> Export CSV
            </Button>
            {canCreate && (
              <Button variant="primary" size="sm" onClick={() => setModalOpen(true)}>
                <Plus className="h-3.5 w-3.5 mr-1" /> Log Achievement
              </Button>
            )}
          </div>
        }
      />

      {/* Filter Toolbar */}
      <div className="p-3 border border-[#a2a9b1] dark:border-[#374151] bg-[#f8f9fa] dark:bg-[#111827] flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 text-xs rounded-[2px]">
        <div className="flex-1 max-w-sm">
          <SearchBar
            value={search}
            onChange={setSearch}
            placeholder="Search honors by title, student, or tournament..."
          />
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <Select
            value={typeFilter}
            onChange={(e) => setTypeFilter(e.target.value)}
            options={ACHIEVEMENT_TYPES.map((t) => ({ value: t, label: t.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase()) }))}
            placeholder="All Event Types"
            className="text-xs w-36"
          />
          <Select
            value={levelFilter}
            onChange={(e) => setLevelFilter(e.target.value)}
            options={ACHIEVEMENT_LEVELS.map((l) => ({ value: l, label: l.charAt(0).toUpperCase() + l.slice(1) }))}
            placeholder="All Competition Tiers"
            className="text-xs w-40"
          />
        </div>
      </div>

      {/* Honors Wikitable */}
      {loading && achievements.length === 0 ? (
        <LoadingSpinner />
      ) : filteredAchievements.length === 0 ? (
        <EmptyState
          title="No achievements found"
          description="Log competition wins or certificates to showcase them on the institutional honor roll."
        />
      ) : (
        <div className="wiki-card overflow-x-auto">
          <div className="wiki-card-header flex items-center justify-between">
            <span>Verified Institutional Honors Roll ({filteredAchievements.length})</span>
          </div>

          <table className="wikitable">
            <thead>
              <tr>
                <th style={{ width: '30%' }}>Laurel & Competition</th>
                <th style={{ width: '25%' }}>Student Scholar</th>
                <th style={{ width: '15%' }}>Recognition Tier</th>
                <th style={{ width: '15%' }}>Date & Position</th>
                <th style={{ width: '15%' }} className="text-right">Audit Status</th>
              </tr>
            </thead>
            <tbody>
              {filteredAchievements.map((a) => (
                <tr key={a.id}>
                  <td>
                    <span className="wiki-link font-bold">{a.title}</span>
                    {a.event_name && (
                      <div className="text-[11px] text-[#54595d] dark:text-[#9ca3af] mt-0.5">
                        {a.event_name}
                      </div>
                    )}
                  </td>
                  <td>
                    <span className="font-medium text-[#202122] dark:text-[#f3f4f6]">
                      {a.student?.name || 'Student Participant'}
                    </span>
                    <div className="text-[11px] text-[#72777d]">
                      {a.student?.department || 'KEC Student'} • {a.organization?.name || 'General Charter'}
                    </div>
                  </td>
                  <td>
                    <span className="border border-[#a2a9b1] bg-[#eaecf0] dark:bg-[#1f2937] px-1.5 py-0.5 text-xs font-semibold capitalize">
                      {a.level || 'College'}
                    </span>
                  </td>
                  <td>
                    <div className="text-xs">{a.position ? `Position: ${a.position}` : formatDate(a.achievement_date)}</div>
                    <div className="text-[11px] text-[#72777d]">{formatDate(a.achievement_date)}</div>
                  </td>
                  <td className="text-right whitespace-nowrap">
                    {a.verified ? (
                      <span className="inline-flex items-center gap-1 text-xs font-bold text-[#10b981]">
                        <Check className="h-3.5 w-3.5" /> Verified
                      </span>
                    ) : (isAdmin || isCoordinator) ? (
                      <button
                        onClick={() => verifyAchievement(a.id)}
                        className="wiki-link text-xs cursor-pointer"
                      >
                        [ Verify Honor ]
                      </button>
                    ) : (
                      <span className="text-xs text-[#54595d] italic">Pending</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Modal */}
      <Modal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        title="Record New Extracurricular Achievement"
        description="Submit verified tournament results, competitive hackathon medals, or paper presentations."
      >
        <div className="space-y-3 pt-1 text-xs">
          <Input
            label="Achievement Title"
            value={newAchievement.title}
            onChange={(e) => setNewAchievement({ ...newAchievement, title: e.target.value })}
            placeholder="e.g. 1st Place - Smart India Hackathon 2026"
            required
          />
          <div className="grid grid-cols-2 gap-3">
            <Select
              label="Achievement Type"
              value={newAchievement.type}
              onChange={(e) => setNewAchievement({ ...newAchievement, type: e.target.value })}
              options={ACHIEVEMENT_TYPES.map((t) => ({ value: t, label: t.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase()) }))}
            />
            <Select
              label="Competition Level"
              value={newAchievement.level}
              onChange={(e) => setNewAchievement({ ...newAchievement, level: e.target.value })}
              options={ACHIEVEMENT_LEVELS.map((l) => ({ value: l, label: l.charAt(0).toUpperCase() + l.slice(1) }))}
            />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <Input
              label="Position / Rank"
              value={newAchievement.position}
              onChange={(e) => setNewAchievement({ ...newAchievement, position: e.target.value })}
              placeholder="e.g. Winner / 1st Runner Up"
            />
            <Input
              label="Date of Event"
              type="date"
              value={newAchievement.achievement_date}
              onChange={(e) => setNewAchievement({ ...newAchievement, achievement_date: e.target.value })}
              required
            />
          </div>
          <Select
            label="Associated Organization"
            value={newAchievement.organization_id}
            onChange={(e) => setNewAchievement({ ...newAchievement, organization_id: e.target.value })}
            options={myOrgs.map((o) => ({ value: o.id, label: o.name }))}
            placeholder="Select Organization"
          />
          <Textarea
            label="Description & Highlights"
            value={newAchievement.description}
            onChange={(e) => setNewAchievement({ ...newAchievement, description: e.target.value })}
            placeholder="Describe the project, judges, and prize credentials..."
          />
          <div className="flex justify-end gap-2 pt-3 border-t border-[#a2a9b1] dark:border-[#374151]">
            <Button variant="outline" size="sm" onClick={() => setModalOpen(false)}>
              Cancel
            </Button>
            <Button variant="primary" size="sm" onClick={handleCreate} loading={creating}>
              Submit Achievement
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
}
