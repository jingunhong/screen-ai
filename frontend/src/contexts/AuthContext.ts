import { createContext } from 'react'
import type { LoginRequest, AuthState } from '../types/auth'

export interface AuthContextType extends AuthState {
  login: (credentials: LoginRequest) => Promise<void>
  logout: () => void
}

export const AuthContext = createContext<AuthContextType | null>(null)
