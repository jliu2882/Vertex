import { api } from "./client";

interface LoginResponse {
  access_token: string;
  token_type: string;
}

export function login(email: string, password: string) {
  return api.post<LoginResponse>("/login", { email, password });
}

export function register(email: string, username: string, password: string) {
  return api.post<LoginResponse>("/register", { email, username, password });
}
