# Routes

Router: React Router v6 (`BrowserRouter`), config defined inline in `src/App.jsx` (see `layouts.md` for full source).

| Path | Component | Auth | Notes |
|---|---|---|---|
| `/login` | `src/pages/LoginPage.jsx` | public | |
| `/signup` | `src/pages/SignupPage.jsx` | public | learner-only signup (admin accounts are seeded, not self-registered) |
| `/verify/:certificateId` | `src/pages/VerifyPage.jsx` | **public, unauthenticated** | certificate verification — must render outside any logged-in shell |
| `/` | `HomePage` (inline in `App.jsx`) | required | minimal welcome + link to `/courses`; candidate for becoming the real learner dashboard |
| `/courses` | `src/pages/CoursesPage.jsx` | required | course catalog, any role |
| `/courses/:courseId` | `src/pages/CourseDetailPage.jsx` | required | modules + quizzes + progress + certificate download for one course |
| `/quizzes/:quizId` | `src/pages/QuizPage.jsx` | required | branches internally on `quiz.adaptive` between static and adaptive quiz UI |
| `/admin/courses` | `src/pages/AdminCoursesPage.jsx` | required, `roles={['admin']}` | admin course/module/quiz/question CRUD |

## Key pages for this design pass

- **`/` (HomePage)** → target for "Learner dashboard" redesign (screen 1)
- **`/courses/:courseId`** → target for "Course/module view" redesign (screen 2)
- **`/quizzes/:quizId`** → target for "Quiz-taking screen" redesign (screen 3)
- **`/verify/:certificateId`** → target for "Certificate/verify page" redesign (screen 4), plus the certificate-earned section inside `/courses/:courseId`
