import { useEffect, useRef, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { answerAdaptiveQuiz, getQuiz, startAdaptiveQuiz, submitQuiz } from "../api/assessments";
import { downloadCertificatePdf, getCourseCertificate } from "../api/certificates";
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

function StaticQuiz({ quiz, onComplete }) {
  const [answers, setAnswers] = useState({});
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
      onComplete(await submitQuiz(quiz.id, answers));
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

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

const DIFFICULTY_RANK = { easy: 0, medium: 1, hard: 2 };

function AdaptiveQuiz({ quiz, onComplete }) {
  const [session, setSession] = useState(null);
  const [selected, setSelected] = useState(null);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [shift, setShift] = useState(null);
  const prevDifficulty = useRef(null);

  useEffect(() => {
    startAdaptiveQuiz(quiz.id)
      .then((s) => {
        prevDifficulty.current = s.question.difficulty;
        setSession(s);
      })
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
        onComplete(response.result);
      } else {
        const prevRank = DIFFICULTY_RANK[prevDifficulty.current];
        const nextRank = DIFFICULTY_RANK[response.question.difficulty];
        setShift(nextRank > prevRank ? "up" : nextRank < prevRank ? "down" : null);
        prevDifficulty.current = response.question.difficulty;
        setSession(response);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  if (error) return <p role="alert">{error}</p>;
  if (!session) return <p>Loading first question...</p>;

  return (
    <>
      <h1>{quiz.title}</h1>
      <div className="adaptive-readout" key={session.question.id}>
        <span className="eyebrow">
          Question {session.question_number} of {session.total_questions}
        </span>
        <span className={`difficulty-badge ${shift ? `difficulty-badge--${shift}` : ""}`}>
          <StatusBadge tone="neutral">{session.question.difficulty}</StatusBadge>
        </span>
      </div>
      <form onSubmit={handleSubmit}>
        <QuestionCard
          key={session.question.id}
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

function QuizResult({ quiz, result, newCertificate }) {
  const [downloading, setDownloading] = useState(false);

  async function handleDownload() {
    setDownloading(true);
    try {
      await downloadCertificatePdf(newCertificate.id);
    } finally {
      setDownloading(false);
    }
  }

  if (newCertificate) {
    return (
      <div>
        <div className="result-panel result-panel--certified">
          <span className="certified-seal">
            <svg width="56" height="56" viewBox="0 0 56 56" fill="none" aria-hidden="true">
              <circle cx="28" cy="28" r="25" stroke="currentColor" strokeWidth="2" />
              <path d="M17 28.5L24 35.5L39 19.5" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </span>
          <p className="eyebrow">Course complete</p>
          <h1 className="certified-title">You&rsquo;re certified.</h1>
          <p className="certified-subtitle">
            You passed every assessment in this course — your certificate is ready.
          </p>
          <div className="certified-actions">
            <button type="button" className="btn btn-primary" onClick={handleDownload} disabled={downloading}>
              {downloading ? "Downloading..." : "Download certificate"}
            </button>
            <Link to={`/courses/${quiz.course_id}`} className="btn btn-secondary">
              Back to course
            </Link>
          </div>
        </div>
        {result.questions.length > 0 && <QuestionReview questions={result.questions} />}
      </div>
    );
  }

  return (
    <div>
      <div className="result-panel">
        <p className="result-score">{result.score_pct.toFixed(0)}%</p>
        <StatusBadge tone={result.passed ? "success" : "warning"}>
          {result.passed ? "Passed" : "Not passed"}
        </StatusBadge>
        <p>
          {result.correct_count}/{result.total_questions} correct
        </p>
        <div className="result-actions">
          <Link to={`/courses/${quiz.course_id}`} className="btn btn-secondary">
            Back to course
          </Link>
        </div>
      </div>
      {result.questions.length > 0 && <QuestionReview questions={result.questions} />}
    </div>
  );
}

function QuestionReview({ questions }) {
  const [open, setOpen] = useState(false);

  return (
    <div className="review-section">
      <button type="button" className="btn btn-secondary review-toggle" onClick={() => setOpen((v) => !v)} aria-expanded={open}>
        {open ? "Hide answer review" : "Review your answers"}
      </button>
      {open && (
        <div className="review-list">
          {questions.map((q, i) => (
            <div className="card review-item" key={q.question_id}>
              <div className="review-item-head">
                <span className="eyebrow">Question {i + 1}</span>
                <StatusBadge tone={q.is_correct ? "success" : "warning"}>
                  {q.is_correct ? "Correct" : "Incorrect"}
                </StatusBadge>
              </div>
              <p className="question-text">{q.text}</p>
              {q.options.map((option, idx) => {
                const isYourAnswer = idx === q.selected_index;
                const isCorrectAnswer = idx === q.correct_index;
                return (
                  <div
                    key={idx}
                    className={`review-option ${isCorrectAnswer ? "review-option--correct" : ""} ${
                      isYourAnswer && !isCorrectAnswer ? "review-option--wrong" : ""
                    }`}
                  >
                    <span>{option}</span>
                    {isCorrectAnswer && <span className="review-tag">Correct answer</span>}
                    {isYourAnswer && !isCorrectAnswer && <span className="review-tag">Your answer</span>}
                  </div>
                );
              })}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default function QuizPage() {
  const { quizId } = useParams();
  const [quiz, setQuiz] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [result, setResult] = useState(null);
  const [newCertificate, setNewCertificate] = useState(null);
  const hadCertificateBefore = useRef(false);

  useEffect(() => {
    getQuiz(quizId)
      .then(async (q) => {
        setQuiz(q);
        try {
          hadCertificateBefore.current = Boolean(await getCourseCertificate(q.course_id));
        } catch {
          hadCertificateBefore.current = false;
        }
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [quizId]);

  async function handleComplete(quizResult) {
    setResult(quizResult);
    if (quizResult.passed && !hadCertificateBefore.current) {
      try {
        const cert = await getCourseCertificate(quiz.course_id);
        if (cert) setNewCertificate(cert);
      } catch {
        // no certificate issued (course has other unfinished quizzes) — routine result stands
      }
    }
  }

  if (loading) return <div className="content content--narrow"><p>Loading...</p></div>;
  if (error) return <div className="content content--narrow"><p role="alert">{error}</p></div>;

  return (
    <div className="content content--narrow">
      {result ? (
        <QuizResult quiz={quiz} result={result} newCertificate={newCertificate} />
      ) : quiz.adaptive ? (
        <AdaptiveQuiz quiz={quiz} onComplete={handleComplete} />
      ) : (
        <StaticQuiz quiz={quiz} onComplete={handleComplete} />
      )}
    </div>
  );
}
