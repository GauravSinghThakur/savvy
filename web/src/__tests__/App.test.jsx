/**
 * App component smoke test using Vitest + React Testing Library.
 * Ensures the page renders and a button exists.
 */
import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import App from "../App.jsx";

describe("App", () => {
  it("renders health check button", () => {
    render(<App />);
    expect(
      screen.getByRole("button", { name: /check api health/i })
    ).toBeInTheDocument();
  });
});

