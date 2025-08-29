/**
 * App verification flow tests
 * Mocks fetch to simulate search and verify endpoints.
 */
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import App from "../App.jsx";

// Simple fetch mock that inspects URL and returns canned responses
function mockFetch() {
  const original = global.fetch;
  const fn = vi.fn(async (url, opts = {}) => {
    const u = String(url);
    if (u.includes("/health")) {
      return new Response(JSON.stringify({ status: "ok" }), { status: 200 });
    }
    if (u.includes("/v1/verify/search")) {
      return new Response(
        JSON.stringify([
          { legal_name: "Acme Corp", address: { line1: "123", city: "X", country: "US" }, registration_status: "Active" },
        ]),
        { status: 200 }
      );
    }
    if (u.includes("/v1/verify")) {
      return new Response(
        JSON.stringify({
          legal_name: "Acme Corp",
          address: { line1: "123", city: "X", country: "US" },
          registration_status: "Active",
          status: "clear",
        }),
        { status: 200 }
      );
    }
    return new Response("not found", { status: 404 });
  });
  global.fetch = fn;
  return () => {
    global.fetch = original;
  };
}

describe("App verify flow", () => {
  let restore;
  beforeEach(() => {
    restore = mockFetch();
  });
  afterEach(() => restore());

  it("searches and verifies a candidate", async () => {
    render(<App />);

    // Fill search fields
    fireEvent.change(screen.getByPlaceholderText(/acme/i), { target: { value: "acme" } });
    fireEvent.click(screen.getByRole("button", { name: /search/i }));

    // Result appears
    await screen.findByText(/Acme Corp/);

    // Click Verify
    fireEvent.click(screen.getByRole("button", { name: /verify/i }));

    // Verify panel shows status
    await waitFor(() => expect(screen.getByText(/Verification Result/i)).toBeInTheDocument());
    expect(screen.getByText(/Status:/i)).toHaveTextContent("clear");
  });
});

