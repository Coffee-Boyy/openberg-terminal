import { create } from 'zustand';

const SESSION_KEY = 'openberg-auth-session';
const DEMO_USERS_KEY = 'openberg-demo-users';

type User = {
  email: string;
  name: string;
  avatar?: string;
};

interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  login: (email: string, _password: string) => void;
  logout: () => void;
  signup: (email: string, name: string, _password: string) => void;
}

function initSession() {
  try {
    const session = localStorage.getItem(SESSION_KEY);
    if (session) {
      const usersRaw = localStorage.getItem(DEMO_USERS_KEY) || '[]';
      const users: Array<Record<string, any> & User> = JSON.parse(usersRaw);
      const saved = JSON.parse(session);
      const found = users.find((u: Record<string, any> & User) => u.email === saved.email);
      if (found) return found;
    }
  } catch {
    // ignore corrupted data
  }
  return null;
}

export const useAuth = create<AuthState>((set) => ({
  isAuthenticated: false,
  user: null,
  login: (email: string, _password: string) => {
    // Demo mode: accept any email/password combo
    const usersRaw = localStorage.getItem(DEMO_USERS_KEY) || '[]';
    const users: Array<Record<string, any> & User> = JSON.parse(usersRaw);
    const existing = users.find((u: Record<string, any> & User) => u.email === email);
    if (!existing) {
      // Auto-create on login for demo convenience
      const user: User = { email, name: email.split('@')[0] };
      users.push(user);
      localStorage.setItem(DEMO_USERS_KEY, JSON.stringify(users));
      localStorage.setItem(SESSION_KEY, JSON.stringify(user));
      set({ isAuthenticated: true, user });
    } else {
      localStorage.setItem(SESSION_KEY, JSON.stringify(existing));
      set({ isAuthenticated: true, user: existing });
    }
  },
  logout: () => {
    localStorage.removeItem(SESSION_KEY);
    set({ isAuthenticated: false, user: null });
  },
  signup: (email: string, name: string, _password: string) => {
    // Demo mode: accept any credentials
    const usersRaw = localStorage.getItem(DEMO_USERS_KEY) || '[]';
    const users: Array<Record<string, any> & User> = JSON.parse(usersRaw);
    if (users.find((u: Record<string, any> & User) => u.email === email)) {
      // Email already exists, just log them in
      const existing = users.find((u: Record<string, any> & User) => u.email === email);
      localStorage.setItem(SESSION_KEY, JSON.stringify(existing));
      set({ isAuthenticated: true, user: existing });
      return;
    }
    const user: User = { email, name, avatar: `https://ui-avatars.com/api/?name=${encodeURIComponent(name)}` };
    users.push(user);
    localStorage.setItem(DEMO_USERS_KEY, JSON.stringify(users));
    localStorage.setItem(SESSION_KEY, JSON.stringify(user));
    set({ isAuthenticated: true, user });
  },
}));

// Restore session on mount
const session = initSession();
if (session) {
  useAuth.setState({ isAuthenticated: true, user: session });
}
