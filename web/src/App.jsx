/**
 * Minimal Investigator Dashboard placeholder.
 *
 * Responsibilities:
 * - Show a simple UI with a health check button.
 * - Provide a basic search form that calls /v1/verify/search.
 * - Fetch the backend /health endpoint using VITE_API_BASE_URL.
 * - Document how environment config is expected to work.
 */
import React, { useState } from "react";

// Read the backend base URL from Vite environment variables
// Example: VITE_API_BASE_URL=http://localhost:8000
const API_BASE = import.meta?.env?.VITE_API_BASE_URL || "http://localhost:8000";

export default function App() {
  const [status, setStatus] = useState("unknown");
  const [error, setError] = useState(null);
  const [q, setQ] = useState("");
  const [country, setCountry] = useState("");
 const [results, setResults] = useState([]);
  const [verifying, setVerifying] = useState(false);
  const [verifyResult, setVerifyResult] = useState(null);

  async function checkHealth() {
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/health`);
      const json = await res.json();
      setStatus(json.status || "unknown");
    } catch (e) {
      setError(String(e));
      setStatus("error");
    }
  }

  async function runSearch() {
    // Clear any previous errors before fetching
    setError(null);
    setResults([]);
    try {
      const params = new URLSearchParams();
      params.set("q", q);
      if (country) params.set("country", country);
      const res = await fetch(`${API_BASE}/v1/verify/search?${params.toString()}`);
      if (!res.ok) {
        throw new Error(`Search failed (${res.status})`);
      }
      const json = await res.json();
      setResults(json);
      setVerifyResult(null); // clear any previous verification output
    } catch (e) {
      setError(String(e));
    }
  }

  async function verifyCandidate(name, countryCode) {
    // POST to /v1/verify with selected candidate name and country
    setError(null);
    setVerifying(true);
    setVerifyResult(null);
    try {
      const res = await fetch(`${API_BASE}/v1/verify`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, country: countryCode })
      });
      if (!res.ok) {
        throw new Error(`Verify failed (${res.status})`);
      }
      const json = await res.json();
      setVerifyResult(json);
    } catch (e) {
      setError(String(e));
    } finally {
      setVerifying(false);
    }
  }

  return (
    <main style={{ fontFamily: "system-ui, sans-serif", padding: 24 }}>
      <h1>Savvy – Investigator Dashboard (Placeholder)</h1>
      <p>
        Backend URL: <code>{API_BASE}</code>
      </p>
      <button onClick={checkHealth}>Check API Health</button>
      <p>
        Status: <strong>{status}</strong>
      </p>
      {error && (
        <pre style={{ color: "crimson", whiteSpace: "pre-wrap" }}>{error}</pre>
      )}

      <hr style={{ margin: "24px 0" }} />

      {/* Simple search form: enter partial name and optional country code */}
      <section>
        <h2>Search Candidates</h2>
        <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
          <label>
            Name contains:
            <input
              type="text"
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="acme"
              style={{ marginLeft: 8 }}
            />
          </label>
          <label>
            Country (ISO2):
            <input
              type="text"
              value={country}
              onChange={(e) => setCountry(e.target.value.toUpperCase())}
              placeholder="US"
              maxLength={2}
              style={{ marginLeft: 8, width: 56 }}
            />
          </label>
          <button onClick={runSearch} disabled={q.trim().length < 2}>
            Search
          </button>
        </div>

        {/* Results list */}
        <ul>
          {results.map((c) => (
            <li key={`${c.legal_name}-${c.address.country}`} style={{ marginBottom: 8 }}>
              <strong>{c.legal_name}</strong> — {c.registration_status}
              <div style={{ color: "#555" }}>
                {c.address.line1}, {c.address.city}, {c.address.country}
              </div>
              <button
                style={{ marginTop: 6 }}
                onClick={() => verifyCandidate(c.legal_name, c.address.country)}
                disabled={verifying}
              >
                {verifying ? "Verifying..." : "Verify"}
              </button>
            </li>
          ))}
        </ul>

        {/* Verification result panel */}
        {verifyResult && (
          <section style={{ marginTop: 16 }}>
            <h3>Verification Result</h3>
            <div>
              <strong>{verifyResult.legal_name}</strong> — {verifyResult.registration_status}
            </div>
            <div style={{ color: "#555" }}>
              {verifyResult.address.line1}, {verifyResult.address.city}, {verifyResult.address.country}
            </div>
            <div style={{ marginTop: 6 }}>
              Status: <strong>{verifyResult.status}</strong>
            </div>
            {Array.isArray(verifyResult.risk_flags) && verifyResult.risk_flags.length > 0 && (
              <div style={{ marginTop: 6 }}>
                Risk Flags: {verifyResult.risk_flags.join(", ")}
              </div>
            )}
            <button style={{ marginTop: 8 }} onClick={() => setVerifyResult(null)}>Clear</button>
          </section>
        )}
      </section>
    </main>
  );
}
