/**
 * VerifyResult
 * Shows the outcome of a verification request with a clear layout.
 */
import React from "react";

export default function VerifyResult({ result, onClear }) {
  if (!result) return null;
  return (
    <section style={{ marginTop: 16 }}>
      <h3>Verification Result</h3>
      <div>
        <strong>{result.legal_name}</strong> — {result.registration_status}
      </div>
      <div style={{ color: "#555" }}>
        {result.address.line1}, {result.address.city}, {result.address.country}
      </div>
      <div style={{ marginTop: 6 }}>
        Status: <strong>{result.status}</strong>
      </div>
      {Array.isArray(result.risk_flags) && result.risk_flags.length > 0 && (
        <div style={{ marginTop: 6 }}>
          Risk Flags: {result.risk_flags.join(", ")}
        </div>
      )}
      <button style={{ marginTop: 8 }} onClick={onClear}>Clear</button>
    </section>
  );
}

