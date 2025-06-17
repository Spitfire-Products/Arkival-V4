# Changelog

All notable changes to Arkival will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.4.0] - 2025-06-17

### Enhanced
- Restructured documentation for true cross-platform compatibility
  Fixed GitHub deployment issue where documentation was Replit-specific despite cross-platform capabilities: 1) Renamed replit.md to PROJECT_CONFIG.md for environment-agnostic project preferences, 2) Updated SETUP_GUIDE.md to provide IDE-specific instructions for all supported environments (Replit, VS Code, Cursor, Codespaces, Gitpod), 3) Enhanced workflow_config.json to reflect cross-platform nature with current_ide instead of detected_ide, 4) Added alternative_methods for different IDE workflow execution, 5) Updated references throughout documentation to emphasize multi-IDE support rather than Replit-first approach

## [1.3.0] - 2025-06-17

## [1.2.0] - 2025-06-17

## [1.0.0] - 2025-06-17

---

## Migration Guide

### From Pre-1.0 Versions
This is the first stable release. Follow the setup instructions in README.md for initial deployment.

### Upgrading to Latest Version
1. Back up your existing workflow_config.json
2. Run the setup script: `python3 setup_workflow_system.py`
3. Review and update configuration as needed