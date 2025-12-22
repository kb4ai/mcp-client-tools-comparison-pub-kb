# MCP Ecosystem Restructure Plan

**Date:** 2025-12-22
**Context:** Expanding scope from "MCP client tools" to full "MCP ecosystem tools" including OpenAPI↔MCP bidirectional tooling.

## Problem Statement

The current repository focuses on:
- CLI clients for MCP
- Transport bridges (stdio↔HTTP, SSE, WebSocket)
- Enterprise gateways

New research reveals a broader ecosystem:
- **OpenAPI → MCP**: Tools that convert REST APIs (with OpenAPI specs) into MCP servers
- **MCP → OpenAPI**: Tools that expose MCP servers as REST APIs
- **MCP Frameworks**: Libraries for building MCP servers (FastMCP, Spring AI)
- **Bidirectional bridges**: Tools that work both ways

## Reader Personas

### Persona 1: "REST API Owner"
**Goal:** "I have an existing REST API with OpenAPI spec, want AI agents to call it"
**Needs:** OpenAPI → MCP conversion
**Looking for:** openapi-to-mcp, FastMCP, openapi-mcp-codegen, Spring AI annotations

### Persona 2: "MCP Server Developer"
**Goal:** "I have/built an MCP server, want to expose it as REST for non-MCP clients"
**Needs:** MCP → REST/OpenAPI proxy
**Looking for:** MCPO, Azure APIM MCP, custom wrappers

### Persona 3: "AI Agent Developer"
**Goal:** "I want a CLI/tool to interact with MCP servers during development"
**Needs:** CLI client, debugging tools
**Looking for:** mcp-cli, mcptools, mcp-client-cli, MCP Inspector

### Persona 4: "Platform Engineer"
**Goal:** "I need to bridge MCP across different transports in our infrastructure"
**Needs:** Transport bridges, proxies
**Looking for:** mcp-proxy, MCP-Bridge, supergateway

### Persona 5: "Enterprise Architect"
**Goal:** "I need production-grade MCP infrastructure with security, RBAC, governance"
**Needs:** Enterprise gateways, audit, auth
**Looking for:** microsoft/mcp-gateway, lasso-security, Azure APIM

### Persona 6: "Framework Evaluator"
**Goal:** "I'm choosing a framework/language for building MCP tools"
**Needs:** Language/framework comparison
**Looking for:** By-language breakdown (Python, TypeScript, Go, Java, R)

### Persona 7: "Security Reviewer"
**Goal:** "I need to assess security of MCP tools before deploying"
**Needs:** Security analysis, code patterns
**Looking for:** security.md, per-project security findings

## Proposed Category Taxonomy

### Current Categories (keep)
```
cli-client           # CLI interfaces for MCP
http-bridge          # stdio ↔ HTTP conversion
websocket-bridge     # stdio ↔ WebSocket
grpc-bridge          # MCP ↔ gRPC/protobuf
rest-api-bridge      # OpenAI-compatible REST
proxy-aggregator     # Multi-server proxy
enterprise-gateway   # Production gateway
kubernetes-integration
docker-integration
specialized-adapter
official-tool
```

### New Categories (add)
```
openapi-to-mcp       # Convert OpenAPI specs → MCP servers
mcp-to-openapi       # Expose MCP servers as REST/OpenAPI
mcp-framework        # Libraries for building MCP (FastMCP, Spring AI)
bidirectional-bridge # Both directions
cloud-integration    # Cloud platform integrations (Azure APIM, etc.)
```

## Proposed File Structure

```
comparisons/
├── auto-generated.md      # Full tables (existing)
├── features.md            # Features by category (existing)
├── security.md            # Security analysis (existing)
├── transports.md          # Transport protocols (existing)
├── openapi-to-mcp.md      # NEW: OpenAPI → MCP tools
├── mcp-to-openapi.md      # NEW: MCP → REST tools
├── by-language.md         # NEW: Tools by programming language
├── by-use-case.md         # NEW: Decision trees, recommendations
└── enterprise.md          # NEW: Enterprise-focused comparison
```

## README Restructure

### Current Structure
- What is MCP?
- Quick Stats
- Top Projects by Stars
- Official/Reputable Sources
- Transport Support
- Detailed Comparisons
- Project Data
- Scripts
- Repository Structure
- Contributing
- Security Considerations
- Research Resources
- License

### Proposed Structure
```markdown
# MCP Ecosystem Tools Comparison

Brief intro...

## 🎯 Quick Navigation (by Goal)

| I want to... | Go to... |
|--------------|----------|
| Connect my REST API to AI agents | [OpenAPI → MCP Guide](comparisons/openapi-to-mcp.md) |
| Expose my MCP server as REST | [MCP → REST Guide](comparisons/mcp-to-openapi.md) |
| Use a CLI with MCP servers | [CLI Clients](#cli-clients) |
| Bridge MCP across transports | [Transport Bridges](comparisons/transports.md) |
| Deploy enterprise MCP infrastructure | [Enterprise Guide](comparisons/enterprise.md) |
| Choose by programming language | [By Language](comparisons/by-language.md) |
| See everything | [Full Comparison](comparisons/auto-generated.md) |

## 📊 Ecosystem Overview

Stats covering all tool types...

## 🔄 OpenAPI ↔ MCP Tools

### OpenAPI → MCP (Make your API AI-callable)
Quick table of top tools...

### MCP → OpenAPI (Expose MCP as REST)
Quick table of top tools...

## 💻 CLI Clients & Development Tools
...existing content refactored...

## 🔌 Transport Bridges
...existing content...

## 🏢 Enterprise & Cloud
...existing + Azure APIM, etc...

## 📚 Detailed Comparisons
Links to all comparison documents...

## 🔧 For Contributors
...
```

## New Projects to Add (from research)

### OpenAPI → MCP Category
1. ouvreboite/openapi-to-mcp (TypeScript, npm)
2. cnoe-io/openapi-mcp-codegen (Python, Cisco)
3. jlowin/fastmcp (Python, framework)
4. Vizioz/Swagger-MCP (TypeScript)
5. ivo-toby/mcp-openapi-server
6. janwilmake/openapi-mcp-server
7. higress-group/openapi-to-mcpserver
8. ckanthony/openapi-mcp
9. spring-ai-community/mcp-annotations (Java)

### MCP → OpenAPI Category
1. open-webui/mcpo (Python, official)
2. Azure API Management MCP (Microsoft, cloud)

### Already Tracked (may need category update)
- steipete/mcporter (already tracked, may fit openapi-to-mcp)
- f/mcptools (already tracked, multi-purpose)

## Schema Updates (spec.yaml)

Add to category enum:
```yaml
category:
  enum:
    # ... existing ...
    - openapi-to-mcp
    - mcp-to-openapi
    - mcp-framework
    - cloud-integration
```

Add new fields:
```yaml
# Conversion direction (for bridge/conversion tools)
conversion-direction:
  type: string
  enum:
    - openapi-to-mcp
    - mcp-to-openapi
    - bidirectional
  description: "For conversion tools, which direction they convert"

# Framework/runtime info
framework:
  type: string
  description: "If tool is a framework, what it's for (e.g., 'MCP server building')"

# Cloud platform
cloud-platform:
  type: string
  description: "Associated cloud platform (Azure, AWS, GCP)"
```

## Implementation Order

1. **Phase 1: Schema & Structure**
   - Update spec.yaml with new categories
   - Create placeholder comparison files
   - Update generate-tables.py to handle new categories

2. **Phase 2: New Project Data**
   - Create YAML files for ~10 new projects from research
   - Focus on OpenAPI↔MCP tools first

3. **Phase 3: Comparison Documents**
   - Create openapi-to-mcp.md
   - Create mcp-to-openapi.md
   - Create by-use-case.md with decision trees

4. **Phase 4: README Restructure**
   - Reorganize with persona-based navigation
   - Add quick navigation table
   - Ensure each persona can find their content in &lt;10 seconds

5. **Phase 5: Documentation**
   - Update CONTRIBUTING.md
   - Update GUIDELINES.md
   - Add new categories explanation

## Success Criteria

1. **Discoverability**: Any reader persona can find relevant tools in <10 seconds from README
2. **Completeness**: All major OpenAPI↔MCP tools are tracked
3. **Navigation**: Clear paths between related content
4. **Maintainability**: New tool additions follow clear patterns
5. **Comparison Value**: Easy side-by-side comparison for decision-making

## Questions to Resolve

1. Should we rename the repo from "mcp-client-tools" to "mcp-ecosystem-tools"?
2. How to handle tools that span multiple categories (e.g., mcptools does CLI + bridging)?
3. Should enterprise/cloud tools be separate comparison or integrated?
