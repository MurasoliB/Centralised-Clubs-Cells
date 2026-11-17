export type UserRole = 'admin' | 'faculty_coordinator' | 'club_coordinator' | 'student';

export type OrganizationType = 'club' | 'cell';
export type OrganizationStatus = 'active' | 'inactive';

export type MembershipRole = 'member' | 'core_member' | 'secretary' | 'treasurer' | 'president' | 'vice_president';
export type MembershipStatus = 'pending' | 'approved' | 'rejected' | 'suspended' | 'left';

export type EventType = 'workshop' | 'seminar' | 'competition' | 'cultural' | 'technical' | 'social' | 'meeting' | 'other';
export type EventStatus = 'upcoming' | 'ongoing' | 'completed' | 'cancelled';

export type ParticipationStatus = 'registered' | 'attended' | 'absent' | 'cancelled';
export type AttendanceStatus = 'present' | 'absent' | 'late' | 'excused';

export type AchievementType = 'competition' | 'project' | 'certification' | 'workshop' | 'paper_presentation' | 'sports' | 'cultural' | 'other';
export type AchievementLevel = 'college' | 'state' | 'national' | 'international';

export type TargetAudience = 'all' | 'members' | 'coordinators';
export type NotificationType = 'info' | 'success' | 'warning' | 'error' | 'membership' | 'event' | 'attendance' | 'achievement' | 'announcement';

export interface Profile {
  id: string;
  name: string;
  email: string;
  role: UserRole;
  phone: string | null;
  department: string | null;
  profile_image: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Student {
  user_id: string;
  register_number: string | null;
  department: string | null;
  year: number | null;
  section: string | null;
  skills: string[];
  interests: string[];
  bio: string | null;
  created_at: string;
  updated_at: string;
}

export interface Organization {
  id: string;
  name: string;
  short_name: string | null;
  type: OrganizationType;
  description: string | null;
  category: string | null;
  logo: string | null;
  cover_image: string | null;
  department: string | null;
  faculty_coordinator_id: string | null;
  student_coordinator_id: string | null;
  contact_email: string | null;
  contact_phone: string | null;
  status: OrganizationStatus;
  created_at: string;
  updated_at: string;
}

export interface Membership {
  id: string;
  student_id: string;
  organization_id: string;
  role: MembershipRole;
  status: MembershipStatus;
  applied_at: string;
  approved_at: string | null;
  approved_by: string | null;
  created_at: string;
  updated_at: string;
}

export interface ClubEvent {
  id: string;
  organization_id: string;
  title: string;
  description: string | null;
  event_type: EventType;
  location: string | null;
  start_date: string | null;
  end_date: string | null;
  registration_deadline: string | null;
  maximum_participants: number | null;
  banner: string | null;
  status: EventStatus;
  instructions: string | null;
  created_by: string | null;
  created_at: string;
  updated_at: string;
}

export interface EventRegistration {
  id: string;
  event_id: string;
  student_id: string;
  registration_date: string;
  participation_status: ParticipationStatus;
  created_at: string;
  updated_at: string;
}

export interface Attendance {
  id: string;
  event_id: string;
  student_id: string;
  status: AttendanceStatus;
  marked_by: string | null;
  marked_at: string;
  created_at: string;
  updated_at: string;
}

export interface Achievement {
  id: string;
  student_id: string;
  organization_id: string | null;
  title: string;
  description: string | null;
  type: AchievementType;
  level: AchievementLevel | null;
  position: string | null;
  achievement_date: string | null;
  certificate: string | null;
  image: string | null;
  verified: boolean;
  verified_by: string | null;
  created_at: string;
  updated_at: string;
}

export interface Announcement {
  id: string;
  organization_id: string;
  title: string;
  content: string;
  created_by: string | null;
  target_audience: TargetAudience;
  publish_date: string;
  created_at: string;
  updated_at: string;
}

export interface Notification {
  id: string;
  user_id: string;
  title: string;
  message: string;
  type: NotificationType;
  is_read: boolean;
  related_id: string | null;
  related_type: string | null;
  created_at: string;
}

export interface AuditLog {
  id: string;
  user_id: string | null;
  action: string;
  entity_type: string | null;
  entity_id: string | null;
  details: Record<string, unknown> | null;
  created_at: string;
}

export interface Database {
  public: {
    Tables: {
      profiles: { Row: Profile; Insert: Partial<Profile>; Update: Partial<Profile> };
      students: { Row: Student; Insert: Partial<Student>; Update: Partial<Student> };
      organizations: { Row: Organization; Insert: Partial<Organization>; Update: Partial<Organization> };
      memberships: { Row: Membership; Insert: Partial<Membership>; Update: Partial<Membership> };
      events: { Row: ClubEvent; Insert: Partial<ClubEvent>; Update: Partial<ClubEvent> };
      event_registrations: { Row: EventRegistration; Insert: Partial<EventRegistration>; Update: Partial<EventRegistration> };
      attendance: { Row: Attendance; Insert: Partial<Attendance>; Update: Partial<Attendance> };
      achievements: { Row: Achievement; Insert: Partial<Achievement>; Update: Partial<Achievement> };
      announcements: { Row: Announcement; Insert: Partial<Announcement>; Update: Partial<Announcement> };
      notifications: { Row: Notification; Insert: Partial<Notification>; Update: Partial<Notification> };
      audit_logs: { Row: AuditLog; Insert: Partial<AuditLog>; Update: Partial<AuditLog> };
    };
  };
}
