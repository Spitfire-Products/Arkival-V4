# Arkival

AI Agent Workflow Orchestration System for seamless knowledge transfer between AI agents and human developers across any IDE.

## 🚀 Quick Start

### Option A: Add to Existing Project (Non-Destructive)
```bash
# In your existing project root
git clone https://github.com/Spitfire-Products/Arkival-V4.git Arkival-V4
cd Arkival-V4
python3 setup_workflow_system.py
```

### Option B: New Project
```bash
git clone https://github.com/Spitfire-Products/Arkival-V4.git my-project
cd my-project
python3 setup_workflow_system.py
```

## 🎯 Core Workflows

### Agent Handoff (Essential for AI Collaboration)
```bash
# When starting work (loads context)
python3 codebase_summary/agent_workflow_orchestrator.py incoming

# When finishing work (saves context)  
python3 codebase_summary/agent_workflow_orchestrator.py outgoing
```

### Project Analysis
```bash
# Generate/update project documentation
python3 codebase_summary/update_project_summary.py

# Add changelog entry
python3 codebase_summary/update_changelog.py
```

## 🌐 Supported Environments

**IDEs**: Replit, VS Code, Cursor, GitHub Codespaces, Gitpod, Windsurf, Any Terminal  
**AI Assistants**: Claude Code, Cline, Cursor AI, GitHub Copilot, Roo Code

## 🏗 System Architecture

- **Agent Orchestration**: Seamless handoffs between AI agents with context preservation
- **Project Analysis**: Automatic codebase documentation and architecture mapping  
- **Cross-Platform**: Works in any IDE with automatic environment detection
- **Version Tracking**: Independent codebase and changelog version systems

## 📁 Key Files

- `codebase_summary.json` - Current project analysis and metrics
- `ARCHITECTURE_DIAGRAM.md` - Visual project overview (auto-generated)
- `modules/claude-code/CLAUDE.md` - AI agent integration guide
- `changelog_summary.json` - Project milestone tracking

## 🔧 Configuration

Arkival automatically detects your environment and creates appropriate workflow files:
- **Replit**: `.replit` with workflow panel integration
- **VS Code/Cursor**: `.vscode/tasks.json` for Command Palette
- **Universal**: Shell scripts in `.workflow_system/scripts/`

## 📚 Documentation

- **AI Agents**: See `modules/claude-code/CLAUDE.md` for integration guide
- **Security**: Review `SECURITY.md` for security policies  
- **Contributing**: Check `CONTRIBUTING.md` for contribution guidelines

## 🎯 Key Features

- **Zero-Config Setup**: Automatic IDE detection and workflow integration
- **Non-Destructive**: Subdirectory mode preserves existing project structure
- **Agent-Optimized**: Built for AI agent collaboration with context management
- **Cross-Platform**: Works across all major IDEs and development environments
- **Documentation Automation**: Auto-generates project analysis and architecture diagrams

## License

Attribution License - see [LICENSE](LICENSE) for details.