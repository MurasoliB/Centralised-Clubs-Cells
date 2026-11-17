import { type ReactNode } from 'react';
import { FileQuestion } from 'lucide-react';
import { cn } from '@/lib/utils';

interface EmptyStateProps {
  icon?: ReactNode;
  title: string;
  description?: string;
  action?: ReactNode;
  className?: string;
}

export function EmptyState({ icon, title, description, action, className }: EmptyStateProps) {
  return (
    <div className={cn('flex flex-col items-center justify-center py-10 px-4 text-center border border-dashed border-[#a2a9b1] dark:border-[#374151] bg-[#f8f9fa] dark:bg-[#111827] my-3', className)}>
      <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-[2px] bg-[#eaecf0] text-[#54595d] dark:bg-[#1f2937] dark:text-[#9ca3af]">
        {icon || <FileQuestion className="h-5 w-5" />}
      </div>
      <h3 className="font-serif text-sm font-bold text-[#202122] dark:text-[#f3f4f6]">{title}</h3>
      {description && <p className="mt-1 text-xs text-[#54595d] dark:text-[#9ca3af] max-w-md">{description}</p>}
      {action && <div className="mt-3">{action}</div>}
    </div>
  );
}

export function LoadingSpinner({ className }: { className?: string }) {
  return (
    <div className={cn('flex flex-col items-center justify-center py-12 gap-2 text-xs text-[#54595d] dark:text-[#9ca3af]', className)}>
      <div className="h-6 w-6 animate-spin rounded-full border-2 border-[#a2a9b1] border-t-[#0645ad] dark:border-[#374151] dark:border-t-[#6b9eff]" />
      <span>Loading repository data...</span>
    </div>
  );
}
