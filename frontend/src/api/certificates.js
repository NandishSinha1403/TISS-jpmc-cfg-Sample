import { getToken } from "./client";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function getCourseCertificate(courseId) {
  const res = await fetch(`${API_BASE_URL}/courses/${courseId}/certificate`, {
    headers: { Authorization: `Bearer ${getToken()}` },
  });
  if (res.status === 404) return null;
  if (!res.ok) throw new Error("Failed to load certificate status");
  return res.json();
}

export async function downloadCertificatePdf(certificateId) {
  const res = await fetch(`${API_BASE_URL}/certificates/${certificateId}/pdf`, {
    headers: { Authorization: `Bearer ${getToken()}` },
  });
  if (!res.ok) throw new Error("Failed to download certificate");

  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `certificate-${certificateId}.pdf`;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

export async function verifyCertificate(certificateId) {
  const res = await fetch(`${API_BASE_URL}/verify/${certificateId}`);
  if (res.status === 404) return { valid: false };
  if (!res.ok) throw new Error("Failed to verify certificate");
  return res.json();
}
