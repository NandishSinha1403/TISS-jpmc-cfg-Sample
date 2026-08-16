import { Routes, Route } from 'react-router-dom'
import LoginPage from './pages/LoginPage'
import SignupPage from './pages/SignupPage'
import CoursesPage from './pages/CoursesPage'
import CourseDetailPage from './pages/CourseDetailPage'
import QuizPage from './pages/QuizPage'
import AdminCoursesPage from './pages/AdminCoursesPage'
import VerifyPage from './pages/VerifyPage'
import DashboardPage from './pages/DashboardPage'
import RequireAuth from './components/RequireAuth'
import AppHeader from './components/AppHeader'
import CustomCursor from './components/CustomCursor'

function App() {
  return (
    <>
      <CustomCursor />
      <AppHeader />
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/verify/:certificateId" element={<VerifyPage />} />
        <Route
          path="/"
          element={
            <RequireAuth>
              <DashboardPage />
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
    </>
  )
}

export default App
