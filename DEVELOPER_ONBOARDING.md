# Developer Onboarding Guide

## Welcome to Arkival Development

This guide helps new developers and AI agents get up to speed quickly with the Arkival codebase.

## 📋 Pre-Requisites

- Python 3.7+
- Git
- Basic understanding of AI agent workflows

## 🚀 Quick Start

### 1. Validate System
```bash
python3 validate_deployment.py
```

### 2. Load Project Context
```bash
# Say "Hi" or run:
python3 codebase_summary/agent_workflow_orchestrator.py incoming
```

### 3. Understand Project Structure
- Review `AGENT_GUIDE.md` for system overview
- Check `CODEBASE_SUMMARY.md` for current state
- Read `documentation_assets/workflow_assets/workflow_docs/engineering_best_practices.md`

## 🛠 Development Workflow

### Session Start
1. Run incoming agent workflow
2. Review session context and unresolved issues
3. Check documentation coverage status

### During Development
1. Follow established patterns
2. Add breadcrumb documentation (`# @codebase-summary:`)
3. Test changes with `python3 codebase_summary/update_project_summary.py --force`

### Session End
1. Run outgoing agent workflow
2. Update changelog for significant changes
3. Verify system integrity

## 📁 Key Directories

- `codebase_summary/` - Core orchestration scripts
- `documentation_assets/` - Documentation and guides
- `modules/` - Additional functionality modules
- `export_package/` - Deployment artifacts

## 🔧 Common Commands

```bash
# Update project analysis
python3 codebase_summary/update_project_summary.py --force

# Add changelog entry
python3 codebase_summary/update_changelog.py add --summary "Description"

# Validate deployment
python3 validate_deployment.py

# Test language detection
ls codebase_summary/language_scan_tests/
```

## 🎯 Key Concepts

### Path Resolution
All scripts use `find_arkival_paths()` for deployment-aware file location.

### Three Deployment Modes
1. **Development Mode**: Working in source repo
2. **Subdirectory Mode**: Arkival cloned into existing project
3. **Nested Execution**: Running from codebase_summary directory

### Documentation Systems
- **Codebase Summary**: Frequent updates, function documentation
- **Changelog**: Infrequent updates, major milestones

## 📖 Additional Resources

- `SETUP_GUIDE.md` - Deployment instructions
- `DEPLOYMENT_GUIDE.md` - Detailed deployment scenarios
- `SCAN_IGNORE_DOCS.md` - Scanner configuration
- `documentation_assets/workflow_assets/workflow_docs/engineering_best_practices.md` - Best practices