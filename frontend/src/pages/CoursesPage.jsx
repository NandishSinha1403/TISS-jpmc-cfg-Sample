import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { listCourses } from "../api/courses";
import { useAuth } from "../context/AuthContext";

export default function CoursesPage() {
  const { user } = useAuth();
  const [courses, setCourses] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    listCourses()
      .then(setCourses)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="content">
      <div className="page-header">
        <h1>Courses</h1>
        {user.role === "admin" && (
          <Link to="/admin/courses" className="btn btn-secondary">
            Manage courses
          </Link>
        )}
      </div>

      {loading && <p>Loading...</p>}
      {error && <p role="alert" className="form-error">{error}</p>}

      {!loading && courses.length === 0 ? (
        <div className="empty-panel">
          <p>No courses yet.</p>
        </div>
      ) : (
        <div className="catalog-list">
          {courses.map((course) => (
            <Link to={`/courses/${course.id}`} className="catalog-row" key={course.id}>
              <span className="catalog-row-title">{course.title}</span>
              <span className="catalog-row-desc">{course.description}</span>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
