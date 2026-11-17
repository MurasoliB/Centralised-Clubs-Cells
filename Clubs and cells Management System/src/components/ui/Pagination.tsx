import { ChevronLeft, ChevronRight } from 'lucide-react';
import { cn } from '@/lib/utils';

interface PaginationProps {
  page: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}

export function Pagination({ page, totalPages, onPageChange }: PaginationProps) {
  if (totalPages <= 1) return null;

  return (
    <div className="flex items-center justify-between border-t border-[#a2a9b1] px-4 py-2.5 text-xs text-[#54595d] dark:border-[#374151] dark:text-[#9ca3af]">
      <p>
        Showing page <span className="font-bold text-[#202122] dark:text-[#f3f4f6]">{page}</span> of <span className="font-bold text-[#202122] dark:text-[#f3f4f6]">{totalPages}</span>
      </p>
      <div className="flex items-center gap-1.5">
        <button
          onClick={() => onPageChange(page - 1)}
          disabled={page <= 1}
          className={cn(
            'inline-flex items-center gap-1 rounded-[2px] border px-2 py-1 text-xs transition-colors',
            page <= 1
              ? 'cursor-not-allowed border-[#c8ccd1] text-[#c8ccd1] dark:border-[#374151] dark:text-[#4b5563]'
              : 'border-[#a2a9b1] bg-[#f8f9fa] text-[#0645ad] hover:bg-white hover:underline dark:border-[#374151] dark:bg-[#1f2937] dark:text-[#6b9eff]',
          )}
        >
          <ChevronLeft className="h-3 w-3" /> Previous
        </button>
        <button
          onClick={() => onPageChange(page + 1)}
          disabled={page >= totalPages}
          className={cn(
            'inline-flex items-center gap-1 rounded-[2px] border px-2 py-1 text-xs transition-colors',
            page >= totalPages
              ? 'cursor-not-allowed border-[#c8ccd1] text-[#c8ccd1] dark:border-[#374151] dark:text-[#4b5563]'
              : 'border-[#a2a9b1] bg-[#f8f9fa] text-[#0645ad] hover:bg-white hover:underline dark:border-[#374151] dark:bg-[#1f2937] dark:text-[#6b9eff]',
          )}
        >
          Next <ChevronRight className="h-3 w-3" />
        </button>
      </div>
    </div>
  );
}
