# Choose an MCP Ecosystem Tool

Interactive guide to selecting the right tool from 38+ MCP ecosystem projects

## Interactive Guide

**Click to expand each section** and drill down to find the right tool for your needs.

<details open>
<summary>🔍 <strong>What's your primary use case?</strong></summary>

<details>
<summary>│  ├─ 📂 CLI - Interactive command-line usage</summary>

<details>
<summary>│  │  ├─ ❓ Do you need LLM integration (chat with AI)?</summary>

<details>
<summary>│  │  │  ├─ 📂 Yes - Chat interface with LLM</summary>

<details>
<summary>│  │  │  │  ├─ ❓ Which LLM provider?</summary>

<details>
<summary>│  │  │  │  │  ├─ 📌 OpenAI-compatible (OpenAI, Groq, local)</summary>

│  │  │  │  │  │
│  │  │  │  │  ├── ✅ **Use adhikasp/mcp-client-cli**
│  │  │  │  │  │   • `adhikasp/mcp-client-cli`
│  │  │  │  │  │
│  │  │  │  │  └── *LLM-agnostic, supports OpenAI, Groq, and local LLMs*

</details>

<details>
<summary>│  │  │  │  │  └─ 📌 Multiple providers / flexible</summary>

│  │  │  │  │  │
│  │  │  │  │  ├── ✅ **Use chrishayuk/mcp-cli**
│  │  │  │  │  │   • `chrishayuk/mcp-cli`
│  │  │  │  │  │
│  │  │  │  │  └── *1.8k stars, multiple modes: chat, interactive shell, command-line*

</details>

</details>
</details>

<details>
<summary>│  │  │  └─ 📂 No - Just call MCP tools directly</summary>

<details>
<summary>│  │  │  │  ├─ ❓ Need scriptable/automation support?</summary>

<details>
<summary>│  │  │  │  │  ├─ 📌 Yes - Scripting and automation</summary>

│  │  │  │  │  │
│  │  │  │  │  ├── ✅ **Use wong2/mcp-cli**
│  │  │  │  │  │   • `wong2/mcp-cli`
│  │  │  │  │  │
│  │  │  │  │  └── *Scriptable automation, bypasses interactive prompts*

</details>

<details>
<summary>│  │  │  │  │  └─ 📌 No - Interactive shell is fine</summary>

│  │  │  │  │  │
│  │  │  │  │  ├── ✅ **Use f/mcptools**
│  │  │  │  │  │   • `f/mcptools`
│  │  │  │  │  │
│  │  │  │  │  └── *1.4k stars, Go-based, interactive shell with persistent connection*

</details>

</details>
</details>

</details>
</details>

<details>
<summary>│  ├─ 📂 REST API - Expose MCP as HTTP endpoints</summary>

<details>
<summary>│  │  ├─ ❓ Need OpenAPI/Swagger documentation?</summary>

<details>
<summary>│  │  │  ├─ 📌 Yes - Full OpenAPI spec</summary>

│  │  │  │
│  │  │  ├── ✅ **Use acehoss/mcp-gateway**
│  │  │  │   • `acehoss/mcp-gateway`
│  │  │  │
│  │  │  └── *REST API exposure with automatic OpenAPI/Swagger generation*

</details>

<details>
<summary>│  │  │  └─ 📌 OpenAI-compatible API format</summary>

│  │  │  │
│  │  │  ├── ✅ **Use SecretiveShell/MCP-Bridge**
│  │  │  │   • `SecretiveShell/MCP-Bridge`
│  │  │  │
│  │  │  └── *882 stars, middleware providing OpenAI-compatible endpoints*

</details>

</details>
</details>

<details>
<summary>│  ├─ 📂 Transport Bridge - stdio ↔ HTTP/SSE/WebSocket</summary>

<details>
<summary>│  │  ├─ ❓ Which transport do you need?</summary>

<details>
<summary>│  │  │  ├─ 📌 SSE (Server-Sent Events)</summary>

│  │  │  │
│  │  │  ├── ✅ **Use sparfenyuk/mcp-proxy**
│  │  │  │   • `sparfenyuk/mcp-proxy`
│  │  │  │
│  │  │  └── *2.1k stars, most popular transport bridge*

</details>

<details>
<summary>│  │  │  ├─ 📂 WebSocket</summary>

<details>
<summary>│  │  │  │  ├─ ❓ Need Nginx/scalable infrastructure?</summary>

<details>
<summary>│  │  │  │  │  ├─ 📌 Yes - Production scale</summary>

│  │  │  │  │  │
│  │  │  │  │  ├── ✅ **Use ConechoAI/nchan-mcp-transport**
│  │  │  │  │  │   • `ConechoAI/nchan-mcp-transport`
│  │  │  │  │  │
│  │  │  │  │  └── *Nchan-based, supports WebSocket, SSE, HTTP*

</details>

<details>
<summary>│  │  │  │  │  └─ 📌 No - Simple WebSocket</summary>

│  │  │  │  │  │
│  │  │  │  │  ├── ✅ **Use supercorp-ai/supergateway**
│  │  │  │  │  │   • `supercorp-ai/supergateway`
│  │  │  │  │  │
│  │  │  │  │  └── *stdio to SSE/WebSocket bridge*

</details>

</details>
</details>

<details>
<summary>│  │  │  └─ 📌 HTTP (stateless)</summary>

│  │  │  │
│  │  │  ├── ✅ **Use EvalsOne/MCP-connect or nccgroup/http-mcp-bridge**
│  │  │  │   • `EvalsOne/MCP-connect`
│  │  │  │   • `nccgroup/http-mcp-bridge`
│  │  │  │
│  │  │  └── *Both support stdio to HTTP bridging*

</details>

</details>
</details>

<details>
<summary>│  ├─ 📂 Enterprise - Production infrastructure</summary>

<details>
<summary>│  │  ├─ ❓ What's your deployment environment?</summary>

<details>
<summary>│  │  │  ├─ 📌 Kubernetes</summary>

│  │  │  │
│  │  │  ├── ✅ **Use microsoft/mcp-gateway**
│  │  │  │   • `microsoft/mcp-gateway`
│  │  │  │
│  │  │  └── *Kubernetes-native with StatefulSets, headless services*

</details>

<details>
<summary>│  │  │  ├─ 📌 Docker/Containers</summary>

│  │  │  │
│  │  │  ├── ✅ **Use docker/mcp-gateway**
│  │  │  │   • `docker/mcp-gateway`
│  │  │  │
│  │  │  └── *Official Docker gateway with container-based isolation*

</details>

<details>
<summary>│  │  │  ├─ 📌 Azure cloud</summary>

│  │  │  │
│  │  │  ├── ✅ **Use Azure API Management MCP integration**
│  │  │  │   • `microsoft/azure-api-management-mcp`
│  │  │  │
│  │  │  └── *Native Azure integration*

</details>

<details>
<summary>│  │  │  └─ 📌 Security-focused (PII, guardrails)</summary>

│  │  │  │
│  │  │  ├── ✅ **Use lasso-security/mcp-gateway**
│  │  │  │   • `lasso-security/mcp-gateway`
│  │  │  │
│  │  │  └── *PII masking, security guardrails*

</details>

</details>
</details>

<details>
<summary>│  ├─ 📂 OpenAPI ↔ MCP Conversion</summary>

<details>
<summary>│  │  ├─ ❓ Which direction?</summary>

<details>
<summary>│  │  │  ├─ 📌 OpenAPI → MCP (expose REST as MCP)</summary>

│  │  │  │
│  │  │  └── ✅ **See openapi-to-mcp category in comparisons/auto-generated.md**

</details>

<details>
<summary>│  │  │  └─ 📌 MCP → OpenAPI (generate OpenAPI from MCP)</summary>

│  │  │  │
│  │  │  └── ✅ **See mcp-to-openapi category in comparisons/auto-generated.md**

</details>

</details>
</details>

<details>
<summary>│  ├─ 📌 gRPC/Protobuf - Convert gRPC to MCP</summary>

│  │
│  ├── ✅ **Use redpanda-data/protoc-gen-go-mcp**
│  │   • `redpanda-data/protoc-gen-go-mcp`
│  │
│  └── *protoc plugin generating MCP servers from gRPC/Connect service definitions*

</details>

<details>
<summary>│  └─ 📂 Specialized - CLI wrapping, Windows, Kubernetes</summary>

<details>
<summary>│  │  ├─ ❓ What specialization?</summary>

<details>
<summary>│  │  │  ├─ 📌 Wrap existing CLI tools as MCP</summary>

│  │  │  │
│  │  │  ├── ✅ **Use eirikb/any-cli-mcp-server**
│  │  │  │   • `eirikb/any-cli-mcp-server`
│  │  │  │
│  │  │  └── *Maps tools from existing CLI help output to MCP*

</details>

<details>
<summary>│  │  │  ├─ 📌 Windows PowerShell/CMD</summary>

│  │  │  │
│  │  │  ├── ✅ **Use simon-ami/win-cli-mcp-server**
│  │  │  │   • `simon-ami/win-cli-mcp-server`
│  │  │  │
│  │  │  └── *Secure Windows CLI server for PowerShell and CMD*

</details>

<details>
<summary>│  │  │  ├─ 📌 Kubernetes/OpenShift</summary>

│  │  │  │
│  │  │  ├── ✅ **Use containers/kubernetes-mcp-server**
│  │  │  │   • `containers/kubernetes-mcp-server`
│  │  │  │
│  │  │  └── *Native Go K8s/OpenShift MCP server*

</details>

<details>
<summary>│  │  │  └─ 📌 Run arbitrary shell commands</summary>

│  │  │  │
│  │  │  ├── ✅ **Use g0t4/mcp-server-commands**
│  │  │  │   • `g0t4/mcp-server-commands`
│  │  │  │
│  │  │  └── *MCP server to run shell commands and scripts*

</details>

</details>
</details>

</details>

---

**Other views:** [Mermaid Flowchart](decision-tree.md) | [Full comparison tables](auto-generated.md) | [Security analysis](security.md)

*Auto-generated from `r-and-d/decision-tree-generator/examples/mcp-tool-chooser.yaml`*
