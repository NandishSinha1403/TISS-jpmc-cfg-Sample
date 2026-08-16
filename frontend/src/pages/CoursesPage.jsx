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
    <section id="center">
      <h1>Courses</h1>
      {user.role === "admin" && (
        <p>
          <Link to="/admin/courses">Manage courses</Link>
        </p>
      )}
      {loading && <p>Loading...</p>}
      {error && <p role="alert">{error}</p>}
      <ul>
        {courses.map((course) => (
          <li key={course.id}>
            <Link to={`/courses/${course.id}`}>{course.title}</Link>
            <p>{course.description}</p>
          </li>
        ))}
      </ul>
      {!loading && courses.length === 0 && <p>No courses yet.</p>}
    </section>
  );
}
