/**
 * Toast component
 * Displays a dismissible error or info message.
 */
import React from "react";

export default function Toast({ message, onClose }) {
  if (!message) return null;
  return (
    <div
      role="alert"
      style={{
        background: "#fee",
        border: "1px solid #f99",
        padding: 12,
        margin: "12px 0",
        color: "#600",
        borderRadius: 4,
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <span>{message}</span>
        <button aria-label="Dismiss message" onClick={onClose}>
          ×
        </button>
      </div>
    </div>
  );
}

