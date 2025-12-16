# MCP Wrapper Tools Comparison

A comprehensive comparison of tools that wrap **MCP (Model Context Protocol) servers** and expose them as CLI tools, REST APIs, WebSocket servers, gRPC services, or other interfaces.

## What is MCP?

MCP (Model Context Protocol) is a protocol for connecting AI models to external tools and data sources. This repository catalogs and compares tools that:

* **CLI clients**: Run MCP servers and interact with them from the command line
* **HTTP/SSE bridges**: Expose stdio MCP servers via HTTP or Server-Sent Events
* **WebSocket bridges**: Enable WebSocket access to MCP servers
* **gRPC bridges**: Convert protobuf/gRPC services to MCP or vice versa
* **Enterprise gateways**: Production-ready proxies with security, aggregation, and orchestration

## Quick Stats

| Metric | Count |
|--------|------:|
| Total projects tracked | 27 |
| Reputable/official sources | 8 |
| Combined GitHub stars | ~9,000+ |

## Top Projects by Stars

| Project | Stars | Language | Category |
|---------|------:|----------|----------|
| [sparfenyuk/mcp-proxy](https://github.com/sparfenyuk/mcp-proxy) | ~2.1k | Python | HTTP bridge |
| [chrishayuk/mcp-cli](https://github.com/chrishayuk/mcp-cli) | ~1.8k | Python | CLI client |
| [f/mcptools](https://github.com/f/mcptools) | ~1.4k | Go | CLI client |
| [SecretiveShell/MCP-Bridge](https://github.com/SecretiveShell/MCP-Bridge) | ~880 | Python | REST bridge |
| [adhikasp/mcp-client-cli](https://github.com/adhikasp/mcp-client-cli) | ~655 | Python | CLI client |
| [TBXark/mcp-proxy](https://github.com/TBXark/mcp-proxy) | ~590 | Go | Proxy/aggregator |

## Official/Reputable Sources

Projects from established organizations:

| Project | Organization | Category |
|---------|--------------|----------|
| [MCP Inspector](https://github.com/modelcontextprotocol/inspector) | Anthropic/MCP | Official tool |
| [mcp-gateway](https://github.com/microsoft/mcp-gateway) | Microsoft | Enterprise gateway |
| [mcp-gateway](https://github.com/docker/mcp-gateway) | Docker | Container integration |
| [protoc-gen-go-mcp](https://github.com/redpanda-data/protoc-gen-go-mcp) | Redpanda | gRPC bridge |
| [http-mcp-bridge](https://github.com/nccgroup/http-mcp-bridge) | NCC Group | Security testing |
| [mcp-gateway](https://github.com/lasso-security/mcp-gateway) | Lasso Security | Security gateway |
| [mcptools](https://github.com/posit-dev/mcptools) | Posit (RStudio) | R client |
| [kubernetes-mcp-server](https://github.com/containers/kubernetes-mcp-server) | containers org | K8s integration |

## Transport Support

| Transport | Projects |
|-----------|----------|
| stdio | 27 (all) |
| HTTP | 14 |
| SSE | 8 |
| WebSocket | 2 |
| gRPC | 1 |

## Detailed Comparisons

* [comparisons/features.md](comparisons/features.md) - Feature comparison
* [comparisons/security.md](comparisons/security.md) - Security analysis
* [comparisons/transports.md](comparisons/transports.md) - Transport support details

## Project Data

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

See [spec.yaml](spec.yaml) for the full schema.

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/clone-all.sh` | Clone all tracked repos to `tmp/` |
| `scripts/check-yaml.py` | Validate YAML files against spec |
| `scripts/generate-tables.py` | Generate comparison tables |

### Generate Tables

```bash
# Generate all comparison tables
./scripts/generate-tables.py

# Specific views
./scripts/generate-tables.py --by-category
./scripts/generate-tables.py --by-transport
./scripts/generate-tables.py --reputable-only
```

## Repository Structure

```
├── README.md                    # This file
├── GUIDELINES.md                # Project guidelines
├── PROCESS.md                   # Research process
├── spec.yaml                    # YAML schema
├── projects/                    # Project YAML files
├── scripts/                     # Utility scripts
├── comparisons/                 # Detailed comparisons
├── ramblings/                   # Research notes
└── tmp/                         # Cloned repos (gitignored)
```

## Contributing

1. Run `./scripts/clone-all.sh` to clone all repos
2. Analyze a project and update its YAML file
3. Run `./scripts/check-yaml.py` to validate
4. Submit a PR

## Security Considerations

When evaluating these tools, we check for:

* **Network isolation**: Only connects to configured MCP servers?
* **Code execution**: Safe handling of `eval`, `exec`, subprocess calls?
* **Input validation**: Proper sanitization of user input?
* **Sandboxing**: Container/isolation support?

See [comparisons/security.md](comparisons/security.md) for detailed analysis.

## License

This research repository is released under MIT License.
