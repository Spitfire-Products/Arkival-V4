# Claude Code Integration Module

## Quick Installation & Setup

### 1. Install Claude Code CLI
```bash
# Install globally via npm
npm install -g @anthropic-ai/claude-code

# Verify installation
claude --version
```

### 2. Authenticate with Claude
```bash
# Login to Claude (opens browser for OAuth)
claude auth

# Verify authentication
claude auth status
```

### 3. Test Direct Communication
```bash
# Test the bridge
python3 modules/claude-code/claude_bridge.py test

# Send a message
python3 modules/claude-code/claude_bridge.py "Hello Claude!"
```

## Usage Options

### Option 1: Direct Bridge Communication (Recommended)
Use the Claude Bridge for reliable direct communication:

```bash
# From project root
python3 modules/claude-code/claude_bridge.py "Your message here"

# Collaboration request
python3 modules/claude-code/claude_bridge.py collab "Help me debug this code"

# Test connection
python3 modules/claude-code/claude_bridge.py test
```

### Option 2: Message System (Fallback)
Use the message system for coordination when direct communication isn't available:

```bash
# Add a message for Claude
python3 modules/claude-code/msg.py add claude_code "Please review the authentication system"

# Add a message from Claude  
python3 modules/claude-code/msg.py add human "I've reviewed the code, here are my suggestions..."

# List all messages
python3 modules/claude-code/msg.py list

# Get latest message
python3 modules/claude-code/msg.py latest
```

## File Overview

| File | Purpose |
|------|---------|
| `claude_bridge.py` | Direct communication with Claude CLI |
| `CLAUDE_BRIDGE_GUIDE.md` | Detailed bridge documentation |
| `msg.py` | Message coordination system |
| `msgs.md` | Message log file |
| `README.md` | This setup guide |

## When to Use Each Method

### Use Claude Bridge When:
- ✅ Claude Code CLI is installed and authenticated
- ✅ You need real-time responses
- ✅ Direct communication is working
- ✅ You want immediate collaboration

### Use Message System When:
- 🔄 Setting up initial communication
- 🔄 Claude CLI authentication issues
- 🔄 Fallback coordination needed
- 🔄 Asynchronous message exchange

## Integration with Arkival Workflows

### From Agent Workflow Orchestrator
```python
# In codebase_summary/agent_workflow_orchestrator.py
import sys
sys.path.append('modules/claude-code')
from claude_bridge import ClaudeBridge

def handoff_to_claude(session_summary):
    bridge = ClaudeBridge()
    result = bridge.collaborate(f"Taking over session: {session_summary}")
    return result
```

### From Setup Scripts
```bash
# In setup_workflow_system.py or other scripts
python3 modules/claude-code/claude_bridge.py collab "Setup complete, ready for development"
```

## Troubleshooting

### "Claude CLI not found"
```bash
# Install or update Claude CLI
npm install -g @anthropic-ai/claude-code
npm update -g @anthropic-ai/claude-code
```

### Authentication Issues
```bash
# Re-authenticate
claude auth logout
claude auth

# Check status
claude auth status
```

### Communication Failures
```bash
# Test bridge
python3 modules/claude-code/claude_bridge.py test

# Fallback to message system
python3 modules/claude-code/msg.py add claude_code "Please respond when available"
```

## Quick Commands Reference

```bash
# Installation
npm install -g @anthropic-ai/claude-code && claude auth

# Test
python3 modules/claude-code/claude_bridge.py test

# Message
python3 modules/claude-code/claude_bridge.py "Your message"

# Collaborate  
python3 modules/claude-code/claude_bridge.py collab "Task description"

# Fallback messaging
python3 modules/claude-code/msg.py add claude_code "Coordination message"
```

This module provides both robust direct communication and reliable fallback messaging for seamless Claude Code integration with Arkival workflows.