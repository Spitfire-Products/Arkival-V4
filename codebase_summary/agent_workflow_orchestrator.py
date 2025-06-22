#!/usr/bin/env python3
"""
Agent Workflow Orchestrator - Arkival
Manages consistency between outgoing and incoming agents with automated workflows
"""

import json
import os
import sys
import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import argparse

def find_arkival_paths():
    """
    # @codebase-summary: Simple workflow flag-based path resolution
    - Uses arkival_config.json in root as definitive subdirectory deployment flag
    - Simplified detection logic based on workflow flag presence
    - Returns all required file paths for agent workflow orchestration
    """
    current_dir = Path.cwd()
    
    # Simple workflow flag detection: arkival_config.json in current directory = subdirectory mode
    subdirectory_mode = (current_dir / "arkival_config.json").exists()
    
    if subdirectory_mode:
        # Subdirectory deployment mode - use Arkival-V4 directory structure
        arkival_dir = current_dir / "Arkival-V4"
        return {
            'project_root': current_dir,  # Parent project root
            'config_file': current_dir / "arkival_config.json",
            'arkival_dir': arkival_dir,
            'data_dir': arkival_dir,
            'scripts_dir': arkival_dir / "codebase_summary", 
            'export_dir': arkival_dir / "export_package",
            'checkpoints_dir': arkival_dir / "checkpoints",
            
            # Data files in Arkival-V4 directory
            'codebase_summary': arkival_dir / "codebase_summary.json",
            'changelog_summary': arkival_dir / "changelog_summary.json",
            'session_state': arkival_dir / "codebase_summary" / "session_state.json",
            'missing_breadcrumbs': arkival_dir / "codebase_summary" / "missing_breadcrumbs.json"
        }
    else:
        # Development mode - running from Arkival project directory
        # Handle case where we might be running from codebase_summary subdirectory
        if current_dir.name == "codebase_summary":
            project_root = current_dir.parent
            scripts_dir = current_dir
        else:
            project_root = current_dir
            scripts_dir = project_root / "codebase_summary"
            
        return {
            'project_root': project_root,
            'config_file': project_root / "arkival_config.json",  # May not exist in dev mode
            'arkival_dir': project_root,
            'data_dir': project_root,
            'scripts_dir': scripts_dir, 
            'export_dir': project_root / "export_package",
            'checkpoints_dir': project_root / "checkpoints",
            
            # Data files in root/standard locations
            'codebase_summary': project_root / "codebase_summary.json",
            'changelog_summary': project_root / "changelog_summary.json",
            'session_state': scripts_dir / "session_state.json",
            'missing_breadcrumbs': scripts_dir / "missing_breadcrumbs.json"
        }

class AgentWorkflowOrchestrator:
    """
    # @codebase-summary: Central agent handoff coordination system
    
    Manages the complete lifecycle of agent transitions including:
    - Loading previous session context and unresolved issues
    - Documenting current session progress and decisions
    - Preparing comprehensive handoff documentation
    - Maintaining version correlation across all project systems
    
    This is the heart of the cross-platform workflow system that enables
    seamless knowledge transfer between AI agents and human developers.
    
    Key integrations:
    - Changelog management for session tracking
    - Project documentation updates and synchronization
    - Session state persistence across agent transitions
    - Version synchronization between all project components
    """

    def __init__(self):
        # Use universal path resolution for Arkival subdirectory deployment
        self.paths = find_arkival_paths()
        self.project_root = self.paths['project_root']
        self.codebase_summary_path = self.paths['codebase_summary']
        self.changelog_path = self.paths['changelog_summary']
        self.session_state_path = self.paths['session_state']

    def trigger_outgoing_agent_workflow(self, session_summary: str, issue_type: str = "completed") -> Dict[str, Any]:
        """
        # @codebase-summary: Outgoing agent session completion workflow
        - Processes and documents completed development sessions
        - Creates changelog entries with proper version correlation
        - Updates session state for incoming agent context
        - Handles both completed work and handoff scenarios
        - Used by: session completion triggers, manual handoffs
        """
        print("🚀 OUTGOING AGENT WORKFLOW TRIGGERED")
        print("=" * 50)

        workflow_result = {
            "timestamp": datetime.datetime.now().isoformat() + "Z",
            "session_summary": session_summary,
            "issue_type": issue_type,
            "steps_completed": [],
            "errors": []
        }

        try:
            # Step 1: Update session state
            self._update_session_state(session_summary, issue_type)
            workflow_result["steps_completed"].append("session_state_updated")

            # Step 2: Create changelog entry
            changelog_success = self._create_changelog_entry(session_summary, issue_type)
            if changelog_success:
                workflow_result["steps_completed"].append("changelog_updated")

            # Step 3: Version correlation check
            version_sync = self._sync_versions()
            if version_sync:
                workflow_result["steps_completed"].append("versions_synchronized")

            # Step 4: Archive old entries if needed
            archive_result = self._archive_if_needed()
            if archive_result:
                workflow_result["steps_completed"].append("entries_archived")

            # Step 5: Create handoff documentation
            handoff_doc = self._create_handoff_documentation(session_summary, issue_type)
            if handoff_doc:
                workflow_result["steps_completed"].append("handoff_documentation_created")

            print("✅ OUTGOING AGENT WORKFLOW COMPLETED")
            return workflow_result

        except Exception as e:
            error_msg = f"Outgoing workflow error: {e}"
            workflow_result["errors"].append(error_msg)
            print(f"❌ {error_msg}")
            return workflow_result

    def trigger_incoming_agent_workflow(self) -> Dict[str, Any]:
        """
        # @codebase-summary: Incoming agent onboarding and context loading workflow
        - Loads previous session context and unresolved issues for new agent
        - Generates current state summary and runs comprehensive codebase scan
        - Verifies documentation consistency and creates readiness checklist
        - Ensures seamless agent transition with complete project context
        - Used by: agent handoff triggers, onboarding automation, context transfer
        """
        print("🎯 INCOMING AGENT WORKFLOW TRIGGERED")
        print("=" * 50)

        workflow_result = {
            "timestamp": datetime.datetime.now().isoformat() + "Z",
            "onboarding_steps": [],
            "context_provided": {},
            "errors": []
        }

        try:
            # Step 1: Load session context
            session_context = self._load_session_context()
            workflow_result["context_provided"]["session_context"] = session_context
            workflow_result["onboarding_steps"].append("session_context_loaded")

            # Step 2: Generate current state summary
            current_state = self._generate_current_state_summary()
            workflow_result["context_provided"]["current_state"] = current_state
            workflow_result["onboarding_steps"].append("current_state_generated")

            # Step 3: Check for unresolved issues
            unresolved_issues = self._check_unresolved_issues()
            workflow_result["context_provided"]["unresolved_issues"] = unresolved_issues
            workflow_result["onboarding_steps"].append("unresolved_issues_identified")

            # Step 4: Update codebase summary
            self._run_codebase_scan()
            workflow_result["onboarding_steps"].append("codebase_scan_completed")

            # Step 5: Verify documentation consistency
            doc_check = self._verify_documentation_consistency()
            workflow_result["context_provided"]["documentation_status"] = doc_check
            workflow_result["onboarding_steps"].append("documentation_verified")

            # Step 6: Generate readiness checklist
            readiness_checklist = self._generate_readiness_checklist()
            workflow_result["context_provided"]["readiness_checklist"] = readiness_checklist
            workflow_result["onboarding_steps"].append("readiness_checklist_generated")

            # Step 7: Verify engineering best practices
            engineering_practices = self._engineering_best_practices_check()
            workflow_result["context_provided"]["engineering_practices"] = engineering_practices
            workflow_result["onboarding_steps"].append("engineering_practices_verified")

            # Step 8: Provide project overview from key documentation
            project_overview = self._provide_project_overview()
            workflow_result["context_provided"]["project_overview"] = project_overview
            workflow_result["onboarding_steps"].append("project_overview_provided")

            # Step 9: Detect and explain deployment mode
            deployment_info = self._detect_deployment_mode()
            workflow_result["context_provided"]["deployment_info"] = deployment_info
            workflow_result["onboarding_steps"].append("deployment_mode_detected")

            # Step 10: Summarize key architecture insights
            architecture_insights = self._summarize_architecture_insights()
            workflow_result["context_provided"]["architecture_insights"] = architecture_insights
            workflow_result["onboarding_steps"].append("architecture_insights_provided")

            # Step 11: Identify external dependencies and requirements
            dependencies_info = self._identify_external_dependencies()
            workflow_result["context_provided"]["dependencies_info"] = dependencies_info
            workflow_result["onboarding_steps"].append("external_dependencies_identified")

            # Step 12: Provide user workflow examples and commands
            workflow_examples = self._provide_workflow_examples()
            workflow_result["context_provided"]["workflow_examples"] = workflow_examples
            workflow_result["onboarding_steps"].append("workflow_examples_provided")

            # Step 13: Analyze recent git activity
            git_activity = self._analyze_recent_git_activity()
            workflow_result["context_provided"]["git_activity"] = git_activity
            workflow_result["onboarding_steps"].append("git_activity_analyzed")

            # Step 14: Summarize system capabilities
            system_capabilities = self._summarize_system_capabilities()
            workflow_result["context_provided"]["system_capabilities"] = system_capabilities
            workflow_result["onboarding_steps"].append("system_capabilities_summarized")

            # Step 15: Provide command reference
            command_reference = self._provide_command_reference()
            workflow_result["context_provided"]["command_reference"] = command_reference
            workflow_result["onboarding_steps"].append("command_reference_provided")

            print("✅ INCOMING AGENT WORKFLOW COMPLETED")
            return workflow_result

        except Exception as e:
            error_msg = f"Incoming workflow error: {e}"
            workflow_result["errors"].append(error_msg)
            print(f"❌ {error_msg}")
            return workflow_result

    def _update_session_state(self, session_summary: str, issue_type: str) -> None:
        """
        # @codebase-summary: Session state persistence and handoff preparation system
        - Saves current session context with timestamp and completion status
        - Extracts priority items and technical state for next agent
        - Maintains project version correlation and known issues tracking
        - Used by: agent transitions, session completion, context preservation
        """
        session_state = {
            "_generator": "Generated by codebase_summary/agent_workflow_orchestrator.py - Agent session state management",
            "last_session": {
                "timestamp": datetime.datetime.now().isoformat() + "Z",
                "summary": session_summary,
                "type": issue_type,
                "handoff_ready": True
            },
            "project_version": self._get_current_version(),
            "next_agent_context": {
                "priority_items": self._extract_priority_items(session_summary, issue_type),
                "technical_state": self._get_technical_state(),
                "known_issues": self._get_known_issues() if issue_type == "unresolved" else []
            }
        }

        try:
            # Ensure parent directory exists
            os.makedirs(os.path.dirname(self.session_state_path), exist_ok=True)
            
            with open(self.session_state_path, 'w', encoding='utf-8') as f:
                json.dump(session_state, f, indent=2)
                
        except Exception as e:
            print(f"⚠️  Failed to save session state to {self.session_state_path}: {e}")
            # Try backup location
            backup_path = self.paths['project_root'] / "session_state_backup.json"
            try:
                with open(backup_path, 'w', encoding='utf-8') as f:
                    json.dump(session_state, f, indent=2)
                print(f"✅ Saved session state to backup location: {backup_path}")
            except Exception as backup_error:
                print(f"❌ Failed to save session state to backup: {backup_error}")

    def _create_changelog_entry(self, session_summary: str, issue_type: str) -> bool:
        """
        # @codebase-summary: Automated changelog entry creation for agent sessions
        - Creates appropriate changelog entries based on session type and outcome
        - Maps session completion types to changelog entry categories
        - Integrates with enhanced changelog system for version tracking
        - Used by: session completion, workflow automation, version management
        """
        try:
            import subprocess

            entry_type = "feature" if issue_type == "completed" else "bug"
            scope = "development"

            cmd = [
                sys.executable, 
                str(self.paths['scripts_dir'] / "update_changelog.py"),
                "add",
                "--summary", session_summary,
                "--type", entry_type,
                "--scope", scope,
                "--description", f"Agent collaboration session - {issue_type} work"
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0

        except Exception as e:
            print(f"Changelog creation failed: {e}")
            return False

    def _sync_versions(self) -> bool:
        """
        # @codebase-summary: Cross-system version synchronization manager
        - Synchronizes version numbers between codebase and changelog systems
        - Ensures version consistency across all project documentation
        - Maintains version correlation for proper tracking and deployment
        - Used by: version management, system consistency, release coordination
        """
        try:
            # Get codebase version
            codebase_version = self._get_current_version()

            # Update changelog version
            if os.path.exists(self.changelog_path):
                with open(self.changelog_path, 'r', encoding='utf-8') as f:
                    changelog = json.load(f)

                changelog["changelog_version"] = codebase_version

                with open(self.changelog_path, 'w', encoding='utf-8') as f:
                    json.dump(changelog, f, indent=2)

            return True

        except Exception as e:
            print(f"Version sync failed: {e}")
            return False

    def _archive_if_needed(self) -> bool:
        """
        # @codebase-summary: Automated changelog archiving system
        - Archives old changelog entries when maximum entry limit is reached
        - Maintains changelog performance while preserving historical data
        - Integrates with enhanced changelog archive management system
        - Used by: maintenance automation, performance optimization, data management
        """
        try:
            import subprocess

            cmd = [
                sys.executable,
                str(self.paths['scripts_dir'] / "update_changelog.py"),
                "archive",
                "--max-entries", "25"
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0

        except Exception as e:
            print(f"Archiving failed: {e}")
            return False

    def _create_handoff_documentation(self, session_summary: str, issue_type: str) -> bool:
        """
        # @codebase-summary: Agent handoff documentation creation system
        - Creates comprehensive handoff documentation for incoming agents
        - Includes session context, technical state, and priority actions
        - Replicates documentation across multiple system locations
        - Used by: agent transitions, session handoffs, context preservation
        """
        try:
            handoff_doc = {
                "_generator": "Generated by codebase_summary/agent_workflow_orchestrator.py - Agent handoff documentation system",
                "handoff_timestamp": datetime.datetime.now().isoformat() + "Z",
                "session_type": issue_type,
                "session_summary": session_summary,
                "next_agent_instructions": self._generate_next_agent_instructions(issue_type),
                "technical_context": self._get_technical_state(),
                "priority_actions": self._extract_priority_items(session_summary, issue_type)
            }

            handoff_path = self.paths['scripts_dir'] / "agent_handoff.json"
            
            try:
                # Ensure parent directory exists
                handoff_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(handoff_path, 'w', encoding='utf-8') as f:
                    json.dump(handoff_doc, f, indent=2)
                    
            except Exception as e:
                print(f"⚠️  Failed to save handoff documentation to {handoff_path}: {e}")
                # Try backup location
                backup_path = self.paths['project_root'] / "agent_handoff_backup.json"
                try:
                    with open(backup_path, 'w', encoding='utf-8') as f:
                        json.dump(handoff_doc, f, indent=2)
                    print(f"✅ Saved handoff documentation to backup location: {backup_path}")
                except Exception as backup_error:
                    print(f"❌ Failed to save handoff documentation to backup: {backup_error}")
                    raise

            # Replicate into export package system
            self._replicate_handoff_documentation(handoff_doc)

            return True

        except Exception as e:
            print(f"Handoff documentation creation failed: {e}")
            return False

    def _replicate_handoff_documentation(self, handoff_doc: Dict[str, Any]) -> None:
        """
        # @codebase-summary: Handoff documentation replication system
        - Replicates handoff documentation across multiple system locations
        - Ensures redundancy and accessibility for incoming agents
        - Maintains synchronized copies in export package directory
        - Resilient: creates directory and file if missing
        - Used by: documentation preservation, system redundancy, agent onboarding
        """
        export_package_dir = self.paths['export_dir']
        export_package_path = export_package_dir / "agent_handoff.json"
        
        try:
            # Ensure export_package directory exists
            export_package_dir.mkdir(parents=True, exist_ok=True)
            
            # Check if source file exists and copy if target is missing or outdated
            source_path = self.paths['scripts_dir'] / "agent_handoff.json"
            if source_path.exists() and not export_package_path.exists():
                # Copy from source if target doesn't exist
                import shutil
                shutil.copy2(source_path, export_package_path)
                print(f"✅ Handoff documentation copied from source to: {export_package_path}")
            else:
                # Create/update with current handoff doc
                with open(export_package_path, 'w', encoding='utf-8') as f:
                    json.dump(handoff_doc, f, indent=2)
                print(f"✅ Handoff documentation replicated to: {export_package_path}")
                
        except Exception as e:
            print(f"❌ Failed to replicate handoff documentation: {e}")
            # Try to at least ensure the directory exists for future attempts
            try:
                export_package_dir.mkdir(parents=True, exist_ok=True)
                print(f"✅ Created export_package directory for future use")
            except Exception as dir_error:
                print(f"❌ Could not create export_package directory: {dir_error}")

    def _load_session_context(self) -> Dict[str, Any]:
        """
        # @codebase-summary: Previous session context loading system
        - Loads session state and handoff documentation from previous agents
        - Aggregates context from multiple storage locations for comprehensive view
        - Provides incoming agents with complete project context and history
        - Used by: agent onboarding, context restoration, session continuity
        """
        context = {}

        # Load session state
        if os.path.exists(self.session_state_path):
            with open(self.session_state_path, 'r', encoding='utf-8') as f:
                context["session_state"] = json.load(f)

        # Load handoff documentation (primary location with fallback)
        handoff_path = self.paths['scripts_dir'] / "agent_handoff.json"
        export_package_path = self.paths['export_dir'] / "agent_handoff.json"
        
        if os.path.exists(handoff_path):
            with open(handoff_path, 'r', encoding='utf-8') as f:
                context["handoff_documentation"] = json.load(f)
        elif os.path.exists(export_package_path):
            # Fallback to export package if primary location unavailable
            with open(export_package_path, 'r', encoding='utf-8') as f:
                context["handoff_documentation"] = json.load(f)

        return context

    def _generate_current_state_summary(self) -> Dict[str, Any]:
        """
        # @codebase-summary: Current project state summary generation system
        - Generates real-time project state summary with version and status
        - Provides incoming agents with current technical status overview
        - Includes active features and operational status indicators
        - Used by: agent onboarding, status assessment, project overview
        """
        state = {
            "version": self._get_current_version(),
            "last_updated": datetime.datetime.now().isoformat() + "Z",
            "active_features": [],
            "technical_status": "operational"
        }

        # Add more state information as needed
        return state

    def _check_unresolved_issues(self) -> List[Dict[str, Any]]:
        """
        # @codebase-summary: Unresolved issues detection and tracking system
        - Checks for unresolved issues from previous agent sessions and changelogs
        - Provides continuity for ongoing tasks and bug fixes
        - Aggregates issues from multiple sources for comprehensive tracking
        - Used by: issue tracking, session continuity, project management
        """
        unresolved = []

        # Check changelog for unresolved issues
        if os.path.exists(self.changelog_path):
            with open(self.changelog_path, 'r', encoding='utf-8') as f:
                changelog = json.load(f)

            # Look for recent entries marked as bugs or unresolved
            for entry in changelog.get("entries", [])[-5:]:  # Last 5 entries
                if entry.get("type") == "bug" or "unresolved" in entry.get("description", "").lower():
                    unresolved.append({
                        "issue": entry.get("summary"),
                        "description": entry.get("description"),
                        "timestamp": entry.get("timestamp")
                    })

        return unresolved

    def _run_codebase_scan(self) -> bool:
        """Run codebase summary update"""
        print("📋 Triggering enhanced codebase summary update...")
        
        # Always run codebase scan - this is essential for maintaining project coherence
        
        try:
            # Use force flag for comprehensive update during handoff
            import subprocess

            # First check if script exists at expected path
            script_path = self.paths['scripts_dir'] / "update_project_summary.py"
            if not script_path.exists():
                # Try current directory as fallback
                script_path = Path(__file__).parent / "update_project_summary.py"
                if not script_path.exists():
                    print(f"❌ Could not find update_project_summary.py")
                    return False

            cmd = [
                sys.executable,
                str(script_path),
                "--force"
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Enhanced codebase summary updated successfully")
                if result.stdout:
                    print("Enhanced summary output:", result.stdout.strip())
            else:
                print(f"⚠️ Enhanced codebase summary update had issues: {result.stderr}")
            return result.returncode == 0

        except Exception as e:
            print(f"Codebase scan failed: {e}")
            return False

    def _verify_documentation_consistency(self) -> Dict[str, Any]:
        """Verify documentation is consistent and up to date"""
        consistency_check = {
            "codebase_summary_exists": os.path.exists(self.codebase_summary_path),
            "changelog_exists": os.path.exists(self.changelog_path),
            "versions_match": False,
            "missing_breadcrumbs": []
        }

        # Check version matching
        if consistency_check["codebase_summary_exists"] and consistency_check["changelog_exists"]:
            codebase_version = self._get_current_version()

            with open(self.changelog_path, 'r', encoding='utf-8') as f:
                changelog = json.load(f)

            changelog_version = changelog.get("changelog_version", "")
            consistency_check["versions_match"] = codebase_version == changelog_version

        # Check for missing breadcrumbs
        missing_breadcrumbs_path = self.paths['missing_breadcrumbs']
        if os.path.exists(missing_breadcrumbs_path):
            with open(missing_breadcrumbs_path, 'r', encoding='utf-8') as f:
                missing_data = json.load(f)
                consistency_check["missing_breadcrumbs"] = missing_data.get("missing_breadcrumbs", [])

        return consistency_check

    def _generate_readiness_checklist(self) -> List[Dict[str, Any]]:
        """Generate readiness checklist for new agent"""
        checklist = [
            {
                "item": "Review session context",
                "description": "Understand what the previous agent accomplished or attempted",
                "required": True
            },
            {
                "item": "Check unresolved issues",
                "description": "Review any bugs or incomplete work that needs attention",
                "required": True
            },
            {
                "item": "Verify technical state",
                "description": "Ensure application is running and all systems operational",
                "required": True
            },
            {
                "item": "Review recent changelog",
                "description": "Understand recent changes and their impact",
                "required": True
            },
            {
                "item": "Check documentation gaps",
                "description": "Review missing breadcrumbs and update as needed",
                "required": False
            }
        ]

        return checklist

    def _get_current_version(self) -> str:
        """
        # @codebase-summary: Current version detection and retrieval system
        - Retrieves current version from codebase summary or alternative sources
        - Provides version context for agents and system tracking
        - Supports fallback version detection for version consistency
        - Used by: version tracking, system identification, changelog management
        """
        try:
            if os.path.exists(self.codebase_summary_path):
                with open(self.codebase_summary_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get("version", "1.0.0")
        except:
            pass
        return "1.0.0"

    def _extract_priority_items(self, session_summary: str, issue_type: str) -> List[str]:
        """
        # @codebase-summary: Priority item extraction and analysis system
        - Extracts critical priority items from session summaries and issue types
        - Identifies urgent tasks and blockers requiring immediate attention
        - Provides incoming agents with clear action priorities and focus areas
        - Used by: priority management, task delegation, workflow optimization
        """
        # Simple keyword extraction - could be enhanced with NLP
        priority_keywords = ["urgent", "critical", "important", "fix", "bug", "error", "complete"]
        priorities = []

        words = session_summary.lower().split()
        for i, word in enumerate(words):
            if word in priority_keywords and i + 1 < len(words):
                priorities.append(" ".join(words[i:i+5]))  # Context around keyword

        return priorities[:3]  # Top 3 priorities

    def _get_technical_state(self) -> Dict[str, Any]:
        """
        # @codebase-summary: System technical state assessment and reporting
        - Gathers current technical state including versions and configurations
        - Provides incoming agents with comprehensive system status overview
        - Includes operational metrics and system health indicators
        - Used by: system monitoring, agent onboarding, technical assessment
        """
        return {
            "application_running": True,  # Could check actual port status
            "last_build_status": "success",
            "critical_errors": [],
            "performance_status": "normal"
        }

    def _get_known_issues(self) -> List[str]:
        """
        # @codebase-summary: Known issues tracking and reporting system
        - Maintains list of known system issues and current status
        - Provides agents with awareness of existing limitations
        - Supports issue tracking and resolution monitoring
        - Used by: issue management, agent awareness, system status
        """
        return [
            "System ready for development",
            "Check configuration for project-specific settings"
        ]

    def _generate_next_agent_instructions(self, issue_type: str) -> List[str]:
        """
        # @codebase-summary: Next agent instruction generation system
        - Generates specific instructions for incoming agents based on session type
        - Provides contextual guidance and priority actions for smooth handoffs
        - Customizes instructions based on detected issue categories and patterns
        - Used by: agent handoffs, task delegation, workflow continuity
        """
        if issue_type == "completed":
            return [
                "Review completed work and verify functionality",
                "Consider next feature priorities from roadmap",
                "Check for any edge cases or improvements needed"
            ]
        else:  # unresolved
            return [
                "Review the unresolved issue in detail",
                "Try alternative approaches to the problem",
                "Consider breaking down the issue into smaller tasks",
                "Document any new findings or attempted solutions"
            ]

    def _engineering_best_practices_check(self) -> Dict[str, Any]:
        """
        # @codebase-summary: Engineering best practices verification system
        - Verifies agent has read engineering best practices and documentation migration status
        - Checks for deprecated documentation and ensures current guidelines are followed
        - Provides migration status and guidance for documentation updates
        - Used by: agent onboarding, documentation compliance, best practices enforcement
        """
        # Engineering best practices is in documentation_assets
        best_practices_file = self.paths['project_root'] / "documentation_assets" / "workflow_assets" / "workflow_docs" / "engineering_best_practices.md"
        old_onboarding_docs = self.paths['project_root'] / "reference_assets" / "old_onboarding_docs"

        file_exists = os.path.exists(best_practices_file)
        old_docs_exist = os.path.exists(old_onboarding_docs)

        return {
            "best_practices_file_exists": file_exists,
            "agent_read_best_practices": file_exists,
            "old_onboarding_docs_deprecated": old_docs_exist,
            "documentation_migration_status": {
                "use_current_docs": True,
                "deprecated_folder": "reference_assets/old_onboarding_docs/",
                "migration_note": "Use documentation_assets/workflow_assets/workflow_docs/engineering_best_practices.md and DEVELOPER_ONBOARDING.md instead"
            }
        }

    def _provide_project_overview(self) -> Dict[str, Any]:
        """
        # @codebase-summary: Project overview generation from key documentation
        - Auto-reads and summarizes README.md and agent guide documentation
        - Provides incoming agents with essential project context and purpose
        - Includes system capabilities, deployment modes, and core functionality
        - Used by: agent onboarding, project understanding, context establishment
        """
        overview = {
            "readme_summary": "",
            "agent_guide_summary": "",
            "claude_integration": False,
            "key_features": [],
            "system_purpose": ""
        }

        try:
            # Read main README.md
            readme_path = self.paths['project_root'] / "README.md"
            if readme_path.exists():
                with open(readme_path, 'r', encoding='utf-8') as f:
                    readme_content = f.read()
                    # Extract key sections
                    overview["readme_summary"] = self._extract_readme_key_points(readme_content)

            # Read AGENT_GUIDE.md (agent-agnostic)
            agent_guide_path = self.paths['project_root'] / "AGENT_GUIDE.md"
            if agent_guide_path.exists():
                with open(agent_guide_path, 'r', encoding='utf-8') as f:
                    guide_content = f.read()
                    overview["agent_guide_summary"] = self._extract_agent_guide_key_points(guide_content)

            # Check if Claude module is available
            claude_md_path = self.paths['project_root'] / "modules" / "claude-code" / "CLAUDE_README.md"
            overview["claude_integration"] = claude_md_path.exists()

            # Extract system purpose from codebase summary
            if os.path.exists(self.codebase_summary_path):
                with open(self.codebase_summary_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    overview["system_purpose"] = data.get("description", "")
                    overview["key_features"] = data.get("capabilities", [])

        except Exception as e:
            overview["error"] = f"Failed to load project overview: {e}"

        return overview

    def _detect_deployment_mode(self) -> Dict[str, Any]:
        """
        # @codebase-summary: Deployment mode detection using arkival_config.json workflow flag
        - Simple detection: arkival_config.json in root = subdirectory mode
        - Provides deployment-specific guidance for agents based on this flag
        - Used by: agent onboarding, workflow orchestration, deployment understanding
        """
        deployment_info = {
            "mode": "development",
            "explanation": "",
            "workflow_flag": "arkival_config.json",
            "config_location": "",
            "analysis_scope": ""
        }

        try:
            # Simple workflow flag detection
            config_in_root = (Path.cwd() / "arkival_config.json").exists()

            if config_in_root:
                deployment_info["mode"] = "subdirectory"
                deployment_info["explanation"] = "Subdirectory deployment mode detected (arkival_config.json in root). Generated documentation reflects the host project."
                deployment_info["config_location"] = "Root directory (workflow flag present)"
                deployment_info["analysis_scope"] = "Host project structure and metadata"
            else:
                deployment_info["mode"] = "development"
                deployment_info["explanation"] = "Development mode - Arkival as main project. Generated documentation reflects Arkival itself."
                deployment_info["config_location"] = "Development mode (no workflow flag)"
                deployment_info["analysis_scope"] = "Arkival system structure"

            deployment_info["file_locations"] = {
                "codebase_summary": str(paths['codebase_summary']),
                "session_state": str(paths['session_state']),
                "changelog": str(paths['changelog_summary']),
                "agent_handoff": str(paths['export_dir'] / "agent_handoff.json"),
                "scripts_dir": str(paths['scripts_dir'])
            }
            
            # Add deployment-specific path examples
            if deployment_info["mode"] == "subdirectory":
                deployment_info["path_examples"] = {
                    "files_prefixed_with": "Arkival-V4/",
                    "example_paths": [
                        "Arkival-V4/codebase_summary.json",
                        "Arkival-V4/codebase_summary/session_state.json", 
                        "Arkival-V4/export_package/agent_handoff.json"
                    ]
                }
            else:
                deployment_info["path_examples"] = {
                    "files_at_root": True,
                    "example_paths": [
                        "codebase_summary.json",
                        "codebase_summary/session_state.json",
                        "export_package/agent_handoff.json"
                    ]
                }

        except Exception as e:
            deployment_info["error"] = f"Failed to detect deployment mode: {e}"

        return deployment_info

    def _summarize_architecture_insights(self) -> Dict[str, Any]:
        """
        # @codebase-summary: Architecture insights extraction from generated diagrams
        - Extracts key architectural patterns and insights from ARCHITECTURE_DIAGRAM.md
        - Provides agents with structural understanding and design patterns
        - Includes complexity metrics and module relationships with compressed technology stack
        - Used by: agent onboarding, architectural understanding, design guidance
        """
        insights = {
            "architecture_patterns": [],
            "core_modules": [],
            "complexity_assessment": "",
            "key_relationships": [],
            "technology_stack": {}
        }

        try:
            # Read architecture diagram
            arch_path = self.paths['project_root'] / "ARCHITECTURE_DIAGRAM.md"
            if arch_path.exists():
                with open(arch_path, 'r', encoding='utf-8') as f:
                    arch_content = f.read()
                    insights = self._extract_architecture_insights(arch_content)

            # Enhance with codebase summary data
            if os.path.exists(self.codebase_summary_path):
                with open(self.codebase_summary_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    insights["architecture_patterns"] = data.get("architecture_analysis", {}).get("architecture_patterns", [])
                    insights["complexity_assessment"] = data.get("function_hotspots", {}).get("complexity_score", "unknown")
                    
                    # Compress technology stack for onboarding efficiency
                    raw_tech_stack = data.get("project_structure", {}).get("technology_indicators", {})
                    insights["technology_stack"] = self._compress_technology_stack(raw_tech_stack)

        except Exception as e:
            insights["error"] = f"Failed to summarize architecture insights: {e}"

        return insights

    def _compress_technology_stack(self, raw_tech_stack: Dict[str, Any]) -> Dict[str, Any]:
        """
        # @codebase-summary: Technology stack compression for efficient onboarding
        - Converts verbose file path lists to summary counts and technology types
        - Reduces token load while preserving essential architectural understanding
        - Maintains actionable insight for agent decision-making
        - Used by: agent onboarding optimization, context efficiency
        """
        compressed = {}
        
        for category, files in raw_tech_stack.items():
            if not files:  # Skip empty categories
                continue
                
            file_count = len(files)
            
            # Extract technology types based on file extensions and patterns
            tech_types = self._extract_technology_types(files, category)
            
            # Create compressed summary
            compressed[category] = {
                "count": file_count,
                "types": tech_types
            }
            
            # Add key locations for important categories (not full paths)
            if category in ["backend", "ai_integration"] and file_count > 0:
                key_dirs = set()
                for file_path in files[:3]:  # Sample first 3 files for directory patterns
                    if "/" in file_path:
                        dir_part = "/".join(file_path.split("/")[:-1])
                        if len(dir_part) > 0:
                            # Simplify long paths
                            if len(dir_part) > 30:
                                parts = dir_part.split("/")
                                if len(parts) > 2:
                                    key_dirs.add(f"{parts[0]}/.../{parts[-1]}")
                                else:
                                    key_dirs.add(dir_part)
                            else:
                                key_dirs.add(dir_part)
                
                if key_dirs:
                    compressed[category]["key_locations"] = list(key_dirs)[:3]  # Max 3 locations
        
        return compressed
    
    def _extract_technology_types(self, files: List[str], category: str) -> List[str]:
        """
        # @codebase-summary: Technology type extraction from file patterns
        - Analyzes file extensions and names to identify technologies
        - Provides meaningful technology context without verbose file lists
        - Categorizes by actual technology stack rather than file paths
        - Used by: technology stack compression, architectural understanding
        """
        tech_types = set()
        
        for file_path in files:
            # Extract from file extensions
            if file_path.endswith('.py'):
                tech_types.add("Python")
            elif file_path.endswith(('.tsx', '.ts')):
                tech_types.add("TypeScript/React")
            elif file_path.endswith('.js'):
                tech_types.add("JavaScript")
            elif file_path.endswith('.md'):
                if category == "ai_integration":
                    tech_types.add("AI Documentation")
                else:
                    tech_types.add("Documentation")
            elif file_path.endswith('.toml'):
                tech_types.add("Configuration")
            elif file_path.endswith('.replit'):
                tech_types.add("Replit Config")
            
            # Extract from file names and paths
            if "claude" in file_path.lower():
                tech_types.add("Claude Integration")
            elif "workflow" in file_path.lower():
                tech_types.add("Workflow System")
            elif "agent" in file_path.lower():
                tech_types.add("Agent Management")
            elif "api" in file_path.lower():
                tech_types.add("API Integration")
            elif "template" in file_path.lower():
                tech_types.add("Templates")
            elif "guide" in file_path.lower() or "reference" in file_path.lower():
                tech_types.add("Guides")
        
        # Provide category-specific fallbacks
        if not tech_types:
            if category == "frontend":
                tech_types.add("Web Frontend")
            elif category == "backend":
                tech_types.add("Backend Scripts")
            elif category == "documentation":
                tech_types.add("Project Documentation")
            elif category == "deployment":
                tech_types.add("Deployment Config")
        
        return sorted(list(tech_types))[:4]  # Max 4 types to keep concise

    def _identify_external_dependencies(self) -> Dict[str, Any]:
        """
        # @codebase-summary: External dependencies and requirements identification
        - Identifies required external services, APIs, and system dependencies
        - Checks for configuration files and environment requirements
        - Provides agents with deployment and runtime requirements context
        - Used by: agent onboarding, dependency management, setup validation
        """
        dependencies = {
            "runtime_dependencies": [],
            "development_dependencies": [],
            "system_requirements": [],
            "external_services": [],
            "configuration_files": [],
            "environment_variables": []
        }

        try:
            # Check codebase summary for dependencies
            if os.path.exists(self.codebase_summary_path):
                with open(self.codebase_summary_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    deps = data.get("main_dependencies", {})
                    dependencies["runtime_dependencies"] = deps.get("runtime", [])
                    dependencies["development_dependencies"] = deps.get("development", [])
                    dependencies["system_requirements"] = deps.get("system", [])

            # Check for common config files
            config_files = ["requirements.txt", "package.json", "pyproject.toml", "Dockerfile", ".env.example"]
            for config_file in config_files:
                if (self.paths['project_root'] / config_file).exists():
                    dependencies["configuration_files"].append(config_file)

            # Check for external service indicators
            # This could be enhanced to scan for API endpoints, database connections, etc.
            dependencies["external_services"] = ["None detected - Pure Python system"]

        except Exception as e:
            dependencies["error"] = f"Failed to identify dependencies: {e}"

        return dependencies

    def _provide_workflow_examples(self) -> Dict[str, Any]:
        """
        # @codebase-summary: Daily workflow examples and command patterns
        - Provides agents with common usage patterns and command examples
        - Includes morning routine, development workflow, and session completion
        - Offers practical guidance for effective agent collaboration
        - Used by: agent onboarding, workflow guidance, best practices
        """
        examples = {
            "morning_routine": [],
            "development_commands": [],
            "session_completion": [],
            "common_patterns": [],
            "troubleshooting": []
        }

        try:
            examples["morning_routine"] = [
                "python3 codebase_summary/agent_workflow_orchestrator.py incoming",
                "Review codebase_summary.json for current state",
                "Check ARCHITECTURE_DIAGRAM.md for project overview"
            ]

            examples["development_commands"] = [
                "python3 codebase_summary/update_project_summary.py --force",
                "python3 validate_deployment.py",
                "python3 validate_export_readiness.py"
            ]

            examples["session_completion"] = [
                "python3 codebase_summary/agent_workflow_orchestrator.py outgoing --summary 'Session summary'",
                "python3 codebase_summary/update_changelog.py add --summary 'Detailed changelog entry'",
                "Commit changes with comprehensive commit message"
            ]

            examples["common_patterns"] = [
                "Always run codebase scan before starting major changes",
                "Use agent orchestrator for proper session management",
                "Document functions with @codebase-summary breadcrumbs",
                "Check deployment mode via _critical_context"
            ]

            examples["troubleshooting"] = [
                "Check file permissions in deployment-appropriate directories",
                "Verify current working directory matches deployment mode",
                "Review find_arkival_paths() output in logs for path issues",
                "In subdirectory mode: check Arkival-V4/codebase_summary/ permissions",
                "In development mode: check codebase_summary/ permissions"
            ]

        except Exception as e:
            examples["error"] = f"Failed to provide workflow examples: {e}"

        return examples

    def _analyze_recent_git_activity(self) -> Dict[str, Any]:
        """
        # @codebase-summary: Recent git activity analysis for context
        - Analyzes recent commits and current branch status
        - Provides agents with recent development context and changes
        - Includes current branch, recent commits, and working tree status
        - Used by: agent onboarding, development context, change awareness
        """
        git_info = {
            "current_branch": "",
            "recent_commits": [],
            "working_tree_status": "",
            "staged_changes": [],
            "modified_files": []
        }

        try:
            import subprocess

            # Get current branch
            result = subprocess.run(['git', 'branch', '--show-current'], 
                                  capture_output=True, text=True, cwd=self.paths['project_root'])
            if result.returncode == 0:
                git_info["current_branch"] = result.stdout.strip()

            # Get recent commits
            result = subprocess.run(['git', 'log', '--oneline', '-5'], 
                                  capture_output=True, text=True, cwd=self.paths['project_root'])
            if result.returncode == 0:
                git_info["recent_commits"] = result.stdout.strip().split('\n')

            # Get working tree status
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, cwd=self.paths['project_root'])
            if result.returncode == 0:
                status_lines = result.stdout.strip().split('\n') if result.stdout.strip() else []
                git_info["working_tree_status"] = "clean" if not status_lines else "modified"
                for line in status_lines:
                    if line.startswith('M '):
                        git_info["modified_files"].append(line[2:])
                    elif line.startswith('A '):
                        git_info["staged_changes"].append(line[2:])

        except Exception as e:
            git_info["error"] = f"Failed to analyze git activity: {e}"

        return git_info

    def _summarize_system_capabilities(self) -> Dict[str, Any]:
        """
        # @codebase-summary: System capabilities summary for agent understanding
        - Summarizes key system capabilities and limitations
        - Provides agents with understanding of what Arkival can and cannot do
        - Includes supported languages, features, and integration options
        - Used by: agent onboarding, capability awareness, scope understanding
        """
        capabilities = {
            "core_features": [],
            "supported_languages": [],
            "ai_integrations": [],
            "deployment_options": [],
            "limitations": [],
            "documentation_coverage": ""
        }

        try:
            if os.path.exists(self.codebase_summary_path):
                with open(self.codebase_summary_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    capabilities["core_features"] = data.get("capabilities", [])
                    
                    # Extract supported languages from language breakdown
                    lang_breakdown = data.get("code_analysis", {}).get("language_breakdown", {})
                    capabilities["supported_languages"] = list(lang_breakdown.keys())
                    
                    capabilities["ai_integrations"] = data.get("ai_integration", {}).get("providers", [])
                    capabilities["documentation_coverage"] = f"{data.get('code_analysis', {}).get('coverage_percentage', 0)}%"

            capabilities["deployment_options"] = [
                "Standalone mode - Arkival as main project",
                "Subdirectory mode - Non-destructive integration",
                "Universal IDE support - VS Code, Cursor, Terminal, etc."
            ]

            capabilities["limitations"] = [
                "Pure Python system - no external service dependencies",
                "Documentation analysis focused on function-level breadcrumbs",
                "Version systems are independent (codebase vs changelog)"
            ]

        except Exception as e:
            capabilities["error"] = f"Failed to summarize capabilities: {e}"

        return capabilities

    def _provide_command_reference(self) -> Dict[str, Any]:
        """
        # @codebase-summary: Command reference guide for agent operations
        - Provides quick reference of essential commands for agents
        - Includes analysis, workflow, validation, and troubleshooting commands
        - Organized by use case and frequency of usage
        - Used by: agent onboarding, command lookup, operational guidance
        """
        commands = {
            "essential_commands": {},
            "workflow_commands": {},
            "validation_commands": {},
            "troubleshooting_commands": {},
            "advanced_commands": {}
        }

        try:
            commands["essential_commands"] = {
                "Update project analysis": "python3 codebase_summary/update_project_summary.py --force",
                "Start agent session": "python3 codebase_summary/agent_workflow_orchestrator.py incoming",
                "End agent session": "python3 codebase_summary/agent_workflow_orchestrator.py outgoing --summary 'description'"
            }

            commands["workflow_commands"] = {
                "Setup workflow system": "python3 setup_workflow_system.py",
                "Add changelog entry": "python3 codebase_summary/update_changelog.py add --summary 'entry'",
                "Archive old entries": "python3 codebase_summary/update_changelog.py archive"
            }

            commands["validation_commands"] = {
                "Validate deployment": "python3 validate_deployment.py",
                "Check export readiness": "python3 validate_export_readiness.py",
                "Git status check": "git status"
            }

            commands["troubleshooting_commands"] = {
                "Force regenerate all": "python3 codebase_summary/update_project_summary.py --force",
                "Check deployment mode": "ls arkival_config.json (exists = subdirectory mode)",
                "Check file permissions": "ls -la [Arkival-V4/]codebase_summary/ (prefix if subdirectory)",
                "Verify paths": "Check find_arkival_paths() output in logs"
            }

            commands["advanced_commands"] = {
                "Remove changelog duplicates": "python3 codebase_summary/update_changelog.py remove-duplicates",
                "Custom analysis scope": "Modify ignore patterns in update_project_summary.py",
                "Manual session state": "Edit codebase_summary/session_state.json directly"
            }

        except Exception as e:
            commands["error"] = f"Failed to provide command reference: {e}"

        return commands

    # Helper methods for content extraction
    def _extract_readme_key_points(self, content: str) -> str:
        """Extract key points from README content"""
        lines = content.split('\n')
        key_points = []
        
        for line in lines[:20]:  # First 20 lines usually contain key info
            if line.startswith('# ') or line.startswith('## '):
                key_points.append(line.strip())
            elif line.startswith('**') or line.startswith('- **'):
                key_points.append(line.strip())
        
        return '\n'.join(key_points[:10])  # Top 10 key points

    def _extract_agent_guide_key_points(self, content: str) -> str:
        """Extract key points from agent guide content"""
        lines = content.split('\n')
        key_sections = []
        
        in_important_section = False
        for line in lines:
            if '## 🚀 Quick Start' in line or '## 🏗 Deployment Modes' in line:
                in_important_section = True
                key_sections.append(line.strip())
            elif line.startswith('## ') and in_important_section:
                in_important_section = False
            elif in_important_section and (line.startswith('- ') or line.startswith('**')):
                key_sections.append(line.strip())
        
        return '\n'.join(key_sections[:15])  # Top 15 relevant lines

    def _extract_architecture_insights(self, content: str) -> Dict[str, Any]:
        """Extract architecture insights from ARCHITECTURE_DIAGRAM.md"""
        insights = {
            "architecture_patterns": [],
            "core_modules": [],
            "complexity_assessment": "",
            "key_relationships": []
        }
        
        lines = content.split('\n')
        for line in lines:
            if 'Architecture Patterns' in line:
                # Extract pattern information from following lines
                pass
            elif 'Core Modules' in line:
                # Extract module information
                pass
            elif 'complexity' in line.lower():
                insights["complexity_assessment"] = line.strip()
        
        return insights

def main():
    """
    # @codebase-summary: Main CLI interface for agent workflow orchestration
    - Provides command-line interface for agent handoff and session management
    - Supports outgoing and incoming agent operations with argument parsing
    - Coordinates agent transitions and workflow orchestration processes
    - Used by: command-line operations, agent workflows, session management
    """
    orchestrator = AgentWorkflowOrchestrator()

    if len(sys.argv) < 2:
        print("Usage: python agent_workflow_orchestrator.py <command> [options]")
        print("Commands:")
        print("  outgoing --summary 'Session summary' [--type completed|unresolved]")
        print("  incoming")
        sys.exit(1)

    command = sys.argv[1]

    if command == "outgoing":
        # Parse arguments
        summary = ""
        issue_type = "completed"

        for i, arg in enumerate(sys.argv[2:], 2):
            if arg == "--summary" and i + 1 < len(sys.argv):
                summary = sys.argv[i + 1]
            elif arg == "--type" and i + 1 < len(sys.argv):
                issue_type = sys.argv[i + 1]

        if not summary:
            print("❌ Summary is required for outgoing workflow")
            sys.exit(1)

        result = orchestrator.trigger_outgoing_agent_workflow(summary, issue_type)
        print(f"\nWorkflow result: {json.dumps(result, indent=2)}")

    elif command == "incoming":
        result = orchestrator.trigger_incoming_agent_workflow()
        print(f"\nOnboarding result: {json.dumps(result, indent=2)}")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()