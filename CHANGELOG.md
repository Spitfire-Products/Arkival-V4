# Changelog

All notable changes to Arkival will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

*Automated changelog system*

## [Unreleased]

## [1.2.0] - 2025-06-18

## [1.1.0] - 2025-06-18

### Enhanced
- MAJOR REFACTOR COMPLETED: Arkival Subdirectory Deployment System - Implemented universal path resolution across all 5 Python scripts. Added find_arkival_paths() function for automatic detection of deployment context. System now supports non-destructive integration where Arkival operates from /Arkival subdirectory with only arkival_config.json in project root. Updated 12+ file operations in agent_workflow_orchestrator.py to use resolved paths. Validated all scripts work correctly in both source and subdirectory contexts. Created comprehensive documentation.

## [1.0.2] - 2025-06-18

### Enhanced
- Implemented comprehensive file generator attribution system - Added _generator field to all JSON outputs for transparency and traceability. Each generated file now includes clear attribution showing which script created it and its purpose. Standardized attribution format across all Python scripts.

## [1.0.1] - 2025-06-18

### Enhanced
- Implemented comprehensive file regeneration resilience system - Added automatic file regeneration with intelligent retry logic, comprehensive error handling across all file operations, backup and recovery mechanisms for critical files, graceful degradation for non-critical operations, detailed logging for debugging failed operations. System now handles file corruption, disk space issues, permission errors, and concurrent access conflicts.

---

## Migration Guide

### From Pre-1.0 Versions
This is the first stable release. Follow the setup instructions in README.md for initial deployment.

### Upgrading to Latest Version
1. Back up your existing workflow_config.json
2. Run the setup script: `python3 setup_workflow_system.py`
3. Review and update configuration as needed