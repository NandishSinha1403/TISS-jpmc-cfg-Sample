import { apiFetch } from "./client";

export function listQuizzes(courseId) {
  return apiFetch(`/courses/${courseId}/quizzes`);
}

export function createQuiz(courseId, { title, passThresholdPct, adaptive, questionsPerAttempt }) {
  return apiFetch(`/courses/${courseId}/quizzes`, {
    method: "POST",
    body: JSON.stringify({
      title,
      pass_threshold_pct: passThresholdPct,
      adaptive,
      questions_per_attempt: questionsPerAttempt,
    }),
  });
}

export function startAdaptiveQuiz(quizId) {
  return apiFetch(`/quizzes/${quizId}/start`, { method: "POST" });
}

export function answerAdaptiveQuiz(quizId, sessionId, { questionId, selectedIndex }) {
  return apiFetch(`/quizzes/${quizId}/sessions/${sessionId}/answer`, {
    method: "POST",
    body: JSON.stringify({ question_id: questionId, selected_index: selectedIndex }),
  });
}

export function getQuiz(quizId) {
  return apiFetch(`/quizzes/${quizId}`);
}

export function addQuestion(quizId, { text, options, correctIndex, difficulty }) {
  return apiFetch(`/quizzes/${quizId}/questions`, {
    method: "POST",
    body: JSON.stringify({ text, options, correct_index: correctIndex, difficulty }),
  });
}

export function submitQuiz(quizId, answers) {
  return apiFetch(`/quizzes/${quizId}/submit`, {
    method: "POST",
    body: JSON.stringify({ answers }),
  });
}
