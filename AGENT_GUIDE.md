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
- **`codebase_summary/session_state.json`** - Previous agent tasks and handoff context
- **`ARCHITECTURE_DIAGRAM.md`** - Visual project overview with decision trees
- **`modules/claude-code/CLAUDE.md`** - Claude integration guide (if using Claude module)

### 3. Agent Workflow Commands
```bash
# Load context when starting work
python3 codebase_summary/agent_workflow_orchestrator.py incoming

# Save context when finishing work  
python3 codebase_summary/agent_workflow_orchestrator.py outgoing "Detailed session summary here"
```

**⚠️ CRITICAL: Changelog Update Requirements**
When updating changelog, ALWAYS provide detailed summary:
```bash
# ❌ WRONG - Missing detail
python3 codebase_summary/update_changelog.py add --summary "Fixed some bugs"

# ✅ CORRECT - Comprehensive detail  
python3 codebase_summary/update_changelog.py add --summary "Fixed critical path resolution bugs in agent_workflow_orchestrator.py

## Key Accomplishments:
- **Specific fix 1**: Detailed description of what was fixed
- **Specific fix 2**: Impact and scope of changes  
- **Testing**: Validation steps completed
- **Documentation**: Updated relevant docs

Impact: System now handles all deployment modes correctly."
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

## 🚨 Session Completion Checklist

**MANDATORY steps for proper agent handoff:**

### 1. Stage All Changes
```bash
git add .
git status  # Verify all changes are staged
```

### 2. Create Comprehensive Commit
```bash
git commit -m "$(cat <<'EOF'
Brief commit title describing main changes

## 📋 Session Summary - [Brief description]

### 🔄 Major Accomplishments
- **Achievement 1**: Specific description with impact
- **Achievement 2**: Technical details and scope
- **Achievement 3**: Files affected and purpose

### 🛠 Technical Changes
- List specific file modifications
- Document architectural changes
- Note any breaking changes

### 📚 Documentation Updates
- Document any new or updated documentation
- Note removed or consolidated files

### 📋 Next Session Priorities
1. Task 1 with specific details
2. Task 2 with expected outcomes
3. Validation/testing requirements

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### 3. Update Changelog with Detailed Summary
```bash
python3 codebase_summary/update_changelog.py add --summary "Session title with comprehensive details

## Key Accomplishments:
- **Specific Achievement**: Detailed description and impact
- **Technical Change**: Scope and purpose 
- **Documentation**: What was updated/added/removed

Transform brief summary into detailed context for future agents."
```

### 4. **CRITICAL**: Only ONE changelog_summary.json file should exist
- **PRIMARY**: `/home/runner/workspace/changelog_summary.json` (root level)
- **REMOVE**: Any `codebase_summary/changelog_summary.json` (legacy artifact)
- If you find duplicates, delete the nested one and keep the root file

### 5. Update Todo List for Next Agent
Use TodoWrite to set clear priorities for the next session with specific actionable tasks.

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

## 🎯 Agent Task-Specific Workflows

### Adding New Features
1. Review current architecture from `codebase_summary.json` and `ARCHITECTURE_DIAGRAM.md`
2. Check `session_state.json` for previous agent context and priorities
3. Implement changes following existing patterns and architecture
4. Run `update_project_summary.py` to update analysis after changes
5. Update session state with your progress using agent orchestrator

### Bug Fixes
1. Check `missing_breadcrumbs.json` for documentation gaps that might indicate issues
2. Review `ARCHITECTURE_DIAGRAM.md` for system understanding and dependencies
3. Implement fixes maintaining system patterns and architecture
4. Regenerate documentation after changes to reflect fixes
5. Document resolution approach for future agents

### Code Analysis Tasks
1. Use `codebase_summary.json` for comprehensive project overview
2. Check function hotspots and complexity metrics for focus areas
3. Review documentation coverage percentages to identify gaps
4. Focus analysis on areas marked as needing attention
5. Update documentation with findings and recommendations

## ⚠️ System Boundaries - Critical Understanding

### What NOT to Change
- **Core Arkival system files** - Preserve all Arkival references and core functionality
- **Path resolution logic** - Never modify `find_arkival_paths()` function
- **Agent handoff mechanisms** - Don't alter session state structure or workflow orchestration
- **Configuration file structures** - Maintain existing config file formats and locations
- **Version system logic** - Don't modify the dual versioning approach

### What DOES Change
- **Generated documentation** - Adapts automatically to reflect host project or Arkival itself
- **Project analysis results** - Updates with each codebase scan to reflect current state
- **Documentation coverage metrics** - Changes as code and documentation evolve
- **Session state data** - Updates with each agent transition and task completion
- **Changelog entries** - Grows with development progress and milestone achievements

## 🎯 Best Practices

1. **Start every session** with `update_project_summary.py` and agent orchestrator incoming
2. **Check deployment mode** via `_critical_context.deployment_mode` 
3. **Review session state** from previous agent before starting work
4. **Use agent orchestrator** for proper session management and handoffs
5. **Document functions** with `@codebase-summary:` breadcrumbs
6. **Verify system state** before major changes
7. **Understand system boundaries** - know what to change vs preserve

## 🔄 Agent Transition Workflow

### Incoming Agent Checklist
1. **Load project context**: Run `python3 codebase_summary/agent_workflow_orchestrator.py incoming`
2. **Review session state**: Check `session_state.json` for previous agent tasks and context
3. **Understand deployment mode**: Check `_critical_context.deployment_mode` in codebase_summary.json
4. **Check for unresolved issues**: Review any incomplete work or known problems
5. **Verify system state**: Ensure application is running and all systems operational

### Outgoing Agent Checklist
1. **Update session state**: Document completed tasks and current project state
2. **Run outgoing workflow**: `python3 codebase_summary/agent_workflow_orchestrator.py outgoing --summary "Detailed session summary"`
3. **Update changelog**: Add comprehensive entry with specific accomplishments and impact
4. **Set priorities**: Use TodoWrite to establish clear priorities for next agent session
5. **Commit changes**: Follow structured commit message format with session summary

## 🔧 Troubleshooting Common Issues

### Documentation Generation Problems
- **Check deployment mode detection**: Review logs for path resolution and project detection
- **Verify project files**: Ensure README.md, package.json, or pyproject.toml are findable
- **Confirm directory context**: Make sure you're running from correct working directory
- **Force regeneration**: Use `--force` flag if cache issues suspected

### Agent Handoff Issues
- **Verify session_state.json**: Check file exists and is readable in `codebase_summary/` directory
- **Check file permissions**: Ensure write access to `codebase_summary/` and `export_package/` directories
- **Previous agent completion**: Verify previous agent properly completed handoff workflow
- **Path resolution**: Confirm `find_arkival_paths()` is returning expected file locations

### Path Resolution Problems
- **Config file location**: Check `arkival_config.json` exists in expected location (parent dir for subdirectory mode)
- **Working directory**: Verify current directory matches expected deployment mode
- **Deployment mode mismatch**: Review `find_arkival_paths()` output in logs for detection logic
- **Permission issues**: Ensure read/write access to all required directories

### Performance and Analysis Issues
- **Large codebase handling**: Use ignore patterns to exclude unnecessary files from analysis
- **Memory constraints**: Consider running analysis in smaller increments for very large projects
- **Function detection**: Verify language-specific patterns are working for your target files
- **Breadcrumb coverage**: Check `missing_breadcrumbs.json` for systematic documentation gaps

The system is optimized for seamless AI agent collaboration with comprehensive context management and automatic documentation generation.