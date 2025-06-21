# Arkival Agent Guide

## System Overview

Arkival is a complete AI Agent Workflow Orchestration System with comprehensive multi-language function detection capabilities. The system enables seamless knowledge transfer between AI agents and human developers across different development environments.

## 🚀 Quick Start for Agents

### 1. Load Project Context
```bash
# Essential first step - loads current project state
python3 codebase_summary/update_project_summary.py
```

### 2. Read Critical Context
- **`codebase_summary.json`** - Current project analysis with `_critical_context` section
- **`ARCHITECTURE_DIAGRAM.md`** - Visual project overview with decision trees
- **`modules/claude-code/CLAUDE.md`** - Claude integration guide (if using Claude module)

### 3. Agent Workflow Commands
```bash
# Load context when starting work
python3 codebase_summary/agent_workflow_orchestrator.py incoming

# Save context when finishing work  
python3 codebase_summary/agent_workflow_orchestrator.py outgoing
```

## 🏗 Deployment Modes (Auto-Detected)

**Subdirectory Mode**: When Arkival is cloned into an existing project
- Files generated in `/Arkival-V4/` subdirectory
- Only `arkival_config.json` added to project root
- Generated documentation reflects **host project**

**Development Mode**: When Arkival is the main project
- Files generated in root and `codebase_summary/` directories
- Generated documentation reflects **Arkival itself**

**Smart Path Resolution**: All scripts use `find_arkival_paths()` to automatically determine correct file locations based on deployment context.

## 📊 Key Capabilities

### Multi-Language Function Detection
Supports comprehensive analysis across:
- **Python** (.py) - Functions, classes, methods with docstring detection
- **JavaScript/TypeScript** (.js, .jsx, .ts, .tsx) - Functions, arrow functions, classes
- **And 15+ other languages** - See codebase_summary.json for complete list

### Documentation Breadcrumb System
Functions are documented with `@codebase-summary:` breadcrumbs:
```python
def example_function():
    """
    # @codebase-summary: Function purpose description
    - Detailed explanation of functionality
    - Usage context and integration notes
    """
```

### Version Independence
- **Codebase Version**: Auto-increments with each analysis run (1.1.x)
- **Changelog Version**: Manual milestone tracking (independent)
- **These are SEPARATE systems** - version mismatch is normal

## 🎯 Agent Workflow Integration

### Session State Management
- **`session_state.json`** - Tracks current session context
- **`agent_handoff.json`** - Agent transition documentation
- **Automatic handoff preparation** on session completion

### Project Analysis
- **94.57% documentation coverage** with breadcrumb system
- **Real-time metrics** updated with each analysis run
- **Architecture diagrams** auto-generated from codebase structure

## 🛠 Development Context

### Prerequisites
- Python 3.7+
- Git
- Understanding of AI agent workflow patterns

### Validation
```bash
# Validate system integrity
python3 validate_deployment.py

# Check export readiness
python3 validate_export_readiness.py
```

### Key Patterns
- **Always run `update_project_summary.py`** before starting work
- **Use agent workflow orchestrator** for session management
- **Check `_critical_context`** in codebase_summary.json for current state
- **Follow breadcrumb documentation** patterns for new functions

## 📁 Critical File Locations

### Configuration
- `arkival_config.json` - System configuration (parent dir in subdirectory mode)
- `workflow_config.json` - Workflow system settings

### Analysis & Documentation  
- `codebase_summary.json` - Complete project analysis
- `missing_breadcrumbs.json` - Documentation coverage tracking
- `ARCHITECTURE_DIAGRAM.md` - Auto-generated visual overview

### Agent Handoff
- `codebase_summary/session_state.json` - Current session tracking
- `export_package/agent_handoff.json` - Transition documentation

## 🎯 Best Practices

1. **Start every session** with `update_project_summary.py`
2. **Check deployment mode** via `_critical_context.deployment_mode`
3. **Use agent orchestrator** for proper session management
4. **Document functions** with `@codebase-summary:` breadcrumbs
5. **Verify system state** before major changes

## 🔄 Agent Transition Workflow

1. **Incoming Agent**: Run `incoming` workflow to load context
2. **During Work**: Use `update_project_summary.py` to refresh analysis
3. **Outgoing Agent**: Run `outgoing` workflow to save session state
4. **Context Preserved**: Next agent gets comprehensive handoff documentation

The system is optimized for seamless AI agent collaboration with comprehensive context management and automatic documentation generation.