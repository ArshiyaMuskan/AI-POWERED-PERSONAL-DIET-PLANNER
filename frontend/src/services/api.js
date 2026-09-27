const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export function getToken() {
  return localStorage.getItem("token");
}

export function setToken(token) {
  localStorage.setItem("token", token);
}

export function clearToken() {
  localStorage.removeItem("token");
}

async function request(path, options = {}) {
  const headers = new Headers(options.headers || {});
  const token = getToken();

  if (token) headers.set("Authorization", `Bearer ${token}`);

  let body = options.body;
  if (body && !(body instanceof FormData)) {
    headers.set("Content-Type", "application/json");
    body = JSON.stringify(body);
  }

  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers,
    body,
  });

  if (!response.ok) {
    let message = "Request failed";
    try {
      const data = await response.json();
      message = data.detail || message;
    } catch {}
    throw new Error(message);
  }

  if (response.status === 204) return null;
  return response.json();
}

export const api = {
  register: (data) => request("/api/auth/register", { method: "POST", body: data }),
  login: (data) => request("/api/auth/login", { method: "POST", body: data }),
  getProfile: () => request("/api/profile"),
  updateProfile: (data) => request("/api/profile", { method: "PUT", body: data }),
  generatePlan: () => request("/api/plans/generate", { method: "POST" }),
  getPlans: () => request("/api/plans"),
  deletePlan: (id) => request(`/api/plans/${id}`, { method: "DELETE" }),
  getFiles: () => request("/api/files"),
  uploadFile: (file) => {
    const form = new FormData();
    form.append("file", file);
    return request("/api/files", { method: "POST", body: form });
  },
  deleteFile: (id) => request(`/api/files/${id}`, { method: "DELETE" }),
  downloadUrl: (id) => `${API_URL}/api/files/${id}/download`,
};
