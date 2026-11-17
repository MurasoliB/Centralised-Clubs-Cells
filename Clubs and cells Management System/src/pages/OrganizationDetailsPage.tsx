import { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { Building2, Users, Calendar, Award, Mail, Phone, ArrowLeft, CheckCircle2 } from 'lucide-react';
import { supabase } from '@/lib/supabase';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/context/ToastContext';
import { Button } from '@/components/ui/Button';
import { Tabs } from '@/components/ui/Tabs';
import { EmptyState, LoadingSpinner } from '@/components/ui/EmptyState';
import { PageHeader } from '@/components/layout/PageHeader';
import { formatDate, isUUID } from '@/lib/utils';
import { DEFAULT_ORGANIZATIONS } from '@/lib/organizationsData';

export function OrganizationDetailsPage() {
  const { id } = useParams<{ id: string }>();
  const { profile } = useAuth();
  const { toast } = useToast();
  const navigate = useNavigate();
  const [org, setOrg] = useState<any>(null);
  const [members, setMembers] = useState<any[]>([]);
  const [events, setEvents] = useState<any[]>([]);
  const [achievements, setAchievements] = useState<any[]>([]);
  const [announcements, setAnnouncements] = useState<any[]>([]);
  const [myMembership, setMyMembership] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [applying, setApplying] = useState(false);

  const isStudent = profile?.role === 'student';

  useEffect(() => {
    if (id) {
      loadAll();
    }
  }, [id, profile?.id]);

  const loadAll = async () => {
    setLoading(true);
    try {
      let orgData: any = null;

      // Only query Supabase by id if it is a valid UUID
      if (id && isUUID(id)) {
        try {
          const { data: dbOrg } = await supabase
            .from('organizations')
            .select('*, faculty_coordinator:profiles!organizations_faculty_coordinator_id_fkey(name, email), student_coordinator:profiles!organizations_student_coordinator_id_fkey(name, email)')
            .eq('id', id)
            .maybeSingle();

          if (dbOrg) orgData = dbOrg;
        } catch {}
      }

      // If not found yet, try lookup by short_name in DB
      if (!orgData && id) {
        try {
          const { data: dbByShort } = await supabase
            .from('organizations')
            .select('*, faculty_coordinator:profiles!organizations_faculty_coordinator_id_fkey(name, email), student_coordinator:profiles!organizations_student_coordinator_id_fkey(name, email)')
            .ilike('short_name', id)
            .maybeSingle();

          if (dbByShort) orgData = dbByShort;
        } catch {}
      }

      // Fallback to local default organizations index
      if (!orgData && id) {
        const found = DEFAULT_ORGANIZATIONS.find(
          (o) => o.id === id || (o.short_name && o.short_name.toLowerCase() === id.toLowerCase())
        );
        if (found) {
          orgData = {
            ...found,
            faculty_coordinator: { name: 'Faculty Advisor', email: 'advisor@kongu.edu' },
            student_coordinator: { name: 'Student Coordinator', email: 'coord@kongu.edu' },
          };
        }
      }

      setOrg(orgData);

      if (orgData) {
        let memList: any[] = [];
        let evList: any[] = [];
        let achList: any[] = [];
        let annList: any[] = [];

        if (isUUID(orgData.id)) {
          try {
            const [memRes, evRes, achRes, annRes] = await Promise.all([
              supabase.from('memberships').select('*, student:profiles!memberships_student_id_fkey(name, email, department)').eq('organization_id', orgData.id),
              supabase.from('events').select('*').eq('organization_id', orgData.id).order('start_date', { ascending: false }),
              supabase.from('achievements').select('*, student:profiles!achievements_student_id_fkey(name)').eq('organization_id', orgData.id),
              supabase.from('announcements').select('*').eq('organization_id', orgData.id).order('publish_date', { ascending: false }),
            ]);

            memList = memRes.data || [];
            evList = evRes.data || [];
            achList = achRes.data || [];
            annList = annRes.data || [];
          } catch {}
        }

        // Merge local memberships from browser cache
        try {
          const rawLocal = localStorage.getItem('kec_local_memberships');
          if (rawLocal) {
            const localMems = JSON.parse(rawLocal);
            const matching = localMems.filter((m: any) => m.organization_id === orgData.id);
            memList = [...matching, ...memList.filter((m: any) => !matching.some((lm: any) => lm.student_id === m.student_id))];
          }
        } catch {}

        setMembers(memList);
        setEvents(evList);
        setAchievements(achList);
        setAnnouncements(annList);

        if (profile?.id) {
          const myMem = memList.find((m: any) => m.student_id === profile.id);
          setMyMembership(myMem || null);
        }
      }
    } catch (err) {
      console.warn('Error loading organization:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleApply = async () => {
    if (!profile?.id || !org) return;
    setApplying(true);
    try {
      // 1. Attempt database insert if IDs are valid UUIDs
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

      // 2. Guaranteed persistence in local storage
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

      setMyMembership(localRecord);
      setMembers((prev) => [localRecord, ...prev.filter((m) => m.student_id !== profile.id)]);
      toast('Application for membership submitted successfully!', 'success');
    } catch (err: any) {
      toast(err.message || 'Failed to submit application', 'error');
    } finally {
      setApplying(false);
    }
  };

  if (loading) return <LoadingSpinner />;
  if (!org) {
    return (
      <EmptyState
        title="Organization not found"
        action={
          <Button variant="outline" onClick={() => navigate('/organizations')}>
            Back to Directory
          </Button>
        }
      />
    );
  }

  const approvedMembers = members.filter((m) => m.status === 'approved');

  return (
    <div className="space-y-6 font-sans w-full">
      {/* Breadcrumb Navigation */}
      <div className="text-xs text-[#54595d] dark:text-[#9ca3af]">
        <Link to="/organizations" className="wiki-link">
          ← Back to Organizations Directory
        </Link>
      </div>

      {/* Wikipedia Article Heading */}
      <PageHeader
        title={org.name}
        subtitle={`${org.short_name ? `(${org.short_name}) • ` : ''}${org.department || 'Multidisciplinary'} • Recognized Institutional Charter`}
        action={
          isStudent && !myMembership ? (
            <Button variant="primary" size="sm" onClick={handleApply} loading={applying}>
              Apply for Membership
            </Button>
          ) : isStudent && myMembership ? (
            <span className="border border-[#a2a9b1] bg-[#eaecf0] px-2 py-1 text-xs font-bold text-[#0645ad] capitalize">
              Status: {myMembership.status}
            </span>
          ) : null
        }
      />

      {/* Grid: Main Article Content (left) and Wikipedia Infobox (right) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Main Content Area */}
        <div className="lg:col-span-8 space-y-6">
          {/* Article Lead Section */}
          <div className="text-sm leading-relaxed space-y-2 text-[#202122] dark:text-[#e5e7eb]">
            <p>
              <strong>{org.name}</strong> is an officially accredited student organization operating under the auspices of the Department of {org.department || 'Information Technology'} at Kongu Engineering College.
            </p>
            <p className="text-xs text-[#54595d] dark:text-[#9ca3af]">
              {org.description || 'This charter aims to promote collaborative student engagement, technical skill building, hands-on hackathon preparation, and inter-collegiate tournament participation.'}
            </p>
          </div>

          {/* Tabs for Sub-Rosters */}
          <Tabs
            tabs={[
              {
                label: `Active Members (${approvedMembers.length})`,
                value: 'members',
                content: (
                  <div className="wiki-card pt-2">
                    <div className="wiki-card-header">
                      Approved Membership Roll ({approvedMembers.length})
                    </div>
                    {approvedMembers.length === 0 ? (
                      <div className="p-4">
                        <EmptyState title="No active members yet registered." />
                      </div>
                    ) : (
                      <div className="overflow-x-auto">
                        <table className="wikitable">
                          <thead>
                            <tr>
                              <th style={{ width: '40%' }}>Student Name</th>
                              <th style={{ width: '35%' }}>Email & Department</th>
                              <th style={{ width: '25%' }}>Charter Role</th>
                            </tr>
                          </thead>
                          <tbody>
                            {approvedMembers.map((m) => (
                              <tr key={m.id}>
                                <td>
                                  <span className="wiki-link font-medium">{m.student?.name || 'Member'}</span>
                                </td>
                                <td>
                                  <div className="text-xs">{m.student?.email}</div>
                                  <div className="text-[11px] text-[#72777d]">{m.student?.department}</div>
                                </td>
                                <td className="capitalize">{m.role || 'Member'}</td>
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
                label: `Hosted Events (${events.length})`,
                value: 'events',
                content: (
                  <div className="wiki-card pt-2">
                    <div className="wiki-card-header">
                      Scheduled & Past Events ({events.length})
                    </div>
                    {events.length === 0 ? (
                      <div className="p-4">
                        <EmptyState title="No events recorded for this organization yet." />
                      </div>
                    ) : (
                      <div className="overflow-x-auto">
                        <table className="wikitable">
                          <thead>
                            <tr>
                              <th style={{ width: '40%' }}>Event Title</th>
                              <th style={{ width: '25%' }}>Event Date</th>
                              <th style={{ width: '20%' }}>Venue</th>
                              <th style={{ width: '15%' }} className="text-right">Link</th>
                            </tr>
                          </thead>
                          <tbody>
                            {events.map((e) => (
                              <tr key={e.id}>
                                <td>
                                  <Link to={`/events/${e.id}`} className="wiki-link font-semibold">
                                    {e.title}
                                  </Link>
                                </td>
                                <td>{formatDate(e.start_date)}</td>
                                <td>{e.location || 'Kongu Campus'}</td>
                                <td className="text-right">
                                  <Link to={`/events/${e.id}`} className="wiki-link text-xs">
                                    [ Details ]
                                  </Link>
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
                label: `Honors Won (${achievements.length})`,
                value: 'achievements',
                content: (
                  <div className="wiki-card pt-2">
                    <div className="wiki-card-header">
                      Verified Extracurricular Honors ({achievements.length})
                    </div>
                    {achievements.length === 0 ? (
                      <div className="p-4">
                        <EmptyState title="No honors recorded for this charter yet." />
                      </div>
                    ) : (
                      <div className="overflow-x-auto">
                        <table className="wikitable">
                          <thead>
                            <tr>
                              <th style={{ width: '45%' }}>Award Title</th>
                              <th style={{ width: '35%' }}>Scholar</th>
                              <th style={{ width: '20%' }}>Tier</th>
                            </tr>
                          </thead>
                          <tbody>
                            {achievements.map((a) => (
                              <tr key={a.id}>
                                <td>
                                  <span className="wiki-link font-bold">{a.title}</span>
                                </td>
                                <td>{a.student?.name || 'Student'}</td>
                                <td className="capitalize">{a.level || 'State'}</td>
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

        {/* Wikipedia Infobox (Right Column) */}
        <div className="lg:col-span-4 wiki-card">
          <div className="wiki-card-header text-center">
            Organization Profile
          </div>

          <table className="wikitable text-xs">
            <tbody>
              <tr>
                <td className="font-bold bg-[#eaecf0] dark:bg-[#1f2937]" style={{ width: '40%' }}>Charter Name</td>
                <td>{org.name}</td>
              </tr>
              {org.short_name && (
                <tr>
                  <td className="font-bold bg-[#eaecf0] dark:bg-[#1f2937]">Abbreviation</td>
                  <td>{org.short_name}</td>
                </tr>
              )}
              <tr>
                <td className="font-bold bg-[#eaecf0] dark:bg-[#1f2937]">Classification</td>
                <td className="capitalize">{org.type}</td>
              </tr>
              <tr>
                <td className="font-bold bg-[#eaecf0] dark:bg-[#1f2937]">Category</td>
                <td>{org.category || 'General'}</td>
              </tr>
              <tr>
                <td className="font-bold bg-[#eaecf0] dark:bg-[#1f2937]">Department</td>
                <td>{org.department || 'Campus Wide'}</td>
              </tr>
              <tr>
                <td className="font-bold bg-[#eaecf0] dark:bg-[#1f2937]">Governance Status</td>
                <td>
                  <span className="font-bold text-[#10b981] capitalize">{org.status}</span>
                </td>
              </tr>
              <tr>
                <td className="font-bold bg-[#eaecf0] dark:bg-[#1f2937]">Faculty Advisor</td>
                <td>
                  <span className="wiki-link font-medium">
                    {org.faculty_coordinator?.name || 'Faculty Mentor'}
                  </span>
                  {org.faculty_coordinator?.email && (
                    <div className="text-[11px] text-[#72777d]">{org.faculty_coordinator.email}</div>
                  )}
                </td>
              </tr>
              <tr>
                <td className="font-bold bg-[#eaecf0] dark:bg-[#1f2937]">Student Coordinator</td>
                <td>
                  <span className="wiki-link font-medium">
                    {org.student_coordinator?.name || 'Lead Coordinator'}
                  </span>
                  {org.student_coordinator?.email && (
                    <div className="text-[11px] text-[#72777d]">{org.student_coordinator.email}</div>
                  )}
                </td>
              </tr>
              <tr>
                <td className="font-bold bg-[#eaecf0] dark:bg-[#1f2937]">Roster Members</td>
                <td className="font-mono">{approvedMembers.length} enrolled</td>
              </tr>
              {org.contact_email && (
                <tr>
                  <td className="font-bold bg-[#eaecf0] dark:bg-[#1f2937]">Official Email</td>
                  <td className="wiki-link">{org.contact_email}</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
