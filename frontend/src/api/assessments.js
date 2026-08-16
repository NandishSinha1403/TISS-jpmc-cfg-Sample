import { apiFetch } from "./client";

export function listQuizzes(courseId) {
  return apiFetch(`/courses/${courseId}/quizzes`);
}

export function createQuiz(courseId, { title, passThresholdPct }) {
  return apiFetch(`/courses/${courseId}/quizzes`, {
    method: "POST",
    body: JSON.stringify({ title, pass_threshold_pct: passThresholdPct }),
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
