import { apiFetch } from "./client";

export function getCourseProgress(courseId) {
  return apiFetch(`/courses/${courseId}/progress`);
}

export function completeModule(moduleId) {
  return apiFetch(`/modules/${moduleId}/complete`, { method: "POST" });
}
