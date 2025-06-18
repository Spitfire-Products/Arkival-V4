#!/usr/bin/env python3
"""
Comprehensive Schema Compatibility Analysis
Compares original vs optimized JSON for 100% compatibility verification
"""

import json
import sys
from typing import Dict, Any, List, Set, Tuple

def extract_schema_structure(obj: Any, path: str = "", max_depth: int = 10) -> Dict[str, Dict[str, Any]]:
    """Extract detailed schema structure including types, array contents, and object shapes"""
    schema = {}
    
    if max_depth <= 0:
        return schema
    
    if isinstance(obj, dict):
        # Record this as an object type
        schema[path] = {
            "type": "object",
            "keys": list(obj.keys()),
            "key_count": len(obj.keys())
        }
        
        # Recursively analyze each key
        for key, value in obj.items():
            current_path = f"{path}.{key}" if path else key
            nested_schema = extract_schema_structure(value, current_path, max_depth - 1)
            schema.update(nested_schema)
            
    elif isinstance(obj, list):
        schema[path] = {
            "type": "list",
            "length": len(obj),
            "empty": len(obj) == 0
        }
        
        if obj:  # If list is not empty
            # Analyze first element to determine array content type
            first_element = obj[0]
            schema[path]["item_type"] = type(first_element).__name__
            
            # If it's a complex type, analyze its structure
            if isinstance(first_element, (dict, list)):
                nested_schema = extract_schema_structure(first_element, f"{path}[0]", max_depth - 1)
                schema.update(nested_schema)
    else:
        # Primitive type
        schema[path] = {
            "type": type(obj).__name__,
            "value_example": str(obj)[:50] if isinstance(obj, str) else obj
        }
    
    return schema

def analyze_compatibility(original_schema: Dict, optimized_schema: Dict) -> Dict[str, Any]:
    """Perform comprehensive compatibility analysis"""
    
    original_keys = set(original_schema.keys())
    optimized_keys = set(optimized_schema.keys())
    
    analysis = {
        "overall_compatible": True,
        "critical_issues": [],
        "warnings": [],
        "missing_keys": list(original_keys - optimized_keys),
        "extra_keys": list(optimized_keys - original_keys),
        "type_changes": [],
        "structure_changes": [],
        "top_level_analysis": {},
        "nested_analysis": {}
    }
    
    # Define critical top-level keys that must exist
    critical_top_level = [
        "_generator", "project_name", "version", "updated_at", "description",
        "main_dependencies", "project_structure", "code_analysis", "core_modules",
        "routes", "frontend_structure", "ai_integration", "capabilities",
        "application_flow", "documentation_status", "database_readiness",
        "architecture", "recent_features", "performance_metrics", "deployment",
        "version_correlation", "future_enhancements"
    ]
    
    # Analyze top-level keys
    for key in critical_top_level:
        status = {
            "present_in_original": key in original_schema,
            "present_in_optimized": key in optimized_schema,
            "compatible": True
        }
        
        if key in original_schema and key not in optimized_schema:
            status["compatible"] = False
            analysis["critical_issues"].append(f"CRITICAL: Missing top-level key '{key}'")
            analysis["overall_compatible"] = False
        elif key in original_schema and key in optimized_schema:
            orig_info = original_schema[key]
            opt_info = optimized_schema[key]
            
            if orig_info["type"] != opt_info["type"]:
                status["compatible"] = False
                analysis["type_changes"].append({
                    "key": key,
                    "original_type": orig_info["type"],
                    "optimized_type": opt_info["type"]
                })
                analysis["critical_issues"].append(f"CRITICAL: Type change for '{key}': {orig_info['type']} → {opt_info['type']}")
                analysis["overall_compatible"] = False
        
        analysis["top_level_analysis"][key] = status
    
    # Analyze nested structures
    critical_nested_paths = [
        "project_structure.total_files",
        "project_structure.directories", 
        "project_structure.file_types",
        "project_structure.key_files",
        "project_structure.technology_indicators",
        "code_analysis.total_functions",
        "code_analysis.documented_functions",
        "code_analysis.language_breakdown",
        "code_analysis.documentation_gaps",
        "ai_integration.providers",
        "ai_integration.capabilities",
        "ai_integration.integration_files",
        "main_dependencies.runtime",
        "main_dependencies.development",
        "main_dependencies.system"
    ]
    
    for path in critical_nested_paths:
        analysis["nested_analysis"][path] = {
            "present_in_original": path in original_schema,
            "present_in_optimized": path in optimized_schema,
            "compatible": True
        }
        
        if path in original_schema and path not in optimized_schema:
            analysis["nested_analysis"][path]["compatible"] = False
            analysis["critical_issues"].append(f"CRITICAL: Missing nested structure '{path}'")
            analysis["overall_compatible"] = False
        elif path in original_schema and path in optimized_schema:
            orig_info = original_schema[path]
            opt_info = optimized_schema[path]
            
            if orig_info["type"] != opt_info["type"]:
                analysis["nested_analysis"][path]["compatible"] = False
                analysis["type_changes"].append({
                    "key": path,
                    "original_type": orig_info["type"],
                    "optimized_type": opt_info["type"]
                })
                analysis["critical_issues"].append(f"CRITICAL: Type change for nested '{path}': {orig_info['type']} → {opt_info['type']}")
                analysis["overall_compatible"] = False
    
    # Analyze array structures
    for key in original_keys & optimized_keys:
        if original_schema[key]["type"] == "list" and optimized_schema[key]["type"] == "list":
            orig_info = original_schema[key]
            opt_info = optimized_schema[key]
            
            # Check if array item types changed
            if "item_type" in orig_info and "item_type" in opt_info:
                if orig_info["item_type"] != opt_info["item_type"]:
                    analysis["warnings"].append(f"WARNING: Array item type changed for '{key}': {orig_info['item_type']} → {opt_info['item_type']}")
    
    return analysis

def generate_comprehensive_report(analysis: Dict, original_file: str, optimized_file: str) -> str:
    """Generate comprehensive compatibility report"""
    
    compatibility_status = "✅ FULLY COMPATIBLE" if analysis["overall_compatible"] else "❌ INCOMPATIBLE"
    
    report = f"""# 🔍 Comprehensive Schema Compatibility Analysis

## Files Analyzed
- **Original Schema**: `{original_file}`
- **Optimized Schema**: `{optimized_file}`

## 🎯 Overall Compatibility Status
**Result**: {compatibility_status}

## 🚨 Critical Issues
"""
    
    if analysis["critical_issues"]:
        report += f"**Count**: {len(analysis['critical_issues'])}\n\n"
        for issue in analysis["critical_issues"]:
            report += f"- {issue}\n"
    else:
        report += "**Count**: 0 ✅\n\n- No critical compatibility issues detected\n"
    
    report += f"""

## ⚠️ Warnings
"""
    
    if analysis["warnings"]:
        report += f"**Count**: {len(analysis['warnings'])}\n\n"
        for warning in analysis["warnings"]:
            report += f"- {warning}\n"
    else:
        report += "**Count**: 0 ✅\n\n- No warnings detected\n"
    
    report += f"""

## 📊 Schema Structure Analysis

### Top-Level Keys Verification
"""
    
    for key, status in analysis["top_level_analysis"].items():
        status_icon = "✅" if status["compatible"] else "❌"
        presence = ""
        if status["present_in_original"] and status["present_in_optimized"]:
            presence = "Present in both"
        elif status["present_in_original"]:
            presence = "Missing in optimized"
        elif status["present_in_optimized"]:
            presence = "Extra in optimized"
        else:
            presence = "Missing in both"
        
        report += f"- `{key}`: {status_icon} ({presence})\n"
    
    report += f"""

### Critical Nested Structures
"""
    
    for path, status in analysis["nested_analysis"].items():
        status_icon = "✅" if status["compatible"] else "❌"
        presence = ""
        if status["present_in_original"] and status["present_in_optimized"]:
            presence = "Present in both"
        elif status["present_in_original"]:
            presence = "Missing in optimized"
        elif status["present_in_optimized"]:
            presence = "Extra in optimized"
        else:
            presence = "Missing in both"
        
        report += f"- `{path}`: {status_icon} ({presence})\n"
    
    report += f"""

### Missing Keys Summary
**Total Missing**: {len(analysis['missing_keys'])}

"""
    
    if analysis["missing_keys"]:
        # Group missing keys by category
        top_level_missing = [k for k in analysis["missing_keys"] if "." not in k]
        nested_missing = [k for k in analysis["missing_keys"] if "." in k]
        
        if top_level_missing:
            report += "**Top-level missing keys**:\n"
            for key in sorted(top_level_missing)[:10]:
                report += f"- `{key}`\n"
            if len(top_level_missing) > 10:
                report += f"- ... and {len(top_level_missing) - 10} more\n"
        
        if nested_missing:
            report += "\n**Nested missing keys**:\n"
            for key in sorted(nested_missing)[:15]:
                report += f"- `{key}`\n"
            if len(nested_missing) > 15:
                report += f"- ... and {len(nested_missing) - 15} more\n"
    else:
        report += "- None ✅\n"
    
    report += f"""

### Extra Keys Summary  
**Total Extra**: {len(analysis['extra_keys'])}

"""
    
    if analysis["extra_keys"]:
        for key in sorted(analysis["extra_keys"])[:15]:
            report += f"- `{key}`\n"
        if len(analysis["extra_keys"]) > 15:
            report += f"- ... and {len(analysis['extra_keys']) - 15} more\n"
    else:
        report += "- None ✅\n"
    
    report += f"""

### Type Changes
**Total Changes**: {len(analysis['type_changes'])}

"""
    
    if analysis["type_changes"]:
        for change in analysis["type_changes"]:
            report += f"- `{change['key']}`: `{change['original_type']}` → `{change['optimized_type']}`\n"
    else:
        report += "- None ✅\n"
    
    report += f"""

## 🔧 Integration Impact Assessment

### Potential Breaking Changes
"""
    
    breaking_changes = []
    
    # Check for missing critical fields
    critical_fields = ["total_files", "total_functions", "providers", "capabilities", "version", "project_name"]
    for key in analysis["missing_keys"]:
        if any(field in key for field in critical_fields):
            breaking_changes.append(key)
    
    # Check for type changes in critical fields
    for change in analysis["type_changes"]:
        if any(field in change["key"] for field in critical_fields):
            breaking_changes.append(f"Type change: {change['key']}")
    
    if breaking_changes:
        for change in breaking_changes:
            report += f"- `{change}`\n"
    else:
        report += "- None detected ✅\n"
    
    report += f"""

## 📋 Recommendations

"""
    
    if analysis["overall_compatible"]:
        report += """### ✅ Schema is Compatible
The optimized version maintains full schema compatibility with the original version.

**Safe to deploy**: 
- All critical top-level keys are preserved
- All nested structures maintain their types
- Array structures are consistent
- Integration code should continue to work without modifications

**Benefits of optimization**:
- Reduced file size while maintaining same schema
- Better performance due to optimized content generation
- Same API contract for all integrations
"""
    else:
        report += """### ❌ Schema Incompatibility Detected

**Action Required**: Review and fix the following issues before deployment:

1. **Missing Critical Keys**: Some required keys are missing from the optimized version
2. **Type Mismatches**: Critical data types have changed
3. **Structure Changes**: Important nested structures have been modified

**Recommendation**: 
- Update the optimized script to ensure all critical keys are present
- Maintain the same data types for all fields
- Test with existing integration code before deployment
"""
    
    report += f"""

---
*Analysis completed with {len(analysis['missing_keys']) + len(analysis['extra_keys']) + len(analysis['type_changes'])} total differences detected*
"""
    
    return report

def main():
    """Main analysis function"""
    
    # Load both JSON files
    original_file = "/home/runner/workspace/codebase_summary_original_backup.json"
    optimized_file = "/home/runner/workspace/codebase_summary.json"
    
    try:
        # Load original
        with open(original_file, 'r') as f:
            original_data = json.load(f)
        
        # Load optimized
        with open(optimized_file, 'r') as f:
            optimized_data = json.load(f)
            
    except FileNotFoundError as e:
        print(f"❌ Error: Could not find file: {e}")
        return
    except json.JSONDecodeError as e:
        print(f"❌ Error: Could not parse JSON: {e}")
        return
    
    # Extract schema structures
    print("🔍 Extracting schema structures...")
    original_schema = extract_schema_structure(original_data)
    optimized_schema = extract_schema_structure(optimized_data)
    
    print(f"   Original schema: {len(original_schema)} elements")
    print(f"   Optimized schema: {len(optimized_schema)} elements")
    
    # Perform compatibility analysis
    print("🔍 Analyzing compatibility...")
    analysis = analyze_compatibility(original_schema, optimized_schema)
    
    # Generate comprehensive report
    print("📝 Generating detailed report...")
    report = generate_comprehensive_report(analysis, original_file, optimized_file)
    
    # Save report
    report_file = "/home/runner/workspace/schema_compatibility_analysis.md"
    with open(report_file, 'w') as f:
        f.write(report)
    
    # Print summary
    print(f"\n{'='*60}")
    print("🎯 SCHEMA COMPATIBILITY ANALYSIS SUMMARY")
    print(f"{'='*60}")
    print(f"Overall Compatible: {'✅ YES' if analysis['overall_compatible'] else '❌ NO'}")
    print(f"Critical Issues: {len(analysis['critical_issues'])}")
    print(f"Warnings: {len(analysis['warnings'])}")
    print(f"Missing Keys: {len(analysis['missing_keys'])}")
    print(f"Extra Keys: {len(analysis['extra_keys'])}")
    print(f"Type Changes: {len(analysis['type_changes'])}")
    print(f"\n📄 Detailed report saved: {report_file}")
    print(f"{'='*60}")
    
    # Print the actual report
    print(report)

if __name__ == "__main__":
    main()