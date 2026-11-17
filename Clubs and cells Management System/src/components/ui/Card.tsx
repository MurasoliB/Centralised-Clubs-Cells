import { type HTMLAttributes, forwardRef } from 'react';
import { cn } from '@/lib/utils';

export const Card = forwardRef<HTMLDivElement, HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        'rounded-[2px] border border-[#a2a9b1] bg-white shadow-[0_1px_1px_rgba(0,0,0,0.05)] dark:border-slate-700 dark:bg-slate-900 transition-colors',
        className,
      )}
      {...props}
    />
  ),
);
Card.displayName = 'Card';

export const CardHeader = forwardRef<HTMLDivElement, HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        'px-4 py-2.5 bg-[#eaecf0] border-b border-[#a2a9b1] dark:bg-slate-800 dark:border-slate-700',
        className,
      )}
      {...props}
    />
  ),
);
CardHeader.displayName = 'CardHeader';

export const CardTitle = forwardRef<HTMLHeadingElement, HTMLAttributes<HTMLHeadingElement>>(
  ({ className, ...props }, ref) => (
    <h3
      ref={ref}
      className={cn(
        'text-sm sm:text-base font-bold text-[#202122] dark:text-slate-100 font-sans tracking-tight flex items-center gap-2',
        className,
      )}
      {...props}
    />
  ),
);
CardTitle.displayName = 'CardTitle';

export const CardDescription = forwardRef<HTMLParagraphElement, HTMLAttributes<HTMLParagraphElement>>(
  ({ className, ...props }, ref) => (
    <p
      ref={ref}
      className={cn('text-xs text-[#54595d] dark:text-slate-400 mt-0.5 font-sans', className)}
      {...props}
    />
  ),
);
CardDescription.displayName = 'CardDescription';

export const CardContent = forwardRef<HTMLDivElement, HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn('p-4 text-sm text-[#202122] dark:text-slate-200', className)} {...props} />
  ),
);
CardContent.displayName = 'CardContent';

export const CardFooter = forwardRef<HTMLDivElement, HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        'px-4 py-2.5 bg-[#f8f9fa] border-t border-[#a2a9b1] dark:bg-slate-800/60 dark:border-slate-700 text-xs text-[#54595d] dark:text-slate-400',
        className,
      )}
      {...props}
    />
  ),
);
CardFooter.displayName = 'CardFooter';
