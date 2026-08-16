import { Routes, Route, Link } from 'react-router-dom'
import tissLogo from './assets/tiss-logo.svg'
import { useAuth } from './context/AuthContext'
import LoginPage from './pages/LoginPage'
import SignupPage from './pages/SignupPage'
import CoursesPage from './pages/CoursesPage'
import CourseDetailPage from './pages/CourseDetailPage'
import QuizPage from './pages/QuizPage'
import AdminCoursesPage from './pages/AdminCoursesPage'
import VerifyPage from './pages/VerifyPage'
import RequireAuth from './components/RequireAuth'
import './App.css'

function HomePage() {
  const { user, logout } = useAuth()
  return (
    <section id="center">
      <img src={tissLogo} alt="TISS logo" width="120" />
      <h1>TISS Learning Platform</h1>
      <p>Signed in as <strong>{user.full_name}</strong> ({user.role})</p>
      <p>
        <Link to="/courses">Browse courses</Link>
      </p>
      <button type="button" onClick={logout}>Log out</button>
    </section>
  )
}

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/signup" element={<SignupPage />} />
      <Route path="/verify/:certificateId" element={<VerifyPage />} />
      <Route
        path="/"
        element={
          <RequireAuth>
            <HomePage />
          </RequireAuth>
        }
      />
      <Route
        path="/courses"
        element={
          <RequireAuth>
            <CoursesPage />
          </RequireAuth>
        }
      />
      <Route
        path="/courses/:courseId"
        element={
          <RequireAuth>
            <CourseDetailPage />
          </RequireAuth>
        }
      />
      <Route
        path="/quizzes/:quizId"
        element={
          <RequireAuth>
            <QuizPage />
          </RequireAuth>
        }
      />
      <Route
        path="/admin/courses"
        element={
          <RequireAuth roles={['admin']}>
            <AdminCoursesPage />
          </RequireAuth>
        }
      />
    </Routes>
  )
}

export default App
