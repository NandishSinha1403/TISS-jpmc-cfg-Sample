import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { getQuiz, submitQuiz } from "../api/assessments";

export default function QuizPage() {
  const { quizId } = useParams();
  const [quiz, setQuiz] = useState(null);
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    getQuiz(quizId)
      .then(setQuiz)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [quizId]);

  function selectAnswer(questionId, optionIndex) {
    setAnswers((prev) => ({ ...prev, [questionId]: optionIndex }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      setResult(await submitQuiz(quizId, answers));
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) return <p>Loading...</p>;
  if (error && !quiz) return <p role="alert">{error}</p>;

  if (result) {
    return (
      <section id="center">
        <h1>{quiz.title} — Result</h1>
        <p>
          Score: {result.score_pct.toFixed(1)}% ({result.correct_count}/{result.total_questions}{" "}
          correct)
        </p>
        <p>{result.passed ? "Passed" : "Not passed"}</p>
        <Link to={`/courses/${quiz.course_id}`}>Back to course</Link>
      </section>
    );
  }

  return (
    <section id="center">
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
    </section>
  );
}
