import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { listCourses } from "../api/courses";
import { getCourseProgress } from "../api/progress";
import { getCourseCertificate } from "../api/certificates";
import { useAuth } from "../context/AuthContext";
import ProgressBar from "../components/ProgressBar";
import StatusBadge from "../components/StatusBadge";

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
        setCertificates(withProgress.filter((e) => e.certificate).map((e) => ({ ...e.certificate, courseTitle: e.course.title })));
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="content"><p>Loading dashboard...</p></div>;
  if (error) return <div className="content"><p role="alert">{error}</p></div>;

  return (
    <div className="content">
      <p className="eyebrow">Dashboard</p>
      <h1 className="dashboard-hero">Welcome back, {user.full_name}</h1>

      <h2>Your courses</h2>
      {enrolled.length === 0 && <p>No courses yet — visit Courses to get started.</p>}
      <div className="course-grid">
        {enrolled.map(({ course, progress, certificate }) => (
          <Link to={`/courses/${course.id}`} key={course.id} className="card course-card">
            <h3>{course.title}</h3>
            <p>{course.description}</p>
            <ProgressBar percent={progress.pct_complete} label={`${course.title} progress`} />
            <StatusBadge tone={certificate ? "success" : progress.pct_complete > 0 ? "neutral" : "neutral"}>
              {certificate ? "Complete" : progress.pct_complete > 0 ? "In progress" : "Not started"}
            </StatusBadge>
          </Link>
        ))}
      </div>

      <h2>Certificates earned</h2>
      {certificates.length === 0 && <p>Complete a course to earn your first certificate.</p>}
      <div className="cert-row">
        {certificates.map((cert) => (
          <div className="card cert-card" key={cert.id}>
            <p className="eyebrow">Certificate</p>
            <h3>{cert.courseTitle}</h3>
            <p>{new Date(cert.issued_at).toLocaleDateString()}</p>
            <Link to={`/courses/${cert.course_id}`} className="btn btn-secondary">
              View
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}
