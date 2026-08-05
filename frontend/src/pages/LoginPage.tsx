import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useMutation } from '@tanstack/react-query'
import LoginForm from '../components/LoginForm'
import { login } from '../api/auth'
import { setToken } from '../api/token'

function LoginPage() {
  const navigate = useNavigate()
  const [error, setError] = useState('')

  useEffect(() => {
    if (!error) return

    const timer = window.setTimeout(() => setError(''), 4000)
    return () => window.clearTimeout(timer)
  }, [error])

  const mutation = useMutation({
    mutationFn: ({ email, password }: { email: string; password: string }) =>
      login(email, password),
    onSuccess: (data) => {
      setToken(data.access_token)
      navigate('/tasks')
    },
    onError: () => setError('Invalid email or password'),
  })

  return (
    <LoginForm
      onSubmit={(email, password) => {
        setError('')
        mutation.mutate({ email, password })
      }}
      isSubmitting={mutation.isPending}
      error={error}
    />
  )
}

export default LoginPage