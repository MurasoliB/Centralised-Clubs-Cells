import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from '@/context/AuthContext';
import { ThemeProvider } from '@/context/ThemeContext';
import { ToastProvider } from '@/context/ToastContext';
import { ProtectedRoute } from '@/components/layout/ProtectedRoute';
import { AppLayout } from '@/components/layout/AppLayout';
import { LandingPage } from '@/pages/LandingPage';
import { LoginPage } from '@/pages/auth/LoginPage';
import { SignupPage } from '@/pages/auth/SignupPage';
import { DashboardPage } from '@/pages/DashboardPage';
import { TasksPage } from '@/pages/TasksPage';
import { StaffManagementPage } from '@/pages/StaffManagementPage';
import { StudentsPage } from '@/pages/StudentsPage';
import { OrganizationsPage } from '@/pages/OrganizationsPage';
import { OrganizationDetailsPage } from '@/pages/OrganizationDetailsPage';
import { MembershipsPage } from '@/pages/MembershipsPage';
import { EventsPage } from '@/pages/EventsPage';
import { EventDetailsPage } from '@/pages/EventDetailsPage';
import { AttendancePage } from '@/pages/AttendancePage';
import { AchievementsPage } from '@/pages/AchievementsPage';
import { AnnouncementsPage } from '@/pages/AnnouncementsPage';
import { NotificationsPage } from '@/pages/NotificationsPage';
import { ReportsPage } from '@/pages/ReportsPage';
import { ProfilePage } from '@/pages/ProfilePage';
import { SettingsPage } from '@/pages/SettingsPage';
import { AuditLogsPage } from '@/pages/AuditLogsPage';
import { NotFoundPage, ForbiddenPage } from '@/pages/NotFoundPage';

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <ToastProvider>
          <BrowserRouter>
            <Routes>
              {/* Public Landing Page */}
              <Route path="/" element={<LandingPage />} />

              <Route path="/login" element={<LoginPage />} />
              <Route path="/signup" element={<SignupPage />} />

              <Route
                path="/dashboard"
                element={
                  <ProtectedRoute>
                    <AppLayout>
                      <DashboardPage />
                    </AppLayout>
                  </ProtectedRoute>
                }
              />

              <Route
                path="/tasks"
                element={
                  <ProtectedRoute roles={['admin', 'faculty_coordinator', 'club_coordinator']}>
                    <AppLayout>
                      <TasksPage />
                    </AppLayout>
                  </ProtectedRoute>
                }
              />

              <Route
                path="/staff"
                element={
                  <ProtectedRoute roles={['admin', 'faculty_coordinator']}>
                    <AppLayout>
                      <StaffManagementPage />
                    </AppLayout>
                  </ProtectedRoute>
                }
              />

              <Route
                path="/students"
                element={
                  <ProtectedRoute roles={['admin', 'faculty_coordinator', 'club_coordinator']}>
                    <AppLayout>
                      <StudentsPage />
                    </AppLayout>
                  </ProtectedRoute>
                }
              />

              <Route
                path="/organizations"
                element={
                  <ProtectedRoute>
                    <AppLayout>
                      <OrganizationsPage />
                    </AppLayout>
                  </ProtectedRoute>
                }
              />

              <Route
                path="/organizations/:id"
                element={
                  <ProtectedRoute>
                    <AppLayout>
                      <OrganizationDetailsPage />
                    </AppLayout>
                  </ProtectedRoute>
                }
              />

              <Route
                path="/memberships"
                element={
                  <ProtectedRoute>
                    <AppLayout>
                      <MembershipsPage />
                    </AppLayout>
                  </ProtectedRoute>
                }
              />

              <Route
                path="/events"
                element={
                  <ProtectedRoute>
                    <AppLayout>
                      <EventsPage />
                    </AppLayout>
                  </ProtectedRoute>
                }
              />

              <Route
                path="/events/:id"
                element={
                  <ProtectedRoute>
                    <AppLayout>
                      <EventDetailsPage />
                    </AppLayout>
                  </ProtectedRoute>
                }
              />

              <Route
                path="/attendance"
                element={
                  <ProtectedRoute>
                    <AppLayout>
                      <AttendancePage />
                    </AppLayout>
                  </ProtectedRoute>
                }
              />

              <Route
                path="/achievements"
                element={
                  <ProtectedRoute>
                    <AppLayout>
                      <AchievementsPage />
                    </AppLayout>
                  </ProtectedRoute>
                }
              />

              <Route
                path="/announcements"
                element={
                  <ProtectedRoute>
                    <AppLayout>
                      <AnnouncementsPage />
                    </AppLayout>
                  </ProtectedRoute>
                }
              />

              <Route
                path="/notifications"
                element={
                  <ProtectedRoute>
                    <AppLayout>
                      <NotificationsPage />
                    </AppLayout>
                  </ProtectedRoute>
                }
              />

              <Route
                path="/reports"
                element={
                  <ProtectedRoute>
                    <AppLayout>
                      <ReportsPage />
                    </AppLayout>
                  </ProtectedRoute>
                }
              />

              <Route
                path="/profile"
                element={
                  <ProtectedRoute>
                    <AppLayout>
                      <ProfilePage />
                    </AppLayout>
                  </ProtectedRoute>
                }
              />

              <Route
                path="/settings"
                element={
                  <ProtectedRoute>
                    <AppLayout>
                      <SettingsPage />
                    </AppLayout>
                  </ProtectedRoute>
                }
              />

              <Route
                path="/audit-logs"
                element={
                  <ProtectedRoute roles={['admin']}>
                    <AppLayout>
                      <AuditLogsPage />
                    </AppLayout>
                  </ProtectedRoute>
                }
              />

              <Route path="/403" element={<ForbiddenPage />} />
              <Route path="*" element={<NotFoundPage />} />
            </Routes>
          </BrowserRouter>
        </ToastProvider>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
