import type { LoginRequest, TokenResponse, User } from '../types/auth'
import { apiRequest } from './api'

export async function login(credentials: LoginRequest): Promise<TokenResponse> {
  return apiRequest<TokenResponse>('/auth/login', {
    method: 'POST',
    body: JSON.stringify(credentials),
  })
}

export async function getCurrentUser(): Promise<User> {
  return apiRequest<User>('/auth/me')
}

export function logout(): void {
  localStorage.removeItem('access_token')
}

export function getStoredToken(): string | null {
  return localStorage.getItem('access_token')
}

export function setStoredToken(token: string): void {
  localStorage.setItem('access_token', token)
}
