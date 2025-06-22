# Arkival - Dynamic Architecture Analysis

*Auto-generated from codebase structure analysis*
*Version: 1.1.3 | Generated: 2025-06-22T00:06:25Z*

## ⚠️ Version Systems - IMPORTANT
| System | Current | Purpose | Updates |
|--------|---------|---------|---------|
| **Codebase Analysis** | v1.1.3 | Documentation scan version | Every `update_project_summary.py` run |
| **Changelog/Project** | vNone | Feature release version | Major milestones only |

**These are INDEPENDENT systems - version mismatch is NORMAL and EXPECTED**

## 🎯 30-Second Overview
| What | Details |
|------|---------|
| **System Type** | AI Agent Workflow Orchestration System for seamless knowledge transfer between AI agents and human developers |
| **Architecture** | Python Application |
| **State Management** | In-memory/Custom |
| **Current State** | operational |
| **Deployment Mode** | standalone |

## 🗺️ Where Should I Start?
```mermaid
graph TD
    START{What are you doing?} 
    START -->|New to project| README[Check README/Documentation]
    START -->|Adding feature| MAIN[Find main entry point]
    START -->|Fixing bug| TESTS[Run test suite]
    START -->|Understanding flow| STRUCTURE[Explore project structure]
    
    README --> DOCS[Read key documentation]
    MAIN --> CODE[Examine codebase patterns]
    TESTS --> DEBUG[Debug specific issues]
```

## 🔥 Critical Areas
- **Active Issues**: 0 current issues
- **Missing Docs**: 0 functions (see missing_breadcrumbs.json)
- **Complexity**: low complexity project
- **Critical Files**: session_state.json, workflow_config.json, missing_breadcrumbs.json

## Core System Architecture
```mermaid
graph TB
    subgraph "📁 Core Modules"
        M0[Client Templates]
        M1[Documentation Assets]
        M2[Documentation Assets/Workflow Assets]
        M3[Documentation Assets/Workflow Assets/Ai Integrations]
        M4[Documentation Assets/Project Templates]
        M5[Modules]

        M0 --> M1
        M1 --> M2
        M2 --> M3
        M3 --> M4
        M4 --> M5
    end

    subgraph "🏗 Architecture Patterns"
        P0[Workflow Orchestration]
        P1[AI Agent System]
        P2[Template System]
    end

    subgraph "📊 Technology Distribution"
        T1[Backend Files: 8]
        T2[Frontend Files: 2]
        T3[AI Integration: 5]
        T4[Total Functions: 64]
    end

    subgraph "🤖 Agent Context"
        A1[Documentation Coverage: 100.0%]
        A2[Files Analyzed: 9]
        A3[Missing Docs: 0]
    end
```

## Module Relationships
```mermaid
flowchart LR
    subgraph "Core System Flow"
        START[Project Entry] --> ANALYSIS[Code Analysis]
        ANALYSIS --> WORKFLOW[Workflow System]
        WORKFLOW --> OUTPUT[Agent Output]
    end
    
    subgraph "Documentation Layer"
        BREADCRUMBS[Function Breadcrumbs]
        COVERAGE[Coverage Tracking] 
        MISSING[Missing Analysis]
        
        BREADCRUMBS --> COVERAGE
        COVERAGE --> MISSING
    end
    
    ANALYSIS --> BREADCRUMBS
    MISSING --> OUTPUT
```

## 🔥 Critical Execution Paths
```mermaid
sequenceDiagram
    participant User
    participant Setup
    participant Orchestrator
    participant Summary
    participant State
    
    User->>Setup: setup_workflow_system.py
    Setup->>State: Creates workflow_config.json
    User->>Orchestrator: incoming agent workflow
    Orchestrator->>State: Loads session_state.json
    Orchestrator->>Summary: Triggers update_project_summary.py
    Summary->>State: Updates codebase_summary.json
    Note over State: All state in JSON files
```

## Directory Structure Map
```mermaid
graph TD
    ROOT[Arkival]
    ROOT --> D0[client templates]
    ROOT --> D1[documentation assets]
    ROOT --> D2[documentation assets/workflow assets]
    ROOT --> D3[documentation assets/workflow assets/ai integrations]
    ROOT --> D4[documentation assets/project templates]
    ROOT --> D5[modules]

    classDef coreModule fill:#e3f2fd,stroke:#1976d2
    classDef analysis fill:#f3e5f5,stroke:#7b1fa2
    classDef output fill:#e8f5e8,stroke:#388e3c
    
    class M0,M1,M2,M3,M4,M5 coreModule
    class T1,T2,T3,T4 analysis
    class A1,A2,A3 output
```

---
*Dynamic architecture analysis - reflects actual codebase structure*  
*Core Directories: 6 | Patterns: 3 | Coverage: 100.0%*
