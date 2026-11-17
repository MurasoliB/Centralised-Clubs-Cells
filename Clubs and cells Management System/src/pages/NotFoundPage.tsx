import { Link } from 'react-router-dom';
import { Home, ShieldAlert } from 'lucide-react';
import { Button } from '@/components/ui/Button';

export function NotFoundPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-[#f6f8fa] dark:bg-[#0b0f17] p-4 font-sans">
      <div className="max-w-md w-full text-center space-y-4 p-6 rounded-[2px] bg-white dark:bg-[#111827] border border-[#a2a9b1] dark:border-[#374151] shadow-sm">
        <h1 className="font-serif text-3xl font-bold text-[#202122] dark:text-[#f3f4f6]">
          Page Not Found (404)
        </h1>
        <p className="text-xs text-[#54595d] dark:text-[#9ca3af] leading-relaxed">
          The requested article or repository resource does not exist or has been moved under institutional archiving.
        </p>
        <div className="pt-2">
          <Link to="/dashboard" className="wiki-link text-sm font-semibold">
            ← Return to ClubHub Dashboard
          </Link>
        </div>
      </div>
    </div>
  );
}

export function ForbiddenPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-[#f6f8fa] dark:bg-[#0b0f17] p-4 font-sans">
      <div className="max-w-md w-full text-center space-y-4 p-6 rounded-[2px] bg-white dark:bg-[#111827] border border-[#a2a9b1] dark:border-[#374151] shadow-sm">
        <h1 className="font-serif text-3xl font-bold text-[#202122] dark:text-[#f3f4f6]">
          Access Restricted (403)
        </h1>
        <p className="text-xs text-[#54595d] dark:text-[#9ca3af] leading-relaxed">
          This administrative module requires authorized coordinator credentials or institutional administrative permissions.
        </p>
        <div className="pt-2">
          <Link to="/dashboard" className="wiki-link text-sm font-semibold">
            ← Return to Institutional Dashboard
          </Link>
        </div>
      </div>
    </div>
  );
}
