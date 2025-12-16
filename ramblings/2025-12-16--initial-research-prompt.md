# Initial Research Prompt

**Date:** 2025-12-16

## Original Task Request

> Please run knowledge researchers to find about tools that allow wrapping MCP servers and exposing them as CLI tools or REST/websocket/protobuf/etc servers, collect in .yaml files for each repo how many stars, repo url, is it reputable source etc, and `last-update:` as first field so we remember to track when we update information, and `repo-commit:` and `repo-url:` so we track on which repo version we based analysis.
>
> Goal of repo is to end up having github repo comparing different tools doing this kinds of things in different ways, so README.md is most high level intro and comparison with links to more markdown pages with more comparisons, there is GUIDELINES.md file, and we also may want additional file where we describe process, standard like about keeping data in .yaml files and generating from those, using `yq` e.g. to get data from multiple .yaml files for table easily, maybe even making ./scripts/ that will be shebang python3 files capable to e.g. generate comparison tables or bullet point lists later used in markdown documents.
>
> We keep track in some files how we do things, so e.g. `{script}.py` have `{script}.README.md`, we have `ramblings/` with notes about what we found, how we use scripts etc...
>
> We want to first knowledge researchers to find candidates, make .yaml files about each projects, stars etc, then make scripts `./clone-all.sh` that will clone all into `tmp` gitignored subdirectory, then do analyze repositories and update .yaml files with findings, so then final comparison analysis for production outputs can occur.
>
> We want to keep updating `spec.yaml` and `check-yaml.py` scripts to check if yaml files adhere to same standard, to avoid unnecessary overbloating of yaml files assume most fields will be optional, and start by adding this prompt to ramblings/
>
> We want to have nice research in this repo in nice to track git commits, comparing first reputation or how much one can trust given repositories, then features comparison, keep track, also consider in analysis what security properties we may want to check in source code to analyze safety of those tools, e.g. if we can check that all network connections they do are to configured MCP server and if they do not execute other commands or `eval` type of code unless expected...
>
> And of course if they support only MCP stdio transport or other MCP transports, and some MCP servers may require authentication so if they support this and how much...

## Key Research Goals

1. **Find tools** that wrap MCP servers and expose them as:
   * CLI tools
   * REST APIs
   * WebSocket servers
   * gRPC/protobuf servers
   * Other transports

2. **Track metadata** for each project:
   * GitHub stars
   * Repository URL
   * Commit hash for analysis version
   * Reputation/trustworthiness indicators
   * Last update timestamp

3. **Security analysis considerations**:
   * Network connection behavior (only to configured MCP servers?)
   * Presence of `eval` or command injection vectors
   * Code execution patterns
   * MCP transport support (stdio, SSE, other)
   * Authentication support for MCP servers

4. **Comparison dimensions**:
   * Feature comparison
   * Security properties
   * Transport support
   * Authentication mechanisms
   * Maturity and maintenance status

## Repository Structure Plan

```
.
├── README.md                    # High-level overview and comparison
├── GUIDELINES.md                # Project guidelines and standards
├── PROCESS.md                   # How we do research and update data
├── spec.yaml                    # YAML schema specification
├── .gitignore                   # Ignore tmp/ and other artifacts
├── projects/                    # YAML files for each project
│   └── {project-name}.yaml
├── scripts/
│   ├── clone-all.sh             # Clone all repos to tmp/
│   ├── check-yaml.py            # Validate YAML files against spec
│   ├── check-yaml.README.md     # Documentation for check-yaml.py
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
