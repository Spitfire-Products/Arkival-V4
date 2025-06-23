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
    
    # Debug output for deployment troubleshooting
    print(f"🔍 DEBUG: Script running from: {current_dir}")
    
    # The setup script places arkival_config.json in the parent directory when in subdirectory mode
    # Search upward for this workflow flag to determine deployment mode
    project_root = None
    search_path = current_dir
    
    for _ in range(5):  # Search up to 5 levels up
        workflow_flag = search_path / "arkival_config.json"
        if workflow_flag.exists():
            project_root = search_path
            subdirectory_mode = True
            print(f"🔍 DEBUG: Found workflow flag at: {workflow_flag}")
            print(f"🔍 DEBUG: Subdirectory mode - project root: {project_root}")
            break
        if search_path.parent == search_path:  # Reached filesystem root
            break
        search_path = search_path.parent
    
    if project_root is None:
        # No workflow flag found - development mode
        project_root = current_dir
        subdirectory_mode = False
        print(f"🔍 DEBUG: No workflow flag found - development mode at: {project_root}")
    
    if subdirectory_mode:
        # Subdirectory deployment mode - place ALL generated files in Arkival-V4 directory
        arkival_dir = project_root / "Arkival-V4"
        print(f"🔍 DEBUG: All files will be written to: {arkival_dir}")
        
        return {
            'project_root': project_root,         # Parent project directory (for scanning)
            'scan_root': project_root,            # Directory to scan (parent project)
            'config_file': project_root / "arkival_config.json",
            'arkival_dir': arkival_dir,
            'data_dir': arkival_dir,
            'scripts_dir': arkival_dir / "codebase_summary",
            'export_dir': arkival_dir / "export_package",
            'checkpoints_dir': arkival_dir / "checkpoints",
            
            # ALL data files in Arkival-V4 directory - NEVER in project root
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
            'config_file': project_root / "arkival_config.json",
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
                r'(?:export\s+)?const\s+([A-Za-z_]\w*)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>',
                r'(?:export\s+)?const\s+([A-Za-z_]\w*)\s*=\s*(?:async\s+)?function',
                r'(?:export\s+)?let\s+([A-Za-z_]\w*)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>',
                r'(?:export\s+)?var\s+([A-Za-z_]\w*)\s*=\s*(?:async\s+)?function',
                r'const\s+(use[A-Z]\w*)\s*=\s*\([^)]*\)\s*=>',
                r'class\s+([A-Z]\w*)',
                r'\.([a-zA-Z_]\w*)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>',
                r'router\.(get|post|put|patch|delete|all)\s*\(',
                r'app\.(get|post|put|patch|delete|all)\s*\('
            ],
            'typescript': [
                r'(?:export\s+)?(?:async\s+)?function\s+([A-Za-z_]\w*)',
                r'(?:export\s+)?const\s+([A-Za-z_]\w*)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>',
                r'(?:export\s+)?const\s+([A-Za-z_]\w*)\s*=\s*(?:async\s+)?function',
                r'(?:export\s+)?let\s+([A-Za-z_]\w*)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>',
                r'(?:export\s+)?var\s+([A-Za-z_]\w*)\s*=\s*(?:async\s+)?function',
                r'const\s+(use[A-Z]\w*)\s*=\s*\([^)]*\)\s*=>',
                r'class\s+([A-Z]\w*)',
                r'\.([a-zA-Z_]\w*)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>',
                r'router\.(get|post|put|patch|delete|all)\s*\(',
                r'app\.(get|post|put|patch|delete|all)\s*\('
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
        
        # Collect metadata from all available sources (README first for name priority)
        self._extract_git_metadata(search_dir, project_info)
        self._extract_readme_metadata(search_dir, project_info)  # PRIORITY 1: Human-readable names
        self._extract_package_json_metadata(search_dir, project_info)
        self._extract_pyproject_toml_metadata(search_dir, project_info)
        self._extract_cargo_toml_metadata(search_dir, project_info)
        self._extract_composer_json_metadata(search_dir, project_info)
        self._extract_gemfile_metadata(search_dir, project_info)
        self._extract_go_mod_metadata(search_dir, project_info)
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
                    
                    # Extract dependencies for later use
                    if "dependencies" in data:
                        project_info["dependencies"] = data.get("dependencies", {})
                    if "devDependencies" in data:
                        project_info["devDependencies"] = data.get("devDependencies", {})
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
                    
                    # Extract Python dependencies - pyproject.toml can have dependencies in multiple formats
                    dependencies = []
                    dev_dependencies = []
                    
                    # Standard dependencies section
                    deps_match = re.search(r'dependencies\s*=\s*\[(.*?)\]', content, re.DOTALL)
                    if deps_match:
                        deps_content = deps_match.group(1)
                        # Extract dependency names (everything before version specifiers like >=, ==, etc.)
                        dep_patterns = re.findall(r'["\']([a-zA-Z0-9_-]+)(?:[><=~!].*?)?["\']', deps_content)
                        dependencies.extend(dep_patterns)
                    
                    # Development dependencies in [tool.poetry.group.dev.dependencies] or [project.optional-dependencies]
                    dev_deps_patterns = [
                        r'\[tool\.poetry\.group\.dev\.dependencies\](.*?)(?=\[|\Z)',
                        r'\[project\.optional-dependencies\].*?dev\s*=\s*\[(.*?)\]',
                        r'dev-dependencies\s*=\s*\[(.*?)\]'
                    ]
                    
                    for pattern in dev_deps_patterns:
                        dev_match = re.search(pattern, content, re.DOTALL)
                        if dev_match:
                            dev_content = dev_match.group(1)
                            dev_patterns = re.findall(r'["\']([a-zA-Z0-9_-]+)(?:[><=~!].*?)?["\']', dev_content)
                            dev_dependencies.extend(dev_patterns)
                    
                    # Store extracted dependencies
                    if dependencies:
                        project_info["python_dependencies"] = dependencies
                    if dev_dependencies:
                        project_info["python_dev_dependencies"] = dev_dependencies
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
                    
                    # Extract Rust dependencies from [dependencies] and [dev-dependencies] sections
                    dependencies = []
                    dev_dependencies = []
                    
                    # Regular dependencies
                    deps_match = re.search(r'\[dependencies\](.*?)(?=\[|\Z)', content, re.DOTALL)
                    if deps_match:
                        deps_content = deps_match.group(1)
                        # Extract dependency names (before = sign)
                        dep_names = re.findall(r'^([a-zA-Z0-9_-]+)\s*=', deps_content, re.MULTILINE)
                        dependencies.extend(dep_names)
                    
                    # Development dependencies
                    dev_deps_match = re.search(r'\[dev-dependencies\](.*?)(?=\[|\Z)', content, re.DOTALL)
                    if dev_deps_match:
                        dev_deps_content = dev_deps_match.group(1)
                        dev_dep_names = re.findall(r'^([a-zA-Z0-9_-]+)\s*=', dev_deps_content, re.MULTILINE)
                        dev_dependencies.extend(dev_dep_names)
                    
                    # Store extracted dependencies
                    if dependencies:
                        project_info["rust_dependencies"] = dependencies
                    if dev_dependencies:
                        project_info["rust_dev_dependencies"] = dev_dependencies
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
                    
                    # Extract PHP dependencies
                    if "require" in data:
                        project_info["php_dependencies"] = list(data.get("require", {}).keys())
                    if "require-dev" in data:
                        project_info["php_dev_dependencies"] = list(data.get("require-dev", {}).keys())
            except:
                pass

    def _extract_gemfile_metadata(self, search_dir: Path, project_info: dict):
        """Extract metadata from Gemfile for Ruby projects"""
        gemfile = search_dir / "Gemfile"
        if gemfile.exists():
            try:
                with open(gemfile, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    if not project_info.get("main_language"):
                        project_info["main_language"] = "Ruby"
                    
                    # Extract Ruby gems
                    dependencies = []
                    dev_dependencies = []
                    
                    # Regular gems
                    gem_matches = re.findall(r"gem\s+['\"]([^'\"]+)['\"]", content)
                    dependencies.extend(gem_matches)
                    
                    # Development/test gems
                    dev_blocks = re.findall(r"group\s+[:'](?:development|test)['\s,]*.*?do(.*?)end", content, re.DOTALL)
                    for block in dev_blocks:
                        dev_gems = re.findall(r"gem\s+['\"]([^'\"]+)['\"]", block)
                        dev_dependencies.extend(dev_gems)
                        # Remove from regular dependencies to avoid duplicates
                        for gem in dev_gems:
                            if gem in dependencies:
                                dependencies.remove(gem)
                    
                    # Store extracted dependencies
                    if dependencies:
                        project_info["ruby_dependencies"] = dependencies
                    if dev_dependencies:
                        project_info["ruby_dev_dependencies"] = dev_dependencies
                        
            except:
                pass

    def _extract_go_mod_metadata(self, search_dir: Path, project_info: dict):
        """Extract metadata from go.mod for Go projects"""
        go_mod = search_dir / "go.mod"
        if go_mod.exists():
            try:
                with open(go_mod, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    if not project_info.get("main_language"):
                        project_info["main_language"] = "Go"
                    
                    # Extract module name
                    module_match = re.search(r'module\s+([^\s]+)', content)
                    if module_match and (not project_info.get("name") or project_info["name"] == "Unknown Project"):
                        module_name = module_match.group(1).split('/')[-1]  # Get last part of module path
                        project_info["name"] = module_name
                    
                    # Extract Go dependencies
                    dependencies = []
                    
                    # Direct dependencies in require block
                    require_match = re.search(r'require\s*\((.*?)\)', content, re.DOTALL)
                    if require_match:
                        require_content = require_match.group(1)
                        dep_matches = re.findall(r'([^\s]+)\s+v[^\s]+', require_content)
                        dependencies.extend(dep_matches)
                    
                    # Single line requires
                    single_requires = re.findall(r'require\s+([^\s]+)\s+v[^\s]+', content)
                    dependencies.extend(single_requires)
                    
                    # Store extracted dependencies
                    if dependencies:
                        project_info["go_dependencies"] = dependencies
                        
            except:
                pass

    def _aggregate_runtime_dependencies(self, project_info: dict) -> List[str]:
        """Aggregate runtime dependencies from all package managers"""
        all_deps = []
        
        # JavaScript/Node.js (package.json)
        if project_info.get("dependencies"):
            all_deps.extend(list(project_info["dependencies"].keys()))
        
        # Python (pyproject.toml)
        if project_info.get("python_dependencies"):
            all_deps.extend(project_info["python_dependencies"])
        
        # Rust (Cargo.toml)
        if project_info.get("rust_dependencies"):
            all_deps.extend(project_info["rust_dependencies"])
        
        # PHP (composer.json)
        if project_info.get("php_dependencies"):
            all_deps.extend(project_info["php_dependencies"])
        
        # Ruby (Gemfile)
        if project_info.get("ruby_dependencies"):
            all_deps.extend(project_info["ruby_dependencies"])
        
        # Go (go.mod)
        if project_info.get("go_dependencies"):
            all_deps.extend(project_info["go_dependencies"])
        
        return list(set(all_deps))  # Remove duplicates

    def _aggregate_dev_dependencies(self, project_info: dict) -> List[str]:
        """Aggregate development dependencies from all package managers"""
        all_dev_deps = []
        
        # JavaScript/Node.js (package.json)
        if project_info.get("devDependencies"):
            all_dev_deps.extend(list(project_info["devDependencies"].keys()))
        
        # Python (pyproject.toml)
        if project_info.get("python_dev_dependencies"):
            all_dev_deps.extend(project_info["python_dev_dependencies"])
        
        # Rust (Cargo.toml)
        if project_info.get("rust_dev_dependencies"):
            all_dev_deps.extend(project_info["rust_dev_dependencies"])
        
        # PHP (composer.json)
        if project_info.get("php_dev_dependencies"):
            all_dev_deps.extend(project_info["php_dev_dependencies"])
        
        # Ruby (Gemfile)
        if project_info.get("ruby_dev_dependencies"):
            all_dev_deps.extend(project_info["ruby_dev_dependencies"])
        
        return list(set(all_dev_deps))  # Remove duplicates

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
            # First, count all files by extension to determine primary language
            file_counts = defaultdict(int)
            try:
                for root, dirs, files in os.walk(search_dir):
                    # Skip ignored directories
                    if self._should_ignore_path(Path(root)):
                        continue
                    dirs[:] = [d for d in dirs if not self._should_ignore_path(Path(root) / d)]
                    
                    for file in files:
                        if not self._should_ignore_path(Path(root) / file):
                            ext = Path(file).suffix.lower()
                            if ext in ['.py', '.js', '.ts', '.java', '.rb', '.go', '.rs', '.php', '.cs', '.cpp', '.c']:
                                file_counts[ext] += 1
                
                # Determine main language by file count
                if file_counts:
                    main_ext = max(file_counts, key=file_counts.get)
                    language_map = {
                        '.py': 'Python',
                        '.js': 'JavaScript', 
                        '.ts': 'TypeScript',
                        '.java': 'Java',
                        '.rb': 'Ruby',
                        '.go': 'Go',
                        '.rs': 'Rust',
                        '.php': 'PHP',
                        '.cs': 'C#',
                        '.cpp': 'C++',
                        '.c': 'C'
                    }
                    project_info["main_language"] = language_map.get(main_ext, 'Unknown')
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

    def _analyze_route_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Analyze Express.js route files for endpoints"""
        routes = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # Common Express.js route patterns
            route_patterns = [
                r'router\.(get|post|put|patch|delete|all)\s*\(\s*[\'"`]([^\'"`]+)[\'"`]',
                r'app\.(get|post|put|patch|delete|all)\s*\(\s*[\'"`]([^\'"`]+)[\'"`]',
                r'\.(get|post|put|patch|delete|all)\s*\(\s*[\'"`]([^\'"`]+)[\'"`]'
            ]
            
            for pattern in route_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for method, path in matches:
                    routes.append({
                        'method': method.upper(),
                        'path': path,
                        'file': str(Path(file_path).relative_to(self.project_root))
                    })
                    
        except Exception as e:
            print(f"⚠️ Error analyzing route file {file_path}: {e}")
            
        return routes

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

    def _single_pass_scan(self) -> Dict[str, Any]:
        """
        # @codebase-summary: Consolidated single-pass file system traversal
        - Replaces 5 separate os.walk() operations with one efficient scan
        - Collects project structure, code analysis, entry points, and file data simultaneously
        - Dramatically improves performance by eliminating redundant directory traversals
        """
        # Initialize all data structures for consolidated collection
        scan_data = {
            'project_structure': {
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
            },
            'code_analysis': {
                'file_analysis': [],
                'total_functions': 0,
                'documented_functions': 0,
                'missing_breadcrumbs': [],
                'language_breakdown': defaultdict(lambda: {"files": 0, "functions": 0})
            },
            'entry_points': {},
            'all_files': []
        }
        
        # Code file extensions
        code_extensions = {
            '.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.go', '.rs', '.c', '.cpp', '.cc', '.cxx',
            '.php', '.rb', '.swift', '.kt', '.dart', '.sql', '.css', '.scss', '.sass', '.vue', 
            '.lua', '.scala', '.clj', '.cljs', '.r', '.m', '.mm', '.cs', '.sh', '.bash', '.zsh', '.ps1'
        }
        
        # Key file patterns
        key_patterns = ["LICENSE", "README*", ".gitignore", "package.json", "pyproject.toml", "Cargo.toml"]
        
        # Entry point patterns
        entry_patterns = {
            'main': ['main.py', 'app.py', 'index.js', 'server.js', 'main.go', 'main.rs'],
            'setup': ['setup.py', 'install.py', 'setup.sh', 'install.sh'],
            'test': ['test.py', 'run_tests.py', 'test.sh', 'pytest.ini'],
            'build': ['build.py', 'build.sh', 'Makefile', 'package.json'],
            'docs': ['docs.py', 'mkdocs.yml', 'sphinx-build']
        }
        
        print("🔍 SINGLE-PASS OPTIMIZATION: Scanning entire project in one traversal...")
        
        # SINGLE os.walk() operation to replace all 5 separate scans
        for root, dirs, files in os.walk(self.project_root):
            root_path = Path(root)
            
            # Skip ignored directories
            if self._should_ignore_path(root_path):
                continue
                
            # Remove ignored directories from dirs list to prevent os.walk from entering them
            dirs[:] = [d for d in dirs if not self._should_ignore_path(root_path / d)]
                
            # Project structure data collection
            rel_root = str(Path(root).relative_to(self.project_root))
            if rel_root != '.':
                scan_data['project_structure']["directories"].append(rel_root)

            for file in files:
                file_path = Path(root) / file
                
                # Skip ignored files
                if self._should_ignore_path(file_path):
                    continue
                    
                scan_data['project_structure']["total_files"] += 1
                ext = Path(file).suffix
                scan_data['project_structure']["file_types"][ext] += 1
                
                rel_path = str(file_path.relative_to(self.project_root))
                scan_data['all_files'].append(rel_path)
                
                # Key files detection
                if any(pattern.replace('*', '') in file for pattern in key_patterns):
                    scan_data['project_structure']["key_files"].append(rel_path)
                
                # Technology indicators categorization
                if ext in ['.py', '.java', '.go', '.rs']:
                    scan_data['project_structure']["technology_indicators"]["backend"].append(rel_path)
                elif ext in ['.js', '.jsx', '.ts', '.tsx', '.vue']:
                    scan_data['project_structure']["technology_indicators"]["frontend"].append(rel_path)
                elif any(ai_term in file.lower() for ai_term in ['ai', 'gpt', 'claude', 'gemini', 'llm', 'openai', 'anthropic', 'model']):
                    scan_data['project_structure']["technology_indicators"]["ai_integration"].append(rel_path)
                elif ext in ['.sql', '.db']:
                    scan_data['project_structure']["technology_indicators"]["database"].append(rel_path)
                elif file.lower() in ['dockerfile', '.replit', 'docker-compose.yml']:
                    scan_data['project_structure']["technology_indicators"]["deployment"].append(rel_path)
                elif ext in ['.md', '.txt'] or 'doc' in file.lower():
                    scan_data['project_structure']["technology_indicators"]["documentation"].append(rel_path)
                
                # Entry points detection
                for entry_type, patterns in entry_patterns.items():
                    for pattern in patterns:
                        if file.endswith(pattern) or pattern in file:
                            if entry_type not in scan_data['entry_points']:
                                scan_data['entry_points'][entry_type] = rel_path
                            break
                
                # Route file detection - check file name, path, or if in routes directory
                is_route_file = (
                    ('route' in file.lower() or 
                     'route' in rel_path.lower() or
                     '/routes/' in rel_path or
                     rel_path.startswith('routes/')) 
                    and ext in ['.js', '.ts']
                )
                if is_route_file:
                    print(f"🔍 DEBUG: Found route file: {rel_path}")
                    route_analysis = self._analyze_route_file(str(file_path))
                    if route_analysis:
                        print(f"✅ DEBUG: Found {len(route_analysis)} routes in {rel_path}")
                        if 'routes' not in scan_data:
                            scan_data['routes'] = []
                        scan_data['routes'].extend(route_analysis)
                
                # Code analysis for programming files
                if ext in code_extensions:
                    analysis = self._analyze_code_file(str(file_path))
                    if analysis["function_count"] > 0:
                        scan_data['code_analysis']['file_analysis'].append(analysis)
                        scan_data['code_analysis']['total_functions'] += analysis["function_count"]
                        scan_data['code_analysis']['documented_functions'] += analysis["documented_count"]
                        
                        # Language breakdown
                        lang_key = ext
                        scan_data['code_analysis']['language_breakdown'][lang_key]["files"] += 1
                        scan_data['code_analysis']['language_breakdown'][lang_key]["functions"] += analysis["function_count"]
                        
                        # Missing breadcrumbs collection
                        if analysis["missing_breadcrumbs"]:
                            scan_data['code_analysis']['missing_breadcrumbs'].append({
                                "file": analysis["file"],
                                "missing": analysis["missing_breadcrumbs"]
                            })
        
        # Add update_summary entry point if this script exists
        if (self.paths['scripts_dir'] / "update_project_summary.py").exists():
            rel_path = str(self.paths['scripts_dir'] / "update_project_summary.py").replace(str(self.project_root) + '/', '')
            scan_data['entry_points']['update_summary'] = f"python3 {rel_path}"
        
        # Limit arrays for optimization
        for category in scan_data['project_structure']["technology_indicators"]:
            scan_data['project_structure']["technology_indicators"][category] = scan_data['project_structure']["technology_indicators"][category][:20]
        
        # Convert defaultdicts to regular dicts
        scan_data['project_structure']["file_types"] = dict(scan_data['project_structure']["file_types"])
        scan_data['code_analysis']['language_breakdown'] = dict(scan_data['code_analysis']['language_breakdown'])
        
        print(f"✅ OPTIMIZATION COMPLETE: Single scan processed {scan_data['project_structure']['total_files']} files")
        return scan_data

    def _generate_optimized_summary(self, version: str):
        """Generate optimized project summary using single-pass scanning"""
        project_info = self._detect_project_info()
        
        # Use single-pass scan to replace all separate scanning operations
        scan_data = self._single_pass_scan()
        structure = scan_data['project_structure']
        file_analysis = scan_data['code_analysis']['file_analysis']
        total_functions = scan_data['code_analysis']['total_functions']
        documented_functions = scan_data['code_analysis']['documented_functions']
        missing_breadcrumbs = scan_data['code_analysis']['missing_breadcrumbs']
        language_breakdown = scan_data['code_analysis']['language_breakdown']

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
            "language_breakdown": language_breakdown,
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
        
        summary = {
            "_generator": f"Generated by {self._get_generator_path()} - Core project documentation and analysis system",
            "_critical_context": {
                "what_this_is": project_info["description"],
                "primary_purpose": project_info["description"],
                "entry_points": scan_data['entry_points'],
                "deployment_mode": deployment_mode,
                "key_file_paths": {
                    "session_state": self._get_doc_file_path("session_state.json"),
                    "agent_handoff": self._get_doc_file_path("agent_handoff.json"),
                    "changelog": self._get_doc_file_path("changelog_summary.json"),
                    "workflow_config": self._get_doc_file_path("workflow_config.json"),
                    "missing_breadcrumbs": self._get_doc_file_path("missing_breadcrumbs.json")
                },
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
            "main_dependencies": {
                "runtime": self._aggregate_runtime_dependencies(project_info),
                "development": self._aggregate_dev_dependencies(project_info),
                "system": []
            },
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
        
        return (summary, scan_data)

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
- **Critical Files**: {self._get_doc_file_path("session_state.json")}, {self._get_doc_file_path("workflow_config.json")}, {self._get_doc_file_path("missing_breadcrumbs.json")}

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
    Orchestrator->>State: Loads {self._get_doc_file_path("session_state.json")}
    Orchestrator->>Summary: Triggers {self._get_generator_path()}
    Summary->>State: Updates {self._get_doc_file_path("codebase_summary.json")}
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
        
        # Extract actual technologies from project structure
        tech_indicators = summary["project_structure"]["technology_indicators"]
        detected_technologies = self._extract_technologies_from_project(tech_indicators, summary)
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

*Generated by: {self._get_generator_path()} - Enhanced project summary generator*

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
- **Backend:** {detected_technologies['backend']} ({backend_count} files)
- **Frontend:** {detected_technologies['frontend']} ({frontend_count} files)
- **AI Integration:** {detected_technologies['ai']} ({ai_count} files)
- **Documentation:** {detected_technologies['documentation']} ({doc_count} files)

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

    def _update_contributing_metadata_if_exists(self) -> bool:
        """
        # @codebase-summary: Metadata-only update for existing CONTRIBUTING.md in subdirectory mode
        - Only runs in subdirectory mode when CONTRIBUTING.md exists
        - Updates project name, description, and repo URL from parent directory metadata
        - Preserves existing content structure and user modifications
        """
        # Only update in subdirectory mode
        if not self._is_subdirectory_mode():
            return False
            
        contributing_path = self.paths['arkival_dir'] / "CONTRIBUTING.md"
        
        # Only update if file already exists
        if not contributing_path.exists():
            return False
            
        try:
            # Read existing content
            with open(contributing_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Scrape metadata from parent directory (project_root in subdirectory mode)
            project_info = self._detect_project_info()
            project_name = project_info.get("name", "Project")
            repo_url = project_info.get("git_url", "{repository-url}")
            
            # Generate description from detected metadata
            if project_info.get("description") and len(project_info["description"]) > 20:
                project_description = project_info["description"]
            else:
                project_description = f"{project_name} with AI agent workflow orchestration capabilities."
            
            # Update metadata sections (preserving existing structure)
            import re
            
            # Update title if it follows pattern "# Contributing to [Project]"
            content = re.sub(
                r'^# Contributing to [^#\n]+', 
                f'# Contributing to {project_name}', 
                content, flags=re.MULTILINE
            )
            
            # Update description in intro paragraph
            content = re.sub(
                r'(Thank you for your interest in contributing!) [^#]+?(## Getting Started)',
                f'\\1 {project_description}\n\n\\2',
                content, flags=re.DOTALL
            )
            
            # Update git clone URL in bash blocks
            content = re.sub(
                r'(git clone )[^\n]+',
                f'\\1{repo_url}',
                content
            )
            
            # Write updated content
            with open(contributing_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            return True
            
        except Exception as e:
            print(f"⚠️ Could not update CONTRIBUTING.md metadata: {e}")
            return False

    def _write_missing_breadcrumbs(self, missing_breadcrumbs: List[Dict], total_funcs: int, doc_funcs: int, language_breakdown: Dict):
        """Write separate missing breadcrumbs file"""
        missing_data = {
            "_generator": f"Generated by {self._get_generator_path()} - Missing documentation breadcrumbs analysis",
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
            '.next', '.nuxt', 'coverage', 'test-results', '.pytest_cache', '.claude',
            '.cursor', '.aider', '.codeium', '.copilot'  # AI coding tools
        }
        
        # CRITICAL: In subdirectory mode, ignore the Arkival directory itself
        deployment_mode = self._detect_deployment_mode()
        if deployment_mode == "subdirectory":
            default_ignores.add('Arkival-V4')
            default_ignores.add('Arkival')
            default_ignores.add('arkival-v4')
            default_ignores.add('arkival')
            print(f"🔍 DEBUG: Subdirectory mode - added Arkival directory ignores")
        ignore_patterns.update(default_ignores)
        print(f"🔍 DEBUG: Loaded {len(default_ignores)} default ignore patterns")
        
        # Load custom patterns from .scanignore
        ignore_file = self.paths.get('scan_ignore')
        print(f"🔍 DEBUG: Looking for .scanignore at: {ignore_file}")
        
        if ignore_file and ignore_file.exists():
            try:
                print(f"🔍 DEBUG: Loading .scanignore from: {ignore_file}")
                with open(ignore_file, 'r', encoding='utf-8') as f:
                    custom_patterns = []
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            ignore_patterns.add(line.rstrip('/'))
                            custom_patterns.append(line.rstrip('/'))
                print(f"✅ Loaded {len(custom_patterns)} custom ignore patterns: {custom_patterns}")
            except Exception as e:
                print(f"⚠️ Warning: Could not load .scanignore: {e}")
        else:
            print(f"🔍 DEBUG: No .scanignore file found at {ignore_file}")
        
        print(f"🔍 DEBUG: Total ignore patterns: {len(ignore_patterns)}")
        return ignore_patterns
    
    def _should_ignore_path(self, path: Path) -> bool:
        """Check if a path should be ignored based on patterns"""
        try:
            # Handle path relative to project_root with error checking
            if not path.is_relative_to(self.project_root):
                print(f"🔍 DEBUG: Path {path} not relative to project_root {self.project_root}")
                return False
                
            path_str = str(path.relative_to(self.project_root))
            
            # Debug: Print first few path checks
            if hasattr(self, '_debug_count'):
                self._debug_count += 1
            else:
                self._debug_count = 1
                
            if self._debug_count <= 5:
                print(f"🔍 DEBUG: Checking path: {path_str} against {len(self.ignore_patterns)} patterns")
                if self._debug_count == 1:
                    print(f"🔍 DEBUG: Ignore patterns: {sorted(list(self.ignore_patterns))[:10]}...")
            
            # Check each part of the path
            for part in path.parts:
                if part in self.ignore_patterns:
                    if self._debug_count <= 5:
                        print(f"🔍 DEBUG: IGNORED {path_str} - part '{part}' matches pattern")
                    return True
            
            # Check full path against glob patterns
            for pattern in self.ignore_patterns:
                if '*' in pattern or '?' in pattern:
                    if fnmatch.fnmatch(path_str, pattern):
                        if self._debug_count <= 5:
                            print(f"🔍 DEBUG: IGNORED {path_str} - matches glob pattern '{pattern}'")
                        return True
                # For non-glob patterns, check if it's a complete directory/file name match
                elif '/' not in pattern:
                    # Check if pattern matches any complete part of the path
                    path_parts = path_str.split('/')
                    if pattern in path_parts:
                        if self._debug_count <= 5 or 'routes' in path_str:
                            print(f"🔍 DEBUG: IGNORED {path_str} - part '{pattern}' matches complete directory/file name")
                        return True
                # For patterns with slashes, check if they match the path
                elif pattern in path_str:
                    if self._debug_count <= 5 or 'routes' in path_str:
                        print(f"🔍 DEBUG: IGNORED {path_str} - contains pattern '{pattern}'")
                    return True
            
            if self._debug_count <= 5:
                print(f"🔍 DEBUG: SCANNING {path_str} - no patterns matched")
            return False
            
        except Exception as e:
            print(f"🔍 DEBUG: Path ignore error for {path}: {e}")
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
        """Detect deployment mode by searching for arkival_config.json workflow flag"""
        current_dir = Path.cwd()
        search_path = current_dir
        
        # Search upward for arkival_config.json workflow flag
        for _ in range(5):
            workflow_flag = search_path / "arkival_config.json"
            if workflow_flag.exists():
                print(f"🔍 DEBUG: Deployment mode detection - found workflow flag: subdirectory mode")
                return "subdirectory"
            if search_path.parent == search_path:
                break
            search_path = search_path.parent
        
        print(f"🔍 DEBUG: Deployment mode detection - no workflow flag found: development mode")
        return "development"
    
    def _get_generator_path(self) -> str:
        """Get deployment-mode aware path for generator attribution"""
        deployment_mode = self._detect_deployment_mode()
        if deployment_mode == "subdirectory":
            return "Arkival-V4/codebase_summary/update_project_summary.py"
        return "codebase_summary/update_project_summary.py"
    
    def _get_doc_file_path(self, filename: str) -> str:
        """Get deployment-mode aware file path for documentation"""
        deployment_mode = self._detect_deployment_mode()
        if deployment_mode == "subdirectory":
            if filename in ["codebase_summary.json", "changelog_summary.json"]:
                return f"Arkival-V4/{filename}"
            elif "session_state.json" in filename or "missing_breadcrumbs.json" in filename or "agent_handoff.json" in filename:
                return f"Arkival-V4/codebase_summary/{filename}"
            elif filename == "workflow_config.json":
                return f"Arkival-V4/{filename}"
            else:
                return f"Arkival-V4/{filename}"
        return filename
    
    def _extract_technologies_from_project(self, tech_indicators: Dict, summary: Dict) -> Dict[str, str]:
        """Extract actual technology names from project files and structure"""
        technologies = {
            'backend': "None detected",
            'frontend': "None detected", 
            'ai': "None detected",
            'documentation': "None detected"
        }
        
        # Backend technologies
        backend_techs = []
        backend_files = tech_indicators.get("backend", [])
        for file in backend_files:
            if file.endswith('.py'):
                backend_techs.append("Python")
            elif file.endswith('.js'):
                backend_techs.append("Node.js")
            elif file.endswith('.java'):
                backend_techs.append("Java")
            elif file.endswith('.go'):
                backend_techs.append("Go")
            elif file.endswith('.rs'):
                backend_techs.append("Rust")
                
        # Check for frameworks in project files
        project_files = summary.get("project_structure", {}).get("key_files", [])
        for file in project_files:
            if "package.json" in file.lower():
                backend_techs.append("Node.js/npm")
            elif "requirements.txt" in file.lower() or "pyproject.toml" in file.lower():
                if "Python" not in backend_techs:
                    backend_techs.append("Python")
            elif "cargo.toml" in file.lower():
                if "Rust" not in backend_techs:
                    backend_techs.append("Rust")
        
        if backend_techs:
            technologies['backend'] = ", ".join(sorted(set(backend_techs)))
        
        # Frontend technologies
        frontend_techs = []
        frontend_files = tech_indicators.get("frontend", [])
        for file in frontend_files:
            if file.endswith(('.tsx', '.ts')):
                frontend_techs.append("TypeScript")
            elif file.endswith(('.jsx', '.js')):
                frontend_techs.append("JavaScript")
            elif file.endswith('.vue'):
                frontend_techs.append("Vue.js")
                
        # Check for React patterns
        if any('.tsx' in f or '.jsx' in f for f in frontend_files):
            frontend_techs.append("React")
            
        if frontend_techs:
            technologies['frontend'] = ", ".join(sorted(set(frontend_techs)))
        
        # AI technologies
        ai_techs = []
        ai_providers = summary.get("ai_integration", {}).get("providers", [])
        if ai_providers:
            ai_techs.extend(ai_providers)
            
        ai_files = tech_indicators.get("ai_integration", [])
        for file in ai_files:
            if "claude" in file.lower():
                ai_techs.append("Claude")
            elif "openai" in file.lower() or "gpt" in file.lower():
                ai_techs.append("OpenAI")
            elif "gemini" in file.lower():
                ai_techs.append("Google Gemini")
                
        if ai_techs:
            technologies['ai'] = ", ".join(sorted(set(ai_techs)))
        
        # Documentation technologies
        doc_techs = []
        doc_files = tech_indicators.get("documentation", [])
        if doc_files:
            if any('.md' in f for f in doc_files):
                doc_techs.append("Markdown")
            if any('readme' in f.lower() for f in doc_files):
                doc_techs.append("README")
            if any('changelog' in f.lower() for f in doc_files):
                doc_techs.append("Changelog")
                
        if doc_techs:
            technologies['documentation'] = ", ".join(sorted(set(doc_techs)))
        
        return technologies

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

    # REMOVED: _detect_entry_points - now handled in single-pass scan
    # Entry points are detected during the consolidated file traversal

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
            
            summary, scan_data = self._generate_optimized_summary(new_version)
            
            # Write main summary
            self.summary_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.summary_path, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2)
            
            # Missing breadcrumbs already collected in single-pass scan - use that data
            missing_breadcrumbs = scan_data['code_analysis']['missing_breadcrumbs']
            
            self._write_missing_breadcrumbs(
                missing_breadcrumbs,
                summary["code_analysis"]["total_functions"],
                summary["code_analysis"]["documented_functions"],
                summary["code_analysis"]["language_breakdown"]
            )
            
            # Generate architecture diagram
            architecture_diagram = self._generate_architecture_diagram(summary)
            architecture_path = self.paths['arkival_dir'] / "ARCHITECTURE_DIAGRAM.md"
            with open(architecture_path, 'w', encoding='utf-8') as f:
                f.write(architecture_diagram)
            
            # Generate markdown summary
            markdown_summary = self._generate_markdown_summary(summary)
            markdown_path = self.paths['arkival_dir'] / "CODEBASE_SUMMARY.md"
            with open(markdown_path, 'w', encoding='utf-8') as f:
                f.write(markdown_summary)
            
            # Update CONTRIBUTING.md metadata only (subdirectory mode only, when file exists)
            self._update_contributing_metadata_if_exists()
            
            print("✅ Enhanced project summary generated successfully")
            print(f"\n📊 PROJECT SUMMARY STATISTICS")
            print(f"Project: {summary['project_name']} v{summary['version']}")
            print(f"Total Files: {summary['project_structure']['total_files']}")
            print(f"Total Functions: {summary['code_analysis']['total_functions']}")
            print(f"Documentation Coverage: {summary['code_analysis']['coverage_percentage']}%")
            print(f"AI Providers: {len(summary['ai_integration']['providers'])}")
            
        except Exception as e:
            import traceback
            print(f"❌ Error generating summary: {e}")
            traceback.print_exc()
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