# scan.ignore Configuration Guide

The `scan.ignore` file allows you to exclude directories and files from Arkival's codebase analysis. This improves performance and focuses the analysis on relevant code.

## 📍 File Location

- **Development Mode**: Place `scan.ignore` in your project root directory
- **Subdirectory Mode**: Place `scan.ignore` in the project root (same level as `/Arkival` folder)

## 📝 Format Rules

1. **One pattern per line**
2. **Comments**: Lines starting with `#` are ignored
3. **Case-sensitive**: Patterns match exactly as written
4. **Directory matching**: Both `dirname/` and `dirname` work the same
5. **Glob support**: Use `*` and `?` wildcards for complex patterns

## 🚫 Default Ignores (Always Applied)

These directories are ignored by default for performance:
```
.git
__pycache__
node_modules
.cache
.vscode
.idea
.DS_Store
vendor
build
dist
target
bin
obj
out
.next
.nuxt
coverage
test-results
.pytest_cache
```

## 📋 Common Ignore Patterns

### Performance Excludes
```
# Large dependency directories
node_modules/
vendor/
.venv/
venv/

# Build artifacts
build/
dist/
target/
out/
.output/

# IDE and editor files
.vscode/
.idea/
*.swp
*.swo
```

### File Type Excludes
```
# Logs and temporary files
*.log
*.tmp
*.temp
*.lock

# Archives and backups
*.zip
*.tar.gz
*.backup
*.bak

# Database files
*.db
*.sqlite
*.sqlite3
```

### Asset Directories
```
# Media files
assets/images/
public/uploads/
media/
uploads/
static/images/
images/
videos/
audio/

# Generated documentation
docs/_build/
docs/build/
site/
_site/
```

### Glob Patterns
```
# All test files
**/test_*
**/*_test.py
**/*.test.js

# All minified files
*.min.js
*.min.css

# All hidden files
.*
```

## 💡 Best Practices

1. **Start Conservative**: Begin with just the largest directories
2. **Test Impact**: Run the scanner before and after to see the difference
3. **Keep It Simple**: Use directory excludes rather than complex glob patterns when possible
4. **Document Custom Rules**: Add comments explaining project-specific exclusions

## 🔧 Example Configuration

```bash
# Performance excludes
node_modules/
.cache/
build/
dist/

# Development tools
.vscode/
.idea/
*.log

# Project specific
legacy_code/
deprecated/
third_party/
vendor/

# Large datasets
data/raw/
exports/
*.csv
*.json

# Generated files
coverage/
docs/build/
```

## 🚨 Impact on Analysis

When directories/files are ignored:
- ✅ **Faster scanning**: Reduced processing time
- ✅ **Smaller output**: More focused codebase_summary.json
- ✅ **Better AI context**: Excludes noise from analysis
- ⚠️ **Reduced coverage**: Some code won't be analyzed

## 🛠 Testing Your Configuration

1. Run: `python codebase_summary/update_project_summary.py`
2. Check the output for: `✅ Loaded X custom ignore patterns`
3. Compare file counts before/after adding patterns
4. Verify important code directories are still included

## 🔍 Troubleshooting

**Pattern not working?**
- Check file path case sensitivity
- Use relative paths from project root
- Test with simpler patterns first

**Still scanning too much?**
- Add parent directory patterns
- Use broader wildcards like `**/build/`

**Missing important files?**
- Review your patterns
- Remove overly broad exclusions
- Use more specific patterns