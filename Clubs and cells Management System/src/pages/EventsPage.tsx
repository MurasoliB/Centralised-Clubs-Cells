import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Plus, Calendar, MapPin, Users, Clock, Download, Search } from 'lucide-react';
import { supabase } from '@/lib/supabase';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/context/ToastContext';
import { Button } from '@/components/ui/Button';
import { Modal } from '@/components/ui/Modal';
import { Input, Select, Textarea } from '@/components/ui/Input';
import { SearchBar } from '@/components/ui/SearchBar';
import { EmptyState, LoadingSpinner } from '@/components/ui/EmptyState';
import { PageHeader } from '@/components/layout/PageHeader';
import { EVENT_TYPES } from '@/lib/constants';
import { formatDate, exportToCsv } from '@/lib/utils';
import { cache } from '@/lib/cache';
import { getAssignedClubForUser, type AssignedClub } from '@/lib/orgScope';
import { REAL_CAMPUS_EVENTS } from '@/lib/eventsData';

export function EventsPage() {
  const { profile } = useAuth();
  const { toast } = useToast();
  const navigate = useNavigate();
  const cachedEvents = cache.get<any[]>('events_list');
  const [events, setEvents] = useState<any[]>(cachedEvents && cachedEvents.length > 0 ? cachedEvents : REAL_CAMPUS_EVENTS);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [typeFilter, setTypeFilter] = useState('');
  const [clubFilter, setClubFilter] = useState<'all' | 'my_club'>('all');
  const [myClub, setMyClub] = useState<AssignedClub | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [creating, setCreating] = useState(false);
  const [myOrgs, setMyOrgs] = useState<any[]>([]);
  const [newEvent, setNewEvent] = useState({
    organization_id: '', title: '', description: '', event_type: 'workshop',
    location: '', start_date: '', end_date: '', registration_deadline: '',
    maximum_participants: '', instructions: '', banner: '',
  });

  const isAdmin = profile?.role === 'admin';
  const isCoordinator = profile?.role === 'faculty_coordinator' || profile?.role === 'club_coordinator';
  const canCreate = isAdmin || isCoordinator;

  useEffect(() => {
    loadEvents();
    if (canCreate) loadMyOrgs();
  }, [profile?.id, profile?.role]);

  const loadMyOrgs = async () => {
    if (!isAdmin && profile) {
      const club = await getAssignedClubForUser(profile);
      setMyClub(club);
      if (club) {
        setMyOrgs([{ id: club.id, name: club.name }]);
        setNewEvent((prev) => ({ ...prev, organization_id: club.id }));
      }
    } else {
      const { data } = await supabase.from('organizations').select('id, name').eq('status', 'active');
      setMyOrgs(data || []);
      if (data && data.length > 0) {
        setNewEvent((prev) => ({ ...prev, organization_id: data[0].id }));
      }
    }
  };

  const loadEvents = async () => {
    if (!cache.has('events_list')) {
      setLoading(true);
    }
    try {
      const [eventsRes, regsRes, resolvedClub] = await Promise.all([
        supabase.from('events').select('*, organization:organizations(id, name, type, short_name)').order('start_date', { ascending: true }),
        supabase.from('event_registrations').select('event_id').neq('participation_status', 'cancelled'),
        getAssignedClubForUser(profile),
      ]);

      if (resolvedClub) setMyClub(resolvedClub);

      const rawEvents = eventsRes.data && eventsRes.data.length > 0 ? eventsRes.data : REAL_CAMPUS_EVENTS;
      const regMap: Record<string, number> = {};
      (regsRes.data || []).forEach((r) => {
        regMap[r.event_id] = (regMap[r.event_id] || 0) + 1;
      });

      const eventsWithCounts = rawEvents.map((e: any) => ({
        ...e,
        registrationCount: regMap[e.id] || 0,
      }));

      setEvents(eventsWithCounts);
      cache.set('events_list', eventsWithCounts);
    } catch {
      setEvents(REAL_CAMPUS_EVENTS);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async () => {
    if (!newEvent.title || !newEvent.start_date || !newEvent.end_date || !newEvent.organization_id) {
      toast('Please provide event title, organizing club, and start/end dates', 'error');
      return;
    }
    setCreating(true);
    try {
      const { error } = await supabase.from('events').insert({
        organization_id: newEvent.organization_id,
        title: newEvent.title,
        description: newEvent.description,
        event_type: newEvent.event_type,
        location: newEvent.location,
        start_date: newEvent.start_date,
        end_date: newEvent.end_date,
        registration_deadline: newEvent.registration_deadline || newEvent.start_date,
        maximum_participants: newEvent.maximum_participants ? parseInt(newEvent.maximum_participants) : null,
        instructions: newEvent.instructions,
        status: 'upcoming',
        created_by: profile?.id,
      });
      if (error) throw error;
      toast('Event published successfully', 'success');
      setModalOpen(false);
      loadEvents();
    } catch (err: any) {
      toast(err.message || 'Failed to publish event', 'error');
    } finally {
      setCreating(false);
    }
  };

  const handleExport = () => {
    exportToCsv('campus_events_schedule.csv', events.map((e) => ({
      title: e.title,
      organization: e.organization?.name,
      event_type: e.event_type,
      start_date: e.start_date,
      end_date: e.end_date,
      location: e.location,
      status: e.status,
      registrations: e.registrationCount || 0,
    })));
    toast('Events schedule exported to CSV', 'success');
  };

  const filteredEvents = events.filter((e) => {
    if (clubFilter === 'my_club' && myClub) {
      const isMatch = e.organization_id === myClub.id || e.organization?.name?.toLowerCase() === myClub.name.toLowerCase();
      if (!isMatch) return false;
    }
    if (statusFilter && e.status !== statusFilter) return false;
    if (typeFilter && e.event_type !== typeFilter) return false;
    if (search.trim()) {
      const q = search.toLowerCase();
      return (
        e.title?.toLowerCase().includes(q) ||
        (e.location && e.location.toLowerCase().includes(q)) ||
        (e.organization?.name && e.organization.name.toLowerCase().includes(q))
      );
    }
    return true;
  });

  return (
    <div className="space-y-6 font-sans w-full">
      <PageHeader
        title="Calendar of Events & Symposia"
        subtitle="Chronological roster of accredited technical hackathons, workshops, symposiums, and cultural tournaments"
        action={
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm" onClick={handleExport}>
              <Download className="h-3.5 w-3.5 mr-1" /> Export CSV
            </Button>
            {canCreate && (
              <Button variant="primary" size="sm" onClick={() => setModalOpen(true)}>
                <Plus className="h-3.5 w-3.5 mr-1" /> Create Event
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
            placeholder="Search events by title, venue, or keyword..."
          />
        </div>

        <div className="flex flex-wrap items-center gap-2">
          {isCoordinator && myClub && (
            <div className="inline-flex border border-[#a2a9b1] dark:border-[#374151]">
              <button
                onClick={() => setClubFilter('all')}
                className={`px-2.5 py-1 text-xs ${
                  clubFilter === 'all'
                    ? 'bg-white dark:bg-[#111827] font-bold text-[#202122] dark:text-[#f3f4f6]'
                    : 'bg-[#f8f9fa] dark:bg-[#1f2937] wiki-link'
                }`}
              >
                All Events
              </button>
              <button
                onClick={() => setClubFilter('my_club')}
                className={`px-2.5 py-1 text-xs ${
                  clubFilter === 'my_club'
                    ? 'bg-white dark:bg-[#111827] font-bold text-[#202122] dark:text-[#f3f4f6]'
                    : 'bg-[#f8f9fa] dark:bg-[#1f2937] wiki-link'
                }`}
              >
                {myClub.name}
              </button>
            </div>
          )}

          <Select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            options={[
              { value: 'upcoming', label: 'Upcoming' },
              { value: 'ongoing', label: 'Ongoing' },
              { value: 'completed', label: 'Completed' },
              { value: 'cancelled', label: 'Cancelled' },
            ]}
            placeholder="All Statuses"
            className="text-xs w-32"
          />

          <Select
            value={typeFilter}
            onChange={(e) => setTypeFilter(e.target.value)}
            options={EVENT_TYPES.map((t) => ({ value: t, label: t.charAt(0).toUpperCase() + t.slice(1) }))}
            placeholder="All Categories"
            className="text-xs w-36"
          />
        </div>
      </div>

      {/* Events Table View */}
      {loading && events.length === 0 ? (
        <LoadingSpinner />
      ) : filteredEvents.length === 0 ? (
        <EmptyState
          title="No events match your criteria"
          description="Try broadening your search filters or check back later for newly scheduled activities."
        />
      ) : (
        <div className="wiki-card overflow-x-auto">
          <div className="wiki-card-header flex items-center justify-between">
            <span>Official Campus Schedule ({filteredEvents.length} Events)</span>
            <span className="text-xs font-normal text-[#54595d] dark:text-[#9ca3af]">
              Accredited Participation Points Apply
            </span>
          </div>

          <table className="wikitable">
            <thead>
              <tr>
                <th style={{ width: '32%' }}>Event Title & Category</th>
                <th style={{ width: '22%' }}>Organizing Body</th>
                <th style={{ width: '16%' }}>Date & Time</th>
                <th style={{ width: '16%' }}>Venue Location</th>
                <th style={{ width: '14%' }} className="text-right">Action</th>
              </tr>
            </thead>
            <tbody>
              {filteredEvents.map((evt) => (
                <tr key={evt.id}>
                  <td>
                    <Link to={`/events/${evt.id}`} className="wiki-link font-bold text-sm">
                      {evt.title}
                    </Link>
                    <div className="text-[11px] text-[#54595d] dark:text-[#9ca3af] mt-0.5">
                      Type: <span className="capitalize">{evt.event_type}</span> • Status: <span className="capitalize font-medium">{evt.status}</span>
                    </div>
                  </td>
                  <td>
                    <span className="font-medium text-[#202122] dark:text-[#f3f4f6]">
                      {evt.organization?.name || 'Kongu Campus'}
                    </span>
                  </td>
                  <td>
                    <span className="text-xs">{formatDate(evt.start_date)}</span>
                  </td>
                  <td>
                    <span className="text-xs">{evt.location || 'Kongu Engineering College'}</span>
                  </td>
                  <td className="text-right whitespace-nowrap">
                    <Link to={`/events/${evt.id}`} className="wiki-link text-xs">
                      [ RSVP / Details ]
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Create Event Modal */}
      <Modal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        title="Schedule New Extracurricular Event"
        description="Publish an institutional symposium, workshop, or contest to the student radar."
      >
        <div className="space-y-3 pt-1 text-xs">
          <Input
            label="Event Title"
            value={newEvent.title}
            onChange={(e) => setNewEvent({ ...newEvent, title: e.target.value })}
            placeholder="e.g. HackKEC 2026: 24-Hour Hackathon"
            required
          />
          <Select
            label="Organizing Club or Cell"
            value={newEvent.organization_id}
            onChange={(e) => setNewEvent({ ...newEvent, organization_id: e.target.value })}
            options={myOrgs.map((o) => ({ value: o.id, label: o.name }))}
            required
          />
          <div className="grid grid-cols-2 gap-3">
            <Select
              label="Event Type"
              value={newEvent.event_type}
              onChange={(e) => setNewEvent({ ...newEvent, event_type: e.target.value })}
              options={EVENT_TYPES.map((t) => ({ value: t, label: t.charAt(0).toUpperCase() + t.slice(1) }))}
            />
            <Input
              label="Campus Venue"
              value={newEvent.location}
              onChange={(e) => setNewEvent({ ...newEvent, location: e.target.value })}
              placeholder="e.g. CC3 Lab / Convention Center"
            />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <Input
              label="Start Date & Time"
              type="datetime-local"
              value={newEvent.start_date}
              onChange={(e) => setNewEvent({ ...newEvent, start_date: e.target.value })}
              required
            />
            <Input
              label="End Date & Time"
              type="datetime-local"
              value={newEvent.end_date}
              onChange={(e) => setNewEvent({ ...newEvent, end_date: e.target.value })}
              required
            />
          </div>
          <Textarea
            label="Description & Event Objectives"
            value={newEvent.description}
            onChange={(e) => setNewEvent({ ...newEvent, description: e.target.value })}
            placeholder="Detailed overview and rules for participating students..."
          />
          <div className="flex justify-end gap-2 pt-3 border-t border-[#a2a9b1] dark:border-[#374151]">
            <Button variant="outline" size="sm" onClick={() => setModalOpen(false)}>
              Cancel
            </Button>
            <Button variant="primary" size="sm" onClick={handleCreate} loading={creating}>
              Publish Event
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
}
