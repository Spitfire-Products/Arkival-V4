#!/usr/bin/env python3
"""
Export Readiness Validation Script - Arkival
Validates system is ready for GitHub deployment with current metrics
This script is EXCLUDED from git commits and generates deployment-ready manifests
"""

import json
import os
import sys
import datetime
from pathlib import Path
from typing import Dict, Any, List

def find_arkival_paths():
    """
    Universal path resolution for Arkival subdirectory deployment
    Returns: Dict with all required paths
    """
    current_dir = Path.cwd()
    project_root = None
    
    # Check if we're running from within the codebase_summary directory
    if current_dir.name == "codebase_summary" and current_dir.parent.name != "Arkival":
        # Running from source repo's codebase_summary directory
        project_root = current_dir.parent
        is_in_scripts_dir = True
    else:
        is_in_scripts_dir = False
        
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
    
    # Determine deployment mode
    if current_dir.name.lower() in ['arkival', 'arkival-v4'] or (
        not is_in_scripts_dir and (project_root / "arkival_config.json").exists()
    ):
        # Subdirectory deployment mode
        arkival_dir = current_dir if current_dir.name.lower() in ['arkival', 'arkival-v4'] else project_root
        return {
            'project_root': project_root,
            'arkival_dir': arkival_dir,
            'scripts_dir': arkival_dir / "codebase_summary",
            'export_dir': arkival_dir / "export_package",
            'codebase_summary': arkival_dir / "codebase_summary.json",
            'changelog_summary': arkival_dir / "changelog_summary.json",
            'missing_breadcrumbs': arkival_dir / "codebase_summary" / "missing_breadcrumbs.json",
            'manifest_file': arkival_dir / "EXPORT_PACKAGE_MANIFEST.json"
        }
    else:
        # Development mode
        if is_in_scripts_dir:
            scripts_dir = current_dir
        else:
            scripts_dir = project_root / "codebase_summary"
            
        return {
            'project_root': project_root,
            'arkival_dir': project_root,
            'scripts_dir': scripts_dir,
            'export_dir': project_root / "export_package",
            'codebase_summary': project_root / "codebase_summary.json",
            'changelog_summary': project_root / "changelog_summary.json",
            'missing_breadcrumbs': scripts_dir / "missing_breadcrumbs.json",
            'manifest_file': project_root / "EXPORT_PACKAGE_MANIFEST.json"
        }

class ExportReadinessValidator:
    """
    # @codebase-summary: Export readiness validation system
    - Validates system is ready for GitHub deployment
    - Generates updated export manifest with current metrics
    - Ensures all required files exist and are properly configured
    - Creates deployment-ready package validation
    """
    
    def __init__(self):
        self.paths = find_arkival_paths()
        self.validation_results = {
            "timestamp": datetime.datetime.now().isoformat() + "Z",
            "status": "UNKNOWN",
            "errors": [],
            "warnings": [],
            "metrics": {}
        }
    
    def validate_complete_system(self) -> Dict[str, Any]:
        """
        # @codebase-summary: Complete system validation for export readiness
        - Validates all core files and configurations
        - Collects current project metrics
        - Generates updated export manifest
        - Returns comprehensive readiness report
        """
        print("🚀 EXPORT READINESS VALIDATION")
        print("=" * 50)
        
        # Step 1: Validate core system files
        self._validate_core_files()
        
        # Step 2: Collect current metrics
        self._collect_current_metrics()
        
        # Step 3: Validate configuration files
        self._validate_configurations()
        
        # Step 4: Check documentation status
        self._validate_documentation()
        
        # Step 5: Generate updated export manifest
        self._generate_export_manifest()
        
        # Step 6: Final readiness assessment
        self._assess_export_readiness()
        
        return self.validation_results
    
    def _validate_core_files(self):
        """Validate all core system files exist"""
        print("📁 Validating core system files...")
        
        required_files = [
            "setup_workflow_system.py",
            "validate_deployment.py", 
            "workflow_config.json",
            "codebase_summary/agent_workflow_orchestrator.py",
            "codebase_summary/update_project_summary.py",
            "codebase_summary/update_changelog.py",
            "README.md",
            "SETUP_GUIDE.md",
            "AGENT_GUIDE.md",
            "DEVELOPER_ONBOARDING.md",
            ".scanignore"
        ]
        
        missing_files = []
        for file_path in required_files:
            full_path = self.paths['arkival_dir'] / file_path
            if full_path.exists():
                print(f"  ✅ {file_path}")
            else:
                print(f"  ❌ {file_path} - MISSING")
                missing_files.append(file_path)
        
        if missing_files:
            self.validation_results["errors"].extend([f"Missing file: {f}" for f in missing_files])
    
    def _collect_current_metrics(self):
        """Collect current project metrics from live data"""
        print("📊 Collecting current project metrics...")
        
        try:
            # Get codebase summary metrics
            with open(self.paths['codebase_summary'], 'r') as f:
                codebase_data = json.load(f)
            
            # Get documentation metrics
            with open(self.paths['missing_breadcrumbs'], 'r') as f:
                breadcrumb_data = json.load(f)
            
            # Get changelog metrics
            with open(self.paths['changelog_summary'], 'r') as f:
                changelog_data = json.load(f)
            
            # Compile current metrics
            self.validation_results["metrics"] = {
                "project_version": codebase_data.get("version", "1.0.0"),
                "changelog_version": changelog_data.get("changelog_version", "1.0.0"),
                "total_files": codebase_data.get("project_structure", {}).get("total_files", 0),
                "total_functions": breadcrumb_data.get("summary", {}).get("total_functions", 0),
                "documented_functions": breadcrumb_data.get("summary", {}).get("documented_functions", 0),
                "missing_breadcrumbs": breadcrumb_data.get("summary", {}).get("missing_count", 0),
                "documentation_coverage": breadcrumb_data.get("summary", {}).get("coverage_percentage", 0),
                "changelog_entries": changelog_data.get("statistics", {}).get("total_entries", 0),
                "last_updated": codebase_data.get("updated_at", ""),
                "ai_providers": len(codebase_data.get("ai_providers", [])),
                "architecture_patterns": len(codebase_data.get("architecture_patterns", []))
            }
            
            print(f"  ✅ Version: {self.validation_results['metrics']['project_version']}")
            print(f"  ✅ Functions: {self.validation_results['metrics']['total_functions']}")
            print(f"  ✅ Documentation: {self.validation_results['metrics']['documentation_coverage']:.1f}%")
            
        except Exception as e:
            self.validation_results["errors"].append(f"Failed to collect metrics: {e}")
            print(f"  ❌ Failed to collect metrics: {e}")
    
    def _validate_configurations(self):
        """Validate all JSON configuration files"""
        print("⚙️  Validating configuration files...")
        
        config_files = [
            ("workflow_config.json", self.paths['arkival_dir'] / "workflow_config.json"),
            ("codebase_summary.json", self.paths['codebase_summary']),
            ("changelog_summary.json", self.paths['changelog_summary']),
            ("missing_breadcrumbs.json", self.paths['missing_breadcrumbs'])
        ]
        
        for name, path in config_files:
            try:
                if path.exists():
                    with open(path, 'r') as f:
                        json.load(f)  # Validate JSON syntax
                    print(f"  ✅ {name} - Valid JSON")
                else:
                    print(f"  ⚠️  {name} - Missing")
                    self.validation_results["warnings"].append(f"Missing config: {name}")
            except json.JSONDecodeError as e:
                print(f"  ❌ {name} - Invalid JSON: {e}")
                self.validation_results["errors"].append(f"Invalid JSON in {name}: {e}")
    
    def _validate_documentation(self):
        """Validate documentation completeness"""
        print("📚 Validating documentation...")
        
        doc_files = [
            "README.md",
            "SETUP_GUIDE.md", 
            "AGENT_GUIDE.md",
            "DEVELOPER_ONBOARDING.md",
            "CODEBASE_SUMMARY.md",
            "ARCHITECTURE_DIAGRAM.md",
            "SCAN_IGNORE_DOCS.md"
        ]
        
        missing_docs = []
        for doc in doc_files:
            doc_path = self.paths['arkival_dir'] / doc
            if doc_path.exists():
                print(f"  ✅ {doc}")
            else:
                print(f"  ❌ {doc} - Missing")
                missing_docs.append(doc)
        
        if missing_docs:
            self.validation_results["errors"].extend([f"Missing documentation: {d}" for d in missing_docs])
    
    def _generate_export_manifest(self):
        """Generate updated export manifest with current metrics"""
        print("📦 Generating updated export manifest...")
        
        try:
            # Load existing manifest as template
            if self.paths['manifest_file'].exists():
                with open(self.paths['manifest_file'], 'r') as f:
                    manifest = json.load(f)
            else:
                manifest = {"package_name": "Arkival Export Package"}
            
            # Update with current metrics
            current_metrics = self.validation_results["metrics"]
            
            manifest.update({
                "package_name": "Arkival V4 - Cross-Platform Workflow Export Package",
                "version": current_metrics.get("project_version", "1.0.0"),
                "export_date": datetime.datetime.now().isoformat() + "Z",
                "status": "VALIDATING",
                "confidence_level": "HIGH" if len(self.validation_results["errors"]) == 0 else "MEDIUM",
                "validation_timestamp": self.validation_results["timestamp"]
            })
            
            # Update quality metrics with current data
            manifest["quality_metrics"] = {
                "total_files": current_metrics.get("total_files", 0),
                "function_count": current_metrics.get("total_functions", 0),
                "documented_functions": current_metrics.get("documented_functions", 0),
                "missing_breadcrumbs": current_metrics.get("missing_breadcrumbs", 0),
                "documentation_coverage": current_metrics.get("documentation_coverage", 0),
                "changelog_entries": current_metrics.get("changelog_entries", 0),
                "ai_providers": current_metrics.get("ai_providers", 0),
                "architecture_patterns": current_metrics.get("architecture_patterns", 0),
                "version_correlation_active": True,
                "cross_platform_support": True,
                "environment_detection": True
            }
            
            # Write updated manifest (this file should be gitignored)
            manifest_output_path = self.paths['arkival_dir'] / "EXPORT_READINESS_MANIFEST.json"
            with open(manifest_output_path, 'w') as f:
                json.dump(manifest, f, indent=2)
            
            print(f"  ✅ Updated manifest written to: {manifest_output_path}")
            
        except Exception as e:
            self.validation_results["errors"].append(f"Failed to generate manifest: {e}")
            print(f"  ❌ Failed to generate manifest: {e}")
    
    def _assess_export_readiness(self):
        """Final assessment of export readiness"""
        print("🎯 Assessing export readiness...")
        
        error_count = len(self.validation_results["errors"])
        warning_count = len(self.validation_results["warnings"])
        
        if error_count == 0:
            if warning_count == 0:
                self.validation_results["status"] = "READY_FOR_EXPORT"
                print("  ✅ SYSTEM READY FOR GITHUB DEPLOYMENT")
            else:
                self.validation_results["status"] = "READY_WITH_WARNINGS"
                print(f"  ⚠️  READY FOR EXPORT ({warning_count} warnings)")
        else:
            self.validation_results["status"] = "NOT_READY"
            print(f"  ❌ NOT READY FOR EXPORT ({error_count} errors)")
        
        print(f"\n📊 VALIDATION SUMMARY:")
        print(f"   Status: {self.validation_results['status']}")
        print(f"   Errors: {error_count}")
        print(f"   Warnings: {warning_count}")
        print(f"   Functions: {self.validation_results['metrics'].get('total_functions', 0)}")
        print(f"   Documentation: {self.validation_results['metrics'].get('documentation_coverage', 0):.1f}%")

def main():
    """Main validation execution"""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Export Readiness Validation Script")
        print("Usage: python3 validate_export_readiness.py")
        print("\nValidates system is ready for GitHub deployment with current metrics")
        print("Generates EXPORT_READINESS_MANIFEST.json (excluded from git)")
        return
    
    validator = ExportReadinessValidator()
    results = validator.validate_complete_system()
    
    # Save detailed results (this file should be gitignored)
    results_path = validator.paths['arkival_dir'] / "EXPORT_VALIDATION_RESULTS.json"
    try:
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n📋 Detailed results saved to: {results_path}")
    except Exception as e:
        print(f"\n⚠️  Could not save results: {e}")
    
    # Exit with appropriate code
    if results["status"] == "NOT_READY":
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()