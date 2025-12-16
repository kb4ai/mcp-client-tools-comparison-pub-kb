# Guidelines for MCP Wrapper Tools Comparison

## Purpose

This repository compares tools that wrap MCP (Model Context Protocol) servers and expose them as:

* CLI tools
* REST APIs
* WebSocket servers
* gRPC/protobuf servers
* Other interfaces/transports

## Repository Structure

```
.
├── README.md                    # High-level overview and comparison tables
├── GUIDELINES.md                # This file - project guidelines
├── PROCESS.md                   # How we collect and update data
├── spec.yaml                    # YAML schema specification
├── .gitignore                   # Ignore tmp/ and build artifacts
├── projects/                    # YAML files for each project
│   └── {project-name}.yaml
├── scripts/
│   ├── clone-all.sh             # Clone all repos to tmp/
│   ├── clone-all.README.md
│   ├── check-yaml.py            # Validate YAML files against spec
│   ├── check-yaml.README.md
│   ├── generate-tables.py       # Generate comparison tables
│   └── generate-tables.README.md
├── comparisons/                 # Detailed comparison documents
│   ├── features.md
│   ├── security.md
│   └── transports.md
├── ramblings/                   # Research notes and discoveries
│   └── YYYY-MM-DD--{topic}.md
└── tmp/                         # Cloned repositories (gitignored)
```

## Data Collection Standards

### YAML File Requirements

1. **File naming**: `projects/{repo-owner}--{repo-name}.yaml`
   * Use double-dash to separate owner from repo name
   * Example: `sparfenyuk--mcp-proxy.yaml`

2. **Required fields** (must be first):
   * `last-update`: YYYY-MM-DD format
   * `repo-url`: Full GitHub/GitLab URL

3. **Optional fields**: See `spec.yaml` for full schema

4. **Field ordering**: Keep tracking fields first, then group related fields

### Example YAML Structure

```yaml
last-update: "2025-12-16"
repo-commit: "abc123def"
repo-url: "https://github.com/owner/repo"

name: "Project Name"
description: "What it does"
language: "Python"
stars: 1234

category: "cli-client"

transports:
  stdio: true
  http: true

features:
  - Feature 1
  - Feature 2
```

## Comparison Dimensions

### 1. Reputation & Trust

* GitHub stars, forks, contributors
* Organization/author reputation
* Maintenance status (last commit, open issues)
* Whether from official source (Anthropic, Microsoft, Docker, etc.)

### 2. Feature Comparison

* Supported transports (stdio, SSE, HTTP, WebSocket, gRPC)
* Authentication methods
* Installation options
* Documentation quality

### 3. Security Properties

* Code execution patterns (eval, exec)
* Network isolation (only connects to configured endpoints?)
* Input validation/sanitization
* Subprocess/shell command handling
* Sandboxing support

### 4. Transport Support

* stdio ↔ HTTP bridges
* WebSocket support
* gRPC/protobuf converters
* Bidirectional vs unidirectional

## Script Conventions

1. Scripts in `scripts/` should be executable Python with shebang:
   ```python
   #!/usr/bin/env python3
   ```

2. Each script has a companion README:
   * `{script}.py` → `{script}.README.md`

3. Scripts should use `yq` or Python for YAML processing

4. Output should be suitable for inclusion in markdown documents

## Git Commit Practices

* Small, focused commits with clear messages
* Commit after each logical change
* Use present tense imperative mood
* Include attribution footer for AI-assisted work

## Updating Information

1. Update `last-update` field when modifying a project YAML
2. Update `repo-commit` if analysis was based on specific commit
3. Document significant findings in `ramblings/`
4. Re-run `check-yaml.py` after changes
