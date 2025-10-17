import { apiFetch } from "./utils";

export type User = {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  role: "client" | "admin";
};

export type TokenResponse = {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: User;
};

export async function signup(data: {
  firstName: string;
  lastName: string;
  email: string;
  password: string;
}) {
  const body = new URLSearchParams();
  body.set("firstName", data.firstName);
  body.set("lastName", data.lastName);
  body.set("email", data.email);
  body.set("password", data.password);
  return apiFetch<{ message: string; user: User }>(`/api/auth/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
  });
}

export async function login(data: {
  email: string;
  password: string;
}): Promise<TokenResponse> {
  const body = new URLSearchParams();
  body.set("email", data.email);
  body.set("password", data.password);
  return apiFetch<TokenResponse>(`/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
  });
}

export async function me(token: string) {
  return apiFetch<User>(`/api/auth/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export type ApiService = {
  id: number;
  service_name: string;
  service_description: string | null;
  is_active: boolean;
};
export async function getServices() {
  return apiFetch<ApiService[]>(`/api/services`);
}

export type ApiRequest = {
  id: string;
  service: { id: number; service_name: string };
  status: "pending" | "approved" | "rejected" | "completed";
  request_date: string;
  notes: string | null;
  admin_notes: string | null;
  updated_at: string;
};

export async function createRequest(
  token: string,
  service_id: number,
  notes?: string
) {
  const params = new URLSearchParams();
  params.set("service_id", String(service_id));
  if (notes) params.set("notes", notes);
  return apiFetch<{ id: string; status: string }>(`/api/requests`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      Authorization: `Bearer ${token}`,
    },
    body: params,
  });
}

export async function myRequests(token: string) {
  return apiFetch<ApiRequest[]>(`/api/requests/my-requests`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function adminRequests(token: string, status?: string) {
  const q = status ? `?status=${encodeURIComponent(status)}` : "";
  return apiFetch<any[]>(`/api/admin/requests${q}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function adminUpdateRequest(
  token: string,
  id: string,
  status: string,
  admin_notes?: string
) {
  const params = new URLSearchParams();
  params.set("status", status);
  if (admin_notes) params.set("admin_notes", admin_notes);
  return apiFetch<{ id: string; status: string }>(`/api/admin/requests/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      Authorization: `Bearer ${token}`,
    },
    body: params,
  });
}
