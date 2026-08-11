// ============================================================================
// File: frontend/src/services/api.js
// Role: Centralized API client — axios instance, JWT storage + refresh,
//       and every backend endpoint (auth, mentalhealth, media, modules).
// ============================================================================

import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";
const ACCESS_TOKEN_KEY = "mb_access_token";
const REFRESH_TOKEN_KEY = "mb_refresh_token";

export const tokenStore = {
  getAccess: () => localStorage.getItem(ACCESS_TOKEN_KEY),
  getRefresh: () => localStorage.getItem(REFRESH_TOKEN_KEY),
  set: (access, refresh) => {
    if (access) localStorage.setItem(ACCESS_TOKEN_KEY, access);
    if (refresh) localStorage.setItem(REFRESH_TOKEN_KEY, refresh);
  },
  clear: () => {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
  },
};

const client = axios.create({ baseURL: BASE_URL });

client.interceptors.request.use((config) => {
  const token = tokenStore.getAccess();
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Silent-refresh on 401, single retry, avoids infinite loops.
let refreshInFlight = null;

client.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;
    const refresh = tokenStore.getRefresh();

    if (error.response?.status === 401 && refresh && !original._retried) {
      original._retried = true;
      try {
        refreshInFlight =
          refreshInFlight ||
          axios.post(`${BASE_URL}/auth/token/refresh/`, { refresh });
        const { data } = await refreshInFlight;
        tokenStore.set(data.access, null);
        original.headers.Authorization = `Bearer ${data.access}`;
        return client(original);
      } catch (refreshError) {
        tokenStore.clear();
        window.location.href = "/login";
        return Promise.reject(refreshError);
      } finally {
        refreshInFlight = null;
      }
    }
    return Promise.reject(error);
  }
);

// ---------------------------------------------------------------------------
// Auth
// ---------------------------------------------------------------------------
export const authApi = {
  register: (payload) => client.post("/auth/registration/", payload).then((r) => r.data),
  login: (payload) => client.post("/auth/login/", payload).then((r) => r.data),
  logout: () => client.post("/auth/logout/").then((r) => r.data),
  loginWithGoogle: (idToken) =>
    client.post("/auth/google/", { access_token: idToken }).then((r) => r.data),
  me: () => client.get("/auth/user/").then((r) => r.data),
};

// ---------------------------------------------------------------------------
// Mental health module (V1's only module — others register the same shape)
// ---------------------------------------------------------------------------
export const mentalHealthApi = {
  listSessions: () =>
    client.get("/modules/mental-health/sessions/").then((r) => r.data),

  getSession: (sessionId) =>
    client.get(`/modules/mental-health/sessions/${sessionId}/`).then((r) => r.data),

  deleteSession: (sessionId) =>
    client.delete(`/modules/mental-health/sessions/${sessionId}/`).then((r) => r.data),

  sendMessage: ({ sessionId, content, image }) => {
    const form = new FormData();
    if (sessionId) form.append("session_id", sessionId);
    if (content) form.append("content", content);
    if (image) form.append("image", image);

    return client
      .post("/modules/mental-health/message/", form, {
        headers: { "Content-Type": "multipart/form-data" },
      })
      .then((r) => r.data);
  },
};

// ---------------------------------------------------------------------------
// Media (image generation)
// ---------------------------------------------------------------------------
export const mediaApi = {
  generateImage: (prompt) =>
    client.post("/media/generate/", { prompt }).then((r) => r.data),
};

// ---------------------------------------------------------------------------
// Modules registry (for future modules beyond mental health)
// ---------------------------------------------------------------------------
export const modulesApi = {
  list: () => client.get("/modules/").then((r) => r.data),
};

export default client;