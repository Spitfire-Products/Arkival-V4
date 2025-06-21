# Arkival - Replit Agent Workflow Guide

## Overview

Arkival is an AI Agent Workflow Orchestration System designed for seamless knowledge transfer between AI agents and human developers in Replit environments. This guide provides Replit-specific implementation patterns, workflow integration, and troubleshooting for optimal agent collaboration.

## 🚀 Agent Onboarding Workflow (Replit-Specific)

### Step 1: Environment Verification
```bash
# Verify Python 3.11+ availability
python3 --version

# Check Replit environment variables
echo $REPLIT_SLUG
echo $REPLIT_DB_URL

# Verify file system access
ls -la codebase_summary/
```

### Step 2: Automated Context Loading
**Option A: Use Replit Workflow Panel (Recommended)**
- Click "Agent Incoming Workflow" button in Replit sidebar
- Monitor console output for successful context loading

**Option B: Console Command**
```bash
python3 codebase_summary/agent_workflow_orchestrator.py incoming
```

### Step 3: Replit-Specific Validation
- Confirm `.replit` file workflow integration exists
- Test workflow panel responsiveness 
- Validate `codebase_summary.json` accessibility in Replit file browser
- Verify console output shows all 15 onboarding steps completed

### Step 4: Review Critical Context Files
- **codebase_summary.json** - Open in Replit editor for project context
- **AGENT_GUIDE.md** - Review universal agent workflows
- **session_state.json** - Check previous agent handoff context
- **ARCHITECTURE_DIAGRAM.md** - Understand system structure

## System Architecture

### Core Architecture Pattern
- **Type**: Python-based workflow orchestration system
- **Deployment Mode**: Supports both standalone and subdirectory deployment modes
- **Multi-language Support**: Comprehensive function detection across 15+ programming languages
- **AI Integration**: Built-in support for Claude, OpenAI, Google Gemini, and other AI providers

### Key Components

1. **Codebase Analysis Engine** (`codebase_summary/update_project_summary.py`)
   - Multi-language function detection and analysis
   - Automatic documentation coverage tracking
   - Architecture pattern recognition
   - Real-time project structure analysis

2. **Agent Workflow Orchestrator** (`codebase_summary/agent_workflow_orchestrator.py`)
   - Manages handoffs between AI agents and human developers
   - Session state preservation and context management
   - Automated workflow trigger handling

3. **Changelog Management System** (`codebase_summary/update_changelog.py`)
   - Automated changelog generation and version tracking
   - Workflow integration for seamless updates
   - Archive management and version correlation

4. **Setup and Validation Scripts**
   - `setup_workflow_system.py`: Cross-platform environment setup
   - `validate_deployment.py`: Deployment readiness validation
   - `validate_export_readiness.py`: Export package validation

## Data Flow

### Agent Handoff Workflow
1. **Incoming Agent**: Loads project context from `session_state.json` and `codebase_summary.json`
2. **Active Development**: Agent performs tasks while maintaining context
3. **Outgoing Agent**: Updates session state and regenerates documentation
4. **Knowledge Transfer**: Context preserved for next agent via structured handoff files

### Documentation Generation Flow
1. **File Scanning**: Multi-language parser scans all source files
2. **Function Detection**: Identifies functions, methods, and documentation breadcrumbs
3. **Analysis**: Calculates coverage metrics, complexity analysis, and architecture patterns
4. **Output Generation**: Creates comprehensive JSON summaries and markdown documentation

## External Dependencies

### Runtime Dependencies
- **Python 3.11+**: Core runtime environment
- **Node.js 20**: For JavaScript/TypeScript analysis and AI integrations
- **Standard Libraries**: pathlib, json, datetime, subprocess, collections

### Optional AI Integrations
- **Claude CLI**: For direct Claude communication via `modules/claude-code/`
- **OpenAI API**: Via environment variables or direct integration
- **Google Gemini**: Through official client libraries

### Development Tools
- **Git**: Version control integration
- **Various Package Managers**: npm, pip, cargo, etc. for multi-language projects

## 🔧 Replit Workflow Panel Integration

### Automated Workflow Buttons
The system creates workflow buttons in Replit's workflow panel:

1. **Agent Incoming Workflow**: Automatically loads project context and session state
2. **Agent Outgoing Workflow**: Handles session completion and agent handoff

### .replit Configuration Example
```toml
[[workflows.workflow]]
name = "Agent Incoming Workflow"
author = "workflow-system"
mode = "sequential"

[[workflows.workflow.tasks]]
task = "shell.exec"
args = "python3 codebase_summary/agent_workflow_orchestrator.py incoming"

[[workflows.workflow]]
name = "Agent Outgoing Workflow"
author = "workflow-system"
mode = "sequential"

[[workflows.workflow.tasks]]
task = "shell.exec"
args = "python3 codebase_summary/agent_workflow_orchestrator.py outgoing --summary 'Replit session completed'"
```

### Manual Workflow Execution
If workflow panel is unavailable, use console commands:
```bash
# Start new agent session
python3 codebase_summary/agent_workflow_orchestrator.py incoming

# Complete agent session with detailed summary
python3 codebase_summary/agent_workflow_orchestrator.py outgoing --summary "Detailed session summary"

# Force regenerate project analysis
python3 codebase_summary/update_project_summary.py --force
```

## 💻 Replit Development Patterns

### File Management in Replit
- Use Replit file browser for efficient navigation
- Leverage integrated editor for code changes
- Monitor generated files in `codebase_summary/` directory
- Access all project files through Replit's file tree

### Replit Console Integration
- All agent workflows execute in Replit console
- Monitor real-time output for workflow status
- Use console for validation and troubleshooting commands
- Leverage Replit's persistent console session

### Task-Specific Workflows in Replit

#### Adding New Features
1. **Use Workflow Panel**: Click "Agent Incoming Workflow" 
2. **Review Context**: Open `codebase_summary.json` in Replit editor
3. **Implement Changes**: Use Replit's integrated editor
4. **Update Analysis**: Run `python3 codebase_summary/update_project_summary.py --force`
5. **Complete Session**: Use "Agent Outgoing Workflow" button

#### Bug Fixes in Replit
1. **Load Context**: Start with incoming workflow 
2. **Analyze Issues**: Review `missing_breadcrumbs.json` in Replit file browser
3. **Debug in Console**: Use Replit console for testing and validation
4. **Document Fixes**: Update relevant files using Replit editor
5. **Save Progress**: Complete with outgoing workflow

#### Code Analysis Tasks
1. **Start Analysis**: Use incoming workflow to load current state
2. **Review Metrics**: Open generated analysis files in Replit editor
3. **Identify Focus Areas**: Use Replit search for function hotspots
4. **Document Findings**: Create analysis reports in Replit
5. **Preserve Context**: Use outgoing workflow for handoff

## Deployment Strategy

### Subdirectory Mode (Recommended for Existing Replit Projects)
- Clone Arkival into existing Replit project as `Arkival-V4/`
- Configuration stored at project root as `arkival_config.json`
- Generated documentation reflects host project structure
- Non-destructive integration with existing Replit codebases
- Workflow panel integration remains functional

### Standalone Mode (For New Replit Projects)
- Direct deployment in Replit project root
- Full feature access and development capabilities
- Ideal for Replit projects built around Arkival workflows
- Complete workflow panel integration

## 🔄 Agent Handoff in Replit Environment

### Outgoing Agent Checklist (Replit-Specific)
1. **Use Workflow Panel**: Click "Agent Outgoing Workflow" button in sidebar
2. **Alternative Console**: `python3 codebase_summary/agent_workflow_orchestrator.py outgoing --summary "Comprehensive session summary"`
3. **Verify in Replit Console**: Check workflow completion messages
4. **Update Documentation**: Ensure changes visible in Replit file browser
5. **Test Workflow Panel**: Verify both workflow buttons remain functional for next agent

### Incoming Agent Checklist (Replit-Specific)
1. **Start with Workflow Panel**: Click "Agent Incoming Workflow" button
2. **Verify Context Loading**: Check console output for successful 15-step onboarding
3. **Review Replit File Browser**: Confirm access to all necessary files
4. **Test Environment**: Verify Python modules and dependencies
5. **Validate Workflow Integration**: Ensure workflow panel remains accessible

## 🚨 Replit Environment Troubleshooting

### Common Replit Issues

#### Workflow Panel Not Loading
- **Symptom**: Workflow buttons don't appear in Replit sidebar
- **Root Cause**: Missing or malformed `.replit` file
- **Solution**: Verify `.replit` file exists and contains workflow configuration
- **Alternative**: Use console commands directly
- **Prevention**: Run `python3 setup_workflow_system.py` to regenerate configuration

#### Python Module Import Errors
- **Symptom**: `ModuleNotFoundError` when running scripts
- **Root Cause**: Wrong Python version or missing modules
- **Solution**: Ensure Python 3.11+ is selected in Replit environment
- **Check**: Verify `modules = ["python-3.11"]` in `.replit` file
- **Alternative**: Use `pip install` for missing packages

#### File Path Resolution Issues
- **Symptom**: Scripts can't find `codebase_summary` files
- **Root Cause**: Wrong working directory
- **Solution**: Verify working directory is project root
- **Check Command**: `pwd` to verify current directory
- **Fix**: `cd` to project root before running scripts

#### Agent Context Loading Failures
- **Symptom**: Incoming workflow fails to load session state
- **Root Cause**: Corrupted or missing session files
- **Solution**: Check `codebase_summary/session_state.json` exists and is readable
- **Recovery**: Run `python3 codebase_summary/update_project_summary.py --force`
- **Prevention**: Always complete outgoing workflow properly

#### Replit Console Unresponsive
- **Symptom**: Commands hang or produce no output
- **Root Cause**: Replit environment overload or network issues
- **Solution**: Refresh Replit page and restart console
- **Alternative**: Use Replit's "Stop" button to kill hanging processes
- **Prevention**: Monitor resource usage during large analysis tasks

#### Git Integration Issues
- **Symptom**: Git commands fail or produce errors
- **Root Cause**: Replit git configuration or permissions
- **Solution**: Configure git user: `git config user.name` and `git config user.email`
- **Alternative**: Use Replit's built-in version control interface
- **Check**: Verify git status with `git status`

## ⚡ Replit Performance Optimization

### Efficient Workflow Execution
- **Use Workflow Panel**: Buttons are faster than manual console commands
- **Parallel Tasks**: Leverage Replit's integrated terminal for concurrent operations
- **Resource Monitoring**: Watch Replit console for memory and CPU usage
- **Batch Operations**: Group related commands to reduce startup overhead

### File System Optimization
- **Organized Structure**: Keep generated files in designated directories
- **Browser Navigation**: Use Replit's file browser for efficient file access
- **Minimal File Operations**: Reduce unnecessary file reads/writes in scripts
- **Cache Utilization**: Leverage Replit's persistent file system for caching

### Memory Management for Large Projects
- **Incremental Processing**: Use `--force` flag selectively to avoid memory issues
- **Selective Analysis**: Modify ignore patterns to exclude large unnecessary files
- **Monitor Usage**: Watch Replit's resource indicators during analysis
- **Recovery Strategy**: Split large analysis tasks into smaller chunks if needed

## 📚 Integration with Enhanced Agent System

### Reference Hierarchy for Replit Agents
1. **Start Here**: `replit.md` (Replit-specific setup and workflows)
2. **Core Guidance**: `AGENT_GUIDE.md` (comprehensive agent workflows)
3. **Architecture**: `ARCHITECTURE_DIAGRAM.md` (system understanding) 
4. **Technical Reference**: `codebase_summary.json` (project analysis)
5. **Session Context**: `codebase_summary/session_state.json` (agent handoff state)

### Replit-Specific Workflow Enhancement
The enhanced agent system provides 15-step comprehensive onboarding adapted for Replit:
- **Project overview** from README.md and AGENT_GUIDE.md
- **Deployment mode detection** (standalone vs subdirectory)
- **Architecture insights** from generated diagrams
- **External dependencies** identification
- **Workflow examples** with Replit-specific patterns
- **Git activity analysis** integrated with Replit's git interface
- **System capabilities** summary
- **Command reference** optimized for Replit console

### Advanced Replit Integration Patterns
- **Workflow Panel Priority**: Use buttons when available, fallback to console
- **File Browser Integration**: Navigate and edit files using Replit's interface
- **Console Monitoring**: Watch real-time output for all agent operations
- **Environment Validation**: Verify Replit-specific settings before major operations
- **Performance Awareness**: Adapt workflows for Replit's resource constraints

## Changelog

```
Changelog:
- June 21, 2025: Enhanced with comprehensive agent onboarding workflows
- June 21, 2025: Added Replit-specific troubleshooting and performance optimization
- June 21, 2025: Integrated with 15-step enhanced agent workflow system
- June 21, 2025: Initial setup
```

## User Preferences

```
Preferred communication style: Simple, everyday language with actionable technical guidance.
Focus: Replit-specific implementation details and practical troubleshooting.
```