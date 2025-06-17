
# IDE Integration Guide

## Supported Development Environments

### 🎯 Primary IDE Support

#### Replit (Native Integration)
- **Workflows**: Native workflow panel integration
- **Setup**: Automatic `.replit` configuration
- **Execution**: Click workflows in UI panel
- **Features**: Port management, hot reload prevention

#### VS Code / Cursor (Task Integration)
- **Tasks**: Command Palette task execution
- **Setup**: `.vscode/tasks.json` auto-generated
- **Execution**: `Ctrl+Shift+P` → "Tasks: Run Task"
- **Features**: Input prompts, integrated terminal

#### GitHub Codespaces (Cloud Native)
- **Environment**: Browser-based development
- **Setup**: Automatic cloud environment configuration
- **Execution**: Terminal and task integration
- **Features**: Pre-configured workspace

#### Gitpod (Browser IDE)
- **Configuration**: `.gitpod.yml` auto-generated
- **Setup**: Automatic workspace initialization
- **Execution**: Terminal commands and tasks
- **Features**: Cloud development environment

### 🤖 AI Assistant Compatibility

#### Cline (VS Code Extension)
```json
// Cline can execute workflows via VS Code tasks
{
  "workflow_trigger": "Ctrl+Shift+P → Tasks: Run Task → Agent Incoming Workflow",
  "integration_method": "vscode_tasks",
  "ai_context": "Full workflow context available to Cline"
}
```

#### Cursor AI (Native)
```json
// Cursor's built-in AI can trigger workflows
{
  "workflow_trigger": "Task execution via Command Palette", 
  "integration_method": "cursor_tasks",
  "ai_context": "Seamless integration with Cursor's AI"
}
```

#### Claude Code (Multi-IDE)
```bash
# Claude can execute via terminal in any IDE
python3 codebase_summary/agent_workflow_orchestrator.py incoming
./.workflow_system/scripts/agent_incoming.sh
```

### 🔧 Setup Commands by IDE

#### Universal Setup (All IDEs)
```bash
# 1. Copy package files to project root
# 2. Run setup script
python3 setup_workflow_system.py

# The script auto-detects your IDE and configures accordingly
```

#### VS Code Specific
```bash
# After setup, workflows available via:
# Ctrl+Shift+P → Tasks: Run Task → [Workflow Name]

# Or via npm (if Node.js project):
npm run workflow:incoming
npm run agent:hi
```

#### Terminal-Only IDEs
```bash
# Direct command execution:
python3 codebase_summary/agent_workflow_orchestrator.py incoming

# Or use generated shell scripts:
chmod +x .workflow_system/scripts/*.sh
./.workflow_system/scripts/agent_incoming.sh
```

## 🚨 Critical: Git Hook Avoidance Strategy

### The Problem
Direct shell command execution can trigger Git hooks that cause:
- "nothing to commit" messages
- Process termination and halts
- Inability to wait for command completion
- Workflow interruption

### The Solution - Command Execution Priority:

1. **PRIMARY**: Replit Native Workflows
   - Use workflow panel buttons (Agent Incoming/Outgoing)
   - Executes Python scripts without Git interference
   - Maintains process control and completion waiting

2. **SECONDARY**: File-Based Operations
   - Read project state through file parsing
   - Use `workflow_status_checker.py` for status
   - Direct file modification instead of shell commands

3. **LAST RESORT**: Direct Shell Commands
   - Only when workflows AND file operations fail
   - Expect potential Git hook interruptions
   - May require manual intervention

### 📝 Configuration Files by IDE

#### VS Code / Cursor
```
.vscode/
├── tasks.json          # Workflow task definitions
├── settings.json       # Workspace settings
└── extensions.json     # Recommended extensions
```

#### Replit
```
.replit                 # Workflow definitions added to existing config
```

#### Gitpod
```
.gitpod.yml            # Workspace configuration
```

#### Universal
```
.workflow_system/
├── scripts/
│   ├── agent_incoming.sh
│   ├── agent_outgoing.sh
│   └── update_changelog.sh
└── ide_configs/       # IDE-specific configurations
```

### 🎪 Execution Methods Comparison

| IDE | Method 1 | Method 2 | Method 3 |
|-----|----------|----------|----------|
| **Replit** | Workflow Panel | Terminal | - |
| **VS Code** | Command Palette | Terminal | npm scripts |
| **Cursor** | Command Palette | Terminal | npm scripts |
| **Codespaces** | Tasks | Terminal | npm scripts |
| **Gitpod** | Terminal | Tasks | npm scripts |
| **Other** | Terminal | Shell Scripts | npm scripts |

### 🚀 AI Assistant Integration Examples

#### Example 1: Cline in VS Code
```typescript
// Cline can be instructed to:
// "Run the incoming agent workflow"
// This triggers: Ctrl+Shift+P → Tasks: Run Task → Agent Incoming Workflow
```

#### Example 2: Claude in Terminal
```bash
# Claude can execute:
"Please run the incoming agent workflow"
# Results in: python3 codebase_summary/agent_workflow_orchestrator.py incoming
```

#### Example 3: Cursor AI Native
```javascript
// Cursor AI can directly trigger workflows through task system
// while maintaining full context of the conversation
```

### 🔄 Workflow Triggers by Environment

#### Greeting Triggers ("Hi", "Hello")
- **Replit**: Auto-triggers "Agent Incoming Workflow"
- **VS Code**: Prompts to run incoming task
- **Terminal**: Suggests command execution
- **All IDEs**: Consistent behavior across environments

#### Changelog Triggers ("Update the changelog")
- **All IDEs**: Triggers outgoing workflow with session documentation
- **Method varies**: Task runner, workflow panel, or terminal command
- **Consistent result**: Same changelog update across all environments

### ⚡ Performance Optimization by IDE

#### Replit
- Prevents duplicate workflow executions
- Manages hot reload cycles
- Optimizes checkpoint creation

#### VS Code/Cursor
- Terminal session reuse
- Task result caching
- Extension compatibility checks

#### Cloud IDEs (Codespaces/Gitpod)
- Environment persistence
- Resource usage optimization
- Network-aware execution

### 🛠 Troubleshooting by IDE

#### Common Issues

**VS Code/Cursor**: 
- Tasks not appearing → Check `.vscode/tasks.json` exists
- Python not found → Verify Python extension installed

**Replit**:
- Workflows missing → Check `.replit` configuration
- Port conflicts → Run port cleanup script

**Terminal-based**:
- Permission denied → Run `chmod +x .workflow_system/scripts/*.sh`
- Python not found → Verify `python3` command available

**All IDEs**:
- Workflow fails → Check `workflow_config.json` syntax
- Files missing → Re-run setup script

This integration system ensures that regardless of your IDE choice or AI assistant preference, you get consistent, reliable workflow orchestration with seamless agent handoffs.
