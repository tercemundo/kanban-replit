import { useState, useEffect, useCallback, createContext, useContext, ReactNode } from "react";
import { postLogin, type AuthUser } from "@workspace/api-client-react";

export type { AuthUser };

interface AuthState {
  user: AuthUser | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  loginError: string | null;
  login: (username?: string, password?: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthState | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [loginError, setLoginError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    fetch("/api/auth/user", { credentials: "include" })
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json() as Promise<{ user: AuthUser | null }>;
      })
      .then((data) => {
        if (!cancelled) {
          setUser(data.user ?? null);
          setIsLoading(false);
        }
      })
      .catch(() => {
        if (!cancelled) {
          setUser(null);
          setIsLoading(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, []);

  const login = useCallback(async (username?: string, password?: string) => {
    setLoginError(null);
    if (!username || !password) {
      const baseUrl = (import.meta as any).env?.BASE_URL || "/";
      const base = baseUrl.replace(/\/+$/, "") || "/";
      window.location.href = `/api/auth/login/browser?returnTo=${encodeURIComponent(base)}&username=${username || 'user'}`;
      return;
    }

    try {
      const data = await postLogin({ username, password });
      setUser(data.user);
    } catch (err: any) {
      setLoginError("Credenciales inválidas. Intente de nuevo.");
      throw err;
    }
  }, []);

  const logout = useCallback(() => {
    window.location.href = "/api/auth/logout/browser";
  }, []);

  const value: AuthState = {
    user,
    isLoading,
    isAuthenticated: !!user,
    loginError,
    login,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthState {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}

