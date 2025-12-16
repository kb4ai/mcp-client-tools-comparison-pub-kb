# Contributing Guide

This document provides step-by-step instructions for maintaining and updating this repository.

## Quick Reference

| Task | Command |
|------|---------|
| Clone all repos | `./scripts/clone-all.sh` |
| Update existing clones | `./scripts/clone-all.sh --update` |
| Validate YAML files | `./scripts/check-yaml.py` |
| Validate strictly | `./scripts/check-yaml.py --strict` |
| Generate tables | `./scripts/generate-tables.py > comparisons/auto-generated.md` |

## Common Workflows

### 1. Adding a New Project

```bash
# 1. Create YAML file with naming convention: {owner}--{repo}.yaml
touch projects/newowner--newrepo.yaml

# 2. Add required fields (minimum viable entry)
cat > projects/newowner--newrepo.yaml << 'EOF'
last-update: "2025-12-16"
repo-url: "https://github.com/newowner/newrepo"

name: "newrepo"
description: "Brief description of what it does"
EOF

# 3. Clone the repo for analysis
./scripts/clone-all.sh

# 4. Analyze and fill in remaining fields
# See "Analyzing a Repository" section below

# 5. Validate your YAML
./scripts/check-yaml.py projects/newowner--newrepo.yaml

# 6. Regenerate comparison tables
./scripts/generate-tables.py > comparisons/auto-generated.md

# 7. Commit your changes
git add projects/newowner--newrepo.yaml comparisons/auto-generated.md
git commit -m "Add newowner/newrepo to comparison

* Category: {category}
* Stars: {stars}
* Key features: {features}"
```

### 2. Updating an Existing Project

When a project releases new features or you need to refresh data:

```bash
# 1. Update the clone
./scripts/clone-all.sh --update

# 2. Get current date for last-update field
date +%Y-%m-%d

# 3. Get current commit hash
cd tmp/owner--repo && git rev-parse --short HEAD && cd ../..

# 4. Update the YAML file with new info:
#    - last-update: current date
#    - repo-commit: current HEAD
#    - stars: check GitHub
#    - features: check README for new features
#    - security.*: re-analyze if significant changes

# 5. Validate and regenerate tables
./scripts/check-yaml.py
./scripts/generate-tables.py > comparisons/auto-generated.md
```

### 3. Periodic Maintenance (Monthly)

```bash
# 1. Update all clones
./scripts/clone-all.sh --update

# 2. Refresh star counts from GitHub
# Visit each repo on GitHub or use GitHub API:
for f in projects/*.yaml; do
  url=$(yq '.repo-url' "$f")
  echo "Check: $url"
done

# 3. Update last-commit dates
for dir in tmp/*/; do
  name=$(basename "$dir")
  last=$(cd "$dir" && git log -1 --format='%Y-%m-%d')
  echo "$name: $last"
done

# 4. Regenerate tables
./scripts/generate-tables.py > comparisons/auto-generated.md

# 5. Commit updates
git add projects/ comparisons/
git commit -m "Monthly refresh: update star counts and commit dates"
```

### 4. Bulk Update Star Counts (with GitHub CLI)

```bash
# If you have `gh` CLI installed:
for f in projects/*.yaml; do
  url=$(yq '.repo-url' "$f")
  repo=$(echo "$url" | sed 's|https://github.com/||')
  if [ -n "$repo" ]; then
    stars=$(gh api "repos/$repo" --jq '.stargazers_count' 2>/dev/null || echo "?")
    echo "$f: $stars stars"
  fi
done
```

## Analyzing a Repository

When you clone a new repo, perform this analysis:

### Step 1: Basic Information

```bash
cd tmp/owner--repo

# Get repo info
cat README.md | head -50

# Check language
find . -name "*.py" -o -name "*.go" -o -name "*.ts" -o -name "*.js" | head -20

# Check license
cat LICENSE 2>/dev/null || cat LICENSE.md 2>/dev/null
```

### Step 2: Transport Support

Look for evidence of transport support:

```bash
# stdio (almost always present)
grep -r "stdio" --include="*.py" --include="*.go" --include="*.ts" .

# HTTP
grep -ri "http\|server\|express\|fastapi\|gin" --include="*.py" --include="*.go" --include="*.ts" .

# SSE (Server-Sent Events)
grep -ri "sse\|server-sent\|event-stream" --include="*.py" --include="*.go" --include="*.ts" .

# WebSocket
grep -ri "websocket\|ws://" --include="*.py" --include="*.go" --include="*.ts" .

# gRPC
grep -ri "grpc\|protobuf\|\.proto" .
```

### Step 3: Security Analysis

**CRITICAL**: Check for dangerous code patterns:

```bash
# Python: eval/exec
grep -rn "eval(\|exec(\|compile(" --include="*.py" .

# Python: subprocess with shell=True
grep -rn "shell=True\|os.system\|os.popen" --include="*.py" .

# JavaScript/TypeScript: eval
grep -rn "eval(\|Function(" --include="*.js" --include="*.ts" .

# Go: os/exec
grep -rn "exec.Command" --include="*.go" .

# Check if user input flows to these (manual review required)
```

### Step 4: Authentication Support

```bash
# OAuth
grep -ri "oauth\|oauth2" .

# Bearer tokens
grep -ri "bearer\|authorization.*header\|api.key" .

# API keys
grep -ri "api_key\|apikey\|x-api-key" .
```

### Step 5: Documentation Quality

Check for:

* README.md - exists and comprehensive?
* Examples - are there usage examples?
* API docs - is the API documented?
* Tests - are there test files?

```bash
# Count test files
find . -name "*test*" -o -name "*spec*" | wc -l

# Check for examples
ls -la examples/ 2>/dev/null || ls -la example/ 2>/dev/null
```

### Step 6: Fill in YAML

Based on your analysis, update the YAML file:

```yaml
last-update: "YYYY-MM-DD"
repo-commit: "abc1234"
repo-url: "https://github.com/owner/repo"

name: "repo-name"
description: "What it does in one line"
language: "Python"
stars: 1234
license: "MIT"
last-commit: "YYYY-MM-DD"

category: "cli-client"  # See spec.yaml for valid categories
reputable-source: false
organization: ""  # Only if from known org

transports:
  stdio: true
  sse: false
  http: true
  websocket: false
  grpc: false

authentication:
  oauth: false
  bearer: true
  api-key: false

features:
  - "Feature 1"
  - "Feature 2"

installation:
  pip: "package-name"  # or npm, brew, go-install, etc.

security:
  analyzed: true
  analysis-commit: "abc1234"
  eval-usage: "none"  # none, safe, unsafe
  subprocess-usage: "safe"  # none, safe, unsafe
  network-isolation: "verified"  # verified, partial, none
  input-validation: "thorough"  # thorough, basic, none
  sandboxing: false
  notes:
    - "Specific security observation"

documentation:
  readme: true
  api-docs: false
  examples: true
  tests: true

notes:
  - "Any other relevant information"
```

## Valid Categories

From `spec.yaml`:

* `cli-client` - Command-line interface for MCP
* `http-bridge` - stdio ↔ HTTP/SSE conversion
* `websocket-bridge` - stdio ↔ WebSocket
* `grpc-bridge` - MCP ↔ gRPC/protobuf
* `rest-api-bridge` - OpenAI-compatible REST APIs
* `proxy-aggregator` - Multi-server proxy
* `enterprise-gateway` - Production-ready gateway
* `kubernetes-integration` - K8s-native MCP
* `docker-integration` - Docker-native MCP
* `specialized-adapter` - CLI wrapper or adapter
* `official-tool` - Official Anthropic/MCP tool

## Reputable Sources

Mark `reputable-source: true` only for projects from:

* Anthropic / modelcontextprotocol org
* Microsoft
* Docker
* Google
* Major security firms (NCC Group, Lasso, etc.)
* Established open-source foundations
* Well-known companies with verified GitHub orgs

## Git Commit Practices

Follow these commit conventions:

```bash
# Adding a new project
git commit -m "Add owner/repo to comparison

* Category: cli-client
* Stars: 500
* Key feature: interactive shell mode"

# Updating existing project
git commit -m "Update owner/repo with security analysis

* Analyzed commit abc1234
* No dangerous patterns found
* Added authentication details"

# Monthly refresh
git commit -m "Monthly refresh: update star counts

* Updated 27 projects with current star counts
* Regenerated comparison tables"

# Fixing data
git commit -m "Fix owner/repo transport info

* Corrected: supports SSE, not just HTTP
* Verified against v2.0 release"
```

## Research Notes

When you discover something interesting, document it:

```bash
# Get current date
date +%Y-%m-%d

# Create rambling file
vim ramblings/$(date +%Y-%m-%d)--topic-name.md
```

Template for ramblings:

```markdown
# Topic Name

**Date:** YYYY-MM-DD
**Context:** Why you're writing this

## Findings

Your observations...

## Code Examples

```language
code snippets if relevant
```

## Recommendations

What to do with this information...
```

## Troubleshooting

### YAML Validation Fails

```bash
# Check specific file
./scripts/check-yaml.py projects/problematic-file.yaml

# Common issues:
# - Missing required fields (last-update, repo-url)
# - Invalid date format (must be YYYY-MM-DD in quotes)
# - Invalid URL format
# - stars must be integer, not string
```

### Clone Script Fails

```bash
# Try shallow clone for large repos
./scripts/clone-all.sh --shallow

# Skip existing repos
./scripts/clone-all.sh  # automatically skips existing

# Force update
./scripts/clone-all.sh --update
```

### Script Permission Denied

```bash
chmod +x scripts/*.sh scripts/*.py
```

## Questions?

If you have questions about the process, check:

* `PROCESS.md` - Detailed workflow description
* `GUIDELINES.md` - Project standards
* `spec.yaml` - Full YAML schema
* `ramblings/` - Previous research notes
