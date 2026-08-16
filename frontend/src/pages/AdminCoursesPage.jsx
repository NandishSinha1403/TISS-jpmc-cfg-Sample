import { useEffect, useState } from "react";
import { addModule, createCourse, deleteCourse, deleteModule, getCourse, listCourses } from "../api/courses";
import { addQuestion, createQuiz, getQuiz, listQuizzes } from "../api/assessments";

function ModuleForm({ courseId, onAdded }) {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    try {
      await addModule(courseId, { title, content, orderIndex: 0 });
      setTitle("");
      setContent("");
      onAdded();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        placeholder="Module title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        required
      />
      <textarea
        placeholder="Module content"
        value={content}
        onChange={(e) => setContent(e.target.value)}
      />
      <button type="submit">Add module</button>
      {error && <p role="alert">{error}</p>}
    </form>
  );
}

function QuestionForm({ quizId, onAdded }) {
  const [text, setText] = useState("");
  const [options, setOptions] = useState(["", ""]);
  const [correctIndex, setCorrectIndex] = useState(0);
  const [error, setError] = useState("");

  function updateOption(idx, value) {
    setOptions((prev) => prev.map((o, i) => (i === idx ? value : o)));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    try {
      await addQuestion(quizId, { text, options, correctIndex });
      setText("");
      setOptions(["", ""]);
      setCorrectIndex(0);
      onAdded();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input placeholder="Question text" value={text} onChange={(e) => setText(e.target.value)} required />
      {options.map((option, idx) => (
        <div key={idx}>
          <input
            type="radio"
            name="correct"
            checked={correctIndex === idx}
            onChange={() => setCorrectIndex(idx)}
          />
          <input
            placeholder={`Option ${idx + 1}`}
            value={option}
            onChange={(e) => updateOption(idx, e.target.value)}
            required
          />
        </div>
      ))}
      <button type="button" onClick={() => setOptions((prev) => [...prev, ""])}>
        Add option
      </button>
      <button type="submit">Add question (mark correct with radio)</button>
      {error && <p role="alert">{error}</p>}
    </form>
  );
}

function QuizManager({ courseId }) {
  const [quizzes, setQuizzes] = useState([]);
  const [title, setTitle] = useState("");
  const [passThreshold, setPassThreshold] = useState(70);
  const [expandedQuizId, setExpandedQuizId] = useState(null);
  const [expandedQuiz, setExpandedQuiz] = useState(null);
  const [error, setError] = useState("");

  function refresh() {
    return listQuizzes(courseId)
      .then(setQuizzes)
      .catch((err) => setError(err.message));
  }

  useEffect(() => {
    refresh();
  }, [courseId]);

  async function handleCreateQuiz(e) {
    e.preventDefault();
    setError("");
    try {
      await createQuiz(courseId, { title, passThresholdPct: Number(passThreshold) });
      setTitle("");
      refresh();
    } catch (err) {
      setError(err.message);
    }
  }

  async function toggleQuiz(quizId) {
    if (expandedQuizId === quizId) {
      setExpandedQuizId(null);
      return;
    }
    setExpandedQuizId(quizId);
    try {
      setExpandedQuiz(await getQuiz(quizId));
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div>
      <h4>Quizzes</h4>
      <ul>
        {quizzes.map((quiz) => (
          <li key={quiz.id}>
            {quiz.title} (pass: {quiz.pass_threshold_pct}%)
            <button type="button" onClick={() => toggleQuiz(quiz.id)}>
              {expandedQuizId === quiz.id ? "Hide" : "Manage questions"}
            </button>
            {expandedQuizId === quiz.id && expandedQuiz && (
              <div>
                <ul>
                  {expandedQuiz.questions.map((q) => (
                    <li key={q.id}>{q.text}</li>
                  ))}
                </ul>
                <QuestionForm quizId={quiz.id} onAdded={() => getQuiz(quiz.id).then(setExpandedQuiz)} />
              </div>
            )}
          </li>
        ))}
      </ul>
      <form onSubmit={handleCreateQuiz}>
        <input
          placeholder="Quiz title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
        <input
          type="number"
          placeholder="Pass %"
          value={passThreshold}
          onChange={(e) => setPassThreshold(e.target.value)}
        />
        <button type="submit">Create quiz</button>
      </form>
      {error && <p role="alert">{error}</p>}
    </div>
  );
}

function CourseRow({ course, onChanged }) {
  const [expanded, setExpanded] = useState(false);
  const [detail, setDetail] = useState(null);
  const [error, setError] = useState("");

  async function loadDetail() {
    try {
      setDetail(await getCourse(course.id));
    } catch (err) {
      setError(err.message);
    }
  }

  function toggle() {
    const next = !expanded;
    setExpanded(next);
    if (next && !detail) loadDetail();
  }

  async function handleDeleteCourse() {
    if (!confirm(`Delete course "${course.title}"? This deletes its modules too.`)) return;
    try {
      await deleteCourse(course.id);
      onChanged();
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleDeleteModule(moduleId) {
    try {
      await deleteModule(course.id, moduleId);
      loadDetail();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <li>
      <strong>{course.title}</strong>
      <button type="button" onClick={toggle}>
        {expanded ? "Hide" : "Manage"}
      </button>
      <button type="button" onClick={handleDeleteCourse}>
        Delete course
      </button>
      {error && <p role="alert">{error}</p>}
      {expanded && detail && (
        <div>
          <ul>
            {detail.modules.map((m) => (
              <li key={m.id}>
                {m.title}
                <button type="button" onClick={() => handleDeleteModule(m.id)}>
                  Remove
                </button>
              </li>
            ))}
          </ul>
          <ModuleForm courseId={course.id} onAdded={loadDetail} />
          <QuizManager courseId={course.id} />
        </div>
      )}
    </li>
  );
}

export default function AdminCoursesPage() {
  const [courses, setCourses] = useState([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  function refresh() {
    return listCourses()
      .then(setCourses)
      .catch((err) => setError(err.message));
  }

  useEffect(() => {
    refresh().finally(() => setLoading(false));
  }, []);

  async function handleCreate(e) {
    e.preventDefault();
    setError("");
    try {
      await createCourse({ title, description });
      setTitle("");
      setDescription("");
      refresh();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <section id="center">
      <h1>Manage courses</h1>
      <form onSubmit={handleCreate}>
        <input
          placeholder="Course title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
        <input
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <button type="submit">Create course</button>
      </form>
      {error && <p role="alert">{error}</p>}
      {loading && <p>Loading...</p>}
      <ul>
        {courses.map((course) => (
          <CourseRow key={course.id} course={course} onChanged={refresh} />
        ))}
      </ul>
    </section>
  );
}
