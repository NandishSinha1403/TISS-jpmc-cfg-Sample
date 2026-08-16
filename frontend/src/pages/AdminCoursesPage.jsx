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
    <form onSubmit={handleSubmit} className="field-list admin-subform">
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
      <button type="submit" className="btn btn-secondary">
        Add module
      </button>
      {error && <p role="alert" className="form-error">{error}</p>}
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
    <form onSubmit={handleSubmit} className="field-list admin-subform">
      <input placeholder="Question text" value={text} onChange={(e) => setText(e.target.value)} required />
      {options.map((option, idx) => (
        <label className="option-row admin-option-row" key={idx}>
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
        </label>
      ))}
      <button type="button" className="btn btn-secondary" onClick={() => setOptions((prev) => [...prev, ""])}>
        Add option
      </button>
      <button type="submit" className="btn btn-primary">
        Add question (mark correct with radio)
      </button>
      {error && <p role="alert" className="form-error">{error}</p>}
    </form>
  );
}

function QuizManager({ courseId }) {
  const [quizzes, setQuizzes] = useState([]);
  const [title, setTitle] = useState("");
  const [passThreshold, setPassThreshold] = useState(70);
  const [expandedQuizId, setExpandedQuizId] = useState(null);
  const [expandedQuiz, setExpandedQuiz] = useState(null);
  const [adaptive, setAdaptive] = useState(false);
  const [questionsPerAttempt, setQuestionsPerAttempt] = useState(5);
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
      await createQuiz(courseId, {
        title,
        passThresholdPct: Number(passThreshold),
        adaptive,
        questionsPerAttempt: Number(questionsPerAttempt),
      });
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
    <div className="admin-section">
      <h4 className="admin-section-title">Quizzes</h4>
      {quizzes.length === 0 && <p className="admin-empty">No quizzes yet.</p>}
      <div className="admin-row-list">
        {quizzes.map((quiz) => (
          <div className="admin-row" key={quiz.id}>
            <div className="admin-row-head">
              <span>
                {quiz.title}{" "}
                <span className="stat-label">
                  ({quiz.pass_threshold_pct}% pass{quiz.adaptive ? `, adaptive` : ""})
                </span>
              </span>
              <button type="button" className="btn btn-secondary" onClick={() => toggleQuiz(quiz.id)}>
                {expandedQuizId === quiz.id ? "Hide" : "Manage questions"}
              </button>
            </div>
            {expandedQuizId === quiz.id && expandedQuiz && (
              <div className="admin-row-body">
                {expandedQuiz.questions.length === 0 && <p className="admin-empty">No questions yet.</p>}
                <ul className="admin-plain-list">
                  {expandedQuiz.questions.map((q) => (
                    <li key={q.id}>{q.text}</li>
                  ))}
                </ul>
                <QuestionForm quizId={quiz.id} onAdded={() => getQuiz(quiz.id).then(setExpandedQuiz)} />
              </div>
            )}
          </div>
        ))}
      </div>

      <form onSubmit={handleCreateQuiz} className="field-list admin-subform">
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
        <label className="admin-checkbox-row">
          <input type="checkbox" checked={adaptive} onChange={(e) => setAdaptive(e.target.checked)} />
          Adaptive difficulty
        </label>
        {adaptive && (
          <input
            type="number"
            placeholder="Questions per attempt"
            value={questionsPerAttempt}
            onChange={(e) => setQuestionsPerAttempt(e.target.value)}
            min={1}
          />
        )}
        <button type="submit" className="btn btn-primary">
          Create quiz
        </button>
      </form>
      {error && <p role="alert" className="form-error">{error}</p>}
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
    <div className="card admin-course-card">
      <div className="admin-row-head">
        <strong>{course.title}</strong>
        <div className="admin-row-actions">
          <button type="button" className="btn btn-secondary" onClick={toggle}>
            {expanded ? "Hide" : "Manage"}
          </button>
          <button type="button" className="btn btn-secondary" onClick={handleDeleteCourse}>
            Delete
          </button>
        </div>
      </div>
      {error && <p role="alert" className="form-error">{error}</p>}
      {expanded && detail && (
        <div className="admin-row-body">
          <div className="admin-section">
            <h4 className="admin-section-title">Modules</h4>
            {detail.modules.length === 0 && <p className="admin-empty">No modules yet.</p>}
            <ul className="admin-plain-list">
              {detail.modules.map((m) => (
                <li key={m.id}>
                  <span>{m.title}</span>
                  <button type="button" className="btn btn-secondary" onClick={() => handleDeleteModule(m.id)}>
                    Remove
                  </button>
                </li>
              ))}
            </ul>
            <ModuleForm courseId={course.id} onAdded={loadDetail} />
          </div>
          <QuizManager courseId={course.id} />
        </div>
      )}
    </div>
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
    <div className="content">
      <h1>Manage courses</h1>

      <div className="card admin-create-card">
        <h3>New course</h3>
        <form onSubmit={handleCreate} className="field-list">
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
          <button type="submit" className="btn btn-primary">
            Create course
          </button>
        </form>
        {error && <p role="alert" className="form-error">{error}</p>}
      </div>

      {loading && <p>Loading...</p>}
      <div className="admin-course-list">
        {courses.map((course) => (
          <CourseRow key={course.id} course={course} onChanged={refresh} />
        ))}
      </div>
    </div>
  );
}
