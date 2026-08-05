import { useEffect, useState } from 'react'

interface LoginFormProps {
  onSubmit: (email: string, password: string) => void
  isSubmitting: boolean
  error?: string
}

function LoginForm({ onSubmit, isSubmitting, error }: LoginFormProps) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [visibleError, setVisibleError] = useState('')

  useEffect(() => {
    if (!error) {
      setVisibleError('')
      return
    }

    setVisibleError(error)
  }, [error])

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    onSubmit(email, password)
  }

  return (
    <div className="page-shell">
      <div className="auth-card">
        <span className="page-badge">Welcome back</span>
        <h1 className="page-title">Log in to your account</h1>
        <p className="page-subtitle">Pick up where you left off and continue planning your day.</p>

        <form onSubmit={handleSubmit} className="auth-form">
          <label className="auth-field">
            <span>Email</span>
            <input
              className="auth-input"
              type="email"
              value={email}
              onChange={(e) => {
                setEmail(e.target.value)
                setVisibleError('')
              }}
              placeholder="you@example.com"
              required
            />
          </label>
          <label className="auth-field">
            <span>Password</span>
            <input
              className="auth-input"
              type="password"
              value={password}
              onChange={(e) => {
                setPassword(e.target.value)
                setVisibleError('')
              }}
              placeholder="Enter your password"
              required
            />
          </label>
          <button type="submit" disabled={isSubmitting} className="auth-button">
            {isSubmitting ? 'Logging in...' : 'Log in'}
          </button>
          {visibleError && <p className="auth-error" role="alert">{visibleError}</p>}
          <p className="page-subtitle" style={{ fontSize: '0.95rem' }}>
            New here? <a className="auth-link" href="/register">Create an account</a>
          </p>
        </form>
      </div>
    </div>
  )
}

export default LoginForm