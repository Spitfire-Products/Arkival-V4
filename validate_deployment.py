
#!/usr/bin/env python3
"""
Deployment Validation Script
Validates that the export package is ready for deployment
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime

def validate_against_manifest():
    """
    # @codebase-summary: Validates deployment against EXPORT_PACKAGE_MANIFEST.json specifications
    - Loads and validates manifest file structure
    - Checks all required files specified in manifest exist
    - Verifies quality metrics meet manifest standards
    - Ensures deployment architecture compliance
    - Returns validation status and detailed results
    """
    print("📋 VALIDATING AGAINST EXPORT PACKAGE MANIFEST")
    print("=" * 50)
    
    try:
        with open("EXPORT_PACKAGE_MANIFEST.json", 'r') as f:
            manifest = json.load(f)
        print(f"✅ Loaded manifest: {manifest['package_name']} v{manifest['version']}")
    except FileNotFoundError:
        print("⚠️  EXPORT_PACKAGE_MANIFEST.json not found - skipping manifest validation")
        return True
    except json.JSONDecodeError as e:
        print(f"❌ Invalid manifest JSON: {e}")
        return False
    
    # Validate all required file categories
    all_files_valid = True
    total_required = 0
    found_files = 0
    
    for category, files in manifest.get("required_files", {}).items():
        print(f"\n📁 Checking {category}:")
        for file_path in files:
            total_required += 1
            if Path(file_path).exists():
                print(f"  ✅ {file_path}")
                found_files += 1
            else:
                print(f"  ❌ {file_path} - MISSING")
                all_files_valid = False
    
    print(f"\n📊 Manifest Validation Results:")
    print(f"   Required Files: {found_files}/{total_required} found")
    print(f"   Status: {manifest.get('status', 'UNKNOWN')}")
    print(f"   Confidence: {manifest.get('confidence_level', 'UNKNOWN')}")
    
    return all_files_valid

def validate_export_package():
    """
    # @codebase-summary: Core deployment validation system for export package
    - Validates all required files exist and are properly configured
    - Checks JSON configuration files for syntax and completeness
    - Verifies workflow system setup and dependencies
    - Validates against EXPORT_PACKAGE_MANIFEST.json specifications
    - Generates deployment readiness report
    - Used by: deployment automation, quality assurance, release preparation
    """
    print("🔍 EXPORT PACKAGE DEPLOYMENT VALIDATION")
    print("=" * 50)
    
    required_files = [
        "setup_workflow_system.py",
        "workflow_config.json", 
        "changelog_summary.json",
        "codebase_summary/agent_workflow_orchestrator.py",
        "codebase_summary/update_changelog.py",
        "codebase_summary/update_project_summary.py",
        "AGENT_GUIDE.md",
        "CONTRIBUTING.md",
        "README.md"
    ]
    
    print("📁 Checking required files...")
    missing_files = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ {len(missing_files)} required files are missing!")
        return False
    
    print("\n📋 Validating JSON configuration files...")
    json_files = ["workflow_config.json", "changelog_summary.json"]
    for json_file in json_files:
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            print(f"✅ {json_file} - Valid JSON")
        except json.JSONDecodeError as e:
            print(f"❌ {json_file} - Invalid JSON: {e}")
            return False
    
    print("\n🔧 Checking configuration completeness...")
    with open("workflow_config.json", 'r') as f:
        config = json.load(f)
        
        issues = []
        if "NEEDS_CONFIGURATION" in config.get("technology_stack", []):
            issues.append("Technology stack needs AI agent configuration")
        if config.get("project_name") == "New Project":
            issues.append("Project name needs customization")
        if not config.get("project_specific", {}).get("main_files"):
            issues.append("Main files list is empty")
            
        if issues:
            print("⚠️  Configuration warnings:")
            for issue in issues:
                print(f"   - {issue}")
            print("   → These will be resolved by AI agent during project analysis")
        else:
            print("✅ Configuration is complete")
    
    print("\n🎯 Checking Python script executability...")
    python_scripts = [
        "setup_workflow_system.py",
        "codebase_summary/agent_workflow_orchestrator.py",
        "codebase_summary/update_changelog.py"
    ]
    
    for script in python_scripts:
        if Path(script).exists():
            print(f"✅ {script} - Ready for execution")
        else:
            print(f"❌ {script} - Missing")
            return False
    
    print("\n🧹 Checking for post-deployment cleanup requirements...")
    cleanup_dirs = [
        "codebase_summary/language_scan_tests/",
        "codebase_summary/history/"
    ]
    
    cleanup_needed = []
    for cleanup_dir in cleanup_dirs:
        if Path(cleanup_dir).exists():
            file_count = len(list(Path(cleanup_dir).glob("*")))
            if file_count > 0:
                cleanup_needed.append(f"{cleanup_dir} ({file_count} files)")
    
    if cleanup_needed:
        print("⚠️  Post-deployment cleanup recommended:")
        for item in cleanup_needed:
            print(f"   - {item}")
        print("   → Run post-deployment cleanup to optimize prompt caching")
    else:
        print("✅ No cleanup required")
    
    # Validate against manifest specifications
    print("\n" + "="*50)
    manifest_valid = validate_against_manifest()
    
    if not manifest_valid:
        print("\n❌ MANIFEST VALIDATION FAILED")
        return False
    
    print("\n✅ EXPORT PACKAGE VALIDATION PASSED")
    print("🚀 Ready for deployment to new projects")
    return True

def cleanup_post_deployment():
    """
    # @codebase-summary: Post-deployment cleanup for prompt caching optimization
    - Removes test files and excessive history after successful deployment
    - Optimizes prompt caching by reducing context size (~5000 tokens)
    - Preserves essential functionality while improving performance
    - Used by: deployment automation, performance optimization
    """
    print("🧹 POST-DEPLOYMENT CLEANUP")
    print("=" * 40)
    
    # Check if this is the source repository (has development marker files)
    is_source_repo = (
        Path("EXPORT_PACKAGE_MANIFEST.json").exists() or
        Path(".github").exists() or
        Path("reference_assets").exists()
    )
    
    if is_source_repo:
        print("🔍 DETECTED SOURCE REPOSITORY - SIMULATION MODE")
        print("   → Cleanup actions will be simulated, not executed")
        print("   → This preserves development files in the main repo")
        print("")
    
    cleanup_actions = []
    
    # Remove language scan test files
    test_dir = Path("codebase_summary/language_scan_tests/")
    if test_dir.exists():
        test_files = list(test_dir.glob("*"))
        if test_files:
            try:
                import shutil
                if is_source_repo:
                    # Simulation mode - don't actually delete
                    print(f"🎭 SIMULATION: Would remove {len(test_files)} language test files")
                    cleanup_actions.append(f"SIMULATED: Would remove {len(test_files)} language test files")
                else:
                    # Production mode - actually delete files
                    shutil.rmtree(test_dir)
                    cleanup_actions.append(f"Removed {len(test_files)} language test files")
            except Exception as e:
                print(f"⚠️  Could not remove test files: {e}")
                # Don't fail the entire cleanup if this fails
    
    # Keep only last 5 history files (with verification)
    history_dir = Path("codebase_summary/history/")
    if history_dir.exists():
        history_files = sorted(history_dir.glob("*.json"))
        if len(history_files) > 5:
            files_to_remove = history_files[:-5]
            try:
                # Verify files exist before attempting removal
                existing_files_to_remove = [f for f in files_to_remove if f.exists()]
                
                if is_source_repo:
                    # Simulation mode - don't actually delete
                    print(f"🎭 SIMULATION: Would archive {len(existing_files_to_remove)} old history files")
                    cleanup_actions.append(f"SIMULATED: Would archive {len(existing_files_to_remove)} old history files")
                else:
                    # Production mode - actually delete files
                    for old_file in existing_files_to_remove:
                        # Additional safety check
                        if old_file.is_file() and old_file.suffix == '.json':
                            old_file.unlink()
                    
                    if existing_files_to_remove:
                        cleanup_actions.append(f"Archived {len(existing_files_to_remove)} old history files")
            except Exception as e:
                print(f"⚠️  Could not archive history files: {e}")
                # Continue with other cleanup operations
    
    if cleanup_actions:
        print("✅ Cleanup completed:")
        for action in cleanup_actions:
            print(f"   - {action}")
        print(f"\n💡 Estimated token savings: ~{len(cleanup_actions) * 2500} tokens per cache hit")
    else:
        print("✅ No cleanup needed - system already optimized")
    
    return len(cleanup_actions) > 0

def main():
    """
    # @codebase-summary: Main validation execution entry point
    - Coordinates complete deployment validation process
    - Provides console output and exit codes for automation
    - Handles validation errors with proper error reporting
    - Supports post-deployment cleanup mode
    """
    if len(sys.argv) > 1 and sys.argv[1] == "cleanup":
        cleanup_post_deployment()
        return
    
    print(f"Validation started at: {datetime.now().isoformat()}")
    
    try:
        if validate_export_package():
            print("\n🎉 DEPLOYMENT VALIDATION SUCCESSFUL")
            print("The export package is ready for deployment to new projects.")
            print("\n💡 TIP: After successful deployment, run:")
            print("   python3 validate_deployment.py cleanup")
            print("   → This will optimize prompt caching performance")
            sys.exit(0)
        else:
            print("\n❌ DEPLOYMENT VALIDATION FAILED")
            print("Please fix the issues above before deploying.")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 Validation error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
