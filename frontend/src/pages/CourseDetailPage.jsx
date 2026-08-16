import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { getCourse } from "../api/courses";
import { listQuizzes } from "../api/assessments";
import { completeModule, getCourseProgress } from "../api/progress";
import { downloadCertificatePdf, getCourseCertificate } from "../api/certificates";
import ProgressBar from "../components/ProgressBar";
import StatusBadge from "../components/StatusBadge";

export default function CourseDetailPage() {
  const { courseId } = useParams();
  const [course, setCourse] = useState(null);
  const [quizzes, setQuizzes] = useState([]);
  const [progress, setProgress] = useState(null);
  const [certificate, setCertificate] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState(false);

  function loadAll() {
    return Promise.all([
      getCourse(courseId),
      listQuizzes(courseId),
      getCourseProgress(courseId),
      getCourseCertificate(courseId),
    ]).then(([courseData, quizzesData, progressData, certificateData]) => {
      setCourse(courseData);
      setQuizzes(quizzesData);
      setProgress(progressData);
      setCertificate(certificateData);
    });
  }

  async function handleDownloadCertificate() {
    setDownloading(true);
    try {
      await downloadCertificatePdf(certificate.id);
    } catch (err) {
      setError(err.message);
    } finally {
      setDownloading(false);
    }
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

  if (loading) return <div className="content"><p>Loading...</p></div>;
  if (error) return <div className="content"><p role="alert">{error}</p></div>;

  const completedModuleIds = new Set(progress.completed_module_ids);
  const quizProgressByQuizId = Object.fromEntries(progress.quizzes.map((q) => [q.quiz_id, q]));

  return (
    <div className="content">
      <p>
        <Link to="/courses">&larr; Back to courses</Link>
      </p>
      <h1>{course.title}</h1>
      <p className="prose">{course.description}</p>
      <ProgressBar percent={progress.pct_complete} label="Course progress" />

      {certificate && (
        <div className="card cert-callout">
          <div>
            <StatusBadge tone="success">Certificate earned</StatusBadge>
          </div>
          <button type="button" className="btn btn-primary" onClick={handleDownloadCertificate} disabled={downloading}>
            {downloading ? "Downloading..." : "Download certificate"}
          </button>
        </div>
      )}

      <h2>Modules</h2>
      {course.modules.length === 0 && <p>No modules yet.</p>}
      {course.modules.map((module) => {
        const done = completedModuleIds.has(module.id);
        return (
          <article className="card module-card" key={module.id}>
            <h3>{module.title}</h3>
            <p className="prose">{module.content}</p>
            {done ? (
              <StatusBadge tone="success">Completed</StatusBadge>
            ) : (
              <button type="button" className="btn btn-primary" onClick={() => handleCompleteModule(module.id)}>
                Mark as complete
              </button>
            )}
          </article>
        );
      })}

      <h2>Quizzes</h2>
      {quizzes.length === 0 && <p>No quizzes yet.</p>}
      <div className="quiz-list">
        {quizzes.map((quiz) => {
          const qp = quizProgressByQuizId[quiz.id];
          return (
            <div className="quiz-row" key={quiz.id}>
              <Link to={`/quizzes/${quiz.id}`}>{quiz.title}</Link>
              {qp?.attempted && (
                <span className="quiz-row-status">
                  <StatusBadge tone={qp.passed ? "success" : "warning"}>
                    {qp.passed ? "Passed" : "Not passed"}
                  </StatusBadge>
                  <span className="progress-percent">{qp.best_score_pct.toFixed(0)}%</span>
                </span>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
