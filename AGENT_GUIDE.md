# Arkival Agent Guide

## System Overview

Arkival is a complete AI Agent Workflow Orchestration System with comprehensive multi-language function detection capabilities. The system enables seamless knowledge transfer between AI agents and human developers across different development environments.

## Quick Start for New Agents

### 1. Validate System
**Verify the complete Arkival system:**
```bash
python3 validate_deployment.py
```

### 2. Test Multi-Language Detection
**Validate function detection capability:**
```bash
python3 codebase_summary/update_project_summary.py --force
```

### 3. Understand Documentation Systems
**Two independent systems serve different purposes:**

**Codebase Summary (Run Often):**
- Updates function documentation and breadcrumb coverage
- Independent of project versions
- Run frequently during development
- Tracks technical implementation details

**Changelog (Run Infrequently):**
- Documents major changes and milestones  
- Version controlled project evolution
- Run for significant features or agent handoffs
- Tracks user-facing changes

### 4. Load Previous Context
**Start with incoming workflow:**
```bash
python3 codebase_summary/agent_workflow_orchestrator.py incoming
```

## What to Expect

### Function Detection Output
The multi-language detection system will show:
- Function detection across all project files 
- Python files (test + main Arkival system files combined)
- Multiple language test files validating detection capability
- 100% documentation coverage with breadcrumb system

### Language Test Coverage
Comprehensive test files validate detection across:
- Python, JavaScript, TypeScript, Rust, Go, Java
- C++, C, PHP, Ruby, Swift, Kotlin, Dart
- CSS, SQL, Vue templates
- All located in `codebase_summary/language_scan_tests/`

## Configuration Guidelines

### Project Analysis
When starting with a new project:
```bash
python3 codebase_summary/agent_workflow_orchestrator.py incoming
```

### Update Project Configuration
Edit `workflow_config.json` to match your project:
- Set correct `project_name`
- Update `technology_stack` array
- Configure `main_files` and `important_directories`

### Enhanced Features
- `architecture_diagrams`: Generate system diagrams
- `ai_integration_detection`: Detect AI service usage
- `breadcrumb_enforcement`: Require documentation comments

### Workflow Settings
- `auto_changelog`: Automatic version tracking
- `agent_handoff_enabled`: Enable session handoffs
- `version_correlation`: Synchronize component versions

## Workflow Integration

### Incoming Agent Workflow
- Loads previous session context
- Reviews unresolved issues
- Updates project summary

### Outgoing Agent Workflow  
- Documents session progress
- Updates changelog
- Prepares handoff notes

### Session Management
1. Start sessions with "Hi" or incoming workflow
2. Maintain real-time documentation
3. End with changelog updates and outgoing workflow

## Documentation Standards

Use breadcrumb format in all code:
```python
def example_function():
    """
    # @codebase-summary: Brief description of function purpose
    - What it does and how it's used
    - Integration points and dependencies
    - Used by: other components that call this
    """
```

## Cross-Platform Compatibility

- Use relative paths only
- Test across multiple IDE environments
- Maintain Python 3.7+ compatibility

## Troubleshooting

### Common Issues
- Missing breadcrumb documentation
- Incorrect file paths
- Version synchronization problems

### Validation Commands
```bash
# Run multi-language function detection
python3 codebase_summary/update_project_summary.py --force

# Deployment validation
python3 validate_deployment.py
```

## IDE Integration Examples

### VS Code Integration
The system creates `.vscode/tasks.json` with workflow commands.

### Replit Integration  
Uses native workflows for agent handoff automation.

### Generic IDE Integration
Falls back to shell scripts for universal compatibility.

## Technology Stack Detection

The AI agent should identify and configure:
- **Frontend Framework** (React, Vue, Svelte, etc.)
- **Backend Technology** (Node.js, Express, FastAPI, etc.)
- **Build Tools** (Vite, Webpack, etc.)
- **Special Integrations** (Three.js, SpacetimeDB, etc.)

## Project-Specific File Detection

The AI agent should populate:
```json
{
  "project_specific": {
    "main_files": ["vite.config.ts", "src/main.tsx", "package.json"],
    "important_directories": ["src", "public", "components"],
    "integration_notes": {
      "build_system": "Vite with TypeScript",
      "development_flow": "Vite dev server → Production build"
    }
  }
}
```