# Testing Arkival in the Source Repository

## Overview
The Arkival source repository is configured to prevent generating configuration and state files that would be committed to GitHub. This document explains how to test Arkival functionality while developing in the source repo.

## Source Repository Protection
When running in the source repository (detected by absence of `arkival_config.json`), the following operations are skipped:
- Codebase summary generation
- File generation that would create tracked files
- Setup operations that modify the repository structure

## Testing Approaches

### 1. Deploy to Test Project (Recommended)
The best way to test Arkival is to deploy it to a separate test project:

```bash
# Create a test project
mkdir ~/test-project
cd ~/test-project

# Clone Arkival as subdirectory
git clone https://github.com/Arkival/Arkival-V4.git Arkival

# Run setup
python Arkival/setup.py subdirectory

# Test the workflows
python Arkival/codebase_summary/agent_workflow_orchestrator.py incoming
```

### 2. Manual Testing
For testing specific functions without full deployment:
- Use Python REPL to test individual functions
- Create temporary test directories outside the source repo
- Use environment variables to override path detection

### 3. Unit Testing
Consider adding unit tests that:
- Mock file system operations
- Test path resolution logic
- Verify workflow behavior in different deployment modes

## Files Already in .gitignore
The following generated files are properly excluded from git:
- `codebase_summary.json`
- `changelog_summary.json`
- `codebase_summary/session_state.json`
- `codebase_summary/agent_handoff.json`
- `codebase_summary/missing_breadcrumbs.json`
- `export_package/agent_handoff.json`
- `codebase_summary/history/`
- `Arkival/data/`

## Development Workflow
1. Make changes in the source repository
2. Test in a separate project using subdirectory deployment
3. Verify functionality works in both deployment modes
4. Commit only source code changes, not generated files

## Important Notes
- The source repository should remain clean of generated files
- All testing that generates files should be done in separate test projects
- The `.gitignore` is configured to exclude all generated files
- When the incoming/outgoing workflows detect source repo, they skip file generation