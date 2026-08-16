# Shared Layout Components

**There is no app shell, nav bar, header, sidebar, or footer anywhere in this codebase.** Each page renders standalone inside `<section id="center">`, and there is no persistent chrome — no logo/nav bar carries over between routes except that `HomePage` (in `App.jsx`) happens to show the TISS logo once, on the `/` route only.

This is another greenfield opportunity: the Editorial Tech redesign should introduce a persistent header/nav (logo, primary nav links, user identity + logout) shared across the authenticated app, since none exists today.

## `src/App.jsx` — Router root (closest thing to a "layout")

```jsx
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
```

## `src/components/RequireAuth.jsx` — route guard (not a layout, but gates every authenticated route)

```jsx
import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function RequireAuth({ roles, children }) {
  const { user, loading } = useAuth();

  if (loading) return <p>Loading...</p>;
  if (!user) return <Navigate to="/login" replace />;
  if (roles && !roles.includes(user.role)) return <Navigate to="/" replace />;

  return children;
}
```

## `src/main.jsx` — provider/router mount

```jsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import './index.css'
import App from './App.jsx'
import { AuthProvider } from './context/AuthContext.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <App />
      </AuthProvider>
    </BrowserRouter>
  </StrictMode>,
)
```
