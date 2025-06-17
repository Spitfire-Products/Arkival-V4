# Breadcrumb Implementation Guide

**NOTICE:** This is the authoritative breadcrumb documentation for the workflow export package.

## Standard Format

All breadcrumbs follow this pattern:
```
@codebase-summary: feature="feature_name" purpose="brief_description" description="detailed_explanation"
```

## Language-Specific Implementations

### JavaScript/TypeScript/JSX/TSX

**Single-line comments:**
```javascript
// @codebase-summary: feature="ui_components" purpose="Main dashboard display"
// @codebase-summary: description="Renders interactive workflow dashboard with status indicators"
function WorkflowDashboard() {
  // Implementation
}
```

**Multi-line comments:**
```javascript
/* @codebase-summary: feature="api_endpoints" purpose="User authentication API"
   @codebase-summary: description="Handles login, logout, and session management" */
export async function authenticateUser(credentials) {
  // Implementation
}
```

**JSDoc style:**
```javascript
/** @codebase-summary: feature="data_processing" purpose="Workflow data validation"
 *  @codebase-summary: description="Validates and sanitizes workflow configuration input" */
function validateWorkflowData(workflowData) {
  // Implementation
}
```

### Python

**Single-line comments:**
```python
# @codebase-summary: feature="data_processing" purpose="Session metadata processor"
# @codebase-summary: description="Validates and transforms session data for storage"
def process_session_metadata(metadata: dict) -> dict:
    """Process session metadata"""
    # Implementation
```

**Docstring format:**
```python
def generate_workflow_summary(session_data):
    """ @codebase-summary: feature="ai_integration" purpose="AI-powered summary generation"
        @codebase-summary: description="Uses AI to create comprehensive workflow summaries"
    """
    # Implementation
```

### Rust

**Documentation comments:**
```rust
/// @codebase-summary: feature="performance" purpose="High-speed data processing"
/// @codebase-summary: description="Optimized workflow state processing engine"
pub fn process_workflow_state(state_data: &StateData) -> Result<ProcessedState, ProcessError> {
    // Implementation
}
```

**Attribute style:**
```rust
#[ @codebase-summary: feature="database" purpose="Session storage schema"
   @codebase-summary: description="Defines database structure for workflow session storage" ]
pub struct SessionData {
    // Fields
}
```

**Block comments:**
```rust
/* @codebase-summary: feature="async_processing" purpose="Async workflow execution"
   @codebase-summary: description="Handles concurrent workflow task processing" */
async fn process_tasks_concurrent(tasks: Vec<TaskData>) {
    // Implementation
}
```

### Go

**Single-line comments:**
```go
// @codebase-summary: feature="api_server" purpose="HTTP server configuration"
// @codebase-summary: description="Sets up REST API endpoints for workflow operations"
func SetupServer() *gin.Engine {
    // Implementation
}
```

**Multi-line comments:**
```go
/* @codebase-summary: feature="data_processing" purpose="Data transformation utilities"
   @codebase-summary: description="Provides workflow data processing and formatting functions" */
func ProcessWorkflowData(data WorkflowData) WorkflowData {
    // Implementation
}
```

### Java/Kotlin

**Single-line comments:**
```java
// @codebase-summary: feature="session_management" purpose="Session data model"
// @codebase-summary: description="Represents workflow session with state tracking"
public class WorkflowSession {
    // Implementation
}
```

**JavaDoc style:**
```java
/** @codebase-summary: feature="workflow_engine" purpose="Workflow progression manager"
 *  @codebase-summary: description="Handles workflow states and task orchestration" */
public class WorkflowManager {
    // Implementation
}
```

### C/C++

**Single-line comments:**
```cpp
// @codebase-summary: feature="processing_engine" purpose="High-performance data processor"
// @codebase-summary: description="Optimized data processing engine for workflow operations"
void ProcessWorkflowData(const DataSet& data) {
    // Implementation
}
```

**Multi-line comments:**
```cpp
/* @codebase-summary: feature="memory_management" purpose="Efficient data caching"
   @codebase-summary: description="Manages memory allocation for workflow data structures" */
class DataCache {
    // Implementation
};
```

### Swift

**Single-line comments:**
```swift
// @codebase-summary: feature="mobile_ui" purpose="iOS workflow interface"
// @codebase-summary: description="Native iOS interface for workflow management and monitoring"
class WorkflowViewController: UIViewController {
    // Implementation
}
```

### Ruby

**Single-line comments:**
```ruby
# @codebase-summary: feature="data_extraction" purpose="Configuration data extraction"
# @codebase-summary: description="Extracts metadata from workflow configuration files"
def extract_config_data(config_path)
  # Implementation
end
```

**Block comments:**
```ruby
=begin @codebase-summary: feature="background_jobs" purpose="Async workflow processing"
       @codebase-summary: description="Background job system for heavy workflow operations"
=end
class WorkflowProcessingJob
  # Implementation
end
```

### SQL/PostgreSQL

**Single-line comments:**
```sql
-- @codebase-summary: feature="database_schema" purpose="Workflow sessions table"
-- @codebase-summary: description="Stores workflow session metadata and state"
CREATE TABLE workflow_sessions (
    id SERIAL PRIMARY KEY,
    session_name VARCHAR(255) NOT NULL
);
```

**Multi-line comments:**
```sql
/* @codebase-summary: feature="database_functions" purpose="Session search functionality"
   @codebase-summary: description="Full-text search across workflow session data" */
CREATE OR REPLACE FUNCTION search_sessions(search_term TEXT)
RETURNS TABLE(session_id INT, session_name TEXT) AS $$
-- Implementation
$$ LANGUAGE plpgsql;
```

### HTML/XML

**HTML comments:**
```html
<!-- @codebase-summary: feature="responsive_ui" purpose="Workflow dashboard layout"
     @codebase-summary: description="Responsive HTML structure for workflow status display" -->
<div class="workflow-dashboard-container">
    <!-- Content -->
</div>
```

### CSS/SCSS

**CSS comments:**
```css
/* @codebase-summary: feature="visual_design" purpose="Workflow status styling"
   @codebase-summary: description="Defines visual appearance of workflow status indicators" */
.workflow-status {
    /* Styles */
}
```

### YAML

**YAML comments:**
```yaml
# @codebase-summary: feature="deployment_config" purpose="Production deployment settings"
# @codebase-summary: description="Kubernetes configuration for workflow system deployment"
apiVersion: apps/v1
kind: Deployment
metadata:
  name: workflow-system
```

### Shell Scripts

**Shell comments:**
```bash
#!/bin/bash
# @codebase-summary: feature="build_automation" purpose="Workflow system build script"
# @codebase-summary: description="Automated build and deployment pipeline for workflow orchestrator"

build_workflow_system() {
    # Implementation
}
```

### Markdown

**Markdown comments:**
```markdown
<!-- @codebase-summary: feature="documentation" purpose="API documentation"
     @codebase-summary: description="Complete API reference for workflow management endpoints" -->

# Workflow Management API

Documentation content here...
```

## Advanced Patterns

### Flow Documentation

For multi-step processes, use the `flow` and `stage` attributes:

```python
# @codebase-summary: feature="workflow_execution" flow="session_handoff" stage="1"
# @codebase-summary: purpose="Initialize session handoff process"
# @codebase-summary: description="Sets up initial data structures and validates session state"
def initialize_session_handoff(session_data):
    # Implementation
```

### Relationship Documentation

Document code relationships using `dependencies` and `called_by`:

```javascript
// @codebase-summary: feature="ai_integration" purpose="Session context manager"
// @codebase-summary: description="Maintains consistency across workflow session transitions"
// @codebase-summary: dependencies="ai-service, session-database"
// @codebase-summary: called_by="workflow-orchestrator, session-manager"
function maintainSessionConsistency(sessionData) {
    // Implementation
}
```

## Validation

Both the main application and export package scripts validate breadcrumbs using these patterns. The scripts generate:

- `CODEBASE_SUMMARY.md` - Comprehensive project documentation
- `missing_breadcrumbs.json` - Functions lacking proper documentation
- Coverage reports showing documentation completeness

## Best Practices

1. **Always add breadcrumbs** to new functions, classes, and significant code blocks
2. **Use consistent feature names** across related functionality
3. **Keep descriptions concise** but informative
4. **Document relationships** between components
5. **Use flow documentation** for multi-step processes
6. **Run validation scripts** after adding new code

## Supported File Extensions

The breadcrumb system actively scans these file types:

- **Code:** `.py`, `.js`, `.ts`, `.tsx`, `.jsx`, `.rs`, `.go`, `.java`, `.cpp`, `.c`, `.h`, `.swift`, `.kt`, `.rb`, `.php`
- **Web:** `.html`, `.css`, `.scss`, `.sass`, `.vue`
- **Data:** `.json`, `.yaml`, `.yml`, `.toml`, `.sql`
- **Documentation:** `.md`, `.txt`, `.rst`
- **Configuration:** `.sh`, `.bat`, `.ps1`

This comprehensive approach ensures consistent documentation across all project components, enabling better AI assistance and developer onboarding.