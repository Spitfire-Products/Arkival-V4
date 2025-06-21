# Arkival - Replit Configuration Guide

## Overview

Arkival is an AI Agent Workflow Orchestration System designed for seamless knowledge transfer between AI agents and human developers. The system provides comprehensive multi-language function detection, automated documentation generation, and cross-platform IDE integration capabilities.

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

## Deployment Strategy

### Subdirectory Mode (Recommended for Existing Projects)
- Clone Arkival into existing project as `ProjectRoot/Arkival-V4/`
- Configuration stored at `ProjectRoot/arkival_config.json`
- Generated documentation reflects host project structure
- Non-destructive integration with existing codebases

### Standalone Mode (For New Projects)
- Direct deployment in project root
- Full feature access and development capabilities
- Ideal for projects built around Arkival workflows

### Cross-Platform IDE Support
- **Replit**: Native workflow panel integration with `.replit` configuration
- **VS Code/Cursor**: Task integration via `.vscode/tasks.json`
- **GitHub Codespaces**: Cloud-native browser development
- **Terminal-based**: Universal command-line interface

## Changelog

```
Changelog:
- June 21, 2025. Initial setup
```

## User Preferences

```
Preferred communication style: Simple, everyday language.
```