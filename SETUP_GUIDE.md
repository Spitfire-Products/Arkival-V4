# Workflow System Setup Guide - REPLIT

## Quick Start
1. The workflow system has been automatically configured for REPLIT
2. Test the system by running the incoming workflow
3. Begin development with full agent handoff support

## Available Workflows

### Agent Incoming Workflow
**Purpose**: Load context when starting a new session

**How to run**: 
- Click on "Agent Incoming Workflow" in the workflows panel
- Or use the terminal: `python3 codebase_summary/agent_workflow_orchestrator.py incoming`

### Update Changelog
**Purpose**: Add entries to project changelog

## AI Agent Integration

### After Setup - Important Next Steps:
1. **Edit `workflow_config.json`** with your project-specific details:
   - Update `project_name` and `technology_stack`
   - Add `main_files` and `important_directories`
   - Customize integration notes for your development workflow

2. **AI Agent Onboarding Process**:
   - The AI agent you're working with should **analyze your project structure**
   - Ask the agent to **update workflow_config.json** with detected technology stack
   - Request the agent to **configure project-specific settings** based on your codebase

### Example Agent Instructions:
```
"Analyze this project and update workflow_config.json with the correct technology stack, main files, and project-specific configuration. This is a [your-tech-stack] project with [key-features]."
```

### What the AI Agent Should Configure:
- **Technology Stack Detection** (Vite, React, Three.js, SpacetimeDB, etc.)
- **Main Files Identification** (package.json, vite.config.ts, src/main.tsx)
- **Important Directories** (src, public, components, etc.)
- **Integration Notes** for your specific development workflow

## IDE Integration Features
- **Detected IDE**: REPLIT
- **Workflow Method**: replit_workflows
- **Task Runner**: replit_workflows

## Troubleshooting
- Ensure Python 3.7+ is available in your terminal
- Check that all files in `codebase_summary/` directory exist
- Verify workflow configuration files are present
- If workflow_config.json needs updates, ask your AI agent to analyze and configure it

## Customization
Edit `workflow_config.json` to customize the system for your project needs, or ask your AI agent to configure it based on your project structure.
