/**
 * SearchForm tests
 * Verifies enable/disable logic and submit callback behavior.
 */
import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import SearchForm from "../components/SearchForm.jsx";

describe("SearchForm", () => {
  it("disables Search for short queries", () => {
    const onSearch = vi.fn();
    render(<SearchForm onSearch={onSearch} />);
    const btn = screen.getByRole("button", { name: /search/i });
    expect(btn).toBeDisabled();
  });

  it("calls onSearch with normalized inputs", () => {
    const onSearch = vi.fn();
    render(<SearchForm onSearch={onSearch} />);
    fireEvent.change(screen.getByPlaceholderText(/acme/i), { target: { value: "  ac  me  " } });
    fireEvent.change(screen.getByPlaceholderText(/us/i), { target: { value: "us" } });
    fireEvent.click(screen.getByRole("button", { name: /search/i }));
    expect(onSearch).toHaveBeenCalled();
    const arg = onSearch.mock.calls[0][0];
    expect(arg.q).toBe("ac  me");
    expect(arg.country).toBe("US");
  });
});

