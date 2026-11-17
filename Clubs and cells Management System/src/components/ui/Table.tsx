import { type ReactNode } from 'react';
import { cn } from '@/lib/utils';

interface Column<T> {
  key: string;
  header: string;
  render?: (row: T) => ReactNode;
  className?: string;
}

interface DataTableProps<T> {
  columns: Column<T>[];
  data: T[];
  loading?: boolean;
  emptyMessage?: string;
  onRowClick?: (row: T) => void;
}

export function DataTable<T extends { id: string }>({
  columns,
  data,
  loading,
  emptyMessage = 'No data found',
  onRowClick,
}: DataTableProps<T>) {
  if (loading) {
    return (
      <div className="flex items-center justify-center py-12 border border-[#a2a9b1] bg-white dark:bg-slate-900">
        <div className="h-6 w-6 animate-spin rounded-full border-2 border-slate-300 border-t-[#0645ad]" />
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="py-8 text-center text-xs text-[#54595d] dark:text-slate-400 border border-[#a2a9b1] bg-[#f8f9fa] dark:bg-slate-900 rounded-[2px]">
        {emptyMessage}
      </div>
    );
  }

  return (
    <div className="overflow-x-auto shadow-[0_1px_1px_rgba(0,0,0,0.05)]">
      <table className="wikitable w-full border-collapse border border-[#a2a9b1] dark:border-slate-700">
        <thead>
          <tr className="bg-[#eaecf0] dark:bg-slate-800">
            {columns.map((col) => (
              <th
                key={col.key}
                className={cn(
                  'border border-[#a2a9b1] dark:border-slate-700 px-3 py-2 text-left text-xs font-bold text-[#202122] dark:text-slate-100 uppercase tracking-tight',
                  col.className,
                )}
              >
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, idx) => (
            <tr
              key={row.id}
              onClick={() => onRowClick?.(row)}
              className={cn(
                idx % 2 === 1 ? 'bg-[#f8f9fa] dark:bg-slate-850' : 'bg-white dark:bg-slate-900',
                'hover:bg-[#eaf3ff] dark:hover:bg-slate-800 transition-colors',
                onRowClick && 'cursor-pointer',
              )}
            >
              {columns.map((col) => (
                <td
                  key={col.key}
                  className={cn(
                    'border border-[#a2a9b1] dark:border-slate-700 px-3 py-2 text-xs sm:text-[13px] text-[#202122] dark:text-slate-300',
                    col.className,
                  )}
                >
                  {col.render ? col.render(row) : (row as Record<string, unknown>)[col.key] as ReactNode}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
