# replit.md

## Overview

Arkival is a comprehensive AI Agent Workflow Orchestration System designed for seamless knowledge transfer between AI agents and human developers across different development environments. The system provides cross-platform compatibility, automated documentation generation, and intelligent workflow management.

## System Architecture

### Core Architecture Pattern
- **Workflow Orchestration System**: Manages agent handoffs and session continuity
- **Cross-Platform Deployment**: Supports both subdirectory integration and standalone deployment
- **Multi-Language Detection**: Comprehensive function detection across Python, TypeScript, JavaScript, and other languages
- **Configuration-Driven**: JSON-based configuration system with automatic environment detection

### Deployment Modes
1. **Subdirectory Mode**: Non-destructive integration into existing projects
2. **Development Mode**: Full integration for dedicated Arkival development
3. **Auto-Detection**: Intelligent detection of deployment context and IDE environment

## Key Components

### 1. Workflow Management
- **Agent Workflow Orchestrator** (`codebase_summary/agent_workflow_orchestrator.py`): Manages session handoffs and context preservation
- **Session State Management**: Maintains context across development sessions via `session_state.json`
- **Automated Handoff System**: Seamless transitions between AI agents and human developers

### 2. Documentation System
- **Project Summary Generator** (`codebase_summary/update_project_summary.py`): Creates comprehensive codebase documentation
- **Breadcrumb Documentation**: Standardized `@codebase-summary:` format for function documentation
- **Missing Documentation Tracking**: Identifies undocumented functions via `missing_breadcrumbs.json`

### 3. Version Management
- **Dual Version System**: Separate versioning for codebase analysis and project releases
- **Changelog Management** (`codebase_summary/update_changelog.py`): Automated changelog generation and tracking
- **Version Correlation**: Synchronizes versions across all system components

### 4. Cross-Platform Support
- **IDE Detection**: Automatic detection of Replit, VS Code, Cursor, GitHub Codespaces, and other environments
- **Universal Path Resolution**: Intelligent path detection across different deployment scenarios
- **Environment-Specific Configuration**: IDE-optimized workflows and task integration

## Data Flow

### Incoming Agent Workflow
1. Agent triggers incoming workflow (`python3 codebase_summary/agent_workflow_orchestrator.py incoming`)
2. System loads project context from `session_state.json`
3. Agent receives current project state, unresolved issues, and technical context
4. Development session begins with full context awareness

### Development Process
1. Code changes and feature development
2. Automatic breadcrumb documentation detection
3. Function analysis and documentation coverage tracking
4. Real-time project summary updates

### Outgoing Agent Workflow
1. Agent triggers outgoing workflow (changelog update)
2. Session summary generation with completed work documentation
3. Context preservation for next agent/developer
4. Automated handoff documentation creation

## External Dependencies

### Core Dependencies
- **Python 3.11+**: Primary runtime environment
- **Node.js 20**: For JavaScript/TypeScript analysis and client templates
- **Standard Libraries**: json, os, pathlib, datetime, subprocess

### Optional AI Integrations
- **Claude Code Integration**: Direct communication bridge via `modules/claude-code/`
- **Multi-Provider Support**: OpenAI, Google Gemini, Anthropic (configurable)
- **OAuth Authentication**: Reliable authentication mechanisms

### Development Tools
- **Cross-Platform Package Managers**: Support for npm, pip, poetry, cargo
- **Template System**: Project templates for Rust, Python, Node.js, and TypeScript
- **WebSocket Mitigation**: Development environment compatibility fixes

## Deployment Strategy

### Quick Start Options
1. **Subdirectory Integration** (Recommended for existing projects):
   ```bash
   git clone https://github.com/spitfire-products/arkival.git Arkival
   cd Arkival
   python3 setup_workflow_system.py
   ```

2. **Standalone Deployment**:
   ```bash
   git clone https://github.com/spitfire-products/arkival.git
   cd arkival
   python3 setup_workflow_system.py
   ```

### Validation and Testing
- **Deployment Validation**: `python3 validate_deployment.py`
- **System Testing**: `python3 codebase_summary/update_project_summary.py --force`
- **Export Readiness**: `python3 validate_export_readiness.py`

## Changelog

Changelog:
- June 20, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.