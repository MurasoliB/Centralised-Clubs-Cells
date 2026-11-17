import { type ButtonHTMLAttributes, forwardRef } from 'react';
import { Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';

type Variant = 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger' | 'gradient' | 'emerald' | 'amber' | 'white' | 'darkOutline';
type Size = 'sm' | 'md' | 'lg' | 'icon';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  size?: Size;
  loading?: boolean;
}

const variants: Record<Variant, string> = {
  primary: 'bg-[#0645ad] hover:bg-[#0b0080] text-white border border-[#0645ad] font-semibold hover:underline active:bg-[#082a66]',
  gradient: 'bg-[#2a4b8d] hover:bg-[#1a3668] text-white border border-[#1a3668] font-semibold hover:underline',
  emerald: 'bg-[#1b7e42] hover:bg-[#145d31] text-white border border-[#145d31] font-semibold hover:underline',
  amber: 'bg-[#b8860b] hover:bg-[#8f6808] text-white border border-[#8f6808] font-semibold hover:underline',
  secondary: 'bg-[#f8f9fa] hover:bg-[#ffffff] text-[#202122] border border-[#a2a9b1] hover:border-[#72777d] dark:bg-slate-800 dark:text-slate-100 dark:border-slate-700 dark:hover:bg-slate-750 font-medium',
  outline: 'bg-[#ffffff] hover:bg-[#f8f9fa] text-[#0645ad] hover:text-[#0b0080] hover:underline border border-[#a2a9b1] dark:border-slate-700 dark:bg-slate-900 dark:text-[#6b9eff] font-medium',
  ghost: 'text-[#0645ad] hover:text-[#0b0080] hover:underline hover:bg-[#eaecf0] dark:text-[#6b9eff] dark:hover:bg-slate-800 font-medium',
  danger: 'bg-[#d33] hover:bg-[#b32424] text-white border border-[#b32424] font-semibold hover:underline',
  white: 'bg-white text-[#202122] hover:bg-[#f8f9fa] border border-[#a2a9b1] font-medium',
  darkOutline: 'border border-[#a2a9b1] bg-slate-800 text-white hover:bg-slate-700 font-medium',
};

const sizes: Record<Size, string> = {
  sm: 'h-7 px-2.5 text-xs rounded-[2px]',
  md: 'h-8 px-3.5 text-xs sm:text-[13px] rounded-[2px]',
  lg: 'h-9 px-4 text-sm rounded-[2px] font-semibold',
  icon: 'h-8 w-8 rounded-[2px]',
};

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', size = 'md', loading, children, disabled, ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          'inline-flex items-center justify-center gap-1.5 font-sans transition-all duration-100 cursor-pointer disabled:pointer-events-none disabled:opacity-50 select-none shadow-[0_1px_1px_rgba(0,0,0,0.05)]',
          variants[variant],
          sizes[size],
          className,
        )}
        disabled={disabled || loading}
        {...props}
      >
        {loading && <Loader2 className="h-3.5 w-3.5 animate-spin" />}
        {children}
      </button>
    );
  },
);

Button.displayName = 'Button';
