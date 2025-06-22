# Changelog

All notable changes to Arkival will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

*Automated changelog system*

## [Unreleased]

## [1.8.0] - 2025-06-21

## [1.7.0] - 2025-06-21

## [1.6.0] - 2025-06-21

### Enhanced
- AI Agent Architecture Documentation Enhancement: Transformed ARCHITECTURE_DIAGRAM.md from abstract diagrams to practical AI agent onboarding guide. Modified update_project_summary.py generator to produce agent-focused content including system purpose, quick start guide, critical files table, and functional architecture diagrams. Successfully tested and implemented version 1.1.86 with 100% documentation coverage.

## [1.5.0] - 2025-06-21

### Enhanced
- Major documentation and system optimization: Comprehensive README rewrite, documentation reorganization, and deployment clarity improvements. 

## Key Accomplishments:
- **README.md Complete Transformation**: Rewrote from basic instructions to comprehensive user guide with clear 3-step setup, daily workflow routines, and advanced usage patterns
- **Documentation Architecture Cleanup**: Moved ENGINEERING_BEST_PRACTICES.md to root level, removed empty directories, enhanced discoverability  
- **Vendor-Agnostic Positioning**: Removed Claude/Replit as defaults, positioned as optional modules, updated command hierarchies for universal compatibility
- **System Configuration**: Comprehensive .gitignore cleanup, better organization, added missing environment exclusions
- **COMPONENTS_AUTO_UPDATE.md Audit**: Determined value as post-deployment developer resource, added Figma integration future module
- **Setup Instructions Fix**: Corrected Arkival-V4 clone naming, established Development Mode as primary pattern vs add-on tool
- **Changelog Cleanup**: Removed duplicate/outdated changelog_summary.json from codebase_summary/ directory

Transformed Arkival from technical tool into accessible AI development accelerator with clear setup paths and universal compatibility.

## [1.4.0] - 2025-06-21

### Enhanced
- Major documentation and system optimization: Comprehensive README rewrite, documentation reorganization, and deployment clarity improvements. Moved ENGINEERING_BEST_PRACTICES.md to root, cleaned up .gitignore, positioned system as vendor-agnostic with Claude/Replit as optional modules. Enhanced setup instructions to reflect Development Mode as primary usage pattern.

## [1.3.0] - 2025-06-22

### Enhanced
- Implemented comprehensive project metadata extraction system for subdirectory deployments. Enhanced scanner to extract project details from README, package.json, pyproject.toml, Git config, and auto-detect languages/frameworks. Fixed subdirectory scanning to analyze parent projects instead of Arkival directory. Now extracts git URLs, versions, licenses, authors, and technical stack details for rich documentation generation.
- Dynamic CONTRIBUTING.md generation with correct repository URLs
  Implemented dynamic CONTRIBUTING.md generation that adapts to host project name and repository. Fixed all git repository references from spitfire-products/arkival to Spitfire-Products/Arkival-V4. Added generator attribution and updated registry. CONTRIBUTING.md now auto-generates with correct project name in subdirectory mode and proper repository URLs throughout codebase.

## [1.2.0] - 2025-06-22

### Enhanced
- Fixed deployment validation path resolution for subdirectory mode and updated workflow configuration with actual project details. Resolved validation failures when Arkival deployed as 'Arkival-V4' subdirectory and replaced placeholder values with real project information.
- Massive documentation cleanup - 90% reduction achieved
  Executed comprehensive documentation audit and cleanup: Removed 19+ redundant/outdated .md files. Consolidated SETUP_GUIDE.md, DEPLOYMENT_GUIDE.md into streamlined README.md (678→84 lines). Consolidated AGENT_GUIDE.md with DEVELOPER_ONBOARDING.md. Preserved essential documentation_assets/ai_integrations and .claude folders. Reduced total files from 83→64 while maintaining full functionality. Documentation is now concise and focused.
- Complete documentation breadcrumb system implementation
  Added comprehensive @codebase-summary breadcrumbs to 21+ functions across core system files. Improved documentation coverage from 71.74% to 94.57% (+22.83%). Enhanced agent onboarding with CLAUDE.md guide and verified all deployment modes. System now ready for GitHub deployment with full AI agent workflow orchestration capabilities.
- Documentation cleanup and consolidation needed post-testing
  After testing passes, consolidate excessive and overlapping documentation. Current docs are overly verbose with information bloat rather than providing clear guidance. Need to streamline: README.md, SETUP_GUIDE.md, DEPLOYMENT_GUIDE.md, AGENT_GUIDE.md, DEVELOPER_ONBOARDING.md and remove redundancies while maintaining essential information for quick agent onboarding

## [1.1.55] - 2025-06-19

## [1.1.54] - 2025-06-19

## [1.1.53] - 2025-06-19

## [1.1.52] - 2025-06-19

## [1.1.51] - 2025-06-19

## [1.1.50] - 2025-06-19

## [1.1.44] - 2025-06-19

## [1.1.43] - 2025-06-19

## [1.1.0] - 2025-06-18

---

## Migration Guide

### From Pre-1.0 Versions
This is the first stable release. Follow the setup instructions in README.md for initial deployment.

### Upgrading to Latest Version
1. Back up your existing workflow_config.json
2. Run the setup script: `python3 setup_workflow_system.py`
3. Review and update configuration as needed