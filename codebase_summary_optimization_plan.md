# Codebase Summary Optimization Plan

## Problem
- Current codebase_summary.json can balloon to 70k+ tokens in large projects
- The `code_analysis` section alone can be 29KB+
- Main culprit: Storing individual function names and file-by-file details

## Current Structure Issues

### 1. File Analysis Array (Biggest Issue)
```json
"file_analysis": [
  {
    "file": "path/to/file.py",
    "language": ".py",
    "function_count": 10,
    "documented_count": 5,
    "functions": ["func1", "func2", ...],  // Up to 15 names per file
    "missing_breadcrumbs": ["func3", "func4", ...],  // Up to 15 names
    "lines_of_code": 500
  },
  // ... repeated for EVERY code file
]
```

### 2. Redundant Storage
- Function names stored multiple times (in file_analysis and missing_breadcrumbs)
- File paths repeated throughout
- Language breakdown duplicates file counts

## Proposed Optimizations

### 1. **Aggregate-Only Approach** (Most Aggressive)
Remove `file_analysis` array entirely, keep only aggregated stats:
```json
"code_analysis": {
  "total_functions": 625,
  "documented_functions": 412,
  "documentation_coverage": 65.9,
  "total_files_analyzed": 33,
  "total_lines_of_code": 12500,
  "language_breakdown": {
    ".py": {"files": 15, "functions": 200},
    ".js": {"files": 10, "functions": 150}
  }
}
```
**Token Reduction**: ~90% (from 29KB to ~3KB)

### 2. **Top-Level Summary with Hotspots** (Balanced)
Keep aggregates + identify only problematic files:
```json
"code_analysis": {
  "summary": {
    "total_functions": 625,
    "documented_functions": 412,
    "documentation_coverage": 65.9
  },
  "documentation_gaps": [
    {"file": "src/utils.py", "undocumented": 15},
    {"file": "src/api.py", "undocumented": 12}
    // Only top 5-10 files with most missing docs
  ],
  "language_breakdown": {
    ".py": {"files": 15, "functions": 200}
  }
}
```
**Token Reduction**: ~80% (from 29KB to ~6KB)

### 3. **Configurable Verbosity Levels**
Add a verbosity parameter to control detail level:
- `--summary-level minimal`: Aggregates only (3KB)
- `--summary-level standard`: Aggregates + top issues (6KB) [DEFAULT]
- `--summary-level detailed`: Current behavior (29KB+)
- `--summary-level full`: Everything including all function names

### 4. **Smart Exclusions**
- Skip test files by default (`test_*.py`, `*.test.js`)
- Skip generated files (`*.min.js`, `*_pb2.py`)
- Configurable ignore patterns via `.arkivalignore` file
- Max file size limits (skip files > 100KB)

### 5. **Missing Breadcrumbs Optimization**
Instead of storing function names:
```json
"missing_breadcrumbs_summary": {
  "total_missing": 213,
  "by_directory": {
    "src/": 45,
    "lib/": 30,
    "utils/": 25
  },
  "critical_files": [
    "src/main.py",  // Only list files with >10 missing
    "src/api.py"
  ]
}
```

### 6. **Separate Detail Files**
- Keep `codebase_summary.json` minimal (~5-10KB)
- Generate `codebase_analysis_details.json` for full analysis
- Only load details when specifically requested

## Implementation Priority

1. **Quick Win**: Remove function name arrays (Line 1156-1157)
   - Change: `"functions": functions[:15]` → `"functions": []`
   - Change: `"missing_breadcrumbs": missing_breadcrumbs[:15]` → Remove entirely
   - Immediate 50% reduction

2. **Medium**: Implement aggregate-only mode
   - Replace `file_analysis` array with summary stats
   - 80% reduction

3. **Long-term**: Add configurable verbosity
   - Allows users to choose detail level
   - Backward compatible

## Usage Examples

```bash
# Minimal summary for AI agents (default)
python update_project_summary.py

# Detailed analysis for debugging
python update_project_summary.py --summary-level detailed

# With exclusions
python update_project_summary.py --exclude "tests/**,build/**"

# Generate separate detail file
python update_project_summary.py --with-details
```

## Expected Results

For a typical project with 600+ functions:
- Current: 70KB+ (too large for efficient AI processing)
- Optimized (standard): 5-10KB (perfect for AI context)
- Optimized (minimal): 2-3KB (ultra-efficient)

This maintains the value of codebase analysis while making it practical for AI agent handoffs.