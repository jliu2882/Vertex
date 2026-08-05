import { useState } from 'react'

interface LoginFormProps {
  onSubmit: (email: string, username: string, password: string) => void
  isSubmitting: boolean
  error?: string
}

function RegisterForm({ onSubmit, isSubmitting, error }: LoginFormProps) {
  const [email, setEmail] = useState('')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    onSubmit(email, username, password)
  }

  return (
    <div className="page-shell">
      <div className="auth-card">
        <span className="page-badge">Join today</span>
        <h1 className="page-title">Create your account</h1>
        <p className="page-subtitle">Start organizing your tasks with a clean, calming workspace.</p>

        <form onSubmit={handleSubmit} className="auth-form">
          <label className="auth-field">
            <span>Email</span>
            <input
              className="auth-input"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              required
            />
          </label>
          <label className="auth-field">
            <span>Username</span>
            <input
              className="auth-input"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Choose a username"
              required
            />
          </label>
          <label className="auth-field">
            <span>Password</span>
            <input
              className="auth-input"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Create a password"
              required
            />
          </label>
          <button type="submit" disabled={isSubmitting} className="auth-button">
            {isSubmitting ? 'Creating account...' : 'Register'}
          </button>
          {error && <p className="auth-error">{error}</p>}
          <p className="page-subtitle" style={{ fontSize: '0.95rem' }}>
            Already have an account? <a className="auth-link" href="/login">Log in</a>
          </p>
        </form>
      </div>
    </div>
  )
}

export default RegisterForm