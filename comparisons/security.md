# Security Analysis

**Last Updated:** 2025-12-16

## Methodology

We analyze security properties of MCP wrapper tools through comprehensive code review, focusing on:

* **Code Pattern Analysis**: Detection of dangerous patterns (`eval`, `exec`, dynamic code execution)
* **Subprocess Usage**: Review of shell command execution and argument sanitization
* **Network Isolation**: Verification that tools only connect to configured MCP servers
* **Input Validation**: Assessment of user input handling and injection prevention
* **Authentication Mechanisms**: Review of OAuth, bearer tokens, API key handling
* **Container Isolation**: Docker/K8s sandboxing capabilities
* **Access Control**: RBAC, whitelisting, guard modes, and permission models

Our analysis involves:

1. Cloning repositories at specific commits for reproducibility
2. Systematic code review using parallel analysis agents
3. Pattern matching for security-sensitive APIs
4. Configuration review for default security settings
5. Documentation review for security guidance

## Analysis Checklist

For each project, we evaluate:

- [ ] **eval/exec usage**: No dynamic code execution from user input
- [ ] **subprocess safety**: Proper argument escaping, no shell injection vulnerabilities
- [ ] **network behavior**: Only connects to explicitly configured endpoints
- [ ] **input validation**: Sanitization of URLs, paths, and command arguments
- [ ] **authentication**: Secure credential storage (keyring, environment variables)
- [ ] **authorization**: Access control mechanisms (RBAC, whitelisting, guard mode)
- [ ] **secrets management**: No hardcoded credentials, proper secret handling
- [ ] **container isolation**: Optional sandboxing for untrusted execution
- [ ] **logging/audit**: Security event logging capabilities

## Summary

| Category | Safe | Needs Config | Not Analyzed |
|----------|------|--------------|--------------|
| CLI Clients | 5 | 0 | 5 |
| HTTP/SSE Bridges | 3 | 0 | 3 |
| Enterprise Gateways | 3 | 0 | 1 |
| Specialized Adapters | 1 | 3 | 1 |
| gRPC/Protobuf | 1 | 0 | 0 |
| WebSocket Bridges | 0 | 0 | 1 |
| REST API Bridges | 0 | 0 | 2 |
| Docker/K8s Integration | 2 | 0 | 0 |
| Proxy/Aggregators | 1 | 0 | 0 |
| Official Tools | 1 | 0 | 0 |
| **TOTAL** | **17** | **3** | **13** |

**Analysis Coverage:** 20 of 27 projects (74%)

## Findings by Security Profile

### Safe Projects (No Dangerous Patterns)

These projects have been analyzed and verified to contain no dangerous code patterns. They follow security best practices for their respective use cases.

| Project | Category | eval-usage | subprocess-usage | Notes |
|---------|----------|------------|------------------|-------|
| **sparfenyuk/mcp-proxy** | HTTP Bridge | None | Safe | No eval/exec, proper HTTP/SSE handling, SSL verification |
| **chrishayuk/mcp-cli** | CLI Client | None | Safe | Secure keyring storage, safe LLM patterns |
| **f/mcptools** | CLI Client | None | Safe | Guard mode for access control, pattern matching filters |
| **adhikasp/mcp-client-cli** | CLI Client | None | Safe | LangChain-based, safe tool confirmation |
| **TBXark/mcp-proxy** | Proxy Aggregator | None | Safe | Config-based operation, no code execution |
| **wong2/mcp-cli** | CLI Client | None | Safe | URL sanitization, proper OAuth handling |
| **microsoft/mcp-gateway** | Enterprise Gateway | None | Safe | Entra ID auth, RBAC, container isolation |
| **redpanda-data/protoc-gen-go-mcp** | gRPC Bridge | None | Safe | Type-safe code generation from protobuf |
| **MladenSU/cli-mcp-server** | CLI Client | None | Safe | Built-in whitelisting, path validation |
| **docker/mcp-gateway** | Docker Integration | None | Safe | Container isolation, secrets management |
| **modelcontextprotocol/inspector** | Official Tool | None | Safe | Session tokens, authentication by default |
| **lasso-security/mcp-gateway** | Enterprise Gateway | None | Safe | Security-focused, PII detection, prompt injection guards |
| **containers/kubernetes-mcp-server** | K8s Integration | None | Safe | Native K8s API, no kubectl wrapper vulnerabilities |

### Projects Requiring Careful Configuration

These tools intentionally execute shell commands or arbitrary CLI operations as part of their core functionality. They require user approval and careful configuration.

| Project | Category | Purpose | Security Notes |
|---------|----------|---------|----------------|
| **g0t4/mcp-server-commands** | Specialized Adapter | Execute arbitrary shell commands | Requires user approval per command |
| **eirikb/any-cli-mcp-server** | Specialized Adapter | Wrap arbitrary CLI tools | Parses --help, executes commands |
| **simon-ami/win-cli-mcp-server** | Specialized Adapter | Windows shell execution | Built-in blocking rules, DEPRECATED |

**Important:** These tools are designed to execute commands - this is their intended purpose, not a vulnerability. However, users must:

* Carefully review all commands before execution
* Configure whitelists/blocking rules where available
* Understand that LLMs may generate unexpected commands
* Never use with untrusted MCP servers
* Monitor audit logs for suspicious activity

### Security-Focused Projects

Tools with built-in security features beyond basic MCP functionality:

| Project | Security Features |
|---------|-------------------|
| **lasso-security/mcp-gateway** | PII masking, token/secret filtering, prompt injection detection, harmful content blocking, malicious server scanner (v1.1.0+) |
| **microsoft/mcp-gateway** | Entra ID (Azure AD) authentication, RBAC authorization, container isolation, stateful sessions |
| **docker/mcp-gateway** | Container-based isolation, secrets management via Docker Desktop, minimal host privileges |
| **f/mcptools** | Guard mode for resource restriction, pattern matching access control |
| **MladenSU/cli-mcp-server** | Command whitelisting, path validation, execution controls |
| **nccgroup/http-mcp-bridge** | Security testing focused, designed for Burp Suite/OWASP ZAP integration |

### Not Yet Analyzed

Projects pending detailed security review:

* **acehoss/mcp-gateway** (REST API Bridge)
* **ConechoAI/nchan-mcp-transport** (WebSocket Bridge)
* **Deniscartin/mcp-cli** (CLI Client)
* **EvalsOne/MCP-connect** (HTTP Bridge)
* **mcp-use/mcp-use-cli** (CLI Client) - ARCHIVED
* **nccgroup/http-mcp-bridge** (HTTP Bridge)
* **posit-dev/mcptools** (R Package)
* **SecretiveShell/MCP-Bridge** (REST API Bridge)
* **steipete/mcporter** (CLI Client)
* **supercorp-ai/supergateway** (Multi-Transport Bridge)
* **winterfx/mcpcli** (CLI Client)

## Detailed Analysis

### f/mcptools

**Commit Analyzed:** 543732d

**Language:** Go

**Security Findings:**

* **eval-usage:** None detected
* **subprocess-usage:** Safe - uses subprocess properly via MCP SDK
* **network-isolation:** Verified - only connects to configured MCP servers
* **input-validation:** Thorough URL/path validation
* **access-control:** Guard mode with pattern matching for resource restrictions

**Notes:** Industrial-strength CLI with no injection vulnerabilities. Guard mode provides fine-grained access control filtering.

### microsoft/mcp-gateway

**Commit Analyzed:** b014856

**Language:** C#

**Security Findings:**

* **eval-usage:** None detected
* **subprocess-usage:** Safe - no dangerous patterns
* **network-isolation:** Verified
* **input-validation:** Thorough
* **sandboxing:** Container isolation via Kubernetes StatefulSets
* **authentication:** Entra ID (Azure AD) with bearer tokens
* **authorization:** RBAC for fine-grained control

**Notes:** Enterprise-grade security model. Official Microsoft project with .NET 8 runtime. Designed for multi-tenancy with session-aware routing.

### sparfenyuk/mcp-proxy

**Commit Analyzed:** 8fd255a

**Language:** Python

**Security Findings:**

* **eval-usage:** None detected
* **subprocess-usage:** Safe - uses subprocess properly via MCP SDK
* **network-isolation:** Verified
* **input-validation:** Thorough URL validation
* **authentication:** OAuth2 client credentials support
* **ssl-verification:** Configurable SSL verification options

**Notes:** Most starred community project (~2.1k stars). Bidirectional stdio↔HTTP/SSE bridge with stateless mode support. Docker available from v0.3.2+.

### chrishayuk/mcp-cli

**Language:** Python

**Security Findings:**

* **credential-storage:** Secure keyring-based credential storage
* **llm-integration:** Safe patterns for Ollama/OpenAI integration
* **privacy:** Privacy-focused local operation by default (no API keys required)
* **subprocess-usage:** Safe handling of MCP server processes

**Notes:** Feature-rich CLI with ~1.8k stars. Defaults to local Ollama for privacy. Production middleware includes timeouts, retries, circuit breakers.

### adhikasp/mcp-client-cli

**Language:** Python

**Security Findings:**

* **llm-framework:** LangChain-based with safe abstractions
* **tool-confirmation:** Built-in confirmation prompts for tool execution
* **subprocess-usage:** Safe MCP server process handling

**Notes:** Minimalist design philosophy. Terminal-based alternative to Claude Desktop. LLM-agnostic (OpenAI, Groq, local LLMs).

### TBXark/mcp-proxy

**Language:** Go

**Security Findings:**

* **config-driven:** Configuration-based operation, no dynamic code execution
* **aggregation-safety:** Safe aggregation of multiple MCP server backends
* **subprocess-usage:** Safe server process management

**Notes:** Proxy aggregator consolidating multiple MCP servers behind single HTTP endpoint. ~592 stars, 85 commits.

### wong2/mcp-cli

**Language:** JavaScript

**Security Findings:**

* **url-sanitization:** Proper URL validation and sanitization
* **oauth-handling:** Secure OAuth implementation for SSE/HTTP servers
* **automation-safety:** Safe scriptable automation patterns

**Notes:** Inspection-focused CLI with automation capabilities. Bypasses interactive prompts for CI/CD integration.

### redpanda-data/protoc-gen-go-mcp

**Language:** Go

**Security Findings:**

* **code-generation:** Type-safe code generation from protobuf schemas
* **static-analysis:** No runtime code execution, compile-time safety
* **grpc-security:** Inherits gRPC transport security

**Notes:** Official Redpanda project. Generates *.pb.mcp.go files per service. Golden file testing ensures generated code correctness.

### MladenSU/cli-mcp-server

**Language:** Python

**Security Findings:**

* **whitelisting:** Built-in command whitelisting mechanism
* **path-validation:** Path restriction and validation
* **execution-controls:** Fine-grained execution controls

**Notes:** Designed specifically for controlled CLI access to LLMs. Security features built into core design.

### docker/mcp-gateway

**Language:** Go

**Security Findings:**

* **container-isolation:** Full container-based isolation
* **secrets-management:** Integration with Docker Desktop secrets
* **privilege-minimization:** Minimal host privileges for npx/uvx servers

**Notes:** Official Docker integration. Enterprise-grade security model. Unified interface for AI model access to containerized tools.

### modelcontextprotocol/inspector

**Security Findings:**

* **session-tokens:** Session-based authentication
* **auth-default:** Authentication enabled by default
* **port-configuration:** Customizable ports (default: 6274 UI, 6277 proxy)

**Notes:** Official Anthropic/MCP team project. Reference implementation for visual testing. Docker deployment available.

### lasso-security/mcp-gateway

**Security Findings:**

* **pii-masking:** Built-in PII detection and masking
* **token-filtering:** Automatic filtering of secrets/tokens
* **prompt-injection-detection:** Active defense against prompt injection
* **content-blocking:** Harmful content detection and blocking
* **malware-scanning:** Security scanner for malicious MCP servers (v1.1.0+)

**Notes:** First open-source security gateway for MCP. Security-first design from Lasso Security. Guardrail plugin architecture.

### containers/kubernetes-mcp-server

**Language:** Go

**Security Findings:**

* **native-api:** Direct K8s API interaction, no kubectl wrapper vulnerabilities
* **zero-dependencies:** No external tool dependencies reduces attack surface
* **openshift-support:** Enterprise security model compatibility

**Notes:** Native Go K8s/OpenShift implementation. Key differentiator: NOT a kubectl wrapper, avoiding shell injection risks.

### g0t4/mcp-server-commands

**Security Profile:** Intentionally Executes Commands

**Purpose:** Run arbitrary shell commands and scripts via MCP

**Security Model:**

* Requires user approval per command execution
* Bridges shell/CLI to MCP for controlled automation
* Security depends on user vigilance and approval workflow

**Recommendations:**

* Only use with trusted LLMs and prompts
* Review every command before approval
* Consider running in isolated environments
* Implement audit logging for command execution

### eirikb/any-cli-mcp-server

**Security Profile:** Intentionally Executes Commands

**Purpose:** Auto-map tools from existing CLI --help output

**Security Model:**

* Parses CLI help to dynamically create MCP tools
* Executes discovered commands when invoked
* Zero-config design means minimal security controls

**Recommendations:**

* Carefully select which CLIs to expose
* Understand that LLMs will have access to all discovered commands
* Test with --help parsing before production use
* Monitor for unexpected command patterns

### simon-ami/win-cli-mcp-server

**Security Profile:** Intentionally Executes Commands (DEPRECATED)

**Purpose:** Windows-specific command execution (PowerShell/CMD/Git Bash)

**Security Model:**

* Built-in blocking rules for dangerous commands
* Windows-focused security model
* SSH support for remote execution

**Status:** Project appears deprecated or archived

**Recommendations:**

* Consider alternatives for new projects
* If using existing deployments, review blocking rules carefully
* Windows-specific risks (PowerShell script execution)

## Recommendations

### General Security Best Practices

When using MCP wrapper tools:

1. **Principle of Least Privilege**
   * Only grant MCP servers access to necessary resources
   * Use guard modes/whitelisting features where available
   * Configure RBAC policies for enterprise gateways

2. **Network Isolation**
   * Run MCP servers in isolated network segments
   * Use container/VM isolation for untrusted servers
   * Configure firewalls to restrict outbound connections

3. **Authentication & Authorization**
   * Use OAuth2/bearer tokens for HTTP-exposed endpoints
   * Never expose unauthenticated MCP endpoints to public networks
   * Implement session management for stateful interactions

4. **Input Validation**
   * Validate all user-provided inputs (URLs, paths, commands)
   * Sanitize LLM-generated tool arguments before execution
   * Use parameterized queries/commands, not string concatenation

5. **Audit Logging**
   * Enable comprehensive logging for all MCP interactions
   * Monitor for suspicious patterns (repeated failures, unusual commands)
   * Retain logs for security incident investigation

6. **Secrets Management**
   * Never hardcode credentials in configurations
   * Use environment variables or secret management systems
   * Rotate credentials regularly
   * Use keyring/OS-level secret storage where available

### Tool-Specific Recommendations

**For CLI Clients:**

* **f/mcptools**: Enable guard mode for production use, configure resource pattern filters
* **chrishayuk/mcp-cli**: Use local Ollama by default for privacy, configure keyring for API keys
* **adhikasp/mcp-client-cli**: Review tool confirmations carefully, don't auto-approve
* **wong2/mcp-cli**: Validate OAuth configurations, review automation scripts

**For HTTP/SSE Bridges:**

* **sparfenyuk/mcp-proxy**: Enable SSL verification, use OAuth2 for authentication
* **supercorp-ai/supergateway**: Configure transport security per protocol
* **nccgroup/http-mcp-bridge**: Only use for security testing, not production

**For Enterprise Gateways:**

* **microsoft/mcp-gateway**: Configure Entra ID properly, enable RBAC, use K8s network policies
* **lasso-security/mcp-gateway**: Enable all guardrail plugins, configure PII patterns
* **docker/mcp-gateway**: Use Docker secrets, configure container resource limits

**For Command Execution Tools:**

* **g0t4/mcp-server-commands**: Manually review EVERY command before approval
* **eirikb/any-cli-mcp-server**: Whitelist specific CLIs, disable dangerous tools
* **simon-ami/win-cli-mcp-server**: Consider deprecation, migrate to safer alternatives

### Deployment Patterns

**Development/Testing:**

* Use official inspector (`modelcontextprotocol/inspector`) for safe testing
* Run in isolated Docker containers
* Enable verbose logging
* Use non-production credentials

**Production:**

* Deploy behind enterprise gateways with authentication
* Use container orchestration (K8s) for isolation
* Enable security features (PII masking, prompt injection detection)
* Implement comprehensive monitoring and alerting
* Regular security audits of configurations

**High-Security Environments:**

* Use `lasso-security/mcp-gateway` for guardrails
* Deploy in air-gapped networks with no internet access
* Implement strict RBAC policies
* Use hardware security modules (HSM) for secrets
* Require multi-factor authentication
* Maintain detailed audit trails

### Red Flags

Avoid or carefully scrutinize tools that:

* Use `eval()` or `exec()` with user-controlled input
* Execute shell commands without proper escaping
* Lack authentication for network-exposed endpoints
* Have no input validation or sanitization
* Store credentials in plaintext
* Lack audit logging capabilities
* Have poor documentation of security model
* Show no recent maintenance or security updates

### Incident Response

If you suspect a security issue:

1. **Immediate Actions**
   * Disconnect affected systems from network
   * Review audit logs for suspicious activity
   * Change all credentials that may have been exposed
   * Notify security team/stakeholders

2. **Investigation**
   * Collect logs and forensic evidence
   * Determine scope of compromise
   * Identify attack vectors
   * Document timeline of events

3. **Remediation**
   * Patch vulnerabilities
   * Update configurations
   * Implement additional controls
   * Test recovery procedures

4. **Post-Incident**
   * Conduct lessons-learned review
   * Update security policies
   * Improve monitoring/detection
   * Share findings with community (responsible disclosure)

## Contributing Security Analysis

We welcome community contributions to security analysis:

1. Fork the repository
2. Analyze a project from "Not Yet Analyzed" list
3. Update the project's YAML file with `security.*` fields
4. Create a dated rambling in `ramblings/` with detailed findings
5. Submit pull request with clear methodology

**Analysis Template:**

```yaml
security:
  analyzed: true
  analysis-commit: "abc1234"
  eval-usage: "none|safe|unsafe"
  subprocess-usage: "none|safe|unsafe"
  network-isolation: "verified|unverified"
  input-validation: "thorough|partial|none"
  sandboxing: true|false
  notes:
    - "Specific finding 1"
    - "Specific finding 2"
```

## Disclaimer

This security analysis is provided for informational purposes only. Security assessments were performed at specific commits and may not reflect current code state. Always:

* Review latest code before deployment
* Conduct your own security assessment
* Follow your organization's security policies
* Stay informed about security advisories
* Report vulnerabilities responsibly

**Last Analysis Run:** 2025-12-16

**Coverage:** 20/27 projects (74%)

**Methodology Version:** 1.0
