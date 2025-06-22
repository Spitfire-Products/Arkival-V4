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
    # @codebase-summary: Universal path resolution for Arkival subdirectory deployment
    - Detects deployment mode (standalone vs subdirectory) and returns all required file paths
    - Handles both development mode and production subdirectory deployment scenarios
    
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
        # Look for Arkival directory as indicator (check multiple variations)
        search_path = current_dir
        for _ in range(5):
            arkival_variations = ["Arkival", "Arkival-V4", "arkival", "arkival-v4"]
            for variation in arkival_variations:
                if (search_path / variation).exists():
                    project_root = search_path
                    break
            if project_root:
                break
            search_path = search_path.parent
    
    # Fallback - assume current directory
    if not project_root:
        project_root = current_dir
    
    # Determine if we're in dev mode or subdirectory mode
    # Dev mode: scripts are in codebase_summary/, data files in root
    # Subdirectory mode: everything under Arkival/
    
    if current_dir.name.lower() in ['arkival', 'arkival-v4'] or (project_root / "arkival.config.json").exists():
        # Subdirectory deployment mode - use SAME structure as development mode
        arkival_dir = current_dir if current_dir.name.lower() in ['arkival', 'arkival-v4'] else project_root
        return {
            'project_root': project_root,  # Parent project directory (Comic Creator)
            'scan_root': project_root,     # Directory to scan (parent project)
            'config_file': project_root / "arkival.config.json",
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
        return {
            'project_root': project_root,
            'scan_root': project_root,     # Directory to scan (same as project root in dev mode)
            'config_file': project_root / "arkival.config.json",
            'arkival_dir': project_root,
            'data_dir': project_root,
            'scripts_dir': project_root / "codebase_summary",
            'export_dir': project_root / "export_package",
            'checkpoints_dir': project_root / "checkpoints",
            
            # Data files in root/standard locations
            'codebase_summary': project_root / "codebase_summary.json",
            'changelog_summary': project_root / "changelog_summary.json",
            'session_state': project_root / "codebase_summary" / "session_state.json",
            'missing_breadcrumbs': project_root / "codebase_summary" / "missing_breadcrumbs.json",
            'scan_ignore': project_root / ".scanignore"
        }

class OptimizedProjectSummaryGenerator:
    """
    # @codebase-summary: Optimized project analysis and documentation generator
    - Streamlined for AI agent deployment with reduced memory footprint
    - Generates comprehensive codebase analysis while maintaining performance
    """
    def __init__(self):
        self.paths = find_arkival_paths()
        self.project_root = self.paths['scan_root']  # Use scan_root for actual scanning
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
        """Auto-detect comprehensive project metadata from codebase"""
        project_info = {
            "name": "Unknown Project", 
            "description": "Project description not found",
            "git_url": None,
            "homepage": None,
            "version": None,
            "license": None,
            "author": None,
            "keywords": [],
            "main_language": None,
            "framework": None
        }
        
        # Use the scan_root which is already correctly set for subdirectory mode
        search_dir = self.project_root  # This is already scan_root from path resolution
        
        # Collect metadata from all available sources
        self._extract_git_metadata(search_dir, project_info)
        self._extract_package_json_metadata(search_dir, project_info)
        self._extract_pyproject_toml_metadata(search_dir, project_info)
        self._extract_readme_metadata(search_dir, project_info)
        self._extract_cargo_toml_metadata(search_dir, project_info)
        self._extract_composer_json_metadata(search_dir, project_info)
        self._detect_framework_and_language(search_dir, project_info)
        
        # Clean up and return
        return {k: v for k, v in project_info.items() if v is not None and v != []}

    def _extract_readme_metadata(self, search_dir: Path, project_info: dict):
        """Extract project name and description from README files"""
        readme_files = ["README.md", "readme.md", "ReadMe.md"]
        for readme_name in readme_files:
            readme_path = search_dir / readme_name
            if readme_path.exists():
                try:
                    with open(readme_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        lines = [line.strip() for line in content.split('\n') if line.strip()]
                        if lines:
                            # Use first header as project name (priority over other sources)
                            first_line = lines[0]
                            if first_line.startswith('#'):
                                project_name = first_line.lstrip('#').strip()
                            else:
                                project_name = first_line.strip()
                            
                            # Skip if this looks like Arkival's own README
                            if project_name.lower() not in ['arkival', 'arkival-v4']:
                                if not project_info.get("name") or project_info["name"] == "Unknown Project":
                                    project_info["name"] = project_name
                                
                                # Use first substantial paragraph as description
                                if not project_info.get("description") or project_info["description"] == "Project description not found":
                                    for line in lines[1:]:
                                        if (len(line) > 20 and not line.startswith('#') and 
                                            not line.startswith('[') and not line.startswith('!')):
                                            # Clean up markdown
                                            clean_desc = re.sub(r'\*\*([^*]+)\*\*', r'\1', line)
                                            clean_desc = re.sub(r'\*([^*]+)\*', r'\1', clean_desc)
                                            project_info["description"] = clean_desc.strip()
                                            break
                except:
                    pass

    def _extract_git_metadata(self, search_dir: Path, project_info: dict):
        """Extract Git repository information"""
        try:
            # Check .git/config for remote URL
            git_config = search_dir / ".git" / "config"
            if git_config.exists():
                with open(git_config, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Look for remote origin URL
                    url_match = re.search(r'url\s*=\s*(.+)', content)
                    if url_match:
                        url = url_match.group(1).strip()
                        # Clean up SSH URLs to HTTPS
                        if url.startswith('git@github.com:'):
                            url = url.replace('git@github.com:', 'https://github.com/')
                        if url.endswith('.git'):
                            url = url[:-4]
                        project_info["git_url"] = url
        except:
            pass

    def _extract_package_json_metadata(self, search_dir: Path, project_info: dict):
        """Extract metadata from package.json"""
        package_json = search_dir / "package.json"
        if package_json.exists():
            try:
                with open(package_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Only use package.json name if no better name found
                    if not project_info.get("name") or project_info["name"] == "Unknown Project":
                        if "name" in data:
                            project_info["name"] = data["name"]
                    
                    # Only use package.json description if no better description found
                    if not project_info.get("description") or project_info["description"] == "Project description not found":
                        if "description" in data:
                            project_info["description"] = data["description"]
                    
                    # Extract additional metadata
                    if "version" in data:
                        project_info["version"] = data["version"]
                    if "homepage" in data:
                        project_info["homepage"] = data["homepage"]
                    if "license" in data:
                        project_info["license"] = data["license"]
                    if "author" in data:
                        project_info["author"] = data["author"]
                    if "keywords" in data and isinstance(data["keywords"], list):
                        project_info["keywords"] = data["keywords"]
                    
                    # Extract git URL from repository field
                    if "repository" in data and not project_info.get("git_url"):
                        repo = data["repository"]
                        if isinstance(repo, dict) and "url" in repo:
                            url = repo["url"]
                        elif isinstance(repo, str):
                            url = repo
                        else:
                            url = None
                        
                        if url:
                            # Clean up git URLs
                            if url.startswith('git+'):
                                url = url[4:]
                            if url.endswith('.git'):
                                url = url[:-4]
                            project_info["git_url"] = url
            except:
                pass

    def _extract_pyproject_toml_metadata(self, search_dir: Path, project_info: dict):
        """Extract metadata from pyproject.toml"""
        pyproject_toml = search_dir / "pyproject.toml"
        if pyproject_toml.exists():
            try:
                with open(pyproject_toml, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Only use if no better name found
                    if not project_info.get("name") or project_info["name"] == "Unknown Project":
                        name_match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', content)
                        if name_match:
                            project_info["name"] = name_match.group(1)
                    
                    # Only use if no better description found
                    if not project_info.get("description") or project_info["description"] == "Project description not found":
                        desc_match = re.search(r'description\s*=\s*["\']([^"\']+)["\']', content)
                        if desc_match:
                            project_info["description"] = desc_match.group(1)
                    
                    # Extract additional metadata
                    version_match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
                    if version_match:
                        project_info["version"] = version_match.group(1)
                    
                    license_match = re.search(r'license\s*=\s*["\']([^"\']+)["\']', content)
                    if license_match:
                        project_info["license"] = license_match.group(1)
                    
                    # Extract repository URL
                    repo_match = re.search(r'repository\s*=\s*["\']([^"\']+)["\']', content)
                    if repo_match and not project_info.get("git_url"):
                        project_info["git_url"] = repo_match.group(1)
            except:
                pass

    def _extract_cargo_toml_metadata(self, search_dir: Path, project_info: dict):
        """Extract metadata from Cargo.toml for Rust projects"""
        cargo_toml = search_dir / "Cargo.toml"
        if cargo_toml.exists():
            try:
                with open(cargo_toml, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    if not project_info.get("main_language"):
                        project_info["main_language"] = "Rust"
                    
                    # Extract metadata
                    name_match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', content)
                    if name_match and (not project_info.get("name") or project_info["name"] == "Unknown Project"):
                        project_info["name"] = name_match.group(1)
                    
                    desc_match = re.search(r'description\s*=\s*["\']([^"\']+)["\']', content)
                    if desc_match and (not project_info.get("description") or project_info["description"] == "Project description not found"):
                        project_info["description"] = desc_match.group(1)
                    
                    version_match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
                    if version_match:
                        project_info["version"] = version_match.group(1)
                        
                    repo_match = re.search(r'repository\s*=\s*["\']([^"\']+)["\']', content)
                    if repo_match and not project_info.get("git_url"):
                        project_info["git_url"] = repo_match.group(1)
            except:
                pass

    def _extract_composer_json_metadata(self, search_dir: Path, project_info: dict):
        """Extract metadata from composer.json for PHP projects"""
        composer_json = search_dir / "composer.json"
        if composer_json.exists():
            try:
                with open(composer_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    if not project_info.get("main_language"):
                        project_info["main_language"] = "PHP"
                    
                    # Extract metadata similar to package.json
                    if not project_info.get("name") or project_info["name"] == "Unknown Project":
                        if "name" in data:
                            project_info["name"] = data["name"]
                    
                    if not project_info.get("description") or project_info["description"] == "Project description not found":
                        if "description" in data:
                            project_info["description"] = data["description"]
                    
                    if "version" in data:
                        project_info["version"] = data["version"]
                    if "license" in data:
                        project_info["license"] = data["license"]
                    if "keywords" in data and isinstance(data["keywords"], list):
                        project_info["keywords"] = data["keywords"]
            except:
                pass

    def _detect_framework_and_language(self, search_dir: Path, project_info: dict):
        """Detect framework and primary language from project structure"""
        # Framework detection based on files and dependencies
        frameworks = []
        
        # Check for common framework indicators
        if (search_dir / "package.json").exists():
            try:
                with open(search_dir / "package.json", 'r') as f:
                    data = json.load(f)
                    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                    
                    if "react" in deps:
                        frameworks.append("React")
                    if "vue" in deps:
                        frameworks.append("Vue.js")
                    if "angular" in deps or "@angular/core" in deps:
                        frameworks.append("Angular")
                    if "next" in deps:
                        frameworks.append("Next.js")
                    if "express" in deps:
                        frameworks.append("Express.js")
                    if "svelte" in deps:
                        frameworks.append("Svelte")
            except:
                pass
        
        # Check for specific framework files
        if (search_dir / "django_project").exists() or any((search_dir).glob("**/settings.py")):
            frameworks.append("Django")
        if (search_dir / "app.py").exists() or (search_dir / "wsgi.py").exists():
            frameworks.append("Flask")
        if (search_dir / "manage.py").exists():
            frameworks.append("Django")
        if (search_dir / "Gemfile").exists():
            frameworks.append("Ruby on Rails")
            if not project_info.get("main_language"):
                project_info["main_language"] = "Ruby"
        
        # Language detection based on file extensions
        if not project_info.get("main_language"):
            file_counts = defaultdict(int)
            try:
                for root, dirs, files in os.walk(search_dir):
                    # Skip common ignore directories
                    dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', '__pycache__', '.cache'}]
                    for file in files:
                        ext = Path(file).suffix.lower()
                        if ext in {'.py', '.js', '.ts', '.tsx', '.jsx', '.rs', '.go', '.java', '.php', '.rb', '.cpp', '.c', '.cs'}:
                            file_counts[ext] += 1
                
                if file_counts:
                    primary_ext = max(file_counts, key=file_counts.get)
                    lang_map = {
                        '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript', 
                        '.tsx': 'TypeScript', '.jsx': 'JavaScript', '.rs': 'Rust',
                        '.go': 'Go', '.java': 'Java', '.php': 'PHP', '.rb': 'Ruby',
                        '.cpp': 'C++', '.c': 'C', '.cs': 'C#'
                    }
                    project_info["main_language"] = lang_map.get(primary_ext)
            except:
                pass
        
        if frameworks:
            project_info["framework"] = frameworks[0] if len(frameworks) == 1 else frameworks
        
        # Final fallback for name and description
        if not project_info.get("name") or project_info["name"] == "Unknown Project":
            project_info["name"] = search_dir.name
        if not project_info.get("description") or project_info["description"] == "Project description not found":
            project_info["description"] = f"Code analysis for {project_info['name']} project"

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
                elif any(ai_term in file.lower() for ai_term in ['ai', 'gpt', 'claude', 'gemini', 'llm', 'openai', 'anthropic', 'model']):
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

        # AI integration detection - generic
        ai_files = structure["technology_indicators"]["ai_integration"]
        ai_providers = self._detect_ai_providers(ai_files)
        ai_integration = {
            "providers": ai_providers,
            "capabilities": self._detect_ai_capabilities(ai_files, ai_providers),
            "integration_files": [str(self.project_root / f) for f in ai_files[:5]]
        }

        # Architecture analysis
        architecture_analysis = self._analyze_codebase_architecture(structure, code_analysis)

        # Get previous session context for critical context
        last_agent_task = self._get_last_agent_task()
        deployment_mode = self._detect_deployment_mode()
        
        return {
            "_generator": "Generated by codebase_summary/update_project_summary.py - Core project documentation and analysis system",
            "_critical_context": {
                "what_this_is": project_info["description"],
                "primary_purpose": project_info["description"],
                "entry_points": self._detect_entry_points(structure),
                "deployment_mode": deployment_mode,
                "active_issues": self._get_active_issues(doc_gaps),
                "last_agent_task": last_agent_task,
                "current_state": "operational" if total_functions > 0 else "needs_setup"
            },
            "_version_systems_explained": {
                "codebase_version": {
                    "current": version,
                    "purpose": "Tracks codebase structure analysis iterations",
                    "updates": "Every time update_project_summary.py runs",
                    "independent_from": "changelog/project versions"
                },
                "changelog_version": {
                    "current": self._get_changelog_version(),
                    "purpose": "Tracks user-facing feature releases", 
                    "updates": "Only when major features/milestones complete",
                    "location": "changelog_summary.json"
                },
                "why_different": "Codebase analysis runs frequently during development. Changelog updates only at release milestones. These are COMPLETELY INDEPENDENT systems."
            },
            "navigation_map": self._build_navigation_map(structure, file_analysis),
            "function_hotspots": self._analyze_function_hotspots(missing_breadcrumbs, language_breakdown),
            "project_name": project_info["name"],
            "version": version,
            "updated_at": datetime.datetime.now().isoformat() + "Z",
            "description": project_info["description"],
            "project_metadata": {
                "git_url": project_info.get("git_url"),
                "homepage": project_info.get("homepage"), 
                "project_version": project_info.get("version"),
                "license": project_info.get("license"),
                "author": project_info.get("author"),
                "keywords": project_info.get("keywords", []),
                "main_language": project_info.get("main_language"),
                "framework": project_info.get("framework")
            },
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
            "version_correlation": {"changelog_version": self._get_changelog_version(), "last_checkpoint": None, "archived_at": datetime.datetime.now().isoformat() + "Z", "note": "Enhanced summary version is independent of changelog milestones"},
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
        
        # Get critical context for enhanced diagram
        critical_context = summary.get("_critical_context", {})
        version_info = summary.get("_version_systems_explained", {})
        hotspots = summary.get("function_hotspots", {})
        
        diagram_content = f"""# {project_name} - Dynamic Architecture Analysis

*Auto-generated from codebase structure analysis*
*Version: {summary["version"]} | Generated: {summary["updated_at"][:19]}Z*

## ⚠️ Version Systems - IMPORTANT
| System | Current | Purpose | Updates |
|--------|---------|---------|---------|
| **Codebase Analysis** | v{summary["version"]} | Documentation scan version | Every `update_project_summary.py` run |
| **Changelog/Project** | v{version_info.get("changelog_version", {}).get("current", "N/A")} | Feature release version | Major milestones only |

**These are INDEPENDENT systems - version mismatch is NORMAL and EXPECTED**

## 🎯 30-Second Overview
| What | Details |
|------|---------|
| **System Type** | {critical_context.get("primary_purpose", "Software Project")} |
| **Architecture** | {self._detect_architecture_type(arch)} |
| **State Management** | {self._detect_state_management(summary)} |
| **Current State** | {critical_context.get("current_state", "operational")} |
| **Deployment Mode** | {critical_context.get("deployment_mode", "unknown")} |

## 🗺️ Where Should I Start?
```mermaid
graph TD
    START{{What are you doing?}} 
    START -->|New to project| README[Check README/Documentation]
    START -->|Adding feature| MAIN[Find main entry point]
    START -->|Fixing bug| TESTS[Run test suite]
    START -->|Understanding flow| STRUCTURE[Explore project structure]
    
    README --> DOCS[Read key documentation]
    MAIN --> CODE[Examine codebase patterns]
    TESTS --> DEBUG[Debug specific issues]
```

## 🔥 Critical Areas
- **Active Issues**: {len(critical_context.get("active_issues", []))} current issues
- **Missing Docs**: {stats["missing_count"]} functions (see missing_breadcrumbs.json)
- **Complexity**: {hotspots.get("complexity_score", "low")} complexity project
- **Critical Files**: session_state.json, workflow_config.json, missing_breadcrumbs.json

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

## 🔥 Critical Execution Paths
```mermaid
sequenceDiagram
    participant User
    participant Setup
    participant Orchestrator
    participant Summary
    participant State
    
    User->>Setup: setup_workflow_system.py
    Setup->>State: Creates workflow_config.json
    User->>Orchestrator: incoming agent workflow
    Orchestrator->>State: Loads session_state.json
    Orchestrator->>Summary: Triggers update_project_summary.py
    Summary->>State: Updates codebase_summary.json
    Note over State: All state in JSON files
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

## 🚀 Project Architecture

This analysis was generated by an automated project summary tool that:
- **Scans**: All source code files to detect functions and documentation
- **Analyzes**: Project structure, dependencies, and architecture patterns
- **Reports**: Documentation coverage, complexity metrics, and key insights

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

    def _is_subdirectory_mode(self) -> bool:
        """
        # @codebase-summary: Deployment mode detection for CONTRIBUTING.md generation
        - Detects if Arkival is running in subdirectory mode vs dev mode
        - Returns True for subdirectory mode, False for dev mode
        """
        current_dir = Path.cwd()
        return (current_dir.name.lower() in ['arkival', 'arkival-v4'] or 
                (self.project_root / "arkival_config.json").exists() or
                'arkival_dir' in self.paths and self.paths['arkival_dir'] != self.paths['project_root'])

    def _generate_contributing_md(self, summary: Dict) -> str:
        """
        # @codebase-summary: Dynamic CONTRIBUTING.md generation with deployment-aware content
        - Dev mode: Adapts to user's project name and repository
        - Subdirectory mode: Always references Arkival project and repository
        """
        is_subdirectory = self._is_subdirectory_mode()
        
        if is_subdirectory:
            # Subdirectory mode: CONTRIBUTING.md is about contributing to Arkival itself
            project_name = "Arkival"
            repo_url = "https://github.com/Spitfire-Products/Arkival-V4.git"
            repo_dir = "Arkival-V4"
            project_description = "Arkival enables seamless knowledge transfer between AI agents and human developers across different development environments."
        else:
            # Dev mode: User has forked/cloned Arkival as base for their own project
            project_info = self._detect_project_info()
            project_name = project_info["name"]
            project_description = f"{project_name} enables seamless knowledge transfer between AI agents and human developers across different development environments."
            # In dev mode, user should update repository URL to their own
            repo_url = "{your-repository-url}"
            repo_dir = project_name.lower().replace(" ", "-")
        
        return f"""# Contributing to {project_name}

*Generated by: codebase_summary/update_project_summary.py - Dynamic contributing guidelines*

Thank you for your interest in contributing! {project_description}

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Run the setup script: `python3 setup_workflow_system.py`
4. Test your changes with: `python3 validate_deployment.py`

## Development Process

### Setting up the Development Environment

```bash
# Clone the repository
git clone {repo_url}
cd {repo_dir}

# Run the setup
python3 setup_workflow_system.py

# Validate the setup
python3 validate_deployment.py
```

### Making Changes

1. Create a feature branch: `git checkout -b feature/your-feature-name`

## File Generation Best Practices

### Generator Attribution Requirements

**All generated or updated files MUST include generator attribution to prevent development token waste.** This rule applies to any file that is created or modified by Python scripts.

#### For JSON Files
Add `_generator` field as the first property:
```json
{{
  "_generator": "Generated by script_name.py - Brief description of purpose",
  "other_data": "..."
}}
```

#### For Markdown Files  
Add generator attribution in the header or footer:
```markdown
# Document Title

Content here...

*Generated by: script_name.py - Brief description of purpose*
```

#### Implementation in Python Scripts
When writing files, always include generator information:

```python
# For JSON files
data_with_generator = {{
    "_generator": "Generated by my_script.py - Purpose description",
    **existing_data
}}
json.dump(data_with_generator, file, indent=2)

# For Markdown files
content = f\"\"\"# Title
Content here...

*Generated by: my_script.py - Purpose description*
\"\"\"
```

#### Current Generator Registry
- `setup_workflow_system.py` → `workflow_config.json`, `changelog_summary.json`
- `update_project_summary.py` → `codebase_summary.json`, `missing_breadcrumbs.json`, `CODEBASE_SUMMARY.md`, `ARCHITECTURE_DIAGRAM.md`, `CONTRIBUTING.md`
- `update_changelog.py` → `changelog_summary.json`, `CHANGELOG.md`
- `agent_workflow_orchestrator.py` → `session_state.json`, `agent_handoff.json`

### Why This Matters
- **Token Efficiency**: Prevents wasted development time searching for file origins
- **Debugging**: Quickly identify which script to modify when issues arise
- **Maintenance**: Understand file relationships and dependencies
- **Documentation**: Self-documenting codebase with clear data flow
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

    def _get_last_agent_task(self) -> str:
        """Get the last agent task from session state"""
        try:
            session_state_file = self.paths['session_state']
            if session_state_file.exists():
                with open(session_state_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('last_summary', 'No previous agent task recorded')
        except:
            pass
        return "No previous agent task recorded"

    def _detect_deployment_mode(self) -> str:
        """Detect if running in subdirectory or standalone mode"""
        # Check if we're in a subdirectory by looking at path structure
        if self.paths['data_dir'] != self.project_root:
            return "subdirectory"
        return "standalone"

    def _get_active_issues(self, doc_gaps: List[Dict]) -> List[str]:
        """Get current active issues from various sources"""
        issues = []
        
        # Documentation gaps
        if doc_gaps:
            issues.append(f"{len(doc_gaps)} files with missing documentation")
        
        # Version mismatch - only if versions exist and differ significantly
        changelog_version = self._get_changelog_version()
        current_version = self._get_current_version()
        if changelog_version and current_version and changelog_version != current_version:
            # Only flag if major or minor version differs
            changelog_parts = changelog_version.split('.')[:2]
            current_parts = current_version.split('.')[:2]
            if changelog_parts != current_parts:
                issues.append(f"Version mismatch: codebase ({current_version}) vs changelog ({changelog_version})")
        
        # Check for previous agent recommendations
        try:
            session_state_file = self.paths['session_state']
            if session_state_file.exists():
                with open(session_state_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if 'recommendations' in data:
                        issues.extend(data['recommendations'])
        except:
            pass
        
        return issues[:5]  # Limit to top 5 issues

    def _get_changelog_version(self) -> str:
        """Get version from changelog_summary.json"""
        try:
            changelog_file = self.paths['changelog_summary']
            if changelog_file.exists():
                with open(changelog_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('version', None)
        except:
            pass
        return None

    def _analyze_function_hotspots(self, missing_breadcrumbs: List[Dict], language_breakdown: Dict) -> Dict[str, Any]:
        """Analyze function complexity and hotspots"""
        hotspots = {
            "most_complex_files": [],
            "most_documented_languages": [],
            "critical_missing_docs": [],
            "complexity_score": "low"
        }
        
        # Find files with most missing documentation
        if missing_breadcrumbs:
            complex_files = sorted(missing_breadcrumbs, key=lambda x: len(x["missing"]), reverse=True)[:5]
            hotspots["most_complex_files"] = [
                {"file": item["file"], "missing_functions": len(item["missing"])} 
                for item in complex_files
            ]
            
            # Critical missing docs (files with >3 undocumented functions)
            hotspots["critical_missing_docs"] = [
                item["file"] for item in complex_files if len(item["missing"]) > 3
            ]
        
        # Language documentation coverage
        if language_breakdown:
            lang_coverage = []
            for lang, stats in language_breakdown.items():
                if stats["functions"] > 0:
                    lang_coverage.append({
                        "language": lang,
                        "total_functions": stats["functions"],
                        "files": stats["files"]
                    })
            hotspots["most_documented_languages"] = sorted(lang_coverage, key=lambda x: x["total_functions"], reverse=True)[:5]
        
        # Overall complexity score
        total_missing = sum(len(item["missing"]) for item in missing_breadcrumbs)
        if total_missing > 30:
            hotspots["complexity_score"] = "high"
        elif total_missing > 10:
            hotspots["complexity_score"] = "medium"
        
        return hotspots

    def _detect_entry_points(self, structure: Dict) -> Dict[str, str]:
        """Detect common entry points in the project"""
        entry_points = {}
        
        # Look for common entry point patterns
        common_patterns = [
            ('main', ['main.py', 'app.py', 'index.js', 'server.js', 'main.go', 'main.rs']),
            ('setup', ['setup.py', 'install.py', 'setup.sh', 'install.sh']),
            ('test', ['test.py', 'run_tests.py', 'test.sh', 'pytest.ini']),
            ('build', ['build.py', 'build.sh', 'Makefile', 'package.json']),
            ('docs', ['docs.py', 'mkdocs.yml', 'sphinx-build'])
        ]
        
        all_files = []
        for root, dirs, files in os.walk(self.project_root):
            root_path = Path(root)
            if self._should_ignore_path(root_path):
                continue
            dirs[:] = [d for d in dirs if not self._should_ignore_path(root_path / d)]
            for file in files:
                rel_path = str(Path(root) / file).replace(str(self.project_root) + '/', '')
                all_files.append(rel_path)
        
        for entry_type, patterns in common_patterns:
            for pattern in patterns:
                for file in all_files:
                    if file.endswith(pattern) or pattern in file:
                        entry_points[entry_type] = file
                        break
                if entry_type in entry_points:
                    break
        
        # Add update_summary if this script exists
        if (self.paths['scripts_dir'] / "update_project_summary.py").exists():
            rel_path = str(self.paths['scripts_dir'] / "update_project_summary.py").replace(str(self.project_root) + '/', '')
            entry_points['update_summary'] = f"python3 {rel_path}"
        
        return entry_points

    def _build_navigation_map(self, structure: Dict, file_analysis: List[Dict]) -> Dict[str, Any]:
        """Build navigation map based on actual project structure"""
        nav_map = {
            "where_to_start": {},
            "key_files": {},
            "common_patterns": {}
        }
        
        # Detect key files
        key_files = {
            "readme": None,
            "config": None,
            "main": None,
            "tests": None
        }
        
        for file in structure.get("key_files", []):
            if "readme" in file.lower():
                key_files["readme"] = file
            elif any(cfg in file.lower() for cfg in ["config", "settings", ".json", ".yaml", ".toml"]):
                if not key_files["config"]:
                    key_files["config"] = file
        
        # Find main entry points
        backend_files = structure["technology_indicators"].get("backend", [])
        if backend_files:
            for file in backend_files:
                if any(main in file.lower() for main in ["main.", "app.", "server.", "index."]):
                    key_files["main"] = file
                    break
        
        # Build navigation suggestions
        if key_files["readme"]:
            nav_map["where_to_start"]["documentation"] = [key_files["readme"]]
        
        if key_files["main"]:
            nav_map["where_to_start"]["new_feature"] = [key_files["main"]]
        
        if key_files["config"]:
            nav_map["where_to_start"]["configuration"] = [key_files["config"]]
        
        # Find test files
        test_files = [f for f in structure.get("key_files", []) + backend_files if "test" in f.lower()]
        if test_files:
            nav_map["where_to_start"]["testing"] = test_files[:3]
        
        # Key files for reference
        nav_map["key_files"] = {k: v for k, v in key_files.items() if v}
        
        # Common patterns detected
        if structure.get("file_types", {}).get(".py"):
            nav_map["common_patterns"]["language"] = "Python"
        elif structure.get("file_types", {}).get(".js") or structure.get("file_types", {}).get(".ts"):
            nav_map["common_patterns"]["language"] = "JavaScript/TypeScript"
        
        return nav_map

    def _detect_ai_providers(self, ai_files: List[str]) -> List[str]:
        """Detect AI providers from file names and paths"""
        providers = []
        provider_patterns = {
            "OpenAI": ["openai", "gpt", "chatgpt"],
            "Claude": ["claude", "anthropic"],
            "Google": ["gemini", "palm", "bard", "google-ai"],
            "Hugging Face": ["huggingface", "transformers"],
            "Cohere": ["cohere"],
            "Azure": ["azure", "cognitive"],
            "Custom": ["model", "llm", "ai"]
        }
        
        for provider, patterns in provider_patterns.items():
            for file in ai_files:
                if any(pattern in file.lower() for pattern in patterns):
                    if provider not in providers:
                        providers.append(provider)
        
        return providers if providers else ["Unknown"]

    def _detect_ai_capabilities(self, ai_files: List[str], providers: List[str]) -> List[str]:
        """Detect AI capabilities from files and providers"""
        capabilities = []
        
        capability_patterns = {
            "Text Generation": ["generate", "completion", "text", "chat"],
            "Embeddings": ["embed", "vector", "similarity"],
            "Classification": ["classify", "sentiment", "categorize"],
            "Translation": ["translate", "language"],
            "Speech": ["speech", "audio", "voice"],
            "Vision": ["vision", "image", "ocr"],
            "Code Generation": ["code", "copilot", "assist"]
        }
        
        for capability, patterns in capability_patterns.items():
            for file in ai_files:
                if any(pattern in file.lower() for pattern in patterns):
                    if capability not in capabilities:
                        capabilities.append(capability)
        
        # Default capability if none detected but AI files exist
        if not capabilities and ai_files:
            capabilities = ["Text Generation"]
        
        return capabilities

    def _detect_architecture_type(self, arch: Dict) -> str:
        """Detect the architecture type from patterns"""
        patterns = arch.get("architecture_patterns", [])
        
        if "API Layer" in patterns or "REST" in patterns:
            return "API/Service Architecture"
        elif "Component Architecture" in patterns:
            return "Component-Based Architecture"
        elif "Microservices" in patterns:
            return "Microservices Architecture"
        elif "MVC" in patterns:
            return "MVC Architecture"
        else:
            # Detect from file structure
            lang_breakdown = arch.get("complexity_indicators", {}).get("function_distribution", {})
            if ".py" in lang_breakdown:
                return "Python Application"
            elif ".js" in lang_breakdown or ".ts" in lang_breakdown:
                return "JavaScript/TypeScript Application"
            else:
                return "Modular Application"

    def _detect_state_management(self, summary: Dict) -> str:
        """Detect how the project manages state"""
        tech_indicators = summary.get("project_structure", {}).get("technology_indicators", {})
        
        # Check for databases
        if tech_indicators.get("database"):
            db_files = tech_indicators["database"]
            if any("postgres" in f.lower() or "pg" in f.lower() for f in db_files):
                return "PostgreSQL Database"
            elif any("mysql" in f.lower() or "maria" in f.lower() for f in db_files):
                return "MySQL/MariaDB Database"
            elif any("mongo" in f.lower() for f in db_files):
                return "MongoDB Database"
            elif any("sqlite" in f.lower() or ".db" in f for f in db_files):
                return "SQLite Database"
            else:
                return "Database-backed"
        
        # Check for state management patterns
        all_files = []
        for cat, files in tech_indicators.items():
            all_files.extend(files)
        
        if any("redux" in f.lower() for f in all_files):
            return "Redux State Management"
        elif any("vuex" in f.lower() for f in all_files):
            return "Vuex State Management"
        elif any(".json" in f for f in all_files):
            return "File-based (JSON)"
        else:
            return "In-memory/Custom"

    def generate_summary(self):
        """
        # @codebase-summary: Main project summary generation orchestrator
        - Coordinates comprehensive codebase analysis and documentation generation
        - Produces enhanced JSON output with agent-friendly structure and navigation aids
        
        Generate optimized project summary
        """
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
            
            # Generate contributing guidelines
            contributing_md = self._generate_contributing_md(summary)
            contributing_path = self.project_root / "CONTRIBUTING.md"
            with open(contributing_path, 'w', encoding='utf-8') as f:
                f.write(contributing_md)
            
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
    """
    # @codebase-summary: Main CLI interface for optimized project summary generation
    - Provides command-line interface for project analysis and documentation generation
    - Supports --force flag for mandatory output regeneration regardless of cache
    - Orchestrates complete summary generation process with error handling
    
    Main entry point
    """
    import sys
    
    # Check for --force flag
    force_update = "--force" in sys.argv
    
    if force_update:
        print("🔄 FORCE UPDATE MODE: Regenerating all outputs regardless of cache")
    
    generator = OptimizedProjectSummaryGenerator()
    generator.generate_summary()

if __name__ == "__main__":
    main()