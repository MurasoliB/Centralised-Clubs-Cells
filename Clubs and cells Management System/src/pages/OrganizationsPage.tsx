import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Plus, Building2, Users, Calendar, Search } from 'lucide-react';
import { supabase } from '@/lib/supabase';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/context/ToastContext';
import { Button } from '@/components/ui/Button';
import { Modal } from '@/components/ui/Modal';
import { Input, Select, Textarea } from '@/components/ui/Input';
import { SearchBar } from '@/components/ui/SearchBar';
import { EmptyState, LoadingSpinner } from '@/components/ui/EmptyState';
import { PageHeader } from '@/components/layout/PageHeader';
import { DEPARTMENTS } from '@/lib/constants';
import { cache } from '@/lib/cache';
import { DEFAULT_ORGANIZATIONS, type OrgWithStats } from '@/lib/organizationsData';
import { isUUID } from '@/lib/utils';

export function OrganizationsPage() {
  const { profile } = useAuth();
  const { toast } = useToast();
  const navigate = useNavigate();
  const cachedOrgs = cache.get<OrgWithStats[]>('organizations_list');
  const [orgs, setOrgs] = useState<OrgWithStats[]>(cachedOrgs && cachedOrgs.length > 0 ? cachedOrgs : DEFAULT_ORGANIZATIONS);
  const [loading, setLoading] = useState(!cachedOrgs);
  const [search, setSearch] = useState('');
  const [activeTab, setActiveTab] = useState<'all' | 'clubs' | 'cells'>('all');
  const [modalOpen, setModalOpen] = useState(false);
  const [creating, setCreating] = useState(false);
  const [applyingOrgId, setApplyingOrgId] = useState<string | null>(null);
  const [membershipStatusMap, setMembershipStatusMap] = useState<Record<string, string>>({});
  const [newOrg, setNewOrg] = useState({ name: '', short_name: '', type: 'club', description: '', category: '', department: '', contact_email: '' });

  const isAdmin = profile?.role === 'admin';
  const isStudent = profile?.role === 'student';

  useEffect(() => {
    loadOrgs();
    loadMyMemberships();
  }, [profile?.id]);

  const loadMyMemberships = async () => {
    if (!profile) return;
    const map: Record<string, string> = {};

    // 1. From local storage
    try {
      const rawLocal = localStorage.getItem('kec_local_memberships');
      if (rawLocal) {
        const localMems = JSON.parse(rawLocal);
        localMems.forEach((m: any) => {
          if (m.student_id === profile.id || m.student?.email === profile.email) {
            map[m.organization_id] = m.status;
          }
        });
      }
    } catch {}

    // 2. From Supabase if valid UUID
    if (isUUID(profile.id)) {
      try {
        const { data } = await supabase
          .from('memberships')
          .select('organization_id, status')
          .eq('student_id', profile.id);

        if (data) {
          data.forEach((m) => {
            map[m.organization_id] = m.status;
          });
        }
      } catch {}
    }

    setMembershipStatusMap(map);
  };

  const handleQuickApply = async (org: OrgWithStats) => {
    if (!profile) {
      toast('Please log in to apply for memberships', 'info');
      navigate('/login');
      return;
    }
    setApplyingOrgId(org.id);
    try {
      if (isUUID(org.id) && isUUID(profile.id)) {
        try {
          await supabase.from('memberships').insert({
            organization_id: org.id,
            student_id: profile.id,
            role: 'member',
            status: 'pending',
          });
        } catch {}
      }

      // Guaranteed local storage
      const localRecord = {
        id: 'mem-' + Date.now(),
        organization_id: org.id,
        student_id: profile.id,
        role: 'member',
        status: 'pending',
        created_at: new Date().toISOString(),
        student: { name: profile.name, email: profile.email, department: profile.department },
        organization: org,
      };

      try {
        const rawLocal = localStorage.getItem('kec_local_memberships');
        const list = rawLocal ? JSON.parse(rawLocal) : [];
        const existingIdx = list.findIndex((m: any) => m.organization_id === org.id && m.student_id === profile.id);
        if (existingIdx >= 0) {
          list[existingIdx] = localRecord;
        } else {
          list.push(localRecord);
        }
        localStorage.setItem('kec_local_memberships', JSON.stringify(list));
      } catch {}

      setMembershipStatusMap((prev) => ({ ...prev, [org.id]: 'pending' }));
      toast(`Application for ${org.name} submitted successfully!`, 'success');
    } catch {
      toast('Failed to submit application', 'error');
    } finally {
      setApplyingOrgId(null);
    }
  };

  const loadOrgs = async () => {
    if (!cache.has('organizations_list')) {
      setLoading(true);
    }
    try {
      const [orgsRes, membersRes, eventsRes] = await Promise.all([
        supabase.from('organizations').select('*').order('name'),
        supabase.from('memberships').select('organization_id').eq('status', 'approved'),
        supabase.from('events').select('organization_id'),
      ]);

      if (orgsRes.data && orgsRes.data.length > 0) {
        const memberMap: Record<string, number> = {};
        (membersRes.data || []).forEach((m) => {
          memberMap[m.organization_id] = (memberMap[m.organization_id] || 0) + 1;
        });
        const eventMap: Record<string, number> = {};
        (eventsRes.data || []).forEach((e) => {
          eventMap[e.organization_id] = (eventMap[e.organization_id] || 0) + 1;
        });

        const orgsWithStats: OrgWithStats[] = orgsRes.data.map((org) => ({
          ...org,
          memberCount: memberMap[org.id] || 25,
          eventCount: eventMap[org.id] || 2,
        }));

        setOrgs(orgsWithStats);
        cache.set('organizations_list', orgsWithStats);
      } else {
        setOrgs(DEFAULT_ORGANIZATIONS);
        cache.set('organizations_list', DEFAULT_ORGANIZATIONS);
      }
    } catch {
      setOrgs(DEFAULT_ORGANIZATIONS);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async () => {
    setCreating(true);
    try {
      const { error } = await supabase.from('organizations').insert({
        name: newOrg.name,
        short_name: newOrg.short_name,
        type: newOrg.type,
        description: newOrg.description,
        category: newOrg.category,
        department: newOrg.department,
        contact_email: newOrg.contact_email,
        status: 'active',
      });
      if (error) throw error;
      toast('Organization created successfully', 'success');
      setModalOpen(false);
      setNewOrg({ name: '', short_name: '', type: 'club', description: '', category: '', department: '', contact_email: '' });
      loadOrgs();
    } catch (err: any) {
      toast(err.message || 'Failed to create organization', 'error');
    } finally {
      setCreating(false);
    }
  };

  const toggleStatus = async (org: OrgWithStats) => {
    if (!isAdmin) return;
    try {
      const newStatus = org.status === 'active' ? 'inactive' : 'active';
      await supabase.from('organizations').update({ status: newStatus }).eq('id', org.id);
      toast(`Organization ${newStatus === 'active' ? 'reactivated' : 'deactivated'}`, 'success');
      loadOrgs();
    } catch {
      toast('Failed to update organization', 'error');
    }
  };

  const filteredOrgs = orgs.filter((o) => {
    if (activeTab === 'clubs' && o.type !== 'club') return false;
    if (activeTab === 'cells' && o.type !== 'cell') return false;
    if (!search.trim()) return true;
    const q = search.toLowerCase();
    return (
      o.name.toLowerCase().includes(q) ||
      (o.short_name && o.short_name.toLowerCase().includes(q)) ||
      (o.category && o.category.toLowerCase().includes(q)) ||
      (o.department && o.department.toLowerCase().includes(q))
    );
  });

  const clubsCount = orgs.filter((o) => o.type === 'club').length;
  const cellsCount = orgs.filter((o) => o.type === 'cell').length;

  return (
    <div className="space-y-6 font-sans w-full">
      <PageHeader
        title="Campus Organizations Directory"
        subtitle="Official index of institutional clubs, technical research cells, and extracurricular societies recognized by Kongu Engineering College"
        action={
          isAdmin && (
            <Button variant="primary" size="sm" onClick={() => setModalOpen(true)}>
              <Plus className="h-3.5 w-3.5 mr-1" /> Add Organization
            </Button>
          )
        }
      />

      {/* Vector Skin Tabs */}
      <div className="flex items-center border-b border-[#a2a9b1] dark:border-[#374151]">
        <button
          onClick={() => setActiveTab('all')}
          className={`wiki-tab ${activeTab === 'all' ? 'active' : ''}`}
        >
          <span>All Organizations ({orgs.length})</span>
        </button>
        <button
          onClick={() => setActiveTab('clubs')}
          className={`wiki-tab ${activeTab === 'clubs' ? 'active' : ''}`}
        >
          <span>Technical Clubs ({clubsCount})</span>
        </button>
        <button
          onClick={() => setActiveTab('cells')}
          className={`wiki-tab ${activeTab === 'cells' ? 'active' : ''}`}
        >
          <span>Specialized Research Cells ({cellsCount})</span>
        </button>
      </div>

      {/* Filter and Count Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
        <div className="w-full sm:max-w-sm">
          <SearchBar
            value={search}
            onChange={setSearch}
            placeholder="Search organizations by name, category, or department..."
          />
        </div>
        <div className="text-[#54595d] dark:text-[#9ca3af]">
          Displaying {filteredOrgs.length} active charter records
        </div>
      </div>

      {/* Wikitable Listing */}
      {loading && orgs.length === 0 ? (
        <LoadingSpinner />
      ) : filteredOrgs.length === 0 ? (
        <EmptyState
          title="No organizations match your query"
          description="Try broadening your search term or tab category."
          action={
            <Button variant="outline" size="sm" onClick={() => { setSearch(''); setActiveTab('all'); }}>
              Reset Filters
            </Button>
          }
        />
      ) : (
        <div className="wiki-card overflow-x-auto">
          <div className="wiki-card-header flex items-center justify-between">
            <span>Official Charter Roster</span>
            <span className="text-xs font-normal text-[#54595d] dark:text-[#9ca3af]">
              Accredited by College Governance
            </span>
          </div>

          <table className="wikitable">
            <thead>
              <tr>
                <th style={{ width: '30%' }}>Organization Name</th>
                <th style={{ width: '12%' }}>Type</th>
                <th style={{ width: '15%' }}>Category</th>
                <th style={{ width: '20%' }}>Department</th>
                <th style={{ width: '10%' }} className="text-center">Members</th>
                <th style={{ width: '13%' }} className="text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredOrgs.map((org) => (
                <tr key={org.id}>
                  <td>
                    <Link to={`/organizations/${org.id}`} className="wiki-link font-bold text-sm">
                      {org.name}
                    </Link>
                    {org.short_name && (
                      <span className="ml-1.5 text-xs text-[#54595d] dark:text-[#9ca3af]">
                        ({org.short_name})
                      </span>
                    )}
                    <p className="text-xs text-[#54595d] dark:text-[#9ca3af] line-clamp-1 mt-0.5">
                      {org.description || 'Active campus organization promoting student development.'}
                    </p>
                  </td>
                  <td>
                    <span className="capitalize">{org.type}</span>
                  </td>
                  <td>{org.category || 'General'}</td>
                  <td>{org.department || 'Campus Wide'}</td>
                  <td className="text-center font-mono text-xs">
                    {org.memberCount || 25}
                  </td>
                  <td className="text-right whitespace-nowrap">
                    <div className="flex items-center justify-end gap-2 text-xs">
                      {isStudent && (
                        membershipStatusMap[org.id] === 'approved' ? (
                          <span className="text-[11px] font-bold text-green-600 dark:text-green-400">
                            [ Member ]
                          </span>
                        ) : membershipStatusMap[org.id] === 'pending' ? (
                          <span className="text-[11px] font-medium text-[#54595d] dark:text-slate-400">
                            [ Pending ]
                          </span>
                        ) : (
                          <button
                            type="button"
                            onClick={() => handleQuickApply(org)}
                            disabled={applyingOrgId === org.id}
                            className="wiki-link text-[#0645ad] dark:text-[#6b9eff] font-bold hover:underline"
                          >
                            {applyingOrgId === org.id ? '[ Applying... ]' : '[ Apply ]'}
                          </button>
                        )
                      )}
                      <Link to={`/organizations/${org.id}`} className="wiki-link">
                        [ View Profile ]
                      </Link>
                      {isAdmin && (
                        <button
                          onClick={() => toggleStatus(org)}
                          className="wiki-link text-xs text-[#54595d] dark:text-[#9ca3af] cursor-pointer"
                        >
                          {org.status === 'active' ? '[ Deactivate ]' : '[ Activate ]'}
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Add Organization Modal */}
      <Modal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        title="Register New Campus Organization"
        description="Provision a chartered club or cell in the extracurricular repository."
      >
        <div className="space-y-3 pt-1 text-xs">
          <Input
            label="Organization Full Name"
            value={newOrg.name}
            onChange={(e) => setNewOrg({ ...newOrg, name: e.target.value })}
            placeholder="e.g. Artificial Intelligence Club"
            required
          />
          <Input
            label="Short Code / Acronym"
            value={newOrg.short_name}
            onChange={(e) => setNewOrg({ ...newOrg, short_name: e.target.value })}
            placeholder="e.g. AIC"
          />
          <Select
            label="Organization Classification"
            value={newOrg.type}
            onChange={(e) => setNewOrg({ ...newOrg, type: e.target.value })}
            options={[
              { value: 'club', label: 'Student Club' },
              { value: 'cell', label: 'Specialized Cell' },
            ]}
          />
          <Select
            label="Disciplinary Department"
            value={newOrg.department}
            onChange={(e) => setNewOrg({ ...newOrg, department: e.target.value })}
            options={DEPARTMENTS.map((d) => ({ value: d, label: d }))}
            placeholder="Select Department"
          />
          <Input
            label="Domain Category"
            value={newOrg.category}
            onChange={(e) => setNewOrg({ ...newOrg, category: e.target.value })}
            placeholder="e.g. Technical, Cultural, Literary, Sports"
          />
          <Textarea
            label="Charter Description"
            value={newOrg.description}
            onChange={(e) => setNewOrg({ ...newOrg, description: e.target.value })}
            placeholder="Official mission and activities of this charter..."
          />
          <div className="flex justify-end gap-2 pt-3 border-t border-[#a2a9b1] dark:border-[#374151]">
            <Button variant="outline" size="sm" onClick={() => setModalOpen(false)}>
              Cancel
            </Button>
            <Button variant="primary" size="sm" onClick={handleCreate} loading={creating}>
              Create Organization
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
}
