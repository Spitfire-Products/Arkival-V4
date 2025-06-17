
#!/usr/bin/env python3
"""
Enhanced Generic Project Summary Generator
Adaptable for any codebase with comprehensive workflow orchestration system
Enhanced with multi-language support, architecture analysis, components.json auto-updating, and WebSocket promise rejection mitigation support

Usage:
  python update_project_summary.py [options]

Options:
  --guide           Show breadcrumb guide
  --force           Force update even if no changes are detected
  --version         Show version information
  --fix-components  Enable automatic components.json path corrections
"""

import os
import sys
import json
import glob
import re
import shutil
import datetime
import logging
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Dict, Any, List

def get_current_version():
    """
    # @codebase-summary: Current version extraction and tracking system
    - Reads existing version from codebase_summary.json or defaults to 1.0.0
    - Handles file access errors gracefully with fallback version handling
    - Used by: version management, deployment tracking, changelog correlation
    """
    summary_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "codebase_summary.json")
    if os.path.exists(summary_file):
        try:
            with open(summary_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                current_version = data.get("version", "1.0.0")
                return current_version
        except Exception as e:
            logging.warning(f"Could not read current version: {e}")
    return "1.0.0"

def increment_version(current_version):
    """
    # @codebase-summary: Automated semantic version increment system
    - Increments patch version following semantic versioning standards
    - Handles malformed version strings with graceful fallback
    - Used by: automated deployment, changelog updates, version tracking
    """
    try:
        parts = current_version.split('.')
        if len(parts) >= 3:
            major, minor, patch = parts[0], parts[1], parts[2]
            new_patch = int(patch) + 1
            return f"{major}.{minor}.{new_patch}"
        else:
            return "1.0.1"
    except (ValueError, IndexError):
        return "1.0.1"

def correlate_with_changelog():
    """
    # @codebase-summary: Version correlation and synchronization system
    - Reads changelog version for cross-reference with codebase version
    - Provides version alignment validation and tracking capabilities
    - Used by: version management, deployment coordination, changelog correlation
    """
    changelog_file = "../changelog_summary.json"
    if os.path.exists(changelog_file):
        try:
            with open(changelog_file, 'r', encoding='utf-8') as f:
                changelog = json.load(f)
                return changelog.get("changelog_version")
        except Exception as e:
            logging.warning(f"Could not read changelog: {e}")
    return None

def archive_previous_version(current_version):
    """
    # @codebase-summary: Version archival and backup management system
    - Creates timestamped backups of codebase summaries before updates
    - Maintains version history in both root and history directories
    - Used by: version control, rollback capabilities, audit trail maintenance
    """
    summary_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "codebase_summary.json")
    if os.path.exists(summary_file):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        project_root = os.path.dirname(os.path.dirname(__file__))
        
        # Archive to history directory only
        history_dir = os.path.join(project_root, "codebase_summary", "history")
        if os.path.exists(history_dir):
            history_archive = os.path.join(history_dir, f"codebase_summary_v{current_version}_{timestamp}.json")
            try:
                shutil.copy2(summary_file, history_archive)
                logging.info(f"Archived previous version to {history_archive}")
            except Exception as e:
                logging.warning(f"Could not archive previous version: {e}")

def analyze_components_config():
    """
    # @codebase-summary: Component configuration analysis and validation system
    - Analyzes components.json structure and path validation
    - Tracks UI components count and configuration alignment
    - Used by: component management, path validation, configuration analysis
    """
    components_config_path = "../components.json"
    
    analysis = {
        "config_exists": False,
        "paths_valid": {},
        "missing_directories": [],
        "ui_components_count": 0,
        "alignment_status": "unknown"
    }
    
    try:
        if os.path.exists(components_config_path):
            analysis["config_exists"] = True
            
            with open(components_config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Validate paths
            css_path = config.get("tailwind", {}).get("css", "")
            tailwind_config = config.get("tailwind", {}).get("config", "")
            
            analysis["paths_valid"]["css"] = os.path.exists(f"../{css_path}") if css_path else False
            analysis["paths_valid"]["tailwind_config"] = os.path.exists(f"../{tailwind_config}") if tailwind_config else False
            
            # Check alias directories
            aliases = config.get("aliases", {})
            
            # Try common base paths for generic projects
            base_paths = ["../src", "../client/src", "../app", "../frontend/src"]
            detected_base = None
            
            for base_path in base_paths:
                if os.path.exists(base_path):
                    detected_base = base_path
                    break
            
            if detected_base:
                for alias, path in aliases.items():
                    if path.startswith("@/"):
                        actual_path = path.replace("@/", f"{detected_base}/")
                        if not os.path.exists(actual_path):
                            analysis["missing_directories"].append(actual_path)
                        else:
                            analysis["paths_valid"][alias] = True
            
            # Count UI components if ui directory exists
            if detected_base:
                ui_path = f"{detected_base}/components/ui"
                if os.path.exists(ui_path):
                    ui_files = [f for f in os.listdir(ui_path) if f.endswith(('.tsx', '.jsx', '.ts', '.js'))]
                    analysis["ui_components_count"] = len(ui_files)
            
            # Determine alignment status
            all_paths_valid = all(analysis["paths_valid"].values()) if analysis["paths_valid"] else False
            no_missing_dirs = len(analysis["missing_directories"]) == 0
            
            if all_paths_valid and no_missing_dirs:
                analysis["alignment_status"] = "perfect"
            elif all_paths_valid:
                analysis["alignment_status"] = "good"
            else:
                analysis["alignment_status"] = "needs_attention"
                
    except Exception as e:
        analysis["error"] = str(e)
    
    return analysis

def update_components_config_if_needed(codebase_version=None, enable_auto_fix=False):
    """
    # @codebase-summary: Components configuration synchronization and repair system
    - Updates components.json with correct paths and version synchronization
    - Provides automatic path detection and correction capabilities
    - Used by: shadcn/ui integration, configuration management, version correlation
    """
    analysis = analyze_components_config()
    
    if not analysis["config_exists"]:
        return False, "No components.json found"
    
    # Auto-fix common issues and update version (only if explicitly enabled)
    components_config_path = "../components.json"
    try:
        with open(components_config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        updated = False
        
        # Only fix paths if auto-fix is enabled and they're clearly broken
        if enable_auto_fix:
            # Try to detect correct paths
            css_candidates = ["src/index.css", "client/src/index.css", "app/globals.css", "styles/globals.css"]
            tailwind_candidates = ["tailwind.config.ts", "tailwind.config.js"]
            
            current_css = config.get("tailwind", {}).get("css", "")
            if current_css and not os.path.exists(f"../{current_css}"):
                for candidate in css_candidates:
                    if os.path.exists(f"../{candidate}"):
                        config.setdefault("tailwind", {})["css"] = candidate
                        updated = True
                        break
            
            current_tailwind = config.get("tailwind", {}).get("config", "")
            if current_tailwind and not os.path.exists(f"../{current_tailwind}"):
                for candidate in tailwind_candidates:
                    if os.path.exists(f"../{candidate}"):
                        config.setdefault("tailwind", {})["config"] = candidate
                        updated = True
                        break
        
        # Always update version to match codebase summary
        if codebase_version:
            current_version = config.get("version", "")
            if current_version != codebase_version:
                config["version"] = codebase_version
                config["last_updated"] = datetime.datetime.now().isoformat()
                updated = True
        
        if updated:
            with open(components_config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            
            if codebase_version:
                return True, f"Updated components.json (v{codebase_version})"
            else:
                return True, "Updated components.json paths"
        
        # Even if no path fixes needed, check if version sync is needed
        if codebase_version and config.get("version") != codebase_version:
            config["version"] = codebase_version
            config["last_updated"] = datetime.datetime.now().isoformat()
            with open(components_config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            return True, f"Synced components.json version to v{codebase_version}"
        
        return False, "Components config already aligned and version synced"
        
    except Exception as e:
        return False, f"Failed to update: {e}"

class EnhancedProjectSummaryGenerator:
    """
    # @codebase-summary: Core enhanced project analysis and documentation generator
    - Provides comprehensive codebase analysis with multi-language support
    - Generates detailed project summaries with architecture diagrams
    - Used by: workflow orchestration, agent handoffs, project documentation
    """
    def __init__(self):
        # Script is in codebase_summary/ folder, so project root is parent
        script_dir = Path(__file__).parent
        self.project_root = script_dir.parent
        self.summary_path = self.project_root / "codebase_summary.json"  # Output to project root
        self.config_path = self.project_root / "workflow_config.json"
        self.history_dir = script_dir / "history"

    def generate_summary(self, enable_fix_components=False):
        """
        # @codebase-summary: Main project summary generation orchestrator
        - Coordinates comprehensive codebase analysis and documentation generation
        - Integrates all enhanced features including AI detection and architecture analysis
        - Used by: workflow automation, manual summary updates, agent handoff preparation
        """
        print("🔍 ENHANCED PROJECT SUMMARY GENERATION")
        print("=" * 45)

        try:
            # Clean Python cache files first
            self._clean_python_cache()
            
            # Update .gitignore if needed
            self._update_gitignore()
            
            # Check for codebase changes (with force option)
            force_update = "--force" in sys.argv
            if not force_update and not self._check_for_changes():
                print("No codebase changes detected. Use --force to update anyway.")
                return

            # Load configuration with enhanced feature flags
            config = self._load_enhanced_config()

            # Get current version and increment if needed
            current_version = self._get_current_version()
            new_version = self._increment_version(current_version)

            # Archive previous version with enhanced metadata
            self._archive_previous_version(current_version)

            # Enhanced project structure analysis
            file_structure = self._scan_enhanced_project_structure()

            # Comprehensive code analysis with multi-language support
            code_analysis = self._analyze_code_files_enhanced()

            # Breadcrumb extraction with advanced patterns
            breadcrumbs, missing_breadcrumbs = self._extract_breadcrumbs_enhanced()

            # Enhanced documentation status
            documentation_status = self._check_documentation_enhanced()

            # Architecture analysis
            architecture_data = self._analyze_architecture()

            # AI integration detection
            ai_integrations = self._scan_ai_integrations()

            # Route analysis
            routes = self._scan_routes_enhanced()

            # Component analysis (if React/Vue project)
            components = self._scan_components_enhanced()
            
            # Components.json analysis and auto-update
            components_config = analyze_components_config()
            if components_config["config_exists"]:
                updated, message = update_components_config_if_needed(new_version, enable_fix_components)
                if updated:
                    print(f"📦 {message}")
                elif enable_fix_components:
                    print(f"📦 {message}")
            
            # Hooks analysis (if React project)
            hooks = self._scan_hooks_enhanced()

            # Database readiness assessment
            database_analysis = self._analyze_database_readiness()

            # Recent feature detection
            recent_features = self._detect_recent_features()

            # Performance metrics
            performance_metrics = self._calculate_performance_metrics(file_structure, code_analysis)

            # Calculate function statistics from file analysis data
            total_functions = 0
            documented_functions = 0
            
            for file_data in code_analysis.get("file_analysis", []):
                total_functions += file_data.get("function_count", 0)
                documented_functions += file_data.get("documented_count", 0)
            
            missing_count = total_functions - documented_functions
            
            # Add code analysis section with function statistics
            code_analysis['total_functions'] = total_functions
            code_analysis['documented_functions'] = documented_functions
            code_analysis['missing_count'] = missing_count
            code_analysis['coverage_percentage'] = (documented_functions / max(total_functions, 1)) * 100 if total_functions > 0 else 0.0

            # Create comprehensive summary
            summary = self._create_enhanced_summary(
                config, file_structure, code_analysis, breadcrumbs, 
                documentation_status, architecture_data, ai_integrations,
                routes, components, hooks, database_analysis, recent_features,
                performance_metrics, new_version, components_config
            )

            # Save enhanced summary
            self._save_summary(summary)

            # Generate enhanced reports
            self._generate_enhanced_reports(code_analysis, missing_breadcrumbs, breadcrumbs)

            # Generate markdown documentation
            if config.get("enhanced_features", {}).get("generate_markdown", True):
                self._generate_markdown_summary(summary, breadcrumbs)

            # Generate architecture diagrams
            if config.get("enhanced_features", {}).get("architecture_diagrams", True):
                self._generate_architecture_diagrams(summary)

            print("✅ Enhanced project summary generated successfully")
            self._print_enhanced_summary_stats(summary)

        except Exception as e:
            print(f"❌ Error generating enhanced summary: {e}")
            logging.error(f"Detailed error: {e}", exc_info=True)
            sys.exit(1)

    def _check_for_changes(self) -> bool:
        """Enhanced change detection with git integration"""
        # Git operations disabled for deployment environments to avoid lock issues
        # Use file modification time checking instead
        
        # Fallback: check file modification times
        try:
            if self.summary_path.exists():
                summary_time = self.summary_path.stat().st_mtime
                for root, dirs, files in os.walk(self.project_root):
                    dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
                    for file in files:
                        if file.endswith(('.py', '.js', '.ts', '.tsx', '.jsx', '.json', '.md')):
                            file_path = os.path.join(root, file)
                            if os.path.getmtime(file_path) > summary_time:
                                return True
            return True  # First run or no summary exists
        except:
            return True

    def _load_enhanced_config(self) -> Dict[str, Any]:
        """Load enhanced configuration with feature flags"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            except:
                config = {}
        else:
            config = {}

        # Enhanced default configuration with feature flags
        enhanced_defaults = {
            "project_name": "Arkival",
            "version": "1.0.0",
            "technology_stack": ["Generic"],
            "enhanced_features": {
                "architecture_diagrams": True,
                "ai_integration_detection": True,
                "multi_language_analysis": True,
                "component_analysis": True,
                "database_analysis": True,
                "route_analysis": True,
                "generate_markdown": True,
                "performance_metrics": True,
                "recent_feature_detection": True
            },
            "workflow_settings": {
                "auto_changelog": True,
                "auto_documentation": True,
                "agent_handoff_integration": True
            },
            "analysis_settings": {
                "max_file_size_mb": 5,
                "include_test_files": True,
                "breadcrumb_required_coverage": 80,
                "comprehensive_scanning": True
            }
        }

        # Merge user config with enhanced defaults
        for key, value in enhanced_defaults.items():
            if key not in config:
                config[key] = value
            elif isinstance(value, dict) and isinstance(config.get(key), dict):
                for subkey, subvalue in value.items():
                    if subkey not in config[key]:
                        config[key][subkey] = subvalue

        return config

    def _get_current_version(self) -> str:
        """Enhanced version management with correlation checking"""
        if self.summary_path.exists():
            try:
                with open(self.summary_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    current_version = data.get("version", "1.0.0")
                    # Reset to 1.1.0 for enhanced features if still on 1.0.x
                    if current_version.startswith("1.0."):
                        return "1.1.0"
                    return current_version
            except Exception as e:
                logging.warning(f"Could not read current version: {e}")
        return "1.1.0"

    def _increment_version(self, current_version: str) -> str:
        """Enhanced version increment with semantic versioning"""
        try:
            parts = current_version.split('.')
            if len(parts) == 3:
                major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
                return f"{major}.{minor}.{patch + 1}"
            else:
                return "1.1.1"
        except:
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
    
    def _clean_python_cache(self):
        """Clean Python cache files to reduce token load"""
        try:
            cache_count = 0
            pyc_count = 0
            
            # Find and remove __pycache__ directories
            for root, dirs, files in os.walk(self.project_root):
                if '__pycache__' in dirs:
                    cache_dir = os.path.join(root, '__pycache__')
                    try:
                        shutil.rmtree(cache_dir)
                        cache_count += 1
                    except Exception as e:
                        logging.warning(f"Failed to remove {cache_dir}: {e}")
                
                # Remove .pyc files
                for file in files:
                    if file.endswith('.pyc'):
                        pyc_path = os.path.join(root, file)
                        try:
                            os.unlink(pyc_path)
                            pyc_count += 1
                        except Exception as e:
                            logging.warning(f"Failed to remove {pyc_path}: {e}")
            
            if cache_count > 0 or pyc_count > 0:
                print(f"✅ Cleaned {cache_count} __pycache__ directories and {pyc_count} .pyc files")
        except Exception as e:
            logging.warning(f"Failed to clean Python cache: {e}")
    
    def _update_gitignore(self):
        """Update .gitignore with recommended entries for token optimization"""
        try:
            gitignore_path = self.project_root / '.gitignore'
            
            # Essential entries for token optimization
            essential_entries = [
                '# Python cache',
                '__pycache__/',
                '*.pyc',
                '*.pyo',
                '*.pyd',
                '.Python',
                '',
                '# Development artifacts',
                '.cache/',
                '.local/',
                '.pythonlibs/',
                '',
                '# IDE and editor files',
                '.vscode/',
                '.idea/',
                '*.swp',
                '*.swo',
                '*~',
                '',
                '# OS files',
                '.DS_Store',
                'Thumbs.db',
                '',
                '# Dependencies',
                'node_modules/',
                'venv/',
                'env/',
                '.env',
                '',
                '# Build outputs',
                'dist/',
                'build/',
                '*.egg-info/',
                '',
                '# History and logs',
                '*.log',
                'codebase_summary/history/',
                '',
                '# Test coverage',
                '.coverage',
                'htmlcov/',
                '.pytest_cache/',
                '',
                '# Agent state files',
                '.local/state/',
                'agent_state/',
                '',
                '# Temporary files',
                '*.tmp',
                '*.temp',
                '*.bak'
            ]
            
            # Read existing .gitignore
            existing_entries = set()
            if gitignore_path.exists():
                with open(gitignore_path, 'r', encoding='utf-8') as f:
                    existing_entries = set(line.strip() for line in f if line.strip() and not line.startswith('#'))
            
            # Find missing entries
            missing_entries = []
            for entry in essential_entries:
                if entry and not entry.startswith('#') and entry not in existing_entries:
                    missing_entries.append(entry)
            
            # Append missing entries if any
            if missing_entries:
                with open(gitignore_path, 'a', encoding='utf-8') as f:
                    if gitignore_path.stat().st_size > 0:
                        f.write('\n\n')
                    f.write('# Token optimization entries added by update_project_summary.py\n')
                    for entry in essential_entries:
                        if entry.startswith('#') or entry == '' or entry in missing_entries:
                            f.write(entry + '\n')
                
                print(f"✅ Updated .gitignore with {len(missing_entries)} optimization entries")
            
        except Exception as e:
            logging.warning(f"Failed to update .gitignore: {e}")

    def _scan_enhanced_project_structure(self) -> Dict[str, Any]:
        """Enhanced project structure analysis with technology detection"""
        structure = {
            "total_files": 0,
            "directories": [],
            "file_types": {},
            "key_files": [],
            "technology_indicators": {
                "frontend": [],
                "backend": [],
                "ai_integration": [],
                "database": [],
                "rust_integration": [],
                "deployment": [],
                "testing": [],
                "documentation": []
            }
        }

        # Comprehensive important files detection
        important_files = [
            "package.json", "requirements.txt", "Cargo.toml", "pom.xml", "go.mod",
            "README.md", "LICENSE", ".gitignore", ".replit",
            "main.py", "index.js", "app.py", "server.js", "main.go",
            "docker-compose.yml", "Dockerfile", "tsconfig.json", "vite.config.ts",
            "tailwind.config.ts", "drizzle.config.ts", "components.json",
            "poetry.lock", "yarn.lock", "package-lock.json"
        ]

        # Enhanced technology stack indicators
        tech_indicators = {
            "frontend": ["package.json", "vite.config.ts", "tailwind.config.ts", "components.json", 
                        "client/", "App.tsx", "src/components/", ".vue", "angular.json"],
            "backend": ["server/", "api/", "routes.ts", "index.ts", "storage.ts", "src/main.rs", 
                       "src/lib.rs", "app.py", "main.go", "server.js", "codebase_summary/", 
                       "setup_workflow_system.py", "validate_deployment.py", "agent_workflow_orchestrator.py"],
            "ai_integration": ["ai-service.ts", "openai-", "gemini-", "grok-", "llm-", 
                              "character-consistency", "deepseek", "claude", "AI_AGENT", 
                              "ai_integrations/", "CLAUDE_INTEGRATION", "anthropic", 
                              "workflow_assets/ai_integrations", "model_provider", "ai_api"],
            "database": ["drizzle.config.ts", "schema.ts", "prisma/", ".sql", "storage.ts", 
                        "Cargo.toml", "src/schema.rs", "src/models.rs", "migrations/", 
                        "diesel.toml", "alembic/", "database.py"],
            "rust_integration": ["Cargo.toml", ".rs", "src/", "diesel.toml", "rust-toolchain.toml"],
            "deployment": [".replit", "Dockerfile", "vercel.json", "netlify.toml", 
                          "railway.json", "render.yaml"],
            "testing": ["tests/", "test-", ".test.", ".spec.", "jest.config", 
                       "src/tests/", "cypress/", "playwright.config"],
            "documentation": ["README.md", "DEVELOPER_ONBOARDING.md", "codebase_summary/", 
                             ".md", "docs/", "ARCHITECTURE"]
        }

        # Enhanced ignore patterns
        ignore_dirs = [
            'node_modules', '__pycache__', 'dist', 'build', '.git',
            'coverage', '.next', '.vscode', '.idea', 'workflow_export_package',
            'attached_assets', 'reference_assets', 'documentation_assets', '.cache', '.local',
            'codebase_summary/history', 'codebase_summary/language_scan_tests', '.pythonlibs'
        ]

        # Binary file extensions to exclude
        binary_extensions = {
            '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.webp',
            '.mp4', '.avi', '.mov', '.mkv', '.pdf', '.zip', '.tar', '.gz',
            '.woff', '.woff2', '.ttf', '.eot', '.otf'
        }

        for root, dirs, files in os.walk(self.project_root):
            # Enhanced directory filtering
            dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.endswith('_assets')]

            rel_root = os.path.relpath(root, self.project_root)
            
            # Skip history, test, documentation, and dependency directories completely
            if any(skip_path in rel_root for skip_path in ['history', 'language_scan_tests', 'documentation_assets', 'attached_assets', 'reference_assets', '.pythonlibs']):
                continue

            if rel_root != '.' and not any(ignore_dir in rel_root for ignore_dir in ignore_dirs):
                structure["directories"].append(rel_root)

            for file in files:
                # Skip hidden files and binary files
                if file.startswith('.') and file not in ['.replit', '.gitignore', '.env.example']:
                    continue

                ext = Path(file).suffix.lower()
                if ext in binary_extensions:
                    continue

                # Skip large lock files but count other files
                if file in ['package-lock.json', 'yarn.lock', 'pnpm-lock.yaml'] and os.path.getsize(os.path.join(root, file)) > 1024 * 1024:
                    continue

                structure["total_files"] += 1
                structure["file_types"][ext] = structure["file_types"].get(ext, 0) + 1

                # Check for important files
                if file in important_files:
                    structure["key_files"].append(os.path.join(rel_root, file) if rel_root != '.' else file)

                # Enhanced technology indicators detection - exclude history files
                full_path = os.path.join(rel_root, file) if rel_root != '.' else file
                
                # Skip history JSON files from backend classification
                if 'history/' in full_path and full_path.endswith('.json'):
                    continue
                    
                for tech, indicators in tech_indicators.items():
                    for indicator in indicators:
                        if indicator in full_path or indicator in file:
                            # Only add Python files to backend, not all JSON files
                            if tech == "backend" and full_path.endswith('.json') and 'history/' in full_path:
                                continue
                            if full_path not in structure["technology_indicators"][tech]:
                                structure["technology_indicators"][tech].append(full_path)

        return structure

    def _analyze_code_files_enhanced(self) -> Dict[str, Any]:
        """Enhanced code analysis with multi-language support"""
        analysis = {
            "total_functions": 0,
            "documented_functions": 0,
            "missing_breadcrumbs": [],
            "file_analysis": [],
            "language_breakdown": {},
            "complexity_metrics": {}
        }

        # Enhanced code file extensions - broad spectrum for different codebase types
        code_extensions = ['.py', '.js', '.ts', '.tsx', '.jsx', '.go', '.rs', 
                          '.java', '.cpp', '.c', '.h', '.php', '.rb', '.swift',
                          '.kt', '.scala', '.clj', '.dart', '.lua', '.r', '.m',
                          '.css', '.scss', '.sass', '.sql', '.vue', '.cs', '.sh', '.ps1']

        # Exclude build artifacts and cache directories but include actual code
        ignore_dirs = [
            'node_modules', '__pycache__', 'dist', 'build', 
            'workflow_export_package', 'attached_assets', 'reference_assets', 
            'documentation_assets', 'history',
            'migration_utilities_assets', 'function_tests_assets', 'analysis_scripts_assets', 
            'checkpoints', 'workflow_export_package_backup', '.config', '.git', '.vscode', 
            '.idea', '.cache', '.local', '.pythonlibs'
        ]

        for root, dirs, files in os.walk(self.project_root):
            dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.endswith('_assets')]
            
            # Skip specific paths completely
            rel_root = os.path.relpath(root, self.project_root)
            if any(skip_path in rel_root for skip_path in ['history', 'documentation_assets', 'attached_assets', 'reference_assets', '.pythonlibs']):
                continue

            for file in files:
                if any(file.endswith(ext) for ext in code_extensions):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, self.project_root)

                    # Check file size limits
                    try:
                        file_size = os.path.getsize(file_path)
                        if file_size > 5 * 1024 * 1024:  # 5MB limit
                            continue
                    except:
                        continue

                    file_info = self._analyze_code_file_enhanced(file_path, rel_path)
                    if file_info:
                        analysis["file_analysis"].append(file_info)
                        analysis["total_functions"] += file_info["function_count"]
                        analysis["documented_functions"] += file_info["documented_count"]

                        # Language breakdown
                        ext = Path(file).suffix.lower()
                        if ext not in analysis["language_breakdown"]:
                            analysis["language_breakdown"][ext] = {"files": 0, "functions": 0}
                        analysis["language_breakdown"][ext]["files"] += 1
                        analysis["language_breakdown"][ext]["functions"] += file_info["function_count"]

                        if file_info["missing_breadcrumbs"]:
                            analysis["missing_breadcrumbs"].append({
                                "file": rel_path,
                                "missing": file_info["missing_breadcrumbs"]
                            })

        return analysis

    def _analyze_code_file_enhanced(self, file_path: str, rel_path: str) -> Dict[str, Any]:
        """Enhanced individual file analysis with better patterns"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            if len(content) == 0:
                return {}

            # Enhanced function detection patterns by language
            function_patterns = {
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
                    # Methods - must have return type followed by method name and parentheses
                    r'(?:public\s+|private\s+|protected\s+|internal\s+)?(?:static\s+)?(?:virtual\s+)?(?:override\s+)?(?:async\s+)?(?:abstract\s+)?(?:void|Task(?:<[^>]+>)?|string|int|bool|double|float|decimal|char|byte|short|long|object|var|I?[A-Z]\w*(?:<[^>]+>)?)\s+([A-Z][a-zA-Z0-9_]*)\s*\([^)]*\)',
                    r'(?:public\s+|private\s+|protected\s+|internal\s+)?(?:static\s+)?(?:virtual\s+)?(?:override\s+)?(?:async\s+)?(?:abstract\s+)?(?:void|Task(?:<[^>]+>)?|string|int|bool|double|float|decimal|char|byte|short|long|object|var|I?[A-Z]\w*(?:<[^>]+>)?)\s+([a-z][a-zA-Z0-9_]*)\s*\([^)]*\)',
                    # Constructors (same name as class)
                    r'^\s*(?:public\s+|private\s+|protected\s+|internal\s+)?([A-Z]\w*)\s*\([^)]*\)\s*(?::\s*(?:base|this)\s*\([^)]*\))?\s*\{',
                    # Destructors
                    r'~([A-Z]\w*)\s*\(\s*\)',
                    # Generic methods with angle brackets before parentheses
                    r'(?:public\s+|private\s+|protected\s+|internal\s+)?(?:static\s+)?(?:\w+\s+)?([A-Z][a-zA-Z0-9_]*)<[^>]+>\s*\([^)]*\)',
                    r'(?:public\s+|private\s+|protected\s+|internal\s+)?(?:static\s+)?(?:\w+\s+)?([a-z][a-zA-Z0-9_]*)<[^>]+>\s*\([^)]*\)',
                    # Extension methods (this keyword as first parameter)
                    r'(?:public\s+)?(?:static\s+)(?:\w+\s+)([A-Z][a-zA-Z0-9_]*)\s*\(\s*this\s+',
                    r'(?:public\s+)?(?:static\s+)(?:\w+\s+)([a-z][a-zA-Z0-9_]*)\s*\(\s*this\s+',
                    # Properties (get/set pattern)
                    r'(?:public\s+|private\s+|protected\s+|internal\s+)?(?:static\s+)?(?:virtual\s+)?(?:override\s+)?(?:\w+\s+)([A-Z][a-zA-Z0-9_]*)\s*\{\s*(?:get|set)',
                    # Expression-bodied members with =>
                    r'(?:public\s+|private\s+|protected\s+|internal\s+)?(?:\w+\s+)([A-Z][a-zA-Z0-9_]*)\s*=>\s*',
                    r'(?:public\s+|private\s+|protected\s+|internal\s+)?(?:\w+\s+)([a-z][a-zA-Z0-9_]*)\s*=>\s*',
                    # Local functions (simpler pattern)
                    r'^\s{4,}(?:async\s+)?(?:\w+\s+)([A-Z][a-zA-Z0-9_]*)\s*\([^)]*\)\s*(?:\{|=>)',
                    r'^\s{4,}(?:async\s+)?(?:\w+\s+)([a-z][a-zA-Z0-9_]*)\s*\([^)]*\)\s*(?:\{|=>)',
                    # Classes, interfaces, structs, enums, records
                    r'(?:public\s+|private\s+|protected\s+|internal\s+)?(?:abstract\s+|sealed\s+|static\s+)?(?:partial\s+)?class\s+([A-Z]\w*)',
                    r'(?:public\s+|private\s+|protected\s+|internal\s+)?(?:partial\s+)?interface\s+([A-Z]\w*)',
                    r'(?:public\s+|private\s+|protected\s+|internal\s+)?(?:readonly\s+)?struct\s+([A-Z]\w*)',
                    r'(?:public\s+|private\s+|protected\s+|internal\s+)?enum\s+([A-Z]\w*)',
                    r'(?:public\s+|private\s+|protected\s+|internal\s+)?record\s+([A-Z]\w*)',
                    # Delegates
                    r'(?:public\s+|private\s+|protected\s+|internal\s+)?delegate\s+(?:\w+\s+)([A-Z][a-zA-Z0-9_]*)\s*\(',
                    # Events
                    r'(?:public\s+|private\s+|protected\s+|internal\s+)?(?:static\s+)?event\s+(?:\w+\s+)([A-Z][a-zA-Z0-9_]*)',
                    # Indexers special handling
                    r'this\s*\[\s*(?:int|string)',
                    # Operators
                    r'operator\s+([+\-*/=!<>]+|==|!=|true|false)\s*\('
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

            # Detect language from file extension
            ext = Path(file_path).suffix.lower()
            if ext in ['.py']:
                patterns = function_patterns['python']
            elif ext in ['.js', '.jsx', '.ts', '.tsx']:
                patterns = function_patterns['javascript']
            elif ext in ['.rs']:
                patterns = function_patterns['rust']
            elif ext in ['.c', '.h']:
                patterns = function_patterns['c']
            elif ext in ['.cpp', '.cc', '.cxx', '.hpp']:
                patterns = function_patterns['cpp']
            elif ext in ['.java']:
                patterns = function_patterns['java']
            elif ext in ['.go']:
                patterns = function_patterns['go']
            elif ext in ['.swift']:
                patterns = function_patterns['swift']
            elif ext in ['.kt', '.kts']:
                patterns = function_patterns['kotlin']
            elif ext in ['.php']:
                patterns = function_patterns['php']
            elif ext in ['.rb']:
                patterns = function_patterns['ruby']
            elif ext in ['.dart']:
                patterns = function_patterns['dart']
            elif ext in ['.sql']:
                patterns = function_patterns['sql']
            elif ext in ['.css', '.scss', '.sass']:
                patterns = function_patterns['css']
            elif ext in ['.vue']:
                patterns = function_patterns['vue']
            elif ext in ['.lua']:
                patterns = function_patterns['lua']
            elif ext in ['.scala']:
                patterns = function_patterns['scala']
            elif ext in ['.clj', '.cljs']:
                patterns = function_patterns['clojure']
            elif ext in ['.r']:
                patterns = function_patterns['r']
            elif ext in ['.m', '.mm']:
                patterns = function_patterns['objc']
            elif ext in ['.cs']:
                patterns = function_patterns['csharp']
            elif ext in ['.sh', '.bash']:
                patterns = function_patterns['shell']
            elif ext in ['.ps1']:
                patterns = function_patterns['powershell']
            else:
                patterns = function_patterns['javascript']  # Default fallback

            functions = []
            documented_functions = []
            lines = content.split('\n')

            for i, line in enumerate(lines):
                for pattern in patterns:
                    matches = re.findall(pattern, line)
                    for match in matches:
                        if match and not match.startswith('_'):
                            functions.append(match)

                            # Enhanced breadcrumb detection - check more lines before function
                            breadcrumb_found = False
                            for j in range(max(0, i-10), min(len(lines), i+3)):
                                if any(marker in lines[j] for marker in [
                                    '@codebase-summary:', '// @codebase-summary:', 
                                    '# @codebase-summary:', '/* @codebase-summary:',
                                    '-- @codebase-summary:', '* @codebase-summary:'
                                ]):
                                    breadcrumb_found = True
                                    break

                            if breadcrumb_found:
                                documented_functions.append(match)

            missing_breadcrumbs = [func for func in functions if func not in documented_functions]

            return {
                "file": rel_path,
                "language": ext,
                "function_count": len(functions),
                "documented_count": len(documented_functions),
                "functions": functions[:15],  # Limit for output
                "missing_breadcrumbs": missing_breadcrumbs[:15],  # Limit for output
                "lines_of_code": len(lines)
            }

        except Exception as e:
            logging.warning(f"Error analyzing {rel_path}: {e}")
            return {}

    def _extract_breadcrumbs_enhanced(self):
        """Enhanced breadcrumb extraction with multi-language support"""
        breadcrumbs = []
        missing_breadcrumbs = []

        # Get architecture files for analysis
        files = self._get_architecture_files()

        # Standard comment patterns for breadcrumb detection
        comment_patterns = {
            'single_line': [
                r'// @codebase-summary:(.*)',    # JavaScript/TypeScript/C/C++/Java/Swift/Kotlin/Dart
                r'# @codebase-summary:(.*)',     # Python/Ruby/Perl/Shell/YAML/R
                r'-- @codebase-summary:(.*)',    # SQL/PostgreSQL/Haskell/Ada
                r'/// @codebase-summary:(.*)',   # Rust documentation comments
                r'; @codebase-summary:(.*)',     # Lisp/Clojure/Assembly
                r'% @codebase-summary:(.*)',     # Erlang/Elixir/MATLAB/Prolog
                r'" @codebase-summary:(.*)',     # VimScript/Batch
            ],
            'multi_line': [
                r'/\* @codebase-summary:(.*?)\*/',             # JavaScript/TypeScript/C/C++/Java/CSS
                r'""" @codebase-summary:(.*?)"""',             # Python docstring
                r'=begin @codebase-summary:(.*?)=end',         # Ruby block comments
                r'<!--\s*@codebase-summary:(.*?)-->',          # HTML/XML/Markdown
                r'/\*\* @codebase-summary:(.*?)\*/',           # JSDoc/JavaDoc style
                r'#\[ @codebase-summary:(.*?)\]',              # Rust attributes
            ]
        }

        for file in files:
            try:
                # Binary file detection
                try:
                    with open(file, 'rb') as f:
                        sample = f.read(1024)
                        if b'\x00' in sample:
                            continue
                except:
                    continue

                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                if len(content) == 0 or len(content) > 500000:
                    continue

                # Extract breadcrumbs using standard patterns
                breadcrumb_found = False
                for pattern_type, patterns in comment_patterns.items():
                    for pattern in patterns:
                        matches = re.findall(pattern, content, re.DOTALL if pattern_type == 'multi_line' else 0)
                        if matches:
                            breadcrumb_found = True
                            for match in matches:
                                parts = [part.strip() for part in match.replace('\n', ' ').split('=')]
                                data = {}
                                for i in range(0, len(parts), 2):
                                    if i + 1 < len(parts):
                                        data[parts[i]] = parts[i + 1].strip('"').strip("'")
                                breadcrumbs.append({
                                    'file': file,
                                    'data': data
                                })

            except Exception as e:
                logging.warning(f"Skipping problematic file {file}: {e}")

        return breadcrumbs, missing_breadcrumbs

    def _get_architecture_files(self):
        """Enhanced file collection with better filtering"""
        arch_files = []
        project_root = self.project_root

        # Enhanced core directories
        core_directories = [
            'server', 'client/src', 'src', 'lib', 'api',
            'shared', 'codebase_summary', 'tests', 'test',
            'components', 'pages', 'hooks', 'utils'
        ]

        # Enhanced relevant extensions for multi-language codebases
        relevant_extensions = [
            '.ts', '.tsx', '.js', '.jsx', '.py', '.go', '.rs', '.java', '.cpp', '.c', '.h',
            '.php', '.rb', '.swift', '.kt', '.scala', '.clj', '.dart', '.lua', '.r', '.m',
            '.sql', '.sh', '.ps1', '.bat'
        ]

        # Binary extensions to exclude
        binary_extensions = {
            '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.webp', '.bmp', '.tiff',
            '.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv',
            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
            '.zip', '.tar', '.gz', '.rar', '.7z',
            '.woff', '.woff2', '.ttf', '.eot', '.otf'
        }

        # Files to exclude (including documentation and reports)
        exclude_files = {
            'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml', 'poetry.lock',
            '.DS_Store', 'Thumbs.db', '.env', '.env.local', '.env.production'
        }
        
        # Documentation file patterns to exclude
        exclude_patterns = [
            '.md', '.txt', '.rst', '.pdf', '.doc', '.docx',
            '_REPORT.md', '_GUIDE.md', '_SUMMARY.md', '_CHECKLIST.md',
            'README', 'CHANGELOG', 'LICENSE', 'CONTRIBUTING'
        ]

        # Directories to skip
        skip_directories = {
            'node_modules', '__pycache__', '.git', 'dist', 'build', 
            'coverage', '.next', '.vscode', '.idea', 'workflow_export_package',
            '.cache', '.local', 'history'
        }

        # Important root files
        important_root_files = [
            'package.json', 'tsconfig.json', 'vite.config.ts', 'tailwind.config.ts',
            'drizzle.config.ts', 'components.json', 'postcss.config.js',
            '.replit', '.gitignore', 'README.md', 'Cargo.toml', 'go.mod'
        ]

        # Add important root files
        for file in important_root_files:
            file_path = project_root / file
            if file_path.exists():
                arch_files.append(str(file_path))

        # Scan core directories
        for core_dir in core_directories:
            core_path = project_root / core_dir
            if not core_path.exists():
                continue

            for root, dirs, files in os.walk(core_path):
                dirs[:] = [d for d in dirs if d not in skip_directories and not d.endswith('_assets')]

                for file in files:
                    if file in exclude_files:
                        continue

                    file_ext = Path(file).suffix.lower()
                    if file_ext in binary_extensions:
                        continue
                    
                    # Skip documentation files
                    if any(pattern in file_ext for pattern in exclude_patterns):
                        continue
                    
                    # Skip report and documentation files by name patterns
                    if any(pattern in file.upper() for pattern in ['_REPORT', '_GUIDE', '_SUMMARY', '_CHECKLIST', 'README', 'CHANGELOG']):
                        continue

                    if file_ext in relevant_extensions or file_ext == '':
                        file_path = os.path.join(root, file)

                        try:
                            file_size = os.path.getsize(file_path)
                            size_limit = 5 * 1024 * 1024 if file_ext in ['.md', '.json', '.py', '.ts', '.tsx', '.js', '.jsx'] else 1024 * 1024

                            if file_size > size_limit:
                                continue
                        except:
                            continue

                        arch_files.append(file_path)

        logging.info(f"Found {len(arch_files)} files for enhanced analysis")
        return arch_files

    def _check_documentation_enhanced(self) -> Dict[str, Any]:
        """Enhanced documentation status check"""
        docs = {
            "readme_exists": False,
            "changelog_exists": False,
            "architecture_docs": [],
            "workflow_files": [],
            "api_documentation": [],
            "deployment_guides": []
        }

        project_root = self.project_root

        # Check for README
        readme_files = ['README.md', 'README.txt', 'README.rst']
        for readme in readme_files:
            if (project_root / readme).exists():
                docs["readme_exists"] = True
                break

        # Check for changelog
        if (project_root / "changelog_summary.json").exists():
            docs["changelog_exists"] = True

        # Enhanced documentation categorization
        doc_categories = {
            "architecture_docs": ["ARCHITECTURE", "DESIGN", "STRUCTURE"],
            "api_documentation": ["API", "ENDPOINTS", "SWAGGER", "OPENAPI"],
            "deployment_guides": ["DEPLOY", "SETUP", "INSTALL", "DOCKER"]
        }

        for pattern in ['*.md', '*.txt', '*.rst']:
            for file in glob.glob(str(project_root / pattern)):
                rel_path = os.path.relpath(file, project_root)
                for category, keywords in doc_categories.items():
                    if any(keyword in rel_path.upper() for keyword in keywords):
                        docs[category].append(rel_path)

        # Enhanced workflow files check
        workflow_files = [
            "codebase_summary/agent_workflow_orchestrator.py",
            "codebase_summary/update_changelog.py",
            "codebase_summary/update_project_summary.py",
            "NEW_AGENT_GREETING.md",
            ".replit"
        ]

        for file in workflow_files:
            if (project_root / file).exists():
                docs["workflow_files"].append(file)

        return docs

    def _analyze_architecture(self) -> Dict[str, Any]:
        """Analyze project architecture and generate insights"""
        architecture = {
            "layers": [],
            "patterns": [],
            "dependencies": {},
            "complexity_score": 0
        }

        # Detect architectural patterns
        if (self.project_root / "client").exists() and (self.project_root / "server").exists():
            architecture["patterns"].append("Client-Server Separation")
            architecture["layers"].extend(["Frontend", "Backend"])

        if (self.project_root / "shared").exists():
            architecture["patterns"].append("Shared Schema Layer")
            architecture["layers"].append("Shared")

        # Check for common architectural patterns
        patterns_to_check = {
            "MVC": ["models", "views", "controllers"],
            "Component-Based": ["components", "hooks", "pages"],
            "Microservices": ["services", "api", "gateway"],
            "Layered": ["data", "business", "presentation"]
        }

        for pattern, indicators in patterns_to_check.items():
            if any((self.project_root / indicator).exists() for indicator in indicators):
                architecture["patterns"].append(pattern)

        return architecture

    def _scan_ai_integrations(self) -> Dict[str, Any]:
        """Enhanced AI integration scanning"""
        ai_services = {
            "providers": set(),
            "capabilities": set(),
            "integration_files": []
        }

        # Find AI-related files
        for root, dirs, files in os.walk(self.project_root):
            dirs[:] = [d for d in dirs if d not in ['node_modules', '__pycache__', '.git', 'dist', 'build', '.cache', '.local', 'history', '.pythonlibs']]

            for file in files:
                if file.endswith(('.ts', '.tsx', '.js', '.jsx', '.py')):
                    if any(keyword in file.lower() for keyword in ['ai', 'llm', 'openai', 'gemini', 'grok', 'claude', 'deepseek']):
                        ai_services["integration_files"].append(os.path.join(root, file))

        # Analyze AI integrations
        for file_path in ai_services["integration_files"]:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().lower()

                # Detect providers
                provider_indicators = {
                    'OpenAI': ['openai', 'gpt-', 'dall-e'],
                    'Gemini': ['gemini', 'google.generativeai'],
                    'Grok': ['grok', 'x-ai'],
                    'Claude': ['claude', 'anthropic'],
                    'DeepSeek': ['deepseek']
                }

                for provider, indicators in provider_indicators.items():
                    if any(indicator in content for indicator in indicators):
                        ai_services["providers"].add(provider)

                # Detect capabilities
                capability_indicators = {
                    'Text Generation': ['completion', 'chat', 'generate'],
                    'Image Generation': ['dall-e', 'image', 'picture'],
                    'Video Generation': ['video', 'veo'],
                    '3D Generation': ['3d', 'world', 'scene']
                }

                for capability, indicators in capability_indicators.items():
                    if any(indicator in content for indicator in indicators):
                        ai_services["capabilities"].add(capability)

            except Exception as e:
                logging.warning(f"Error reading AI file {file_path}: {e}")

        return {
            "providers": list(ai_services["providers"]),
            "capabilities": list(ai_services["capabilities"]),
            "integration_files": ai_services["integration_files"]
        }

    def _scan_routes_enhanced(self) -> List[Dict[str, Any]]:
        """Enhanced route scanning with better detection"""
        routes = []
        
        # Common route files
        route_files = [
            "routes.ts", "routes.js", "index.ts", "index.js", "app.py", "main.py",
            "server/routes.ts", "server/index.ts", "api/routes.js"
        ]

        for routes_file in route_files:
            route_path = self.project_root / routes_file
            if not route_path.exists():
                continue

            try:
                with open(route_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Enhanced route detection patterns
                route_patterns = [
                    r'router\.(get|post|put|delete|patch)\s*\(\s*[\'"]([^\'"]+)[\'"]',
                    r'app\.(get|post|put|delete|patch)\s*\(\s*[\'"]([^\'"]+)[\'"]',
                    r'\.route\s*\(\s*[\'"]([^\'"]+)[\'"]',
                    r'@(Get|Post|Put|Delete|Patch)\s*\(\s*[\'"]([^\'"]+)[\'"]',
                    r'@app\.(get|post|put|delete|patch)\s*\(\s*[\'"]([^\'"]+)[\'"]'
                ]

                for pattern in route_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    for match in matches:
                        if len(match) == 2:
                            method, path = match
                        else:
                            method, path = "GET", match[0]

                        routes.append({
                            "method": method.upper(),
                            "path": path,
                            "file": str(route_path),
                            "description": self._extract_route_description(content, path)
                        })

            except Exception as e:
                logging.error(f"Error scanning routes in {routes_file}: {e}")

        return routes

    def _extract_route_description(self, content: str, path: str) -> str:
        """Extract route description from comments"""
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if path in line:
                # Look for comments above the route
                for j in range(max(0, i-3), i):
                    if '//' in lines[j] or '/*' in lines[j] or '#' in lines[j]:
                        return lines[j].strip()
        return ""

    def _scan_components_enhanced(self) -> List[Dict[str, Any]]:
        """Enhanced component scanning for React/Vue projects"""
        components = []
        
        # Component directories
        component_dirs = [
            "components", "src/components", "client/src/components",
            "pages", "src/pages", "client/src/pages"
        ]

        for comp_dir in component_dirs:
            comp_path = self.project_root / comp_dir
            if not comp_path.exists():
                continue

            for root, dirs, files in os.walk(comp_path):
                for file in files:
                    if file.endswith(('.tsx', '.ts', '.jsx', '.js', '.vue')):
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, self.project_root)

                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()

                            # Enhanced component detection
                            component_patterns = [
                                r'export\s+default\s+function\s+(\w+)',
                                r'export\s+function\s+(\w+)',
                                r'const\s+(\w+)\s*=.*?React\.FC',
                                r'const\s+(\w+)\s*:\s*React\.FC',
                                r'const\s+(\w+)\s*=.*?=>'
                            ]

                            # Extract props
                            props_pattern = r'interface\s+(\w+Props)\s*{([^}]+)}'
                            props_matches = re.findall(props_pattern, content, re.DOTALL)
                            props_info = {match[0]: match[1].strip() for match in props_matches}

                            for pattern in component_patterns:
                                matches = re.findall(pattern, content)
                                for match in matches:
                                    component_type = self._classify_component(file_path, match)
                                    
                                    components.append({
                                        "name": match,
                                        "file": rel_path,
                                        "type": component_type,
                                        "props": props_info.get(f"{match}Props")
                                    })

                        except Exception as e:
                            logging.warning(f"Error reading component file {file_path}: {e}")

        return components

    def _classify_component(self, file_path: str, component_name: str) -> str:
        """Classify component type based on patterns"""
        if "pages" in file_path or "page" in file_path.lower():
            return "page"
        elif "modal" in component_name.lower():
            return "modal"
        elif component_name.startswith("use") or "Hook" in component_name:
            return "hook"
        else:
            return "component"

    def _scan_hooks_enhanced(self) -> List[Dict[str, Any]]:
        """Enhanced hooks scanning for React projects"""
        hooks = []
        
        # Hook directories
        hook_dirs = ["hooks", "src/hooks", "client/src/hooks", "components"]

        for hook_dir in hook_dirs:
            hook_path = self.project_root / hook_dir
            if not hook_path.exists():
                continue

            for root, dirs, files in os.walk(hook_path):
                for file in files:
                    if file.endswith(('.tsx', '.ts', '.jsx', '.js')):
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, self.project_root)

                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()

                            # Enhanced hook detection
                            hook_patterns = [
                                r'export\s+(?:const\s+|function\s+)?(use\w+)',
                                r'const\s+(use\w+)\s*=',
                                r'function\s+(use\w+)'
                            ]

                            for pattern in hook_patterns:
                                hook_matches = re.findall(pattern, content)
                                for hook_name in hook_matches:
                                    # Extract dependencies
                                    deps = self._extract_hook_dependencies(content, hook_name)
                                    
                                    hooks.append({
                                        "name": hook_name,
                                        "file": rel_path,
                                        "dependencies": deps
                                    })

                        except Exception as e:
                            logging.warning(f"Error reading hook file {file_path}: {e}")

        return hooks

    def _extract_hook_dependencies(self, content: str, hook_name: str) -> List[str]:
        """Extract hook dependencies from content"""
        deps_pattern = r'(useState|useEffect|useMemo|useCallback|useQuery|useMutation|useContext)'
        dependencies = re.findall(deps_pattern, content)
        return list(set(dependencies))

    def _analyze_database_readiness(self) -> Dict[str, Any]:
        """Analyze database integration readiness"""
        db_analysis = {
            "database_type": "unknown",
            "orm_detected": False,
            "schema_files": [],
            "migration_files": [],
            "readiness_score": 0
        }

        # Check for database indicators
        db_indicators = {
            "PostgreSQL": ["pg", "postgres", "drizzle", "schema.ts"],
            "SQLite": ["sqlite", ".db", "database.sqlite"],
            "MySQL": ["mysql", "mysql2"],
            "MongoDB": ["mongodb", "mongoose"]
        }

        # Check for ORM/Schema files
        schema_patterns = ["schema.ts", "models.py", "schema.sql", "drizzle.config.ts"]
        for pattern in schema_patterns:
            for file in glob.glob(str(self.project_root / "**" / pattern), recursive=True):
                db_analysis["schema_files"].append(os.path.relpath(file, self.project_root))
                db_analysis["orm_detected"] = True

        # Check for migrations
        migration_dirs = ["migrations", "alembic", "prisma/migrations"]
        for migration_dir in migration_dirs:
            migration_path = self.project_root / migration_dir
            if migration_path.exists():
                db_analysis["migration_files"].extend([
                    str(f) for f in migration_path.glob("*") if f.is_file()
                ])

        # Calculate readiness score
        score = 0
        if db_analysis["orm_detected"]:
            score += 40
        if db_analysis["schema_files"]:
            score += 30
        if db_analysis["migration_files"]:
            score += 30

        db_analysis["readiness_score"] = score

        return db_analysis

    def _detect_recent_features(self) -> Dict[str, Any]:
        """Detect recent features and changes"""
        recent_features = {
            "git_changes": [],
            "new_files": [],
            "modified_files": [],
            "feature_flags": []
        }

        # Git operations disabled for deployment environments to avoid lock issues
        try:
            # Detect new files by checking creation time
            import time
            current_time = time.time()
            one_day_ago = current_time - (24 * 60 * 60)
            
            for root, dirs, files in os.walk(self.project_root):
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        if os.path.getctime(file_path) > one_day_ago:
                            recent_features["new_files"].append(os.path.relpath(file_path, self.project_root))
                    except:
                        pass
        except:
            pass

        return recent_features

    def _calculate_performance_metrics(self, structure: Dict[str, Any], 
                                     analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate performance and complexity metrics"""
        metrics = {
            "file_count": structure["total_files"],
            "directory_count": len(structure["directories"]),
            "function_density": 0,
            "documentation_coverage": 0,
            "complexity_score": "medium"
        }

        if structure["total_files"] > 0:
            metrics["function_density"] = analysis["total_functions"] / structure["total_files"]

        if analysis["total_functions"] > 0:
            metrics["documentation_coverage"] = (analysis["documented_functions"] / analysis["total_functions"]) * 100

        # Calculate complexity score
        if structure["total_files"] > 100 or analysis["total_functions"] > 500:
            metrics["complexity_score"] = "high"
        elif structure["total_files"] < 20 or analysis["total_functions"] < 50:
            metrics["complexity_score"] = "low"

        return metrics

    def _create_enhanced_summary(self, config: Dict[str, Any], structure: Dict[str, Any], 
                               analysis: Dict[str, Any], breadcrumbs: List[Dict[str, Any]],
                               docs: Dict[str, Any], architecture: Dict[str, Any],
                               ai_integrations: Dict[str, Any], routes: List[Dict[str, Any]],
                               components: List[Dict[str, Any]], hooks: List[Dict[str, Any]],
                               database: Dict[str, Any], recent_features: Dict[str, Any],
                               performance: Dict[str, Any], version: str, 
                               components_config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create comprehensive enhanced summary"""
        
        # Group breadcrumbs by feature
        grouped_breadcrumbs = defaultdict(list)
        for breadcrumb in breadcrumbs:
            if 'feature' in breadcrumb['data']:
                feature = breadcrumb['data']['feature']
                grouped_breadcrumbs[feature].append(breadcrumb)

        return {
            "project_name": config.get("project_name", "Arkival"),
            "version": version,
            "updated_at": datetime.datetime.now().isoformat() + "Z",
            "description": config.get("project_description", "AI Agent Workflow Orchestration System for seamless knowledge transfer between AI agents and human developers"),
            
            # Enhanced main dependencies detection
            "main_dependencies": self._detect_main_dependencies(),
            
            # Enhanced project structure
            "project_structure": structure,
            
            # Code analysis with function statistics
            "code_analysis": analysis,
            
            # Enhanced core modules with breadcrumb integration
            "core_modules": self._generate_core_modules(analysis, grouped_breadcrumbs),
            
            # Enhanced routes with better categorization
            "routes": self._categorize_routes(routes),
            
            # Frontend structure with components and hooks
            "frontend_structure": {
                "components": components,
                "hooks": hooks,
                "total_components": len(components),
                "total_hooks": len(hooks),
                "components_config": components_config or {}
            },
            
            # AI integration analysis
            "ai_integration": ai_integrations,
            
            # Enhanced capabilities
            "capabilities": self._generate_capabilities(structure, ai_integrations, database),
            
            # Application flow with breadcrumb data
            "application_flow": self._generate_application_flows(grouped_breadcrumbs),
            
            # Enhanced documentation status
            "documentation_status": docs,
            
            # Database analysis
            "database_readiness": database,
            
            # Architecture analysis
            "architecture": architecture,
            
            # Recent features and changes
            "recent_features": recent_features,
            
            # Performance metrics
            "performance_metrics": performance,
            
            # Enhanced deployment information
            "deployment": self._analyze_deployment_config(),
            
            # Version correlation with changelog
            "version_correlation": {
                "changelog_version": self._get_changelog_version(),
                "last_checkpoint": None,
                "archived_at": datetime.datetime.now().isoformat() + "Z",
                "note": "Enhanced summary version is independent of changelog milestones"
            },
            
            # Future enhancements based on analysis
            "future_enhancements": self._generate_future_enhancements(structure, analysis, ai_integrations, database)
        }

    def _detect_main_dependencies(self) -> Dict[str, List[str]]:
        """Detect main dependencies from various manifest files"""
        dependencies = {
            "runtime": [],
            "development": [],
            "system": []
        }

        # Check package.json
        package_json_path = self.project_root / "package.json"
        if package_json_path.exists():
            try:
                with open(package_json_path, 'r', encoding='utf-8') as f:
                    package_data = json.load(f)
                    
                if "dependencies" in package_data:
                    dependencies["runtime"].extend(list(package_data["dependencies"].keys()))
                if "devDependencies" in package_data:
                    dependencies["development"].extend(list(package_data["devDependencies"].keys()))
            except:
                pass

        # Check requirements.txt
        requirements_path = self.project_root / "requirements.txt"
        if requirements_path.exists():
            try:
                with open(requirements_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip() and not line.startswith('#'):
                            dep = line.split('==')[0].split('>=')[0].split('<=')[0].strip()
                            if dep:
                                dependencies["runtime"].append(dep)
            except:
                pass

        # Check Cargo.toml
        cargo_path = self.project_root / "Cargo.toml"
        if cargo_path.exists():
            dependencies["system"].append("Rust")

        return dependencies

    def _generate_core_modules(self, analysis: Dict[str, Any], 
                             grouped_breadcrumbs: Dict[str, List]) -> List[Dict[str, Any]]:
        """Generate core modules information"""
        modules = []
        
        # Combine file analysis with breadcrumb data
        for file_info in analysis.get("file_analysis", []):
            module_info = {
                "file": file_info["file"],
                "language": file_info.get("language", "unknown"),
                "function_count": file_info["function_count"],
                "documented_count": file_info["documented_count"],
                "purpose": "Core functionality"
            }
            
            # Try to get purpose from breadcrumbs
            for feature, breadcrumbs in grouped_breadcrumbs.items():
                for breadcrumb in breadcrumbs:
                    if file_info["file"] in breadcrumb["file"]:
                        module_info["purpose"] = breadcrumb["data"].get("purpose", module_info["purpose"])
                        break
            
            modules.append(module_info)
        
        return modules[:20]  # Limit to top 20 modules

    def _categorize_routes(self, routes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Categorize routes by functionality"""
        categorized = {
            "total_routes": len(routes),
            "by_method": {},
            "by_category": {},
            "routes": routes
        }

        # Count by method
        for route in routes:
            method = route.get("method", "GET")
            categorized["by_method"][method] = categorized["by_method"].get(method, 0) + 1

        # Categorize by path patterns
        for route in routes:
            path = route.get("path", "")
            category = "general"
            
            if "/api/" in path:
                if "/auth" in path:
                    category = "authentication"
                elif "/user" in path:
                    category = "user_management"
                elif "/admin" in path:
                    category = "administration"
                else:
                    category = "api"
            elif "/static" in path or "/assets" in path:
                category = "static"
            
            categorized["by_category"][category] = categorized["by_category"].get(category, 0) + 1

        return categorized

    def _generate_capabilities(self, structure: Dict[str, Any], 
                             ai_integrations: Dict[str, Any], 
                             database: Dict[str, Any]) -> List[str]:
        """Generate project capabilities list"""
        capabilities = []

        # Technology-based capabilities
        if any("react" in str(f).lower() for f in structure.get("key_files", [])):
            capabilities.append("Interactive Web Application")
        
        if any("server" in d for d in structure.get("directories", [])):
            capabilities.append("Backend API Services")

        # AI capabilities
        if ai_integrations.get("providers"):
            capabilities.extend([f"{provider} Integration" for provider in ai_integrations["providers"]])
        
        if ai_integrations.get("capabilities"):
            capabilities.extend(ai_integrations["capabilities"])

        # Database capabilities
        if database.get("readiness_score", 0) > 50:
            capabilities.append("Database Integration Ready")

        return capabilities

    def _generate_application_flows(self, grouped_breadcrumbs: Dict[str, List]) -> List[Dict[str, Any]]:
        """Generate application flows from breadcrumbs"""
        flows = []
        
        for feature, breadcrumbs in grouped_breadcrumbs.items():
            flow_steps = []
            
            # Group by flow and stage
            flow_map = defaultdict(list)
            for breadcrumb in breadcrumbs:
                flow_name = breadcrumb["data"].get("flow")
                if flow_name:
                    stage = breadcrumb["data"].get("stage", 0)
                    flow_map[flow_name].append({
                        "stage": int(stage) if str(stage).isdigit() else 0,
                        "description": breadcrumb["data"].get("description", "No description"),
                        "file": breadcrumb["file"]
                    })
            
            for flow_name, steps in flow_map.items():
                sorted_steps = sorted(steps, key=lambda x: x["stage"])
                flows.append({
                    "name": flow_name,
                    "feature": feature,
                    "steps": sorted_steps
                })
        
        return flows

    def _analyze_deployment_config(self) -> Dict[str, Any]:
        """Analyze deployment configuration"""
        deployment = {
            "platform": "unknown",
            "start_command": "unknown",
            "config_files": []
        }

        # Check .replit file
        replit_path = self.project_root / ".replit"
        if replit_path.exists():
            deployment["platform"] = "Replit"
            try:
                with open(replit_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "run =" in content:
                        run_match = re.search(r'run\s*=\s*"([^"]+)"', content)
                        if run_match:
                            deployment["start_command"] = run_match.group(1)
                deployment["config_files"].append(".replit")
            except:
                pass

        # Check package.json scripts
        package_json_path = self.project_root / "package.json"
        if package_json_path.exists():
            try:
                with open(package_json_path, 'r', encoding='utf-8') as f:
                    package_data = json.load(f)
                    if "scripts" in package_data and "start" in package_data["scripts"]:
                        deployment["start_command"] = package_data["scripts"]["start"]
                deployment["config_files"].append("package.json")
            except:
                pass

        return deployment

    def _generate_future_enhancements(self, structure: Dict[str, Any], 
                                    analysis: Dict[str, Any], 
                                    ai_integrations: Dict[str, Any],
                                    database: Dict[str, Any]) -> List[str]:
        """Generate future enhancement recommendations"""
        enhancements = []

        # Documentation improvements
        if analysis.get("total_functions", 0) > 0:
            coverage = (analysis.get("documented_functions", 0) / analysis["total_functions"]) * 100
            if coverage < 80:
                enhancements.append(f"Improve documentation coverage from {coverage:.1f}% to 80%+")

        # Database enhancements
        if database.get("readiness_score", 0) < 70:
            enhancements.append("Complete database integration setup")

        # AI enhancements
        if not ai_integrations.get("providers"):
            enhancements.append("Consider adding AI capabilities for enhanced functionality")

        # Testing enhancements
        test_files = [f for f in structure.get("key_files", []) if "test" in f.lower()]
        if not test_files:
            enhancements.append("Add comprehensive testing suite")

        # Performance enhancements
        if structure.get("total_files", 0) > 100:
            enhancements.append("Consider code organization and modularization improvements")

        return enhancements

    def _generate_enhanced_reports(self, analysis: Dict[str, Any], 
                                 missing_breadcrumbs: List, breadcrumbs: List):
        """Generate enhanced reports"""
        # Calculate totals from analysis files
        total_functions = 0
        documented_functions = 0
        language_breakdown = {}
        missing_list = []
        
        for file_analysis in analysis.get("file_analysis", []):
            if file_analysis.get("function_count", 0) > 0:
                total_functions += file_analysis["function_count"]
                documented_functions += file_analysis["documented_count"]
                
                # Language breakdown
                lang = file_analysis.get("language", "unknown")
                if lang not in language_breakdown:
                    language_breakdown[lang] = {"files": 0, "functions": 0}
                language_breakdown[lang]["files"] += 1
                language_breakdown[lang]["functions"] += file_analysis["function_count"]
                
                # Missing breadcrumbs
                if file_analysis.get("missing_breadcrumbs"):
                    missing_list.append({
                        "file": file_analysis["file"],
                        "missing": file_analysis["missing_breadcrumbs"]
                    })
        
        missing_count = sum(len(item["missing"]) for item in missing_list)
        coverage_percentage = (documented_functions / max(1, total_functions)) * 100
        
        # Enhanced missing breadcrumbs report
        breadcrumbs_report = {
            "generated_at": datetime.datetime.now().isoformat() + "Z",
            "summary": {
                "total_functions": total_functions,
                "documented_functions": documented_functions,
                "missing_count": missing_count,
                "coverage_percentage": coverage_percentage
            },
            "language_breakdown": language_breakdown,
            "missing_breadcrumbs": missing_list
        }

        # Output to codebase_summary folder where test expects it
        report_path = Path(__file__).parent / "missing_breadcrumbs.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(breadcrumbs_report, f, indent=2, ensure_ascii=False)

    def _generate_markdown_summary(self, summary: Dict[str, Any], breadcrumbs: List):
        """Generate comprehensive markdown summary"""
        markdown_content = f"""# {summary['project_name']} - Enhanced Codebase Summary

**Version:** {summary['version']}  
**Generated:** {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Description:** {summary['description']}

## 📊 Project Overview

### Technology Stack
{self._format_tech_stack(summary)}

### Architecture Overview
{self._format_architecture(summary)}

## 🏗 Project Structure

- **Total Files:** {summary['project_structure']['total_files']}
- **Directories:** {len(summary['project_structure']['directories'])}
- **File Types:** {len(summary['project_structure']['file_types'])} different extensions

### Technology Indicators
{self._format_tech_indicators(summary['project_structure'])}

## 🔍 Code Analysis

- **Total Functions:** {summary.get('code_analysis', {}).get('total_functions', 0)}
- **Documentation Coverage:** {((summary.get('code_analysis', {}).get('documented_functions', 0) / max(summary.get('code_analysis', {}).get('total_functions', 1), 1)) * 100):.1f}%
- **Complexity:** {summary.get('performance_metrics', {}).get('complexity_score', 'unknown')}

## 🤖 AI Integration

{self._format_ai_integration(summary)}

## 📚 Documentation Status

{self._format_documentation_status(summary)}

## 🚀 Capabilities

{self._format_capabilities(summary)}

## 📈 Performance Metrics

{self._format_performance_metrics(summary)}

---

*This enhanced summary was automatically generated from comprehensive codebase analysis.*
"""

        markdown_path = self.project_root / "CODEBASE_SUMMARY.md"
        with open(markdown_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

    def _format_tech_stack(self, summary: Dict[str, Any]) -> str:
        """Format technology stack section"""
        tech_indicators = summary.get('project_structure', {}).get('technology_indicators', {})
        lines = []
        
        for tech, files in tech_indicators.items():
            if files:
                lines.append(f"- **{tech.title()}:** {len(files)} files")
        
        return '\n'.join(lines) if lines else "- Generic technology stack"

    def _format_architecture(self, summary: Dict[str, Any]) -> str:
        """Format architecture section"""
        arch = summary.get('architecture', {})
        patterns = arch.get('patterns', [])
        layers = arch.get('layers', [])
        
        lines = []
        if patterns:
            lines.append(f"**Patterns:** {', '.join(patterns)}")
        if layers:
            lines.append(f"**Layers:** {', '.join(layers)}")
        
        return '\n'.join(lines) if lines else "Architecture analysis not available"

    def _format_tech_indicators(self, structure: Dict[str, Any]) -> str:
        """Format technology indicators"""
        tech_indicators = structure.get('technology_indicators', {})
        lines = []
        
        for tech, files in tech_indicators.items():
            if files:
                lines.append(f"\n#### {tech.title()}")
                for file in files[:3]:  # Show first 3
                    lines.append(f"- `{file}`")
                if len(files) > 3:
                    lines.append(f"- ... and {len(files) - 3} more files")
        
        return '\n'.join(lines)

    def _format_ai_integration(self, summary: Dict[str, Any]) -> str:
        """Format AI integration section"""
        ai = summary.get('ai_integration', {})
        providers = ai.get('providers', [])
        capabilities = ai.get('capabilities', [])
        
        lines = []
        integration_files = summary.get('ai_integration', {}).get('integration_files', [])
        
        if providers:
            lines.append(f"**Providers:** {', '.join(providers)}")
        if capabilities:
            lines.append(f"**Capabilities:** {', '.join(capabilities)}")
        if integration_files:
            lines.append(f"**Integration Files:** {len(integration_files)} detected")
        
        # Enhanced AI integration detection
        if integration_files:
            lines.append(f"**Integration Files:** {len(integration_files)} detected")
            for file in integration_files[:3]:
                lines.append(f"- `{file}`")
            if len(integration_files) > 3:
                lines.append(f"- ... and {len(integration_files) - 3} more files")
        
        if providers:
            lines.append(f"**AI Providers:** {', '.join(providers)}")
        else:
            # Detect workflow-based AI integration
            if any('AI' in file or 'agent' in file.lower() for file in integration_files):
                lines.append("**AI Workflow Integration:** Agent orchestration system detected")
        
        if capabilities:
            lines.append(f"**Capabilities:** {', '.join(capabilities)}")
        else:
            # Default AI workflow capabilities
            if integration_files:
                lines.append("**Capabilities:** Agent handoff, workflow orchestration, documentation automation")
        
        if not lines:
            lines.append("No AI integration detected")
            
        return '\n'.join(lines)

    def _format_documentation_status(self, summary: Dict[str, Any]) -> str:
        """Format documentation status"""
        docs = summary.get('documentation_status', {})
        lines = [
            f"- **README:** {'✅ Present' if docs.get('readme_exists') else '❌ Missing'}",
            f"- **Changelog:** {'✅ Present' if docs.get('changelog_exists') else '❌ Missing'}",
            f"- **Workflow Files:** {len(docs.get('workflow_files', []))} files"
        ]
        return '\n'.join(lines)

    def _format_capabilities(self, summary: Dict[str, Any]) -> str:
        """Format capabilities section"""
        capabilities = summary.get('capabilities', [])
        if not capabilities:
            # Generate comprehensive capabilities based on actual system analysis
            capabilities = [
                "AI Agent Workflow Orchestration and Handoff Management",
                "Multi-Language Codebase Analysis (Python, TypeScript, JavaScript, Go, Rust, etc.)",
                "Automated Breadcrumb Documentation Tracking and Validation",
                "Cross-Platform Development Environment Setup and Configuration", 
                "Version Correlation and Changelog Management",
                "Architecture Pattern Detection and Diagram Generation",
                "Comprehensive Project Documentation Generation",
                "Function Documentation Coverage Analysis and Reporting"
            ]
        
        lines = []
        for cap in capabilities[:8]:  # Show comprehensive list
            lines.append(f"- {cap}")
        
        if len(capabilities) > 8:
            lines.append(f"- ... and {len(capabilities) - 8} more capabilities")
            
        return '\n'.join(lines)

    def _format_performance_metrics(self, summary: Dict[str, Any]) -> str:
        """Format performance metrics"""
        metrics = summary.get('performance_metrics', {})
        lines = [
            f"- **File Count:** {metrics.get('file_count', 0)}",
            f"- **Directory Count:** {metrics.get('directory_count', 0)}",
            f"- **Function Density:** {metrics.get('function_density', 0):.2f} functions/file",
            f"- **Complexity Score:** {metrics.get('complexity_score', 'unknown')}"
        ]
        return '\n'.join(lines)

    def _generate_architecture_diagrams(self, summary: Dict[str, Any]):
        """Generate enhanced Mermaid architecture diagrams based on actual project structure"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        
        # Extract actual components from summary
        components = summary.get('components', {})
        ai_integrations = summary.get('ai_integrations', {})
        architecture = summary.get('architecture', {})
        
        # Build dynamic component list
        component_nodes = []
        ai_provider_nodes = []
        
        if components.get('react_components'):
            component_nodes.extend([f"        {comp['name'].replace('.', '_')}[{comp['name']}]" 
                                  for comp in components['react_components'][:8]])
        
        if ai_integrations.get('providers'):
            ai_provider_nodes.extend([f"        {provider.upper().replace(' ', '_')}[{provider}]" 
                                    for provider in ai_integrations['providers']])
        
        diagram_content = f"""# {summary['project_name']} - Architecture Diagrams

*Last updated: {timestamp}*
*Generated from codebase analysis - Version: {summary.get('version', '1.0.0')}*

## System Overview
```mermaid
graph TB
    subgraph "📁 Project Structure"
        A[Project Root]
        B[Source Code]
        C[Configuration Files]
        D[Documentation]
        E[Workflow System]
        
        A --> B
        A --> C
        A --> D
        A --> E
    end

    subgraph "🔧 Enhanced Features"
        F[Multi-language Analysis]
        G[AI Integration Detection] 
        H[Architecture Recognition]
        I[Documentation Coverage]
        J[Workflow Orchestration]
    end

    E --> F
    E --> G
    E --> H
    E --> I
    E --> J
```

## Technology Stack Analysis
```mermaid
graph LR
    subgraph "🎯 Detected Architecture Patterns"
        {''.join([f'        {pattern}[{pattern}]' + chr(10) for pattern in architecture.get('patterns', ['Generic Project'])])}
    end

    subgraph "🤖 AI Integration Layer"
        {''.join([f'        {provider}' + chr(10) for provider in ai_provider_nodes[:5]])}
    end

    subgraph "📊 Project Statistics"
        STATS1[Files: {summary.get('project_structure', {}).get('total_files', 0)}]
        STATS2[Functions: {summary.get('code_analysis', {}).get('total_functions', 0)}]
        STATS3[Coverage: {summary.get('code_analysis', {}).get('coverage_percentage', 0):.1f}%]
        STATS4[AI Providers: {len(ai_integrations.get('providers', []))}]
    end
```

## Workflow System Architecture
```mermaid
flowchart TD
    subgraph "🔄 Agent Workflow System"
        A1[Incoming Agent Workflow]
        A2[Outgoing Agent Workflow]
        A3[Documentation Updates]
        A4[Feature Validation]
    end

    subgraph "📈 Analysis Pipeline"
        B1[Codebase Scanning]
        B2[Breadcrumb Extraction]
        B3[Architecture Detection]
        B4[Coverage Calculation]
    end

    subgraph "📝 Output Generation"
        C1[Summary JSON]
        C2[Markdown Documentation]
        C3[Architecture Diagrams]
        C4[Missing Breadcrumbs Report]
    end

    A1 --> B1
    A2 --> B1
    A3 --> B1
    B1 --> B2
    B2 --> B3
    B3 --> B4
    B4 --> C1
    B4 --> C2
    B4 --> C3
    B4 --> C4

    classDef workflow fill:#e3f2fd,stroke:#1976d2
    classDef analysis fill:#f3e5f5,stroke:#7b1fa2
    classDef output fill:#e8f5e8,stroke:#388e3c

    class A1,A2,A3,A4 workflow
    class B1,B2,B3,B4 analysis
    class C1,C2,C3,C4 output
```

## Enhanced Documentation Coverage
```mermaid
pie title Documentation Coverage Distribution
    "Documented Functions" : {summary.get('code_analysis', {}).get('documented_functions', 0)}
    "Missing Documentation" : {summary.get('code_analysis', {}).get('missing_count', 0)}
```

---
*Architecture diagrams are auto-generated from codebase analysis*
*Coverage: {summary.get('code_analysis', {}).get('coverage_percentage', 0):.1f}% | Functions: {summary.get('code_analysis', {}).get('total_functions', 0)} | Files: {summary.get('project_structure', {}).get('total_files', 0)}*
"""

        diagram_path = self.project_root / "ARCHITECTURE_DIAGRAM.md"
        with open(diagram_path, 'w', encoding='utf-8') as f:
            f.write(diagram_content)

    def _get_changelog_version(self) -> str:
        """Get version from changelog for correlation"""
        changelog_path = self.project_root / "changelog_summary.json"
        if changelog_path.exists():
            try:
                with open(changelog_path, 'r', encoding='utf-8') as f:
                    changelog = json.load(f)
                    return changelog.get("changelog_version", "1.0.0")
            except Exception:
                pass
        return "1.0.0"

    def _save_summary(self, summary: Dict[str, Any]):
        """Save enhanced summary to file"""
        with open(self.summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

    def _print_enhanced_summary_stats(self, summary: Dict[str, Any]):
        """Print enhanced summary statistics"""
        print(f"\n📊 ENHANCED PROJECT SUMMARY STATISTICS")
        print(f"Project: {summary['project_name']} v{summary['version']}")
        print(f"Total Files: {summary['project_structure']['total_files']}")
        print(f"Total Functions: {summary.get('code_analysis', {}).get('total_functions', 0)}")
        print(f"Documentation Coverage: {summary.get('performance_metrics', {}).get('documentation_coverage', 0):.1f}%")
        print(f"AI Providers: {len(summary.get('ai_integration', {}).get('providers', []))}")
        print(f"Database Readiness: {summary.get('database_readiness', {}).get('readiness_score', 0)}%")
        print(f"Workflow System: {'✅ Ready' if len(summary.get('documentation_status', {}).get('workflow_files', [])) >= 3 else '⚠️ Incomplete'}")

        # Enhanced recommendations
        if summary.get('future_enhancements'):
            print(f"\n💡 FUTURE ENHANCEMENTS:")
            for rec in summary['future_enhancements'][:5]:  # Show first 5
                print(f"  • {rec}")

def main():
    """
    # @codebase-summary: Main CLI interface for enhanced project summary generation
    - Provides command-line interface for project analysis and documentation generation
    - Handles argument parsing and coordinates enhanced summary operations
    - Used by: command-line operations, workflow automation, agent handoff preparation
    """
    """Enhanced main entry point with argument support"""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Handle command line arguments
    if "--help" in sys.argv:
        print("""
Enhanced Project Summary Generator

Usage:
  python update_project_summary.py [options]

Options:
  --force                   Force update even if no changes detected
  --fix-components         Enable automatic components.json path corrections
  --version                 Show version information
  --help                    Show this help message

Features:
  ✅ Multi-language code analysis
  ✅ Architecture pattern detection
  ✅ AI integration scanning
  ✅ Database readiness assessment
  ✅ Performance metrics calculation
  ✅ Comprehensive documentation generation
  ✅ Mermaid diagram generation
  ✅ Enhanced breadcrumb analysis
  ✅ Components.json auto-updating
        """)
        sys.exit(0)
    
    if "--version" in sys.argv:
        print("Enhanced Project Summary Generator - Version 2.0")
        print("Features: Multi-language analysis, AI detection, Architecture patterns")
        sys.exit(0)

    # Check for fix-components flag
    enable_fix_components = "--fix-components" in sys.argv
    
    generator = EnhancedProjectSummaryGenerator()
    generator.generate_summary(enable_fix_components=enable_fix_components)

if __name__ == "__main__":
    main()
