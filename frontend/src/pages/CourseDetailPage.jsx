import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { getCourse } from "../api/courses";
import { listQuizzes } from "../api/assessments";
import { completeModule, getCourseProgress } from "../api/progress";

export default function CourseDetailPage() {
  const { courseId } = useParams();
  const [course, setCourse] = useState(null);
  const [quizzes, setQuizzes] = useState([]);
  const [progress, setProgress] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  function loadAll() {
    return Promise.all([getCourse(courseId), listQuizzes(courseId), getCourseProgress(courseId)]).then(
      ([courseData, quizzesData, progressData]) => {
        setCourse(courseData);
        setQuizzes(quizzesData);
        setProgress(progressData);
      }
    );
  }

  useEffect(() => {
    loadAll()
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [courseId]);

  async function handleCompleteModule(moduleId) {
    try {
      await completeModule(moduleId);
      setProgress(await getCourseProgress(courseId));
    } catch (err) {
      setError(err.message);
    }
  }

  if (loading) return <p>Loading...</p>;
  if (error) return <p role="alert">{error}</p>;

  const completedModuleIds = new Set(progress.completed_module_ids);
  const quizProgressByQuizId = Object.fromEntries(progress.quizzes.map((q) => [q.quiz_id, q]));

  return (
    <section id="center">
      <p>
        <Link to="/courses">&larr; Back to courses</Link>
      </p>
      <h1>{course.title}</h1>
      <p>{course.description}</p>
      <p>
        Progress: {progress.modules_completed}/{progress.modules_total} modules (
        {progress.pct_complete.toFixed(0)}%)
      </p>
      <h2>Modules</h2>
      {course.modules.length === 0 && <p>No modules yet.</p>}
      {course.modules.map((module) => (
        <article key={module.id}>
          <h3>{module.title}</h3>
          <p>{module.content}</p>
          <button
            type="button"
            onClick={() => handleCompleteModule(module.id)}
            disabled={completedModuleIds.has(module.id)}
          >
            {completedModuleIds.has(module.id) ? "Completed" : "Mark as complete"}
          </button>
        </article>
      ))}
      <h2>Quizzes</h2>
      {quizzes.length === 0 && <p>No quizzes yet.</p>}
      <ul>
        {quizzes.map((quiz) => {
          const qp = quizProgressByQuizId[quiz.id];
          return (
            <li key={quiz.id}>
              <Link to={`/quizzes/${quiz.id}`}>{quiz.title}</Link>
              {qp?.attempted && (
                <span>
                  {" "}
                  — best: {qp.best_score_pct.toFixed(0)}% ({qp.passed ? "passed" : "not passed"})
                </span>
              )}
            </li>
          );
        })}
      </ul>
    </section>
  );
}
