import { useState, type ReactNode } from 'react';
import { cn } from '@/lib/utils';

interface Tab {
  label: string;
  value: string;
  content: ReactNode;
}

interface TabsProps {
  tabs: Tab[];
  defaultTab?: string;
  className?: string;
}

export function Tabs({ tabs, defaultTab, className }: TabsProps) {
  const [active, setActive] = useState(defaultTab || tabs[0]?.value);

  return (
    <div className={className}>
      <div className="border-b border-[#a2a9b1] dark:border-slate-700 mb-4">
        <nav className="flex gap-1 overflow-x-auto -mb-px">
          {tabs.map((tab) => {
            const isActive = active === tab.value;
            return (
              <button
                key={tab.value}
                onClick={() => setActive(tab.value)}
                className={cn(
                  'px-3.5 py-1.5 text-xs sm:text-sm transition-all whitespace-nowrap cursor-pointer rounded-t-[2px]',
                  isActive
                    ? 'bg-white dark:bg-slate-900 border-t-2 border-t-[#0645ad] border-x border-x-[#a2a9b1] dark:border-x-slate-700 border-b border-b-white dark:border-b-slate-900 font-bold text-[#202122] dark:text-white'
                    : 'bg-[#f8f9fa] dark:bg-slate-800 border border-[#c8ccd1] dark:border-slate-700 text-[#0645ad] dark:text-[#6b9eff] hover:underline hover:bg-white dark:hover:bg-slate-750 font-medium'
                )}
              >
                {tab.label}
              </button>
            );
          })}
        </nav>
      </div>
      <div>
        {tabs.find((t) => t.value === active)?.content}
      </div>
    </div>
  );
}
