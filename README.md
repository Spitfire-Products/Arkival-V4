# Arkival

Arkival is a complete AI agent workflow orchestration system for seamless knowledge transfer, version control, and project onboarding across **any IDE or development environment**.

## 🌐 Supported Environments

### Fully Supported IDEs
- **Replit** - Native workflow integration
- **VS Code** - Tasks and terminal integration
- **Cursor** - VS Code-compatible task system
- **GitHub Codespaces** - Cloud development environment
- **Gitpod** - Browser-based development
- **Windsurf** - Shell script integration
- **Lovable** - Terminal-based workflows
- **Any IDE** - Generic shell script fallback

### AI Coding Assistants Compatible
- **Cline** (VS Code extension)
- **Roo Code** (Multi-IDE)
- **Claude Code** (IDE integrations)
- **GitHub Copilot** (All supported IDEs)
- **Cursor AI** (Native integration)

## 🚀 Quick Start

### GitHub Deployment & Multi-IDE Setup
Arkival is designed for seamless deployment to GitHub and use across multiple development environments.

#### 1. Deploy to GitHub
```bash
git clone https://github.com/spitfire-products/arkival.git
cd arkival
```

#### 2. Configure for Your First IDE
```bash
python3 setup_workflow_system.py
```
**The setup script automatically detects your current IDE** and creates appropriate configuration files.

#### 3. Switch Between IDEs Seamlessly
**Working in VS Code:**
- Clone from GitHub → Run setup → Gets VS Code task integration
- Workflows available via `Ctrl+Shift+P` → Tasks: Run Task
- AI assistants (Cline, Cursor AI) can trigger workflows directly

**Working in Replit:**
- Import from GitHub → Run setup → Gets native Replit workflows  
- Workflows appear as clickable buttons in UI panel
- Hot reload and port management automatically configured

**Working in Other IDEs:**
- Clone from GitHub → Run setup → Gets universal shell scripts
- Terminal-based execution works in any IDE
- Compatible with all AI coding assistants

#### 4. Session Continuity Across IDEs
The system maintains complete session continuity when switching environments:
- Start work in VS Code → Session state automatically saved
- Switch to Replit → Previous session context loads automatically
- Agent handoffs work seamlessly across environment switches
- Shared project state, documentation, and version history

#### 5. IDE-Specific Configuration Details

**VS Code Setup Creates:**
```
.vscode/
├── tasks.json      # Workflow commands in Command Palette
├── settings.json   # Recommended IDE settings  
└── extensions.json # Suggested extensions
```

**Replit Setup Creates:**
```
.replit             # Native workflow buttons in UI
```

**Universal Setup Creates:**
```
.workflow_system/
└── scripts/        # Shell scripts for any terminal
```

#### 6. Additional Configuration (Optional)
- **WebSocket Setup** (Vite/React): Copy `client_templates/vite-client.js` to `public/`
- **Components.json** (shadcn/ui): Auto-detection and validation included
- **Custom Configuration**: Update `workflow_config.json` with your tech stack

#### 7. Validation & Testing
```bash
python3 validate_deployment.py  # Verify system integrity
```
**Test the system**: Say "Hi" to trigger the incoming agent workflow in any IDE

## 📝 Documentation Update Workflows

### Two Independent Documentation Systems

Arkival maintains **two separate documentation systems** that serve different purposes and update frequencies:

#### 1. Codebase Summary (Run Frequently)
**Purpose**: Track function documentation and detect missing breadcrumbs
```bash
python3 codebase_summary/update_project_summary.py --force
```

**When to Run**:
- After adding new functions or components
- When implementing new features
- During development to check documentation coverage
- **Run often** - this is your function documentation health check

**What it Updates**:
- `CODEBASE_SUMMARY.md` - Project structure and function analysis
- `ARCHITECTURE_DIAGRAM.md` - Auto-generated system diagrams
- `missing_breadcrumbs.json` - Functions lacking documentation
- `codebase_summary.json` - Raw analysis data

**Not Version Controlled**: These files are **independent of your project version** and update frequently

#### 2. Changelog (Run Infrequently)
**Purpose**: Document major changes and agent handoffs
```bash
python3 codebase_summary/update_changelog.py add --summary "Description of major changes"
```

**When to Run**:
- After completing major features
- Before ending development sessions
- When preparing agent handoffs
- For significant architectural changes
- **Run infrequently** - only for notable milestones

**What it Updates**:
- `CHANGELOG.md` - User-facing change history
- `changelog_summary.json` - Structured change data
- `PROJECT_CONFIG.md` changelog section - Project preferences record

**Version Controlled**: These track your project's evolution over time

### Recommended Usage Patterns

#### During Active Development
```bash
# Check documentation coverage frequently
python3 codebase_summary/update_project_summary.py --force

# Add functions with breadcrumb documentation
# @codebase-summary: Brief description
# Run summary again to verify documentation detected
```

#### At Development Milestones
```bash
# Document major changes
python3 codebase_summary/update_changelog.py add --summary "Implemented user authentication system"

# Or use agent workflow for session handoffs
python3 codebase_summary/agent_workflow_orchestrator.py outgoing --summary "Completed auth feature"
```

#### For Agent Handoffs
```bash
# Outgoing agent documents session
python3 codebase_summary/agent_workflow_orchestrator.py outgoing --summary "What was accomplished"

# Incoming agent loads context
python3 codebase_summary/agent_workflow_orchestrator.py incoming
```

### Key Differences Summary

| Aspect | Codebase Summary | Changelog |
|--------|------------------|-----------|
| **Frequency** | Run often (multiple times per day) | Run infrequently (major milestones) |
| **Purpose** | Function documentation health | Project evolution tracking |
| **Scope** | Technical implementation details | User-facing changes and features |
| **Audience** | Developers and AI agents | Users, stakeholders, new team members |
| **Version Sync** | Independent of project versions | Tied to project milestones |

## 🧪 Post-Setup Validation

After completing the setup, validate your installation:

```bash
python3 validate_deployment.py
```

**What this validation checks:**
- All required files are properly installed
- Configuration files are valid JSON syntax
- Core Python scripts are executable
- System dependencies are available
- Export package integrity is verified

**Success indicators:**
- All files show ✅ status
- No missing files reported
- "DEPLOYMENT VALIDATION SUCCESSFUL" message appears

**If validation fails:**
- Review specific error messages in the output
- Ensure the setup script completed successfully
- Verify Python 3.7+ is installed
- Check file permissions in the project directory

## 🚀 Post-Deployment Optimization

After successful deployment and initial setup, optimize for Claude Code prompt caching:

```bash
python3 validate_deployment.py cleanup
```

**What this cleanup does:**
- Removes language scan test files (16 files, ~500 tokens)
- Archives excessive history files (keeps last 5, removes 100+)
- **Total savings: ~5000 tokens per prompt cache hit**
- Preserves all functionality while improving performance

**When to run cleanup:**
- ✅ After successful GitHub clone and deployment
- ✅ When prompt caching performance becomes important
- ✅ Before production usage with high API volume
- ❌ NOT during development (test files help with language detection)

### Adding to Existing Projects

To integrate Arkival into an existing project:
```bash
# In your existing project directory
git clone https://github.com/spitfire-products/arkival.git temp-arkival
cp -r temp-arkival/* .
rm -rf temp-arkival
python3 setup_workflow_system.py
```

Or use as a Git submodule:
```bash
git submodule add https://github.com/spitfire-products/arkival.git arkival
cd arkival && python3 setup_workflow_system.py
```

## 📁 Package Contents

### Core Cross-Platform Files
- `codebase_summary/agent_workflow_orchestrator.py` - Main orchestration engine
- `codebase_summary/update_changelog.py` - Changelog management system with semantic versioning
- `codebase_summary/update_project_summary.py` - Generic project summary generator with components.json auto-updating
- `setup_workflow_system.py` - **Cross-platform setup script with complete workflow system**
- `workflow_config.json` - IDE-aware configuration system (v1.1.34-export)

### WebSocket Promise Rejection Mitigation
- `client_templates/vite-client.js` - WebSocket blocking system for Vite/HMR
- `client_templates/main-template.tsx` - React error boundary templates
- `WEBSOCKET_MITIGATION.md` - Complete implementation guide

### Components.json Auto-Update System
- `COMPONENTS_AUTO_UPDATE.md` - Auto-update system documentation
- Integrated path validation and version synchronization
- Safe auto-fixing with --fix-components flag

### Essential Utilities
- `git_hook_safe_utils.py` - Safe system operations without Git hook triggers
- `kill_port_process.py` - Process and port management utilities


### Testing and Validation Framework
- `validate_deployment.py` - Post-setup deployment validation and system verification

### IDE Integration Files (Auto-Generated)
- `.vscode/tasks.json` - VS Code/Cursor task definitions
- `.vscode/settings.json` - VS Code workspace settings
- `.gitpod.yml` - Gitpod environment configuration
- `.workflow_system/scripts/` - Universal shell scripts
- `SETUP_GUIDE.md` - IDE-specific setup instructions

### Documentation Templates
- `NEW_AGENT_GREETING.md` - Auto-greeting for new agents
- `DEVELOPER_ONBOARDING.md` - Project onboarding guide template
- `workflow_assets/` - Complete AI integration and workflow documentation

## 🎯 IDE-Specific Features

### Replit Integration
- **Native Workflows**: Integrated workflow panel
- **One-click execution**: Direct from UI
- **Automatic port management**: Built-in development server

### VS Code / Cursor Integration
- **Command Palette**: `Ctrl+Shift+P` → Run Task
- **Task Runner**: Integrated terminal execution
- **Input prompts**: Interactive session summaries
- **Extension recommendations**: Auto-suggested extensions

### Codespaces / Gitpod Integration
- **Cloud-native**: Works in browser environments
- **Pre-configured tasks**: Automatic environment setup
- **Terminal integration**: Full shell access

### Universal Shell Scripts
- **Cross-platform**: Works on any Unix-like system
- **Executable scripts**: Direct command-line execution
- **Parameterized**: Accept command-line arguments

## 🔧 Workflow Execution Methods

### Method 1: IDE Tasks (VS Code/Cursor/Codespaces)
```bash
# Press Ctrl+Shift+P, then:
Tasks: Run Task → Agent Incoming Workflow
Tasks: Run Task → Agent Outgoing Workflow
Tasks: Run Task → Update Changelog
```

### Method 2: Replit Workflows
```bash
# Click in workflows panel:
Agent Incoming Workflow
Agent Outgoing Workflow
```

### Method 3: Direct Terminal Commands
```bash
# Works in any IDE with terminal:
python3 codebase_summary/agent_workflow_orchestrator.py incoming
python3 codebase_summary/agent_workflow_orchestrator.py outgoing --summary "Session completed" --type completed
python3 codebase_summary/update_changelog.py add --summary "Added new features"
```

### Method 4: Shell Scripts (Universal)
```bash
# Executable scripts for any environment:
./.workflow_system/scripts/agent_incoming.sh
./.workflow_system/scripts/agent_outgoing.sh "Session summary" completed
./.workflow_system/scripts/update_changelog.sh "Change description"
```

## 🔄 AI Assistant Integration

### With Cline (VS Code)
1. Install Cline extension in VS Code
2. Run setup script - auto-detects VS Code environment
3. Use Cline with enhanced workflow context
4. Trigger workflows via VS Code Command Palette

### With Cursor AI
1. Open project in Cursor
2. Setup script auto-configures Cursor-specific tasks
3. Use Cursor's AI with full workflow context
4. Seamless agent handoffs maintain conversation history

### With Claude Code (Any IDE)
1. Setup script creates universal shell commands
2. Claude can execute workflows via terminal commands
3. Full compatibility with any Claude integration
4. Maintains consistent context across sessions

## 📋 Multi-Environment Deployment Guide

### From GitHub to Any IDE
1. **Deploy to GitHub**: Push Arkival to your repository
2. **Clone in Primary IDE**: `git clone` in VS Code, Replit, or other IDE
3. **Auto-Configure**: `python3 setup_workflow_system.py` detects environment
4. **Verify Setup**: `python3 validate_deployment.py` confirms configuration
5. **Test Workflows**: Say "Hi" to trigger incoming agent workflow

### Switch Between IDEs
1. **Same Repository**: Use same Git repository across all IDEs
2. **Run Setup in New IDE**: Script detects new environment automatically
3. **Load Previous Context**: Session state transfers seamlessly
4. **Continue Development**: Full project context preserved

### Configuration Files Created
**All IDEs Get:**
- `workflow_config.json` - Shared project configuration
- `codebase_summary/` - Agent orchestration system
- `changelog_summary.json` - Version history

**IDE-Specific Additions:**
- **VS Code**: `.vscode/tasks.json`, `.vscode/settings.json`
- **Replit**: `.replit` with native workflows
- **Others**: `.workflow_system/scripts/` shell scripts

## 🚨 IDE-Specific Notes

### For VS Code/Cursor Users
- Tasks appear in Command Palette
- Settings automatically configured
- Extension recommendations provided
- Terminal integration included

### For Replit Users  
- Workflows appear in native panel
- No additional setup required
- Works with existing .replit configuration

### For Cloud IDE Users (Codespaces/Gitpod)
- Pre-configured for cloud environments
- Works with browser-based terminals
- Automatic environment setup

### For Other IDEs
- Universal shell scripts provided
- Terminal-based execution
- Works with any IDE that supports terminal access

## 🔗 Multi-IDE & AI Assistant Workflow

### Cross-Platform Session Management
Arkival's unique strength is maintaining **complete session continuity** across different development environments:

#### GitHub → VS Code → Replit Workflow
1. **Deploy to GitHub** with complete Arkival system
2. **Clone in VS Code** → Setup detects environment → Creates VS Code tasks
3. **Start development session** → Agent state tracked in shared files
4. **Switch to Replit** → Same repository → Setup detects new environment
5. **Continue work seamlessly** → Previous session context loads automatically

#### AI Assistant Compatibility Across IDEs

**VS Code Integration:**
- **Cline**: Executes workflows via VS Code tasks (`Ctrl+Shift+P` → Tasks)
- **Cursor AI**: Native integration with task system
- **GitHub Copilot**: Compatible with all workflow commands

**Replit Integration:**
- **Native AI**: Can click workflow buttons in UI panel
- **Any AI**: Can execute shell commands in terminal

**Universal Integration:**
- **Claude Code**: Terminal command execution in any IDE
- **Any AI Assistant**: Shell script compatibility across all environments

### Shared Configuration Benefits
- **Same `workflow_config.json`** across all environments
- **Unified agent session state** in `codebase_summary/session_state.json`
- **Consistent project documentation** and version tracking
- **Cross-platform context preservation** for seamless handoffs

The workflow system maintains context consistency regardless of which IDE or AI assistant triggers the workflows, ensuring seamless knowledge transfer between different environments, AI agents, and human developers.

### 📨 Inter-Agent Messaging System

**Universal Message Path**: `modules/claude-code/msgs.md`

All AI assistants and agents can communicate using the standardized messaging system:

```bash
# Any agent can send messages
python3 modules/claude-code/msg.py add <agent_type> "message content"

# Read message history  
python3 modules/claude-code/msg.py read 10
```

**Supported Agent Types:**
- **cline_agent** (VS Code/Cline)
- **cursor_agent** (Cursor AI) 
- **replit_agent** (Replit AI)
- **copilot_agent** (GitHub Copilot)
- **windsurf_agent** (Windsurf)
- **ide_agent** (Generic IDE assistant)
- **developer** (Human developer)

This ensures consistent communication logging regardless of which IDE or AI assistant is being used.

## 🌟 Benefits of Cross-Platform Design

### For GitHub-Based Development
- **Deploy Once, Use Everywhere**: Single GitHub repository works across all IDEs
- **Environment Auto-Detection**: Setup script configures appropriately for each IDE
- **Session Continuity**: Switch between VS Code, Replit, and other IDEs seamlessly
- **Shared Project State**: Complete context preservation across environment switches

### For Teams & Collaboration  
- **IDE Flexibility**: Different team members can use different IDEs
- **AI Assistant Agnostic**: Compatible with all major AI coding tools
- **Consistent Workflows**: Same commands work regardless of environment
- **Zero Lock-in**: Portable across different setups and platforms

### For Development Workflow
- **Git Hook Safe**: Avoids "nothing to commit" process halts
- **File-Based Operations**: Primary method prevents Git interference  
- **Context Preservation**: Agent handoffs maintain conversation history
- **Future Proof**: Adapts to new IDE environments automatically

### Real-World Usage Examples
**Scenario 1:** Start project in VS Code with Cline → Deploy to Replit for collaboration → Return to VS Code for final touches
**Scenario 2:** Develop on local VS Code → Switch to Codespaces for cloud deployment → Test on Replit for sharing
**Scenario 3:** Team lead uses Cursor → Developer uses VS Code → Junior developer learns on Replit → All maintain shared context

## ⭐ Key Features

### Enhanced Automated Workflow Orchestration
- **Agent Handoff System**: Seamless knowledge transfer between AI agents
- **Comprehensive Context**: Complete project state capture and restoration
- **Version Correlation**: Synchronized versioning across all documentation
- **Automated Updates**: Smart detection of changes and automatic documentation
- **Interactive Testing Framework**: Comprehensive validation with user prompts
- **Enhanced Setup Workflows**: AI-powered configuration with testing integration
- **Deployment Validation**: Automated verification of export package integrity

### 🚀 Enhanced Analysis Capabilities
- **Multi-Language Code Analysis**: Python, TypeScript, JavaScript, Rust, Go, Java support
- **Architecture Pattern Detection**: Automatic identification of MVC, Component-Based, Microservices patterns
- **AI Integration Scanning**: Detection of OpenAI, Gemini, Grok, Claude, DeepSeek integrations
- **Database Readiness Assessment**: PostgreSQL, MySQL, SQLite, MongoDB analysis
- **Performance Metrics**: Complexity scoring, function density, documentation coverage
- **Component Analysis**: React/Vue component and hooks detection

## 🧪 Language Scan Tests

The `codebase_summary/language_scan_tests/` directory contains comprehensive test files that validate Arkival's multi-language function detection capabilities across 14+ programming languages.

### Test Coverage
- **16 comprehensive test files** covering major programming languages
- **100% documentation coverage** validation across entire project
- **Advanced pattern detection** including generics, async functions, operators, traits, protocols, and mixins

### Supported Languages
| Language | Functions | Features Tested |
|----------|-----------|----------------|
| Python | 51 | Classes, async, generators, decorators |
| PHP | 41 | Traits, namespaces, magic methods, closures |
| JavaScript | 30 | Arrow functions, classes, async, generators |
| C | 29 | Static, inline, variadic, pointers |
| Dart | 28 | Async, generics, extensions, streams |
| TypeScript | 25 | Generics, overloads, type guards |
| C++ | 25 | Templates, virtual, operators, namespaces |
| Kotlin | 25 | Suspend, inline, extensions, data classes |
| Swift | 24 | Async, throwing, protocols, extensions |
| Rust | 23 | Traits, impl blocks, async, const |
| Go | 21 | Generics, interfaces, goroutines, contexts |
| Ruby | 4 | Blocks, modules, metaprogramming |
| Java | 3 | Generics, lambdas, streams |
| React TSX | 2 | Components, hooks |

### Additional File Types
- **CSS**: Functions, variables, animations, media queries
- **SQL**: Stored procedures, triggers, window functions  
- **Vue**: Component methods, lifecycle hooks, computed properties

### Expected Output
When running the project summary script on the language scan tests, you should see output similar to:

```bash
python3 codebase_summary/update_project_summary.py --force

# The output will show function detection across ALL files:
# - Test files in codebase_summary/language_scan_tests/ 
# - Main Arkival system Python files with extensive breadcrumb documentation
# - 100% documentation coverage across the project
# - Language breakdown showing function counts detected:
#   • Python (includes both test and main system files)
#   • PHP, JavaScript, C, Dart, and other languages (test files)
#   • Complete validation of multi-language detection capability
```

This comprehensive test suite ensures Arkival can accurately detect and document functions across diverse technology stacks, making it suitable for deployment in any development environment.

## License

This project is licensed under the Attribution License - see the [LICENSE](LICENSE) file for details.

## Contributing

We welcome contributions! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## Security

For security concerns or vulnerability reports, please review our [Security Policy](SECURITY.md).

## Project Configuration

### For Different Project Types

**Web Applications:**
```json
{
  "technology_stack": ["React", "Node.js", "TypeScript"],
  "project_specific": {
    "main_files": ["package.json", "src/App.tsx", "server/index.ts"],
    "important_directories": ["src", "server", "public"]
  }
}
```

**Python Applications:**
```json
{
  "technology_stack": ["Python", "Flask/Django", "SQLAlchemy"],
  "project_specific": {
    "main_files": ["requirements.txt", "main.py", "app.py"],
    "important_directories": ["src", "models", "templates"]
  }
}
```

### Integration Guidelines

**For Existing Projects:**
1. Ensure `.gitignore` includes workflow cache files
2. Test system in development environment first
3. Configure cost optimization settings appropriately

**For Team Projects:**
1. Share Arkival package with all team members
2. Establish workflow conventions in team documentation
3. Set up consistent agent handoff procedures

## Troubleshooting

**Setup Issues:**
- Ensure Python 3.7+ is installed
- Check file permissions in project directory
- Verify no conflicting files exist

**Workflow Execution:**
- Run `python3 validate_deployment.py` for validation
- Check `workflow_config.json` syntax
- Verify all required files are present

**Getting Help:**
1. Check setup log output for specific error messages
2. Verify all required files using validation step
3. Review configuration for project-specific settings

## Support

- Documentation: Check the comprehensive guides in `workflow_assets/`
- Issues: Report bugs or request features via GitHub Issues
- Testing: Use the integrated test suite for validation
- Community: Engage through GitHub Discussions

## Acknowledgments

- Built for the AI-assisted development community
- Supports all major IDEs and coding assistants
- Designed for seamless human-AI collaboration
- **Route Analysis**: API endpoint categorization and documentation