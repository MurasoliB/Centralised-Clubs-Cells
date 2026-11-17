import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Check, X, Users, ArrowRight, ShieldCheck, Search, Building2 } from 'lucide-react';
import { supabase } from '@/lib/supabase';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/context/ToastContext';
import { Button } from '@/components/ui/Button';
import { Tabs } from '@/components/ui/Tabs';
import { Input } from '@/components/ui/Input';
import { EmptyState, LoadingSpinner } from '@/components/ui/EmptyState';
import { PageHeader } from '@/components/layout/PageHeader';
import { StatCard } from '@/components/ui/StatCard';
import { formatDate, isUUID } from '@/lib/utils';
import { cache } from '@/lib/cache';
import { getAssignedClubForUser, type AssignedClub } from '@/lib/orgScope';

export function MembershipsPage() {
  const { profile } = useAuth();
  const { toast } = useToast();
  const cacheKey = `memberships_${profile?.id || 'guest'}`;
  const cached = cache.get<any>(cacheKey);
  const [myMemberships, setMyMemberships] = useState<any[]>(cached?.my || []);
  const [pendingRequests, setPendingRequests] = useState<any[]>(cached?.pending || []);
  const [allMemberships, setAllMemberships] = useState<any[]>(cached?.all || []);
  const [myClub, setMyClub] = useState<AssignedClub | null>(null);
  const [loading, setLoading] = useState(!cached);
  const [actionLoading, setActionLoading] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');

  const isAdmin = profile?.role === 'admin';
  const isStudent = profile?.role === 'student';
  const isCoordinator = profile?.role === 'faculty_coordinator' || profile?.role === 'club_coordinator';

  useEffect(() => {
    loadMemberships();
  }, [profile?.id, profile?.role]);

  const loadMemberships = async () => {
    if (!cache.has(cacheKey)) {
      setLoading(true);
    }
    try {
      let myData: any[] = [];
      let pendingData: any[] = [];
      let allData: any[] = [];

      if (isStudent && profile) {
        if (isUUID(profile.id)) {
          try {
            const { data } = await supabase
              .from('memberships')
              .select('*, organization:organizations(*)')
              .eq('student_id', profile.id)
              .order('created_at', { ascending: false });
            myData = data || [];
          } catch {}
        }

        // Merge local student applications
        try {
          const rawLocal = localStorage.getItem('kec_local_memberships');
          if (rawLocal) {
            const localMems = JSON.parse(rawLocal);
            const mine = localMems.filter((m: any) => m.student_id === profile.id || m.student?.email === profile.email);
            myData = [...mine, ...myData.filter((m: any) => !mine.some((lm: any) => lm.organization_id === m.organization_id))];
          }
        } catch {}

        setMyMemberships(myData);
      } else if (isCoordinator) {
        const club = await getAssignedClubForUser(profile);
        setMyClub(club);

        let scoped: any[] = [];
        try {
          let query = supabase
            .from('memberships')
            .select('*, student:profiles!memberships_student_id_fkey(name, email, department), organization:organizations(id, name, type)')
            .order('created_at', { ascending: false });

          if (club?.id && isUUID(club.id)) {
            query = query.eq('organization_id', club.id);
          }

          const { data: rawData } = await query;
          scoped = rawData || [];
        } catch {}

        // Merge local applications for coordinator
        try {
          const rawLocal = localStorage.getItem('kec_local_memberships');
          if (rawLocal) {
            const localMems = JSON.parse(rawLocal);
            scoped = [...localMems, ...scoped];
          }
        } catch {}

        if (club?.name) {
          scoped = scoped.filter((m) => {
            if (club.id && m.organization_id === club.id) return true;
            if (m.organization?.name && m.organization.name.toLowerCase() === club.name.toLowerCase()) return true;
            return false;
          });
        }

        allData = scoped;
        pendingData = scoped.filter((m) => m.status === 'pending');
        setAllMemberships(allData);
        setPendingRequests(pendingData);
      } else if (isAdmin) {
        let dbList: any[] = [];
        try {
          const { data } = await supabase
            .from('memberships')
            .select('*, student:profiles!memberships_student_id_fkey(name, email, department), organization:organizations(id, name, type)')
            .order('created_at', { ascending: false });
          dbList = data || [];
        } catch {}

        // Merge local applications for admin review
        try {
          const rawLocal = localStorage.getItem('kec_local_memberships');
          if (rawLocal) {
            const localMems = JSON.parse(rawLocal);
            dbList = [...localMems, ...dbList];
          }
        } catch {}

        allData = dbList;
        pendingData = allData.filter((m) => m.status === 'pending');
        setAllMemberships(allData);
        setPendingRequests(pendingData);
      }

      cache.set(cacheKey, { my: myData, pending: pendingData, all: allData });
    } catch {
      console.warn('Failed to load memberships data');
    } finally {
      setLoading(false);
    }
  };

  const handleAction = async (membershipId: string, status: 'approved' | 'rejected') => {
    setActionLoading(membershipId);
    try {
      if (isUUID(membershipId)) {
        try {
          await supabase
            .from('memberships')
            .update({ status })
            .eq('id', membershipId);
        } catch {}
      }

      // Update in local cache as well
      try {
        const rawLocal = localStorage.getItem('kec_local_memberships');
        if (rawLocal) {
          const list = JSON.parse(rawLocal);
          const idx = list.findIndex((m: any) => m.id === membershipId);
          if (idx >= 0) {
            list[idx].status = status;
            localStorage.setItem('kec_local_memberships', JSON.stringify(list));
          }
        }
      } catch {}

      toast(`Membership request ${status === 'approved' ? 'approved' : 'rejected'}`, 'success');
      loadMemberships();
    } catch {
      toast('Failed to update membership status', 'error');
    } finally {
      setActionLoading(null);
    }
  };

  const filteredPending = pendingRequests.filter((m) => {
    if (!searchQuery.trim()) return true;
    const q = searchQuery.toLowerCase();
    return (
      m.student?.name?.toLowerCase().includes(q) ||
      m.student?.email?.toLowerCase().includes(q) ||
      m.organization?.name?.toLowerCase().includes(q)
    );
  });

  const filteredApproved = allMemberships.filter((m) => {
    if (m.status !== 'approved') return false;
    if (!searchQuery.trim()) return true;
    const q = searchQuery.toLowerCase();
    return (
      m.student?.name?.toLowerCase().includes(q) ||
      m.student?.email?.toLowerCase().includes(q) ||
      m.organization?.name?.toLowerCase().includes(q)
    );
  });

  if (loading) return <LoadingSpinner />;

  if (isStudent) {
    return (
      <div className="space-y-6 font-sans w-full">
        <PageHeader
          title="My Extracurricular Memberships"
          subtitle="Official institutional records of student charters, approved memberships, and active participation credentials"
        />

        <div className="wiki-card">
          <div className="wiki-card-header flex items-center justify-between">
            <span>Enrolled Charters ({myMemberships.length})</span>
            <Link to="/organizations" className="wiki-link text-xs font-normal">
              Browse More Organizations →
            </Link>
          </div>

          {myMemberships.length === 0 ? (
            <div className="p-6">
              <EmptyState
                title="You have not joined any campus organizations yet"
                description="Explore active clubs and technical research cells to submit your membership applications."
                action={
                  <Link to="/organizations">
                    <Button variant="primary" size="sm">Browse Campus Clubs</Button>
                  </Link>
                }
              />
            </div>
          ) : (
            <div className="p-0 overflow-x-auto">
              <table className="wikitable">
                <thead>
                  <tr>
                    <th style={{ width: '40%' }}>Organization Name</th>
                    <th style={{ width: '20%' }}>Classification</th>
                    <th style={{ width: '20%' }}>Date Joined</th>
                    <th style={{ width: '20%' }} className="text-right">Membership Status</th>
                  </tr>
                </thead>
                <tbody>
                  {myMemberships.map((m) => (
                    <tr key={m.id}>
                      <td>
                        <Link to={`/organizations/${m.organization?.id}`} className="wiki-link font-bold">
                          {m.organization?.name}
                        </Link>
                        <div className="text-[11px] text-[#54595d] dark:text-[#9ca3af] mt-0.5">
                          {m.organization?.department || 'College Wide'}
                        </div>
                      </td>
                      <td className="capitalize">{m.organization?.type}</td>
                      <td>{formatDate(m.created_at)}</td>
                      <td className="text-right">
                        <span
                          className={`inline-block border px-1.5 py-0.2 text-[11px] font-medium capitalize ${
                            m.status === 'approved'
                              ? 'border-[#a2a9b1] bg-[#eaf3ff] text-[#0645ad]'
                              : m.status === 'pending'
                              ? 'border-[#a2a9b1] bg-[#f8f9fa] text-[#54595d]'
                              : 'border-[#a2a9b1] bg-[#fee] text-[#d33]'
                          }`}
                        >
                          {m.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6 font-sans w-full">
      <PageHeader
        title={isCoordinator && myClub ? `${myClub.name} • Applications & Member Roll` : "Organization Memberships & Applications Portal"}
        subtitle="Review, authenticate, and maintain membership rosters in accordance with institutional guidelines"
      />

      {/* Scoped Notice */}
      {isCoordinator && myClub && (
        <div className="border border-[#a2a9b1] dark:border-[#374151] bg-[#f8f9fa] dark:bg-[#111827] p-3 text-xs flex items-center justify-between rounded-[2px]">
          <div>
            <span className="font-bold text-[#202122] dark:text-[#f3f4f6]">Exclusive Governance: </span>
            <span className="text-[#54595d] dark:text-[#9ca3af]">
              You have authentication authority for <strong>{myClub.name}</strong> applications.
            </span>
          </div>
          <span className="border border-[#a2a9b1] bg-white dark:bg-[#1f2937] px-2 py-0.5 font-bold text-xs text-[#0645ad] dark:text-[#6b9eff]">
            {myClub.name}
          </span>
        </div>
      )}

      {/* Wikipedia Infobox Key Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <StatCard label="Pending Applications" value={pendingRequests.length} description="Awaiting authentication" icon={Users} />
        <StatCard label="Active Roster Members" value={allMemberships.filter((m) => m.status === 'approved').length} description="Verified charter members" icon={ShieldCheck} />
        <StatCard label="Total Submissions" value={allMemberships.length} description="All-time membership logs" icon={Building2} />
      </div>

      {/* Search Bar */}
      <div className="p-3 border border-[#a2a9b1] dark:border-[#374151] bg-[#f8f9fa] dark:bg-[#111827] flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 text-xs rounded-[2px]">
        <div className="flex-1 max-w-sm">
          <Input
            placeholder="Search applicants by name, email or charter..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
        <div className="text-[#54595d] dark:text-[#9ca3af]">
          {searchQuery ? `${filteredPending.length} pending / ${filteredApproved.length} approved matching` : `${pendingRequests.length} pending approval`}
        </div>
      </div>

      <Tabs
        tabs={[
          {
            label: `Pending Applications (${pendingRequests.length})`,
            value: 'pending',
            content: (
              <div className="wiki-card pt-2">
                <div className="wiki-card-header">
                  Pending Membership Applications ({filteredPending.length})
                </div>
                {filteredPending.length === 0 ? (
                  <div className="p-6">
                    <EmptyState
                      title="No pending applications awaiting review"
                      description="New student requests will appear here when submitted."
                    />
                  </div>
                ) : (
                  <div className="p-0 overflow-x-auto">
                    <table className="wikitable">
                      <thead>
                        <tr>
                          <th style={{ width: '35%' }}>Applicant Scholar</th>
                          <th style={{ width: '25%' }}>Charter Body</th>
                          <th style={{ width: '20%' }}>Date Submitted</th>
                          <th style={{ width: '20%' }} className="text-right">Actions</th>
                        </tr>
                      </thead>
                      <tbody>
                        {filteredPending.map((m) => (
                          <tr key={m.id}>
                            <td>
                              <span className="wiki-link font-bold">{m.student?.name}</span>
                              <div className="text-[11px] text-[#72777d]">{m.student?.email} • {m.student?.department}</div>
                            </td>
                            <td>{m.organization?.name}</td>
                            <td>{formatDate(m.created_at)}</td>
                            <td className="text-right whitespace-nowrap">
                              <div className="flex items-center justify-end gap-2 text-xs">
                                <button
                                  onClick={() => handleAction(m.id, 'approved')}
                                  disabled={actionLoading === m.id}
                                  className="wiki-link text-xs cursor-pointer font-bold"
                                >
                                  [ Approve ]
                                </button>
                                <button
                                  onClick={() => handleAction(m.id, 'rejected')}
                                  disabled={actionLoading === m.id}
                                  className="text-[#cc0000] hover:underline text-xs cursor-pointer"
                                >
                                  [ Reject ]
                                </button>
                              </div>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            ),
          },
          {
            label: `Approved Members (${allMemberships.filter((m) => m.status === 'approved').length})`,
            value: 'approved',
            content: (
              <div className="wiki-card pt-2">
                <div className="wiki-card-header">
                  Active Approved Members ({filteredApproved.length})
                </div>
                {filteredApproved.length === 0 ? (
                  <div className="p-6">
                    <EmptyState title="No approved members found" />
                  </div>
                ) : (
                  <div className="p-0 overflow-x-auto">
                    <table className="wikitable">
                      <thead>
                        <tr>
                          <th style={{ width: '35%' }}>Student Name</th>
                          <th style={{ width: '30%' }}>Email & Department</th>
                          <th style={{ width: '20%' }}>Charter Club</th>
                          <th style={{ width: '15%' }} className="text-center">Status</th>
                        </tr>
                      </thead>
                      <tbody>
                        {filteredApproved.map((m) => (
                          <tr key={m.id}>
                            <td>
                              <span className="wiki-link font-semibold">{m.student?.name}</span>
                            </td>
                            <td>
                              <div className="text-xs">{m.student?.email}</div>
                              <div className="text-[11px] text-[#72777d]">{m.student?.department}</div>
                            </td>
                            <td>{m.organization?.name}</td>
                            <td className="text-center">
                              <span className="border border-[#a2a9b1] bg-[#eaf3ff] text-[#0645ad] px-1.5 py-0.2 text-[11px] font-medium">
                                Active Member
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            ),
          },
        ]}
      />
    </div>
  );
}
