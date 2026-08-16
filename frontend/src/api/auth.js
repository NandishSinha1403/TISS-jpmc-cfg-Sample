import { apiFetch } from "./client";

export function signup({ email, password, fullName }) {
  return apiFetch("/auth/signup", {
    method: "POST",
    body: JSON.stringify({ email, password, full_name: fullName }),
  });
}

export function login({ email, password }) {
  const body = new URLSearchParams({ username: email, password });
  return apiFetch("/auth/login", { method: "POST", body });
}

export function fetchCurrentUser() {
  return apiFetch("/auth/me");
}
