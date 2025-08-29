/**
 * React application entrypoint.
 * - Creates the root and renders <App/>
 * - Kept minimal to mirror Vite’s default structure.
 */
import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx";

const container = document.getElementById("root");
const root = createRoot(container);
root.render(<App />);

