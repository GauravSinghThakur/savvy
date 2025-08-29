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
// Components for clearer separation of concerns
import SearchForm from "./components/SearchForm.jsx";
import CandidateList from "./components/CandidateList.jsx";
import VerifyResult from "./components/VerifyResult.jsx";
import Toast from "./components/Toast.jsx";
// API helpers centralize backend calls and improve testability
import { apiBaseUrl as API_BASE, getHealth, searchCandidates, verifyEntity } from "./utils/api.js";

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
      const json = await getHealth();
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
      const json = await searchCandidates(q, country);
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
      const json = await verifyEntity(name, countryCode);
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
      <Toast message={error} onClose={() => setError(null)} />

      <hr style={{ margin: "24px 0" }} />

      {/* Simple search form: enter partial name and optional country code */}
      <section>
        <h2>Search Candidates</h2>
        <SearchForm
          initialQ={q}
          initialCountry={country}
          busy={false}
          onSearch={({ q: nq, country: nc }) => {
            setQ(nq);
            setCountry(nc || "");
            runSearch();
          }}
        />

        <CandidateList items={results} onVerify={verifyCandidate} verifying={verifying} />

        <VerifyResult result={verifyResult} onClear={() => setVerifyResult(null)} />
      </section>
    </main>
  );
}
