import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { getCourse } from "../api/courses";

export default function CourseDetailPage() {
  const { courseId } = useParams();
  const [course, setCourse] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getCourse(courseId)
      .then(setCourse)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [courseId]);

  if (loading) return <p>Loading...</p>;
  if (error) return <p role="alert">{error}</p>;

  return (
    <section id="center">
      <p>
        <Link to="/courses">&larr; Back to courses</Link>
      </p>
      <h1>{course.title}</h1>
      <p>{course.description}</p>
      <h2>Modules</h2>
      {course.modules.length === 0 && <p>No modules yet.</p>}
      {course.modules.map((module) => (
        <article key={module.id}>
          <h3>{module.title}</h3>
          <p>{module.content}</p>
        </article>
      ))}
    </section>
  );
}
