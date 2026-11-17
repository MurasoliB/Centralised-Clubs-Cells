import { type HTMLAttributes } from 'react';
import { cn } from '@/lib/utils';

interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  className?: string;
  dot?: boolean;
  dotColor?: string;
}

export function Badge({ className, dot, dotColor, children, ...props }: BadgeProps) {
  return (
    <span
      className={cn(
        'inline-flex items-center gap-1.5 rounded-[2px] border border-[#a2a9b1] bg-[#eaecf0] px-2 py-0.5 text-xs font-medium text-[#202122] dark:border-[#374151] dark:bg-[#1f2937] dark:text-[#f3f4f6]',
        className,
      )}
      {...props}
    >
      {dot && (
        <span
          className={cn(
            'h-1.5 w-1.5 rounded-full',
            dotColor || 'bg-current',
          )}
        />
      )}
      {children}
    </span>
  );
}
