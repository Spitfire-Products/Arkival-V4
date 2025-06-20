#!/usr/bin/env python3
"""
Optimized Project Summary Generator - Streamlined for AI agent deployment
Reduced from 124KB to ~30KB while maintaining same JSON output quality
"""

import os
import sys
import json
import re
import datetime
import logging
import shutil
import fnmatch
from collections import defaultdict
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
    # Three scenarios:
    # 1. Running from source repo (dev mode)
    # 2. Running from subdirectory deployment (Arkival/)
    # 3. Running from within codebase_summary directory in source repo
    
    if current_dir.name.lower() in ['arkival', 'arkival-v4'] or (
        not is_in_scripts_dir and (project_root / "arkival_config.json").exists()
    ):
        # Subdirectory deployment mode - use SAME structure as development mode
        arkival_dir = current_dir if current_dir.name.lower() in ['arkival', 'arkival-v4'] else project_root
        return {
            'project_root': project_root,
            'config_file': project_root / "arkival_config.json",
            'arkival_dir': arkival_dir,
            'data_dir': arkival_dir,
            'scripts_dir': arkival_dir / "codebase_summary",
            'export_dir': arkival_dir / "export_package",
            'checkpoints_dir': arkival_dir / "checkpoints",
            
            # Data files - SAME as development mode!
            'codebase_summary': arkival_dir / "codebase_summary.json",
            'changelog_summary': arkival_dir / "changelog_summary.json",
            'session_state': arkival_dir / "codebase_summary" / "session_state.json",
            'missing_breadcrumbs': arkival_dir / "codebase_summary" / "missing_breadcrumbs.json",
            'scan_ignore': project_root / ".scanignore"
        }
    else:
        # Development mode - use root directory structure
        # Special handling when running from codebase_summary directory
        if is_in_scripts_dir:
            scripts_dir = current_dir
        else:
            scripts_dir = project_root / "codebase_summary"
            
        return {
            'project_root': project_root,
            'config_file': project_root / "arkival_config.json",
            'arkival_dir': project_root,
            'data_dir': project_root,
            'scripts_dir': scripts_dir, 
            'export_dir': project_root / "export_package",
            'checkpoints_dir': project_root / "checkpoints",
            
            # Data files in root/standard locations
            'codebase_summary': project_root / "codebase_summary.json",
            'changelog_summary': project_root / "changelog_summary.json",
            'session_state': scripts_dir / "session_state.json",
            'missing_breadcrumbs': scripts_dir / "missing_breadcrumbs.json",
            'scan_ignore': project_root / ".scanignore"
        }

class OptimizedProjectSummaryGenerator:
    def __init__(self):
        self.paths = find_arkival_paths()
        self.project_root = self.paths['project_root']
        self.summary_path = self.paths['codebase_summary']
        self.history_dir = self.paths['scripts_dir'] / "history"
        self.ignore_patterns = self._load_ignore_patterns()
        
        # Comprehensive language patterns for all supported languages
        self.function_patterns = {
            'python': [
                r'def\s+([a-z_][a-z0-9_]*)\s*\(',
                r'async\s+def\s+([a-z_][a-z0-9_]*)\s*\(',
                r'class\s+([A-Z]\w*)\s*[:\(]'
            ],
            'javascript': [
                r'(?:export\s+)?(?:async\s+)?function\s+([A-Za-z_]\w*)',
                r'(?:export\s+)?const\s+([A-Za-z_]\w*)\s*=.*?(?:=>|\()',
                r'const\s+(use[A-Z]\w*)\s*=',
                r'class\s+([A-Z]\w*)'
            ],
            'typescript': [
                r'(?:export\s+)?(?:async\s+)?function\s+([A-Za-z_]\w*)',
                r'(?:export\s+)?const\s+([A-Za-z_]\w*)\s*=.*?(?:=>|\()',
                r'const\s+(use[A-Z]\w*)\s*=',
                r'class\s+([A-Z]\w*)'
            ],
            'rust': [
                r'fn\s+([a-z_][a-z0-9_]*)\s*[\(<]',
                r'pub\s+fn\s+([a-z_][a-z0-9_]*)\s*[\(<]',
                r'async\s+fn\s+([a-z_][a-z0-9_]*)\s*[\(<]',
                r'struct\s+([A-Z]\w*)',
                r'enum\s+([A-Z]\w*)',
                r'trait\s+([A-Z]\w*)'
            ],
            'c': [
                r'(?:static\s+)?(?:inline\s+)?(?:\w+\s+)*([a-z_][a-z0-9_]*)\s*\([^)]*\)\s*\{',
                r'(?:extern\s+)?(?:\w+\s+)*([a-z_][a-z0-9_]*)\s*\([^)]*\);'
            ],
            'cpp': [
                r'(?:virtual\s+)?(?:static\s+)?(?:inline\s+)?(?:\w+\s+)*([a-z_][a-z0-9_]*)\s*\([^)]*\)\s*\{',
                r'(?:\w+\s+)*([A-Z]\w*)\s*::\s*([a-z_][a-z0-9_]*)\s*\(',
                r'class\s+([A-Z]\w*)',
                r'template.*class\s+([A-Z]\w*)'
            ],
            'java': [
                r'(?:public\s+)?(?:private\s+)?(?:protected\s+)?(?:static\s+)?(?:\w+\s+)*([a-z][a-zA-Z0-9_]*)\s*\([^)]*\)\s*\{',
                r'(?:public\s+)?(?:private\s+)?(?:protected\s+)?class\s+([A-Z]\w*)',
                r'(?:public\s+)?(?:private\s+)?(?:protected\s+)?interface\s+([A-Z]\w*)'
            ],
            'go': [
                r'func\s+([a-z][a-zA-Z0-9_]*)\s*\(',
                r'func\s+\(\w+\s+\*?\w+\)\s+([a-z][a-zA-Z0-9_]*)\s*\(',
                r'type\s+([A-Z]\w*)\s+(?:struct|interface)'
            ],
            'swift': [
                r'(?:public\s+)?(?:private\s+)?(?:internal\s+)?func\s+([a-z][a-zA-Z0-9_]*)\s*\(',
                r'(?:public\s+)?(?:private\s+)?(?:internal\s+)?class\s+([A-Z]\w*)',
                r'(?:public\s+)?(?:private\s+)?(?:internal\s+)?struct\s+([A-Z]\w*)'
            ],
            'kotlin': [
                r'(?:suspend\s+)?(?:inline\s+)?fun\s+([a-z][a-zA-Z0-9_]*)\s*\(',
                r'(?:data\s+)?class\s+([A-Z]\w*)',
                r'(?:sealed\s+)?interface\s+([A-Z]\w*)'
            ],
            'php': [
                r'(?:public\s+)?(?:private\s+)?(?:protected\s+)?function\s+([a-z_][a-zA-Z0-9_]*)\s*\(',
                r'class\s+([A-Z]\w*)',
                r'trait\s+([A-Z]\w*)'
            ],
            'ruby': [
                r'def\s+([a-z_][a-zA-Z0-9_]*[?!]?)',
                r'class\s+([A-Z]\w*)',
                r'module\s+([A-Z]\w*)'
            ],
            'dart': [
                r'(?:static\s+)?(?:async\s+)?(?:\w+\s+)*([a-z][a-zA-Z0-9_]*)\s*\([^)]*\)\s*(?:async\s*)?\{',
                r'class\s+([A-Z]\w*)',
                r'mixin\s+([A-Z]\w*)'
            ],
            'sql': [
                r'(?:CREATE\s+)?(?:OR\s+REPLACE\s+)?(?:FUNCTION|PROCEDURE)\s+([a-z_][a-zA-Z0-9_]*)',
                r'CREATE\s+TRIGGER\s+([a-z_][a-zA-Z0-9_]*)'
            ],
            'css': [
                r'@function\s+([a-z-][a-z0-9-]*)',
                r'@mixin\s+([a-z-][a-z0-9-]*)',
                r'\.([a-z-][a-z0-9-]*)\s*\{'
            ],
            'vue': [
                r'(?:async\s+)?([a-z][a-zA-Z0-9_]*)\s*\([^)]*\)\s*\{',
                r'computed:\s*\{',
                r'methods:\s*\{'
            ],
            'lua': [
                r'function\s+([a-z_][a-zA-Z0-9_]*)\s*\(',
                r'local\s+function\s+([a-z_][a-zA-Z0-9_]*)\s*\(',
                r'([a-z_][a-zA-Z0-9_]*)\s*=\s*function\s*\('
            ],
            'scala': [
                r'def\s+([a-z_][a-zA-Z0-9_]*)\s*[\(\[]',
                r'class\s+([A-Z]\w*)',
                r'object\s+([A-Z]\w*)',
                r'trait\s+([A-Z]\w*)'
            ],
            'clojure': [
                r'\(defn\s+([a-z-][a-z0-9-]*)',
                r'\(defn-\s+([a-z-][a-z0-9-]*)',
                r'\(defmacro\s+([a-z-][a-z0-9-]*)'
            ],
            'r': [
                r'([a-z_][a-zA-Z0-9_\.]*)\s*<-\s*function\s*\(',
                r'([a-z_][a-zA-Z0-9_\.]*)\s*=\s*function\s*\(',
                r'function\s*\('
            ],
            'objc': [
                r'-\s*\([^)]+\)\s*([a-z_][a-zA-Z0-9_]*)',
                r'\+\s*\([^)]+\)\s*([a-z_][a-zA-Z0-9_]*)',
                r'@interface\s+([A-Z]\w*)',
                r'@implementation\s+([A-Z]\w*)'
            ],
            'csharp': [
                r'(?:public\s+|private\s+|protected\s+|internal\s+)?(?:static\s+)?(?:virtual\s+)?(?:override\s+)?(?:async\s+)?(?:abstract\s+)?(?:void|Task(?:<[^>]+>)?|string|int|bool|double|float|decimal|char|byte|short|long|object|var|I?[A-Z]\w*(?:<[^>]+>)?)\s+([A-Z][a-zA-Z0-9_]*)\s*\([^)]*\)',
                r'(?:public\s+|private\s+|protected\s+|internal\s+)?(?:static\s+)?(?:virtual\s+)?(?:override\s+)?(?:async\s+)?(?:abstract\s+)?(?:void|Task(?:<[^>]+>)?|string|int|bool|double|float|decimal|char|byte|short|long|object|var|I?[A-Z]\w*(?:<[^>]+>)?)\s+([a-z][a-zA-Z0-9_]*)\s*\([^)]*\)',
                r'^\s*(?:public\s+|private\s+|protected\s+|internal\s+)?([A-Z]\w*)\s*\([^)]*\)\s*(?::\s*(?:base|this)\s*\([^)]*\))?\s*\{',
                r'(?:public\s+|private\s+|protected\s+|internal\s+)?(?:abstract\s+|sealed\s+|static\s+)?(?:partial\s+)?class\s+([A-Z]\w*)',
                r'(?:public\s+|private\s+|protected\s+|internal\s+)?(?:partial\s+)?interface\s+([A-Z]\w*)'
            ],
            'shell': [
                r'function\s+([a-z_][a-zA-Z0-9_]*)\s*\(',
                r'([a-z_][a-zA-Z0-9_]*)\s*\(\s*\)\s*\{',
                r'^\s*([a-z_][a-zA-Z0-9_]*)\s*\(\)\s*\{'
            ],
            'powershell': [
                r'function\s+([A-Za-z][a-zA-Z0-9_-]*)',
                r'Filter\s+([A-Za-z][a-zA-Z0-9_-]*)',
                r'([A-Za-z][a-zA-Z0-9_-]*)\s*=\s*\{'
            ]
        }

    def _detect_project_info(self) -> Dict[str, str]:
        """Auto-detect project name and description from codebase"""
        project_info = {"name": "Unknown Project", "description": "Project description not found"}
        
        # Priority 1: package.json
        package_json = self.project_root / "package.json"
        if package_json.exists():
            try:
                with open(package_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if "name" in data:
                        project_info["name"] = data["name"]
                    if "description" in data:
                        project_info["description"] = data["description"]
                    return project_info
            except:
                pass
        
        # Priority 2: pyproject.toml
        pyproject_toml = self.project_root / "pyproject.toml"
        if pyproject_toml.exists():
            try:
                with open(pyproject_toml, 'r', encoding='utf-8') as f:
                    content = f.read()
                    name_match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', content)
                    if name_match:
                        project_info["name"] = name_match.group(1)
                    desc_match = re.search(r'description\s*=\s*["\']([^"\']+)["\']', content)
                    if desc_match:
                        project_info["description"] = desc_match.group(1)
                    return project_info
            except:
                pass
        
        # Priority 3: README.md
        readme_files = ["README.md", "readme.md", "ReadMe.md"]
        for readme_name in readme_files:
            readme_path = self.project_root / readme_name
            if readme_path.exists():
                try:
                    with open(readme_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        lines = [line.strip() for line in content.split('\n') if line.strip()]
                        if lines:
                            # Use first header as project name
                            first_line = lines[0]
                            if first_line.startswith('#'):
                                project_info["name"] = first_line.lstrip('#').strip()
                            else:
                                project_info["name"] = first_line.strip()
                            
                            # Use first substantial paragraph as description
                            for line in lines[1:]:
                                if (len(line) > 20 and not line.startswith('#') and 
                                    not line.startswith('[') and not line.startswith('!')):
                                    # Clean up markdown
                                    clean_desc = re.sub(r'\*\*([^*]+)\*\*', r'\1', line)
                                    clean_desc = re.sub(r'\*([^*]+)\*', r'\1', clean_desc)
                                    project_info["description"] = clean_desc.strip()
                                    break
                        return project_info
                except:
                    pass
        
        # Fallback
        project_info["name"] = self.project_root.name
        project_info["description"] = f"Code analysis for {self.project_root.name} project"
        return project_info

    def _analyze_code_file(self, file_path: str) -> Dict[str, Any]:
        """Streamlined code analysis for a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except:
            return {"file": file_path, "functions": [], "missing_breadcrumbs": [], "function_count": 0, "documented_count": 0}

        # Detect language
        ext = Path(file_path).suffix.lower()
        lang_map = {
            '.py': 'python', '.js': 'javascript', '.jsx': 'javascript', '.ts': 'typescript', 
            '.tsx': 'typescript', '.java': 'java', '.go': 'go', '.rs': 'rust', '.c': 'c', 
            '.cpp': 'cpp', '.cc': 'cpp', '.cxx': 'cpp', '.php': 'php', '.rb': 'ruby', 
            '.swift': 'swift', '.kt': 'kotlin', '.dart': 'dart', '.sql': 'sql', '.css': 'css',
            '.scss': 'css', '.sass': 'css', '.vue': 'vue', '.lua': 'lua', '.scala': 'scala',
            '.clj': 'clojure', '.cljs': 'clojure', '.r': 'r', '.m': 'objc', '.mm': 'objc',
            '.cs': 'csharp', '.sh': 'shell', '.bash': 'shell', '.zsh': 'shell', '.ps1': 'powershell'
        }
        
        patterns = self.function_patterns.get(lang_map.get(ext, 'javascript'), self.function_patterns['javascript'])
        
        functions = []
        documented_functions = []
        missing_breadcrumbs = []
        lines = content.split('\n')

        for i, line in enumerate(lines):
            for pattern in patterns:
                matches = re.findall(pattern, line)
                for match in matches:
                    if match and not match.startswith('_'):
                        functions.append(match)
                        
                        # Check for documentation breadcrumbs
                        breadcrumb_found = False
                        for j in range(max(0, i-5), min(len(lines), i+3)):
                            if '@codebase-summary:' in lines[j]:
                                breadcrumb_found = True
                                documented_functions.append(match)
                                break
                        
                        if not breadcrumb_found:
                            missing_breadcrumbs.append(match)

        return {
            "file": str(Path(file_path).relative_to(self.project_root)),
            "language": ext,
            "function_count": len(functions),
            "documented_count": len(documented_functions),
            "functions": [],  # Empty for optimization
            "missing_breadcrumbs": missing_breadcrumbs,
            "lines_of_code": len(lines)
        }

    def _scan_project_structure(self) -> Dict[str, Any]:
        """Optimized project structure analysis"""
        structure = {
            "total_files": 0,
            "directories": [],
            "file_types": defaultdict(int),
            "key_files": [],
            "technology_indicators": {
                "frontend": [],
                "backend": [],
                "ai_integration": [],
                "database": [],
                "deployment": [],
                "documentation": []
            }
        }

        # Key file patterns
        key_patterns = ["LICENSE", "README*", ".gitignore", "package.json", "pyproject.toml", "Cargo.toml"]
        
        for root, dirs, files in os.walk(self.project_root):
            root_path = Path(root)
            
            # Skip ignored directories
            if self._should_ignore_path(root_path):
                continue
                
            # Remove ignored directories from dirs list to prevent os.walk from entering them
            dirs[:] = [d for d in dirs if not self._should_ignore_path(root_path / d)]
                
            rel_root = str(Path(root).relative_to(self.project_root))
            if rel_root != '.':
                structure["directories"].append(rel_root)

            for file in files:
                file_path = Path(root) / file
                
                # Skip ignored files
                if self._should_ignore_path(file_path):
                    continue
                    
                structure["total_files"] += 1
                ext = Path(file).suffix
                structure["file_types"][ext] += 1
                
                rel_path = str(file_path.relative_to(self.project_root))
                
                # Categorize files
                if any(pattern.replace('*', '') in file for pattern in key_patterns):
                    structure["key_files"].append(rel_path)
                
                if ext in ['.py', '.java', '.go', '.rs']:
                    structure["technology_indicators"]["backend"].append(rel_path)
                elif ext in ['.js', '.jsx', '.ts', '.tsx', '.vue']:
                    structure["technology_indicators"]["frontend"].append(rel_path)
                elif 'claude' in file.lower() or 'ai' in file.lower():
                    structure["technology_indicators"]["ai_integration"].append(rel_path)
                elif ext in ['.sql', '.db']:
                    structure["technology_indicators"]["database"].append(rel_path)
                elif file.lower() in ['dockerfile', '.replit', 'docker-compose.yml']:
                    structure["technology_indicators"]["deployment"].append(rel_path)
                elif ext in ['.md', '.txt'] or 'doc' in file.lower():
                    structure["technology_indicators"]["documentation"].append(rel_path)

        # Limit arrays for optimization
        for category in structure["technology_indicators"]:
            structure["technology_indicators"][category] = structure["technology_indicators"][category][:20]
        
        structure["file_types"] = dict(structure["file_types"])
        return structure

    def _generate_optimized_summary(self, version: str) -> Dict[str, Any]:
        """Generate optimized project summary"""
        project_info = self._detect_project_info()
        structure = self._scan_project_structure()
        
        # Analyze code files - comprehensive language support
        code_extensions = {
            '.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.go', '.rs', '.c', '.cpp', '.cc', '.cxx',
            '.php', '.rb', '.swift', '.kt', '.dart', '.sql', '.css', '.scss', '.sass', '.vue', 
            '.lua', '.scala', '.clj', '.cljs', '.r', '.m', '.mm', '.cs', '.sh', '.bash', '.zsh', '.ps1'
        }
        file_analysis = []
        total_functions = 0
        documented_functions = 0
        missing_breadcrumbs = []
        language_breakdown = defaultdict(lambda: {"files": 0, "functions": 0})
        
        for root, dirs, files in os.walk(self.project_root):
            root_path = Path(root)
            
            # Skip ignored directories
            if self._should_ignore_path(root_path):
                continue
                
            # Remove ignored directories from dirs list to prevent os.walk from entering them
            dirs[:] = [d for d in dirs if not self._should_ignore_path(root_path / d)]
                
            for file in files:
                if Path(file).suffix in code_extensions:
                    file_path = Path(root) / file
                    analysis = self._analyze_code_file(str(file_path))
                    
                    if analysis["function_count"] > 0:
                        file_analysis.append(analysis)
                        total_functions += analysis["function_count"]
                        documented_functions += analysis["documented_count"]
                        
                        # Track missing breadcrumbs
                        if analysis["missing_breadcrumbs"]:
                            missing_breadcrumbs.append({
                                "file": analysis["file"],
                                "missing": analysis["missing_breadcrumbs"]
                            })
                        
                        # Language breakdown
                        lang = analysis["language"]
                        language_breakdown[lang]["files"] += 1
                        language_breakdown[lang]["functions"] += analysis["function_count"]

        # Calculate documentation gaps (top 10)
        doc_gaps = []
        for item in missing_breadcrumbs:
            if len(item["missing"]) > 0:
                doc_gaps.append({
                    "file": item["file"],
                    "undocumented": len(item["missing"])
                })
        doc_gaps.sort(key=lambda x: x["undocumented"], reverse=True)
        doc_gaps = doc_gaps[:10]

        # Optimized output - always minimal mode
        code_analysis = {
            "total_functions": total_functions,
            "documented_functions": documented_functions,
            "language_breakdown": dict(language_breakdown),
            "documentation_gaps": doc_gaps,
            "total_files_analyzed": len(file_analysis),
            "total_lines_of_code": sum(f["lines_of_code"] for f in file_analysis),
            "coverage_percentage": round((documented_functions / max(1, total_functions)) * 100, 2),
            "missing_count": total_functions - documented_functions,
            "missing_breadcrumbs_summary": {
                "total_missing": total_functions - documented_functions,
                "by_directory": self._summarize_missing_by_dir(missing_breadcrumbs)
            }
        }

        # AI integration detection
        ai_files = structure["technology_indicators"]["ai_integration"]
        ai_integration = {
            "providers": ["Claude"] if any("claude" in f.lower() for f in ai_files) else [],
            "capabilities": ["Text Generation"] if ai_files else [],
            "integration_files": [str(self.project_root / f) for f in ai_files[:5]]
        }

        # Architecture analysis
        architecture_analysis = self._analyze_codebase_architecture(structure, code_analysis)

        return {
            "_generator": "Generated by codebase_summary/update_project_summary.py - Core project documentation and analysis system",
            "project_name": project_info["name"],
            "version": version,
            "updated_at": datetime.datetime.now().isoformat() + "Z",
            "description": project_info["description"],
            "main_dependencies": {"runtime": [], "development": [], "system": []},
            "project_structure": structure,
            "code_analysis": code_analysis,
            "core_modules": [],
            "routes": {"total_routes": 0, "by_method": {}, "by_category": {}, "routes": []},
            "frontend_structure": {
                "components": [],
                "hooks": [],
                "total_components": 0,
                "total_hooks": 0,
                "components_config": {"config_exists": False, "paths_valid": {}, "missing_directories": [], "ui_components_count": 0, "alignment_status": "unknown"}
            },
            "ai_integration": ai_integration,
            "capabilities": list(ai_integration["capabilities"]) + (["Claude Integration"] if ai_integration["providers"] else []),
            "application_flow": [],
            "documentation_status": {
                "readme_exists": any("readme" in f.lower() for f in structure["key_files"]),
                "changelog_exists": any("changelog" in f.lower() for f in structure["technology_indicators"]["documentation"]),
                "architecture_docs": [f for f in structure["technology_indicators"]["documentation"] if "architecture" in f.lower()],
                "workflow_files": [f for f in structure["technology_indicators"]["backend"] if "workflow" in f.lower() or "orchestrator" in f.lower()],
                "api_documentation": [],
                "deployment_guides": [f for f in structure["technology_indicators"]["documentation"] if any(term in f.lower() for term in ["deploy", "setup"])]
            },
            "database_readiness": {"database_type": "unknown", "orm_detected": False, "schema_files": [], "migration_files": [], "readiness_score": 0},
            "architecture": {"layers": [], "patterns": [], "dependencies": {}, "complexity_score": 0},
            "architecture_analysis": architecture_analysis,
            "recent_features": {"git_changes": [], "new_files": structure["key_files"] + list(structure["technology_indicators"]["documentation"])[:20], "modified_files": [], "feature_flags": []},
            "performance_metrics": {
                "file_count": structure["total_files"],
                "directory_count": len(structure["directories"]),
                "function_density": round(total_functions / max(1, structure["total_files"]), 2),
                "documentation_coverage": round((documented_functions / max(1, total_functions)) * 100, 2),
                "complexity_score": "high" if total_functions > 500 else "medium" if total_functions > 100 else "low"
            },
            "deployment": {"platform": "Replit" if ".replit" in str(structure["key_files"]) else "unknown", "start_command": "unknown", "config_files": [f for f in structure["key_files"] if f.endswith(('.replit', 'Dockerfile', 'docker-compose.yml'))]},
            "version_correlation": {"changelog_version": "1.1.10", "last_checkpoint": None, "archived_at": datetime.datetime.now().isoformat() + "Z", "note": "Enhanced summary version is independent of changelog milestones"},
            "future_enhancements": [
                f"Improve documentation coverage from {round((documented_functions / max(1, total_functions)) * 100, 1)}% to 80%+",
                "Complete database integration setup",
                "Add comprehensive testing suite"
            ]
        }

    def _summarize_missing_by_dir(self, missing_breadcrumbs: List[Dict]) -> Dict[str, int]:
        """Summarize missing breadcrumbs by directory"""
        dir_counts = {}
        for item in missing_breadcrumbs:
            dir_path = os.path.dirname(item["file"])
            if dir_path not in dir_counts:
                dir_counts[dir_path] = 0
            dir_counts[dir_path] += len(item["missing"])
        return dict(sorted(dir_counts.items(), key=lambda x: x[1], reverse=True)[:10])

    def _analyze_codebase_architecture(self, structure: Dict, code_analysis: Dict) -> Dict[str, Any]:
        """Analyze actual codebase architecture and relationships"""
        # Core directories (exclude system/cache dirs)
        core_dirs = [d for d in structure["directories"] 
                    if not any(skip in d for skip in ['.cache', '.local', '.pythonlibs', '.upm', '.config'])][:15]
        
        # Detect architecture patterns from structure
        patterns = []
        if any('api' in d.lower() or 'routes' in d.lower() for d in core_dirs):
            patterns.append("API Layer")
        if any('components' in d.lower() or 'ui' in d.lower() for d in core_dirs):
            patterns.append("Component Architecture")
        if any('workflow' in d.lower() or 'orchestrat' in d.lower() for d in core_dirs):
            patterns.append("Workflow Orchestration")
        if any('agent' in d.lower() or 'ai' in d.lower() for d in core_dirs):
            patterns.append("AI Agent System")
        if any('template' in d.lower() or 'client' in d.lower() for d in core_dirs):
            patterns.append("Template System")
        
        # Main modules (directories with most functions)
        lang_breakdown = code_analysis.get("language_breakdown", {})
        main_modules = core_dirs[:8]  # Top 8 core directories
        
        return {
            "core_directories": main_modules,
            "architecture_patterns": patterns,
            "complexity_indicators": {
                "total_directories": len(core_dirs),
                "function_distribution": dict(list(lang_breakdown.items())[:5]),
                "integration_points": len(structure["technology_indicators"]["ai_integration"])
            }
        }

    def _generate_architecture_diagram(self, summary: Dict) -> str:
        """Generate dynamic architecture diagram from actual codebase analysis"""
        arch = summary.get("architecture_analysis", {})
        project_name = summary["project_name"]
        stats = summary["code_analysis"]
        
        # Build core modules diagram
        core_modules = arch.get("core_directories", [])[:6]
        module_nodes = ""
        module_connections = ""
        
        for i, module in enumerate(core_modules):
            clean_name = module.replace('_', ' ').replace('-', ' ').title()
            module_nodes += f"        M{i}[{clean_name}]\n"
            if i > 0:
                module_connections += f"        M{i-1} --> M{i}\n"
        
        # Architecture patterns
        patterns = arch.get("architecture_patterns", [])
        pattern_nodes = ""
        for i, pattern in enumerate(patterns[:4]):
            pattern_nodes += f"        P{i}[{pattern}]\n"
        
        # Technology indicators
        tech_stats = summary["project_structure"]["technology_indicators"]
        backend_count = len(tech_stats.get("backend", []))
        frontend_count = len(tech_stats.get("frontend", []))
        ai_count = len(tech_stats.get("ai_integration", []))
        
        diagram_content = f"""# {project_name} - Dynamic Architecture Analysis

*Auto-generated from codebase structure analysis*
*Version: {summary["version"]} | Generated: {summary["updated_at"][:19]}Z*

## Core System Architecture
```mermaid
graph TB
    subgraph "📁 Core Modules"
{module_nodes}
{module_connections}    end

    subgraph "🏗 Architecture Patterns"
{pattern_nodes}    end

    subgraph "📊 Technology Distribution"
        T1[Backend Files: {backend_count}]
        T2[Frontend Files: {frontend_count}]
        T3[AI Integration: {ai_count}]
        T4[Total Functions: {stats["total_functions"]}]
    end

    subgraph "🤖 Agent Context"
        A1[Documentation Coverage: {stats["coverage_percentage"]}%]
        A2[Files Analyzed: {stats["total_files_analyzed"]}]
        A3[Missing Docs: {stats["missing_count"]}]
    end
```

## Module Relationships
```mermaid
flowchart LR
    subgraph "Core System Flow"
        START[Project Entry] --> ANALYSIS[Code Analysis]
        ANALYSIS --> WORKFLOW[Workflow System]
        WORKFLOW --> OUTPUT[Agent Output]
    end
    
    subgraph "Documentation Layer"
        BREADCRUMBS[Function Breadcrumbs]
        COVERAGE[Coverage Tracking] 
        MISSING[Missing Analysis]
        
        BREADCRUMBS --> COVERAGE
        COVERAGE --> MISSING
    end
    
    ANALYSIS --> BREADCRUMBS
    MISSING --> OUTPUT
```

## Directory Structure Map
```mermaid
graph TD
    ROOT[{project_name}]
"""
        
        # Add directory structure
        for i, dir_name in enumerate(core_modules):
            clean_dir = dir_name.replace('_', ' ').replace('-', ' ')
            diagram_content += f"    ROOT --> D{i}[{clean_dir}]\n"
        
        diagram_content += f"""
    classDef coreModule fill:#e3f2fd,stroke:#1976d2
    classDef analysis fill:#f3e5f5,stroke:#7b1fa2
    classDef output fill:#e8f5e8,stroke:#388e3c
    
    class M0,M1,M2,M3,M4,M5 coreModule
    class T1,T2,T3,T4 analysis
    class A1,A2,A3 output
```

---
*Dynamic architecture analysis - reflects actual codebase structure*  
*Core Directories: {len(core_modules)} | Patterns: {len(patterns)} | Coverage: {stats["coverage_percentage"]}%*
"""
        
        return diagram_content

    def _generate_markdown_summary(self, summary: Dict) -> str:
        """Generate markdown summary for human-readable documentation"""
        project_name = summary["project_name"]
        version = summary["version"]
        description = summary["description"]
        updated_at = summary["updated_at"][:19].replace('T', ' ')
        
        # Technology indicators
        tech_indicators = summary["project_structure"]["technology_indicators"]
        backend_count = len(tech_indicators.get("backend", []))
        frontend_count = len(tech_indicators.get("frontend", []))
        ai_count = len(tech_indicators.get("ai_integration", []))
        doc_count = len(tech_indicators.get("documentation", []))
        
        # Code analysis stats
        code_stats = summary["code_analysis"]
        total_files = summary["project_structure"]["total_files"]
        total_dirs = len(summary["project_structure"]["directories"])
        
        # AI integration
        ai_integration = summary["ai_integration"]
        providers = ", ".join(ai_integration.get("providers", []))
        capabilities = ", ".join(ai_integration.get("capabilities", []))
        
        return f"""# {project_name} - Enhanced Codebase Summary

*Generated by: codebase_summary/update_project_summary.py - Enhanced project summary generator*

**Version:** {version}  
**Generated:** {updated_at}  
**Description:** {description}

*Core project documentation system*

## 🚀 Deployment Architecture

This system supports **dual deployment modes** with universal path resolution:
- **Development Mode**: Full integration with project root file structure
- **Subdirectory Mode**: Non-destructive integration as `/Arkival` subdirectory
- **Universal Path Resolution**: Automatic detection and path adjustment via `find_arkival_paths()`

## 📊 Project Overview

### Technology Stack
- **Backend:** {backend_count} files
- **Frontend:** {frontend_count} files
- **AI Integration:** {ai_count} files
- **Documentation:** {doc_count} files

### Architecture Overview
{len(summary.get("architecture_analysis", {}).get("architecture_patterns", []))} architecture patterns detected: {", ".join(summary.get("architecture_analysis", {}).get("architecture_patterns", []))}

## 🏗 Project Structure

- **Total Files:** {total_files}
- **Directories:** {total_dirs}
- **File Types:** {len(summary["project_structure"]["file_types"])} different extensions

## 🔍 Code Analysis

- **Total Functions:** {code_stats["total_functions"]}
- **Documentation Coverage:** {code_stats["coverage_percentage"]}%
- **Files Analyzed:** {code_stats["total_files_analyzed"]}
- **Missing Documentation:** {code_stats["missing_count"]} functions

## 🤖 AI Integration

**Providers:** {providers or "None detected"}  
**Capabilities:** {capabilities or "None detected"}  
**Integration Files:** {len(ai_integration.get("integration_files", []))} detected

## 📚 Documentation Status

- **README:** {'✅ Present' if summary["documentation_status"]["readme_exists"] else '❌ Missing'}
- **Changelog:** {'✅ Present' if summary["documentation_status"]["changelog_exists"] else '❌ Missing'}
- **Architecture Docs:** {len(summary["documentation_status"]["architecture_docs"])} files
- **Workflow Files:** {len(summary["documentation_status"]["workflow_files"])} files

## 🚀 Capabilities

{chr(10).join(f"- {cap}" for cap in summary.get("capabilities", []))}

## 📈 Performance Metrics

- **File Count:** {summary["performance_metrics"]["file_count"]}
- **Directory Count:** {summary["performance_metrics"]["directory_count"]}
- **Function Density:** {summary["performance_metrics"]["function_density"]} functions/file
- **Complexity Score:** {summary["performance_metrics"]["complexity_score"]}

---

*This enhanced summary was automatically generated from comprehensive codebase analysis.*
"""

    def _write_missing_breadcrumbs(self, missing_breadcrumbs: List[Dict], total_funcs: int, doc_funcs: int, language_breakdown: Dict):
        """Write separate missing breadcrumbs file"""
        missing_data = {
            "_generator": "Generated by codebase_summary/update_project_summary.py - Missing documentation breadcrumbs analysis",
            "generated_at": datetime.datetime.now().isoformat() + "Z",
            "summary": {
                "total_functions": total_funcs,
                "documented_functions": doc_funcs,
                "missing_count": total_funcs - doc_funcs,
                "coverage_percentage": round((doc_funcs / max(1, total_funcs)) * 100, 2)
            },
            "language_breakdown": language_breakdown,
            "missing_breadcrumbs": missing_breadcrumbs
        }
        
        self.paths['missing_breadcrumbs'].parent.mkdir(parents=True, exist_ok=True)
        with open(self.paths['missing_breadcrumbs'], 'w', encoding='utf-8') as f:
            json.dump(missing_data, f, indent=2)

    def _get_current_version(self) -> str:
        """Get current version from existing summary"""
        if self.summary_path.exists():
            try:
                with open(self.summary_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get("version", "1.1.0")
            except:
                pass
        return "1.1.0"

    def _increment_version(self, current_version: str) -> str:
        """Increment version number"""
        try:
            parts = current_version.split('.')
            if len(parts) == 3:
                major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
                return f"{major}.{minor}.{patch + 1}"
        except:
            pass
        return "1.1.1"

    def _archive_previous_version(self, current_version: str):
        """Enhanced archiving with metadata and history cleanup"""
        if not self.summary_path.exists():
            return

        self.history_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_filename = f"codebase_summary_v{current_version}_{timestamp}.json"
        archive_path = self.history_dir / archive_filename

        try:
            shutil.copy2(self.summary_path, archive_path)
            logging.info(f"Archived previous version to {archive_filename}")
            
            # Clean up old history files - keep only 6 most recent
            self._cleanup_history_files()
        except Exception as e:
            logging.error(f"Failed to archive previous version: {e}")
    
    def _cleanup_history_files(self):
        """Keep only the 6 most recent history files to reduce token load"""
        try:
            # Get all history JSON files
            history_files = list(self.history_dir.glob("codebase_summary_v*.json"))
            
            if len(history_files) > 6:
                # Sort by modification time (newest first)
                history_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
                
                # Remove files beyond the 6 most recent
                for old_file in history_files[6:]:
                    old_file.unlink()
                    logging.info(f"Removed old history file: {old_file.name}")
                
                print(f"✅ Cleaned up {len(history_files) - 6} old history files")
        except Exception as e:
            logging.warning(f"Failed to cleanup history files: {e}")
    
    def _load_ignore_patterns(self) -> set:
        """Load ignore patterns from .scanignore file"""
        ignore_patterns = set()
        
        # Default patterns for performance
        default_ignores = {
            '.git', '__pycache__', 'node_modules', '.cache', '.vscode', '.idea',
            '.DS_Store', 'vendor', 'build', 'dist', 'target', 'bin', 'obj', 'out',
            '.next', '.nuxt', 'coverage', 'test-results', '.pytest_cache'
        }
        ignore_patterns.update(default_ignores)
        
        # Load custom patterns from .scanignore
        ignore_file = self.paths.get('scan_ignore')
        if ignore_file and ignore_file.exists():
            try:
                with open(ignore_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            ignore_patterns.add(line.rstrip('/'))
                print(f"✅ Loaded {len(ignore_patterns) - len(default_ignores)} custom ignore patterns")
            except Exception as e:
                print(f"⚠️ Warning: Could not load .scanignore: {e}")
        
        return ignore_patterns
    
    def _should_ignore_path(self, path: Path) -> bool:
        """Check if a path should be ignored based on patterns"""
        path_str = str(path.relative_to(self.project_root))
        
        # Check each part of the path
        for part in path.parts:
            if part in self.ignore_patterns:
                return True
        
        # Check full path against glob patterns
        for pattern in self.ignore_patterns:
            if '*' in pattern or '?' in pattern:
                if fnmatch.fnmatch(path_str, pattern):
                    return True
            elif pattern in path_str:
                return True
        
        return False

    def generate_summary(self):
        """Generate optimized project summary"""
        print("🔍 OPTIMIZED PROJECT SUMMARY GENERATION")
        if "--verbose" in sys.argv:
            print("   📄 Running in VERBOSE mode (detailed output)")
        else:
            print("   📦 Running in OPTIMIZED mode (AI agent friendly)")
        print("=" * 45)

        try:
            current_version = self._get_current_version()
            new_version = self._increment_version(current_version)
            
            # Archive previous version before generating new one
            self._archive_previous_version(current_version)
            
            summary = self._generate_optimized_summary(new_version)
            
            # Write main summary
            self.summary_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.summary_path, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2)
            
            # Write missing breadcrumbs separately (for detailed analysis)
            code_extensions = {
                '.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.go', '.rs', '.c', '.cpp', '.cc', '.cxx',
                '.php', '.rb', '.swift', '.kt', '.dart', '.sql', '.css', '.scss', '.sass', '.vue', 
                '.lua', '.scala', '.clj', '.cljs', '.r', '.m', '.mm', '.cs', '.sh', '.bash', '.zsh', '.ps1'
            }
            missing_breadcrumbs = []
            for root, dirs, files in os.walk(self.project_root):
                root_path = Path(root)
                
                # Skip ignored directories
                if self._should_ignore_path(root_path):
                    continue
                    
                # Remove ignored directories from dirs list to prevent os.walk from entering them
                dirs[:] = [d for d in dirs if not self._should_ignore_path(root_path / d)]
                    
                for file in files:
                    if Path(file).suffix in code_extensions:
                        file_path = Path(root) / file
                        analysis = self._analyze_code_file(str(file_path))
                        if analysis["missing_breadcrumbs"]:
                            missing_breadcrumbs.append({
                                "file": analysis["file"],
                                "missing": analysis["missing_breadcrumbs"]
                            })
            
            self._write_missing_breadcrumbs(
                missing_breadcrumbs,
                summary["code_analysis"]["total_functions"],
                summary["code_analysis"]["documented_functions"],
                summary["code_analysis"]["language_breakdown"]
            )
            
            # Generate architecture diagram
            architecture_diagram = self._generate_architecture_diagram(summary)
            architecture_path = self.project_root / "ARCHITECTURE_DIAGRAM.md"
            with open(architecture_path, 'w', encoding='utf-8') as f:
                f.write(architecture_diagram)
            
            # Generate markdown summary
            markdown_summary = self._generate_markdown_summary(summary)
            markdown_path = self.project_root / "CODEBASE_SUMMARY.md"
            with open(markdown_path, 'w', encoding='utf-8') as f:
                f.write(markdown_summary)
            
            print("✅ Enhanced project summary generated successfully")
            print(f"\n📊 PROJECT SUMMARY STATISTICS")
            print(f"Project: {summary['project_name']} v{summary['version']}")
            print(f"Total Files: {summary['project_structure']['total_files']}")
            print(f"Total Functions: {summary['code_analysis']['total_functions']}")
            print(f"Documentation Coverage: {summary['code_analysis']['coverage_percentage']}%")
            print(f"AI Providers: {len(summary['ai_integration']['providers'])}")
            
        except Exception as e:
            print(f"❌ Error generating summary: {e}")
            return False
        
        return True

def main():
    """Main entry point"""
    generator = OptimizedProjectSummaryGenerator()
    generator.generate_summary()

if __name__ == "__main__":
    main()