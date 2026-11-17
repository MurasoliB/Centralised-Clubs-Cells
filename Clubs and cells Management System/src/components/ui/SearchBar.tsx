import { Search } from 'lucide-react';

interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
}

export function SearchBar({ value, onChange, placeholder = 'Search repository...' }: SearchBarProps) {
  return (
    <div className="relative w-full sm:w-72">
      <Search className="absolute left-2.5 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-[#72777d]" />
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="w-full rounded-[2px] border border-[#a2a9b1] bg-white py-1.5 pl-8 pr-2.5 text-xs text-[#202122] placeholder-[#72777d] focus:border-[#0645ad] focus:outline-none dark:border-[#374151] dark:bg-[#111827] dark:text-[#e5e7eb]"
      />
    </div>
  );
}
