
# 🛠 Engineering Best Practices

*Generated by: documentation_assets/workflow_assets/workflow_docs/engineering_best_practices.md - Technical development standards and workflow guidelines*

## 📋 Overview

This guide establishes engineering standards for projects using Arkival, ensuring consistency between AI agents and human developers.

## 🎯 Core Principles

### 1. **Context-First Development**
- Always load project context before making changes
- Use workflow triggers to maintain session continuity
- Document decisions and rationale in breadcrumbs
- Preserve context for the next developer/agent

### 2. **Workflow Integration**
- Start sessions with incoming workflow ("Hi")
- End sessions with outgoing workflow (changelog update)
- Use natural language triggers consistently
- Maintain changelog discipline

### 3. **Cross-Platform Compatibility**
- Write code that works across all supported IDEs
- Use relative paths and environment-agnostic commands
- Test functionality in multiple environments
- Avoid IDE-specific dependencies in core logic

### 4. **Testing and Validation**
- Use the multi-language detection system for validation (23+ languages supported)
- Run function detection with `python3 codebase_summary/update_project_summary.py --force`
- Validate deployment readiness with `python3 validate_deployment.py`
- Validate export readiness with `python3 validate_export_readiness.py`
- Test language scan tests in `codebase_summary/language_scan_tests/` directory (excluded by default for performance)
- Validate deployment integrity before distribution

## 🔄 Development Workflow Standards

### Session Management
```bash
# 1. Start of session
# Say "Hi" or run: python3 codebase_summary/agent_workflow_orchestrator.py incoming

# 2. Review context
# - Check session_state.json for previous work
# - Review unresolved issues
# - Understand current project state

# 3. During development
# - Follow established patterns
# - Add breadcrumbs for new functionality
# - Test changes thoroughly

# 4. End of session
# Say "Update the changelog from the last entry" or run manual handoff
```

### 🚨 Shell Command Execution Protocol
**CRITICAL: Sequential execution with verification**

#### Command Execution Rules:
1. **Execute ONE command at a time**
2. **Wait for complete output** before generating next response
3. **Verify success** by checking:
   - Exit codes (0 = success)
   - Expected output patterns
   - File modifications that should occur
   - Version consistency
4. **Stop on failure** - do not continue if command fails
5. **Confirm results** before proceeding to next step

#### Command Execution Priority:
1. **PRIMARY**: Universal terminal commands (work in any environment)
2. **SECONDARY**: IDE-specific workflows (when available and appropriate)
3. **FALLBACK**: Direct file operations when shell commands fail

#### Example Proper Execution:
```bash
# ❌ WRONG: Don't batch commands without verification
python3 script1.py && python3 script2.py && python3 script3.py

# ✅ CORRECT: Execute, verify, then proceed
# Step 1: Execute single command
python3 codebase_summary/update_changelog.py remove-duplicates

# Step 2: Wait for output and verify:
# - Check for "Removed X duplicates" or "No duplicates found"
# - Ensure no error messages
# - Confirm expected file changes occurred

# Step 3: Only then proceed to next command
```

### Code Quality Standards

#### Function Documentation
```python
def process_ai_response(response: str, context: dict) -> ProcessedResponse:
    """
    # @codebase-summary: AI response processing pipeline
    - Parses and validates AI model responses
    - Handles error cases and malformed responses
    - Integrates with workflow orchestration system
    - Used by: agent communication, response validation, workflow processing
    """
    # Implementation with clear error handling
    try:
        # Process response
        pass
    except Exception as e:
        # Log error with context
        logger.error(f"AI response processing failed: {e}", extra={"context": context})
        raise ProcessingError(f"Failed to process AI response: {e}")
```

#### Error Handling
```python
# Standard error handling pattern
try:
    result = risky_operation()
except SpecificException as e:
    # Log with context
    logger.error(f"Operation failed: {e}", extra={
        "operation": "risky_operation",
        "context": current_context
    })
    # Provide meaningful error to user
    return {"error": "Operation failed", "details": str(e)}
except Exception as e:
    # Unexpected errors
    logger.exception("Unexpected error in risky_operation")
    return {"error": "Unexpected error occurred"}
```

#### Configuration Management
```python
# Use environment variables for configuration
import os
from typing import Optional

def get_config(key: str, default: Optional[str] = None) -> str:
    """
    # @codebase-summary: Centralized configuration management
    - Handles environment variables with fallbacks
    - Provides consistent config access across the application
    - Logs missing critical configuration
    """
    value = os.environ.get(key, default)
    if value is None:
        logger.warning(f"Missing configuration for {key}")
    return value
```

## 📁 File Organization Standards

### Directory Structure
```
project/
├── codebase_summary/           # Workflow system files
│   ├── agent_workflow_orchestrator.py
│   ├── update_changelog.py
│   └── *.json files
├── src/                        # Source code
│   ├── components/             # UI components
│   ├── services/               # Business logic
│   ├── utils/                  # Utility functions
│   └── types/                  # Type definitions
├── tests/                      # Test files
├── docs/                       # Documentation
└── workflow_config.json        # Project configuration
```

### Naming Conventions
- **Files**: `kebab-case.ts`, `snake_case.py`
- **Functions**: `camelCase` (JS/TS), `snake_case` (Python)
- **Classes**: `PascalCase` (all languages)
- **Constants**: `UPPER_SNAKE_CASE`
- **Components**: `PascalCase.tsx`

### Import Organization
```typescript
// External libraries
import React from 'react';
import { useState, useEffect } from 'react';

// Internal utilities
import { formatDate, validateInput } from '../utils';

// Components
import Button from './Button';
import Modal from './Modal';

// Types
import type { User, Project } from '../types';
```

## 🧪 Testing Standards

### Test Structure
```python
def test_workflow_orchestrator():
    """
    # @codebase-summary: Workflow orchestrator integration test
    - Tests complete agent handoff cycle
    - Validates session state persistence
    - Ensures changelog integration works
    """
    # Arrange
    orchestrator = AgentWorkflowOrchestrator()
    test_summary = "Test session summary"
    
    # Act
    result = orchestrator.trigger_outgoing_agent_workflow(test_summary)
    
    # Assert
    assert result["steps_completed"]
    assert "session_state_updated" in result["steps_completed"]
    assert len(result["errors"]) == 0
```

### AI Integration Testing
```python
def test_ai_service_with_mock():
    """Test AI service with mocked responses to avoid API costs"""
    with patch('ai_service.call_model') as mock_call:
        mock_call.return_value = "Expected response"
        
        result = process_ai_request("test prompt")
        
        assert result == "Expected response"
        mock_call.assert_called_once()
```

## 🔧 Performance Guidelines

### API Cost Optimization
```python
# Cache expensive AI calls
from functools import lru_cache

@lru_cache(maxsize=100)
def generate_ai_response(query: str) -> str:
    """
    # @codebase-summary: AI response generation with caching
    - Caches AI responses to avoid repeated API calls
    - Reduces AI model costs for frequently accessed queries
    - Cache size tuned for typical workflow patterns
    """
    return call_ai_model(f"Process query: {query}")
```

### Database Optimization
```python
# Batch operations when possible
def update_multiple_files(file_updates: List[FileUpdate]) -> bool:
    """
    # @codebase-summary: Batch file update optimization
    - Processes multiple file updates in single transaction
    - Reduces I/O operations and improves performance
    - Used by: bulk documentation updates, batch processing
    """
    with file_system.transaction():
        for update in file_updates:
            file_system.update_file(update)
    return True
```

## 🔐 Security Practices

### API Key Management
```python
# Never hardcode API keys
API_KEY = os.environ.get('OPENAI_API_KEY')
if not API_KEY:
    raise EnvironmentError("OPENAI_API_KEY environment variable required")

# Use secure headers
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}
```

### Input Validation
```python
def validate_user_input(input_data: str) -> str:
    """
    # @codebase-summary: User input validation and sanitization
    - Sanitizes user input to prevent injection attacks
    - Validates input length and format
    - Used by: all user-facing input handlers
    """
    if not input_data or len(input_data) > 10000:
        raise ValueError("Invalid input length")
    
    # Remove potentially dangerous content
    sanitized = re.sub(r'[<>"\']', '', input_data)
    return sanitized.strip()
```

## 📊 Monitoring and Logging

### Structured Logging
```python
import logging
import json

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def log_workflow_event(event_type: str, details: dict):
    """
    # @codebase-summary: Structured workflow event logging
    - Logs workflow events in consistent format
    - Enables monitoring and debugging of agent handoffs
    - Integrates with external monitoring systems
    """
    logger.info(f"Workflow event: {event_type}", extra={
        "event_type": event_type,
        "details": details,
        "timestamp": datetime.now().isoformat()
    })
```

### Performance Monitoring
```python
import time
from functools import wraps

def monitor_performance(func):
    """
    # @codebase-summary: Performance monitoring decorator
    - Tracks function execution time
    - Logs slow operations for optimization
    - Used on: AI service calls, file operations
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            if execution_time > 5.0:  # Log slow operations
                logger.warning(f"Slow operation: {func.__name__} took {execution_time:.2f}s")
            
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Operation failed: {func.__name__} after {execution_time:.2f}s - {e}")
            raise
    
    return wrapper
```

## 🤖 AI Agent Collaboration

### Context Sharing
```python
def prepare_ai_context(session_data: dict) -> dict:
    """
    # @codebase-summary: AI context preparation for agent handoffs
    - Packages session data for next AI agent
    - Includes relevant project state and decisions
    - Optimizes context size to reduce token costs
    """
    return {
        "project_state": session_data.get("current_state"),
        "recent_changes": session_data.get("changes", [])[-5:],  # Last 5 changes
        "unresolved_issues": session_data.get("unresolved_issues", []),
        "next_priorities": session_data.get("priorities", [])
    }
```

### Decision Documentation
```python
def document_technical_decision(decision: str, rationale: str, alternatives: List[str]):
    """
    # @codebase-summary: Technical decision documentation
    - Records important technical decisions for future reference
    - Helps AI agents understand previous reasoning
    - Prevents repeated evaluation of settled decisions
    """
    decision_record = {
        "timestamp": datetime.now().isoformat(),
        "decision": decision,
        "rationale": rationale,
        "alternatives_considered": alternatives,
        "impact": "Document expected impact here"
    }
    
    # Add to project documentation
    with open("technical_decisions.json", "a") as f:
        json.dump(decision_record, f)
        f.write("\n")
```

## 🔄 Deployment Practices

### Environment Configuration
```python
# Environment-specific configuration
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')

if ENVIRONMENT == 'production':
    # Production settings
    DEBUG = False
    DATABASE_URL = os.environ.get('PROD_DATABASE_URL')
else:
    # Development settings
    DEBUG = True
    DATABASE_URL = os.environ.get('DEV_DATABASE_URL', 'sqlite:///dev.db')
```

### Health Checks
```python
def health_check() -> dict:
    """
    # @codebase-summary: Application health check endpoint
    - Validates all critical services are operational
    - Used by: deployment systems, monitoring tools
    - Returns: Service status and version information
    """
    return {
        "status": "healthy",
        "version": get_app_version(),
        "services": {
            "file_system": check_file_system_access(),
            "ai_service": check_ai_service_availability(),
            "workflow_system": check_workflow_system_status()
        }
    }
```

## 📚 Documentation Standards

### README Requirements
Every project should include:
- Setup instructions for all supported IDEs
- Workflow system usage guide
- API key and environment variable setup
- Common troubleshooting steps

### Code Comments
```python
# Use comments for complex business logic
# @codebase-summary: sections for important functions
# TODO: Use TODO comments for known improvements
# FIXME: Use FIXME for known issues that need addressing
```

### Changelog Discipline
- Update changelog for all significant changes using `python3 codebase_summary/update_changelog.py`
- Use workflow triggers consistently (`python3 codebase_summary/agent_workflow_orchestrator.py`)
- Include breaking change notes
- Maintain version correlation between codebase and changelog versions

---

## 🚨 Git Hook Avoidance - Best Practice

### Command Execution Hierarchy:
1. **PRIMARY**: Universal File-Based Operations
   - Read `codebase_summary.json` for comprehensive project status
   - Read/write files directly instead of shell commands
   - Parse project state through file analysis
   - Use `python3 codebase_summary/update_project_summary.py` for status updates

2. **SECONDARY**: IDE-Specific Workflows (when available)
   - Use IDE workflow panels when present (Replit, VS Code tasks, etc.)
   - Prevents Git hook interference and process halts
   - Environment-specific optimization

3. **FALLBACK**: Direct Shell Commands
   - Only when file operations AND workflows fail
   - Expect potential "nothing to commit" halts
   - May require manual intervention

### Why This Matters:
- Git hooks trigger on shell command execution
- Cause "nothing to commit" messages that terminate processes
- Prevent waiting for command completion
- Interrupt AI agent workflows

## 📝 File Edit Batching and Token Limit Management

### Output Token Awareness (CRITICAL)
AI agents MUST be aware of their platform's output token limits:

1. **Know Your Limits**: Understand the exact token limit for your platform
2. **Ask When Uncertain**: If unsure about token limits, ask the user immediately
3. **Reserve Safety Buffer**: Never exceed 90% of token capacity for file edits
4. **Prevent File Truncation**: Incomplete files cause compilation errors and workflow disruption

### File Edit Batching Rules
```
Maximum Token Usage for File Edits = Platform_Limit × 0.90
```

#### Token Limit Examples:
- **Claude 3.5 Sonnet**: ~200K tokens → Max 180K for file edits
- **GPT-4**: ~128K tokens → Max 115K for file edits  
- **Gemini Pro**: ~128K tokens → Max 115K for file edits
- **Custom Platforms**: Ask user for specific limits

#### Batching Strategy:
1. **Estimate token usage** before proposing file changes
2. **Group related changes** into single operations when possible
3. **Split large changes** across multiple responses if needed
4. **Prioritize critical files** in first batch
5. **Verify completion** before proceeding to next batch

#### File Change Prioritization:
```
High Priority (First Batch):
- Core functionality files
- Type definitions and schemas
- Critical configuration files

Medium Priority (Second Batch):  
- UI components and styling
- Helper utilities
- Test files

Low Priority (Final Batch):
- Documentation updates
- Comment additions
- Non-critical optimizations
```

### Implementation Guidelines:
```typescript
// Example: Check estimated token usage before file changes
const estimatedTokens = calculateTokenUsage(proposedChanges);
const tokenLimit = getPlatformTokenLimit(); // Ask user if unknown
const safeLimit = tokenLimit * 0.90;

if (estimatedTokens > safeLimit) {
  // Split into multiple batches
  const batches = splitIntoSafeBatches(proposedChanges, safeLimit);
  processBatch(batches[0]); // Process first batch only
} else {
  // Safe to process all changes
  processAllChanges(proposedChanges);
}
```

## 🎯 Summary

These best practices ensure:
- **Git Hook Safety**: Primary focus on avoiding process halts
- **Consistent development experience** across AI agents and human developers
- **Maintainable codebase** with proper documentation and structure  
- **Efficient workflow integration** that reduces development overhead
- **Quality code** that follows established patterns and standards

Follow these guidelines to maximize the benefits of Arkival while avoiding Git-related interruptions and ensure smooth collaboration across your development team.

## 📝 Documentation Migration and Deprecation

### Documentation Organization
All documentation has been consolidated into the main workflow system structure for better accessibility and maintenance.

#### Migration Checklist:
- ✅ **Engineering Best Practices**: Current document (this file)
- ✅ **Agent Onboarding**: Available in `AGENT_GUIDE.md` and `modules/claude-code/CLAUDE.md`
- ✅ **Breadcrumb Guide**: Integrated into workflow system (current schema: `# @codebase-summary:`)
- ✅ **Changelog Guide**: Incorporated into agent workflow orchestrator
- ✅ **Codebase Summary Guide**: Updated for current workflow system
- ✅ **Architecture Diagrams**: Auto-generated in `ARCHITECTURE_DIAGRAM.md`
- ✅ **Documentation Coverage**: Achieved 100% function documentation

#### New Agent Onboarding Priority:
The immediate new agent onboarding workflow should prioritize:

1. **Primary Documentation** (Current System):
   - `AGENT_GUIDE.md` - Comprehensive agent workflow guide
   - `CONTRIBUTING.md` - Development standards and contribution guidelines
   - This file (`engineering_best_practices.md`) - Technical standards
   - AI integration docs (if applicable): `modules/claude-code/CLAUDE.md` or equivalent

2. **Workflow System** (Export Package):
   - Agent workflow orchestration system
   - Cross-platform compatibility documentation
   - Cost optimization guidelines

3. **Legacy Reference** (Deprecated - Use Only When Needed):
   - Architecture diagrams for system understanding
   - Future work planning documents
   - Historical context documentation

#### Current System Notes:
- **Use current** breadcrumb schema: `# @codebase-summary:` with bullet points
- **Reference** auto-generated documentation in `ARCHITECTURE_DIAGRAM.md` and `CODEBASE_SUMMARY.md`
- **Follow** workflow orchestration patterns established in `codebase_summary/agent_workflow_orchestrator.py`
- **Maintain** 100% documentation coverage as established in current system

---

*This guide is living documentation - update it as new patterns and practices emerge in your project.*
