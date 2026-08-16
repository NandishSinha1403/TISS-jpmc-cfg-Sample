import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { listCourses } from "../api/courses";
import { getCourseProgress } from "../api/progress";
import { getCourseCertificate } from "../api/certificates";
import { useAuth } from "../context/AuthContext";
import ProgressBar from "../components/ProgressBar";
import StatusBadge from "../components/StatusBadge";

function ArrowIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true">
      <path d="M4 14L14 4M14 4H6M14 4V12" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

function SealIcon() {
  return (
    <svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true">
      <circle cx="10" cy="10" r="8.5" stroke="currentColor" strokeWidth="1.4" />
      <path d="M6.5 10.2L8.7 12.4L13.5 7.4" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

function StatCluster({ courseCount, avgProgress, certCount }) {
  return (
    <dl className="stat-strip">
      <div className="stat-strip-item">
        <dt className="stat-label">Enrolled</dt>
        <dd className="stat-value">{courseCount}</dd>
      </div>
      <div className="stat-strip-item">
        <dt className="stat-label">Avg. progress</dt>
        <dd className="stat-value">{avgProgress.toFixed(0)}%</dd>
      </div>
      <div className="stat-strip-item">
        <dt className="stat-label">Certificates</dt>
        <dd className="stat-value">{certCount}</dd>
      </div>
    </dl>
  );
}

function FeaturedCourse({ entry }) {
  const { course, progress, certificate } = entry;
  const isComplete = Boolean(certificate);

  return (
    <Link to={`/courses/${course.id}`} className="featured-course">
      <div className="featured-course-body">
        <div className="featured-course-heading">
          <h2 className="featured-course-title">{course.title}</h2>
          <StatusBadge tone={isComplete ? "success" : "neutral"}>
            {isComplete ? "Completed" : "In progress"}
          </StatusBadge>
        </div>
        <p className="featured-course-desc">{course.description}</p>
        <ProgressBar percent={progress.pct_complete} label={`${course.title} progress`} />
      </div>
      <span className="featured-course-cta">
        {isComplete ? "Review course" : "Resume"}
        <ArrowIcon />
      </span>
    </Link>
  );
}

function CourseRow({ entry }) {
  const { course, progress, certificate } = entry;
  return (
    <Link to={`/courses/${course.id}`} className="course-row">
      <span className="course-row-title">{course.title}</span>
      <span className="course-row-meta">
        <ProgressBar percent={progress.pct_complete} label={`${course.title} progress`} />
        <StatusBadge tone={certificate ? "success" : progress.pct_complete > 0 ? "neutral" : "neutral"}>
          {certificate ? "Complete" : progress.pct_complete > 0 ? "In progress" : "Not started"}
        </StatusBadge>
      </span>
    </Link>
  );
}

export default function DashboardPage() {
  const { user } = useAuth();
  const [enrolled, setEnrolled] = useState([]);
  const [certificates, setCertificates] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    listCourses()
      .then(async (courses) => {
        const withProgress = await Promise.all(
          courses.map(async (course) => {
            const [progress, certificate] = await Promise.all([
              getCourseProgress(course.id),
              getCourseCertificate(course.id),
            ]);
            return { course, progress, certificate };
          })
        );
        setEnrolled(withProgress);
        setCertificates(
          withProgress.filter((e) => e.certificate).map((e) => ({ ...e.certificate, courseTitle: e.course.title }))
        );
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const { featured, rest, avgProgress } = useMemo(() => {
    if (enrolled.length === 0) return { featured: null, rest: [], avgProgress: 0 };
    const sorted = [...enrolled].sort((a, b) => {
      const aDone = Boolean(a.certificate);
      const bDone = Boolean(b.certificate);
      if (aDone !== bDone) return aDone ? 1 : -1;
      return b.progress.pct_complete - a.progress.pct_complete;
    });
    const total = enrolled.reduce((sum, e) => sum + e.progress.pct_complete, 0);
    return { featured: sorted[0], rest: sorted.slice(1), avgProgress: total / enrolled.length };
  }, [enrolled]);

  if (loading) return <div className="content"><p>Loading dashboard...</p></div>;
  if (error) return <div className="content"><p role="alert">{error}</p></div>;

  return (
    <div className="content">
      <div className="dashboard-masthead">
        <h1 className="dashboard-hero">Welcome back, {user.full_name}</h1>
        {enrolled.length > 0 && (
          <StatCluster courseCount={enrolled.length} avgProgress={avgProgress} certCount={certificates.length} />
        )}
      </div>

      <h2>Your courses</h2>
      {enrolled.length === 0 ? (
        <div className="empty-panel">
          <p>You haven&rsquo;t enrolled in a course yet.</p>
          <Link to="/courses" className="btn btn-primary">
            Browse courses
          </Link>
        </div>
      ) : (
        <>
          <FeaturedCourse entry={featured} />
          {rest.length > 0 && (
            <div className="course-list">
              {rest.map((entry) => (
                <CourseRow key={entry.course.id} entry={entry} />
              ))}
            </div>
          )}
        </>
      )}

      <h2>Certificates earned</h2>
      {certificates.length === 0 ? (
        <div className="empty-panel">
          <p>Complete a course to earn your first certificate.</p>
        </div>
      ) : (
        <div className="cert-ledger">
          {certificates.map((cert) => (
            <Link to={`/courses/${cert.course_id}`} className="cert-ledger-row" key={cert.id}>
              <span className="cert-ledger-icon">
                <SealIcon />
              </span>
              <span className="cert-ledger-title">{cert.courseTitle}</span>
              <span className="cert-ledger-date">
                {new Date(cert.issued_at).toLocaleDateString(undefined, {
                  day: "2-digit",
                  month: "short",
                  year: "numeric",
                })}
              </span>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
