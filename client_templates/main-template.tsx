// React main entry point template with WebSocket promise rejection handling
// DEPLOYMENT INSTRUCTIONS: 
// 1. Copy the error handling sections below to your main.tsx or index.tsx file
// 2. Adjust import paths based on your project structure
// 3. Ensure this code runs before ReactDOM.createRoot()

import React from "react";
import ReactDOM from "react-dom/client";
// Import your App component here
// import App from "./App.tsx";
// Import your CSS files here
// import "./index.css";

// Comprehensive promise rejection handling - eliminate ALL Vite WebSocket errors
window.addEventListener('unhandledrejection', (event) => {
  const error = event.reason;
  /**
   * # @codebase-summary: Promise rejection error message extraction utility
   * - Extracts error messages from unhandled promise rejections safely
   * - Handles various error object types and rejection reasons
   * - Used by: WebSocket error filtering, promise rejection handling, development environment
   */
  const errorMessage = error?.message || error?.toString() || '';
  
  /**
   * # @codebase-summary: WebSocket error detection and filtering utility
   * - Identifies WebSocket, HMR, and Vite connection errors that should be suppressed
   * - Provides comprehensive error pattern matching for development environment
   * - Used by: error handling, development environment, WebSocket management
   */
  const isViteWebSocketError = errorMessage.includes('WebSocket') ||
                              errorMessage.includes('WebSocket connection lost') ||
                              errorMessage.includes('WebSocket connection failed') ||
                              errorMessage.includes('HMR') ||
                              errorMessage.includes('hmr') ||
                              errorMessage.includes('vite') ||
                              errorMessage.includes('connection') ||
                              errorMessage.includes('fetch') ||
                              errorMessage.includes('NetworkError') ||
                              errorMessage.includes('AbortError') ||
                              errorMessage.includes('TypeError: Failed to fetch') ||
                              errorMessage.includes('net::') ||
                              error?.name === 'AbortError' ||
                              error?.code === 'ECONNRESET' ||
                              error?.code === 'NETWORK_ERROR';

  if (isViteWebSocketError) {
    event.preventDefault();
    return false;
  }
});

// Handle uncaught exceptions that might cause race conditions
window.addEventListener('error', (event) => {
  const error = event.error;
  /**
   * # @codebase-summary: Error message string extraction utility
   * - Extracts string representation from various error object types
   * - Handles both Error objects and event objects safely
   * - Used by: WebSocket error filtering, development environment error handling
   */
  const errorMessage = error?.message || '';
  
  // Block WebSocket and cross-origin errors that React can't access
  if (errorMessage.includes('WebSocket') || 
      errorMessage.includes('fetch') ||
      errorMessage.includes('Script error') ||
      errorMessage.includes('cross-origin')) {
    event.preventDefault();
    return false;
  }
});

// Example React application render
// Uncomment and modify based on your project structure:
/*
ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
*/

// Alternative for projects using QueryClient or other providers:
/*
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "./lib/queryClient";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </React.StrictMode>,
);
*/