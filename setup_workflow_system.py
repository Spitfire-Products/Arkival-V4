#!/usr/bin/env python3
"""
Cross-Platform Workflow System Setup Script
Automatically configures the agent workflow orchestration system for any IDE/environment
"""

import os
import json
import shutil
import sys
import platform
from pathlib import Path
from datetime import datetime

# Validate required dependencies
def validate_dependencies():
    """
    # @codebase-summary: Cross-platform dependency validation system
    - Validates Python standard library availability for workflow system
    - Ensures compatibility across different IDE environments
    - Used by: setup automation, environment validation, deployment checks
    """
    try:
        import json, os, shutil, platform
        from pathlib import Path
        from datetime import datetime
        return True
    except ImportError as e:
        print(f"❌ Missing required dependency: {e}")
        print("Please ensure Python 3.7+ is installed with standard libraries")
        return False

class WorkflowSystemSetup:
    """
    # @codebase-summary: Core workflow system setup orchestrator
    - Manages cross-platform workflow system installation and configuration
    - Detects IDE environment and adapts setup procedures accordingly
    - Handles file copying, configuration, and validation
    - Used by: project initialization, environment setup, deployment automation
    """
    def __init__(self):
        self.project_root = Path.cwd()
        self.package_root = Path(__file__).parent
        self.detected_ide = self._detect_ide_environment()

    def _detect_ide_environment(self):
        """Detect the current IDE/development environment"""
        # Check for various IDE indicators
        if os.environ.get('REPLIT_DB_URL'):
            return 'replit'
        elif os.environ.get('CODESPACES'):
            return 'codespaces'
        elif os.environ.get('GITPOD_WORKSPACE_URL'):
            return 'gitpod'
        elif (self.project_root / '.vscode').exists():
            return 'vscode'
        elif (self.project_root / '.cursor').exists():
            return 'cursor'
        elif os.environ.get('WINDSURF_SESSION'):
            return 'windsurf'
        elif os.environ.get('LOVABLE_PROJECT'):
            return 'lovable'
        else:
            return 'generic'

    def setup_complete_system(self):
        """
        # @codebase-summary: Complete workflow system setup orchestrator
        - Manages full workflow system installation across all supported platforms
        - Handles IDE detection, configuration, and validation
        - Provides comprehensive setup with error handling and recovery
        - Used by: project initialization, system deployment, environment setup
        """
        """Set up the complete workflow orchestration system"""
        print("🚀 SETTING UP CROSS-PLATFORM AGENT WORKFLOW ORCHESTRATION SYSTEM")
        print("=" * 70)
        print(f"📍 Detected environment: {self.detected_ide.upper()}")

        try:
            # Step 1: Create directory structure
            self._create_directory_structure()

            # Step 2: Copy core system files
            self._copy_core_files()

            # Step 3: Initialize project configuration
            self._initialize_project_config()

            # Step 4: Set up changelog system
            self._initialize_changelog()

            # Step 5: Configure IDE-specific workflows
            self._setup_ide_workflows()

            # Step 6: Create initial documentation
            self._create_initial_documentation()

            # Step 6.5: Create community standards files
            self._create_community_standards_files()

            # Step 7: Set up IDE integration files
            self._setup_ide_integration()

            # Step 8: Run initial system check
            self._run_system_verification()

            print("\n✅ WORKFLOW SYSTEM SETUP COMPLETED SUCCESSFULLY!")
            print("=" * 70)
            print("Next steps:")
            print("1. Edit workflow_config.json with your project details")
            print("2. Review IDE-specific setup instructions in SETUP_GUIDE.md")
            print("3. Say 'Hi' to test the incoming agent workflow")
            print("4. Begin development with full workflow support")
            print("\n🔍 Running post-setup validation...")
            self._validate_deployment()
            
            print("\n🔬 Running comprehensive deployment validation...")
            self._run_comprehensive_validation()
            
            print("\n🧪 AVAILABLE TESTING OPTIONS:")
            print("=" * 40)
            print("📋 System Validation (Recommended):")
            print("   python3 validate_deployment.py")
            print("")
            print("💡 Run any of these commands to validate specific functionality")
            
            # Ask if user wants to run basic tests
            self._prompt_for_testing()

        except Exception as e:
            print(f"❌ Setup failed: {e}")
            sys.exit(1)

    def _create_directory_structure(self):
        """Create necessary directory structure"""
        directories = [
            "codebase_summary",
            "codebase_summary/history",
            "attached_assets",
            "reference_assets",
            "reference_assets/workflow_docs",
            ".workflow_system",
            ".workflow_system/scripts",
            ".workflow_system/ide_configs"
        ]

        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"📁 Created directory: {directory}")

    def _copy_core_files(self):
        """Copy core system files to project"""
        core_files = [
            ("codebase_summary/agent_workflow_orchestrator.py", "codebase_summary/agent_workflow_orchestrator.py"),
            ("codebase_summary/update_changelog.py", "codebase_summary/update_changelog.py"),
            ("codebase_summary/update_project_summary.py", "codebase_summary/update_project_summary.py"),
            ("NEW_AGENT_GREETING.md", "NEW_AGENT_GREETING.md"),
            ("DEVELOPER_ONBOARDING.md", "DEVELOPER_ONBOARDING.md"),
            ("workflow_assets/workflow_docs/breadcrumb_guide.md", "codebase_summary/breadcrumb_guide.md"),
            ("workflow_assets/workflow_docs/engineering_best_practices.md", "codebase_summary/engineering_best_practices.md")
        ]

        for source, dest in core_files:
            source_path = self.package_root / source
            dest_path = self.project_root / dest

            # Skip if source and destination are the same file
            if source_path.resolve() == dest_path.resolve():
                print(f"✅ Already exists: {dest}")
                continue

            if source_path.exists():
                shutil.copy2(source_path, dest_path)
                print(f"📄 Copied: {dest}")
            else:
                print(f"⚠️  Source file not found: {source}")

    def _initialize_project_config(self):
        """Initialize project configuration with IDE detection"""
        config = {
            "project_name": "New Project",
            "project_description": "AI-powered application with workflow orchestration",
            "version": "1.0.0",
            "technology_stack": ["Generic"],
            "environment": {
                "detected_ide": self.detected_ide,
                "platform": platform.system(),
                "supports_integrated_terminal": True,
                "supports_tasks": self.detected_ide in ['vscode', 'cursor', 'codespaces']
            },
            "workflow_settings": {
                "auto_changelog": True,
                "auto_documentation": True,
                "cost_optimization": True,
                "agent_handoff_enabled": True,
                "ide_integration": True
            },
            "customization": {
                "greeting_triggers": ["hi", "hello", "hey"],
                "changelog_triggers": ["update the changelog", "update changelog"],
                "documentation_required": True,
                "terminal_commands": True
            },
            "ide_specific": {
                "workflow_method": self._get_workflow_method(),
                "terminal_integration": True,
                "task_runner": self._get_task_runner(),
                "extensions_recommended": self._get_recommended_extensions()
            },
            "setup_timestamp": datetime.now().isoformat() + "Z"
        }

        config_path = self.project_root / "workflow_config.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)

        print(f"⚙️  Created workflow_config.json for {self.detected_ide}")

    def _get_workflow_method(self):
        """Get the workflow method based on IDE"""
        workflow_methods = {
            'replit': 'replit_workflows',
            'vscode': 'vscode_tasks',
            'cursor': 'vscode_tasks',
            'codespaces': 'vscode_tasks', 
            'gitpod': 'gitpod_tasks',
            'windsurf': 'shell_scripts',
            'lovable': 'shell_scripts',
            'generic': 'shell_scripts'
        }
        return workflow_methods.get(self.detected_ide, 'shell_scripts')

    def _get_task_runner(self):
        """Get recommended task runner for IDE"""
        task_runners = {
            'replit': 'replit_workflows',
            'vscode': 'vscode_tasks',
            'cursor': 'vscode_tasks',
            'codespaces': 'vscode_tasks',
            'gitpod': 'gitpod_tasks',
            'windsurf': 'npm_scripts',
            'lovable': 'npm_scripts',
            'generic': 'shell_scripts'
        }
        return task_runners.get(self.detected_ide, 'shell_scripts')

    def _get_recommended_extensions(self):
        """Get recommended extensions for IDE"""
        if self.detected_ide in ['vscode', 'cursor', 'codespaces']:
            return [
                "ms-python.python",
                "ms-vscode.vscode-json",
                "bradlc.vscode-tailwindcss",
                "esbenp.prettier-vscode"
            ]
        return []

    def _setup_ide_workflows(self):
        """Set up IDE-specific workflow configurations"""
        if self.detected_ide == 'replit':
            self._setup_replit_workflows()
        elif self.detected_ide in ['vscode', 'cursor', 'codespaces']:
            self._setup_vscode_tasks()
        elif self.detected_ide == 'gitpod':
            self._setup_gitpod_tasks()
        else:
            self._setup_shell_scripts()

    def _setup_replit_workflows(self):
        """Set up Replit workflows with proper .replit file integration"""
        # Create .replit file with workflow integration
        replit_file_config = '''modules = ["python-3.11", "nodejs-20", "python3"]

[nix]
channel = "stable-24_05"
packages = ["libyaml"]

[[workflows.workflow]]
name = "Agent Incoming Workflow"
author = "workflow-system"
mode = "sequential"

[[workflows.workflow.tasks]]
task = "shell.exec"
args = "echo '🎯 NEW AGENT ONBOARDING WORKFLOW'"

[[workflows.workflow.tasks]]
task = "shell.exec"
args = "python3 codebase_summary/agent_workflow_orchestrator.py incoming"

[[workflows.workflow]]
name = "Agent Outgoing Workflow"
author = "workflow-system"
mode = "sequential"

[[workflows.workflow.tasks]]
task = "shell.exec"
args = "echo '🚀 OUTGOING AGENT HANDOFF WORKFLOW'"

[[workflows.workflow.tasks]]
task = "shell.exec"
args = "python3 codebase_summary/agent_workflow_orchestrator.py outgoing --summary \\"Session summary\\" --type completed"
'''

        # Write the main .replit file
        replit_file_path = self.project_root / ".replit"
        with open(replit_file_path, 'w', encoding='utf-8') as f:
            f.write(replit_file_config)

        # Also create backup in .workflow_system for reference
        workflow_path = self.project_root / ".workflow_system" / "replit_workflows.toml"
        workflow_only_config = '''[[workflows.workflow]]
name = "Agent Incoming Workflow"
author = "workflow-system"
mode = "sequential"

[[workflows.workflow.tasks]]
task = "shell.exec"
args = "echo '🎯 NEW AGENT ONBOARDING WORKFLOW'"

[[workflows.workflow.tasks]]
task = "shell.exec"
args = "python3 codebase_summary/agent_workflow_orchestrator.py incoming"

[[workflows.workflow]]
name = "Agent Outgoing Workflow"
author = "workflow-system"
mode = "sequential"

[[workflows.workflow.tasks]]
task = "shell.exec"
args = "echo '🚀 OUTGOING AGENT HANDOFF WORKFLOW'"

[[workflows.workflow.tasks]]
task = "shell.exec"
args = "python3 codebase_summary/agent_workflow_orchestrator.py outgoing --summary \\"Session summary\\" --type completed"
'''
        with open(workflow_path, 'w', encoding='utf-8') as f:
            f.write(workflow_only_config)

        print("🔧 Created Replit .replit file with integrated workflows")
        print("🔧 Created Replit workflow configuration backup")

    def _setup_vscode_tasks(self):
        """Set up VS Code tasks.json"""
        vscode_tasks = {
            "version": "2.0.0",
            "tasks": [
                {
                    "label": "Agent Incoming Workflow",
                    "type": "shell",
                    "command": "python3",
                    "args": ["codebase_summary/agent_workflow_orchestrator.py", "incoming"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared"
                    },
                    "problemMatcher": []
                },
                {
                    "label": "Agent Outgoing Workflow",
                    "type": "shell",
                    "command": "python3",
                    "args": ["codebase_summary/agent_workflow_orchestrator.py", "outgoing", "--summary", "${input:sessionSummary}", "--type", "${input:sessionType}"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared"
                    },
                    "problemMatcher": []
                },
                {
                    "label": "Update Changelog",
                    "type": "shell",
                    "command": "python3",
                    "args": ["codebase_summary/update_changelog.py", "add", "--summary", "${input:changelogSummary}"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared"
                    },
                    "problemMatcher": []
                }
            ],
            "inputs": [
                {
                    "id": "sessionSummary",
                    "description": "Session summary for handoff",
                    "default": "Completed development session",
                    "type": "promptString"
                },
                {
                    "id": "sessionType",
                    "description": "Session completion type",
                    "default": "completed",
                    "type": "pickString",
                    "options": ["completed", "unresolved", "partial"]
                },
                {
                    "id": "changelogSummary",
                    "description": "Changelog entry summary",
                    "default": "Updated project features",
                    "type": "promptString"
                }
            ]
        }

        vscode_dir = self.project_root / ".vscode"
        vscode_dir.mkdir(exist_ok=True)

        tasks_path = vscode_dir / "tasks.json"
        with open(tasks_path, 'w', encoding='utf-8') as f:
            json.dump(vscode_tasks, f, indent=2)

        print("🔧 Created VS Code tasks.json")

    def _setup_gitpod_tasks(self):
        """Set up Gitpod tasks in .gitpod.yml"""
        gitpod_config = """
tasks:
  - name: Agent Workflow System
    init: |
      echo "🎯 Agent Workflow System Ready"
      echo "Available commands:"
      echo "- gp tasks:run 'Agent Incoming Workflow'"
      echo "- gp tasks:run 'Agent Outgoing Workflow'"
    command: |
      echo "Workflow system ready. Use 'python3 codebase_summary/agent_workflow_orchestrator.py incoming' to start."

vscode:
  extensions:
    - ms-python.python
    - ms-vscode.vscode-json
"""

        gitpod_path = self.project_root / ".gitpod.yml"
        with open(gitpod_path, 'w', encoding='utf-8') as f:
            f.write(gitpod_config)

        print("🔧 Created .gitpod.yml configuration")

    def _setup_shell_scripts(self):
        """Set up shell scripts for generic IDE environments"""
        scripts = {
            "agent_incoming.sh": """#!/bin/bash
echo "🎯 NEW AGENT ONBOARDING WORKFLOW"
echo "================================"
python3 codebase_summary/agent_workflow_orchestrator.py incoming
echo ""
echo "✅ Incoming workflow completed."
""",
            "agent_outgoing.sh": """#!/bin/bash
echo "🚀 OUTGOING AGENT HANDOFF WORKFLOW"
echo "=================================="
if [ -z "$1" ]; then
    echo "Usage: ./agent_outgoing.sh \"Session summary\" [completed|unresolved]"
    echo "Example: ./agent_outgoing.sh \"Implemented new features\" completed"
    exit 1
fi
SUMMARY="$1"
TYPE="${2:-completed}"
python3 codebase_summary/agent_workflow_orchestrator.py outgoing --summary "$SUMMARY" --type "$TYPE"
""",
            "update_changelog.sh": """#!/bin/bash
if [ -z "$1" ]; then
    echo "Usage: ./update_changelog.sh \"Change summary\""
    echo "Example: ./update_changelog.sh \"Added new login functionality\""
    exit 1
fi
python3 codebase_summary/update_changelog.py add --summary "$1"
"""
        }

        scripts_dir = self.project_root / ".workflow_system" / "scripts"

        for script_name, script_content in scripts.items():
            script_path = scripts_dir / script_name
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(script_content)

            # Make scripts executable on Unix systems
            if platform.system() != 'Windows':
                os.chmod(script_path, 0o755)

        print("🔧 Created shell scripts for workflow execution")

    def _initialize_changelog(self):
        """Initialize changelog system (existing functionality)"""
        changelog = {
            "project_name": "New Project",
            "changelog_version": "1.0.0",
            "last_updated": datetime.now().isoformat() + "Z",
            "description": "Comprehensive changelog tracking all significant changes",
            "environment": {
                "ide": self.detected_ide,
                "platform": platform.system(),
                "workflow_method": self._get_workflow_method()
            },
            "team_workflow": {
                "update_instructions": "When asked to 'update the changelog from the last entry', analyze the collaboration session and document completed work or unresolved issues",
                "quick_start": f"Run: {self._get_changelog_command()}",
                "attribution": "Author should be the team member who collaborated on the work"
            },
            "entries": [
                {
                    "id": "change_001",
                    "timestamp": datetime.now().isoformat() + "Z",
                    "author": "Workflow System",
                    "version": "1.0.0",
                    "type": "feature",
                    "scope": "infrastructure",
                    "summary": "Initialized cross-platform agent workflow orchestration system",
                    "description": f"Set up complete workflow system with agent handoff, changelog management, and documentation automation for {self.detected_ide.upper()} environment",
                    "files_changed": [
                        {
                            "file": "multiple",
                            "action": "created",
                            "changes": ["Cross-platform workflow orchestration system files"]
                        }
                    ],
                    "breaking_changes": False,
                    "migration_notes": "No migration required - initial setup",
                    "related_issues": [],
                    "tags": ["setup", "workflow", "infrastructure", self.detected_ide]
                }
            ],
            "statistics": {
                "total_entries": 1,
                "entries_by_type": {"feature": 1},
                "entries_by_scope": {"infrastructure": 1}
            }
        }

        changelog_path = self.project_root / "changelog_summary.json"
        with open(changelog_path, 'w', encoding='utf-8') as f:
            json.dump(changelog, f, indent=2)

        print("📝 Created changelog_summary.json")

    def _get_changelog_command(self):
        """Get appropriate changelog command for the IDE"""
        if self.detected_ide in ['vscode', 'cursor', 'codespaces']:
            return "Ctrl+Shift+P -> Tasks: Run Task -> Update Changelog"
        elif self.detected_ide == 'replit':
            return "Use 'Agent Outgoing Workflow' from workflows menu"
        else:
            return "./.workflow_system/scripts/update_changelog.sh 'Summary'"

    def _create_initial_documentation(self):
        """Create initial project documentation (existing functionality enhanced)"""
        codebase_summary = {
            "project_name": "New Project",
            "version": "1.0.0",
            "last_updated": datetime.now().isoformat() + "Z",
            "description": "Project with cross-platform agent workflow orchestration system",
            "technology_stack": ["Generic"],
            "environment": {
                "ide": self.detected_ide,
                "platform": platform.system(),
                "workflow_integration": self._get_workflow_method()
            },
            "workflow_system": {
                "enabled": True,
                "version": "1.0.0",
                "cross_platform": True,
                "features": [
                    "Agent handoff automation",
                    "Changelog management",
                    "Documentation tracking",
                    "Cost optimization",
                    "Cross-IDE compatibility"
                ]
            },
            "statistics": {
                "total_files": 0,
                "documented_functions": 0,
                "missing_breadcrumbs": []
            }
        }

        summary_path = self.project_root / "codebase_summary" / "codebase_summary.json"
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(codebase_summary, f, indent=2)

        print("📊 Created codebase_summary.json")

    def _create_community_standards_files(self):
        """Create GitHub community standards files"""
        # Create .gitignore
        gitignore_content = """# Dependencies
node_modules/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
pip-log.txt
pip-delete-this-directory.txt
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git
.mypy_cache
.pytest_cache
.hypothesis

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Build outputs
dist/
build/
*.egg-info/
.parcel-cache/

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Temporary files
*.tmp
*.temp
.tmp/
temp/

# Logs
logs/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Runtime data
pids/
*.pid
*.seed
*.pid.lock

# System files
.workflow_system/logs/
.workflow_system/backups/
codebase_summary/history/
"""

        gitignore_path = self.project_root / ".gitignore"
        with open(gitignore_path, 'w', encoding='utf-8') as f:
            f.write(gitignore_content)

        # Create LICENSE (Attribution to Spitfire Products)
        license_content = """Attribution License

Copyright (c) 2025 Spitfire Products

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

Attribution to Spitfire Products must be maintained in all copies, substantial
portions, derivative works, and distributions of the Software. This includes
but is not limited to:
- Source code headers and comments
- Documentation and README files
- User interfaces and about pages
- Distribution packages and releases

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Original work by Spitfire Products
Arkival - AI Agent Workflow Orchestration System
"""

        license_path = self.project_root / "LICENSE"
        with open(license_path, 'w', encoding='utf-8') as f:
            f.write(license_content)

        # Create CONTRIBUTING.md
        contributing_content = """# Contributing to Arkival

Thank you for your interest in contributing! Arkival enables seamless knowledge transfer between AI agents and human developers across different development environments.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Run the setup script: `python3 setup_workflow_system.py`
4. Test your changes with: `python3 validate_deployment.py`

## Development Process

### Setting up the Development Environment

```bash
# Clone the repository
git clone https://github.com/spitfire-products/arkival.git
cd arkival

# Run the setup
python3 setup_workflow_system.py

# Validate the setup
python3 validate_deployment.py
```

### Making Changes

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Add tests for new functionality
4. Validate the setup: `python3 validate_deployment.py`
5. Update documentation as needed
6. Commit your changes with clear messages

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings for all functions and classes
- Include breadcrumb documentation using `@codebase-summary:` format

### Testing

- Write tests for new features
- Ensure all tests pass before submitting
- Test across different IDE environments when possible

### Documentation

- Update README.md if needed
- Add or update docstrings
- Include examples for new features
- Update CHANGELOG.md following semantic versioning

## Submitting Changes

1. Push your branch to your fork
2. Submit a pull request
3. Describe your changes clearly
4. Link any related issues

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help maintain a welcoming environment for all contributors

## Questions?

- Open an issue for bugs or feature requests
- Start a discussion for general questions
- Check existing issues before creating new ones

Thank you for contributing to making AI agent workflows more efficient!
"""

        contributing_path = self.project_root / "CONTRIBUTING.md"
        with open(contributing_path, 'w', encoding='utf-8') as f:
            f.write(contributing_content)

        # Create SECURITY.md
        security_content = """# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security vulnerabilities in Arkival seriously.

### How to Report

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please send a report to the maintainers privately. Include:

- Type of issue (e.g. buffer overflow, SQL injection, cross-site scripting)
- Full paths of source file(s) related to the manifestation of the issue
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit the issue

### Response Timeline

- We will acknowledge receipt of your vulnerability report within 48 hours
- We will provide a detailed response within 7 days indicating next steps
- We will work on a fix and coordinate disclosure timeline with you

### Security Best Practices

When using this system:

1. **API Keys**: Never commit API keys or sensitive credentials to version control
2. **Environment Variables**: Use environment variables for sensitive configuration
3. **File Permissions**: Ensure proper file permissions on system files
4. **Updates**: Keep the system updated to the latest version
5. **Validation**: Validate all inputs and outputs in your workflows

### Safe Usage Guidelines

- Run the system in isolated environments when possible
- Regularly update dependencies
- Monitor system logs for unusual activity
- Use the built-in validation features
- Follow the principle of least privilege

Thank you for helping keep Arkival secure!
"""

        security_path = self.project_root / "SECURITY.md"
        with open(security_path, 'w', encoding='utf-8') as f:
            f.write(security_content)

        print("📋 Created community standards files (.gitignore, LICENSE, CONTRIBUTING.md, SECURITY.md)")

    def _setup_ide_integration(self):
        """Set up IDE-specific integration files"""
        # Create setup guide
        setup_guide = self._generate_setup_guide()
        guide_path = self.project_root / "SETUP_GUIDE.md"
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(setup_guide)

        # Create IDE-specific settings if applicable
        if self.detected_ide in ['vscode', 'cursor', 'codespaces']:
            self._create_vscode_settings()

        print(f"📖 Created setup guide for {self.detected_ide.upper()}")

    def _generate_setup_guide(self):
        """Generate IDE-specific setup guide"""
        base_guide = f"""# Workflow System Setup Guide - {self.detected_ide.upper()}

## Quick Start
1. The workflow system has been automatically configured for {self.detected_ide.upper()}
2. Test the system by running the incoming workflow
3. Begin development with full agent handoff support

## Available Workflows

### Agent Incoming Workflow
**Purpose**: Load context when starting a new session
"""

        if self.detected_ide in ['vscode', 'cursor', 'codespaces']:
            base_guide += """
**How to run**: 
- Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
- Type "Tasks: Run Task"
- Select "Agent Incoming Workflow"

**Or use terminal**: `python3 codebase_summary/agent_workflow_orchestrator.py incoming`
"""
        elif self.detected_ide == 'replit':
            base_guide += """
**How to run**: 
- Click on "Agent Incoming Workflow" in the workflows panel
- Or use the terminal: `python3 codebase_summary/agent_workflow_orchestrator.py incoming`
"""
        else:
            base_guide += """
**How to run**: 
- Terminal: `python3 codebase_summary/agent_workflow_orchestrator.py incoming`
- Or: `./.workflow_system/scripts/agent_incoming.sh`
"""

        base_guide += f"""
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
- **Detected IDE**: {self.detected_ide.upper()}
- **Workflow Method**: {self._get_workflow_method()}
- **Task Runner**: {self._get_task_runner()}

## Troubleshooting
- Ensure Python 3.7+ is available in your terminal
- Check that all files in `codebase_summary/` directory exist
- Verify workflow configuration files are present
- If workflow_config.json needs updates, ask your AI agent to analyze and configure it

## Customization
Edit `workflow_config.json` to customize the system for your project needs, or ask your AI agent to configure it based on your project structure.
"""

        return base_guide

    def _create_vscode_settings(self):
        """Create VS Code specific settings"""
        vscode_settings = {
            "python.defaultInterpreterPath": "python3",
            "terminal.integrated.defaultProfile.linux": "bash",
            "terminal.integrated.defaultProfile.osx": "zsh",
            "files.associations": {
                "*.json": "jsonc"
            },
            "json.schemas": [
                {
                    "fileMatch": ["workflow_config.json"],
                    "schema": {
                        "type": "object",
                        "properties": {
                            "project_name": {"type": "string"},
                            "version": {"type": "string"},
                            "workflow_settings": {"type": "object"}
                        }
                    }
                }
            ]
        }

        vscode_dir = self.project_root / ".vscode"
        settings_path = vscode_dir / "settings.json"

        with open(settings_path, 'w', encoding='utf-8') as f:
            json.dump(vscode_settings, f, indent=2)

        print("⚙️  Created VS Code settings.json")

    def _run_system_verification(self):
        """Verify system setup (enhanced)"""
        required_files = [
            "codebase_summary/agent_workflow_orchestrator.py",
            "codebase_summary/update_changelog.py",
            "changelog_summary.json",
            "NEW_AGENT_GREETING.md",
            "workflow_config.json",
            "SETUP_GUIDE.md"
        ]

        # Add IDE-specific verification
        if self.detected_ide in ['vscode', 'cursor', 'codespaces']:
            required_files.extend([".vscode/tasks.json", ".vscode/settings.json"])
        elif self.detected_ide == 'gitpod':
            required_files.append(".gitpod.yml")
        else:
            required_files.extend([
                ".workflow_system/scripts/agent_incoming.sh",
                ".workflow_system/scripts/agent_outgoing.sh"
            ])

        print(f"\n🔍 VERIFYING SYSTEM SETUP FOR {self.detected_ide.upper()}...")
        all_good = True

        for file_path in required_files:
            file_full_path = self.project_root / file_path
            if file_full_path.exists():
                print(f"✅ {file_path}")
            else:
                print(f"❌ {file_path} - MISSING")
                all_good = False

        if all_good:
            print("✅ All required files present")
            print(f"🎯 System ready for {self.detected_ide.upper()} environment")
        else:
            print("❌ Some files are missing - setup may be incomplete")

        return all_good

    def _validate_deployment(self):
        """Validate deployment configuration"""
        issues = []
        
        # Check workflow_config.json
        config_path = self.project_root / "workflow_config.json"
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    
                if "NEEDS_CONFIGURATION" in config.get("technology_stack", []):
                    issues.append("⚠️  Technology stack needs AI agent configuration")
                    
                if config.get("project_name") == "New Project":
                    issues.append("⚠️  Project name should be customized")
                    
            except json.JSONDecodeError:
                issues.append("❌ workflow_config.json has invalid JSON")
        
        if issues:
            print("\n📋 POST-SETUP CONFIGURATION NEEDED:")
            for issue in issues:
                print(f"   {issue}")
            print("\n💡 Ask your AI agent to analyze the project and update workflow_config.json")
        else:
            print("✅ Deployment validation passed")
            
        return len(issues) == 0

    def _run_comprehensive_validation(self):
        """Run the comprehensive deployment validation script"""
        try:
            import subprocess
            result = subprocess.run([
                "python3", "validate_deployment.py"
            ], capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                print("✅ Comprehensive validation passed")
            else:
                print("⚠️  Comprehensive validation found issues:")
                print(result.stdout)
                print(result.stderr)
        except Exception as e:
            print(f"⚠️  Could not run comprehensive validation: {e}")
            print("💡 You can run it manually: python3 validate_deployment.py")

    def _prompt_for_testing(self):
        """Prompt user for interactive testing"""
        try:
            print(f"\n❓ Would you like to run basic feature testing now? (y/n): ", end="")
            response = input().lower().strip()
            
            if response in ['y', 'yes']:
                print("\n🧪 Running basic enhanced features test...")
                import subprocess
                result = subprocess.run([
                    "python3", "validate_deployment.py"
                ], cwd=self.project_root)
                
                if result.returncode == 0:
                    print("\n✅ Basic testing completed successfully!")
                else:
                    print("\n⚠️  Basic testing found some issues - review output above")
            else:
                print("\n⏭️  Skipping tests - you can run them anytime using the commands above")
        except (EOFError, KeyboardInterrupt):
            print("\n⏭️  Skipping interactive testing")
        except Exception as e:
            print(f"\n⚠️  Could not run interactive testing: {e}")

def main():
    """
    # @codebase-summary: Standard workflow system setup entry point
    - Main orchestrator for basic workflow system installation
    - Coordinates setup scripts and configuration validation
    - Used by: project initialization, basic setup procedures, system deployment
    """
    """Main setup function"""
    if not validate_dependencies():
        sys.exit(1)
    
    setup = WorkflowSystemSetup()
    setup.setup_complete_system()

if __name__ == "__main__":
    main()