import { supabase } from '@/lib/supabase';
import type { Profile } from '@/types/database';
import { isUUID } from '@/lib/utils';

export const MAX_COORDINATORS_PER_CLUB = 5;

export interface AssignedClub {
  id: string;
  name: string;
  short_name?: string | null;
  type?: 'club' | 'cell';
  faculty_coordinator_id?: string | null;
  student_coordinator_id?: string | null;
}

/**
 * Resolves the exclusive assigned club for a faculty coordinator or club coordinator.
 */
export async function getAssignedClubForUser(profile: Profile | null): Promise<AssignedClub | null> {
  if (!profile) return null;

  // Admin oversees all clubs
  if (profile.role === 'admin') {
    return null;
  }

  // 1. Check local storage cache
  const cachedOrgId = localStorage.getItem(`kec_faculty_org_${profile.id}`) 
    || localStorage.getItem(`kec_coord_org_${profile.id}`)
    || localStorage.getItem(`kec_user_org_${profile.id}`);
  const cachedOrgName = localStorage.getItem(`kec_assigned_club_${profile.id}`);

  // 2. Query Supabase organizations table
  try {
    if (profile.role === 'faculty_coordinator' && isUUID(profile.id)) {
      const { data } = await supabase
        .from('organizations')
        .select('*')
        .eq('faculty_coordinator_id', profile.id)
        .maybeSingle();

      if (data) {
        localStorage.setItem(`kec_faculty_org_${profile.id}`, data.id);
        localStorage.setItem(`kec_assigned_club_${profile.id}`, data.name);
        return data as AssignedClub;
      }
    } else if (profile.role === 'club_coordinator' && isUUID(profile.id)) {
      // Check direct student_coordinator_id
      const { data: orgData } = await supabase
        .from('organizations')
        .select('*')
        .eq('student_coordinator_id', profile.id)
        .maybeSingle();

      if (orgData) {
        localStorage.setItem(`kec_coord_org_${profile.id}`, orgData.id);
        localStorage.setItem(`kec_assigned_club_${profile.id}`, orgData.name);
        return orgData as AssignedClub;
      }

      // Check memberships table
      const { data: memData } = await supabase
        .from('memberships')
        .select('organization_id, organization:organizations(*)')
        .eq('student_id', profile.id)
        .eq('status', 'approved')
        .maybeSingle();

      if (memData?.organization) {
        const org = memData.organization as any;
        localStorage.setItem(`kec_coord_org_${profile.id}`, org.id);
        localStorage.setItem(`kec_assigned_club_${profile.id}`, org.name);
        return org as AssignedClub;
      }
    }
  } catch (err) {
    console.warn('Error fetching assigned club:', err);
  }

  // Fallback to local storage
  if (cachedOrgId && cachedOrgName) {
    return { id: cachedOrgId, name: cachedOrgName };
  }

  // Demo fallback for default user accounts
  if (profile.role === 'faculty_coordinator' || profile.role === 'club_coordinator') {
    return { id: 'default-coding-club', name: 'Coding Club' };
  }

  return null;
}

/**
 * Checks whether a user has permission to manage a given club/cell.
 * - Admin: Access to all.
 * - Faculty Coordinator: ONLY their own assigned club.
 * - Club Coordinator: ONLY their own assigned club.
 * - Others: Denied.
 */
export function canManageClub(profile: Profile | null, targetOrgId?: string, targetOrgName?: string, userClub?: AssignedClub | null): boolean {
  if (!profile) return false;
  if (profile.role === 'admin') return true;

  if (profile.role !== 'faculty_coordinator' && profile.role !== 'club_coordinator') {
    return false;
  }

  if (!userClub) return false;

  if (targetOrgId && userClub.id && targetOrgId === userClub.id) return true;
  if (targetOrgName && userClub.name && targetOrgName.toLowerCase() === userClub.name.toLowerCase()) return true;

  return false;
}

export interface UserWorkPortfolio {
  scopeTitle: string; // e.g. "All Campus Clubs & Cells" or "Coding Club"
  workDesignation: string; // e.g. "Faculty Coordinator for Coding Club", "Institutional Administrator for Clubs & Cells"
  roleCategory: string; // e.g. "Institutional Leadership", "Faculty Advisor", "Student Coordinator", "Club Member"
  clubId?: string | null;
  isSynced: boolean;
  memberClubs?: string[];
}

/**
 * Automatically syncs and derives the user's official work portfolio and designated club
 * directly from Supabase database tables (organizations & memberships) without requiring manual dropdown selection.
 */
export async function getUserWorkPortfolio(profile: Profile | null): Promise<UserWorkPortfolio> {
  if (!profile) {
    return {
      scopeTitle: 'Campus Member',
      workDesignation: 'General Campus User',
      roleCategory: 'Guest',
      isSynced: false,
    };
  }

  // 1. Admin: Institutional Oversight across all clubs
  if (profile.role === 'admin') {
    return {
      scopeTitle: 'All Campus Clubs & Cells (Institutional Scope)',
      workDesignation: 'Institutional Administrator for Clubs & Cells',
      roleCategory: 'Institutional Leadership',
      isSynced: true,
    };
  }

  // 2. Faculty Coordinator: Strictly assigned club from database organizations table
  if (profile.role === 'faculty_coordinator') {
    const club = await getAssignedClubForUser(profile);
    const clubName = club?.name || 'Coding Club';
    return {
      scopeTitle: clubName,
      workDesignation: `Faculty Coordinator for ${clubName}`,
      roleCategory: 'Faculty Leadership',
      clubId: club?.id,
      isSynced: true,
    };
  }

  // 3. Club Coordinator: Assigned club from organizations table / approved coordinator membership
  if (profile.role === 'club_coordinator') {
    const club = await getAssignedClubForUser(profile);
    const clubName = club?.name || 'Coding Club';
    return {
      scopeTitle: clubName,
      workDesignation: `Student Coordinator for ${clubName}`,
      roleCategory: 'Student Coordinator',
      clubId: club?.id,
      isSynced: true,
    };
  }

  // 4. Student: Directly synced from approved memberships table in database & local storage
  if (profile.role === 'student') {
    try {
      let approvedClubs: string[] = [];

      try {
        const rawLocal = localStorage.getItem('kec_local_memberships');
        if (rawLocal) {
          const localMems = JSON.parse(rawLocal);
          const mine = localMems.filter((m: any) => (m.student_id === profile.id || m.student?.email === profile.email) && m.status === 'approved');
          approvedClubs = mine.map((m: any) => m.organization?.name).filter(Boolean);
        }
      } catch {}

      if (isUUID(profile.id)) {
        const { data: memberships } = await supabase
          .from('memberships')
          .select('role, organization:organizations(id, name)')
          .eq('student_id', profile.id)
          .eq('status', 'approved');

        const dbClubs = (memberships || [])
          .map((m: any) => m.organization?.name)
          .filter(Boolean);
        approvedClubs = [...new Set([...approvedClubs, ...dbClubs])];
      }

      if (approvedClubs.length > 0) {
        const primaryClub = approvedClubs[0];
        const clubsStr = approvedClubs.join(', ');
        return {
          scopeTitle: clubsStr,
          workDesignation: approvedClubs.length === 1
            ? `Student Member for ${primaryClub}`
            : `Student Member for ${approvedClubs.length} Clubs (${clubsStr})`,
          roleCategory: 'Active Club Member',
          memberClubs: approvedClubs,
          isSynced: true,
        };
      }
    } catch (err) {
      console.warn('Error fetching student memberships:', err);
    }

    return {
      scopeTitle: 'General Student Body',
      workDesignation: 'Campus Student (Not Enrolled in Clubs)',
      roleCategory: 'Student Body',
      isSynced: true,
    };
  }

  return {
    scopeTitle: 'Campus Member',
    workDesignation: 'Campus Member',
    roleCategory: 'Member',
    isSynced: true,
  };
}

