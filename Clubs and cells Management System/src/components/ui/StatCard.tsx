import React from 'react';
import { type LucideIcon } from 'lucide-react';
import { cn } from '@/lib/utils';

export interface StatCardProps {
  label?: string;
  title?: string;
  value: string | number;
  icon?: LucideIcon | React.ReactNode;
  color?: 'blue' | 'emerald' | 'amber' | 'purple' | 'red' | 'cyan' | 'rose' | 'indigo';
  variant?: 'blue' | 'emerald' | 'amber' | 'purple' | 'red' | 'cyan' | 'rose' | 'indigo';
  trend?: string;
  description?: string;
  subtitle?: string;
}

export function StatCard({
  label,
  title,
  value,
  icon,
  trend,
  description,
  subtitle,
}: StatCardProps) {
  const displayLabel = label || title || 'Summary Data';
  const displayDesc = description || subtitle;

  const renderIcon = () => {
    if (!icon) return null;
    if (React.isValidElement(icon)) {
      return icon;
    }
    const IconComponent = icon as LucideIcon;
    return <IconComponent className="h-4 w-4 text-[#54595d] dark:text-[#9ca3af]" />;
  };

  return (
    <div className="rounded-[2px] border border-[#a2a9b1] bg-white dark:border-[#374151] dark:bg-[#111827] shadow-[0_1px_1px_rgba(0,0,0,0.05)]">
      {/* Wikipedia Infobox style top bar */}
      <div className="bg-[#eaecf0] dark:bg-[#1f2937] border-b border-[#a2a9b1] dark:border-[#374151] px-3 py-1.5 flex items-center justify-between">
        <span className="font-sans text-xs font-bold text-[#202122] dark:text-[#f3f4f6] uppercase tracking-wide">
          {displayLabel}
        </span>
        <div className="opacity-80">
          {renderIcon()}
        </div>
      </div>

      {/* Body */}
      <div className="p-3.5">
        <div className="text-2xl sm:text-3xl font-serif font-bold text-[#202122] dark:text-[#f9fafb]">
          {value}
        </div>

        {(trend || displayDesc) && (
          <div className="mt-2 flex items-center gap-2 text-xs text-[#54595d] dark:text-[#9ca3af]">
            {trend && (
              <span className="inline-block border border-[#a2a9b1] dark:border-[#374151] bg-[#f8f9fa] dark:bg-[#1f2937] px-1.5 py-0.2 text-[11px] font-medium text-[#0645ad] dark:text-[#6b9eff]">
                {trend}
              </span>
            )}
            {displayDesc && (
              <span className="truncate">{displayDesc}</span>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
