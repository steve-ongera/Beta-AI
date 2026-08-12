// ============================================================================
// File: frontend/src/hooks/useAuth.jsx
// Note: .jsx extension (not .js) — this file returns JSX
// (<AuthContext.Provider>), and Vite/esbuild only parse JSX syntax in
// files with a .jsx/.tsx extension. A .js file with JSX in it fails the
// dependency-scan step with "Unexpected JSX expression".
// ============================================================================

// Role: Auth context/provider — login, register, Google OAuth, logout, and
//       the current user's session state. Wraps <App/> in main.jsx.

import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { authApi, tokenStore } from "../services/api.js";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const loadUser = useCallback(async () => {
    if (!tokenStore.getAccess()) {
      setIsLoading(false);
      return;
    }
    try {
      const me = await authApi.me();
      setUser(me);
    } catch {
      tokenStore.clear();
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadUser();
  }, [loadUser]);

  const login = useCallback(async (credentials) => {
    const data = await authApi.login(credentials);
    tokenStore.set(data.access_token || data.access, data.refresh_token || data.refresh);
    await loadUser();
  }, [loadUser]);

  const register = useCallback(async (payload) => {
    const data = await authApi.register(payload);
    tokenStore.set(data.access_token || data.access, data.refresh_token || data.refresh);
    await loadUser();
  }, [loadUser]);

  const loginWithGoogle = useCallback(async (idToken) => {
    const data = await authApi.loginWithGoogle(idToken);
    tokenStore.set(data.access_token || data.access, data.refresh_token || data.refresh);
    await loadUser();
  }, [loadUser]);

  const logout = useCallback(async () => {
    try {
      await authApi.logout();
    } finally {
      tokenStore.clear();
      setUser(null);
    }
  }, []);

  const value = useMemo(
    () => ({
      user,
      isAuthenticated: Boolean(user),
      isLoading,
      login,
      register,
      loginWithGoogle,
      logout,
    }),
    [user, isLoading, login, register, loginWithGoogle, logout]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    // Allows components to render sensibly even if a provider hasn't been
    // wired yet during incremental development.
    return { user: null, isAuthenticated: false, isLoading: false };
  }
  return ctx;
}