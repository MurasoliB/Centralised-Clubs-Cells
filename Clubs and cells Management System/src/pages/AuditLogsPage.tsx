import { useEffect, useState } from 'react';
import { Shield, Clock } from 'lucide-react';
import { supabase } from '@/lib/supabase';
import { useToast } from '@/context/ToastContext';
import { Input } from '@/components/ui/Input';
import { LoadingSpinner, EmptyState } from '@/components/ui/EmptyState';
import { PageHeader } from '@/components/layout/PageHeader';
import { formatDateTime } from '@/lib/utils';
import { cache } from '@/lib/cache';

export function AuditLogsPage() {
  const { toast } = useToast();
  const cached = cache.get<any[]>('audit_logs');
  const [logs, setLogs] = useState<any[]>(cached || []);
  const [loading, setLoading] = useState(!cached);
  const [search, setSearch] = useState('');

  useEffect(() => {
    loadLogs();
  }, []);

  const loadLogs = async () => {
    if (!cache.has('audit_logs')) {
      setLoading(true);
    }
    try {
      const { data } = await supabase
        .from('audit_logs')
        .select('*, user:profiles!audit_logs_user_id_fkey(name)')
        .order('created_at', { ascending: false })
        .limit(100);
      const list = data || [];
      setLogs(list);
      cache.set('audit_logs', list);
    } catch {
      toast('Failed to load audit logs', 'error');
    } finally {
      setLoading(false);
    }
  };

  const filteredLogs = logs.filter(
    (l) =>
      l.action?.toLowerCase().includes(search.toLowerCase()) ||
      l.user?.name?.toLowerCase().includes(search.toLowerCase()) ||
      l.entity_type?.toLowerCase().includes(search.toLowerCase())
  );

  if (loading) return <LoadingSpinner />;

  return (
    <div className="space-y-6 font-sans w-full">
      <PageHeader
        title="System Governance & Audit Trail"
        subtitle="Chronological audit log of administrative events, account provisioning, and accreditation records"
      />

      <div className="p-3 border border-[#a2a9b1] dark:border-[#374151] bg-[#f8f9fa] dark:bg-[#111827] flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 text-xs rounded-[2px]">
        <div className="flex-1 max-w-sm">
          <Input
            placeholder="Search audit trail by user, action or entity..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <div className="text-[#54595d] dark:text-[#9ca3af]">
          Showing {filteredLogs.length} logged actions
        </div>
      </div>

      {filteredLogs.length === 0 ? (
        <EmptyState
          title="No audit entries match the query"
          description="Administrative actions are automatically recorded in this log."
        />
      ) : (
        <div className="wiki-card overflow-x-auto">
          <div className="wiki-card-header">
            Institutional Audit Trail (Recent 100 Actions)
          </div>
          <table className="wikitable">
            <thead>
              <tr>
                <th style={{ width: '22%' }}>Timestamp</th>
                <th style={{ width: '20%' }}>User Authority</th>
                <th style={{ width: '20%' }}>Action Performed</th>
                <th style={{ width: '18%' }}>Target Entity</th>
                <th style={{ width: '20%' }}>IP / Audit Reference</th>
              </tr>
            </thead>
            <tbody>
              {filteredLogs.map((log) => (
                <tr key={log.id}>
                  <td className="font-mono text-xs whitespace-nowrap">
                    {formatDateTime(log.created_at)}
                  </td>
                  <td>
                    <span className="wiki-link font-medium">
                      {log.user?.name || 'Administrator'}
                    </span>
                  </td>
                  <td>
                    <span className="font-semibold text-[#202122] dark:text-[#f3f4f6]">
                      {log.action}
                    </span>
                  </td>
                  <td>
                    <span className="border border-[#a2a9b1] bg-[#f8f9fa] px-1 py-0.2 text-[11px] font-mono">
                      {log.entity_type || 'system'}
                    </span>
                  </td>
                  <td className="text-xs text-[#54595d] dark:text-[#9ca3af]">
                    {log.entity_id ? `ID: ${log.entity_id.slice(0, 8)}...` : 'Automated Trigger'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
