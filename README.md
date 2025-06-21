# Arkival

🤖 **AI Agent Workflow Orchestration System** - Transform any project into an AI-collaborative workspace with seamless knowledge transfer between AI agents and human developers.

## 🎯 What is Arkival?

Arkival is your **AI development accelerator** that:
- ✅ **Auto-documents** your entire codebase (23+ languages supported)
- ✅ **Enables seamless AI agent handoffs** with preserved context
- ✅ **Works in any IDE** (Replit, VS Code, Cursor, Terminal, etc.)
- ✅ **Non-destructively integrates** into existing projects
- ✅ **Tracks development progress** with automated changelogs

**Perfect for:** Solo developers using AI assistants, teams collaborating with AI agents, or anyone wanting better project documentation automation.

---

## 🚀 Get Started (3 Steps)

### Step 1: Choose Your Deployment Mode

**Option A: New Development Project** (Primary Mode - Recommended):
```bash
# Clone Arkival as your project foundation
git clone https://github.com/Spitfire-Products/Arkival-V4.git my-project
cd my-project

# Initialize the workflow system
python3 setup_workflow_system.py

# The cloned repo BECOMES your project root - start building here!
```

**Option B: Add to Existing Project** (Non-Destructive):
```bash
# Navigate to your existing project root
cd /path/to/your-existing-project

# Clone Arkival as subdirectory 
git clone https://github.com/Spitfire-Products/Arkival-V4.git

# Setup the system in subdirectory mode
cd Arkival-V4 && python3 setup_workflow_system.py
```

### Step 2: Initialize Project Analysis
```bash
# Generate complete project documentation
python3 codebase_summary/update_project_summary.py

# This creates: codebase_summary.json, ARCHITECTURE_DIAGRAM.md, and more
```

### Step 3: Start Using AI Agent Workflows
```bash
# When starting work with an AI assistant
python3 codebase_summary/agent_workflow_orchestrator.py incoming

# When finishing work (saves context for next session)  
python3 codebase_summary/agent_workflow_orchestrator.py outgoing
```

---

## 🔄 Daily Usage Workflow

### Morning Routine (Start Work)
1. **Load Context**: `python3 codebase_summary/agent_workflow_orchestrator.py incoming`
2. **Check Project State**: Open `codebase_summary.json` for current status
3. **Review Recent Changes**: Check `ARCHITECTURE_DIAGRAM.md` for project overview

### During Development
- **AI agents automatically understand your project** through generated documentation
- **Add new features** - breadcrumbs are auto-detected and documented
- **Run analysis anytime**: `python3 codebase_summary/update_project_summary.py --force`

### End of Session
1. **Save Progress**: `python3 codebase_summary/agent_workflow_orchestrator.py outgoing`
2. **Update Changelog**: `python3 codebase_summary/update_changelog.py`
3. **Validate System**: `python3 validate_deployment.py`

---

## 💡 Advanced Usage & Features

### 🔄 Maximize AI Agent Efficiency
- **Context Preservation**: Never lose project context between AI sessions
- **Smart Handoffs**: Incoming agents instantly understand previous work
- **Progress Tracking**: Automated changelog generation shows development velocity
- **Multi-Language Support**: 23+ programming languages with function detection

### 🛠 Power User Commands
```bash
# Force regenerate all documentation
python3 codebase_summary/update_project_summary.py --force

# Validate export readiness (for sharing/deployment)
python3 validate_export_readiness.py

# Advanced changelog management
python3 codebase_summary/update_changelog.py remove-duplicates
```

### 🎯 Integration Patterns

**For New Development** (Primary Pattern):
- Use Arkival as your project foundation - clone and start building
- All your source code lives alongside Arkival's workflow system
- Perfect for AI-assisted development from day one
- Example: This current workspace demonstrates this pattern

**With AI Assistants**:
- Start sessions: Load context with `incoming` workflow
- During development: AI agents read `codebase_summary.json` for project understanding
- End sessions: Save context with `outgoing` workflow

**With Existing Projects**:
- Add Arkival as subdirectory without affecting existing structure
- Workflow system analyzes and documents the parent project
- Non-destructive integration preserves all existing files

### 📂 Key Files You'll Use Daily

| File | Purpose | When to Use |
|------|---------|-------------|
| `codebase_summary.json` | **Complete project analysis** | AI agents read this for context |
| `ARCHITECTURE_DIAGRAM.md` | **Visual project overview** | Quick project understanding |
| `changelog_summary.json` | **Milestone tracking** | Project progress reviews |
| `AGENT_GUIDE.md` | **AI agent instructions** | Onboarding new AI assistants |

---

## 🌐 Supported Environments

**IDEs**: VS Code, Cursor, GitHub Codespaces, Gitpod, Windsurf, Replit, Any Terminal  
**AI Assistants**: Cline, Cursor AI, GitHub Copilot, Roo Code, Claude Code (optional module)  
**Languages**: Python, JavaScript, TypeScript, Rust, Go, Java, C++, and 16+ more

## 🔧 How It Works

Arkival automatically detects your environment and creates appropriate workflow integrations:
- **VS Code/Cursor**: `.vscode/tasks.json` for Command Palette access
- **Universal Terminal**: Shell scripts in `.workflow_system/scripts/` for any environment
- **IDE-Specific**: Optional integrations for Replit (`.replit`), Gitpod, etc.

**Smart Deployment Modes**:
- **Development Mode**: Arkival becomes your project foundation (primary use case)
- **Subdirectory Mode**: Non-destructive integration into existing projects  
- **Auto-Detection**: Intelligently chooses the right mode based on your setup

---

## 📚 Documentation & Support

| Resource | Description |
|----------|-------------|
| **[AGENT_GUIDE.md](AGENT_GUIDE.md)** | Complete guide for AI agents |
| **[ENGINEERING_BEST_PRACTICES.md](ENGINEERING_BEST_PRACTICES.md)** | Development standards and workflows |
| **[CONTRIBUTING.md](CONTRIBUTING.md)** | Contribution guidelines |
| **[SECURITY.md](SECURITY.md)** | Security policies and practices |
| **[REFERENCE_README.md](documentation_assets/REFERENCE_README.md)** | Technical reference docs & future modules |
| **[modules/claude-code/](modules/claude-code/)** | Optional Claude integration module |

## 🚀 Why Arkival?

- **🎯 Purpose-Built for AI**: Designed specifically for AI-human collaboration
- **⚡ Zero Learning Curve**: Works immediately with any AI assistant
- **🔒 Non-Destructive**: Safe to add to any existing project
- **📈 Productivity Boost**: Eliminates context-switching overhead
- **🌍 Universal**: Works across all development environments

## License

Attribution License - see [LICENSE](LICENSE) for details.