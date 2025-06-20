# Generic Deployment Work Plan - Making Scripts Codebase Agnostic

## Overview
This work plan addresses making the workflow system completely generic and deployable to ANY codebase without hardcoded project-specific data.

## Phase 1: Configuration System Design (Priority: High)

### 1.1 Create Universal Configuration Schema
- **File**: `.workflow_config_schema.json`
- **Contents**:
  - Project metadata (name, description, version)
  - Directory structure mapping
  - Script locations and paths
  - Workflow integration settings
  - AI provider configurations
  - Documentation templates

### 1.2 Update Path Resolution System
- **Replace**: All `find_arkival_paths()` functions
- **With**: Generic `find_project_paths()` that reads configuration
- **Files affected**:
  - setup_workflow_system.py
  - agent_workflow_orchestrator.py
  - update_changelog.py
  - update_project_summary.py (already updated)

## Phase 2: Remove Hardcoded References (Priority: Critical)

### 2.1 setup_workflow_system.py
- [ ] Remove all "Arkival" text references
- [ ] Make directory names configurable
- [ ] Remove company-specific attribution
- [ ] Generalize documentation templates
- [ ] Use generic configuration keys
- [ ] Dynamic version detection
- [ ] Configurable file naming

### 2.2 agent_workflow_orchestrator.py
- [ ] Replace "Arkival" with generic terms
- [ ] Use generic config file name
- [ ] Make directory structure configurable
- [ ] Remove hardcoded documentation paths
- [ ] Make archive limits configurable
- [ ] Add script existence checks

### 2.3 update_changelog.py
- [ ] Remove "Arkival" from all outputs
- [ ] Make workflow integration optional
- [ ] Configurable versioning schemes
- [ ] Generic default values
- [ ] Remove project-specific documentation

### 2.4 update_project_summary.py
- [ ] Already updated - verify integration with other scripts

## Phase 3: Template System (Priority: High)

### 3.1 Create Template Directory
- **Location**: `templates/`
- **Contents**:
  - README.md.template
  - CONTRIBUTING.md.template
  - LICENSE.template
  - CHANGELOG.md.template
  - Setup documentation templates

### 3.2 Template Variables System
- Use placeholders like `{{PROJECT_NAME}}`, `{{PROJECT_DESCRIPTION}}`
- Support custom template directories
- Allow project-specific overrides

## Phase 4: Integration Testing (Priority: High)

### 4.1 Test Suite Creation
- Test with empty project
- Test with existing Python project
- Test with existing JavaScript project
- Test with mixed technology project
- Test subdirectory deployment
- Test standalone deployment

### 4.2 Validation Scripts
- Create `validate_generic_deployment.py`
- Check for any hardcoded values
- Verify configuration completeness
- Test all workflows end-to-end

## Phase 5: Documentation (Priority: Medium)

### 5.1 Create Generic Documentation
- Installation guide for any project
- Configuration reference
- Customization guide
- Migration guide from hardcoded version

### 5.2 Create CLAUDE.md
- Best practices for AI agents
- Workflow system usage
- Configuration management
- Integration guidelines

## Implementation Order

1. **Configuration System** (Foundation for everything else)
   - Define schema
   - Create default configuration
   - Update path resolution

2. **Core Scripts Updates**
   - setup_workflow_system.py (most critical)
   - agent_workflow_orchestrator.py
   - update_changelog.py

3. **Template System**
   - Create template structure
   - Convert hardcoded content to templates

4. **Testing & Validation**
   - Create test projects
   - Run full workflow tests
   - Fix integration issues

5. **Documentation**
   - Update all docs for generic deployment
   - Create CLAUDE.md guide

## Success Criteria

- [ ] No "Arkival" references in any script
- [ ] All paths and names come from configuration
- [ ] Scripts work with any project type
- [ ] Templates are customizable
- [ ] Documentation is project-agnostic
- [ ] Full test suite passes
- [ ] AI agents can understand and use the system

## Estimated Timeline

- Phase 1: 2-3 hours
- Phase 2: 3-4 hours  
- Phase 3: 2 hours
- Phase 4: 2 hours
- Phase 5: 1-2 hours

Total: ~12-14 hours of implementation work