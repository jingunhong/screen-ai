import { useState, type FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { ApiError } from '../services/api'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [rememberDevice, setRememberDevice] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError(null)
    setIsSubmitting(true)

    try {
      await login({ email, password })
      navigate('/')
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message)
      } else {
        setError('An unexpected error occurred. Please try again.')
      }
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="flex min-h-screen flex-1 flex-col lg:flex-row">
      {/* Left Panel: Visual/Context */}
      <div className="relative hidden flex-col justify-end overflow-hidden bg-slate-900 p-16 text-white lg:flex lg:w-1/2">
        {/* Background Image with Overlay */}
        <div className="absolute inset-0 z-0">
          <div
            className="h-full w-full bg-cover bg-center"
            style={{
              backgroundImage:
                "url('https://lh3.googleusercontent.com/aida-public/AB6AXuCAC4_5JlldfN_3T5J-FAwXviz3GneuIbXWPjnP5zh4FnHoasJ8bpngmG6SYZnRXjmBI9pALnuu-2u6VikZYiHyNjPa6jkzW7rYn_tE7ZSUFHxA12fHJkM2bjHwI6kxGTjISR1OhBODVCcsufbLnaWE_VSie9oxzhQ8HLFK5toyRQ987sB0YzewmU3RgMOKIdByghdflKjK3Awc45GIR0A96Y06fyZxHspey0yy4WGU_OOIuOrbZvjLJwYjtn0mqANzU83SK9k6uZs')",
            }}
          />
          <div className="absolute inset-0 bg-blue-900/80 mix-blend-multiply" />
          <div className="absolute inset-0 bg-gradient-to-t from-slate-900 via-transparent to-transparent opacity-90" />
        </div>

        {/* Branding overlay content */}
        <div className="relative z-10 max-w-xl pb-10">
          <div className="mb-6 flex items-center gap-3">
            <svg
              className="h-9 w-9 text-blue-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={1.5}
                d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23.693L5 14.5m14.8.8l1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0112 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5"
              />
            </svg>
            <span className="text-xl font-bold uppercase tracking-wide opacity-90">Screen AI</span>
          </div>
          <h1 className="mb-6 text-5xl font-bold leading-tight">
            Precision data
            <br />
            for <span className="text-blue-400">drug discovery.</span>
          </h1>
          <p className="max-w-md text-lg font-light leading-relaxed text-blue-100">
            Secure platform for high-throughput screening analysis. Manage, visualize, and analyze
            microscopy datasets with ease.
          </p>
        </div>
      </div>

      {/* Right Panel: Login Form */}
      <div className="relative flex flex-1 flex-col items-center justify-center bg-white p-6 sm:p-12 xl:p-24">
        {/* Top Right: Help/Support Link */}
        <div className="absolute right-6 top-6 sm:right-10 sm:top-10">
          <a
            className="flex items-center gap-1 text-sm font-medium text-slate-500 transition-colors hover:text-blue-600"
            href="#"
          >
            <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={1.5}
                d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9 5.25h.008v.008H12v-.008z"
              />
            </svg>
            Support
          </a>
        </div>

        <div className="flex w-full max-w-[420px] flex-col">
          {/* Mobile Branding */}
          <div className="mb-8 flex items-center gap-2 text-blue-600 lg:hidden">
            <svg className="h-8 w-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={1.5}
                d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23.693L5 14.5m14.8.8l1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0112 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5"
              />
            </svg>
            <span className="text-lg font-bold">Screen AI</span>
          </div>

          {/* Header */}
          <div className="mb-10">
            <h2 className="mb-2 text-3xl font-bold leading-tight text-slate-900">Welcome Back</h2>
            <p className="text-base text-slate-500">Sign in to access your screening data.</p>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-6 rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700">
              {error}
            </div>
          )}

          {/* Form */}
          <form className="flex flex-col gap-6" onSubmit={handleSubmit}>
            {/* Email Input */}
            <label className="flex flex-col gap-2">
              <span className="text-sm font-semibold leading-normal text-slate-900">Email</span>
              <div className="group relative">
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="flex h-14 w-full rounded-lg border border-slate-300 bg-slate-50 py-2 pl-12 pr-4 text-base font-normal text-slate-900 placeholder:text-slate-400 focus:border-blue-600 focus:ring-2 focus:ring-blue-600/20"
                  placeholder="you@example.com"
                  required
                  disabled={isSubmitting}
                />
                <svg
                  className="absolute left-4 top-[14px] h-6 w-6 text-slate-400 transition-colors group-focus-within:text-blue-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={1.5}
                    d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75"
                  />
                </svg>
              </div>
            </label>

            {/* Password Input */}
            <label className="flex flex-col gap-2">
              <span className="text-sm font-semibold leading-normal text-slate-900">Password</span>
              <div className="group relative">
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="flex h-14 w-full rounded-lg border border-slate-300 bg-slate-50 py-2 pl-12 pr-4 text-base font-normal text-slate-900 placeholder:text-slate-400 focus:border-blue-600 focus:ring-2 focus:ring-blue-600/20"
                  placeholder="Enter your password"
                  required
                  disabled={isSubmitting}
                />
                <svg
                  className="absolute left-4 top-[14px] h-6 w-6 text-slate-400 transition-colors group-focus-within:text-blue-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={1.5}
                    d="M15.75 5.25a3 3 0 013 3m3 0a6 6 0 01-7.029 5.912c-.563-.097-1.159.026-1.563.43L10.5 17.25H8.25v2.25H6v2.25H2.25v-2.818c0-.597.237-1.17.659-1.591l6.499-6.499c.404-.404.527-1 .43-1.563A6 6 0 1121.75 8.25z"
                  />
                </svg>
              </div>
            </label>

            {/* Primary Action */}
            <button
              type="submit"
              disabled={isSubmitting}
              className="mt-2 flex h-12 w-full items-center justify-center rounded-lg bg-blue-600 text-base font-bold tracking-wide text-white shadow-md transition-all hover:bg-blue-700 hover:shadow-lg focus:ring-4 focus:ring-blue-600/30 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {isSubmitting ? 'Signing in...' : 'Sign In'}
            </button>

            <div className="flex items-center justify-between px-1 text-sm">
              <label className="group flex cursor-pointer items-center gap-2">
                <input
                  type="checkbox"
                  checked={rememberDevice}
                  onChange={(e) => setRememberDevice(e.target.checked)}
                  className="h-4 w-4 rounded border-slate-300 text-blue-600 focus:ring-blue-600"
                  disabled={isSubmitting}
                />
                <span className="text-slate-500 transition-colors group-hover:text-slate-900">
                  Remember me
                </span>
              </label>
              <a className="font-medium text-blue-600 hover:text-blue-700 hover:underline" href="#">
                Forgot password?
              </a>
            </div>
          </form>

          {/* Footer */}
          <div className="mt-12 text-center">
            <p className="text-xs text-slate-400">
              v0.1.0 &bull; Screen AI &bull;{' '}
              <a className="hover:text-blue-600" href="#">
                Terms
              </a>
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
