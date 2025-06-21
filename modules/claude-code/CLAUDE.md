# Claude Code Integration Guide for Arkival

*Generated for AI agents working with Arkival workflow orchestration system*

## 🎯 Quick Start for Incoming Agents

### Context
You're working with the Arkival AI Agent Workflow Orchestration System. This system is designed for seamless knowledge transfer between AI agents and generates project documentation that adapts to the host project.

### Core Commands
```bash
# Generate/update project analysis
python3 codebase_summary/update_project_summary.py

# Setup workflow system (first-time deployment)
python3 setup_workflow_system.py

# Validate deployment readiness
python3 validate_deployment.py
```

### Key Files to Understand
- `codebase_summary.json` - Main project analysis (auto-generated, reflects host project)
- `ARCHITECTURE_DIAGRAM.md` - Visual project overview (auto-generated, reflects host project)
- `codebase_summary/session_state.json` - Agent handoff state
- `arkival_config.json` - Configuration (in parent directory for subdirectory mode)

## 🔄 Agent Handoff Workflow

### When You Start
1. **Read project context**: Check `codebase_summary.json` for current project state
2. **Check agent state**: Read `codebase_summary/session_state.json` for previous agent tasks
3. **Understand deployment**: Check if in dev mode (standalone) or subdirectory mode

### When You Finish
1. **Update session state**: Record your completed tasks in `session_state.json`
2. **Regenerate documentation**: Run `update_project_summary.py` to refresh analysis
3. **Document changes**: Update relevant documentation if you made significant changes

## 🏗 Deployment Modes

### Development Mode (Standalone)
- Running directly in Arkival project root
- All files in current directory structure
- Generated docs reflect Arkival itself

### Subdirectory Mode (Production)
- Arkival cloned as `ParentProject/Arkival-V4/`
- Config at `ParentProject/arkival_config.json`
- Generated docs reflect ParentProject metadata

## 📊 Key System Behaviors

### Auto-Detection Logic
The system automatically detects:
- **Project type**: From package.json, pyproject.toml, README.md
- **Deployment mode**: Subdirectory vs standalone
- **Host project metadata**: When in subdirectory mode, analyzes parent project

### Documentation Generation
- `codebase_summary.json`: Comprehensive project analysis
- `ARCHITECTURE_DIAGRAM.md`: Visual architecture overview
- `missing_breadcrumbs.json`: Documentation coverage analysis
- All output adapts to reflect the host project being analyzed

## 🛠 Common Agent Tasks

### Adding New Features
1. Understand current architecture from generated docs
2. Implement changes following existing patterns
3. Run `update_project_summary.py` to update analysis
4. Update session state with your changes

### Bug Fixes
1. Check `missing_breadcrumbs.json` for documentation gaps
2. Review `ARCHITECTURE_DIAGRAM.md` for system understanding
3. Implement fixes maintaining system patterns
4. Regenerate documentation after changes

### Code Analysis
1. Use generated `codebase_summary.json` for project overview
2. Check function hotspots and complexity metrics
3. Review documentation coverage percentages
4. Focus on areas marked as needing attention

## ⚠️ Important Notes

### Version Systems
- **Codebase version**: Auto-increments with each analysis run
- **Changelog version**: Manual, for major feature releases
- These are INDEPENDENT - version mismatch is normal

### What NOT to Change
- Core Arkival system files (keep all Arkival references)
- Path resolution logic in `find_arkival_paths()`
- Agent handoff mechanisms

### What DOES Change
- Generated output documentation (adapts to host project)
- Project analysis results (reflects current codebase state)
- Documentation coverage metrics (updates with code changes)

## 🔧 Troubleshooting

### If Documentation Seems Wrong
- Check deployment mode detection in logs
- Verify `_detect_project_info()` is finding correct project files
- Ensure you're in the right directory for your deployment mode

### If Agent Handoff Fails
- Check `session_state.json` exists and is readable
- Verify file permissions in `codebase_summary/` directory
- Ensure previous agent updated state before finishing

### If Path Resolution Fails
- Check `arkival_config.json` location (parent dir for subdirectory mode)
- Verify current working directory matches expected deployment mode
- Review `find_arkival_paths()` output in logs

---

*This guide enables seamless AI agent collaboration within the Arkival workflow orchestration system.*