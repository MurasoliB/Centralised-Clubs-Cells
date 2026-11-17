import { useEffect, useState } from 'react';
import { Bell, CheckCheck, Trash2, Calendar, Megaphone, Users, Award, Shield, Check, Clock } from 'lucide-react';
import { supabase } from '@/lib/supabase';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/context/ToastContext';
import { Button } from '@/components/ui/Button';
import { EmptyState, LoadingSpinner } from '@/components/ui/EmptyState';
import { PageHeader } from '@/components/layout/PageHeader';
import { formatRelativeTime } from '@/lib/utils';

export function NotificationsPage() {
  const { profile } = useAuth();
  const { toast } = useToast();
  const [notifications, setNotifications] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    if (profile?.id) {
      loadNotifications();
    }
  }, [profile?.id]);

  const loadNotifications = async () => {
    setLoading(true);
    try {
      const { data, error } = await supabase
        .from('notifications')
        .select('*')
        .eq('user_id', profile?.id)
        .order('created_at', { ascending: false });

      if (error) throw error;
      setNotifications(data || []);
    } catch {
      toast('Failed to load notifications', 'error');
    } finally {
      setLoading(false);
    }
  };

  const markAsRead = async (id: string) => {
    try {
      await supabase.from('notifications').update({ is_read: true }).eq('id', id);
      setNotifications((prev) =>
        prev.map((n) => (n.id === id ? { ...n, is_read: true } : n))
      );
    } catch {
      toast('Failed to update notification', 'error');
    }
  };

  const markAllAsRead = async () => {
    try {
      await supabase
        .from('notifications')
        .update({ is_read: true })
        .eq('user_id', profile?.id)
        .eq('is_read', false);

      setNotifications((prev) => prev.map((n) => ({ ...n, is_read: true })));
      toast('All notifications marked as read', 'success');
    } catch {
      toast('Failed to mark all as read', 'error');
    }
  };

  const deleteNotification = async (id: string) => {
    try {
      await supabase.from('notifications').delete().eq('id', id);
      setNotifications((prev) => prev.filter((n) => n.id !== id));
      toast('Notification deleted', 'success');
    } catch {
      toast('Failed to delete notification', 'error');
    }
  };

  const unreadCount = notifications.filter((n) => !n.is_read).length;

  const filteredNotifications = notifications.filter((n) => {
    if (filter === 'unread') return !n.is_read;
    if (filter === 'event') return n.type === 'event';
    if (filter === 'announcement') return n.type === 'announcement';
    if (filter === 'membership') return n.type === 'membership';
    return true;
  });

  if (loading) return <LoadingSpinner />;

  return (
    <div className="space-y-6 font-sans w-full">
      <PageHeader
        title="Institutional Alerts & Notification Inbox"
        subtitle="Operational announcements, membership authentications, and event notifications"
        action={
          unreadCount > 0 && (
            <Button variant="outline" size="sm" onClick={markAllAsRead}>
              <CheckCheck className="h-3.5 w-3.5 mr-1" /> Mark All Read
            </Button>
          )
        }
      />

      {/* Vector Filter Tabs */}
      <div className="flex items-center border-b border-[#a2a9b1] dark:border-[#374151]">
        {[
          { label: 'All Alerts', value: 'all', count: notifications.length },
          { label: 'Unread', value: 'unread', count: unreadCount },
          { label: 'Events', value: 'event', count: notifications.filter((n) => n.type === 'event').length },
          { label: 'Circulars', value: 'announcement', count: notifications.filter((n) => n.type === 'announcement').length },
          { label: 'Memberships', value: 'membership', count: notifications.filter((n) => n.type === 'membership').length },
        ].map((tab) => (
          <button
            key={tab.value}
            onClick={() => setFilter(tab.value)}
            className={`wiki-tab ${filter === tab.value ? 'active' : ''}`}
          >
            <span>{tab.label} ({tab.count})</span>
          </button>
        ))}
      </div>

      {filteredNotifications.length === 0 ? (
        <EmptyState
          title="No notifications matching this filter"
          description="You are completely caught up on your institutional alerts."
        />
      ) : (
        <div className="wiki-card divide-y divide-[#a2a9b1] dark:divide-[#374151]">
          {filteredNotifications.map((n) => (
            <div
              key={n.id}
              className={`p-4 flex items-start justify-between gap-4 transition-colors ${
                n.is_read
                  ? 'bg-white dark:bg-[#111827]'
                  : 'bg-[#f0f4ff] dark:bg-[#17223b]'
              }`}
            >
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <span className="font-bold text-sm text-[#202122] dark:text-[#f3f4f6]">
                    {n.title}
                  </span>
                  {!n.is_read && (
                    <span className="bg-[#cc0000] text-white text-[9px] px-1 font-bold rounded-[2px]">
                      NEW
                    </span>
                  )}
                </div>
                <p className="mt-1 text-xs text-[#54595d] dark:text-[#9ca3af] leading-relaxed">
                  {n.message}
                </p>
                <div className="mt-2 text-[11px] text-[#72777d] flex items-center gap-2">
                  <span>{formatRelativeTime(n.created_at)}</span>
                  <span>•</span>
                  <span className="capitalize font-medium">{n.type}</span>
                </div>
              </div>

              <div className="flex items-center gap-2 flex-shrink-0 text-xs">
                {!n.is_read && (
                  <button
                    onClick={() => markAsRead(n.id)}
                    className="wiki-link cursor-pointer text-xs"
                  >
                    [ Mark Read ]
                  </button>
                )}
                <button
                  onClick={() => deleteNotification(n.id)}
                  className="text-[#cc0000] hover:underline cursor-pointer text-xs"
                >
                  [ Delete ]
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
