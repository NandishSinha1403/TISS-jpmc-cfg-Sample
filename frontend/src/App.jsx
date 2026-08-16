import { Routes, Route } from 'react-router-dom'
import tissLogo from './assets/tiss-logo.svg'
import { useAuth } from './context/AuthContext'
import LoginPage from './pages/LoginPage'
import SignupPage from './pages/SignupPage'
import RequireAuth from './components/RequireAuth'
import './App.css'

function HomePage() {
  const { user, logout } = useAuth()
  return (
    <section id="center">
      <img src={tissLogo} alt="TISS logo" width="120" />
      <h1>TISS Learning Platform</h1>
      <p>Signed in as <strong>{user.full_name}</strong> ({user.role})</p>
      <button type="button" onClick={logout}>Log out</button>
    </section>
  )
}

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/signup" element={<SignupPage />} />
      <Route
        path="/"
        element={
          <RequireAuth>
            <HomePage />
          </RequireAuth>
        }
      />
    </Routes>
  )
}

export default App
