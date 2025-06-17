# Changelog

All notable changes to Arkival will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.6.0] - 2025-06-17

### Enhanced
- Integrated EXPORT_PACKAGE_MANIFEST.json with modern validation system
  Updated and integrated the EXPORT_PACKAGE_MANIFEST.json to reflect current v1.1.377 system state: 1) Updated manifest from legacy v1.1.223 to current v1.1.377 with accurate file listings and capabilities, 2) Added comprehensive environment-specific file documentation and deployment architecture details, 3) Integrated manifest validation into validate_deployment.py with detailed file checking across all categories, 4) Enhanced validation system to verify 30 required files across setup_scripts, core_modules, configuration, templates, documentation, ai_integration, and documentation_assets, 5) Added quality metrics tracking including 100% documentation coverage and cross-platform support verification, 6) Documented supported environments (6 IDEs, 5 AI assistants, 4 platforms) and deployment architecture benefits

## [1.5.0] - 2025-06-17

### Enhanced
- Implemented proper environment-specific file management for GitHub deployment
  Fixed critical GitHub deployment architecture issue where environment-specific files were included in repository: 1) Enhanced .gitignore to exclude .replit, .vscode/, .gitpod.yml, and .workflow_system/ directories, 2) Modified setup_workflow_system.py to properly generate .replit file with integrated workflows (not just backup toml), 3) Updated SETUP_GUIDE.md to clearly explain the environment-specific file generation design, 4) Documented clean repository approach where IDE-specific files are generated locally during setup but excluded from GitHub, 5) Ensured cross-platform compatibility where each user gets appropriate environment configuration without repository clutter or merge conflicts

## [1.0.0] - 2025-06-17

---

## Migration Guide

### From Pre-1.0 Versions
This is the first stable release. Follow the setup instructions in README.md for initial deployment.

### Upgrading to Latest Version
1. Back up your existing workflow_config.json
2. Run the setup script: `python3 setup_workflow_system.py`
3. Review and update configuration as needed