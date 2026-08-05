import { Navigate } from 'react-router-dom'
import { getToken } from '../api/token'

interface ProtectedRouteProps {
  children: React.ReactNode
}

function ProtectedRoute({ children }: ProtectedRouteProps) {
  const token = getToken()

  if (!token) {
    return <Navigate to="/" replace />
  }

  return children
}

export default ProtectedRoute