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

## Creating & Updating Comparison Files

The `comparisons/` directory contains detailed analysis documents. Here's how to create and maintain them.

### Comparison File Types

| File | Content | Generation Method |
|------|---------|-------------------|
| `auto-generated.md` | Overview tables, stats | Fully automated via `generate-tables.py` |
| `features.md` | Feature comparison by category | Semi-automated + manual curation |
| `security.md` | Security analysis results | Manual analysis + YAML data |
| `transports.md` | Transport support details | Semi-automated from YAML |

### Creating features.md

This file compares features across project categories.

**Data Sources:**
- `features` array in each project YAML
- README analysis from cloned repos
- Ramblings research notes

**Structure:**
```markdown
# Feature Comparison

## Overview
Brief summary of feature landscape.

## By Category

### CLI Clients
| Project | Key Features | Language | Stars |
|---------|--------------|----------|-------|
| ... | ... | ... | ... |

### HTTP Bridges
...

## Feature Matrix
Cross-cutting features across all projects.

## Unique Capabilities
Standout features that differentiate projects.
```

**Update Process:**
1. Run `./scripts/generate-tables.py --by-category` for base data
2. Review each project's `features` array in YAML
3. Group similar features across projects
4. Highlight unique/differentiating features
5. Add context from README analysis

### Creating security.md

This file documents security analysis findings. **Requires manual code review.**

**Data Sources:**
- `security.*` fields in project YAML
- Manual code analysis (grep patterns from "Analyzing a Repository")
- Ramblings security notes

**Structure:**
```markdown
# Security Analysis

## Methodology
How we analyze security properties.

## Analysis Checklist
- [ ] eval/exec usage patterns
- [ ] subprocess/shell command handling
- [ ] Network isolation verification
- [ ] Input validation assessment
- [ ] Sandboxing support

## Findings by Category

### Safe Projects (No Dangerous Patterns)
Projects with verified safe code patterns.

### Projects Requiring Careful Configuration
Tools that intentionally execute commands (with user approval).

### Security-Focused Projects
Tools with built-in security features (PII detection, RBAC, etc.)

## Detailed Analysis

### project-name
- **Analyzed Commit:** abc1234
- **eval-usage:** none/safe/unsafe
- **subprocess-usage:** sanitized/unsafe
- **Network Isolation:** verified/partial/none
- **Notes:** Specific observations
```

**Update Process:**
1. Clone repos: `./scripts/clone-all.sh`
2. Run security grep patterns (see "Security Analysis" section above)
3. Manually review flagged code paths
4. Update project YAML with findings
5. Summarize in security.md

**Security Analysis Priority:**
1. High-star projects (most users at risk)
2. Projects handling sensitive data
3. Projects with HTTP/network exposure
4. Projects from non-reputable sources

### Creating transports.md

This file details transport protocol support.

**Data Sources:**
- `transports.*` fields in project YAML
- `transport-direction` field
- README/code analysis for implementation details

**Structure:**
```markdown
# Transport Support Details

## Transport Overview
| Transport | Description | Projects |
|-----------|-------------|----------|
| stdio | Standard I/O (universal) | 27 |
| HTTP | HTTP/Streamable HTTP | 14 |
| SSE | Server-Sent Events | 8 |
| WebSocket | WebSocket protocol | 2 |
| gRPC | gRPC/protobuf | 1 |

## By Transport Type

### stdio
All projects support stdio as the baseline MCP transport.

### HTTP Bridges
Projects that expose stdio MCP servers via HTTP.

| Project | Direction | Auth Support | Notes |
|---------|-----------|--------------|-------|
| ... | stdio→http | bearer | ... |

### SSE (Server-Sent Events)
...

### WebSocket
...

### gRPC
...

## Transport Combinations
Common transport combinations and use cases.

## Implementation Notes
Technical details about transport implementations.
```

**Update Process:**
1. Run `./scripts/generate-tables.py --by-transport` for base matrix
2. Review each project's transport implementation
3. Document direction (stdio→http, http→stdio, bidirectional)
4. Note authentication requirements per transport
5. Add implementation-specific details

### Keeping Comparisons Updated

**When to Update:**
- After adding new projects
- After updating project YAML with new analysis
- Monthly during maintenance cycle
- After significant project releases

**Update Workflow:**
```bash
# 1. Regenerate auto-generated.md
./scripts/generate-tables.py > comparisons/auto-generated.md

# 2. Check if manual comparisons need updates
git diff projects/  # See what changed

# 3. Update affected comparison files
# - If features changed → update features.md
# - If security analyzed → update security.md
# - If transports changed → update transports.md

# 4. Commit all changes together
git add comparisons/
git commit -m "Update comparison files

* Regenerated auto-generated.md
* Updated features.md with new project features
* Added security analysis for X projects"
```

### Placeholder Files (.empty.md)

Files with `.empty.md` suffix are templates awaiting content:
- They define the expected structure
- They're renamed to `.md` once populated
- Keep the `.empty.md` version as a template reference

```bash
# When ready to populate:
cp comparisons/features.empty.md comparisons/features.md
# Edit features.md with actual content
git add comparisons/features.md
git commit -m "Create features.md comparison document"
```

## Questions?

If you have questions about the process, check:

* `PROCESS.md` - Detailed workflow description
* `GUIDELINES.md` - Project standards
* `spec.yaml` - Full YAML schema
* `ramblings/` - Previous research notes
