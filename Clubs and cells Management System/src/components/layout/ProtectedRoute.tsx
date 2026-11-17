import { type ReactNode } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import type { UserRole } from '@/types/database';
import { LoadingSpinner } from '@/components/ui/EmptyState';

interface ProtectedRouteProps {
  children: ReactNode;
  roles?: UserRole[];
}

export function ProtectedRoute({ children, roles }: ProtectedRouteProps) {
  const { session, user, profile, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return <LoadingSpinner className="min-h-screen" />;
  }

  // Check if authenticated via session, user, or profile
  if (!session && !user && !profile) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // If specific roles are required, wait for profile to be available
  if (roles && !profile) {
    return <LoadingSpinner className="min-h-screen" />;
  }

  if (roles && profile && !roles.includes(profile.role)) {
    return <Navigate to="/dashboard" replace />;
  }

  return <>{children}</>;
}
