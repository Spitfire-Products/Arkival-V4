#!/usr/bin/env python3
"""
Enhanced Changelog Management Script with Workflow Orchestration
Automatically tracks development progress during AI collaboration sessions
Enhanced with comprehensive workflow orchestration integration, version correlation, and archive management
Version: 2.0 - Enhanced Features Enabled
"""

import json
import os
import sys
import shutil
import glob
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
import re

def find_arkival_paths():
    """
    Universal path resolution for Arkival subdirectory deployment
    Returns: Dict with all required paths
    """
    current_dir = Path.cwd()
    project_root = None
    
    # Search upward for arkival.config.json
    search_path = current_dir
    for _ in range(5):  # Max 5 levels up
        if (search_path / "arkival.config.json").exists():
            project_root = search_path
            break
        if search_path.parent == search_path:  # Reached filesystem root
            break
        search_path = search_path.parent
    
    # Try alternative detection methods
    if not project_root:
        # Look for Arkival directory as indicator
        search_path = current_dir
        for _ in range(5):
            if (search_path / "Arkival").exists():
                project_root = search_path
                break
            search_path = search_path.parent
    
    # Fallback - assume current directory
    if not project_root:
        project_root = current_dir
    
    # Return all paths
    return {
        'project_root': project_root,
        'config_file': project_root / "arkival.config.json",
        'arkival_dir': project_root / "Arkival",
        'data_dir': project_root / "Arkival" / "data",
        'scripts_dir': project_root / "Arkival" / "codebase_summary", 
        'export_dir': project_root / "Arkival" / "export_package",
        'checkpoints_dir': project_root / "Arkival" / "checkpoints",
        
        # Data files
        'codebase_summary': project_root / "Arkival" / "data" / "codebase_summary.json",
        'changelog_summary': project_root / "Arkival" / "data" / "changelog_summary.json",
        'session_state': project_root / "Arkival" / "data" / "session_state.json",
        'missing_breadcrumbs': project_root / "Arkival" / "data" / "missing_breadcrumbs.json"
    }

# Enhanced Features Enabled - Version 2.0
ENHANCED_FEATURES_ENABLED = True
WORKFLOW_ORCHESTRATION_INTEGRATION = True
VERSION_CORRELATION_TRACKING = True
ARCHIVE_MANAGEMENT_SYSTEM = True

# enhanced changelog functionality - deployment validation marker
ENHANCED_CHANGELOG_FUNCTIONALITY = True

def get_project_root():
    """
    # @codebase-summary: Project root directory resolution utility
    - Uses universal path resolution for Arkival subdirectory deployment
    - Provides consistent path resolution across different execution contexts
    - Used by: all file operations, path management, configuration loading
    """
    return find_arkival_paths()['project_root']

def load_changelog() -> Dict[str, Any]:
    """
    # @codebase-summary: Changelog data loading and initialization
    - Loads existing changelog from Arkival/data/ directory
    - Handles file corruption gracefully with fallback defaults
    - Used by: all changelog operations, workflow triggers
    - Returns: Standard changelog data structure with workflow integration
    """
    paths = find_arkival_paths()
    changelog_path = paths['changelog_summary']

    if os.path.exists(changelog_path):
        try:
            with open(changelog_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading changelog: {e}")

    # Return structure matching actual file
    return {
        "project_name": "New Project",
        "changelog_version": "1.0.0",
        "last_updated": "",
        "description": "Comprehensive changelog tracking all significant changes",
        "workflow_integration": {
            "auto_triggered": True,
            "agent_handoff_ready": False,
            "last_workflow_trigger": None
        },
        "entries": [],
        "statistics": {
            "total_entries": 0,
            "entries_by_type": {},
            "entries_by_scope": {}
        }
    }

def get_codebase_version() -> str:
    """
    # @codebase-summary: Codebase version extraction for correlation tracking
    - Retrieves current version from codebase_summary.json for synchronization
    - Provides fallback version handling for missing or corrupted files
    - Used by: version correlation, changelog synchronization, deployment tracking
    """
    try:
        project_root = get_project_root()
        codebase_path = project_root / "codebase_summary.json"
        with open(codebase_path, 'r', encoding='utf-8') as f:
            codebase_data = json.load(f)
            return codebase_data.get("version", "1.0.0")
    except:
        return "1.0.0"

def get_checkpoint_version() -> str:
    """
    # @codebase-summary: Checkpoint version tracking and increment calculation
    - Parses checkpoint log to find highest version for proper increment logic
    - Handles version comparison and sorting for accurate version progression
    - Used by: checkpoint management, version progression, deployment coordination
    """
    try:
        checkpoint_path = find_arkival_paths()['checkpoints_dir'] / "checkpoint_log.md"
        with open(checkpoint_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Extract all checkpoint versions and find the highest one
            version_matches = re.findall(r'Version.*?(\d+\.\d+\.\d+)', content)
            if version_matches:
                # Parse versions and find the highest one
                versions = []
                for v in version_matches:
                    try:
                        parts = v.split('.')
                        versions.append((int(parts[0]), int(parts[1]), int(parts[2]), v))
                    except:
                        continue
                
                if versions:
                    # Sort by major, minor, patch and return the highest version string
                    highest = max(versions, key=lambda x: (x[0], x[1], x[2]))
                    return highest[3]  # Return the version string
    except:
        pass
    
    # Fallback to codebase summary version
    try:
        with open("codebase_summary.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("version", "1.0.0")
    except:
        pass
    
    return "1.0.0"  # Use fallback version

def increment_version_by_type(current_version: str, change_type: str) -> str:
    """
    # @codebase-summary: Semantic version increment system based on change type
    - Implements semantic versioning rules for major, minor, and patch increments
    - Maps change types to appropriate version increments (breaking->major, feature->minor, fix->patch)
    - Used by: automated versioning, changelog generation, deployment coordination
    """
    try:
        parts = current_version.split('.')
        major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
        
        if change_type in ["breaking"]:
            major += 1
            minor = 0
            patch = 0
        elif change_type in ["feature", "enhancement"]:
            minor += 1
            patch = 0
        else:  # fix, refactor, etc.
            patch += 1
            
        return f"{major}.{minor}.{patch}"
    except Exception as e:
        return "1.0.1"  # Fallback to next logical version

def update_statistics(changelog: Dict[str, Any]) -> None:
    """
    # @codebase-summary: Changelog statistics calculation and aggregation system
    - Calculates entry counts by type and scope for analytics
    - Maintains comprehensive statistics for project tracking
    - Used by: analytics, reporting, changelog management, project metrics
    """
    entries = changelog.get("entries", [])
    total_entries = len(entries)

    # Count by type
    type_counts = {}
    scope_counts = {}

    for entry in entries:
        entry_type = entry.get("type", "unknown")
        entry_scope = entry.get("scope", "unknown")

        type_counts[entry_type] = type_counts.get(entry_type, 0) + 1
        scope_counts[entry_scope] = scope_counts.get(entry_scope, 0) + 1

    changelog["statistics"] = {
        "total_entries": total_entries,
        "entries_by_type": type_counts,
        "entries_by_scope": scope_counts
    }

def create_automated_checkpoint(change_type: str, summary: str, changelog_version: str) -> None:
    """
    # @codebase-summary: Automated checkpoint creation and management system
    - Creates automated checkpoints for significant changes in project development
    - Maintains version synchronization between changelog and checkpoint logs
    - Used by: automated tracking, checkpoint management, version correlation
    """
    # Only create checkpoints for significant changes
    significant_changes = ["feature", "enhancement", "refactor", "fix", "breaking"]
    
    if change_type not in significant_changes:
        return
    
    checkpoint_path = find_arkival_paths()['checkpoints_dir'] / "checkpoint_log.md"
    
    try:
        # Create checkpoint directory if it doesn't exist
        checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Read existing content or regenerate if missing/corrupted
        if os.path.exists(checkpoint_path):
            try:
                with open(checkpoint_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if content has proper header and generator attribution
                if not content.startswith("# Export Package - Checkpoint Log") or "Generated by:" not in content:
                    print(f"⚠️  Regenerating checkpoint_log.md - missing proper header/attribution")
                    content = None
                    
            except (IOError, UnicodeDecodeError) as e:
                print(f"⚠️  Regenerating checkpoint_log.md - file corrupted: {e}")
                content = None
        else:
            content = None
            
        if content is None:
            # Regenerate the file with proper header and attribution
            content = """# Export Package - Checkpoint Log

*Generated by: codebase_summary/update_changelog.py - Automated changelog and version tracking system*
*Automated checkpoint system*

This log tracks both manual and automated checkpoints for the export package project.

"""
        
        # Use the exact changelog version for the checkpoint
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        new_checkpoint = f"""## Automated Checkpoint: {timestamp}

### Project State
- **Version**: {changelog_version} (matches changelog entry)
- **Features**: Recent development progress with {change_type} changes
- **Status**: Active development - automated checkpoint
- **Type**: Automated checkpoint

### Recent Changes
- {summary}

### Notes
This automated checkpoint was created following significant {change_type} changes to track development progress.

---

"""
        
        # Insert new checkpoint after the header but before existing content
        lines = content.split('\n')
        header_end = 0
        for i, line in enumerate(lines):
            if line.startswith('##') and 'Checkpoint:' in line:
                header_end = i
                break
        
        if header_end == 0:
            # No existing checkpoints, add after main header
            for i, line in enumerate(lines):
                if line.strip() and not line.startswith('#'):
                    header_end = i
                    break
        
        # Insert new checkpoint
        updated_lines = lines[:header_end] + new_checkpoint.split('\n') + lines[header_end:]
        updated_content = '\n'.join(updated_lines)
        
        # Write updated content
        with open(checkpoint_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ Created automated checkpoint (v{changelog_version})")
        
    except Exception as e:
        print(f"⚠️  Failed to create automated checkpoint: {e}")

def save_changelog(changelog: Dict[str, Any]) -> bool:
    """
    # @codebase-summary: Changelog persistence and file management system
    - Saves changelog data to project root with error handling
    - Maintains enhanced structure with workflow integration support
    - Used by: changelog updates, workflow triggers, version tracking
    """
    try:
        changelog["last_updated"] = datetime.now().isoformat() + "Z"
        update_statistics(changelog)

        # Add generator information
        changelog_with_generator = {
            "_generator": "Generated by codebase_summary/update_changelog.py - Automated changelog and version tracking system",
            **changelog
        }
        
        project_root = get_project_root()
        changelog_path = project_root / "changelog_summary.json"
        
        try:
            # Ensure parent directory exists
            changelog_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(changelog_path, 'w', encoding='utf-8') as f:
                json.dump(changelog_with_generator, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"⚠️  Failed to save changelog to {changelog_path}: {e}")
            # Try backup location
            backup_path = project_root / "changelog_summary_backup.json"
            try:
                with open(backup_path, 'w', encoding='utf-8') as f:
                    json.dump(changelog_with_generator, f, indent=2, ensure_ascii=False)
                print(f"✅ Saved changelog to backup location: {backup_path}")
            except Exception as backup_error:
                print(f"❌ Failed to save changelog to backup: {backup_error}")
                return False
        return True
    except Exception as e:
        print(f"Error saving changelog: {e}")
        return False

def cleanup_changelog() -> bool:
    """
    # @codebase-summary: Changelog cleanup and consistency validation system
    - Removes duplicate entries and ensures version consistency across changelog
    - Maintains data integrity and proper chronological ordering
    - Used by: data maintenance, consistency validation, cleanup operations
    """
    changelog = load_changelog()

    print("🧹 Cleaning up changelog...")

    # Remove duplicates based on timestamp and summary
    entries = changelog.get("entries", [])
    seen_combinations = set()
    unique_entries = []
    removed_count = 0

    for entry in entries:
        # Create a unique key based on timestamp and summary
        key = (entry.get("timestamp", ""), entry.get("summary", ""))

        if key not in seen_combinations:
            seen_combinations.add(key)
            unique_entries.append(entry)
        else:
            print(f"Removing duplicate entry: {entry.get('id', 'unknown')}")
            removed_count += 1

    changelog["entries"] = unique_entries

    if removed_count > 0:
        print(f"Removed {removed_count} duplicate entries")

    # Correlate versions
    codebase_version = get_codebase_version()
    changelog["changelog_version"] = codebase_version

    # Update workflow integration status
    changelog["workflow_integration"]["last_workflow_trigger"] = datetime.now().isoformat() + "Z"

    # Save cleaned changelog
    if save_changelog(changelog):
        print("✅ Changelog cleanup completed")
        return True
    else:
        print("❌ Failed to save cleaned changelog")
        return False

def remove_duplicate_entries(changelog: Dict[str, Any]) -> Dict[str, Any]:
    """
    # @codebase-summary: Changelog deduplication and cleanup system
    - Removes duplicate entries based on timestamp and summary combinations
    - Maintains data integrity by preserving unique entries only
    - Used by: changelog maintenance, data cleanup, entry validation
    """
    entries = changelog.get("entries", [])
    if not entries:
        return changelog
    
    seen_combinations = set()
    unique_entries = []
    
    for entry in entries:
        # Create a unique key based on timestamp and summary
        key = (entry.get("timestamp", ""), entry.get("summary", ""))
        
        if key not in seen_combinations:
            seen_combinations.add(key)
            unique_entries.append(entry)
    
    changelog["entries"] = unique_entries
    return changelog

def archive_old_entries(changelog: Dict[str, Any], max_entries: int = 25) -> Dict[str, Any]:
    """
    # @codebase-summary: Changelog archival and retention management system
    - Archives old entries when maximum count is exceeded to maintain performance
    - Creates timestamped archive files with project version correlation
    - Used by: changelog maintenance, performance optimization, historical preservation
    """
    entries = changelog.get("entries", [])
    
    if len(entries) <= max_entries:
        return changelog
    
    # Sort entries by timestamp to ensure proper ordering
    sorted_entries = sorted(entries, key=lambda x: x.get("timestamp", ""), reverse=True)
    recent_entries = sorted_entries[:max_entries]
    old_entries = sorted_entries[max_entries:]
    
    # Create archive directory
    archive_dir = "changelog_archives"
    os.makedirs(archive_dir, exist_ok=True)
    
    # Archive old entries with timestamp and project version correlation
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    project_version = get_codebase_version()
    archive_filename = f"changelog_archive_{timestamp}_v{project_version}.json"
    archive_path = os.path.join(archive_dir, archive_filename)
    
    archive_data = {
        "archived_at": datetime.now().isoformat() + "Z",
        "project_version_correlation": project_version,
        "archive_reason": f"Automatic archiving during checkpoint creation - kept {max_entries} most recent entries",
        "archived_entries_count": len(old_entries),
        "workflow_triggered": True,
        "entries": old_entries
    }
    
    try:
        with open(archive_path, 'w', encoding='utf-8') as f:
            json.dump(archive_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Archived {len(old_entries)} old entries to {archive_filename}")
    except Exception as e:
        print(f"⚠️  Failed to create archive: {e}")
    
    # Update changelog with only recent entries
    changelog["entries"] = recent_entries
    return changelog

def create_archive_index() -> None:
    """
    # @codebase-summary: Archive indexing and catalog management system
    - Creates comprehensive index of all archived changelog files
    - Maintains metadata for archived entries with workflow integration
    - Used by: archive management, historical tracking, workflow coordination
    """
    archive_dir = "changelog_archives"
    
    if not os.path.exists(archive_dir):
        return
    
    # Find all archive files
    import glob
    archive_files = glob.glob(os.path.join(archive_dir, "changelog_archive_*.json"))
    archive_index = []
    
    for archive_file in sorted(archive_files, reverse=True):
        try:
            with open(archive_file, 'r', encoding='utf-8') as f:
                archive_data = json.load(f)
            
            archive_index.append({
                "filename": os.path.basename(archive_file),
                "archived_at": archive_data.get("archived_at"),
                "project_version": archive_data.get("project_version_correlation"),
                "entries_count": archive_data.get("archived_entries_count", 0),
                "archive_reason": archive_data.get("archive_reason"),
                "workflow_triggered": archive_data.get("workflow_triggered", False)
            })
        except Exception as e:
            print(f"Warning: Could not read archive {archive_file}: {e}")
    
    # Save index
    index_path = os.path.join(archive_dir, "archive_index.json")
    index_data = {
        "last_updated": datetime.now().isoformat() + "Z",
        "total_archives": len(archive_index),
        "description": "Index of all archived changelog entries with project version correlation and workflow integration",
        "workflow_integration": {
            "auto_archiving_enabled": True,
            "last_workflow_archive": datetime.now().isoformat() + "Z"
        },
        "archives": archive_index
    }
    
    try:
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Updated archive index with {len(archive_index)} archives")
    except Exception as e:
        print(f"⚠️  Failed to update archive index: {e}")

def mark_handoff_ready(changelog: Dict[str, Any]) -> None:
    """
    # @codebase-summary: Agent handoff preparation and readiness system
    - Marks changelog as ready for agent transitions with timestamp
    - Enables workflow orchestration for seamless agent handoffs
    - Used by: agent transitions, workflow triggers, session management
    """
    if "workflow_integration" not in changelog:
        changelog["workflow_integration"] = {}

    changelog["workflow_integration"]["agent_handoff_ready"] = True
    changelog["workflow_integration"]["handoff_timestamp"] = datetime.now().isoformat() + "Z"

# @codebase-summary: Core changelog entry creation and workflow integration system
# - Creates structured changelog entries with version correlation and validation
# - Integrates with agent workflow orchestration for automated tracking  
# - Handles version incrementing, checkpoint creation, and handoff preparation
# - Used by: agent handoffs, manual workflow triggers, deployment tracking, session transitions
# - Critical path: All project changes and agent transitions flow through this function
def add_changelog_entry(
    author: str = "AI Assistant",
    version: str = "",
    change_type: str = "enhancement",
    scope: str = "development", 
    summary: str = "",
    description: str = "",
    tags: str = "",
    workflow_triggered: bool = False
) -> bool:
    if not summary:
        print("❌ Summary is required")
        return False

    changelog = load_changelog()

    # Clean up duplicates first
    changelog = remove_duplicate_entries(changelog)

    # Generate next version based on change type if not provided
    if not version:
        current_version = get_checkpoint_version()
        try:
            parts = current_version.split('.')
            major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
            
            if change_type in ["breaking"]:
                major += 1
                minor = 0
                patch = 0
            elif change_type in ["feature", "enhancement"]:
                minor += 1
                patch = 0
            else:  # fix, refactor, etc.
                patch += 1
                
            version = f"{major}.{minor}.{patch}"
        except Exception as e:
            version = "1.0.1"  # Fallback to next logical version

    # Generate change ID based on existing entries
    existing_entries = changelog.get("entries", [])
    change_count = len(existing_entries) + 1
    change_id = f"change_{change_count:03d}"

    # Create new entry matching actual structure
    new_entry = {
        "id": change_id,
        "timestamp": datetime.now().isoformat() + "Z",
        "author": author,
        "version": version,
        "type": change_type,
        "scope": scope,
        "summary": summary,
        "description": description,
        "files_changed": [
            {
                "file": "multiple",
                "action": "modified",
                "changes": [
                    "See description for details"
                ]
            }
        ],
        "breaking_changes": False,
        "migration_notes": "No migration required" if change_type != "breaking" else "Migration required",
        "related_issues": [],
        "tags": [tag.strip() for tag in tags.split(",") if tag.strip()],
        "workflow_context": {
            "triggered_by_workflow": workflow_triggered,
            "session_type": "agent_collaboration"
        }
    }

    changelog["entries"].insert(0, new_entry)  # Insert at beginning for newest-first order

    # Update changelog header version to match latest entry
    changelog["changelog_version"] = version
    changelog["last_updated"] = datetime.now().isoformat() + "Z"

    # Update workflow integration
    if "workflow_integration" not in changelog:
        changelog["workflow_integration"] = {}

    changelog["workflow_integration"]["auto_triggered"] = workflow_triggered
    changelog["workflow_integration"]["last_workflow_trigger"] = datetime.now().isoformat() + "Z"

    # Mark as ready for handoff if this is a session summary
    if "session" in summary.lower() or "handoff" in summary.lower():
        mark_handoff_ready(changelog)

    # Update statistics for session tracking
    update_statistics(changelog)

    if save_changelog(changelog):
        print(f"✅ Added changelog entry: {change_id}")

        # Create automated checkpoint for significant changes using changelog version
        create_automated_checkpoint(change_type, summary, version)

        # Update project summary if this is a significant change
        if change_type in ["feature", "enhancement", "refactor"]:
            try:
                import subprocess
                subprocess.run([
                    sys.executable,
                    "codebase_summary/update_project_summary.py"
                ], check=False)
            except Exception:
                pass  # Continue if project summary update fails

        # Trigger workflow if this is a handoff signal
        if "update the changelog from the last entry" in summary.lower():
            try:
                print("🚀 Triggering agent handoff workflow...")
                import subprocess
                subprocess.run([
                    sys.executable,
                    "codebase_summary/agent_workflow_orchestrator.py",
                    "outgoing",
                    "--summary", summary,
                    "--type", "completed" if change_type == "feature" else "unresolved"
                ], check=False)
            except Exception as e:
                print(f"⚠️  Workflow trigger failed: {e}")

        return True
    else:
        print(f"❌ Failed to save changelog entry")
        return False


def generate_markdown_changelog():
    """
    # @codebase-summary: Markdown changelog generation from JSON data
    - Converts changelog_summary.json entries to standard CHANGELOG.md format
    - Maintains Keep a Changelog format with semantic versioning
    - Used by: changelog maintenance, markdown generation, project documentation
    """
    try:
        changelog = load_changelog()
        project_root = get_project_root()
        changelog_md_path = project_root / "CHANGELOG.md"
        
        # Generate markdown content
        content = []
        content.append("# Changelog")
        content.append("")
        content.append("All notable changes to Arkival will be documented in this file.")
        content.append("")
        content.append("The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),")
        content.append("and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).")
        content.append("")
        content.append("*Automated changelog system*")
        content.append("")
        
        # Sort entries by version (newest first)
        entries = changelog.get('entries', [])
        if not entries:
            print("⚠️  No changelog entries found")
            return False
            
        # Group entries by version
        version_groups = {}
        for entry in entries:
            version = entry.get('version', '1.0.0')
            if version not in version_groups:
                version_groups[version] = []
            version_groups[version].append(entry)
        
        # Sort versions (newest first)
        sorted_versions = sorted(version_groups.keys(), 
                               key=lambda x: [int(i) for i in x.split('.')], 
                               reverse=True)
        
        # Add [Unreleased] section if there are recent entries
        latest_entries = version_groups.get(sorted_versions[0], []) if sorted_versions else []
        from datetime import timezone
        now = datetime.now(timezone.utc)
        recent_entries = [e for e in latest_entries if (now - datetime.fromisoformat(e['timestamp'].replace('Z', '+00:00'))).days < 7]
        
        if recent_entries:
            content.append("## [Unreleased]")
            content.append("")
            
            # Group by type
            type_groups = {}
            for entry in recent_entries:
                entry_type = entry.get('type', 'changed').title()
                if entry_type not in type_groups:
                    type_groups[entry_type] = []
                type_groups[entry_type].append(entry)
            
            for entry_type in ['Added', 'Changed', 'Enhanced', 'Fixed', 'Security']:
                if entry_type.lower() in type_groups or entry_type in type_groups:
                    content.append(f"### {entry_type}")
                    entries_for_type = type_groups.get(entry_type.lower(), type_groups.get(entry_type, []))
                    for entry in entries_for_type:
                        content.append(f"- {entry['summary']}")
                    content.append("")
        
        # Add version sections
        for version in sorted_versions:
            version_entries = version_groups[version]
            
            # Get date from first entry in version
            entry_date = version_entries[0]['timestamp'][:10]  # YYYY-MM-DD
            
            content.append(f"## [{version}] - {entry_date}")
            content.append("")
            
            # Group by type
            type_groups = {}
            for entry in version_entries:
                entry_type = entry.get('type', 'changed').title()
                if entry_type == 'Enhancement':
                    entry_type = 'Enhanced'
                if entry_type not in type_groups:
                    type_groups[entry_type] = []
                type_groups[entry_type].append(entry)
            
            # Output in standard order
            for entry_type in ['Added', 'Enhanced', 'Changed', 'Fixed', 'Security']:
                if entry_type.lower() in type_groups or entry_type in type_groups:
                    content.append(f"### {entry_type}")
                    entries_for_type = type_groups.get(entry_type.lower(), type_groups.get(entry_type, []))
                    for entry in entries_for_type:
                        content.append(f"- {entry['summary']}")
                        if entry.get('description') and entry['description'].strip():
                            # Add description if present
                            desc_lines = entry['description'].strip().split('\n')
                            for desc_line in desc_lines:
                                if desc_line.strip():
                                    content.append(f"  {desc_line.strip()}")
                    content.append("")
        
        # Add footer
        content.append("---")
        content.append("")
        content.append("## Migration Guide")
        content.append("")
        content.append("### From Pre-1.0 Versions")
        content.append("This is the first stable release. Follow the setup instructions in README.md for initial deployment.")
        content.append("")
        content.append("### Upgrading to Latest Version")
        content.append("1. Back up your existing workflow_config.json")
        content.append("2. Run the setup script: `python3 setup_workflow_system.py`")
        content.append("3. Review and update configuration as needed")
        
        # Write to file
        with open(changelog_md_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        
        print(f"✅ Generated CHANGELOG.md with {len(entries)} entries across {len(sorted_versions)} versions")
        return True
        
    except Exception as e:
        print(f"❌ Failed to generate markdown changelog: {e}")
        return False


def main():
    """
    # @codebase-summary: Main changelog management CLI interface
    - Provides command-line interface for changelog operations and workflow integration
    - Handles entry creation, cleanup, and agent handoff preparation
    - Used by: manual changelog updates, workflow automation, deployment processes
    """
    if len(sys.argv) < 2:
        print("Usage: python update_changelog.py <command> [options]")
        print("Commands:")
        print("  add --summary 'Description' [--author 'Name'] [--version '1.0.x'] [--workflow-triggered]")
        print("  generate-markdown           # Generate CHANGELOG.md from JSON data")
        print("  cleanup                     # Remove duplicates and fix versions")
        print("  archive --max-entries 25    # Archive old entries")
        print("  create-index                # Rebuild archive index")
        print("  mark-handoff-ready          # Mark changelog ready for agent handoff")
        sys.exit(1)

    command = sys.argv[1]

    if command == "add":
        # Parse command line arguments
        args = {}
        workflow_triggered = False
        i = 2

        while i < len(sys.argv):
            if sys.argv[i] == '--workflow-triggered':
                workflow_triggered = True
                i += 1
            elif sys.argv[i].startswith('--') and i + 1 < len(sys.argv):
                key = sys.argv[i][2:]  # Remove --
                value = sys.argv[i + 1]
                args[key] = value
                i += 2
            else:
                i += 1

        # Use provided args or defaults
        success = add_changelog_entry(
            author=args.get('author', 'AI Assistant'),
            version=str(args.get('version') or ""),  # Will use codebase version if None
            change_type=args.get('type', 'enhancement'),
            scope=args.get('scope', 'development'),
            summary=args.get('summary', ''),
            description=args.get('description', ''),
            tags=args.get('tags', ''),
            workflow_triggered=workflow_triggered
        )

        sys.exit(0 if success else 1)

    elif command == "cleanup":
        success = cleanup_changelog()
        sys.exit(0 if success else 1)

    elif command == "archive":
        max_entries = 25
        if "--max-entries" in sys.argv:
            try:
                idx = sys.argv.index("--max-entries")
                max_entries = int(sys.argv[idx + 1])
            except (ValueError, IndexError):
                print("Invalid --max-entries value")
                sys.exit(1)

        changelog = load_changelog()
        changelog = archive_old_entries(changelog, max_entries)
        success = save_changelog(changelog)
        sys.exit(0 if success else 1)

    elif command == "create-index":
        create_archive_index()
        sys.exit(0)

    elif command == "generate-markdown":
        success = generate_markdown_changelog()
        sys.exit(0 if success else 1)

    elif command == "mark-handoff-ready":
        changelog = load_changelog()
        mark_handoff_ready(changelog)
        success = save_changelog(changelog)
        print("✅ Marked changelog as ready for agent handoff" if success else "❌ Failed to mark handoff ready")
        sys.exit(0 if success else 1)

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()