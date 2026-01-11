<!-- AUTO-GENERATED from README.template.md - Run: ./scripts/generate-readme.py -->

# MCP Ecosystem Tools Comparison

A comprehensive comparison of tools in the **MCP (Model Context Protocol)** ecosystem - from CLI clients to transport bridges to enterprise gateways.

## Quick Navigation

| I want to... | Go here |
|--------------|---------|
| **Find the right tool for me** | [Decision Tree](comparisons/decision-tree-unfoldable.md) ·  [Flowchart](comparisons/decision-tree.md) |
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
| Category | Projects | Description |
|----------|----------|-------------|
| CLI Clients | 11 | Command-line interfaces for MCP |
| Transport Bridges | 5 | stdio <-> HTTP/SSE/WebSocket |
| REST API Bridges | 2 | Expose MCP as REST with OpenAPI |
| Enterprise Gateways | 2 | Production infrastructure |
| Specialized Adapters | 3 | CLI wrapping, command execution |
| OpenAPI Converters | 6 | OpenAPI to/from MCP conversion |
| Cloud Integration | 1 |  |
| Docker Integration | 1 |  |
| Kubernetes Integration | 1 |  |
| MCP Frameworks | 2 | Framework libraries |
| MCP to OpenAPI | 1 |  |
| Official Tool | 1 |  |
| Proxy Aggregator | 1 |  |
| gRPC Bridge | 1 | gRPC/protobuf to MCP |
| **Total** | **38** | All tracked projects |

**Top projects:** 9,141+ combined GitHub stars | 13 reputable/official sources
<!-- /AUTOGEN:STATS -->

## CLI Clients

Interactive command-line tools for working with MCP servers.

<!-- AUTOGEN:CLI_CLIENTS:6 -->
| Org/Project | Stars | Language | Key Features |
|-------------|------:|----------|--------------|
| [chrishayuk/mcp-cli](https://github.com/chrishayuk/mcp-cli) [y](projects/chrishayuk--mcp-cli.yaml) | 1.8k | Python | Multiple modes: chat, interactive shell, command-l... |
| [f/mcptools](https://github.com/f/mcptools) [y](projects/f--mcptools.yaml) | 1.4k | Go | Interactive shell mode (persistent connection) |
| [adhikasp/mcp-client-cli](https://github.com/adhikasp/mcp-client-cli) [y](projects/adhikasp--mcp-client-cli.yaml) | 655 | Python | LLM-agnostic (OpenAI, Groq, local LLMs) |
| [wong2/mcp-cli](https://github.com/wong2/mcp-cli) [y](projects/wong2--mcp-cli.yaml) | 396 | JavaScript | Scriptable automation (bypasses interactive prompt... |
| [apify/mcp-cli](https://github.com/apify/mcp-cli) [y](projects/apify--mcp-cli.yaml) | 167 | TypeScript | Full OAuth 2.1 with PKCE and automatic token refre... |
| [MladenSU/cli-mcp-server](https://github.com/MladenSU/cli-mcp-server) [y](projects/MladenSU--cli-mcp-server.yaml) | 155 | Python | Command whitelisting |
<!-- /AUTOGEN:CLI_CLIENTS -->

**[View all CLI clients ->](comparisons/auto-generated.md#cli-client)**

## REST API Bridges

Expose MCP servers as REST APIs with OpenAPI/Swagger compatibility.

<!-- AUTOGEN:REST_BRIDGES -->
| Org/Project | Stars | Language | Best For |
|-------------|------:|----------|----------|
| [SecretiveShell/MCP-Bridge](https://github.com/SecretiveShell/MCP-Bridge) [y](projects/SecretiveShell--MCP-Bridge.yaml) | 882 | Python | Middleware providing OpenAI-compatible e... |
| [acehoss/mcp-gateway](https://github.com/acehoss/mcp-gateway) [y](projects/acehoss--mcp-gateway.yaml) | 128 | TypeScript | REST API exposure with OpenAPI/Swagger c... |
<!-- /AUTOGEN:REST_BRIDGES -->

**Key use cases:**

* Integrate MCP servers with GPT Actions and custom GPTs
* Provide OpenAPI-compatible REST endpoints
* Enable web applications to call MCP tools

## Transport Bridges

Bridge between stdio MCP and HTTP/SSE/WebSocket transports.

<!-- AUTOGEN:TRANSPORT_BRIDGES:6 -->
| Org/Project | Stars | Type | Transports |
|-------------|------:|------|------------|
| [sparfenyuk/mcp-proxy](https://github.com/sparfenyuk/mcp-proxy) [y](projects/sparfenyuk--mcp-proxy.yaml) | 2.1k | Python | stdio, sse, http |
| [EvalsOne/MCP-connect](https://github.com/EvalsOne/MCP-connect) [y](projects/EvalsOne--MCP-connect.yaml) | 227 | TypeScript | stdio, http |
| [ConechoAI/nchan-mcp-transport](https://github.com/ConechoAI/nchan-mcp-transport) [y](projects/ConechoAI--nchan-mcp-transport.yaml) | 28 | TypeScript | websocket, sse, http |
| [nccgroup/http-mcp-bridge](https://github.com/nccgroup/http-mcp-bridge) [y](projects/nccgroup--http-mcp-bridge.yaml) | - | Python | stdio, sse, http |
| [supercorp-ai/supergateway](https://github.com/supercorp-ai/supergateway) [y](projects/supercorp-ai--supergateway.yaml) | - | TypeScript | stdio, sse, websocket |
<!-- /AUTOGEN:TRANSPORT_BRIDGES -->

**[Full Transport Details ->](comparisons/transports.md)**

## Enterprise & Cloud

Production-ready gateways from major organizations.

<!-- AUTOGEN:ENTERPRISE -->
| Org/Project | Organization | Features |
|-------------|--------------|----------|
| [microsoft/mcp-gateway](https://github.com/microsoft/mcp-gateway) [y](projects/microsoft--mcp-gateway.yaml) | Microsoft | Kubernetes-native design (StatefulSets, headless s... |
| [lasso-security/mcp-gateway](https://github.com/lasso-security/mcp-gateway) [y](projects/lasso-security--mcp-gateway.yaml) | Lasso Security | PII masking |
| [docker/mcp-gateway](https://github.com/docker/mcp-gateway) [y](projects/docker--mcp-gateway.yaml) | Docker | Container-based isolation |
| microsoft/azure-api-management-mcp [y](projects/microsoft--azure-api-management-mcp.yaml) | Microsoft | Native Azure integration |
<!-- /AUTOGEN:ENTERPRISE -->

**Enterprise features:**

* Kubernetes integration and orchestration
* Security guardrails and policy enforcement
* Session management and routing
* Production observability

## gRPC Bridge

Convert between gRPC/protobuf and MCP.

<!-- AUTOGEN:GRPC_BRIDGE -->
| Org/Project | Organization | Description |
|-------------|--------------|-------------|
| [redpanda-data/protoc-gen-go-mcp](https://github.com/redpanda-data/protoc-gen-go-mcp) [y](projects/redpanda-data--protoc-gen-go-mcp.yaml) | Redpanda | protoc plugin generating MCP servers from gRPC/Con... |
<!-- /AUTOGEN:GRPC_BRIDGE -->

## Specialized Adapters

Unique use cases and integrations.

<!-- AUTOGEN:SPECIALIZED -->
| Org/Project | Type | Description |
|-------------|------|-------------|
| [eirikb/any-cli-mcp-server](https://github.com/eirikb/any-cli-mcp-server) [y](projects/eirikb--any-cli-mcp-server.yaml) | Specialized Adapter | MCP server that maps tools from existing CLI help ... |
| [g0t4/mcp-server-commands](https://github.com/g0t4/mcp-server-commands) [y](projects/g0t4--mcp-server-commands.yaml) | Specialized Adapter | MCP server to run arbitrary shell commands and scr... |
| [simon-ami/win-cli-mcp-server](https://github.com/simon-ami/win-cli-mcp-server) [y](projects/simon-ami--win-cli-mcp-server.yaml) | Specialized Adapter | Secure command-line MCP server for Windows (PowerS... |
| [containers/kubernetes-mcp-server](https://github.com/containers/kubernetes-mcp-server) [y](projects/containers--kubernetes-mcp-server.yaml) | Kubernetes Integration | Native Go K8s/OpenShift MCP server implementation ... |
<!-- /AUTOGEN:SPECIALIZED -->

## Detailed Comparisons

* **[Decision tree (unfoldable)](comparisons/decision-tree-unfoldable.md)** - Click-to-expand guide
* **[Decision tree (flowchart)](comparisons/decision-tree.md)** - Mermaid diagram view
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
