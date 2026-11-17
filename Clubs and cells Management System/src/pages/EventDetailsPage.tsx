import { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { Calendar, MapPin, Users, Clock, ArrowLeft, CheckCircle2 } from 'lucide-react';
import { supabase } from '@/lib/supabase';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/context/ToastContext';
import { Button } from '@/components/ui/Button';
import { Tabs } from '@/components/ui/Tabs';
import { EmptyState, LoadingSpinner } from '@/components/ui/EmptyState';
import { PageHeader } from '@/components/layout/PageHeader';
import { formatDate, formatDateTime, isUUID } from '@/lib/utils';
import { REAL_CAMPUS_EVENTS } from '@/lib/eventsData';

export function EventDetailsPage() {
  const { id } = useParams<{ id: string }>();
  const { profile } = useAuth();
  const { toast } = useToast();
  const navigate = useNavigate();
  const [event, setEvent] = useState<any>(null);
  const [registrations, setRegistrations] = useState<any[]>([]);
  const [attendance, setAttendance] = useState<any[]>([]);
  const [myRegistration, setMyRegistration] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);

  const isStudent = profile?.role === 'student';
  const isAdmin = profile?.role === 'admin';
  const isCoordinator = profile?.role === 'faculty_coordinator' || profile?.role === 'club_coordinator';

  useEffect(() => {
    if (id) {
      loadEventData();
    }
  }, [id, profile?.id]);

  const loadEventData = async () => {
    setLoading(true);
    try {
      let eventData: any = null;

      // Only query Supabase by id if it is a valid UUID
      if (id && isUUID(id)) {
        try {
          const { data: dbEvent } = await supabase
            .from('events')
            .select('*, organization:organizations(id, name, type)')
            .eq('id', id)
            .maybeSingle();

          if (dbEvent) eventData = dbEvent;
        } catch {}
      }

      // Fallback to local real campus events list
      if (!eventData && id) {
        const found = REAL_CAMPUS_EVENTS.find((e) => e.id === id);
        if (found) {
          eventData = found;
        }
      }

      setEvent(eventData);

      if (eventData) {
        let regsList: any[] = [];
        let attList: any[] = [];

        if (isUUID(eventData.id)) {
          try {
            const [regsRes, attRes] = await Promise.all([
              supabase.from('event_registrations').select('*, student:profiles!event_registrations_student_id_fkey(name, email, department)').eq('event_id', eventData.id),
              supabase.from('attendance').select('*').eq('event_id', eventData.id),
            ]);
            regsList = regsRes.data || [];
            attList = attRes.data || [];
          } catch {}
        }

        // Merge local registrations from browser cache
        try {
          const rawLocal = localStorage.getItem('kec_local_registrations');
          if (rawLocal) {
            const localRegs = JSON.parse(rawLocal);
            const matching = localRegs.filter((r: any) => r.event_id === eventData.id && r.participation_status !== 'cancelled');
            regsList = [...matching, ...regsList.filter((r: any) => !matching.some((lr: any) => lr.student_id === r.student_id))];
          }
        } catch {}

        setRegistrations(regsList);
        setAttendance(attList);

        if (profile?.id) {
          const myReg = regsList.find((r: any) => r.student_id === profile.id || r.student?.email === profile.email);
          setMyRegistration(myReg || null);
        }
      }
    } catch (err) {
      console.warn('Error loading event data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async () => {
    if (!profile?.id || !event) return;
    setActionLoading(true);
    try {
      if (isUUID(event.id) && isUUID(profile.id)) {
        try {
          await supabase.from('event_registrations').insert({
            event_id: event.id,
            student_id: profile.id,
            participation_status: 'registered',
          });
        } catch {}
      }

      // Guaranteed local storage
      const localRecord = {
        id: 'reg-' + Date.now(),
        event_id: event.id,
        student_id: profile.id,
        participation_status: 'registered',
        registration_date: new Date().toISOString(),
        student: { name: profile.name, email: profile.email, department: profile.department },
      };

      try {
        const rawLocal = localStorage.getItem('kec_local_registrations');
        const list = rawLocal ? JSON.parse(rawLocal) : [];
        const existingIdx = list.findIndex((r: any) => r.event_id === event.id && r.student_id === profile.id);
        if (existingIdx >= 0) {
          list[existingIdx] = localRecord;
        } else {
          list.push(localRecord);
        }
        localStorage.setItem('kec_local_registrations', JSON.stringify(list));
      } catch {}

      setMyRegistration(localRecord);
      setRegistrations((prev) => [localRecord, ...prev.filter((r) => r.student_id !== profile.id)]);
      toast('Successfully registered for event!', 'success');
    } catch (err: any) {
      toast(err.message || 'Failed to register', 'error');
    } finally {
      setActionLoading(false);
    }
  };

  const handleCancelRegistration = async () => {
    if (!myRegistration) return;
    setActionLoading(true);
    try {
      if (isUUID(myRegistration.id)) {
        try {
          await supabase
            .from('event_registrations')
            .update({ participation_status: 'cancelled' })
            .eq('id', myRegistration.id);
        } catch {}
      }

      try {
        const rawLocal = localStorage.getItem('kec_local_registrations');
        if (rawLocal) {
          const list = JSON.parse(rawLocal);
          const idx = list.findIndex((r: any) => r.id === myRegistration.id || (r.event_id === event?.id && r.student_id === profile?.id));
          if (idx >= 0) {
            list[idx].participation_status = 'cancelled';
            localStorage.setItem('kec_local_registrations', JSON.stringify(list));
          }
        }
      } catch {}

      setMyRegistration(null);
      setRegistrations((prev) => prev.filter((r) => r.id !== myRegistration.id && r.student_id !== profile?.id));
      toast('Registration cancelled', 'info');
    } catch {
      toast('Failed to cancel registration', 'error');
    } finally {
      setActionLoading(false);
    }
  };

  if (loading) return <LoadingSpinner />;
  if (!event) {
    return (
      <EmptyState
        title="Event not found"
        action={
          <Button variant="outline" onClick={() => navigate('/events')}>
            Back to Calendar
          </Button>
        }
      />
    );
  }

  const activeRegs = registrations.filter((r) => r.participation_status !== 'cancelled');

  return (
    <div className="space-y-6 font-sans w-full">
      {/* Breadcrumb Navigation */}
      <div className="text-xs text-[#54595d] dark:text-[#9ca3af]">
        <Link to="/events" className="wiki-link">
          ← Back to Events Calendar
        </Link>
      </div>

      {/* Wikipedia Article Heading */}
      <PageHeader
        title={event.title}
        subtitle={`Organized by ${event.organization?.name || 'Kongu Campus'} • ${event.location || 'Kongu Engineering College'}`}
        action={
          isStudent && (
            <div>
              {!myRegistration || myRegistration.participation_status === 'cancelled' ? (
                <Button variant="primary" size="sm" onClick={handleRegister} loading={actionLoading}>
                  Register for Event
                </Button>
              ) : (
                <div className="flex items-center gap-2">
                  <span className="border border-[#a2a9b1] bg-[#eaecf0] px-2 py-1 text-xs font-bold text-[#0645ad]">
                    ✓ Registered
                  </span>
                  <button
                    onClick={handleCancelRegistration}
                    disabled={actionLoading}
                    className="text-[#cc0000] hover:underline text-xs cursor-pointer ml-1"
                  >
                    [ Cancel RSVP ]
                  </button>
                </div>
              )}
            </div>
          )
        }
      />

      {/* Grid: Article Body (left) and Wikipedia Infobox (right) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Main Content Area */}
        <div className="lg:col-span-8 space-y-6">
          <div className="text-sm leading-relaxed space-y-3 text-[#202122] dark:text-[#e5e7eb]">
            <p>
              <strong>{event.title}</strong> is a campus extracurricular event categorized under <em>{event.event_type}</em>, scheduled by <strong>{event.organization?.name}</strong> at Kongu Engineering College.
            </p>
            {event.description && (
              <div className="wiki-card p-4 text-xs leading-relaxed">
                <div className="font-bold text-xs uppercase mb-1">Event Prospectus & Objectives:</div>
                <p className="text-[#54595d] dark:text-[#9ca3af]">{event.description}</p>
              </div>
            )}
            {event.instructions && (
              <div className="wiki-card p-4 text-xs leading-relaxed">
                <div className="font-bold text-xs uppercase mb-1">Instructions for Participants:</div>
                <p className="text-[#54595d] dark:text-[#9ca3af]">{event.instructions}</p>
              </div>
            )}
          </div>

          {/* Roster of Registered Participants */}
          <div className="wiki-card">
            <div className="wiki-card-header flex items-center justify-between">
              <span>Registered Student Participants ({activeRegs.length})</span>
              {(isAdmin || isCoordinator) && (
                <Link to="/attendance" className="wiki-link text-xs font-normal">
                  Take Attendance →
                </Link>
              )}
            </div>
            {activeRegs.length === 0 ? (
              <div className="p-4">
                <EmptyState title="No students have registered for this event yet." />
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="wikitable">
                  <thead>
                    <tr>
                      <th style={{ width: '40%' }}>Student Name</th>
                      <th style={{ width: '35%' }}>Email & Department</th>
                      <th style={{ width: '25%' }} className="text-center">Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {activeRegs.map((r) => (
                      <tr key={r.id}>
                        <td>
                          <span className="wiki-link font-medium">{r.student?.name || 'Student Participant'}</span>
                        </td>
                        <td>
                          <div className="text-xs">{r.student?.email}</div>
                          <div className="text-[11px] text-[#72777d]">{r.student?.department}</div>
                        </td>
                        <td className="text-center">
                          <span className="border border-[#a2a9b1] bg-[#eaf3ff] text-[#0645ad] px-1.5 py-0.2 text-[11px] font-medium capitalize">
                            {r.participation_status}
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

        {/* Wikipedia Infobox (Right Column) */}
        <div className="lg:col-span-4 wiki-card">
          <div className="wiki-card-header text-center">
            Event Specifications
          </div>

          <table className="wikitable text-xs">
            <tbody>
              <tr>
                <td className="font-bold bg-[#eaecf0] dark:bg-[#1f2937]" style={{ width: '40%' }}>Event Name</td>
                <td>{event.title}</td>
              </tr>
              <tr>
                <td className="font-bold bg-[#eaecf0] dark:bg-[#1f2937]">Organizing Body</td>
                <td>
                  <span className="wiki-link font-medium">{event.organization?.name}</span>
                </td>
              </tr>
              <tr>
                <td className="font-bold bg-[#eaecf0] dark:bg-[#1f2937]">Classification</td>
                <td className="capitalize">{event.event_type}</td>
              </tr>
              <tr>
                <td className="font-bold bg-[#eaecf0] dark:bg-[#1f2937]">Status</td>
                <td className="capitalize font-bold text-[#0645ad]">{event.status}</td>
              </tr>
              <tr>
                <td className="font-bold bg-[#eaecf0] dark:bg-[#1f2937]">Start Date</td>
                <td>{formatDateTime(event.start_date)}</td>
              </tr>
              <tr>
                <td className="font-bold bg-[#eaecf0] dark:bg-[#1f2937]">End Date</td>
                <td>{formatDateTime(event.end_date)}</td>
              </tr>
              <tr>
                <td className="font-bold bg-[#eaecf0] dark:bg-[#1f2937]">Campus Venue</td>
                <td>{event.location || 'Kongu Campus'}</td>
              </tr>
              <tr>
                <td className="font-bold bg-[#eaecf0] dark:bg-[#1f2937]">Enrollment</td>
                <td className="font-mono">{activeRegs.length} / {event.maximum_participants || '∞'} Seats</td>
              </tr>
              {event.registration_deadline && (
                <tr>
                  <td className="font-bold bg-[#eaecf0] dark:bg-[#1f2937]">RSVP Deadline</td>
                  <td>{formatDate(event.registration_deadline)}</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
