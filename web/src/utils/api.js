/**
 * API utility
 * Centralizes calls to the backend using the configured base URL.
 * Keeping all fetch logic here simplifies error handling and testing.
 */

// Resolve the API base URL from Vite environment variables, with a sensible default for dev.
const API_BASE = (import.meta?.env?.VITE_API_BASE_URL || "http://localhost:8000").replace(/\/$/, "");

/**
 * GET /health
 * Returns a minimal status payload.
 */
export async function getHealth() {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error(`Health failed (${res.status})`);
  return res.json();
}

/**
 * GET /v1/verify/search?q=...&country=...
 * Returns an array of candidate objects.
 */
export async function searchCandidates(q, country) {
  const params = new URLSearchParams();
  params.set("q", q);
  if (country) params.set("country", country);
  const res = await fetch(`${API_BASE}/v1/verify/search?${params.toString()}`);
  if (!res.ok) throw new Error(`Search failed (${res.status})`);
  return res.json();
}

/**
 * POST /v1/verify
 * Sends { name, country } and returns a verification result.
 */
export async function verifyEntity(name, country) {
  const res = await fetch(`${API_BASE}/v1/verify`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, country })
  });
  if (!res.ok) throw new Error(`Verify failed (${res.status})`);
  return res.json();
}

export const apiBaseUrl = API_BASE;

