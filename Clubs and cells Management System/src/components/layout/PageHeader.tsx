import { type ReactNode } from 'react';
import { cn } from '@/lib/utils';

interface PageHeaderProps {
  title: string;
  description?: string;
  action?: ReactNode;
  badge?: ReactNode;
  className?: string;
}

export function PageHeader({ title, description, action, badge, className }: PageHeaderProps) {
  return (
    <div className={cn('mb-5 pb-2.5 border-b border-[#a2a9b1] dark:border-slate-700', className)}>
      <div className="flex flex-col sm:flex-row sm:items-baseline sm:justify-between gap-3">
        <div className="space-y-1">
          <div className="flex items-baseline gap-3 flex-wrap">
            <h1 className="text-2xl sm:text-3xl font-serif font-normal text-[#202122] dark:text-slate-100 tracking-tight">
              {title}
            </h1>
            {badge}
          </div>
          <p className="text-xs text-[#54595d] dark:text-slate-400 font-sans leading-normal">
            From ClubHub, the official extracurricular repository
            {description && (
              <>
                {' '}• <span className="text-[#202122] dark:text-slate-300 font-medium">{description}</span>
              </>
            )}
          </p>
        </div>
        {action && (
          <div className="flex-shrink-0 flex items-center gap-2 flex-wrap pt-1 sm:pt-0">
            {action}
          </div>
        )}
      </div>
    </div>
  );
}
