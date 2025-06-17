# Claude Bridge - Direct Communication Guide

## Overview

Claude Bridge enables direct communication between Replit agents and Claude with minimal setup. This replaces the complex `/modules/claude-integration/` system with a simple, reliable solution.

## Quick Start

### 1. Install Claude CLI (if not already installed)
```bash
npm install -g @anthropic-ai/claude-code
```

### 2. Test the Bridge
```bash
python3 claude_bridge.py test
```

### 3. Send a Message
```bash
python3 claude_bridge.py "Hello Claude, can you help me with Python?"
```

### 4. Collaboration Request
```bash
python3 claude_bridge.py collab "Debug this authentication error in my Flask app"
```

## Key Features

- **Minimal Setup**: Just one Python script, no complex configuration
- **Replit Optimized**: Handles git locks, terminal issues, and environment constraints
- **OAuth Authentication**: Uses reliable OAuth instead of problematic API keys
- **Error Handling**: Clear error messages and fallback options
- **CLI Interface**: Easy to use from command line or other scripts

## How It Works

### Environment Configuration
The bridge automatically sets optimal environment variables:
```bash
GIT_OPTIONAL_LOCKS=0          # Bypasses git repository locks
TERM=dumb                     # Avoids terminal compatibility issues
CLAUDE_DISABLE_RAW_MODE=1     # Prevents raw mode errors
# Removes ANTHROPIC_API_KEY   # Forces OAuth authentication
```

### Communication Method
Uses direct `subprocess` calls to Claude CLI with:
- 15-second timeout to prevent hanging
- Proper error capture and reporting
- OAuth authentication (more reliable than API keys)

## Usage Examples

### From Python Code
```python
from claude_bridge import ClaudeBridge

bridge = ClaudeBridge()

# Send message
result = bridge.send_message("Explain Python decorators")
if result['success']:
    print(result['response'])

# Collaboration request
result = bridge.collaborate("Help me optimize this database query")
if result['success']:
    print(result['response'])

# Test connection
status = bridge.test_connection()
print(f"Bridge status: {status['status']}")
```

### From Shell Scripts
```bash
# Test connection
python3 claude_bridge.py test

# Send message
python3 claude_bridge.py "What's the best way to handle errors in Python?"

# Collaboration
python3 claude_bridge.py collab "Review my API design for security issues"

# Use in scripts
RESPONSE=$(python3 claude_bridge.py "Generate a TODO list for my project")
echo "Claude's suggestions: $RESPONSE"
```

### Integration with Arkival Workflows
```python
# In agent_workflow_orchestrator.py or other Arkival scripts
from claude_bridge import ClaudeBridge

def handoff_to_claude(session_summary):
    bridge = ClaudeBridge()
    message = f"Taking over development session. Previous work: {session_summary}"
    result = bridge.collaborate(message)
    return result
```

## Troubleshooting

### Common Issues

**1. "Claude CLI not found"**
```bash
# Install Claude CLI
npm install -g @anthropic-ai/claude-code

# Or update if already installed
npm update -g @anthropic-ai/claude-code
```

**2. "Invalid API key" or authentication errors**
```bash
# Bridge automatically removes API key to force OAuth
# Make sure you're logged in with: claude auth
claude auth
```

**3. Command hangs or timeouts**
```bash
# Bridge automatically sets optimal environment
# If issues persist, check Claude CLI status
claude --version
```

**4. Git lock errors**
```bash
# Bridge automatically sets GIT_OPTIONAL_LOCKS=0
# If issues persist, manually clear locks
rm -f .git/index.lock
```

### Verification Commands
```bash
# Check Claude CLI installation
claude --version

# Test direct CLI (should work after bridge setup)
export GIT_OPTIONAL_LOCKS=0 TERM=dumb CLAUDE_DISABLE_RAW_MODE=1
claude --print "test message"

# Check authentication
claude auth status
```

## Why This Replaces the Complex System

The original `/modules/claude-integration/` had:
- 43 files with overlapping functionality
- Complex shell scripts and authentication bridges
- Multiple experimental communication methods
- Extensive documentation and configuration

**Claude Bridge provides the same core functionality with:**
- **1 Python script** (150 lines vs 1000+ lines)
- **1 documentation file** (this guide vs 13 documentation files)
- **Simple, proven approach** using direct Claude CLI calls
- **All essential features**: environment optimization, error handling, OAuth

## Advanced Usage

### Custom Timeouts
```python
bridge = ClaudeBridge()
result = bridge.send_message("Complex analysis task", timeout=60)  # 60 second timeout
```

### Error Handling
```python
bridge = ClaudeBridge()
result = bridge.send_message("Your message")

if result['success']:
    print(f"Claude responded: {result['response']}")
else:
    print(f"Communication failed: {result['error']}")
    # Implement fallback logic (file-based, message queue, etc.)
```

### Batch Operations
```python
bridge = ClaudeBridge()
tasks = ["Task 1", "Task 2", "Task 3"]

for task in tasks:
    result = bridge.collaborate(task)
    if result['success']:
        print(f"Task: {task}")
        print(f"Response: {result['response']}\n")
```

## Integration with Existing Arkival Features

Claude Bridge works seamlessly with:
- **Agent Workflow Orchestrator**: Use for session handoffs
- **Setup Workflow System**: Include in IDE task automation
- **Changelog Updates**: Get Claude input on changes
- **Cross-IDE Development**: Works in any environment with Python

The bridge maintains Arkival's core philosophy of cross-platform compatibility while providing reliable Claude communication with minimal complexity.

## Support

If you encounter issues:
1. Run `python3 claude_bridge.py test` to diagnose problems
2. Check Claude CLI installation with `claude --version`
3. Verify authentication with `claude auth status`
4. Review error messages for specific guidance

This minimal approach provides all the essential Claude communication features while being much easier to maintain and debug than the complex integration system.