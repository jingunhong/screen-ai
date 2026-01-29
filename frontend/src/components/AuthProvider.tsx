import { useEffect, useState, type ReactNode } from 'react'
import type { LoginRequest, AuthState } from '../types/auth'
import { AuthContext } from '../contexts/AuthContext'
import * as authService from '../services/auth'
import { ApiError } from '../services/api'

export default function AuthProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<AuthState>({
    user: null,
    token: authService.getStoredToken(),
    isAuthenticated: false,
    isLoading: true,
  })

  useEffect(() => {
    let isMounted = true

    const initAuth = async () => {
      const token = authService.getStoredToken()
      if (!token) {
        if (isMounted) {
          setState({
            user: null,
            token: null,
            isAuthenticated: false,
            isLoading: false,
          })
        }
        return
      }

      try {
        const user = await authService.getCurrentUser()
        if (isMounted) {
          setState({
            user,
            token,
            isAuthenticated: true,
            isLoading: false,
          })
        }
      } catch (error) {
        if (error instanceof ApiError && error.status === 401) {
          authService.logout()
        }
        if (isMounted) {
          setState({
            user: null,
            token: null,
            isAuthenticated: false,
            isLoading: false,
          })
        }
      }
    }

    initAuth()

    return () => {
      isMounted = false
    }
  }, [])

  const login = async (credentials: LoginRequest) => {
    const response = await authService.login(credentials)
    authService.setStoredToken(response.access_token)

    const user = await authService.getCurrentUser()
    setState({
      user,
      token: response.access_token,
      isAuthenticated: true,
      isLoading: false,
    })
  }

  const logout = () => {
    authService.logout()
    setState({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,
    })
  }

  return <AuthContext.Provider value={{ ...state, login, logout }}>{children}</AuthContext.Provider>
}
