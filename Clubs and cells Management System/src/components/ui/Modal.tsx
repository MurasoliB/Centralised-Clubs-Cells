import { type ReactNode, useEffect } from 'react';
import { X } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ModalProps {
  open: boolean;
  onClose: () => void;
  title?: string;
  description?: string;
  children: ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl';
}

const sizeClasses = {
  sm: 'max-w-md',
  md: 'max-w-lg',
  lg: 'max-w-2xl',
  xl: 'max-w-4xl',
};

export function Modal({ open, onClose, title, description, children, size = 'md' }: ModalProps) {
  useEffect(() => {
    if (open) {
      document.body.style.overflow = 'hidden';
      const handleEsc = (e: KeyboardEvent) => {
        if (e.key === 'Escape') onClose();
      };
      window.addEventListener('keydown', handleEsc);
      return () => {
        document.body.style.overflow = '';
        window.removeEventListener('keydown', handleEsc);
      };
    }
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div
        className="fixed inset-0 bg-black/40 transition-opacity"
        onClick={onClose}
      />
      <div
        className={cn(
          'relative z-10 w-full rounded-[2px] bg-white border border-[#a2a9b1] shadow-lg dark:bg-[#111827] dark:border-[#374151] max-h-[90vh] overflow-y-auto',
          sizeClasses[size],
        )}
      >
        <div className="flex items-center justify-between px-4 py-2.5 bg-[#eaecf0] border-b border-[#a2a9b1] dark:bg-[#1f2937] dark:border-[#374151]">
          <div>
            {title && <h2 className="font-serif text-base font-bold text-[#202122] dark:text-[#f3f4f6]">{title}</h2>}
            {description && <p className="text-xs text-[#54595d] dark:text-[#9ca3af]">{description}</p>}
          </div>
          <button
            onClick={onClose}
            className="rounded-[2px] p-1 text-[#54595d] hover:bg-[#c8ccd1] hover:text-[#202122] dark:text-[#9ca3af] dark:hover:bg-[#374151]"
          >
            <X className="h-4 w-4" />
          </button>
        </div>
        <div className="p-4 sm:p-5">{children}</div>
      </div>
    </div>
  );
}
