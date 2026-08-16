import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { answerAdaptiveQuiz, getQuiz, startAdaptiveQuiz, submitQuiz } from "../api/assessments";

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
          <fieldset key={q.id}>
            <legend>
              {i + 1}. {q.text}
            </legend>
            {q.options.map((option, idx) => (
              <label key={idx}>
                <input
                  type="radio"
                  name={q.id}
                  checked={answers[q.id] === idx}
                  onChange={() => selectAnswer(q.id, idx)}
                />
                {option}
              </label>
            ))}
          </fieldset>
        ))}
        <button type="submit" disabled={submitting}>
          {submitting ? "Submitting..." : "Submit quiz"}
        </button>
      </form>
      {error && <p role="alert">{error}</p>}
    </>
  );
}

function AdaptiveQuiz({ quiz }) {
  const [session, setSession] = useState(null); // { session_id, question, question_number, total_questions }
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
      <p>
        Question {session.question_number} of {session.total_questions} — difficulty:{" "}
        {session.question.difficulty}
      </p>
      <form onSubmit={handleSubmit}>
        <fieldset>
          <legend>{session.question.text}</legend>
          {session.question.options.map((option, idx) => (
            <label key={idx}>
              <input
                type="radio"
                name={session.question.id}
                checked={selected === idx}
                onChange={() => setSelected(idx)}
              />
              {option}
            </label>
          ))}
        </fieldset>
        <button type="submit" disabled={submitting || selected === null}>
          {submitting ? "Submitting..." : "Next"}
        </button>
      </form>
    </>
  );
}

function QuizResult({ quiz, result }) {
  return (
    <>
      <h1>{quiz.title} — Result</h1>
      <p>
        Score: {result.score_pct.toFixed(1)}% ({result.correct_count}/{result.total_questions} correct)
      </p>
      <p>{result.passed ? "Passed" : "Not passed"}</p>
      <Link to={`/courses/${quiz.course_id}`}>Back to course</Link>
    </>
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

  if (loading) return <p>Loading...</p>;
  if (error) return <p role="alert">{error}</p>;

  return (
    <section id="center">
      {quiz.adaptive ? <AdaptiveQuiz quiz={quiz} /> : <StaticQuiz quiz={quiz} />}
    </section>
  );
}
