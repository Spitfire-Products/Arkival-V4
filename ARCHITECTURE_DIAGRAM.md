# Arkival - Dynamic Architecture Analysis

*Auto-generated from codebase structure analysis*
*Version: 1.1.39 | Generated: 2025-06-18T22:13:31Z*

## Core System Architecture
```mermaid
graph TB
    subgraph "📁 Core Modules"
        M0[Client Templates]
        M1[Documentation Assets]
        M2[Documentation Assets/Workflow Assets]
        M3[Documentation Assets/Workflow Assets/Workflow Docs]
        M4[Documentation Assets/Workflow Assets/Ai Integrations]
        M5[Documentation Assets/Project Templates]

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
        T1[Backend Files: 14]
        T2[Frontend Files: 5]
        T3[AI Integration: 2]
        T4[Total Functions: 8017]
    end

    subgraph "🤖 Agent Context"
        A1[Documentation Coverage: 0.71%]
        A2[Files Analyzed: 635]
        A3[Missing Docs: 7960]
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

## Directory Structure Map
```mermaid
graph TD
    ROOT[Arkival]
    ROOT --> D0[client templates]
    ROOT --> D1[documentation assets]
    ROOT --> D2[documentation assets/workflow assets]
    ROOT --> D3[documentation assets/workflow assets/workflow docs]
    ROOT --> D4[documentation assets/workflow assets/ai integrations]
    ROOT --> D5[documentation assets/project templates]

    classDef coreModule fill:#e3f2fd,stroke:#1976d2
    classDef analysis fill:#f3e5f5,stroke:#7b1fa2
    classDef output fill:#e8f5e8,stroke:#388e3c
    
    class M0,M1,M2,M3,M4,M5 coreModule
    class T1,T2,T3,T4 analysis
    class A1,A2,A3 output
```

---
*Dynamic architecture analysis - reflects actual codebase structure*  
*Core Directories: 6 | Patterns: 3 | Coverage: 0.71%*
