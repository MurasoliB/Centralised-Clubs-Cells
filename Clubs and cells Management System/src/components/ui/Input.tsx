import { type InputHTMLAttributes, type TextareaHTMLAttributes, forwardRef, type ReactNode } from 'react';
import { cn } from '@/lib/utils';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  hint?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, label, error, hint, id, ...props }, ref) => {
    const inputId = id || label?.toLowerCase().replace(/\s+/g, '-');
    return (
      <div className="w-full">
        {label && (
          <label htmlFor={inputId} className="mb-1 block text-xs font-bold text-[#202122] dark:text-[#f3f4f6]">
            {label}
          </label>
        )}
        <input
          ref={ref}
          id={inputId}
          className={cn(
            'w-full rounded-[2px] border bg-white px-2.5 py-1.5 text-sm text-[#202122] placeholder-[#72777d] transition-colors focus:border-[#0645ad] focus:outline-none disabled:cursor-not-allowed disabled:opacity-50 dark:bg-[#111827] dark:text-[#e5e7eb]',
            error ? 'border-[#d33]' : 'border-[#a2a9b1] dark:border-[#374151]',
            className,
          )}
          {...props}
        />
        {error && <p className="mt-1 text-xs text-[#d33]">{error}</p>}
        {hint && !error && <p className="mt-1 text-xs text-[#72777d]">{hint}</p>}
      </div>
    );
  },
);
Input.displayName = 'Input';

interface TextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
}

export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ className, label, error, id, ...props }, ref) => {
    const inputId = id || label?.toLowerCase().replace(/\s+/g, '-');
    return (
      <div className="w-full">
        {label && (
          <label htmlFor={inputId} className="mb-1 block text-xs font-bold text-[#202122] dark:text-[#f3f4f6]">
            {label}
          </label>
        )}
        <textarea
          ref={ref}
          id={inputId}
          className={cn(
            'w-full rounded-[2px] border bg-white px-2.5 py-1.5 text-sm text-[#202122] placeholder-[#72777d] transition-colors focus:border-[#0645ad] focus:outline-none disabled:cursor-not-allowed disabled:opacity-50 dark:bg-[#111827] dark:text-[#e5e7eb]',
            error ? 'border-[#d33]' : 'border-[#a2a9b1] dark:border-[#374151]',
            className,
          )}
          {...props}
        />
        {error && <p className="mt-1 text-xs text-[#d33]">{error}</p>}
      </div>
    );
  },
);
Textarea.displayName = 'Textarea';

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  error?: string;
  options?: { value: string; label: string }[];
  placeholder?: string;
  children?: ReactNode;
}

export const Select = forwardRef<HTMLSelectElement, SelectProps>(
  ({ className, label, error, options, placeholder, id, children, ...props }, ref) => {
    const inputId = id || label?.toLowerCase().replace(/\s+/g, '-');
    return (
      <div className="w-full">
        {label && (
          <label htmlFor={inputId} className="mb-1 block text-xs font-bold text-[#202122] dark:text-[#f3f4f6]">
            {label}
          </label>
        )}
        <select
          ref={ref}
          id={inputId}
          className={cn(
            'w-full rounded-[2px] border bg-white px-2.5 py-1.5 text-sm text-[#202122] transition-colors focus:border-[#0645ad] focus:outline-none disabled:cursor-not-allowed disabled:opacity-50 dark:bg-[#111827] dark:text-[#e5e7eb]',
            error ? 'border-[#d33]' : 'border-[#a2a9b1] dark:border-[#374151]',
            className,
          )}
          {...props}
        >
          {placeholder && <option value="">{placeholder}</option>}
          {options && options.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
          {children}
        </select>
        {error && <p className="mt-1 text-xs text-[#d33]">{error}</p>}
      </div>
    );
  },
);
Select.displayName = 'Select';

export function FormField({ children }: { children: ReactNode }) {
  return <div className="space-y-3">{children}</div>;
}
