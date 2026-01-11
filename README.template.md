# MCP Ecosystem Tools Comparison

A comprehensive comparison of tools in the **MCP (Model Context Protocol)** ecosystem - from CLI clients to transport bridges to enterprise gateways.

## Quick Navigation

| I want to... | Go here |
|--------------|---------|
| **Find the right tool for me** | [Interactive Decision Tree](comparisons/decision-tree.md) |
| **Use a CLI with MCP servers** | [CLI Clients](#-cli-clients) |
| **Expose my MCP server as REST/HTTP** | [REST API Bridges](#-rest-api-bridges) |
| **Bridge MCP across transports** | [Transport Bridges](#-transport-bridges) |
| **Deploy enterprise MCP infrastructure** | [Enterprise Tools](#-enterprise--cloud) |
| **Convert gRPC/protobuf to MCP** | [gRPC Bridge](#-grpc-bridge) |
| **Understand MCP authentication** | [Authentication Guide](comparisons/authentication.md) |
| **See security analysis** | [Security Analysis](comparisons/security.md) |
| **Browse all tools** | [Full Comparison](comparisons/auto-generated.md) |

## Ecosystem Overview

<!-- AUTOGEN:STATS -->
<!-- /AUTOGEN:STATS -->

## CLI Clients

Interactive command-line tools for working with MCP servers.

<!-- AUTOGEN:CLI_CLIENTS:6 -->
<!-- /AUTOGEN:CLI_CLIENTS -->

**[View all CLI clients ->](comparisons/auto-generated.md#cli-client)**

## REST API Bridges

Expose MCP servers as REST APIs with OpenAPI/Swagger compatibility.

<!-- AUTOGEN:REST_BRIDGES -->
<!-- /AUTOGEN:REST_BRIDGES -->

**Key use cases:**

* Integrate MCP servers with GPT Actions and custom GPTs
* Provide OpenAPI-compatible REST endpoints
* Enable web applications to call MCP tools

## Transport Bridges

Bridge between stdio MCP and HTTP/SSE/WebSocket transports.

<!-- AUTOGEN:TRANSPORT_BRIDGES:6 -->
<!-- /AUTOGEN:TRANSPORT_BRIDGES -->

**[Full Transport Details ->](comparisons/transports.md)**

## Enterprise & Cloud

Production-ready gateways from major organizations.

<!-- AUTOGEN:ENTERPRISE -->
<!-- /AUTOGEN:ENTERPRISE -->

**Enterprise features:**

* Kubernetes integration and orchestration
* Security guardrails and policy enforcement
* Session management and routing
* Production observability

## gRPC Bridge

Convert between gRPC/protobuf and MCP.

<!-- AUTOGEN:GRPC_BRIDGE -->
<!-- /AUTOGEN:GRPC_BRIDGE -->

## Specialized Adapters

Unique use cases and integrations.

<!-- AUTOGEN:SPECIALIZED -->
<!-- /AUTOGEN:SPECIALIZED -->

## Detailed Comparisons

* **[Decision tree guide](comparisons/decision-tree.md)** - Interactive flowchart to find the right tool
* **[Auto-generated tables](comparisons/auto-generated.md)** - Full comparison data with all projects
* **[Feature comparison](comparisons/features.md)** - Features by category, cross-cutting analysis
* **[Security analysis](comparisons/security.md)** - Code patterns, recommendations, per-project findings
* **[Transport support](comparisons/transports.md)** - Protocol matrix, implementation details
* **[Authentication guide](comparisons/authentication.md)** - OAuth 2.1, env vars, gateway auth bridging

## For Contributors

### Project Data Schema

Each project is documented in a YAML file under `projects/`:

```yaml
last-update: "2025-12-16"
repo-url: "https://github.com/owner/repo"
name: "Project Name"
stars: 1234
category: "cli-client"
transports:
  stdio: true
  http: true
```

See **[spec.yaml](spec.yaml)** for the full schema.

### Scripts

| Script | Purpose |
|--------|---------|
| `scripts/clone-all.sh` | Clone all tracked repos to `tmp/` |
| `scripts/check-yaml.py` | Validate YAML files against spec |
| `scripts/generate-tables.py` | Generate comparison tables |
| `scripts/generate-readme.py` | Generate README.md from template |
| `scripts/generate-decision-tree.py` | Generate decision tree visualizations |

### Generate Tables

```bash
# Generate all comparison tables
./scripts/generate-tables.py > comparisons/auto-generated.md

# Generate README from template
./scripts/generate-readme.py

# Generate decision tree visualizations
./scripts/generate-decision-tree.py

# Specific views
./scripts/generate-tables.py --by-category
./scripts/generate-tables.py --by-transport
./scripts/generate-tables.py --reputable-only
```

### Repository Structure

```
├── README.md                    # Generated from template
├── README.template.md           # Template with AUTOGEN markers
├── GUIDELINES.md                # Project guidelines
├── PROCESS.md                   # Research process
├── spec.yaml                    # YAML schema
├── projects/                    # Project YAML files
├── scripts/                     # Utility scripts
├── comparisons/                 # Detailed comparisons
├── r-and-d/                     # Research & development
│   └── decision-tree-generator/ # Reusable decision tree library
├── ramblings/                   # Research notes
└── tmp/                         # Cloned repos (gitignored)
```

### Contributing

See **[CONTRIBUTING.md](CONTRIBUTING.md)** for detailed instructions.

Quick start:

1. Run `./scripts/clone-all.sh` to clone all repos
2. Analyze a project and update its YAML file
3. Run `./scripts/check-yaml.py` to validate
4. Regenerate: `./scripts/generate-tables.py > comparisons/auto-generated.md && ./scripts/generate-readme.py`
5. Submit a PR

## Security Considerations

When evaluating these tools, we check for:

* **Network isolation**: Only connects to configured MCP servers?
* **Code execution**: Safe handling of `eval`, `exec`, subprocess calls?
* **Input validation**: Proper sanitization of user input?
* **Sandboxing**: Container/isolation support?

**[Full Security Analysis ->](comparisons/security.md)**

## Research Resources

* [Perplexity: MCP Server Wrappers & REST Adapters](https://www.perplexity.ai/search/wrapping-mcp-servers-into-cli-0jIuIvdPSregFphOEGCWbw) - Initial research on wrapping MCP servers into CLI tools and exposing REST servers as MCP

## License

This research repository is released under MIT License.
