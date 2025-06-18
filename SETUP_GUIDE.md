# Workflow System Setup Guide - Cross-Platform

## 🚀 Deployment Modes

Arkival supports **two deployment modes** that are automatically detected:

### 🆕 Subdirectory Mode (Non-Destructive Integration)
**When it activates**: You clone Arkival into an existing project as a subdirectory
```bash
# In your existing project root
git clone https://github.com/spitfire-products/arkival.git Arkival
cd Arkival
python3 setup_workflow_system.py
```

**What happens**:
- ✅ Only `arkival_config.json` is added to your project root
- ✅ All Arkival files remain in `/Arkival` subdirectory  
- ✅ Generated files go to `/Arkival/data/` (not your project root)
- ✅ Your existing project files are **never modified**
- ✅ Easy to remove if needed

### Development Mode (Full Integration)
**When it activates**: You clone Arkival as the main project
```bash
git clone https://github.com/spitfire-products/arkival.git
cd arkival
python3 setup_workflow_system.py
```

**What happens**:
- Generated files go to project root and `codebase_summary/`
- Full integration with project structure
- Ideal for dedicated Arkival development

## Quick Start
1. Choose your deployment mode (see above) and clone Arkival
2. Run the setup script: `python3 setup_workflow_system.py`
   - **Automatically detects** your IDE and deployment mode
   - **Creates appropriate configuration** for your environment
   - **Generates IDE-specific files** (gitignored, won't clutter repos)
3. Test the system by running the incoming workflow
4. Begin development with full agent handoff support

**Path Intelligence**: All scripts automatically detect which mode they're running in and adjust file paths accordingly.

## Environment-Specific File Generation

**Important**: The setup script creates IDE-specific files that are **gitignored** and won't appear in GitHub clones:

### Files Created During Setup:
- **Replit**: `.replit` file with integrated workflows
- **VS Code/Cursor**: `.vscode/tasks.json` with Command Palette integration
- **Gitpod**: `.gitpod.yml` with cloud environment configuration
- **Universal**: `.workflow_system/scripts/` shell scripts for any IDE

### Why These Files Are Gitignored:
- **Clean Repository**: GitHub users get a clean clone without environment-specific clutter
- **Auto-Generation**: Setup script detects your IDE and creates appropriate files
- **No Conflicts**: Different team members can use different IDEs without file conflicts
- **Flexibility**: Each developer gets their preferred IDE configuration

## Available Workflows

### Agent Incoming Workflow
**Purpose**: Load context when starting a new session

**How to run** (choose your method):
- **Replit**: Click "Agent Incoming Workflow" in workflows panel
- **VS Code/Cursor**: Press `Ctrl+Shift+P` → Tasks: Run Task → Agent Incoming Workflow
- **Terminal (Any IDE)**: `python3 codebase_summary/agent_workflow_orchestrator.py incoming`
- **Shell Script**: `./.workflow_system/scripts/agent_incoming.sh`

### Agent Outgoing Workflow
**Purpose**: Document session completion and prepare handoff

**How to run** (choose your method):
- **Replit**: Click "Agent Outgoing Workflow" in workflows panel
- **VS Code/Cursor**: Press `Ctrl+Shift+P` → Tasks: Run Task → Agent Outgoing Workflow
- **Terminal (Any IDE)**: `python3 codebase_summary/agent_workflow_orchestrator.py outgoing --summary "Your session summary"`
- **Shell Script**: `./.workflow_system/scripts/agent_outgoing.sh "Session summary" completed`

### Update Changelog
**Purpose**: Add entries to project changelog

**How to run** (choose your method):
- **Terminal (Any IDE)**: `python3 codebase_summary/update_changelog.py add --summary "Your changes"`
- **Shell Script**: `./.workflow_system/scripts/update_changelog.sh "Change description"`

## Supported Development Environments

### Fully Supported IDEs
- **Replit** - Native workflow integration with UI buttons
- **VS Code** - Task runner integration via Command Palette
- **Cursor** - VS Code-compatible task system
- **GitHub Codespaces** - Cloud development environment
- **Gitpod** - Browser-based development with pre-configured tasks
- **Any IDE with Terminal** - Universal shell script fallback

### AI Coding Assistant Compatibility
- **Cline** (VS Code extension) - Can execute via tasks
- **Claude Code** (Multi-IDE) - Terminal command execution
- **GitHub Copilot** (All IDEs) - Compatible with all methods
- **Cursor AI** (Native) - Direct task integration
- **Roo Code** (Multi-IDE) - Shell script execution

## AI Agent Integration

### After Setup - Important Next Steps:
1. **Edit `workflow_config.json`** with your project-specific details:
   - Update `project_name` and `technology_stack`
   - Add `main_files` and `important_directories`
   - Customize integration notes for your development workflow

2. **AI Agent Onboarding Process**:
   - The AI agent you're working with should **analyze your project structure**
   - Ask the agent to **update workflow_config.json** with detected technology stack
   - Use **"Hi"** as a trigger phrase to start the incoming agent workflow
   - The system will **automatically load project context** and previous session state

3. **Understanding the Cross-Platform Design**:
   - **Setup Once**: Run `python3 setup_workflow_system.py` in any IDE
   - **Environment Detection**: Script automatically detects VS Code, Replit, Codespaces, etc.
   - **Appropriate Configuration**: Creates the right files for your specific environment
   - **Clean GitHub Repo**: Environment files stay local, don't clutter the repository

## Workflow Execution Methods

### Method 1: IDE Tasks (VS Code/Cursor/Codespaces)
```bash
# Press Ctrl+Shift+P, then:
Tasks: Run Task → Agent Incoming Workflow
Tasks: Run Task → Agent Outgoing Workflow
Tasks: Run Task → Update Changelog
```

### Method 2: Replit Workflows
```bash
# Click in workflows panel:
Agent Incoming Workflow
Agent Outgoing Workflow
```

### Method 3: Direct Terminal Commands
```bash
# Works in any IDE with terminal:
python3 codebase_summary/agent_workflow_orchestrator.py incoming
python3 codebase_summary/agent_workflow_orchestrator.py outgoing --summary "Session completed" --type completed
python3 codebase_summary/update_changelog.py add --summary "Added new features"
```

### Method 4: Shell Scripts (Universal)
```bash
# Executable scripts for any environment:
./.workflow_system/scripts/agent_incoming.sh
./.workflow_system/scripts/agent_outgoing.sh "Session summary" completed
./.workflow_system/scripts/update_changelog.sh "Change description"
```

## Repository Structure for GitHub

### What's Included in GitHub Repository:
- ✅ **Core System Files**: All Python scripts and workflow orchestration
- ✅ **Documentation**: README.md, SETUP_GUIDE.md, architecture docs
- ✅ **Configuration Templates**: `workflow_config.json` with cross-platform settings
- ✅ **Universal Components**: Shell scripts and cross-platform compatibility

### What's Generated Locally (Gitignored):
- 🔧 **`.replit`** - Generated for Replit users during setup
- 🔧 **`.vscode/`** - Generated for VS Code/Cursor users during setup
- 🔧 **`.gitpod.yml`** - Generated for Gitpod users during setup
- 🔧 **`.workflow_system/`** - Generated universal scripts and IDE configs

### Benefits of This Design:
- **Clean Repository**: GitHub users see only core system files
- **No IDE Lock-in**: Each user gets their preferred environment setup
- **Zero Conflicts**: No IDE-specific files to cause merge conflicts
- **Automatic Configuration**: Setup script handles all environment detection
- **Future-Proof**: New IDEs can be supported without changing the repository

## Troubleshooting

### Setup Issues:
- Ensure Python 3.7+ is installed
- Check file permissions in project directory
- Verify no conflicting files exist

### Workflow Execution:
- Run `python3 validate_deployment.py` for validation
- Check `workflow_config.json` syntax
- Verify all required files are present

### Environment Detection:
- Setup script automatically detects your IDE
- If detection fails, files are created for universal shell script usage
- All execution methods work regardless of IDE detection accuracy

## Getting Help:
1. Check setup log output for specific error messages
2. Verify all required files using validation step
3. Review configuration for project-specific settings
4. Use terminal commands as fallback if IDE integration fails