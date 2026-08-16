# Page Dependency Trees

## `/` — HomePage (redesign target: Learner Dashboard)
Entry: `src/App.jsx` (inline `HomePage` function, not its own file)
Dependencies:
- `src/assets/tiss-logo.svg` (image import)
- `src/context/AuthContext.jsx` (`useAuth()` → `{ user, logout }`)
- `react-router-dom` `Link`

Current content: logo, "Signed in as {name} ({role})", a link to `/courses`, a logout button. No course list, no progress, no certificates shown here today — this is the gap the redesign fills (dashboard should surface enrolled courses, progress %, and earned certificates per the brief).

Data this page will need once redesigned: `GET /courses` (enrolled/available courses), and per-course progress (`GET /courses/{id}/progress`) and certificate status (`GET /courses/{id}/certificate`) if the dashboard is to show progress/certs without navigating into each course. No existing "my courses" aggregate endpoint — the dashboard mock/design should treat this as a client-side aggregation over `listCourses()` + per-course progress calls (existing API shape), not require a new endpoint, since this design pass is HTML/CSS-only.

## `/courses/:courseId` — CourseDetailPage (redesign target: Course/module view)
Entry: `src/pages/CourseDetailPage.jsx`
Dependencies:
- `src/api/courses.js` → `getCourse(courseId)`
- `src/api/assessments.js` → `listQuizzes(courseId)`
- `src/api/progress.js` → `completeModule(moduleId)`, `getCourseProgress(courseId)`
- `src/api/certificates.js` → `downloadCertificatePdf(certificateId)`, `getCourseCertificate(courseId)`
- `react-router-dom` `Link`, `useParams`

Renders: course title/description, overall progress (`modules_completed`/`modules_total`, `pct_complete`), a "Download certificate" button when `certificate` is non-null, a list of modules (title + content + "Mark as complete" button, disabled once done), and a list of quizzes (title, link to `/quizzes/:id`, best score % + passed/not-passed once attempted).

Data shapes in play:
- `progress.completed_module_ids: string[]` — drives per-module button disabled state
- `progress.quizzes: [{ quiz_id, quiz_title, attempted, best_score_pct, passed }]`
- `certificate: { id, user_id, course_id, issued_at } | null`

## `/quizzes/:quizId` — QuizPage (redesign target: Quiz-taking screen)
Entry: `src/pages/QuizPage.jsx`
Dependencies:
- `src/api/assessments.js` → `getQuiz(quizId)`, `submitQuiz(quizId, answers)`, `startAdaptiveQuiz(quizId)`, `answerAdaptiveQuiz(quizId, sessionId, {...})`
- `react-router-dom` `Link`, `useParams`
- Internal sub-components (same file, not separate files): `StaticQuiz`, `AdaptiveQuiz`, `QuizResult`

Branches on `quiz.adaptive`:
- **`StaticQuiz`** (non-adaptive): all questions rendered at once as `<fieldset>` groups of radio options, single "Submit quiz" button, client holds all answers in state until submit.
- **`AdaptiveQuiz`**: one question at a time. Shows "Question {n} of {total} — difficulty: {easy|medium|hard}", radio options, a "Next" button that both answers the current question and fetches the next (or triggers `result` if `response.completed`).
- **`QuizResult`** (shared by both paths): score %, correct/total count, passed/not-passed, link back to course.

The redesign must accommodate BOTH quiz-taking modes with one coherent visual language — particularly the difficulty indicator (adaptive-only) and the distinction between "all questions visible" vs "one question, progressive" states.

## `/verify/:certificateId` — VerifyPage (redesign target: Certificate/verify page)
Entry: `src/pages/VerifyPage.jsx`
Dependencies:
- `src/api/certificates.js` → `verifyCertificate(certificateId)`
- `react-router-dom` `useParams`
- **No `RequireAuth` wrapper** — this route is public/unauthenticated by design (see `routes.md`); the redesigned page must remain fully functional with no logged-in shell/nav assumed.

Two states:
- **Not found** (`result.valid === false`, i.e. backend 404): "Certificate not found" + explanatory copy.
- **Valid**: "Certificate verified" + `learner_name`, `course_title`, `issued_at` (formatted date), `certificate_id`.

This is the page a third party (employer, verifier) lands on after scanning the QR code embedded in the certificate PDF — the design should read as trustworthy/official at a glance (this is exactly what "Editorial Tech" + Space Mono uppercase metadata labels are suited for), distinct from the learner-only "download certificate" button state that lives inside `CourseDetailPage`.

## Related page (context only, not a primary redesign target)

### `/courses` — CoursesPage
Entry: `src/pages/CoursesPage.jsx`
Dependencies: `src/api/courses.js` → `listCourses()`, `src/context/AuthContext.jsx` (role check for admin "Manage courses" link), `react-router-dom` `Link`
Renders: flat list of course title + description links to `/courses/:id`. Simple catalog browse — likely folds into the redesigned dashboard rather than staying separate, but not a required screen for this pass.
