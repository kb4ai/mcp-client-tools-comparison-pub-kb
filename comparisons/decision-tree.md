# Choose an MCP Ecosystem Tool

Interactive guide to selecting the right tool from 37 MCP ecosystem projects

## Quick Navigation

Click a category below to jump to its decision tree:

* [CLI - Interactive command-line usage](#section-0)
* [REST API - Expose MCP as HTTP endpoints](#section-1)
* [Transport Bridge - stdio ↔ HTTP/SSE/WebSocket](#section-2)
* [Enterprise - Production infrastructure](#section-3)
* [OpenAPI ↔ MCP Conversion](#section-4)
* [gRPC/Protobuf - Convert gRPC to MCP](#section-5)
* [Specialized - CLI wrapping, Windows, Kubernetes](#section-6)
* [Framework - Build MCP servers from scratch](#section-7)
* [Testing/Debugging - Inspect and test MCP servers](#section-8)

## Overview

```mermaid
%% Overview: Choose an MCP Ecosystem Tool

flowchart TD
    mcp_tool_chooser_root["What's your primary use case?"]
    mcp_tool_chooser_root -->|"CLI - Interactive command-l..."| mcp_tool_chooser_0
    mcp_tool_chooser_0("CLI - Interactive command-l...")
    click mcp_tool_chooser_0 "#section-0"
    mcp_tool_chooser_root -->|"REST API - Expose MCP as HT..."| mcp_tool_chooser_1
    mcp_tool_chooser_1("REST API - Expose MCP as HT...")
    click mcp_tool_chooser_1 "#section-1"
    mcp_tool_chooser_root -->|"Transport Bridge - stdio ↔ ..."| mcp_tool_chooser_2
    mcp_tool_chooser_2("Transport Bridge - stdio ↔ ...")
    click mcp_tool_chooser_2 "#section-2"
    mcp_tool_chooser_root -->|"Enterprise - Production inf..."| mcp_tool_chooser_3
    mcp_tool_chooser_3("Enterprise - Production inf...")
    click mcp_tool_chooser_3 "#section-3"
    mcp_tool_chooser_root -->|"OpenAPI ↔ MCP Conversion"| mcp_tool_chooser_4
    mcp_tool_chooser_4("OpenAPI ↔ MCP Conversion")
    click mcp_tool_chooser_4 "#section-4"
    mcp_tool_chooser_root -->|"gRPC/Protobuf - Convert gRP..."| mcp_tool_chooser_5
    mcp_tool_chooser_5("gRPC/Protobuf - Convert gRP...")
    click mcp_tool_chooser_5 "#section-5"
    mcp_tool_chooser_root -->|"Specialized - CLI wrapping,..."| mcp_tool_chooser_6
    mcp_tool_chooser_6("Specialized - CLI wrapping,...")
    click mcp_tool_chooser_6 "#section-6"
    mcp_tool_chooser_root -->|"Framework - Build MCP serve..."| mcp_tool_chooser_7
    mcp_tool_chooser_7("Framework - Build MCP serve...")
    click mcp_tool_chooser_7 "#section-7"
    mcp_tool_chooser_root -->|"Testing/Debugging - Inspect..."| mcp_tool_chooser_8
    mcp_tool_chooser_8("Testing/Debugging - Inspect...")
    click mcp_tool_chooser_8 "#section-8"
```

## CLI - Interactive command-line usage {#section-0}

```mermaid
%% Subtree: CLI - Interactive command-line usage

flowchart TD
    mcp_tool_chooser_0["What's your main goal?"]
    mcp_tool_chooser_0 -->|"Chat with AI using MCP..."| mcp_tool_chooser_0_0
    mcp_tool_chooser_0_0["Which LLM provider?"]
    mcp_tool_chooser_0_0 -->|"OpenAI-compatible (Ope..."| mcp_tool_chooser_0_0_0
    mcp_tool_chooser_0_0_0("Use adhikasp/mcp-client-cli")
    mcp_tool_chooser_0_0 -->|"Multiple providers / f..."| mcp_tool_chooser_0_0_1
    mcp_tool_chooser_0_0_1("Use chrishayuk/mcp-cli")
    mcp_tool_chooser_0_0 -->|"Multi-provider with se..."| mcp_tool_chooser_0_0_2
    mcp_tool_chooser_0_0_2("Use mcp-use/mcp-use-cli")
    mcp_tool_chooser_0 -->|"Call MCP tools directl..."| mcp_tool_chooser_0_1
    mcp_tool_chooser_0_1["What feature matters most?"]
    mcp_tool_chooser_0_1 -->|"Scripting and automation"| mcp_tool_chooser_0_1_0
    mcp_tool_chooser_0_1_0("Use wong2/mcp-cli")
    mcp_tool_chooser_0_1 -->|"Interactive exploration"| mcp_tool_chooser_0_1_1
    mcp_tool_chooser_0_1_1("Use f/mcptools")
    mcp_tool_chooser_0_1 -->|"Server inspection (lis..."| mcp_tool_chooser_0_1_2
    mcp_tool_chooser_0_1_2("Use winterfx/mcpcli or Deniscartin/mcp-cli")
    mcp_tool_chooser_0 -->|"HTTP transport with OA..."| mcp_tool_chooser_0_2
    mcp_tool_chooser_0_2("Use apify/mcp-cli (mcpc)")
    mcp_tool_chooser_0 -->|"TypeScript type genera..."| mcp_tool_chooser_0_3
    mcp_tool_chooser_0_3("Use steipete/mcporter")
    mcp_tool_chooser_0 -->|"R language ecosystem"| mcp_tool_chooser_0_4
    mcp_tool_chooser_0_4("Use posit-dev/mcptools")
    mcp_tool_chooser_0 -->|"Expose CLI commands TO..."| mcp_tool_chooser_0_5
    mcp_tool_chooser_0_5("Use MladenSU/cli-mcp-server")
```

## REST API - Expose MCP as HTTP endpoints {#section-1}

```mermaid
%% Subtree: REST API - Expose MCP as HTTP endpoints

flowchart TD
    mcp_tool_chooser_1["What API format do you need?"]
    mcp_tool_chooser_1 -->|"Full OpenAPI/Swagger s..."| mcp_tool_chooser_1_0
    mcp_tool_chooser_1_0("Use acehoss/mcp-gateway")
    mcp_tool_chooser_1 -->|"OpenAI-compatible API ..."| mcp_tool_chooser_1_1
    mcp_tool_chooser_1_1("Use SecretiveShell/MCP-Bridge")
```

## Transport Bridge - stdio ↔ HTTP/SSE/WebSocket {#section-2}

```mermaid
%% Subtree: Transport Bridge - stdio ↔ HTTP/SSE/WebSocket

flowchart TD
    mcp_tool_chooser_2["Which transport protocol?"]
    mcp_tool_chooser_2 -->|"SSE (Server-Sent Events)"| mcp_tool_chooser_2_0
    mcp_tool_chooser_2_0("Use sparfenyuk/mcp-proxy")
    mcp_tool_chooser_2 -->|"WebSocket"| mcp_tool_chooser_2_1
    mcp_tool_chooser_2_1["Need production-scale infrastructure?"]
    mcp_tool_chooser_2_1 -->|"Yes - Nginx/Nchan scal..."| mcp_tool_chooser_2_1_0
    mcp_tool_chooser_2_1_0("Use ConechoAI/nchan-mcp-transport")
    mcp_tool_chooser_2_1 -->|"No - Simple WebSocket ..."| mcp_tool_chooser_2_1_1
    mcp_tool_chooser_2_1_1("Use supercorp-ai/supergateway")
    mcp_tool_chooser_2 -->|"HTTP (stateless)"| mcp_tool_chooser_2_2
    mcp_tool_chooser_2_2("Use EvalsOne/MCP-connect or nccgroup/http-mcp-b...")
```

## Enterprise - Production infrastructure {#section-3}

```mermaid
%% Subtree: Enterprise - Production infrastructure

flowchart TD
    mcp_tool_chooser_3["What's your deployment environment?"]
    mcp_tool_chooser_3 -->|"Kubernetes"| mcp_tool_chooser_3_0
    mcp_tool_chooser_3_0("Use microsoft/mcp-gateway")
    mcp_tool_chooser_3 -->|"Docker/Containers"| mcp_tool_chooser_3_1
    mcp_tool_chooser_3_1("Use docker/mcp-gateway")
    mcp_tool_chooser_3 -->|"Azure cloud"| mcp_tool_chooser_3_2
    mcp_tool_chooser_3_2("Use microsoft/azure-api-management-mcp")
    mcp_tool_chooser_3 -->|"Security-focused (PII ..."| mcp_tool_chooser_3_3
    mcp_tool_chooser_3_3("Use lasso-security/mcp-gateway")
    mcp_tool_chooser_3 -->|"Multi-server aggregation"| mcp_tool_chooser_3_4
    mcp_tool_chooser_3_4("Use TBXark/mcp-proxy")
```

## OpenAPI ↔ MCP Conversion {#section-4}

```mermaid
%% Subtree: OpenAPI ↔ MCP Conversion

flowchart TD
    mcp_tool_chooser_4["Which direction?"]
    mcp_tool_chooser_4 -->|"OpenAPI → MCP (expose ..."| mcp_tool_chooser_4_0
    mcp_tool_chooser_4_0["What's your priority?"]
    mcp_tool_chooser_4_0 -->|"Quick TypeScript solution"| mcp_tool_chooser_4_0_0
    mcp_tool_chooser_4_0_0("Use ouvreboite/openapi-to-mcp")
    mcp_tool_chooser_4_0 -->|"Swagger 2.0 support (l..."| mcp_tool_chooser_4_0_1
    mcp_tool_chooser_4_0_1("Use Vizioz/Swagger-MCP")
    mcp_tool_chooser_4_0 -->|"Enterprise / CI/CD int..."| mcp_tool_chooser_4_0_2
    mcp_tool_chooser_4_0_2("Use cnoe-io/openapi-mcp-codegen")
    mcp_tool_chooser_4_0 -->|"Go-based / Cloud gatew..."| mcp_tool_chooser_4_0_3
    mcp_tool_chooser_4_0_3("Use higress-group/openapi-to-mcpserver")
    mcp_tool_chooser_4_0 -->|"Runtime server (no cod..."| mcp_tool_chooser_4_0_4
    mcp_tool_chooser_4_0_4("Use ivo-toby/mcp-openapi-server or janwilmake/o...")
    mcp_tool_chooser_4 -->|"MCP → OpenAPI (generat..."| mcp_tool_chooser_4_1
    mcp_tool_chooser_4_1("Use open-webui/mcpo")
```

## gRPC/Protobuf - Convert gRPC to MCP {#section-5}

```mermaid
%% Subtree: gRPC/Protobuf - Convert gRPC to MCP

flowchart TD
    mcp_tool_chooser_5("Use redpanda-data/protoc-gen-go-mcp")
```

## Specialized - CLI wrapping, Windows, Kubernetes {#section-6}

```mermaid
%% Subtree: Specialized - CLI wrapping, Windows, Kubernetes

flowchart TD
    mcp_tool_chooser_6["What specialization?"]
    mcp_tool_chooser_6 -->|"Wrap existing CLI tool..."| mcp_tool_chooser_6_0
    mcp_tool_chooser_6_0("Use eirikb/any-cli-mcp-server")
    mcp_tool_chooser_6 -->|"Windows PowerShell/CMD"| mcp_tool_chooser_6_1
    mcp_tool_chooser_6_1("Use simon-ami/win-cli-mcp-server")
    mcp_tool_chooser_6 -->|"Kubernetes/OpenShift m..."| mcp_tool_chooser_6_2
    mcp_tool_chooser_6_2("Use containers/kubernetes-mcp-server")
    mcp_tool_chooser_6 -->|"Run arbitrary shell co..."| mcp_tool_chooser_6_3
    mcp_tool_chooser_6_3("Use g0t4/mcp-server-commands")
```

## Framework - Build MCP servers from scratch {#section-7}

```mermaid
%% Subtree: Framework - Build MCP servers from scratch

flowchart TD
    mcp_tool_chooser_7["Which programming language?"]
    mcp_tool_chooser_7 -->|"Python"| mcp_tool_chooser_7_0
    mcp_tool_chooser_7_0("Use jlowin/fastmcp")
    mcp_tool_chooser_7 -->|"Java / Spring"| mcp_tool_chooser_7_1
    mcp_tool_chooser_7_1("Use spring-ai-community/mcp-annotations")
```

## Testing/Debugging - Inspect and test MCP servers {#section-8}

```mermaid
%% Subtree: Testing/Debugging - Inspect and test MCP servers

flowchart TD
    mcp_tool_chooser_8("Use modelcontextprotocol/inspector")
```

---

**Other views:** [Unfoldable Tree](decision-tree-unfoldable.md) | [Full Tables](auto-generated.md)

*Auto-generated from `r-and-d/decision-tree-generator/examples/mcp-tool-chooser.yaml`*

*Generated: 2026-01-11T17:07:02+01:00 | Source commit: 1fb70a9*