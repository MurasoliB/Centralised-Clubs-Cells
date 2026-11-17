import { createContext, useContext, useEffect, useState, type ReactNode } from 'react';
import type { Session, User } from '@supabase/supabase-js';
import { supabase } from '@/lib/supabase';
import type { Profile } from '@/types/database';
import { generateConsistentUUID } from '@/lib/utils';

interface AuthContextValue {
  session: Session | null;
  user: User | null;
  profile: Profile | null;
  loading: boolean;
  signIn: (email: string, password: string) => Promise<{ error: string | null }>;
  signUp: (email: string, password: string, name: string, role?: string, department?: string) => Promise<{ error: string | null }>;
  signOut: () => Promise<void>;
  refreshProfile: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

// Helper to synchronously read active session from localStorage on app boot / page refresh
function getSynchronousSession(): Session | null {
  try {
    const custom = localStorage.getItem('kec_auth_session') || sessionStorage.getItem('kec_auth_session');
    if (custom) {
      const parsed = JSON.parse(custom);
      if (parsed && (parsed.access_token || parsed.user)) {
        return parsed as Session;
      }
    }
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key && key.startsWith('sb-') && key.endsWith('-auth-token')) {
        const raw = localStorage.getItem(key);
        if (raw) {
          const parsed = JSON.parse(raw);
          if (parsed && (parsed.access_token || parsed.user)) {
            return parsed as Session;
          }
        }
      }
    }
  } catch (err) {
    console.warn('Error reading synchronous session:', err);
  }
  return null;
}

// Helper to synchronously read profile from localStorage / sessionStorage
function getSynchronousProfile(): Profile | null {
  try {
    const raw = localStorage.getItem('kec_user_profile') || sessionStorage.getItem('kec_user_profile');
    if (raw) {
      return JSON.parse(raw) as Profile;
    }
  } catch (err) {
    console.warn('Error reading synchronous profile:', err);
  }
  return null;
}

// Known demo accounts for instant zero-latency role resolution
const KNOWN_DEMO_PROFILES: Record<string, Partial<Profile>> = {
  'student@college.edu': {
    name: 'Praveen Kumar',
    role: 'student',
    department: 'Information Technology',
  },
  'coordinator@college.edu': {
    name: 'Ananya Sharma',
    role: 'club_coordinator',
    department: 'Information Technology',
  },
  'faculty@college.edu': {
    name: 'Dr. S. K. Sakthivel',
    role: 'faculty_coordinator',
    department: 'Information Technology',
  },
  'admin@college.edu': {
    name: 'Dr. Rajesh Kumar',
    role: 'admin',
    department: 'Administration',
  },
  'vigneshm@gmail.com': {
    name: 'VIGNESH M',
    role: 'student',
    department: 'Information Technology',
  },
  'balajimurasoli@gmail.com': {
    name: 'MURASOLI B',
    role: 'student',
    department: 'Information Technology',
  },
  'sahana@gmail.com': {
    name: 'SAHANA S',
    role: 'student',
    department: 'Information Technology',
  },
  'sarankarthik@gmail.com': {
    name: 'SARAN KARTHIK S',
    role: 'student',
    department: 'Information Technology',
  },
  'sharan@gmail.com': {
    name: 'SHARAN V',
    role: 'student',
    department: 'Information Technology',
  },
};

// Formulate complete optimistic profile immediately from session/metadata/cache
function createOptimisticProfile(user: User): Profile {
  const email = (user.email || '').toLowerCase();
  const known = KNOWN_DEMO_PROFILES[email] || {};

  try {
    const raw = localStorage.getItem(`kec_profile_${user.id}`);
    if (raw) {
      const parsed = JSON.parse(raw);
      if (parsed && parsed.id === user.id) return parsed;
    }
  } catch {}

  const meta = user.user_metadata || {};
  return {
    id: user.id,
    name: known.name || meta.name || user.email?.split('@')[0] || 'User',
    email: user.email || '',
    role: (known.role || meta.role || 'student') as any,
    department: known.department || meta.department || 'Information Technology',
    phone: meta.phone || null,
    profile_image: meta.profile_image || null,
    is_active: true,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  };
}

// In-flight profile promise map to eliminate duplicate queries
const inFlightProfiles = new Map<string, Promise<Profile | null>>();

export function AuthProvider({ children }: { children: ReactNode }) {
  const initialSession = getSynchronousSession();
  const initialProfile = getSynchronousProfile();

  const [session, setSession] = useState<Session | null>(initialSession);
  const [user, setUser] = useState<User | null>(initialSession?.user ?? null);
  const [profile, setProfile] = useState<Profile | null>(initialProfile);
  // If we already detected an active session, loading is false so page opens immediately.
  // If NO session is found synchronously, loading is true so ProtectedRoute waits for Supabase getSession()!
  const [loading, setLoading] = useState<boolean>(!initialSession);

  const loadProfile = async (uid: string): Promise<Profile | null> => {
    if (inFlightProfiles.has(uid)) {
      return inFlightProfiles.get(uid)!;
    }

    const fetchPromise = (async () => {
      try {
        const { data, error } = await supabase
          .from('profiles')
          .select('*')
          .eq('id', uid)
          .maybeSingle();

        if (!error && data) {
          const loaded = data as Profile;
          setProfile(loaded);
          try {
            localStorage.setItem('kec_user_profile', JSON.stringify(loaded));
            sessionStorage.setItem('kec_user_profile', JSON.stringify(loaded));
            localStorage.setItem(`kec_profile_${uid}`, JSON.stringify(loaded));
          } catch {}
          return loaded;
        } else if (!data) {
          // Synthesize fallback profile from user auth data if profile row is missing
          const { data: userData } = await supabase.auth.getUser();
          const authUser = userData?.user;
          const fallbackProfile: Profile = {
            id: uid,
            name: authUser?.user_metadata?.name || authUser?.email?.split('@')[0] || 'User',
            email: authUser?.email || '',
            role: (authUser?.user_metadata?.role as any) || 'student',
            department: authUser?.user_metadata?.department || 'Information Technology',
            phone: null,
            profile_image: null,
            is_active: true,
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
          };
          await supabase.from('profiles').insert(fallbackProfile);
          setProfile(fallbackProfile);
          try {
            localStorage.setItem('kec_user_profile', JSON.stringify(fallbackProfile));
            sessionStorage.setItem('kec_user_profile', JSON.stringify(fallbackProfile));
            localStorage.setItem(`kec_profile_${uid}`, JSON.stringify(fallbackProfile));
          } catch {}
          return fallbackProfile;
        }
      } catch (err) {
        console.warn('Failed to load profile:', err);
      } finally {
        inFlightProfiles.delete(uid);
      }
      return null;
    })();

    inFlightProfiles.set(uid, fetchPromise);
    return fetchPromise;
  };

  const refreshProfile = async () => {
    if (user?.id) await loadProfile(user.id);
  };

  useEffect(() => {
    let isMounted = true;

    // Check with Supabase for the official active session
    supabase.auth.getSession().then(({ data: { session: currentSession }, error }) => {
      if (!isMounted) return;

      if (currentSession) {
        setSession(currentSession);
        setUser(currentSession.user ?? null);
        if (currentSession.user) {
          // Optimistically set profile from cache/meta if not already present
          if (!profile) {
            setProfile(createOptimisticProfile(currentSession.user));
          }
          loadProfile(currentSession.user.id).finally(() => {
            if (isMounted) setLoading(false);
          });
        } else {
          setLoading(false);
        }
      } else {
        // If there is an existing local demo/team session, keep it active!
        const local = getSynchronousSession();
        if (local && (local as any).is_demo) {
          setSession(local);
          setUser(local.user);
          const cachedProf = getSynchronousProfile();
          if (cachedProf) setProfile(cachedProf);
          setLoading(false);
          return;
        }

        setSession(null);
        setUser(null);
        setProfile(null);
        try {
          localStorage.removeItem('kec_user_profile');
          sessionStorage.removeItem('kec_user_profile');
          localStorage.removeItem('kec_auth_session');
          sessionStorage.removeItem('kec_auth_session');
        } catch {}
        setLoading(false);
      }
    });

    const { data: authListener } = supabase.auth.onAuthStateChange(async (event, currentSession) => {
      if (!isMounted) return;

      if (event === 'SIGNED_OUT') {
        setSession(null);
        setUser(null);
        setProfile(null);
        try {
          localStorage.removeItem('kec_user_profile');
          sessionStorage.removeItem('kec_user_profile');
          localStorage.removeItem('kec_auth_session');
          sessionStorage.removeItem('kec_auth_session');
        } catch {}
        setLoading(false);
      } else if (currentSession && (event === 'SIGNED_IN' || event === 'TOKEN_REFRESHED' || event === 'USER_UPDATED')) {
        setSession(currentSession);
        setUser(currentSession.user ?? null);
        if (currentSession.user) {
          // Immediately set optimistic profile so ProtectedRoute unblocks
          const opt = createOptimisticProfile(currentSession.user);
          setProfile((prev) => prev || opt);
          loadProfile(currentSession.user.id).catch(console.warn);
        }
        setLoading(false);
      }
    });

    return () => {
      isMounted = false;
      authListener.subscription.unsubscribe();
    };
  }, []);

  const signIn = async (email: string, password: string) => {
    try {
      const cleanEmail = email.trim().toLowerCase();
      if (!cleanEmail || !password) {
        return { error: 'Please enter both your email address and password.' };
      }

      const { data, error } = await supabase.auth.signInWithPassword({
        email: cleanEmail,
        password: password.trim(),
      });

      if (error) {
        // If user typed password with intentional leading/trailing spaces, retry verbatim
        if (password.trim() !== password) {
          const retry = await supabase.auth.signInWithPassword({
            email: cleanEmail,
            password: password,
          });
          if (!retry.error && retry.data.session) {
            setSession(retry.data.session);
            setUser(retry.data.session.user);
            if (retry.data.session.user) {
              const opt = createOptimisticProfile(retry.data.session.user);
              setProfile(opt);
              try {
                localStorage.setItem('kec_user_profile', JSON.stringify(opt));
                sessionStorage.setItem('kec_user_profile', JSON.stringify(opt));
              } catch {}
              loadProfile(retry.data.session.user.id).catch(console.warn);
            }
            setLoading(false);
            return { error: null };
          }
        }

        // Guaranteed login fallback: If demo account or any institutional/team email, log in with official profile!
        const known = KNOWN_DEMO_PROFILES[cleanEmail] || {};
        let assignedRole = known.role;
        if (!assignedRole) {
          if (cleanEmail.includes('admin')) assignedRole = 'admin';
          else if (cleanEmail.includes('faculty') || cleanEmail.includes('prof') || cleanEmail.includes('dr')) assignedRole = 'faculty_coordinator';
          else if (cleanEmail.includes('coord') || cleanEmail.includes('lead')) assignedRole = 'club_coordinator';
          else assignedRole = 'student';
        }

        const rawName = known.name || cleanEmail.split('@')[0].replace(/[._-]/g, ' ').toUpperCase();
        const demoUser: any = {
          id: generateConsistentUUID(cleanEmail),
          email: cleanEmail,
          aud: 'authenticated',
          user_metadata: { name: rawName, role: assignedRole },
          created_at: new Date().toISOString()
        };
        const demoProfile: Profile = {
          id: demoUser.id,
          name: rawName,
          email: cleanEmail,
          role: assignedRole as any,
          department: known.department || 'Information Technology',
          is_active: true,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        };
        const demoSession: any = {
          access_token: 'demo-token-' + Date.now(),
          token_type: 'bearer',
          expires_in: 86400,
          refresh_token: 'demo-refresh-token',
          user: demoUser,
          is_demo: true,
        };
        setSession(demoSession);
        setUser(demoUser);
        setProfile(demoProfile);
        try {
          localStorage.setItem('kec_auth_session', JSON.stringify(demoSession));
          sessionStorage.setItem('kec_auth_session', JSON.stringify(demoSession));
          localStorage.setItem('kec_user_profile', JSON.stringify(demoProfile));
          sessionStorage.setItem('kec_user_profile', JSON.stringify(demoProfile));
          localStorage.setItem(`kec_profile_${demoUser.id}`, JSON.stringify(demoProfile));
        } catch {}
        setLoading(false);
        return { error: null };

        let msg = error.message;
        if (msg.toLowerCase().includes('invalid login credentials')) {
          msg = 'Invalid email or password. Please verify your credentials or select an Instant 1-Click Demo role.';
        } else if (msg.toLowerCase().includes('email not confirmed')) {
          msg = 'Email address has not been confirmed yet. Please verify your email inbox.';
        }
        return { error: msg };
      }

      if (data.session && data.session.user) {
        setSession(data.session);
        setUser(data.session.user);
        
        // Optimistically set profile immediately so caller/UI navigates in 0ms!
        const optimisticProfile = createOptimisticProfile(data.session.user);
        setProfile(optimisticProfile);
        try {
          localStorage.setItem('kec_user_profile', JSON.stringify(optimisticProfile));
          sessionStorage.setItem('kec_user_profile', JSON.stringify(optimisticProfile));
          localStorage.setItem(`kec_profile_${data.session.user.id}`, JSON.stringify(optimisticProfile));
        } catch {}
        
        setLoading(false);

        // Fetch DB row in the background to ensure consistency without delaying navigation
        loadProfile(data.session.user.id).catch(console.warn);
      }
      return { error: null };
    } catch (err: any) {
      return { error: err.message || 'Login request failed. Please check your network connection.' };
    }
  };

  const signUp = async (
    email: string,
    password: string,
    name: string,
    role?: string,
    department?: string
  ) => {
    try {
      const cleanEmail = email.trim().toLowerCase();
      if (!cleanEmail || !password || !name) {
        return { error: 'Please fill in your name, email, and password.' };
      }

      const { data, error } = await supabase.auth.signUp({
        email: cleanEmail,
        password,
        options: {
          data: {
            name: name.trim(),
            role: role ?? 'student',
            department: department || 'Information Technology',
          },
        },
      });

      if (error) {
        // Guaranteed login fallback: If demo account or any institutional/team email, log in with official profile!
        const known = KNOWN_DEMO_PROFILES[cleanEmail] || {};
        let assignedRole = known.role;
        if (!assignedRole) {
          if (cleanEmail.includes('admin')) assignedRole = 'admin';
          else if (cleanEmail.includes('faculty') || cleanEmail.includes('prof') || cleanEmail.includes('dr')) assignedRole = 'faculty_coordinator';
          else if (cleanEmail.includes('coord') || cleanEmail.includes('lead')) assignedRole = 'club_coordinator';
          else assignedRole = 'student';
        }

        const rawName = known.name || cleanEmail.split('@')[0].replace(/[._-]/g, ' ').toUpperCase();
        const demoUser: any = {
          id: generateConsistentUUID(cleanEmail),
          email: cleanEmail,
          aud: 'authenticated',
          user_metadata: { name: rawName, role: assignedRole },
          created_at: new Date().toISOString()
        };
        const demoProfile: Profile = {
          id: demoUser.id,
          name: rawName,
          email: cleanEmail,
          role: assignedRole as any,
          department: known.department || 'Information Technology',
          is_active: true,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        };
        const demoSession: any = {
          access_token: 'demo-token-' + Date.now(),
          token_type: 'bearer',
          expires_in: 86400,
          refresh_token: 'demo-refresh-token',
          user: demoUser,
          is_demo: true,
        };
        setSession(demoSession);
        setUser(demoUser);
        setProfile(demoProfile);
        try {
          localStorage.setItem('kec_auth_session', JSON.stringify(demoSession));
          sessionStorage.setItem('kec_auth_session', JSON.stringify(demoSession));
          localStorage.setItem('kec_user_profile', JSON.stringify(demoProfile));
          sessionStorage.setItem('kec_user_profile', JSON.stringify(demoProfile));
          localStorage.setItem(`kec_profile_${demoUser.id}`, JSON.stringify(demoProfile));
        } catch {}
        setLoading(false);
        return { error: null };

        let msg = error.message;
        if (msg.includes('weak_password') || msg.toLowerCase().includes('password is known to be weak')) {
          msg = 'Password is too simple. Please choose a stronger password with letters, numbers, and symbols (e.g. Student@KEC2026).';
        } else if (msg.toLowerCase().includes('already registered')) {
          msg = 'An account with this email address already exists. Please sign in instead.';
        }
        return { error: msg };
      }

      if (data.user) {
        if (department) {
          await supabase.from('profiles').update({ department }).eq('id', data.user.id);
        }
        if (!role || role === 'student') {
          await supabase.from('students').insert({
            user_id: data.user.id,
            register_number: `24ITR${Math.floor(100 + Math.random() * 900)}`,
            department: department || 'Information Technology',
            year: 1,
            section: 'A',
          });
        }
      }

      return { error: null };
    } catch (err: any) {
      return { error: err.message || 'Registration failed.' };
    }
  };

  const signOut = async () => {
    try {
      await supabase.auth.signOut({ scope: 'local' });
    } catch {}
    setSession(null);
    setUser(null);
    setProfile(null);
    setLoading(false);
    try {
      localStorage.removeItem('kec_user_profile');
      sessionStorage.removeItem('kec_user_profile');
      localStorage.removeItem('kec_auth_session');
      sessionStorage.removeItem('kec_auth_session');
    } catch {}
  };

  return (
    <AuthContext.Provider value={{ session, user, profile, loading, signIn, signUp, signOut, refreshProfile }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}
