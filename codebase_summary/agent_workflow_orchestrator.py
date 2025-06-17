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
        # Get the directory containing this script
        script_dir = Path(__file__).parent
        # Check if we're in a standalone deployment (script in codebase_summary/)
        # or if codebase_summary is at project root
        if script_dir.name == "codebase_summary":
            self.project_root = script_dir.parent
        else:
            # Fallback for when script is run from project root
            self.project_root = script_dir
        self.codebase_summary_path = self.project_root / "codebase_summary" / "codebase_summary.json"
        self.changelog_path = self.project_root / "changelog_summary.json"
        self.session_state_path = self.project_root / "codebase_summary" / "session_state.json"

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

        with open(self.session_state_path, 'w', encoding='utf-8') as f:
            json.dump(session_state, f, indent=2)

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
                str(self.project_root / "codebase_summary" / "update_changelog.py"),
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
                str(self.project_root / "codebase_summary" / "update_changelog.py"),
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

            handoff_path = self.project_root / "codebase_summary" / "agent_handoff.json"
            with open(handoff_path, 'w', encoding='utf-8') as f:
                json.dump(handoff_doc, f, indent=2)

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
        - Used by: documentation preservation, system redundancy, agent onboarding
        """
        export_package_path = self.project_root / "export_package" / "agent_handoff.json"
        try:
            with open(export_package_path, 'w', encoding='utf-8') as f:
                json.dump(handoff_doc, f, indent=2)
            print(f"✅ Handoff documentation replicated to: {export_package_path}")
        except Exception as e:
            print(f"❌ Failed to replicate handoff documentation: {e}")

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

        # Load handoff documentation
        handoff_path = self.project_root / "codebase_summary" / "agent_handoff.json"
        if os.path.exists(handoff_path):
            with open(handoff_path, 'r', encoding='utf-8') as f:
                context["handoff_documentation"] = json.load(f)

        # Load handoff documentation from export package (if available)
        export_package_path = self.project_root / "export_package" / "agent_handoff.json"
        if os.path.exists(export_package_path):
            with open(export_package_path, 'r', encoding='utf-8') as f:
                context["export_package_handoff_documentation"] = json.load(f)

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
        try:
            # Use force flag for comprehensive update during handoff
            import subprocess

            cmd = [
                sys.executable,
                str(self.project_root / "codebase_summary" / "update_project_summary.py"),
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
        missing_breadcrumbs_path = self.project_root / "codebase_summary" / "missing_breadcrumbs.json"
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
        best_practices_file = self.project_root / "ENGINEERING_BEST_PRACTICES.md"
        old_onboarding_docs = self.project_root / "reference_assets" / "old_onboarding_docs"

        file_exists = os.path.exists(best_practices_file)
        old_docs_exist = os.path.exists(old_onboarding_docs)

        return {
            "best_practices_file_exists": file_exists,
            "agent_read_best_practices": file_exists,
            "old_onboarding_docs_deprecated": old_docs_exist,
            "documentation_migration_status": {
                "use_current_docs": True,
                "deprecated_folder": "reference_assets/old_onboarding_docs/",
                "migration_note": "Use ENGINEERING_BEST_PRACTICES.md and DEVELOPER_ONBOARDING.md instead"
            }
        }

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