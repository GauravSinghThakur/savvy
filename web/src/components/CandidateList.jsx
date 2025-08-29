/**
 * CandidateList
 * Renders search results and exposes Verify action for each item or via row click.
 */
import React from "react";

export default function CandidateList({ items, onVerify, verifying }) {
  if (!items?.length) return <p>No results yet.</p>;
  return (
    <ul style={{ listStyle: "none", padding: 0 }}>
      {items.map((c) => (
        <li
          key={`${c.legal_name}-${c.address.country}`}
          style={{ marginBottom: 10, padding: 8, border: "1px solid #ddd", borderRadius: 4, cursor: "pointer" }}
          onClick={() => onVerify(c.legal_name, c.address.country)}
        >
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div>
              <strong>{c.legal_name}</strong> — {c.registration_status}
              <div style={{ color: "#555" }}>
                {c.address.line1}, {c.address.city}, {c.address.country}
              </div>
            </div>
            <button
              onClick={(e) => {
                e.stopPropagation();
                onVerify(c.legal_name, c.address.country);
              }}
              disabled={verifying}
            >
              {verifying ? "Verifying..." : "Verify"}
            </button>
          </div>
        </li>
      ))}
    </ul>
  );
}

