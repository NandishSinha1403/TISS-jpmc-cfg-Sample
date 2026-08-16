import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { answerAdaptiveQuiz, getQuiz, startAdaptiveQuiz, submitQuiz } from "../api/assessments";
import StatusBadge from "../components/StatusBadge";

function QuestionCard({ number, question, selected, onSelect }) {
  return (
    <fieldset className="card question-card">
      <legend className="eyebrow">Question {number}</legend>
      <p className="question-text">{question.text}</p>
      {question.options.map((option, idx) => (
        <label key={idx} className={`option-row ${selected === idx ? "option-row--selected" : ""}`}>
          <input
            type="radio"
            name={question.id}
            checked={selected === idx}
            onChange={() => onSelect(idx)}
          />
          {option}
        </label>
      ))}
    </fieldset>
  );
}

function StaticQuiz({ quiz }) {
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  function selectAnswer(questionId, optionIndex) {
    setAnswers((prev) => ({ ...prev, [questionId]: optionIndex }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      setResult(await submitQuiz(quiz.id, answers));
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  if (result) return <QuizResult quiz={quiz} result={result} />;

  return (
    <>
      <h1>{quiz.title}</h1>
      <form onSubmit={handleSubmit}>
        {quiz.questions.map((q, i) => (
          <QuestionCard
            key={q.id}
            number={i + 1}
            question={q}
            selected={answers[q.id]}
            onSelect={(idx) => selectAnswer(q.id, idx)}
          />
        ))}
        <button type="submit" className="btn btn-primary" disabled={submitting}>
          {submitting ? "Submitting..." : "Submit quiz"}
        </button>
      </form>
      {error && <p role="alert">{error}</p>}
    </>
  );
}

function AdaptiveQuiz({ quiz }) {
  const [session, setSession] = useState(null);
  const [result, setResult] = useState(null);
  const [selected, setSelected] = useState(null);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    startAdaptiveQuiz(quiz.id)
      .then(setSession)
      .catch((err) => setError(err.message));
  }, [quiz.id]);

  async function handleSubmit(e) {
    e.preventDefault();
    if (selected === null) return;
    setError("");
    setSubmitting(true);
    try {
      const response = await answerAdaptiveQuiz(quiz.id, session.session_id, {
        questionId: session.question.id,
        selectedIndex: selected,
      });
      setSelected(null);
      if (response.completed) {
        setResult(response.result);
      } else {
        setSession(response);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  if (result) return <QuizResult quiz={quiz} result={result} />;
  if (error) return <p role="alert">{error}</p>;
  if (!session) return <p>Loading first question...</p>;

  return (
    <>
      <h1>{quiz.title}</h1>
      <div className="adaptive-readout">
        <span className="eyebrow">
          Question {session.question_number} of {session.total_questions}
        </span>
        <StatusBadge tone="neutral">{session.question.difficulty}</StatusBadge>
      </div>
      <form onSubmit={handleSubmit}>
        <QuestionCard
          number={session.question_number}
          question={session.question}
          selected={selected}
          onSelect={setSelected}
        />
        <button type="submit" className="btn btn-primary" disabled={submitting || selected === null}>
          {submitting ? "Submitting..." : "Next"}
        </button>
      </form>
    </>
  );
}

function QuizResult({ quiz, result }) {
  return (
    <div className="result-panel">
      <p className="result-score">{result.score_pct.toFixed(0)}%</p>
      <StatusBadge tone={result.passed ? "success" : "warning"}>
        {result.passed ? "Passed" : "Not passed"}
      </StatusBadge>
      <p>
        {result.correct_count}/{result.total_questions} correct
      </p>
      <Link to={`/courses/${quiz.course_id}`} className="btn btn-secondary">
        Back to course
      </Link>
    </div>
  );
}

export default function QuizPage() {
  const { quizId } = useParams();
  const [quiz, setQuiz] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getQuiz(quizId)
      .then(setQuiz)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [quizId]);

  if (loading) return <div className="content content--narrow"><p>Loading...</p></div>;
  if (error) return <div className="content content--narrow"><p role="alert">{error}</p></div>;

  return (
    <div className="content content--narrow">
      {quiz.adaptive ? <AdaptiveQuiz quiz={quiz} /> : <StaticQuiz quiz={quiz} />}
    </div>
  );
}
