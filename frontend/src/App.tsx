import { Routes, Route } from 'react-router-dom'
import TaskListPage from './pages/TaskListPage'
import LoginPage from './pages/LoginPage'
import ProtectedRoute from './components/ProtectedRoute'
import RegisterPage from './pages/RegisterPage'
import { LandingPage } from './pages/LandingPage'

function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/tasks" element={
        <ProtectedRoute>
            <TaskListPage />
        </ProtectedRoute>
      }/>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
    </Routes>
  )
}

export default App
