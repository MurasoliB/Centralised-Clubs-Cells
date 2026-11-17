import { useState, useEffect } from 'react';
import {
  Users, UserPlus, Building2, Shield, CheckCircle2, Mail, Phone,
  Search, Filter, Plus, KeyRound, Sparkles, AlertCircle, Lock, AlertTriangle, Trash2
} from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/context/ToastContext';
import { Button } from '@/components/ui/Button';
import { Modal } from '@/components/ui/Modal';
import { Input, Select } from '@/components/ui/Input';
import { PageHeader } from '@/components/layout/PageHeader';
import { EmptyState, LoadingSpinner } from '@/components/ui/EmptyState';
import { DEPARTMENTS, ROLE_LABELS } from '@/lib/constants';
import { supabase } from '@/lib/supabase';
import {
  createFacultyAccount,
  createCoordinatorAccount,
  deleteFacultyAccount,
  deleteCoordinatorAccount,
  assignFacultyToOrganization
} from '@/lib/authHelpers';
import { initials } from '@/lib/utils';
import { cache } from '@/lib/cache';
import { MAX_COORDINATORS_PER_CLUB, getAssignedClubForUser, type AssignedClub } from '@/lib/orgScope';

export function StaffManagementPage() {
  const { profile } = useAuth();
  const { toast } = useToast();

  const cached = cache.get<any>('staff_leadership');
  const [loading, setLoading] = useState(!cached);
  const [facultyMembers, setFacultyMembers] = useState<any[]>(cached?.faculty || []);
  const [coordinators, setCoordinators] = useState<any[]>(cached?.coordinators || []);
  const [orgs, setOrgs] = useState<any[]>(cached?.orgs || []);
  const [myClub, setMyClub] = useState<AssignedClub | null>(null);
  const [search, setSearch] = useState('');
  const [activeTab, setActiveTab] = useState<'coordinators' | 'faculty'>(
    profile?.role === 'admin' ? 'faculty' : 'coordinators'
  );

  // Modal states
  const [facultyModalOpen, setFacultyModalOpen] = useState(false);
  const [coordModalOpen, setCoordModalOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  // Deletion states
  const [deletingFaculty, setDeletingFaculty] = useState<any | null>(null);
  const [deletingCoord, setDeletingCoord] = useState<any | null>(null);
  const [deleteLoading, setDeleteLoading] = useState(false);

  // Assignment states (for unassigned faculty)
  const [assigningFaculty, setAssigningFaculty] = useState<any | null>(null);
  const [assignOrgId, setAssignOrgId] = useState('');
  const [assignLoading, setAssignLoading] = useState(false);

  // Forms
  const [facultyForm, setFacultyForm] = useState({
    name: '',
    email: '',
    department: 'Information Technology',
    phone: '',
    password: 'Faculty@KEC2026',
    organizationId: '',
  });

  const [coordForm, setCoordForm] = useState({
    name: '',
    email: '',
    organizationId: '',
    department: 'Information Technology',
    phone: '',
    password: 'Coord@KEC2026',
  });

  const isAdmin = profile?.role === 'admin';
  const isFaculty = profile?.role === 'faculty_coordinator';

  useEffect(() => {
    loadStaff();
  }, [profile?.id, profile?.role]);

  const loadStaff = async () => {
    if (!cache.has('staff_leadership')) {
      setLoading(true);
    }
    try {
      const [facRes, coordRes, orgsRes, resolvedClub] = await Promise.all([
        supabase.from('profiles').select('*').eq('role', 'faculty_coordinator').order('name'),
        supabase.from('profiles').select('*').eq('role', 'club_coordinator').order('name'),
        supabase.from('organizations').select('id, name, type, student_coordinator_id, faculty_coordinator_id').eq('status', 'active'),
        getAssignedClubForUser(profile),
      ]);

      const facList = facRes.data || [];
      const coordList = coordRes.data || [];
      const orgList = orgsRes.data || [];
      setFacultyMembers(facList);
      setCoordinators(coordList);
      setOrgs(orgList);
      setMyClub(resolvedClub);

      if (resolvedClub) {
        setCoordForm((prev) => ({ ...prev, organizationId: resolvedClub.id }));
      }

      cache.set('staff_leadership', { faculty: facList, coordinators: coordList, orgs: orgList });
    } catch {
      toast('Failed to load coordinator records', 'error');
    } finally {
      setLoading(false);
    }
  };

  const getCoordinatorOrg = (coordId: string) => {
    const directOrg = orgs.find((o) => o.student_coordinator_id === coordId);
    if (directOrg) return directOrg;

    const cachedOrgId = localStorage.getItem(`kec_coord_org_${coordId}`);
    if (cachedOrgId) {
      const matched = orgs.find((o) => o.id === cachedOrgId);
      if (matched) return matched;
    }

    const cachedOrgName = localStorage.getItem(`kec_assigned_club_${coordId}`);
    if (cachedOrgName) {
      const matched = orgs.find((o) => o.name === cachedOrgName);
      if (matched) return matched;
    }

    return null;
  };

  const getFacultyOrg = (facultyId: string) => {
    const directOrg = orgs.find((o) => o.faculty_coordinator_id === facultyId);
    if (directOrg) return directOrg;

    const cachedOrgId = localStorage.getItem(`kec_faculty_org_${facultyId}`);
    if (cachedOrgId) {
      const matched = orgs.find((o) => o.id === cachedOrgId);
      if (matched) return matched;
    }

    const cachedOrgName = localStorage.getItem(`kec_assigned_club_${facultyId}`);
    if (cachedOrgName) {
      const matched = orgs.find((o) => o.name === cachedOrgName);
      if (matched) return matched;
    }

    return null;
  };

  const myClubCoordinators = coordinators.filter((c) => {
    if (isAdmin) return true;
    if (!myClub) return false;
    const org = getCoordinatorOrg(c.id);
    return org?.id === myClub.id || org?.name === myClub.name;
  });

  const isMaxCoordinatorsReached = isFaculty && myClubCoordinators.length >= MAX_COORDINATORS_PER_CLUB;

  const handleCreateFaculty = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!isAdmin) {
      toast('Only Administrator can create Faculty Coordinator profiles', 'error');
      return;
    }

    if (!facultyForm.organizationId) {
      toast('Please select an exclusive Club or Cell to assign to this Faculty Coordinator', 'error');
      return;
    }

    const targetOrg = orgs.find((o) => o.id === facultyForm.organizationId);
    if (targetOrg?.faculty_coordinator_id) {
      const assignedFac = facultyMembers.find((f) => f.id === targetOrg.faculty_coordinator_id);
      if (assignedFac) {
        toast(
          `Conflict: ${targetOrg.name} is already assigned to ${assignedFac.name}. No two faculty can access the same club.`,
          'error'
        );
        return;
      }
    }

    setSubmitting(true);
    try {
      const newFacultyUser = await createFacultyAccount({
        name: facultyForm.name,
        email: facultyForm.email,
        department: facultyForm.department,
        phone: facultyForm.phone,
        password: facultyForm.password,
        organizationId: facultyForm.organizationId,
        role: 'faculty_coordinator',
      });

      if (newFacultyUser && targetOrg) {
        localStorage.setItem(`kec_faculty_org_${newFacultyUser.id}`, targetOrg.id);
        localStorage.setItem(`kec_assigned_club_${newFacultyUser.id}`, targetOrg.name);
      }

      toast(
        `Faculty Coordinator created exclusively for ${targetOrg?.name || 'Club'}! Login: ${facultyForm.email} / ${facultyForm.password}`,
        'success'
      );
      setFacultyModalOpen(false);
      setFacultyForm({
        name: '',
        email: '',
        department: 'Information Technology',
        phone: '',
        password: 'Faculty@KEC2026',
        organizationId: '',
      });
      loadStaff();
    } catch (err: any) {
      toast(err.message || 'Failed to create Faculty account', 'error');
    } finally {
      setSubmitting(false);
    }
  };

  const handleCreateCoordinator = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!isFaculty && !isAdmin) {
      toast('Only authorized Faculty Coordinators can create Club Coordinators', 'error');
      return;
    }

    const orgToAssign = isFaculty ? (myClub?.id || coordForm.organizationId) : coordForm.organizationId;
    if (!orgToAssign) {
      toast('No assigned club specified for this coordinator', 'error');
      return;
    }

    if (isFaculty && myClubCoordinators.length >= MAX_COORDINATORS_PER_CLUB) {
      toast(`Maximum limit of ${MAX_COORDINATORS_PER_CLUB} student coordinators already reached for your club.`, 'error');
      return;
    }

    setSubmitting(true);
    try {
      const targetOrg = orgs.find((o) => o.id === orgToAssign);
      const newCoordUser = await createCoordinatorAccount({
        name: coordForm.name,
        email: coordForm.email,
        organizationId: orgToAssign,
        department: coordForm.department,
        phone: coordForm.phone,
        password: coordForm.password,
        role: 'club_coordinator',
      });

      if (newCoordUser && targetOrg) {
        localStorage.setItem(`kec_coord_org_${newCoordUser.id}`, targetOrg.id);
        localStorage.setItem(`kec_assigned_club_${newCoordUser.id}`, targetOrg.name);
      }

      toast(
        `Student Coordinator onboarded for ${targetOrg?.name || 'your club'} (${myClubCoordinators.length + 1}/${MAX_COORDINATORS_PER_CLUB})! Login: ${coordForm.email} / ${coordForm.password}`,
        'success'
      );
      setCoordModalOpen(false);
      setCoordForm({
        name: '',
        email: '',
        organizationId: myClub?.id || '',
        department: 'Information Technology',
        phone: '',
        password: 'Coord@KEC2026',
      });
      loadStaff();
    } catch (err: any) {
      toast(err.message || 'Failed to create Coordinator account', 'error');
    } finally {
      setSubmitting(false);
    }
  };

  const handleDeleteFaculty = async () => {
    if (!isAdmin || !deletingFaculty) return;
    setDeleteLoading(true);
    try {
      const assignedOrg = getFacultyOrg(deletingFaculty.id);
      await deleteFacultyAccount({
        facultyId: deletingFaculty.id,
        facultyName: deletingFaculty.name,
        organizationId: assignedOrg?.id,
      });
      toast(`Faculty Coordinator ${deletingFaculty.name} has been permanently deleted.`, 'success');
      setDeletingFaculty(null);
      await loadStaff();
    } catch (err: any) {
      toast(err.message || 'Failed to delete faculty coordinator', 'error');
    } finally {
      setDeleteLoading(false);
    }
  };

  const handleDeleteCoordinator = async () => {
    if (!deletingCoord) return;
    if (!isFaculty && !isAdmin) {
      toast('Permission denied: Only authorized Faculty or Admin can delete coordinators', 'error');
      return;
    }
    setDeleteLoading(true);
    try {
      const assignedOrg = getCoordinatorOrg(deletingCoord.id);
      await deleteCoordinatorAccount({
        coordinatorId: deletingCoord.id,
        coordinatorName: deletingCoord.name,
        organizationId: assignedOrg?.id || myClub?.id,
      });
      toast(`Student Coordinator ${deletingCoord.name} removed from ${assignedOrg?.name || myClub?.name || 'club'}.`, 'success');
      setDeletingCoord(null);
      await loadStaff();
    } catch (err: any) {
      toast(err.message || 'Failed to delete student coordinator', 'error');
    } finally {
      setDeleteLoading(false);
    }
  };

  const handleConfirmAssignFaculty = async () => {
    if (!isAdmin || !assigningFaculty || !assignOrgId) return;
    setAssignLoading(true);
    try {
      const org = orgs.find((o) => o.id === assignOrgId);
      await assignFacultyToOrganization({
        facultyId: assigningFaculty.id,
        facultyName: assigningFaculty.name,
        organizationId: assignOrgId,
      });
      toast(`Successfully assigned ${org?.name || 'club'} to ${assigningFaculty.name}!`, 'success');
      setAssigningFaculty(null);
      setAssignOrgId('');
      await loadStaff();
    } catch (err: any) {
      toast(err.message || 'Failed to assign club to faculty', 'error');
    } finally {
      setAssignLoading(false);
    }
  };

  const visibleCoordinators = isFaculty ? myClubCoordinators : coordinators;

  const filteredCoordinators = visibleCoordinators.filter(
    (c) =>
      c.name.toLowerCase().includes(search.toLowerCase()) ||
      c.email.toLowerCase().includes(search.toLowerCase()) ||
      c.department?.toLowerCase().includes(search.toLowerCase())
  );

  const filteredFaculty = facultyMembers.filter(
    (f) =>
      f.name.toLowerCase().includes(search.toLowerCase()) ||
      f.email.toLowerCase().includes(search.toLowerCase()) ||
      f.department?.toLowerCase().includes(search.toLowerCase())
  );

  if (loading) return <LoadingSpinner />;

  return (
    <div className="space-y-6 font-sans w-full">
      <PageHeader
        title="Faculty & Coordinator Leadership Directory"
        subtitle="Exclusive Onboarding Governance: Institutional administration assigns Faculty Advisors exclusively to single charters; Faculty Advisors appoint and manage up to 5 Student Coordinators."
      />

      {/* Wikipedia Governance Notice Box */}
      <div className="border border-[#a2a9b1] dark:border-[#374151] bg-[#f8f9fa] dark:bg-[#111827] p-4 text-xs leading-relaxed rounded-[2px]">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
          <div>
            <p className="font-bold text-[#202122] dark:text-[#f3f4f6]">
              Institutional Governance Rules & Role Isolation:
            </p>
            <p className="mt-1 text-[#54595d] dark:text-[#9ca3af]">
              • <strong>Admin Privileges:</strong> Creates Faculty Coordinator profiles with exclusive assigned Club/Cell. Only Administrator can delete faculty profiles.<br />
              • <strong>Faculty Privileges:</strong> Manages coordinators for assigned club (Maximum 5 coordinators allowed). Can delete coordinator profiles.<br />
              • <strong>Isolation Enforced:</strong> Faculty members can only view their own designated club coordinators.
            </p>
          </div>
          <div className="flex items-center gap-2 flex-shrink-0">
            {isAdmin && (
              <Button
                variant="primary"
                size="sm"
                onClick={() => setFacultyModalOpen(true)}
              >
                + Create Faculty Account
              </Button>
            )}
            {isFaculty && (
              <Button
                variant="primary"
                size="sm"
                disabled={isMaxCoordinatorsReached}
                onClick={() => {
                  if (isMaxCoordinatorsReached) {
                    toast(`Maximum limit of ${MAX_COORDINATORS_PER_CLUB} coordinators already reached for your club.`, 'warning');
                    return;
                  }
                  setCoordModalOpen(true);
                }}
              >
                {isMaxCoordinatorsReached ? `Max Coordinators (5/5)` : `+ Create Coordinator`}
              </Button>
            )}
          </div>
        </div>
      </div>

      {/* Vector Navigation Tabs */}
      <div className="flex items-center border-b border-[#a2a9b1] dark:border-[#374151]">
        {isAdmin && (
          <button
            onClick={() => setActiveTab('faculty')}
            className={`wiki-tab ${activeTab === 'faculty' ? 'active' : ''}`}
          >
            <span>Faculty Coordinators ({facultyMembers.length})</span>
          </button>
        )}
        <button
          onClick={() => setActiveTab('coordinators')}
          className={`wiki-tab ${activeTab === 'coordinators' ? 'active' : ''}`}
        >
          <span>
            {isFaculty ? `My Club Coordinators (${myClub?.name || 'Assigned'})` : 'Student Coordinators'} ({visibleCoordinators.length})
          </span>
        </button>
      </div>

      {/* Filter and Count Row */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
        <div className="w-full sm:max-w-sm">
          <Input
            placeholder={isFaculty ? `Filter your ${myClub?.name || 'club'} coordinators...` : 'Filter by name, email or department...'}
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <div className="text-[#54595d] dark:text-[#9ca3af]">
          Showing {activeTab === 'coordinators' ? filteredCoordinators.length : filteredFaculty.length}{' '}
          {activeTab === 'coordinators' ? 'coordinator profiles' : 'faculty advisor profiles'}
        </div>
      </div>

      {/* Leadership Directory Tables */}
      {activeTab === 'faculty' ? (
        filteredFaculty.length === 0 ? (
          <EmptyState
            title="No Faculty Coordinators found"
            description="Use '+ Create Faculty Account' above to onboard faculty advisors with exclusive club assignments."
          />
        ) : (
          <div className="wiki-card overflow-x-auto">
            <div className="wiki-card-header">
              Faculty Advisor Leadership Roll
            </div>
            <table className="wikitable">
              <thead>
                <tr>
                  <th style={{ width: '25%' }}>Faculty Advisor</th>
                  <th style={{ width: '25%' }}>Email & Contact</th>
                  <th style={{ width: '20%' }}>Department</th>
                  <th style={{ width: '20%' }}>Exclusively Assigned Club</th>
                  <th style={{ width: '10%' }} className="text-right">Action</th>
                </tr>
              </thead>
              <tbody>
                {filteredFaculty.map((f) => {
                  const assignedOrg = getFacultyOrg(f.id);
                  return (
                    <tr key={f.id}>
                      <td>
                        <span className="font-bold text-[#202122] dark:text-[#f3f4f6]">
                          {f.name}
                        </span>
                        <div className="text-[11px] text-[#54595d] dark:text-[#9ca3af]">
                          {assignedOrg ? 'Sole Club Faculty Mentor' : 'Unassigned Charter'}
                        </div>
                      </td>
                      <td>
                        <div className="text-xs">{f.email}</div>
                        {f.phone && <div className="text-[11px] text-[#72777d]">{f.phone}</div>}
                      </td>
                      <td>{f.department || 'Information Technology'}</td>
                      <td>
                        {assignedOrg ? (
                          <span className="font-bold text-[#0645ad] dark:text-[#6b9eff]">
                            {assignedOrg.name}
                          </span>
                        ) : (
                          <span className="text-[#d33] italic">Unassigned</span>
                        )}
                      </td>
                      <td className="text-right whitespace-nowrap">
                        <div className="flex items-center justify-end gap-2">
                          {isAdmin && !assignedOrg && (
                            <button
                              onClick={() => {
                                setAssigningFaculty(f);
                                setAssignOrgId('');
                              }}
                              className="wiki-link text-xs cursor-pointer"
                            >
                              [ Assign ]
                            </button>
                          )}
                          {isAdmin && (
                            <button
                              onClick={() => setDeletingFaculty(f)}
                              className="text-[#cc0000] hover:underline text-xs cursor-pointer"
                              title="Delete Faculty Profile"
                            >
                              [ Delete ]
                            </button>
                          )}
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )
      ) : (
        filteredCoordinators.length === 0 ? (
          <EmptyState
            title={isFaculty ? `No student coordinators onboarded for ${myClub?.name || 'your club'} yet` : "No Club Coordinators found"}
            description={
              isFaculty
                ? `Click '+ Create Coordinator' above to onboard student coordinators (Up to ${MAX_COORDINATORS_PER_CLUB} allowed).`
                : "No coordinator profiles registered in the system."
            }
          />
        ) : (
          <div className="wiki-card overflow-x-auto">
            <div className="wiki-card-header">
              Student Club Coordinators Roll
            </div>
            <table className="wikitable">
              <thead>
                <tr>
                  <th style={{ width: '25%' }}>Coordinator Name</th>
                  <th style={{ width: '25%' }}>Email & Phone</th>
                  <th style={{ width: '20%' }}>Department</th>
                  <th style={{ width: '20%' }}>Assigned Club</th>
                  <th style={{ width: '10%' }} className="text-right">Action</th>
                </tr>
              </thead>
              <tbody>
                {filteredCoordinators.map((c) => {
                  const assignedOrg = getCoordinatorOrg(c.id);
                  return (
                    <tr key={c.id}>
                      <td>
                        <span className="font-bold text-[#202122] dark:text-[#f3f4f6]">
                          {c.name}
                        </span>
                        <div className="text-[11px] text-[#54595d] dark:text-[#9ca3af]">
                          Authorized Club Coordinator
                        </div>
                      </td>
                      <td>
                        <div className="text-xs">{c.email}</div>
                        {c.phone && <div className="text-[11px] text-[#72777d]">{c.phone}</div>}
                      </td>
                      <td>{c.department || 'Information Technology'}</td>
                      <td>
                        <span className="font-bold text-[#0645ad] dark:text-[#6b9eff]">
                          {assignedOrg ? assignedOrg.name : (myClub?.name || 'General Operations')}
                        </span>
                      </td>
                      <td className="text-right whitespace-nowrap">
                        {(isFaculty || isAdmin) && (
                          <button
                            onClick={() => setDeletingCoord(c)}
                            className="text-[#cc0000] hover:underline text-xs cursor-pointer"
                            title="Delete Student Coordinator"
                          >
                            [ Delete ]
                          </button>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )
      )}

      {/* CREATE FACULTY MODAL (Admin Only) */}
      <Modal
        open={facultyModalOpen}
        onClose={() => setFacultyModalOpen(false)}
        title="Create Faculty Coordinator Profile"
        description="Admin Only: Create a faculty profile with an exclusive Club or Cell assignment."
      >
        <form onSubmit={handleCreateFaculty} className="space-y-3 pt-1">
          <Input
            label="Faculty Name"
            required
            value={facultyForm.name}
            onChange={(e) => setFacultyForm({ ...facultyForm, name: e.target.value })}
            placeholder="Dr. S. Kumar Ph.D"
          />
          <Input
            label="Official College Email"
            type="email"
            required
            value={facultyForm.email}
            onChange={(e) => setFacultyForm({ ...facultyForm, email: e.target.value })}
            placeholder="kumar.faculty@kongu.edu"
          />
          <Input
            label="Initial Account Password"
            required
            value={facultyForm.password}
            onChange={(e) => setFacultyForm({ ...facultyForm, password: e.target.value })}
            placeholder="Faculty@KEC2026"
          />

          <div>
            <label className="block text-xs font-bold text-[#202122] dark:text-[#f3f4f6] mb-1">
              Exclusively Assigned Club or Cell <span className="text-[#d33]">*</span>
            </label>
            <select
              required
              value={facultyForm.organizationId}
              onChange={(e) => setFacultyForm({ ...facultyForm, organizationId: e.target.value })}
              className="w-full rounded-[2px] border border-[#a2a9b1] bg-white dark:border-[#374151] dark:bg-[#111827] py-1.5 px-2.5 text-xs text-[#202122] dark:text-[#e5e7eb] focus:border-[#0645ad] focus:outline-none"
            >
              <option value="">Select Club / Cell to Exclusively Assign</option>
              {orgs.map((o) => {
                const assignedFaculty = facultyMembers.find((f) => f.id === o.faculty_coordinator_id);
                const isAssigned = Boolean(assignedFaculty);
                return (
                  <option key={o.id} value={o.id} disabled={isAssigned}>
                    {o.name} ({o.type.toUpperCase()}) {isAssigned ? `— Already Assigned to ${assignedFaculty?.name}` : '— Available'}
                  </option>
                );
              })}
            </select>
          </div>

          <Select
            label="Department"
            value={facultyForm.department}
            onChange={(e) => setFacultyForm({ ...facultyForm, department: e.target.value })}
            options={DEPARTMENTS.map((d) => ({ value: d, label: d }))}
          />
          <Input
            label="Contact Phone"
            value={facultyForm.phone}
            onChange={(e) => setFacultyForm({ ...facultyForm, phone: e.target.value })}
            placeholder="+91 98427 12345"
          />

          <div className="flex justify-end gap-2 pt-3 border-t border-[#a2a9b1] dark:border-[#374151]">
            <Button variant="outline" size="sm" type="button" onClick={() => setFacultyModalOpen(false)}>
              Cancel
            </Button>
            <Button variant="primary" size="sm" type="submit" loading={submitting}>
              Create Faculty Profile
            </Button>
          </div>
        </form>
      </Modal>

      {/* CREATE COORDINATOR MODAL */}
      <Modal
        open={coordModalOpen}
        onClose={() => setCoordModalOpen(false)}
        title="Create Student Coordinator Profile"
        description={
          isFaculty
            ? `Onboard a student coordinator for ${myClub?.name || 'your club'}. (Limit: ${myClubCoordinators.length} of ${MAX_COORDINATORS_PER_CLUB} coordinators used).`
            : "Onboard student or staff coordinators."
        }
      >
        <form onSubmit={handleCreateCoordinator} className="space-y-3 pt-1">
          <Input
            label="Student Coordinator Name"
            required
            value={coordForm.name}
            onChange={(e) => setCoordForm({ ...coordForm, name: e.target.value })}
            placeholder="e.g. Anandha Kumar"
          />
          <Input
            label="Student Coordinator Email"
            type="email"
            required
            value={coordForm.email}
            onChange={(e) => setCoordForm({ ...coordForm, email: e.target.value })}
            placeholder="coord.hackers@college.edu"
          />
          <Input
            label="Initial Account Password"
            required
            value={coordForm.password}
            onChange={(e) => setCoordForm({ ...coordForm, password: e.target.value })}
            placeholder="Coord@KEC2026"
          />
          <Select
            label="Department"
            value={coordForm.department}
            onChange={(e) => setCoordForm({ ...coordForm, department: e.target.value })}
            options={DEPARTMENTS.map((d) => ({ value: d, label: d }))}
          />
          <Input
            label="Contact Phone"
            value={coordForm.phone}
            onChange={(e) => setCoordForm({ ...coordForm, phone: e.target.value })}
            placeholder="+91 98427 12345"
          />

          <div className="flex justify-end gap-2 pt-3 border-t border-[#a2a9b1] dark:border-[#374151]">
            <Button variant="outline" size="sm" type="button" onClick={() => setCoordModalOpen(false)}>
              Cancel
            </Button>
            <Button variant="primary" size="sm" type="submit" loading={submitting}>
              Create Coordinator Profile
            </Button>
          </div>
        </form>
      </Modal>

      {/* DELETE FACULTY MODAL */}
      <Modal
        open={Boolean(deletingFaculty)}
        onClose={() => !deleteLoading && setDeletingFaculty(null)}
        title="Confirm Faculty Profile Deletion"
        description="Permanently remove this faculty coordinator profile and unassign their club."
      >
        {deletingFaculty && (
          <div className="space-y-3 pt-1 text-xs">
            <p className="text-[#202122] dark:text-[#f3f4f6]">
              Are you sure you want to delete <strong>{deletingFaculty.name}</strong> ({deletingFaculty.email})?
              Their assigned club charter ({getFacultyOrg(deletingFaculty.id)?.name || 'General Operations'}) will become vacant.
            </p>
            <div className="flex justify-end gap-2 pt-3 border-t border-[#a2a9b1] dark:border-[#374151]">
              <Button variant="outline" size="sm" disabled={deleteLoading} onClick={() => setDeletingFaculty(null)}>
                Cancel
              </Button>
              <Button variant="danger" size="sm" loading={deleteLoading} onClick={handleDeleteFaculty}>
                Confirm Delete Faculty
              </Button>
            </div>
          </div>
        )}
      </Modal>

      {/* DELETE COORDINATOR MODAL */}
      <Modal
        open={Boolean(deletingCoord)}
        onClose={() => !deleteLoading && setDeletingCoord(null)}
        title="Confirm Coordinator Profile Deletion"
        description="Remove this student coordinator from your club leadership."
      >
        {deletingCoord && (
          <div className="space-y-3 pt-1 text-xs">
            <p className="text-[#202122] dark:text-[#f3f4f6]">
              Are you sure you want to remove coordinator <strong>{deletingCoord.name}</strong> ({deletingCoord.email})?
              This will free up an appointed coordinator slot for {getCoordinatorOrg(deletingCoord.id)?.name || myClub?.name || 'your club'}.
            </p>
            <div className="flex justify-end gap-2 pt-3 border-t border-[#a2a9b1] dark:border-[#374151]">
              <Button variant="outline" size="sm" disabled={deleteLoading} onClick={() => setDeletingCoord(null)}>
                Cancel
              </Button>
              <Button variant="danger" size="sm" loading={deleteLoading} onClick={handleDeleteCoordinator}>
                Confirm Delete Coordinator
              </Button>
            </div>
          </div>
        )}
      </Modal>

      {/* ASSIGN EXCLUSIVE CLUB MODAL */}
      <Modal
        open={Boolean(assigningFaculty)}
        onClose={() => !assignLoading && setAssigningFaculty(null)}
        title={`Assign Exclusive Club to ${assigningFaculty?.name}`}
        description="Select an available club or cell to assign to this faculty coordinator."
      >
        {assigningFaculty && (
          <div className="space-y-3 pt-1 text-xs">
            <div>
              <label className="block text-xs font-bold text-[#202122] dark:text-[#f3f4f6] mb-1">
                Select Available Club / Cell to Exclusively Assign
              </label>
              <select
                value={assignOrgId}
                onChange={(e) => setAssignOrgId(e.target.value)}
                className="w-full rounded-[2px] border border-[#a2a9b1] bg-white dark:border-[#374151] dark:bg-[#111827] py-1.5 px-2.5 text-xs text-[#202122] dark:text-[#e5e7eb] focus:border-[#0645ad] focus:outline-none"
              >
                <option value="">Select Club / Cell to Exclusively Assign</option>
                {orgs.map((o) => {
                  const assignedFaculty = facultyMembers.find((f) => f.id === o.faculty_coordinator_id);
                  const isAssigned = Boolean(assignedFaculty);
                  return (
                    <option key={o.id} value={o.id} disabled={isAssigned}>
                      {o.name} ({o.type.toUpperCase()}) {isAssigned ? `— Already Assigned to ${assignedFaculty?.name}` : '— Available'}
                    </option>
                  );
                })}
              </select>
            </div>

            <div className="flex justify-end gap-2 pt-3 border-t border-[#a2a9b1] dark:border-[#374151]">
              <Button variant="outline" size="sm" disabled={assignLoading} onClick={() => setAssigningFaculty(null)}>
                Cancel
              </Button>
              <Button
                variant="primary"
                size="sm"
                disabled={!assignOrgId}
                loading={assignLoading}
                onClick={handleConfirmAssignFaculty}
              >
                Confirm Assignment
              </Button>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
}
