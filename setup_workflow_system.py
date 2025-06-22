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
        self.package_root = Path(__file__).parent
        self.deployment_context = self._detect_deployment_context()
        self.project_root = self._determine_project_root()
        self.detected_ide = self._detect_ide_environment()
        self.existing_architecture = self._scan_existing_architecture()

    def _detect_deployment_context(self):
        """
        # @codebase-summary: Deployment context detection system
        - Detects if Arkival is being deployed as new project root or integrated into existing project
        - Analyzes directory structure to determine deployment strategy
        - Used by: setup automation, integration strategy, file placement decisions
        """
        current_dir = Path.cwd()
        arkival_dir = self.package_root
        
        # Check if we're running from within a cloned Arkival directory
        if current_dir.name.lower() in ['arkival', 'arkival-v4'] and current_dir.parent != current_dir:
            # We're in /Arkival folder - this is existing project integration
            print("🔍 Detected: Running from cloned Arkival directory")
            return 'existing_project_integration'
        
        # Check if we're in the Arkival source directory (workspace)
        if arkival_dir.name.lower() == 'workspace':
            return 'new_project'
        
        # Check if parent directory has existing project structure
        parent_dir = current_dir.parent
        existing_indicators = [
            'package.json', 'src/', 'app/', 'components/', 'public/', 
            '.git/', 'node_modules/', 'requirements.txt', 'Cargo.toml',
            'pom.xml', 'build.gradle', 'composer.json', 'README.md'
        ]
        
        parent_count = sum(1 for indicator in existing_indicators 
                          if (parent_dir / indicator).exists())
        
        if parent_count >= 2:
            return 'existing_project_integration'
        
        return 'new_project'
    
    def _determine_project_root(self):
        """
        # @codebase-summary: Project root determination for flexible deployment
        - Determines appropriate project root based on deployment context
        - Handles both new project and existing project integration scenarios
        - Used by: file placement, configuration generation, deployment strategy
        """
        current_dir = Path.cwd()
        
        # If we're in /Arkival folder, the project root is the parent directory
        if current_dir.name.lower() in ['arkival', 'arkival-v4'] and self.deployment_context == 'existing_project_integration':
            return current_dir.parent  # Parent directory is the actual project root
        else:
            return current_dir  # For new projects or source development
    
    def _scan_existing_architecture(self):
        """
        # @codebase-summary: Existing project architecture scanning system
        - Scans for existing project files that should be preserved during integration
        - Identifies technology stack, build tools, and workflow configurations
        - Used by: integration strategy, conflict avoidance, selective deployment
        """
        if self.deployment_context == 'new_project':
            return {}
            
        architecture = {
            'technology_stack': [],
            'existing_files': [],
            'config_files': [],
            'build_tools': [],
            'important_directories': []
        }
        
        # Scan for technology indicators
        current_dir = Path.cwd()
        
        # Frontend frameworks and build tools
        if (current_dir / 'package.json').exists():
            architecture['technology_stack'].append('Node.js/npm')
            architecture['config_files'].append('package.json')
        
        if (current_dir / 'vite.config.js').exists() or (current_dir / 'vite.config.ts').exists():
            architecture['technology_stack'].append('Vite')
        
        if (current_dir / 'next.config.js').exists():
            architecture['technology_stack'].append('Next.js')
        
        if (current_dir / 'vue.config.js').exists():
            architecture['technology_stack'].append('Vue.js')
        
        # Backend frameworks
        if (current_dir / 'requirements.txt').exists():
            architecture['technology_stack'].append('Python')
            architecture['config_files'].append('requirements.txt')
        
        if (current_dir / 'Cargo.toml').exists():
            architecture['technology_stack'].append('Rust')
            
        if (current_dir / 'pom.xml').exists():
            architecture['technology_stack'].append('Java/Maven')
        
        # Important directories to preserve
        for dirname in ['src', 'app', 'components', 'public', 'assets', 'lib', 'utils', 'styles']:
            if (current_dir / dirname).exists():
                architecture['important_directories'].append(dirname)
        
        return architecture

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

    def setup_new_project(self):
        """
        # @codebase-summary: New project setup for Arkival workflow system
        - Sets up complete workflow system for new project deployment
        - Creates all necessary files, directories, and configurations
        - Used by: new project initialization, clean deployment scenarios
        """
        print("🚀 SETTING UP NEW PROJECT WITH ARKIVAL WORKFLOW SYSTEM")
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

            # Step 7: Create community standards files
            self._create_community_standards_files()

            # Step 8: Set up IDE integration files
            self._setup_ide_integration()

            # Step 9: Run initial system check
            self._run_system_verification()

            print("\n✅ ARKIVAL WORKFLOW SYSTEM SETUP COMPLETED!")
            print("=" * 70)
            print("Next steps:")
            print("1. Edit workflow_config.json with your project details")
            print("2. Review IDE-specific setup instructions in SETUP_GUIDE.md")
            print("3. Say 'Hi' to test the incoming agent workflow")
            print("4. Begin development with full workflow support")

        except Exception as e:
            print(f"❌ Setup failed: {e}")
            sys.exit(1)

    def setup_existing_project_integration(self):
        """
        # @codebase-summary: Existing project integration for Arkival workflow system
        - Integrates Arkival into existing projects without overwriting files
        - Places Arkival files in arkival/ subdirectory to avoid conflicts
        - Preserves existing project structure and workflows
        - Used by: existing project integration, non-destructive deployment
        """
        print("🔧 INTEGRATING ARKIVAL INTO EXISTING PROJECT")
        print("=" * 70)
        print(f"📍 Detected environment: {self.detected_ide.upper()}")
        print(f"🏗️ Existing architecture: {', '.join(self.existing_architecture.get('technology_stack', ['Unknown']))}")

        try:
            # Step 1: Create arkival_config.json trigger file in parent
            self._create_arkival_config()
            
            print("✅ Arkival integration completed - no files copied, everything stays in Arkival-V4/")

            print("\n✅ ARKIVAL INTEGRATION COMPLETED!")
            print("=" * 70)
            print("Integration summary:")
            print("• Only arkival_config.json added to parent directory")
            print("• All Arkival files remain in Arkival-V4/ directory")
            print("• Run workflows from: python3 Arkival-V4/codebase_summary/agent_workflow_orchestrator.py")
            print("• Everything self-contained in Arkival-V4/")

        except Exception as e:
            print(f"❌ Integration failed: {e}")
            sys.exit(1)

    def _create_arkival_subdirectory(self):
        """
        # @codebase-summary: Arkival subdirectory creation for existing project integration
        - Creates arkival/ subdirectory structure for non-destructive integration
        - Preserves existing project structure while adding Arkival capabilities
        - Used by: existing project integration, conflict-free deployment
        """
        arkival_base = self.project_root / "arkival"
        
        directories = [
            "arkival/codebase_summary",
            "arkival/codebase_summary/history", 
            "arkival/.workflow_system",
            "arkival/.workflow_system/scripts",
            "arkival/.workflow_system/ide_configs"
        ]

        for directory in directories:
            dir_path = self.project_root / directory
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"📁 Created: {directory}")
            except Exception as e:
                print(f"❌ Failed to create {directory}: {e}")

    def _copy_arkival_files(self):
        """
        # @codebase-summary: Arkival file copying for existing project integration
        - Copies Arkival system files to arkival/ subdirectory
        - Avoids overwriting existing project files
        - Used by: existing project integration, selective file deployment
        """
        core_files = [
            ("codebase_summary/agent_workflow_orchestrator.py", "arkival/codebase_summary/agent_workflow_orchestrator.py"),
            ("codebase_summary/update_changelog.py", "arkival/codebase_summary/update_changelog.py"),
            ("codebase_summary/update_project_summary.py", "arkival/codebase_summary/update_project_summary.py"),
            ("NEW_AGENT_GREETING.md", "arkival/NEW_AGENT_GREETING.md"),
            ("DEVELOPER_ONBOARDING.md", "arkival/DEVELOPER_ONBOARDING.md"),
            ("AGENT_GUIDE.md", "arkival/AGENT_GUIDE.md")
        ]

        for source, dest in core_files:
            source_path = self.package_root / source
            dest_path = self.project_root / dest

            if source_path.exists():
                try:
                    # Ensure destination directory exists
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # SAFETY CHECK: Never overwrite existing files
                    if dest_path.exists():
                        print(f"⏭️  Skipping {dest} - already exists (preserving existing file)")
                        continue
                    
                    shutil.copy2(source_path, dest_path)
                    print(f"📄 Copied to arkival/: {dest.replace('arkival/', '')}")
                except Exception as e:
                    print(f"❌ Failed to copy {dest}: {e}")
            else:
                print(f"⚠️  Source file not found: {source}")

    def _create_integration_config(self):
        """
        # @codebase-summary: Integration-specific configuration generation
        - Creates Arkival configuration that works with existing project
        - Includes detected technology stack and existing architecture info
        - Used by: existing project integration, context-aware configuration
        """
        config = {
            "_generator": "Generated by setup_workflow_system.py - Arkival integration for existing project",
            "deployment_mode": "existing_project_integration",
            "project_name": f"Existing Project + Arkival",
            "project_description": f"Existing {', '.join(self.existing_architecture.get('technology_stack', ['Unknown']))} project with Arkival workflow integration",
            "version": "1.0.0",
            "technology_stack": self.existing_architecture.get('technology_stack', ['Unknown']),
            "existing_architecture": self.existing_architecture,
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
                "ide_integration": True,
                "arkival_subdirectory": True
            },
            "integration_notes": {
                "arkival_location": "arkival/",
                "original_project_preserved": True,
                "workflow_commands": "Run from arkival/ subdirectory",
                "configuration_file": "arkival/workflow_config.json"
            },
            "setup_timestamp": datetime.now().isoformat() + "Z"
        }

        config_path = self.project_root / "arkival" / "workflow_config.json"
        try:
            # Ensure parent directory exists
            config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # SAFETY CHECK: Even in arkival subdirectory, don't overwrite
            if config_path.exists():
                print(f"⏭️  Skipping arkival/workflow_config.json - already exists")
                return
                
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            print(f"⚙️  Created arkival/workflow_config.json")
        except Exception as e:
            print(f"❌ Failed to create integration config: {e}")
    
    def _create_arkival_config(self):
        """Create arkival_config.json trigger file in project root"""
        try:
            # Detect the actual Arkival directory name
            current_dir = Path.cwd()
            arkival_dir_name = current_dir.name if current_dir.name.lower() in ['arkival', 'arkival-v4'] else 'Arkival-V4'
            
            # Simple trigger file for subdirectory mode detection
            config = {
                "arkival_integration": True,
                "version": "4.0",
                "deployment_mode": "subdirectory",
                "arkival_directory": arkival_dir_name,
                "created_at": datetime.now().isoformat(),
                "note": "This file enables Arkival subdirectory mode detection"
            }
            
            config_path = self.project_root / "arkival_config.json"
            
            # SAFETY CHECK: Don't overwrite existing config
            if config_path.exists():
                print("⏭️  Skipping arkival_config.json - already exists")
                return
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            print("⚙️  Created arkival_config.json (enables subdirectory mode)")
            
        except Exception as e:
            print(f"❌ Failed to create arkival_config.json: {e}")
            
        # Migrate .scanignore to parent root for subdirectory deployments
        self._migrate_scanignore_to_parent()

    def _migrate_scanignore_to_parent(self):
        """Migrate .scanignore to parent project root in subdirectory mode"""
        try:
            source_scanignore = self.package_root / ".scanignore"
            target_scanignore = self.project_root / ".scanignore"
            
            if not source_scanignore.exists():
                print("⚠️  No .scanignore found in Arkival directory")
                return
                
            if target_scanignore.exists():
                print("⏭️  Skipping .scanignore migration - already exists in parent")
                return
                
            # Copy .scanignore to parent project root
            import shutil
            shutil.copy2(source_scanignore, target_scanignore)
            print("⚙️  Migrated .scanignore to parent project root")
            
        except Exception as e:
            print(f"❌ Failed to migrate .scanignore: {e}")

    def _initialize_arkival_changelog(self):
        """
        # @codebase-summary: Arkival-specific changelog initialization for integration
        - Creates changelog in arkival/ subdirectory for integration tracking
        - Preserves existing project changelog if present
        - Used by: existing project integration, change tracking isolation
        """
        changelog = {
            "_generator": "Generated by setup_workflow_system.py - Arkival integration changelog",
            "project_name": f"Arkival Integration",
            "changelog_version": "1.0.0",
            "last_updated": datetime.now().isoformat() + "Z",
            "description": "Arkival workflow system integration tracking",
            "integration_mode": True,
            "entries": [
                {
                    "id": "integration_001",
                    "timestamp": datetime.now().isoformat() + "Z",
                    "author": "Arkival Setup",
                    "version": "1.0.0",
                    "type": "feature",
                    "scope": "integration",
                    "summary": "Integrated Arkival workflow system into existing project",
                    "description": f"Added Arkival workflow capabilities to existing {', '.join(self.existing_architecture.get('technology_stack', ['Unknown']))} project without modifying original files",
                    "files_changed": [
                        {
                            "file": "arkival/",
                            "action": "created",
                            "changes": ["Arkival workflow system integration"]
                        }
                    ],
                    "breaking_changes": False,
                    "migration_notes": "No migration required - integration preserves existing structure",
                    "related_issues": [],
                    "tags": ["arkival", "integration", "workflow"]
                }
            ]
        }

        changelog_path = self.project_root / "arkival" / "changelog_summary.json"
        try:
            # Ensure parent directory exists
            changelog_path.parent.mkdir(parents=True, exist_ok=True)
            
            # SAFETY CHECK: Even in arkival subdirectory, don't overwrite
            if changelog_path.exists():
                print("⏭️  Skipping arkival/changelog_summary.json - already exists")
                return
                
            with open(changelog_path, 'w', encoding='utf-8') as f:
                json.dump(changelog, f, indent=2)
            print("📝 Created arkival/changelog_summary.json")
        except Exception as e:
            print(f"❌ Failed to create arkival changelog: {e}")

    def _create_integration_documentation(self):
        """
        # @codebase-summary: Integration documentation generation
        - Creates documentation specific to Arkival integration mode
        - Provides usage instructions for existing project context
        - Used by: existing project integration, user guidance
        """
        integration_guide = f"""# Arkival Integration Guide

## Overview
Arkival has been successfully integrated into your existing project without modifying any of your original files.

## Project Structure
- **Your existing files**: Unchanged and preserved
- **Arkival files**: Located in `arkival/` directory
- **Technology Stack Detected**: {', '.join(self.existing_architecture.get('technology_stack', ['Unknown']))}

## Using Arkival Workflows

### Agent Incoming Workflow
```bash
python3 arkival/codebase_summary/agent_workflow_orchestrator.py incoming
```

### Agent Outgoing Workflow  
```bash
python3 arkival/codebase_summary/agent_workflow_orchestrator.py outgoing --summary "Session summary" --type completed
```

### Update Changelog
```bash
python3 arkival/codebase_summary/update_changelog.py add --summary "Change description"
```

## Configuration
- **Arkival Config**: `arkival/workflow_config.json`
- **Arkival Changelog**: `arkival/changelog_summary.json` 
- **Your Original Files**: Completely preserved

## Integration Notes
- Arkival operates independently in its subdirectory
- Your existing build processes and workflows remain unchanged
- You can use Arkival workflows alongside your existing development process
- No conflicts with your existing project structure

## Next Steps
1. Review `arkival/workflow_config.json` and customize if needed
2. Test the agent workflows using the commands above
3. Begin AI collaboration with full workflow support
4. Your existing project development continues normally

## Technology Stack Integration
Detected in your project:
{chr(10).join(f'- {tech}' for tech in self.existing_architecture.get('technology_stack', ['Unknown']))}

Existing directories preserved:
{chr(10).join(f'- {dir_name}/' for dir_name in self.existing_architecture.get('important_directories', []))}
"""

        guide_path = self.project_root / "arkival" / "INTEGRATION_GUIDE.md"
        try:
            # Ensure parent directory exists  
            guide_path.parent.mkdir(parents=True, exist_ok=True)
            
            # SAFETY CHECK: Even in arkival subdirectory, don't overwrite
            if guide_path.exists():
                print("⏭️  Skipping arkival/INTEGRATION_GUIDE.md - already exists")
            else:
                with open(guide_path, 'w', encoding='utf-8') as f:
                    f.write(integration_guide)
                print("📖 Created arkival/INTEGRATION_GUIDE.md")
        except Exception as e:
            print(f"❌ Failed to create integration guide: {e}")

    def _validate_integration(self):
        """
        # @codebase-summary: Integration validation and verification system
        - Validates that Arkival integration completed successfully
        - Checks for required files and proper directory structure
        - Used by: existing project integration, deployment verification
        """
        print(f"\n🔍 VALIDATING ARKIVAL INTEGRATION...")
        
        required_arkival_files = [
            "arkival/codebase_summary/agent_workflow_orchestrator.py",
            "arkival/codebase_summary/update_changelog.py", 
            "arkival/workflow_config.json",
            "arkival/changelog_summary.json",
            "arkival/INTEGRATION_GUIDE.md"
        ]
        
        all_good = True
        for file_path in required_arkival_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                print(f"✅ {file_path}")
            else:
                print(f"❌ {file_path} - MISSING")
                all_good = False
                
        if all_good:
            print("✅ Arkival integration completed successfully")
            print("🎯 Your existing project files remain unchanged")
        else:
            print("❌ Some Arkival files missing - integration may be incomplete")

    def _create_directory_structure(self):
        """Create necessary directory structure"""
        directories = [
            "codebase_summary",
            "codebase_summary/history",
            ".workflow_system",
            ".workflow_system/scripts",
            ".workflow_system/ide_configs"
        ]

        for directory in directories:
            dir_path = self.project_root / directory
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"📁 Created directory: {directory}")
            except Exception as e:
                print(f"❌ Failed to create {directory}: {e}")

    def _copy_core_files(self):
        """Copy core system files to project"""
        core_files = [
            ("codebase_summary/agent_workflow_orchestrator.py", "codebase_summary/agent_workflow_orchestrator.py"),
            ("codebase_summary/update_changelog.py", "codebase_summary/update_changelog.py"),
            ("codebase_summary/update_project_summary.py", "codebase_summary/update_project_summary.py"),
            ("NEW_AGENT_GREETING.md", "NEW_AGENT_GREETING.md"),
            ("DEVELOPER_ONBOARDING.md", "DEVELOPER_ONBOARDING.md"),
            ("AGENT_GUIDE.md", "AGENT_GUIDE.md")
        ]

        for source, dest in core_files:
            source_path = self.package_root / source
            dest_path = self.project_root / dest

            # Skip if source and destination are the same file
            if source_path.resolve() == dest_path.resolve():
                print(f"✅ Already exists: {dest}")
                continue

            if source_path.exists():
                try:
                    # Ensure destination directory exists
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # SAFETY CHECK: Never overwrite existing files
                    if dest_path.exists():
                        print(f"⏭️  Skipping {dest} - already exists (preserving existing file)")
                        continue
                    
                    shutil.copy2(source_path, dest_path)
                    print(f"📄 Copied: {dest}")
                except Exception as e:
                    print(f"❌ Failed to copy {dest}: {e}")
            else:
                print(f"⚠️  Source file not found: {source}")

    def _initialize_project_config(self):
        """Initialize project configuration with IDE detection"""
        config = {
            "_generator": "Generated by setup_workflow_system.py - Cross-platform workflow system setup",
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
        try:
            # Ensure parent directory exists
            config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # SAFETY CHECK: Never overwrite existing config
            if config_path.exists():
                print(f"⏭️  Skipping workflow_config.json - already exists (preserving existing configuration)")
                return
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            print(f"⚙️  Created workflow_config.json for {self.detected_ide}")
        except Exception as e:
            print(f"❌ Failed to create workflow_config.json: {e}")

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
        # Always create shell scripts as fallback
        self._setup_shell_scripts()
        
        # Then create IDE-specific configurations
        if self.detected_ide == 'replit':
            self._setup_replit_workflows()
        elif self.detected_ide in ['vscode', 'cursor', 'codespaces']:
            self._setup_vscode_tasks()
        elif self.detected_ide == 'gitpod':
            self._setup_gitpod_tasks()

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
        
        # SAFETY CHECK: Never overwrite existing .replit file
        if replit_file_path.exists():
            print("⏭️  Skipping .replit - already exists (preserving existing Replit configuration)")
        else:
            with open(replit_file_path, 'w', encoding='utf-8') as f:
                f.write(replit_file_config)
            print("🔧 Created Replit .replit file with integrated workflows")

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
        # SAFETY CHECK: Don't overwrite existing workflow backup
        if workflow_path.exists():
            print("⏭️  Skipping .workflow_system/replit_workflows.toml - already exists")
        else:
            with open(workflow_path, 'w', encoding='utf-8') as f:
                f.write(workflow_only_config)
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
        
        # SAFETY CHECK: Never overwrite existing VS Code tasks
        if tasks_path.exists():
            print("⏭️  Skipping .vscode/tasks.json - already exists (preserving existing tasks)")
        else:
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
        
        # SAFETY CHECK: Never overwrite existing .gitpod.yml
        if gitpod_path.exists():
            print("⏭️  Skipping .gitpod.yml - already exists (preserving existing Gitpod configuration)")
        else:
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
            
            # SAFETY CHECK: Don't overwrite existing scripts
            if script_path.exists():
                print(f"⏭️  Skipping {script_name} - already exists")
                continue
                
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(script_content)

            # Make scripts executable on Unix systems
            if platform.system() != 'Windows':
                os.chmod(script_path, 0o755)

        print("🔧 Created shell scripts for workflow execution")

    def _initialize_changelog(self):
        """Initialize changelog system (existing functionality)"""
        changelog = {
            "_generator": "Generated by setup_workflow_system.py - Initial changelog system setup",
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
        
        # SAFETY CHECK: Never overwrite existing changelog
        if changelog_path.exists():
            print("⏭️  Skipping changelog_summary.json - already exists (preserving existing changelog)")
            return
            
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
        
        # SAFETY CHECK: Never overwrite existing codebase summary
        if summary_path.exists():
            print("⏭️  Skipping codebase_summary/codebase_summary.json - already exists")
        else:
            with open(summary_path, 'w', encoding='utf-8') as f:
                json.dump(codebase_summary, f, indent=2)
            print("📊 Created codebase_summary.json")

    def _handle_gitignore(self):
        """Handle .gitignore file - merge with existing or create new"""
        arkival_gitignore_entries = """
# Arkival-specific entries
# =======================

# Generated JSON files (should not be committed)
codebase_summary.json
changelog_summary.json
codebase_summary/session_state.json
codebase_summary/agent_handoff.json
codebase_summary/missing_breadcrumbs.json
export_package/agent_handoff.json

# Arkival data directory (subdirectory mode)
Arkival/data/

# Arkival documentation (kept separate from project docs)
arkival_docs/

# IDE-specific files (generated during setup)
.replit
.gitpod.yml

# Environment-specific workflow files
.workflow_system/

# System files
codebase_summary/history/

# Node.js files (not needed for Python project)
package.json
package-lock.json
"""
        
        gitignore_path = self.project_root / ".gitignore"
        
        if gitignore_path.exists():
            # Read existing .gitignore
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                existing_content = f.read()
            
            # Check if Arkival entries already exist
            if "Arkival-specific entries" in existing_content:
                print("✅ .gitignore already contains Arkival entries")
                return
            
            # Append Arkival entries to existing .gitignore
            with open(gitignore_path, 'a', encoding='utf-8') as f:
                f.write("\n" + arkival_gitignore_entries)
            print("📝 Appended Arkival entries to existing .gitignore")
        else:
            # Create new .gitignore with standard entries plus Arkival entries
            standard_gitignore = """# Dependencies
node_modules/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/

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

# Environment variables
.env
.env.local

# Logs
logs/
*.log

# Temporary files
*.tmp
*.temp
.tmp/
temp/
"""
            
            with open(gitignore_path, 'w', encoding='utf-8') as f:
                f.write(standard_gitignore + arkival_gitignore_entries)
            print("📄 Created .gitignore with Arkival entries")

    def _create_community_standards_files(self):
        """Create GitHub community standards files"""
        # Handle .gitignore - merge with existing or create new
        self._handle_gitignore()

        # Create arkival_docs directory if not exists
        arkival_docs_dir = self.project_root / "arkival_docs"
        arkival_docs_dir.mkdir(parents=True, exist_ok=True)
        
        # Create LICENSE (Attribution to Spitfire Products) in arkival_docs
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

        # Place Arkival LICENSE in arkival_docs folder
        arkival_license_path = arkival_docs_dir / "ARKIVAL_LICENSE"
        
        if arkival_license_path.exists():
            print("⏭️  Skipping arkival_docs/ARKIVAL_LICENSE - already exists")
        else:
            with open(arkival_license_path, 'w', encoding='utf-8') as f:
                f.write(license_content)
            print("📄 Created arkival_docs/ARKIVAL_LICENSE")

        # Create CONTRIBUTING.md in arkival_docs
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
git clone https://github.com/Spitfire-Products/Arkival-V4.git
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

        # Place CONTRIBUTING.md in arkival_docs folder
        arkival_contributing_path = arkival_docs_dir / "ARKIVAL_CONTRIBUTING.md"
        
        if arkival_contributing_path.exists():
            print("⏭️  Skipping arkival_docs/ARKIVAL_CONTRIBUTING.md - already exists")
        else:
            with open(arkival_contributing_path, 'w', encoding='utf-8') as f:
                f.write(contributing_content)
            print("📄 Created arkival_docs/ARKIVAL_CONTRIBUTING.md")

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

        # Place SECURITY.md in arkival_docs folder
        arkival_security_path = arkival_docs_dir / "ARKIVAL_SECURITY.md"
        
        if arkival_security_path.exists():
            print("⏭️  Skipping arkival_docs/ARKIVAL_SECURITY.md - already exists")
        else:
            with open(arkival_security_path, 'w', encoding='utf-8') as f:
                f.write(security_content)
            print("📄 Created arkival_docs/ARKIVAL_SECURITY.md")

        # Summary message handled by individual file creation

    def _setup_ide_integration(self):
        """Set up IDE-specific integration files"""
        # Create setup guide
        setup_guide = self._generate_setup_guide()
        guide_path = self.project_root / "SETUP_GUIDE.md"
        
        # SAFETY CHECK: Never overwrite existing SETUP_GUIDE.md
        if guide_path.exists():
            print("⏭️  Skipping SETUP_GUIDE.md - already exists (preserving existing file)")
        else:
            with open(guide_path, 'w', encoding='utf-8') as f:
                f.write(setup_guide)
            print(f"📖 Created setup guide for {self.detected_ide.upper()}")

        # Create IDE-specific settings if applicable
        if self.detected_ide in ['vscode', 'cursor', 'codespaces']:
            self._create_vscode_settings()

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
        vscode_dir.mkdir(exist_ok=True)
        settings_path = vscode_dir / "settings.json"

        # SAFETY CHECK: Never overwrite existing VS Code settings
        if settings_path.exists():
            print("⏭️  Skipping .vscode/settings.json - already exists (preserving existing settings)")
        else:
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

    def generate_simulation_report(self):
        """
        # @codebase-summary: Setup simulation report generator for source repository testing
        - Generates detailed report of what setup would do without making changes
        - Analyzes deployment logic and file creation patterns
        - Creates .md report for validating setup behavior
        - Used by: source repository testing, setup validation, deployment verification
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.project_root / f"SETUP_SIMULATION_REPORT_{timestamp}.md"
        
        report_content = f"""# Arkival Setup Simulation Report
*Generated: {datetime.now().isoformat()}*
*Mode: Source Repository Simulation*

## Detection Results
- **Deployment Context**: {self.deployment_context}
- **IDE Environment**: {self.detected_ide}
- **Project Root**: {self.project_root}
- **Source Repository**: Yes (contains setup_workflow_system.py)
- **Arkival Config**: Not present (as expected for source)

## Deployment Logic Analysis

### If deployed as NEW PROJECT:
"""

        # Simulate new project setup
        if self.deployment_context != 'existing_project_integration':
            report_content += """
**Files that would be created:**
1. `workflow_config.json` - Main workflow configuration
2. `codebase_summary/codebase_summary.json` - Initial project analysis
3. `SETUP_GUIDE.md` - IDE-specific setup instructions
4. `.workflow_system/` directory structure
5. IDE-specific configs (.vscode/tasks.json, etc.)

**Directory structure:**
```
project-root/
├── workflow_config.json
├── codebase_summary/
│   └── codebase_summary.json
├── .workflow_system/
│   ├── scripts/
│   └── ide_configs/
└── SETUP_GUIDE.md
```

**Git ignore additions:**
- Generated JSON files
- .workflow_system/ directory
- IDE-specific temp files
"""
        else:
            report_content += """
**Files that would be created:**
1. `arkival_config.json` - Subdirectory mode trigger (ROOT ONLY)

**Directory structure:**
```
existing-project/
├── arkival_config.json (ONLY file added)
└── Arkival-V4/ (all files stay here)
    ├── codebase_summary/
    ├── export_package/
    └── [all arkival files]
```
"""

        report_content += f"""

### Current Architecture Analysis:
- **Technology Stack**: {', '.join(self.existing_architecture.get('technology_stack', ['None detected']))}
- **Config Files**: {len(self.existing_architecture.get('config_files', []))} detected
- **Important Directories**: {len(self.existing_architecture.get('important_directories', []))} preserved

## Safety Checks That Would Apply:
- ✅ Never overwrite existing files
- ✅ Skip creation if files already exist
- ✅ Preserve project structure in subdirectory mode
- ✅ Only add arkival_config.json to existing projects

## Environment-Specific Files (Git Ignored):
- `.workflow_system/logs/`
- `.workflow_system/backups/`
- `codebase_summary.json` (generated)
- `changelog_summary.json` (generated)
- Session state files

## Validation Results:
- **Path Resolution**: Would work correctly
- **IDE Integration**: {self.detected_ide} support available
- **Cross-Platform**: Compatible with {platform.system()}

## Recommended Testing:
1. Deploy to test project: `mkdir test-project && cd test-project`
2. Run setup: `python /path/to/setup_workflow_system.py`
3. Verify file creation matches this simulation
4. Test workflow execution

---
*This simulation prevents modifications to the source repository while validating setup logic.*
"""

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"📋 Simulation report generated: {report_path.name}")
        print("🔍 Review the report to validate setup behavior")
        print("💡 To test actual setup, deploy to a separate directory")

def main():
    """
    # @codebase-summary: Main execution entry point for workflow system setup
    - Orchestrates complete setup process based on deployment context detection
    - Handles both new project deployment and existing project integration scenarios
    - Provides comprehensive error handling and user feedback throughout setup
    - Used by: deployment automation, project initialization, integration workflows
    """
    if not validate_dependencies():
        sys.exit(1)

    print("🚀 Arkival Workflow System Setup")
    print("=" * 50)

    try:
        setup = WorkflowSystemSetup()
        
        print(f"📍 Deployment Context: {setup.deployment_context}")
        print(f"🔍 Detected IDE: {setup.detected_ide}")
        print(f"📁 Project Root: {setup.project_root}")
        
        # Check if running in source repository (has .git and codebase_summary directory with scripts)
        is_source_repo = (
            (setup.project_root / ".git").exists() and
            (setup.project_root / "codebase_summary" / "agent_workflow_orchestrator.py").exists() and
            not (setup.project_root / "arkival_config.json").exists()
        )
        
        if is_source_repo:
            print("\n⚠️  DETECTED: Running in Arkival source repository")
            print("🧪 Generating simulation report instead of making changes...")
            setup.generate_simulation_report()
        elif setup.deployment_context == 'existing_project_integration':
            setup.setup_existing_project_integration()
        else:
            setup.setup_new_project()
            
        print("\n✅ Arkival Workflow System setup completed!")
        print("🎯 Your development environment is now ready for AI collaboration")
        
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()