/**
 * # @codebase-summary: Custom Vite client for WebSocket promise rejection mitigation
 * - Replaces default Vite HMR client to eliminate WebSocket connection promise rejections
 * - Blocks problematic WebSocket connections while preserving other WebSocket functionality
 * - Used by: development environment setup, promise rejection prevention, HMR optimization
 */
// Custom Vite client that disables WebSocket connections
// This replaces the default Vite HMR client to eliminate promise rejections
// DEPLOYMENT INSTRUCTIONS: Copy this file to your client/public/ directory or appropriate static assets folder

// Override the default WebSocket creation
const originalWebSocket = window.WebSocket;
window.WebSocket = function(url, protocols) {
  /**
   * # @codebase-summary: WebSocket connection filtering and blocking system
   * - Identifies and blocks Vite HMR WebSocket connections that cause promise rejections
   * - Returns mock WebSocket objects for blocked connections to prevent errors
   * - Preserves legitimate WebSocket functionality for application features
   * - Used by: development environment, HMR system optimization, error prevention
   */
  // Block all Vite HMR WebSocket connections
  if (url && (url.includes('ws://') || url.includes('wss://')) && 
      (url.includes('24678') || url.includes('vite') || url.includes('hmr'))) {
    console.log('[Custom Vite Client] Blocking WebSocket connection to prevent promise rejections:', url);
    
    // Return a mock WebSocket that doesn't actually connect
    return {
      close: () => {},
      send: () => {},
      addEventListener: () => {},
      removeEventListener: () => {},
      readyState: 3, // CLOSED
      CONNECTING: 0,
      OPEN: 1,
      CLOSING: 2,
      CLOSED: 3
    };
  }
  
  // Allow other WebSocket connections
  return new originalWebSocket(url, protocols);
};

// Disable Vite's HMR client entirely
if (window.__vite_plugin_react_preamble_installed__) {
  delete window.__vite_plugin_react_preamble_installed__;
}

// Override any existing HMR functions
window.__vite__ = {
  injectQuery: (url) => url,
  reload: () => window.location.reload(),
  createHotContext: () => ({
    accept: () => {},
    dispose: () => {},
    decline: () => {},
    invalidate: () => {},
    on: () => {},
    off: () => {},
    send: () => {}
  })
};

console.log('[Custom Vite Client] WebSocket blocking enabled - promise rejections eliminated');