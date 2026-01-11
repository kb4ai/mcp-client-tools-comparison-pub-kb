# Decision Tree Coverage Analysis

Date: 2026-01-11

## Executive Summary

The current decision tree covers only **51.4% (19/37)** of the projects in the repository. This analysis identifies why 18 projects are missing and proposes specific solutions to achieve comprehensive coverage.

## Missing Projects Summary

| Project | Category | Why Missing from Tree |
|---------|----------|----------------------|
| Deniscartin/mcp-cli | cli-client | Not added to CLI branch alternatives |
| MladenSU/cli-mcp-server | cli-client | Unique "secure CLI server" not categorized |
| TBXark/mcp-proxy | proxy-aggregator | No "proxy-aggregator" branch exists |
| Vizioz/Swagger-MCP | openapi-to-mcp | Tree only has leaf reference, no actual projects |
| apify/mcp-cli | cli-client | Not added to CLI branch - has HTTP auth! |
| cnoe-io/openapi-mcp-codegen | openapi-to-mcp | Tree only has leaf reference, no actual projects |
| higress-group/openapi-to-mcpserver | openapi-to-mcp | Tree only has leaf reference, no actual projects |
| ivo-toby/mcp-openapi-server | openapi-to-mcp | Tree only has leaf reference, no actual projects |
| janwilmake/openapi-mcp-server | openapi-to-mcp | Tree only has leaf reference, no actual projects |
| jlowin/fastmcp | mcp-framework | No "framework" branch exists |
| mcp-use/mcp-use-cli | cli-client | Not added to CLI branch (archived) |
| modelcontextprotocol/inspector | official-tool | No "testing/debugging" branch exists |
| open-webui/mcpo | mcp-to-openapi | Tree only has leaf reference, no actual projects |
| ouvreboite/openapi-to-mcp | openapi-to-mcp | Tree only has leaf reference, no actual projects |
| posit-dev/mcptools | cli-client | R language not represented |
| spring-ai-community/mcp-annotations | mcp-framework | No "framework" branch exists |
| steipete/mcporter | cli-client | Not added to CLI branch |
| winterfx/mcpcli | cli-client | Not added to CLI branch |

## Gap Analysis

### 1. OpenAPI/MCP Conversion Categories (7 projects)

**Problem:** The tree has a branch for "OpenAPI ↔ MCP Conversion" but it only contains generic leaf nodes pointing to comparison documents instead of actual project recommendations.

**Missing projects:**

* **openapi-to-mcp (6 projects):**
  - Vizioz/Swagger-MCP (TypeScript, Swagger 2.0 focus)
  - cnoe-io/openapi-mcp-codegen (Python, enterprise/Cisco)
  - higress-group/openapi-to-mcpserver (Go, Alibaba ecosystem)
  - ivo-toby/mcp-openapi-server (TypeScript, runtime)
  - janwilmake/openapi-mcp-server (TypeScript)
  - ouvreboite/openapi-to-mcp (TypeScript, fastest path)

* **mcp-to-openapi (1 project):**
  - open-webui/mcpo (Python, Swagger UI included)

**Recommendation:** Replace the generic leaf nodes with actual decision sub-trees that help users choose between the 6+ OpenAPI-to-MCP tools based on:

* Language preference (Python vs TypeScript vs Go)
* Enterprise requirements (Cisco-backed vs community)
* Swagger 2.0 vs OpenAPI 3.0 support
* Runtime vs code generation approach

### 2. CLI Clients (7 projects not fully represented)

**Problem:** The CLI branch covers only 4 projects (adhikasp, chrishayuk, wong2, f/mcptools) but there are 11 CLI clients total.

**Missing CLI projects:**

* Deniscartin/mcp-cli - Config management focus
* MladenSU/cli-mcp-server - Secure CLI with whitelisting (actually a SERVER that exposes CLI)
* apify/mcp-cli - **Best-in-class HTTP auth support!**
* mcp-use/mcp-use-cli - Multi-provider LLM (archived)
* posit-dev/mcptools - R language
* steipete/mcporter - TypeScript code generation
* winterfx/mcpcli - Inspection focus

**Recommendation:** Expand CLI branch with additional decision points:

* "Need HTTP transport with OAuth?" -> apify/mcp-cli
* "Need secure CLI exposure to LLMs?" -> MladenSU/cli-mcp-server
* "Working in R?" -> posit-dev/mcptools
* "Need TypeScript type generation?" -> steipete/mcporter

### 3. MCP Frameworks (2 projects)

**Problem:** No "framework" category exists in the tree.

**Missing projects:**

* jlowin/fastmcp - Python framework (FastAPI-style)
* spring-ai-community/mcp-annotations - Java/Spring annotations

**Recommendation:** Add a new top-level branch "Framework - Build MCP Servers" with sub-decisions:

* "Python?" -> jlowin/fastmcp
* "Java/Spring?" -> spring-ai-community/mcp-annotations

### 4. Official/Testing Tools (1 project)

**Problem:** No branch for testing/debugging tools.

**Missing project:**

* modelcontextprotocol/inspector - Official visual testing tool

**Recommendation:** Add a new top-level branch "Testing/Debugging MCP Servers" that leads to the inspector.

### 5. Proxy/Aggregator (1 project)

**Problem:** TBXark/mcp-proxy is a "proxy-aggregator" that aggregates multiple MCP servers, but there's no branch for this use case.

**Missing project:**

* TBXark/mcp-proxy - Multi-server aggregation

**Recommendation:** Add to "Enterprise" branch or create new "Aggregation - Combine multiple MCP servers" branch.

## Proposed YAML Additions

### 1. Add Official Testing Branch

```yaml
      - condition: "Testing/Debugging - Test and inspect MCP servers"
        next:
          leaf-structured:
            recommendation: "Use modelcontextprotocol/inspector"
            projects:
              - modelcontextprotocol/inspector
            notes: "Official Anthropic testing tool with visual UI and CLI mode"
```

### 2. Add Framework Branch

```yaml
      - condition: "Framework - Build MCP servers from scratch"
        next:
          question: "Which language?"
          branches:
            - condition: "Python"
              next:
                leaf-structured:
                  recommendation: "Use jlowin/fastmcp"
                  projects:
                    - jlowin/fastmcp
                  notes: "FastAPI-inspired Python framework with decorator-based server definition"
            - condition: "Java/Spring"
              next:
                leaf-structured:
                  recommendation: "Use spring-ai-community/mcp-annotations"
                  projects:
                    - spring-ai-community/mcp-annotations
                  notes: "Spring AI annotations for enterprise Java MCP development"
```

### 3. Replace OpenAPI Conversion Leaves with Full Sub-trees

```yaml
      - condition: "OpenAPI ↔ MCP Conversion"
        next:
          question: "Which direction?"
          branches:
            - condition: "OpenAPI → MCP (expose REST APIs as MCP)"
              next:
                question: "What's your priority?"
                branches:
                  - condition: "Quick conversion / TypeScript"
                    next:
                      leaf-structured:
                        recommendation: "Use ouvreboite/openapi-to-mcp"
                        projects:
                          - ouvreboite/openapi-to-mcp
                        notes: "Fastest path for OpenAPI to MCP, npm package"
                  - condition: "Swagger 2.0 support"
                    next:
                      leaf-structured:
                        recommendation: "Use Vizioz/Swagger-MCP"
                        projects:
                          - Vizioz/Swagger-MCP
                        notes: "Supports both Swagger 2.0 and OpenAPI 3.0"
                  - condition: "Enterprise / CI/CD integration"
                    next:
                      leaf-structured:
                        recommendation: "Use cnoe-io/openapi-mcp-codegen"
                        projects:
                          - cnoe-io/openapi-mcp-codegen
                        notes: "Cisco-backed, Python-based, enterprise CI/CD focus"
                  - condition: "Go-based / Cloud gateway"
                    next:
                      leaf-structured:
                        recommendation: "Use higress-group/openapi-to-mcpserver"
                        projects:
                          - higress-group/openapi-to-mcpserver
                        notes: "Go implementation, Alibaba Cloud Gateway ecosystem"
                  - condition: "Runtime server / multiple options"
                    next:
                      leaf-structured:
                        recommendation: "Choose based on preference"
                        projects:
                          - ivo-toby/mcp-openapi-server
                          - janwilmake/openapi-mcp-server
                        notes: "TypeScript runtime implementations for OpenAPI serving"
            - condition: "MCP → OpenAPI (generate REST API from MCP)"
              next:
                leaf-structured:
                  recommendation: "Use open-webui/mcpo"
                  projects:
                    - open-webui/mcpo
                  notes: "MCP-to-OpenAPI proxy with Swagger UI, from Open WebUI team"
```

### 4. Expand CLI Branch

```yaml
      - condition: "CLI - Interactive command-line usage"
        next:
          question: "What's your main need?"
          branches:
            - condition: "Chat with LLM"
              next:
                question: "Which LLM provider?"
                branches:
                  - condition: "OpenAI-compatible (OpenAI, Groq, local)"
                    next:
                      leaf-structured:
                        recommendation: "Use adhikasp/mcp-client-cli"
                        projects:
                          - adhikasp/mcp-client-cli
                        notes: "LLM-agnostic, supports OpenAI, Groq, and local LLMs"
                  - condition: "Multiple providers / flexible"
                    next:
                      leaf-structured:
                        recommendation: "Use chrishayuk/mcp-cli"
                        projects:
                          - chrishayuk/mcp-cli
                        notes: "1.8k stars, multiple modes: chat, interactive shell, command-line"
            - condition: "Call MCP tools directly (no LLM)"
              next:
                question: "Need specific features?"
                branches:
                  - condition: "Scripting and automation"
                    next:
                      leaf-structured:
                        recommendation: "Use wong2/mcp-cli"
                        projects:
                          - wong2/mcp-cli
                        notes: "Scriptable automation, bypasses interactive prompts"
                  - condition: "Interactive shell"
                    next:
                      leaf-structured:
                        recommendation: "Use f/mcptools"
                        projects:
                          - f/mcptools
                        notes: "1.4k stars, Go-based, interactive shell with persistent connection"
                  - condition: "Server inspection"
                    next:
                      leaf-structured:
                        recommendation: "Use winterfx/mcpcli or Deniscartin/mcp-cli"
                        projects:
                          - winterfx/mcpcli
                          - Deniscartin/mcp-cli
                        notes: "Inspection-focused CLIs for listing tools, prompts, resources"
                  - condition: "TypeScript code generation"
                    next:
                      leaf-structured:
                        recommendation: "Use steipete/mcporter"
                        projects:
                          - steipete/mcporter
                        notes: "emit-ts for TypeScript type/client generation from MCP servers"
            - condition: "HTTP transport with OAuth support"
              next:
                leaf-structured:
                  recommendation: "Use apify/mcp-cli (mcpc)"
                  projects:
                    - apify/mcp-cli
                  notes: "BEST-IN-CLASS: Full OAuth 2.1, --header flag, OS keychain storage"
            - condition: "R language ecosystem"
              next:
                leaf-structured:
                  recommendation: "Use posit-dev/mcptools"
                  projects:
                    - posit-dev/mcptools
                  notes: "Official Posit project, R as both MCP server and client"
            - condition: "Expose CLI tools TO LLMs (MCP server)"
              next:
                leaf-structured:
                  recommendation: "Use MladenSU/cli-mcp-server"
                  projects:
                    - MladenSU/cli-mcp-server
                  notes: "Secure CLI execution with command whitelisting and path validation"
```

### 5. Add Aggregator Branch (extend Enterprise or create new)

```yaml
            - condition: "Multi-server aggregation"
              next:
                leaf-structured:
                  recommendation: "Use TBXark/mcp-proxy"
                  projects:
                    - TBXark/mcp-proxy
                  notes: "592 stars, aggregates multiple MCP servers behind single HTTP endpoint"
```

## Implementation Priority

1. **High Priority - Missing Categories:**
   - Add "Testing/Debugging" branch (modelcontextprotocol/inspector)
   - Add "Framework" branch (fastmcp, mcp-annotations)
   - Add "Aggregator" option (TBXark/mcp-proxy)

2. **High Priority - Incomplete Trees:**
   - Replace OpenAPI conversion leaves with full sub-trees (7 projects)
   - Expand CLI branch (5 projects: apify, posit-dev, steipete, winterfx, Deniscartin)

3. **Medium Priority - Edge Cases:**
   - MladenSU/cli-mcp-server (unique "CLI exposure to LLM" use case)
   - mcp-use/mcp-use-cli (archived but still functional)

## Notes on Project Classification

### MladenSU/cli-mcp-server Confusion

This project is categorized as "cli-client" but it's actually an MCP SERVER that allows LLMs to execute CLI commands. It's more of a "cli-exposure" or "shell-access" pattern. The decision tree currently has this under "Specialized - Wrap existing CLI tools" which covers eirikb/any-cli-mcp-server but not this one.

**Recommendation:** Add it to the "Specialized" branch under a new condition "Secure CLI access for LLMs".

### Archived Project (mcp-use/mcp-use-cli)

This project is archived but the npm package is still available. Consider whether to include archived projects or add a note about their status.

## Coverage After Implementation

If all recommendations are implemented:

* **Current coverage:** 19/37 (51.4%)
* **After implementation:** 37/37 (100%)

The decision tree would become a comprehensive guide covering:

* 11 CLI clients
* 6 OpenAPI-to-MCP converters
* 1 MCP-to-OpenAPI converter
* 4 HTTP bridges
* 2 MCP frameworks
* 2 enterprise gateways
* 3 specialized adapters
* 1 proxy aggregator
* 1 official testing tool
* 1 gRPC bridge
* 1 WebSocket bridge
* 1 Kubernetes integration
* 1 Docker integration
* 1 cloud integration
