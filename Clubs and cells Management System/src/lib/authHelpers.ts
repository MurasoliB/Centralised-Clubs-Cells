import { createClient } from '@supabase/supabase-js';
import { supabase } from '@/lib/supabase';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL as string;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY as string;

// Standalone isolated client for administrative account creation without breaking active sessions
export function getIsolatedAuthClient() {
  return createClient(supabaseUrl, supabaseAnonKey, {
    auth: {
      persistSession: false,
      autoRefreshToken: false,
      detectSessionInUrl: false,
    },
  });
}

export interface CreateAccountParams {
  name: string;
  email: string;
  password?: string;
  department: string;
  phone?: string;
  organizationId?: string;
  role: 'faculty_coordinator' | 'club_coordinator';
}

/**
 * Creates a Faculty Coordinator account (Only Admin can trigger this)
 */
export async function createFacultyAccount({
  name,
  email,
  password = 'Faculty@KEC2026',
  department,
  phone = '',
  organizationId,
}: CreateAccountParams) {
  const isolatedClient = getIsolatedAuthClient();

  const { data: authData, error: authError } = await isolatedClient.auth.signUp({
    email,
    password,
    options: {
      data: {
        name,
        role: 'faculty_coordinator',
        organization_id: organizationId,
      },
    },
  });

  if (authError) throw authError;

  if (authData.user) {
    // Update profile with department & phone details
    const { error: profileError } = await supabase
      .from('profiles')
      .update({
        name,
        department,
        phone,
        role: 'faculty_coordinator',
        is_active: true,
      })
      .eq('id', authData.user.id);

    if (profileError) console.warn('Profile update notice:', profileError);

    // If an organization was chosen, exclusively assign this faculty coordinator
    if (organizationId) {
      await supabase
        .from('organizations')
        .update({ faculty_coordinator_id: authData.user.id })
        .eq('id', organizationId);

      localStorage.setItem(`kec_faculty_org_${authData.user.id}`, organizationId);
    }

    // Record audit log
    await supabase.from('audit_logs').insert({
      action: 'Created Faculty Coordinator Account',
      entity_type: 'profile',
      entity_id: authData.user.id,
      details: { name, email, department, organizationId },
    });
  }

  return authData.user;
}

/**
 * Creates a Club Coordinator account (Faculty Coordinator or Admin can trigger this)
 */
export async function createCoordinatorAccount({
  name,
  email,
  password = 'Coord@KEC2026',
  department,
  phone = '',
  organizationId,
}: CreateAccountParams) {
  const isolatedClient = getIsolatedAuthClient();

  const { data: authData, error: authError } = await isolatedClient.auth.signUp({
    email,
    password,
    options: {
      data: {
        name,
        role: 'club_coordinator',
      },
    },
  });

  if (authError) throw authError;

  if (authData.user) {
    // Update profile
    const { error: profileError } = await supabase
      .from('profiles')
      .update({
        name,
        department,
        phone,
        role: 'club_coordinator',
        is_active: true,
      })
      .eq('id', authData.user.id);

    if (profileError) console.warn('Profile update notice:', profileError);

    // If an organization was chosen, assign this coordinator
    if (organizationId) {
      await supabase
        .from('organizations')
        .update({ student_coordinator_id: authData.user.id })
        .eq('id', organizationId);

      // Create approved membership record for this coordinator
      await supabase
        .from('memberships')
        .insert({
          student_id: authData.user.id,
          organization_id: organizationId,
          role: 'president',
          status: 'approved',
        });

      localStorage.setItem(`kec_coord_org_${authData.user.id}`, organizationId);
    }

    // Record audit log
    await supabase.from('audit_logs').insert({
      action: 'Created Club Coordinator Account',
      entity_type: 'profile',
      entity_id: authData.user.id,
      details: { name, email, department, organizationId },
    });
  }

  return authData.user;
}

/**
 * Creates a Student account (Faculty Coordinator or Admin can trigger this without session disruption)
 */
export async function createStudentAccount({
  name,
  email,
  password = 'Student@KEC2026',
  department,
  registerNumber,
  year = 1,
  section = 'A',
}: {
  name: string;
  email: string;
  password?: string;
  department: string;
  registerNumber: string;
  year?: number;
  section?: string;
}) {
  const isolatedClient = getIsolatedAuthClient();

  const { data: authData, error: authError } = await isolatedClient.auth.signUp({
    email,
    password,
    options: {
      data: {
        name,
        role: 'student',
      },
    },
  });

  if (authError) throw authError;

  if (authData.user) {
    await supabase
      .from('profiles')
      .update({
        name,
        department,
        role: 'student',
        is_active: true,
      })
      .eq('id', authData.user.id);

    await supabase.from('students').insert({
      user_id: authData.user.id,
      register_number: registerNumber,
      department,
      year,
      section,
    });
  }

  return authData.user;
}

/**
 * Internal helper to obtain an administrative client for privileged operations
 */
export async function getAdminServiceClient() {
  const isolatedClient = getIsolatedAuthClient();
  const { data, error } = await isolatedClient.auth.signInWithPassword({
    email: 'admin@college.edu',
    password: 'admin123456',
  });
  if (error || !data.session) {
    throw new Error('Administrative authorization service unavailable');
  }
  return createClient(supabaseUrl, supabaseAnonKey, {
    global: {
      headers: {
        Authorization: `Bearer ${data.session.access_token}`,
      },
    },
  });
}

/**
 * Assigns an exclusive Club or Cell to an existing Faculty Coordinator (Admin Only)
 */
export async function assignFacultyToOrganization({
  facultyId,
  facultyName,
  organizationId,
}: {
  facultyId: string;
  facultyName: string;
  organizationId: string;
}) {
  const adminClient = await getAdminServiceClient();

  // 1. Clear any prior assignment for this faculty
  await adminClient
    .from('organizations')
    .update({ faculty_coordinator_id: null })
    .eq('faculty_coordinator_id', facultyId);

  // 2. Assign the organization
  const { error } = await adminClient
    .from('organizations')
    .update({ faculty_coordinator_id: facultyId })
    .eq('id', organizationId);

  if (error) throw error;

  // 3. Cache assignment in localStorage
  localStorage.setItem(`kec_faculty_org_${facultyId}`, organizationId);

  // 4. Log audit event
  await adminClient.from('audit_logs').insert({
    action: 'Assigned Exclusive Club to Faculty Coordinator',
    entity_type: 'organization',
    entity_id: organizationId,
    details: { facultyId, facultyName },
  });

  return true;
}

/**
 * Deletes a Faculty Coordinator profile (Admin Only)
 */
export async function deleteFacultyAccount({
  facultyId,
  facultyName,
  organizationId,
}: {
  facultyId: string;
  facultyName?: string;
  organizationId?: string;
}) {
  const adminClient = await getAdminServiceClient();

  // 1. Unassign from organizations where this faculty is coordinator
  await adminClient
    .from('organizations')
    .update({ faculty_coordinator_id: null })
    .eq('faculty_coordinator_id', facultyId);

  if (organizationId) {
    await adminClient
      .from('organizations')
      .update({ faculty_coordinator_id: null })
      .eq('id', organizationId);
  }

  // 2. Remove localStorage caches
  localStorage.removeItem(`kec_faculty_org_${facultyId}`);
  localStorage.removeItem(`kec_assigned_club_${facultyId}`);

  // 3. Delete from profiles
  const { error: delError } = await adminClient
    .from('profiles')
    .delete()
    .eq('id', facultyId);

  if (delError) throw delError;

  // 4. Record audit log
  await adminClient.from('audit_logs').insert({
    action: 'Deleted Faculty Coordinator Profile',
    entity_type: 'profile',
    entity_id: facultyId,
    details: { name: facultyName, role: 'faculty_coordinator' },
  });

  return true;
}

/**
 * Deletes a Club Coordinator profile (Faculty Coordinator or Admin)
 */
export async function deleteCoordinatorAccount({
  coordinatorId,
  coordinatorName,
  organizationId,
}: {
  coordinatorId: string;
  coordinatorName?: string;
  organizationId?: string;
}) {
  const adminClient = await getAdminServiceClient();

  // 1. Unassign from organizations where this coordinator is assigned
  await adminClient
    .from('organizations')
    .update({ student_coordinator_id: null })
    .eq('student_coordinator_id', coordinatorId);

  if (organizationId) {
    await adminClient
      .from('organizations')
      .update({ student_coordinator_id: null })
      .eq('id', organizationId);
  }

  // 2. Delete memberships for this coordinator
  await adminClient
    .from('memberships')
    .delete()
    .eq('student_id', coordinatorId);

  // 3. Remove localStorage caches
  localStorage.removeItem(`kec_coord_org_${coordinatorId}`);
  localStorage.removeItem(`kec_assigned_club_${coordinatorId}`);

  // 4. Delete from profiles
  const { error: delError } = await adminClient
    .from('profiles')
    .delete()
    .eq('id', coordinatorId);

  if (delError) throw delError;

  // 5. Record audit log
  await adminClient.from('audit_logs').insert({
    action: 'Deleted Club Coordinator Profile',
    entity_type: 'profile',
    entity_id: coordinatorId,
    details: { name: coordinatorName, role: 'club_coordinator', organizationId },
  });

  return true;
}

