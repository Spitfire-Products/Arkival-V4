# Arkival Deployment Guide

## Overview

Arkival supports two deployment modes that are automatically detected and configured. Choose the mode that best fits your workflow.

## 🆕 Subdirectory Mode (Recommended for Existing Projects)

### When to Use
- Adding Arkival to an existing project
- Want zero disruption to existing files
- Need easy removal option
- Working in a team with mixed AI tool preferences

### Setup Process
```bash
# Navigate to your existing project root
cd /path/to/your/existing/project

# Clone Arkival as a subdirectory
git clone https://github.com/spitfire-products/arkival.git Arkival

# Navigate into Arkival directory
cd Arkival

# Run setup (auto-detects subdirectory mode)
python3 setup_workflow_system.py
```

### What Gets Created
```
your_project/
├── arkival_config.json          # Only file added to your project
├── src/                         # Your existing files (untouched)
├── package.json                 # Your existing files (untouched)
├── README.md                    # Your existing files (untouched)
└── Arkival/                     # All Arkival files contained here
    ├── setup_workflow_system.py
    ├── validate_deployment.py
    ├── codebase_summary/
    │   ├── agent_workflow_orchestrator.py
    │   ├── update_changelog.py
    │   ├── update_project_summary.py
    │   ├── session_state.json
    │   ├── agent_handoff.json
    │   └── missing_breadcrumbs.json
    ├── data/                    # Generated files location
    │   ├── codebase_summary.json
    │   ├── changelog_summary.json
    │   └── history/
    ├── checkpoints/
    │   └── checkpoint_log.md
    └── .replit / .vscode/ etc.  # IDE configurations
```

### Benefits
- ✅ **Non-destructive**: Your project files are never modified
- ✅ **Clean separation**: All Arkival files in one directory
- ✅ **Easy removal**: Just delete the `/Arkival` directory
- ✅ **Team friendly**: Only `arkival_config.json` appears in git
- ✅ **Portable**: Works with any existing project structure

### arkival_config.json
```json
{
  "deployment_mode": "subdirectory_integration",
  "project_name": "Your Project Name",
  "arkival_directory": "./Arkival",
  "version": "1.0.0"
}
```

## Development Mode (For Arkival-First Projects)

### When to Use
- Creating a new project with Arkival as the main system
- Contributing to Arkival development
- Want full integration with project structure

### Setup Process
```bash
# Clone Arkival as the main project
git clone https://github.com/spitfire-products/arkival.git
cd arkival

# Run setup (auto-detects development mode)
python3 setup_workflow_system.py
```

### What Gets Created
```
arkival/                         # Project root
├── setup_workflow_system.py
├── validate_deployment.py
├── codebase_summary.json        # Generated in root
├── changelog_summary.json       # Generated in root
├── codebase_summary/
│   ├── agent_workflow_orchestrator.py
│   ├── update_changelog.py
│   ├── update_project_summary.py
│   ├── session_state.json
│   ├── agent_handoff.json
│   ├── missing_breadcrumbs.json
│   └── history/                 # Archived versions
├── checkpoints/
│   └── checkpoint_log.md
└── .replit / .vscode/ etc.      # IDE configurations
```

### Benefits
- ✅ **Full integration**: Complete access to all Arkival capabilities
- ✅ **Development ready**: Ideal for Arkival development
- ✅ **Performance**: No subdirectory overhead

## Universal Path Resolution System

### How It Works
All Arkival scripts use the `find_arkival_paths()` function to automatically detect deployment mode:

```python
def find_arkival_paths():
    current_dir = Path.cwd()
    
    # Check deployment mode
    if current_dir.name.lower() == 'arkival' or (project_root / "arkival_config.json").exists():
        # Subdirectory mode - use Arkival/ paths
        return {
            'codebase_summary': project_root / "Arkival" / "data" / "codebase_summary.json",
            'changelog_summary': project_root / "Arkival" / "data" / "changelog_summary.json",
            # ... other Arkival/ paths
        }
    else:
        # Development mode - use root paths
        return {
            'codebase_summary': project_root / "codebase_summary.json",
            'changelog_summary': project_root / "changelog_summary.json",
            # ... other root paths
        }
```

### Smart Detection
The system detects deployment mode by checking:
1. **Current directory name**: If running from directory named "arkival"
2. **Config file presence**: If `arkival_config.json` exists in project root
3. **Fallback**: Assumes development mode

## IDE Integration

### Automatic IDE Detection
The setup script detects and configures:
- **Replit**: Creates `.replit` with workflow buttons
- **VS Code/Cursor**: Creates `.vscode/tasks.json` with Command Palette integration
- **Gitpod**: Creates `.gitpod.yml` for cloud development
- **Universal**: Creates `.workflow_system/scripts/` for any terminal

### Cross-IDE Compatibility
- Works the same regardless of deployment mode
- Session state persists across IDE switches
- Agent handoffs work seamlessly in any environment

## Validation and Testing

### System Validation
```bash
# Validate the deployment (works in both modes)
python3 validate_deployment.py
```

### Test Workflows
```bash
# Test incoming agent workflow
python3 codebase_summary/agent_workflow_orchestrator.py incoming

# Test changelog system
python3 codebase_summary/update_changelog.py add --summary "Test entry"

# Test codebase analysis
python3 codebase_summary/update_project_summary.py --force
```

## Migration Between Modes

### From Development to Subdirectory
```bash
# 1. Create target project structure
mkdir your_project && cd your_project

# 2. Move arkival into subdirectory
mv /path/to/arkival ./Arkival
cd Arkival

# 3. Re-run setup to detect new mode
python3 setup_workflow_system.py

# 4. The system will automatically start using subdirectory paths
```

### From Subdirectory to Development
```bash
# 1. Move Arkival out of subdirectory
mv your_project/Arkival ./arkival-standalone
cd arkival-standalone

# 2. Remove the config file that triggers subdirectory mode
rm arkival_config.json

# 3. Re-run setup
python3 setup_workflow_system.py
```

## Troubleshooting

### Common Issues

**Files appearing in wrong location:**
- Check if `arkival_config.json` exists in project root
- Verify current working directory when running scripts
- Re-run setup script to refresh configuration

**Scripts not detecting mode correctly:**
- Ensure you're running from correct directory
- Check that `find_arkival_paths()` function is present in script
- Validate deployment with `python3 validate_deployment.py`

**IDE integration not working:**
- Re-run `python3 setup_workflow_system.py`
- Check that IDE-specific files were created
- Verify your IDE is properly detected

### Debug Mode Detection
```python
# Add this to any script to debug path resolution
paths = find_arkival_paths()
print("Detected paths:", paths)
print("Mode: Subdirectory" if "Arkival" in str(paths['codebase_summary']) else "Development")
```

## Best Practices

### For Subdirectory Mode
- Keep the `/Arkival` directory in your project's `.gitignore` if you don't want to version Arkival
- Or include it in git for team-wide Arkival usage
- Only `arkival_config.json` needs to be committed for basic integration

### For Development Mode
- Use this mode when contributing to Arkival itself
- Ideal for projects where Arkival is the primary workflow system
- Full access to all development and debugging capabilities

### General
- Always run `validate_deployment.py` after setup
- Test both incoming and outgoing workflows before production use
- Keep Arkival updated by pulling latest changes from the repository

---

*This deployment guide reflects the universal path resolution system implemented in Arkival v1.1.8+*