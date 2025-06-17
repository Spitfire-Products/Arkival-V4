# Project Template Usage Guide

This directory contains configuration templates for deploying the workflow system to different programming languages and environments.

## Available Templates

### Rust Projects
- **File:** `rust_cargo_template.toml`
- **Copy to:** `Cargo.toml` in your Rust project root
- **Purpose:** Provides dependencies for AI integrations, async runtime, and web frameworks
- **Setup:** Run `cargo build` after copying to install dependencies

### Python Projects
- **File:** `python_pyproject_template.toml`
- **Copy to:** `pyproject.toml` in your Python project root
- **Purpose:** Poetry configuration with AI SDKs and development tools
- **Setup:** Run `poetry install` after copying to set up virtual environment

### Node.js Projects
- **File:** `nodejs_package_template.json`
- **Copy to:** `package.json` in your Node.js project root
- **Purpose:** NPM configuration with workflow scripts and AI dependencies
- **Setup:** Run `npm install` after copying to install packages

### Replit Workflows
- **File:** `../.replit_workflows_template.toml`
- **Copy to:** `.replit` file (append workflows section)
- **Purpose:** Replit-specific workflow definitions for agent handoff
- **Setup:** Restart your Repl after adding workflows

## Quick Setup Instructions

### For Rust Projects
1. Copy `rust_cargo_template.toml` to `Cargo.toml`
2. Create `src/main.rs` with workflow integration
3. Run `cargo build` to install dependencies
4. Configure environment variables for AI services

### For Python Projects
1. Copy `python_pyproject_template.toml` to `pyproject.toml`
2. Run `poetry install` to create virtual environment
3. Copy workflow system scripts to project
4. Run setup script with `python setup_workflow_system.py`

### For Node.js Projects
1. Copy `nodejs_package_template.json` to `package.json`
2. Run `npm install` to install dependencies
3. Copy workflow system scripts to project
4. Test with `npm run validate:features`

## Integration Steps

After copying the appropriate template:

1. **Copy Workflow System:**
   ```bash
   cp -r workflow_export_package/codebase_summary ./
   cp workflow_export_package/setup_workflow_system.py ./
   cp workflow_export_package/workflow_config.json ./
   ```

2. **Run Setup:**
   ```bash
   python setup_workflow_system.py
   ```

3. **Configure Environment:**
   Create `.env` file with required API keys:
   ```
   OPENAI_API_KEY=your_openai_key
   ANTHROPIC_API_KEY=your_anthropic_key
   ```

4. **Test Installation:**
   ```bash
   python3 codebase_summary/update_project_summary.py --force
   ```

## Language-Specific Notes

### Rust
- Use `tokio` for async operations
- AI integrations require proper error handling
- WebSocket mitigation may need custom implementation

### Python
- Poetry manages dependencies and virtual environments
- Compatible with FastAPI, Flask, or Django
- Full async/await support for AI operations

### Node.js
- Express server ready for immediate use
- Built-in workflow script commands
- WebSocket mitigation templates included

## Environment Variables

All project types require these environment variables:
- `OPENAI_API_KEY` - OpenAI API access
- `ANTHROPIC_API_KEY` - Anthropic Claude access
- `GOOGLE_AI_API_KEY` - Google Gemini access (optional)

## Troubleshooting

**Dependencies not installing:**
- Ensure you have the correct package manager installed
- Check internet connectivity for package downloads
- Verify template syntax is valid

**Workflow scripts not working:**
- Confirm Python 3.7+ is available
- Check file permissions on script files
- Verify all required files were copied

**AI integrations failing:**
- Confirm API keys are set correctly
- Test API connectivity independently
- Check rate limits and billing status

## Custom Adaptations

These templates provide baseline configurations. Customize them based on:
- Specific framework requirements
- Additional dependencies needed
- Performance optimization settings
- Security configurations

The workflow system is designed to be language-agnostic in its core functionality while providing language-specific integration points.