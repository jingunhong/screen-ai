const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

export class ApiError extends Error {
  status: number
  statusText: string

  constructor(status: number, statusText: string, message: string) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.statusText = statusText
  }
}

export async function apiRequest<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = localStorage.getItem('access_token')

  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  }

  if (token) {
    ;(headers as Record<string, string>)['Authorization'] = `Bearer ${token}`
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  })

  if (!response.ok) {
    let errorMessage = response.statusText
    try {
      const errorData = await response.json()
      errorMessage = errorData.detail || errorMessage
    } catch {
      // Ignore JSON parse errors
    }
    throw new ApiError(response.status, response.statusText, errorMessage)
  }

  return response.json()
}
