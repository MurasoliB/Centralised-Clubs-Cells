import { useEffect, useState } from 'react';
import { Plus, Megaphone, Building2, Calendar } from 'lucide-react';
import { supabase } from '@/lib/supabase';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/context/ToastContext';
import { Button } from '@/components/ui/Button';
import { Modal } from '@/components/ui/Modal';
import { Input, Select, Textarea } from '@/components/ui/Input';
import { EmptyState, LoadingSpinner } from '@/components/ui/EmptyState';
import { PageHeader } from '@/components/layout/PageHeader';
import { formatRelativeTime, formatDate } from '@/lib/utils';
import { cache } from '@/lib/cache';

export function AnnouncementsPage() {
  const { profile } = useAuth();
  const { toast } = useToast();
  const cached = cache.get<any[]>('announcements_list');
  const [announcements, setAnnouncements] = useState<any[]>(cached || []);
  const [loading, setLoading] = useState(!cached);
  const [modalOpen, setModalOpen] = useState(false);
  const [creating, setCreating] = useState(false);
  const [myOrgs, setMyOrgs] = useState<any[]>([]);
  const [selectedOrgFilter, setSelectedOrgFilter] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [newAnn, setNewAnn] = useState({ organization_id: '', title: '', content: '', target_audience: 'all' });

  const isCoordinator = profile?.role === 'faculty_coordinator' || profile?.role === 'club_coordinator';
  const isAdmin = profile?.role === 'admin';
  const canCreate = isCoordinator || isAdmin;

  useEffect(() => {
    loadAnnouncements();
    if (canCreate) loadMyOrgs();
  }, []);

  const loadMyOrgs = async () => {
    let query = supabase.from('organizations').select('id, name').eq('status', 'active');
    if (!isAdmin && profile) {
      query = query.or(`faculty_coordinator_id.eq.${profile.id},student_coordinator_id.eq.${profile.id}`);
    }
    const { data } = await query;
    setMyOrgs(data || []);
  };

  const loadAnnouncements = async () => {
    if (!cache.has('announcements_list')) {
      setLoading(true);
    }
    try {
      const { data } = await supabase
        .from('announcements')
        .select('*, organization:organizations(name, type)')
        .order('publish_date', { ascending: false });
      const list = data || [];
      setAnnouncements(list);
      cache.set('announcements_list', list);
    } catch {
      toast('Failed to load announcements', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async () => {
    if (!newAnn.organization_id || !newAnn.title.trim() || !newAnn.content.trim()) {
      toast('Please fill in all required fields', 'error');
      return;
    }

    setCreating(true);
    try {
      const { error } = await supabase.from('announcements').insert({
        organization_id: newAnn.organization_id,
        title: newAnn.title.trim(),
        content: newAnn.content.trim(),
        created_by: profile?.id,
        target_audience: newAnn.target_audience,
        publish_date: new Date().toISOString(),
      });
      if (error) throw error;

      const { data: members } = await supabase
        .from('memberships')
        .select('student_id')
        .eq('organization_id', newAnn.organization_id)
        .eq('status', 'approved');

      if (members && members.length > 0) {
        const notifications = members.map((m) => ({
          user_id: m.student_id,
          title: `Announcement: ${newAnn.title}`,
          message: newAnn.content.slice(0, 100),
          type: 'announcement',
          related_id: newAnn.organization_id,
          related_type: 'organization',
        }));
        await supabase.from('notifications').insert(notifications);
      }

      toast('Announcement published successfully!', 'success');
      setModalOpen(false);
      setNewAnn({ organization_id: '', title: '', content: '', target_audience: 'all' });
      loadAnnouncements();
    } catch (err: any) {
      toast(err.message || 'Failed to publish announcement', 'error');
    } finally {
      setCreating(false);
    }
  };

  const filteredAnnouncements = announcements.filter((a) => {
    const matchesFilter = selectedOrgFilter === 'all' || a.organization_id === selectedOrgFilter;
    const matchesSearch =
      a.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      a.content.toLowerCase().includes(searchQuery.toLowerCase()) ||
      a.organization?.name?.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  if (loading) return <LoadingSpinner />;

  return (
    <div className="space-y-6 font-sans w-full">
      <PageHeader
        title="Institutional Operational Notices & Circulars"
        subtitle="Official updates, executive circulars, and notifications issued by clubs, cells, and college administration"
        action={
          canCreate && (
            <Button variant="primary" size="sm" onClick={() => setModalOpen(true)}>
              <Plus className="h-3.5 w-3.5 mr-1" /> Post Notice
            </Button>
          )
        }
      />

      {/* Pinned Broadcast Banner */}
      {announcements.length > 0 && (
        <div className="wiki-card">
          <div className="wiki-card-header flex items-center justify-between">
            <span>Latest Official Institutional Release</span>
            <span className="text-xs font-normal text-[#54595d] dark:text-[#9ca3af]">
              {formatRelativeTime(announcements[0]?.publish_date)}
            </span>
          </div>
          <div className="p-4 space-y-1.5">
            <h2 className="font-serif text-lg font-bold text-[#202122] dark:text-[#f3f4f6]">
              {announcements[0]?.title}
            </h2>
            <p className="text-xs text-[#0645ad] dark:text-[#6b9eff] font-medium">
              Issued by: {announcements[0]?.organization?.name || 'College Wide Governance'}
            </p>
            <p className="text-xs text-[#54595d] dark:text-[#9ca3af] leading-relaxed pt-1">
              {announcements[0]?.content}
            </p>
          </div>
        </div>
      )}

      {/* Search and Filters Bar */}
      <div className="p-3 border border-[#a2a9b1] dark:border-[#374151] bg-[#f8f9fa] dark:bg-[#111827] flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 text-xs rounded-[2px]">
        <div className="flex-1 max-w-sm">
          <Input
            placeholder="Search circulars by keyword..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
        <div className="flex items-center gap-2">
          <span>Filter by charter:</span>
          <select
            value={selectedOrgFilter}
            onChange={(e) => setSelectedOrgFilter(e.target.value)}
            className="rounded-[2px] border border-[#a2a9b1] bg-white px-2 py-1 text-xs text-[#202122] dark:border-[#374151] dark:bg-[#111827] dark:text-[#e5e7eb] focus:border-[#0645ad] focus:outline-none"
          >
            <option value="all">All Charters</option>
            {Array.from(new Set(announcements.map((a) => a.organization?.name).filter(Boolean))).map((orgName) => {
              const ann = announcements.find((a) => a.organization?.name === orgName);
              return (
                <option key={ann?.organization_id} value={ann?.organization_id}>
                  {orgName}
                </option>
              );
            })}
          </select>
        </div>
      </div>

      {/* Table of Notices */}
      {filteredAnnouncements.length === 0 ? (
        <EmptyState
          title="No notices found"
          description={searchQuery ? 'Try clearing your search query.' : 'Check back later for newly published circulars.'}
        />
      ) : (
        <div className="wiki-card overflow-x-auto">
          <div className="wiki-card-header flex items-center justify-between">
            <span>Official Circulars Registry ({filteredAnnouncements.length})</span>
          </div>

          <table className="wikitable">
            <thead>
              <tr>
                <th style={{ width: '30%' }}>Circular Subject</th>
                <th style={{ width: '20%' }}>Issuing Body</th>
                <th style={{ width: '15%' }}>Target Audience</th>
                <th style={{ width: '20%' }}>Date Published</th>
                <th style={{ width: '15%' }}>Details</th>
              </tr>
            </thead>
            <tbody>
              {filteredAnnouncements.map((a) => (
                <tr key={a.id}>
                  <td>
                    <span className="wiki-link font-bold">{a.title}</span>
                    <p className="text-xs text-[#54595d] dark:text-[#9ca3af] line-clamp-1 mt-0.5">
                      {a.content}
                    </p>
                  </td>
                  <td>{a.organization?.name || 'General College'}</td>
                  <td>
                    <span className="capitalize">{a.target_audience || 'All'}</span>
                  </td>
                  <td>{formatDate(a.publish_date)}</td>
                  <td>
                    <span className="text-xs text-[#54595d] dark:text-[#9ca3af]">
                      {formatRelativeTime(a.publish_date)}
                    </span>
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
        title="Publish Official Campus Circular"
        description="Broadcast circular to member rosters and notification dashboards."
      >
        <div className="space-y-3 pt-1 text-xs">
          <Select
            label="Issuing Organization"
            value={newAnn.organization_id}
            onChange={(e) => setNewAnn({ ...newAnn, organization_id: e.target.value })}
            options={myOrgs.map((o) => ({ value: o.id, label: o.name }))}
            placeholder="Select Organization"
            required
          />
          <Input
            label="Notice Title"
            value={newAnn.title}
            onChange={(e) => setNewAnn({ ...newAnn, title: e.target.value })}
            placeholder="e.g. Schedule for HackKEC 2026 Orientation"
            required
          />
          <Select
            label="Target Audience"
            value={newAnn.target_audience}
            onChange={(e) => setNewAnn({ ...newAnn, target_audience: e.target.value })}
            options={[
              { value: 'all', label: 'All Students & Staff' },
              { value: 'members', label: 'Club Members Only' },
              { value: 'coordinators', label: 'Leadership Coordinators' },
            ]}
          />
          <Textarea
            label="Official Message Body"
            value={newAnn.content}
            onChange={(e) => setNewAnn({ ...newAnn, content: e.target.value })}
            placeholder="Enter the complete text of the notice..."
            required
          />
          <div className="flex justify-end gap-2 pt-3 border-t border-[#a2a9b1] dark:border-[#374151]">
            <Button variant="outline" size="sm" onClick={() => setModalOpen(false)}>
              Cancel
            </Button>
            <Button variant="primary" size="sm" onClick={handleCreate} loading={creating}>
              Publish Notice
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
}
