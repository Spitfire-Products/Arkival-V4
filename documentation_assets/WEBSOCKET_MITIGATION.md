# WebSocket Promise Rejection Mitigation Guide

This guide explains how to implement WebSocket promise rejection mitigation in any project using the templates provided in this package.

## Problem Overview

Vite development servers create WebSocket connections for Hot Module Replacement (HMR) that can fail silently, causing unhandled promise rejections that clutter the console and may interfere with application functionality.

## Solution Components

### 1. Client-Side WebSocket Blocking

**File:** `client_templates/vite-client.js`

**Implementation Steps:**
1. Copy `vite-client.js` to your project's public directory or static assets folder
2. Include it in your HTML before any other scripts:
   ```html
   <script src="/vite-client.js"></script>
   ```

**For Vite Projects:**
- Place in `public/vite-client.js`
- Reference in `index.html`: `<script src="/vite-client.js"></script>`

**For Next.js Projects:**
- Place in `public/vite-client.js`
- Reference in `_document.js` or layout component

### 2. React Error Boundary Integration

**File:** `client_templates/main-template.tsx`

**Implementation Steps:**
1. Copy the error handling sections from `main-template.tsx`
2. Add to your main React entry point (typically `main.tsx`, `index.tsx`, or `App.tsx`)
3. Ensure the error handling code runs before `ReactDOM.createRoot()`

**Key Error Handling Patterns:**
```typescript
// Unhandled promise rejection prevention
window.addEventListener('unhandledrejection', (event) => {
  const error = event.reason;
  const errorMessage = error?.message || error?.toString() || '';
  
  const isViteWebSocketError = errorMessage.includes('WebSocket') ||
                              errorMessage.includes('HMR') ||
                              errorMessage.includes('connection') ||
                              error?.name === 'AbortError';

  if (isViteWebSocketError) {
    event.preventDefault();
    return false;
  }
});
```

## Framework-Specific Implementation

### React + Vite
1. Add WebSocket blocking script to `index.html`
2. Integrate error handling in `main.tsx`
3. Verify HMR still works for development

### React + Next.js
1. Add WebSocket blocking to `public/` directory
2. Include in `_document.js` or root layout
3. Add error boundaries to main app component

### Vue + Vite
1. Add WebSocket blocking script to `index.html`
2. Integrate error handling in `main.js` or `main.ts`
3. Use Vue's global error handler for additional coverage

### Svelte + Vite
1. Add WebSocket blocking script to `app.html`
2. Integrate error handling in main application file
3. Use Svelte's error boundary patterns

## Verification Steps

1. **Check Console:** WebSocket blocking message should appear
2. **Test HMR:** Hot reload should still work for development
3. **Monitor Errors:** No unhandled promise rejections in console
4. **Production Build:** Ensure blocking doesn't affect production builds

## Troubleshooting

### Common Issues

**HMR Not Working:**
- Ensure WebSocket blocking only targets HMR connections
- Check port numbers in blocking logic
- Verify development server configuration

**Error Handling Too Aggressive:**
- Refine error message filtering
- Add specific error type checks
- Ensure legitimate errors still surface

**Production Interference:**
- WebSocket blocking should not affect production
- Remove or conditionally load blocking script for production
- Use environment variables to control behavior

### Environment-Specific Configuration

**Development Only:**
```javascript
if (import.meta.env.DEV) {
  // WebSocket blocking code here
}
```

**Conditional Loading:**
```html
<!-- Only load in development -->
<script>
  if (location.hostname === 'localhost') {
    const script = document.createElement('script');
    script.src = '/vite-client.js';
    document.head.appendChild(script);
  }
</script>
```

## Best Practices

1. **Environment Awareness:** Only apply blocking in development
2. **Selective Blocking:** Target specific WebSocket patterns
3. **Error Preservation:** Don't suppress legitimate application errors
4. **Testing:** Verify both development and production functionality
5. **Documentation:** Document any project-specific modifications

## Integration with Workflow System

This mitigation system integrates with the broader workflow orchestration:
- Automatic detection of WebSocket issues in system status checks
- Documentation generation includes WebSocket configuration
- Version tracking includes mitigation system updates
- Agent handoff documentation covers WebSocket status

## Advanced Configuration

### Custom WebSocket Patterns
Modify the blocking logic to match your specific development setup:

```javascript
const isViteWebSocketError = url.includes('your-custom-port') ||
                            url.includes('your-hmr-path') ||
                            url.includes('your-ws-prefix');
```

### Error Reporting Integration
Integrate with error reporting services while maintaining blocking:

```javascript
if (isViteWebSocketError) {
  // Log to development console only
  console.debug('Blocked WebSocket connection:', url);
  event.preventDefault();
  return false;
} else {
  // Report legitimate errors to error service
  errorReportingService.captureException(error);
}
```

This mitigation system provides comprehensive WebSocket promise rejection prevention while maintaining development functionality and production compatibility.