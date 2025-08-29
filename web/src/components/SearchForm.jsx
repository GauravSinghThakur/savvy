/**
 * SearchForm
 * Collects partial name and optional country code; calls onSearch when submitted.
 */
import React, { useState, useEffect } from "react";

export default function SearchForm({ initialQ = "", initialCountry = "", onSearch, busy }) {
  const [q, setQ] = useState(initialQ);
  const [country, setCountry] = useState(initialCountry);

  // Keep inputs in sync with parent props if they change
  useEffect(() => setQ(initialQ), [initialQ]);
  useEffect(() => setCountry(initialCountry), [initialCountry]);

  function submit(e) {
    e.preventDefault();
    if (q.trim().length >= 2) onSearch({ q: q.trim(), country: country.trim().toUpperCase() || undefined });
  }

  return (
    <form onSubmit={submit} style={{ display: "flex", gap: 8, alignItems: "center" }}>
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
      <button type="submit" disabled={busy || q.trim().length < 2}>
        {busy ? "Searching..." : "Search"}
      </button>
    </form>
  );
}

