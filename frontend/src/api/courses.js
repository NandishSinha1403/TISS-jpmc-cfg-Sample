import { apiFetch } from "./client";

export function listCourses() {
  return apiFetch("/courses");
}

export function getCourse(courseId) {
  return apiFetch(`/courses/${courseId}`);
}

export function createCourse({ title, description }) {
  return apiFetch("/courses", {
    method: "POST",
    body: JSON.stringify({ title, description }),
  });
}

export function updateCourse(courseId, data) {
  return apiFetch(`/courses/${courseId}`, {
    method: "PUT",
    body: JSON.stringify(data),
  });
}

export function deleteCourse(courseId) {
  return apiFetch(`/courses/${courseId}`, { method: "DELETE" });
}

export function addModule(courseId, { title, content, orderIndex }) {
  return apiFetch(`/courses/${courseId}/modules`, {
    method: "POST",
    body: JSON.stringify({ title, content, order_index: orderIndex }),
  });
}

export function deleteModule(courseId, moduleId) {
  return apiFetch(`/courses/${courseId}/modules/${moduleId}`, { method: "DELETE" });
}
