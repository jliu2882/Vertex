import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useMutation } from '@tanstack/react-query'
import RegisterForm from '../components/RegisterForm'
import { register } from '../api/auth'
import { setToken } from '../api/token'

function RegisterPage() {
  const navigate = useNavigate()
  const [error, setError] = useState('')

  const mutation = useMutation({
    mutationFn: ({ email, username, password }: { email: string; username: string, password: string }) =>
      register(email, username, password),
    onSuccess: (data) => {
      setToken(data.access_token)
      navigate('/tasks')
    },
    onError: () => setError('Invalid email or password'),
  })

  return (
    <RegisterForm
      onSubmit={(email, username, password) => mutation.mutate({ email, username, password })}
      isSubmitting={mutation.isPending}
      error={error}
    />
  )
}

export default RegisterPage