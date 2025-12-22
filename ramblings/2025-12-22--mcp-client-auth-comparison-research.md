# MCP Client Authentication Capabilities: Comprehensive Comparison

**Research Date:** 2025-12-22
**Protocol Version Context:** MCP spec evolved significantly through 2025 (2025-03-26, 2025-06-18, 2025-11-25 releases)

## Executive Summary: Authentication Landscape

MCP authentication bifurcates along **transport mechanism** boundaries:

* **STDIO (local process):** Environment variable injection, OS keychain integration, no OAuth (spec-discouraged)
* **HTTP/SSE (remote):** OAuth 2.1 mandatory, resource indicators (RFC 8707), PKCE, token audience validation

**Critical Insight:** Most clients exhibit **implementation lag** behind spec—many support basic env vars but lack OAuth refresh logic, dynamic client registration, or secure credential storage.

---

## Transport-Level Authentication Dichotomy

| Dimension | STDIO Transport | HTTP/SSE Transport |
|-----------|----------------|-------------------|
| **Threat Model** | OS process isolation; local attacker | Network-based; MITM, token theft |
| **Auth Mechanism** | ENV vars, device flow (optional) | OAuth 2.1 (mandatory per spec) |
| **Credential Passing** | `env: { API_KEY: "..." }` in config | `Authorization: Bearer` header + OAuth |
| **Spec Guidance** | "SHOULD NOT use OAuth" | "MUST implement OAuth 2.1" |
| **Use Cases** | CLI tools, IDE extensions, single-user desktop | Production web services, multi-tenant SaaS |
| **Security Posture** | Filesystem permissions + keychain | TLS, PKCE, token binding, audience validation |

**Rationale:** STDIO's threat model assumes mutual trust between spawned process and parent; HTTP assumes zero-trust network environment requiring cryptographic auth.

---

## Per-Client Authentication Matrix

### 1. Claude Desktop (Reference Implementation)

**Transport Support:** STDIO (primary), HTTP (limited)
**Auth Methods:**

* ✅ **Environment Variables:** `env: { API_KEY: "..." }` in `claude_desktop_config.json`
* ✅ **OAuth 2.0:** Support for remote servers (as of late 2024)
* ⚠️ **Variable Expansion:** `${VAR:-default}` syntax in config (Claude Code CLI)
* ❌ **Token Refresh:** Implicit (handled by SDK)

**Configuration Pattern:**

```json
{
  "mcpServers": {
    "weather": {
      "command": "node",
      "args": ["weather-server.js"],
      "env": { "API_KEY": "your-api-key" }
    },
    "remote-api": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": { "Authorization": "Bearer ${API_KEY}" }
    }
  }
}
```

**Pain Points:**

* [Bug #1254](https://github.com/anthropics/claude-code/issues/1254): ENV vars not passed to servers during initialization (crash on auth errors)
* Windows `%APPDATA%` expansion requires manual config editing
* No built-in secure prompt for API keys (stored plaintext in JSON)

**Credential Storage:** Plaintext in `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)
**Best Practice:** Use `${ENV_VAR}` refs + system keychain integration via wrapper scripts

**Sources:**

* [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp)
* [Claude Code Issue #1254](https://github.com/anthropics/claude-code/issues/1254)

---

### 2. Cursor IDE

**Transport Support:** STDIO, HTTP (SSE)
**Auth Methods:**

* ✅ **Environment Variables:** Standard `env` block
* ⚠️ **OAuth 2.0:** Supported but **broken implementation** (active bugs)
* ❌ **Token Refresh:** Non-functional (Issue #130765)

**Critical Bugs:**

1. **[Issue #3734](https://github.com/cursor/cursor/issues/3734):** Dynamic client registration sends `token_endpoint_auth_method: "none"` but includes `Authorization: Basic` header (spec violation)
2. **Token Refresh Failure:** Access token expiry → 401 → server marked "Logged out" → manual re-auth required (no automatic refresh)
3. **OAuth Flow:** Works for initial connection but breaks on token expiration

**Configuration Example:**

```json
{
  "mcpServers": {
    "remote-server": {
      "type": "http",
      "url": "https://api.example.com/mcp",
      "headers": { "Authorization": "Bearer <token>" }
    }
  }
}
```

**Pain Points:**

* OAuth is "only MCP-native auth protocol" but Cursor's implementation is **enterprise-hostile** (no refresh, manual re-auth)
* Remote SSE-only MCPs **cannot use API keys** (forced into broken OAuth path)
* Community demand for OAuth fixes (Forum: [91719](https://forum.cursor.com/t/we-need-cursor-to-support-oauth-flow-for-remote-mcp-servers/91719))

**Sources:**

* [Cursor MCP Documentation](https://cursor.com/docs/context/mcp)
* [GitHub Issue #3734](https://github.com/cursor/cursor/issues/3734)
* [Forum: Missing Refresh Token Logic](https://forum.cursor.com/t/missing-refresh-token-logic-for-mcp-oauth/130765)

---

### 3. Continue.dev

**Transport Support:** STDIO (primary), HTTP/SSE (experimental)
**Auth Methods:**

* ✅ **Secrets Interpolation:** `${{ secrets.TOKEN }}` syntax in YAML config
* ✅ **Environment Variables:** Standard `env` block
* ❌ **OAuth:** [Requested](https://github.com/continuedev/continue/issues/6282) but **not implemented** (as of Dec 2025)

**Configuration Pattern (`.continue/mcpServers/*.yaml`):**

```yaml
mcpServers:
  - name: GitHub
    command: npx
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: ${{ secrets.GITHUB_PERSONAL_ACCESS_TOKEN }}

  - name: PDX Parks (HTTP)
    type: streamable-http
    url: "http://127.0.0.1:5173/mcp"
```

**Pain Points:**

* OAuth feature [Issue #6282](https://github.com/continuedev/continue/issues/6282) open since early 2025—no timeline
* "Adding auth to hosted servers is a different beast" (community acknowledgment)
* Browser-redirect flow for token acquisition **not supported**
* HTTP transport marked "experimental"—limited production readiness

**Credential Storage:** Workspace `.continue/secrets` (plaintext risk if not gitignored)
**Best Practice:** Use Continue's secrets manager (stores in VSCode's SecretStorage API)

**Sources:**

* [Continue.dev MCP Setup](https://docs.continue.dev/customize/deep-dives/mcp)
* [GitHub Issue #6282](https://github.com/continuedev/continue/issues/6282)

---

### 4. Zed Editor

**Transport Support:** STDIO (mature), HTTP (limited/outdated spec)
**Auth Methods:**

* ✅ **Environment Variables:** Implicit via OS process env
* ✅ **HTTP Headers:** `Authorization: Bearer <token>` in `settings.json`
* ❌ **OAuth Flow:** No interactive flow support
* ❌ **Modern Spec:** Doesn't support `2025-06-18` protocol version

**Configuration (`settings.json`):**

```json
{
  "context_servers": {
    "remote-mcp-server": {
      "url": "custom",
      "headers": { "Authorization": "Bearer <token>" }
    }
  }
}
```

**Pain Points:**

* **Spec Lag:** Community notes Zed lacks streamable HTTP + auth from newer spec versions
* **No SDK Migration:** Still using custom implementation vs. official Rust MCP SDK (causes compatibility drift)
* **Static Tokens Only:** No OAuth refresh, device flow, or dynamic client registration
* Manual token rotation required

**Credential Storage:** Plaintext in `settings.json`
**Workaround:** Use environment variable references if Zed adds interpolation support

**Sources:**

* [Zed MCP Documentation](https://zed.dev/docs/ai/mcp)
* [GitHub Discussion #29370](https://github.com/zed-industries/zed/discussions/29370)

---

### 5. VS Code (Official MCP Extensions)

**Transport Support:** STDIO, HTTP (SSE/streamable)
**Auth Methods:**

* ✅ **Input Prompts:** `promptString` with `password: true` flag (SecretStorage API)
* ✅ **Environment Variables:** Standard `env` block
* ✅ **OAuth 2.0/2.1:** Full support (GitHub, Microsoft Entra built-in)
* ✅ **Custom IdPs:** OAuth delegation to external providers
* ✅ **Dynamic Client Registration:** Supported

**Configuration with Secure Prompts:**

```json
{
  "inputs": [
    {
      "type": "promptString",
      "id": "my-api-key",
      "description": "API Key for MyService",
      "password": true
    }
  ],
  "servers": {
    "my-mcp-server": {
      "type": "http",
      "url": "https://api.example.com",
      "headers": { "API_Key": "${input:my-api-key}" }
    }
  }
}
```

**HTTP Server Definition (Extension API):**

```javascript
new vscode.McpHttpServerDefinition({
  label: 'myRemoteServer',
  uri: 'http://localhost:3000',
  headers: { 'API_VERSION': '1.0.0' },
  version: '1.0.0'
});
```

**OAuth Flow (June 2025 Spec):**

1. VS Code connects → HTTP 401 + `WWW-Authenticate` header with `resource_metadata`
2. Client reads Protected Resource Metadata (PRM) document
3. Extracts Authorization Server info → initiates OAuth flow
4. Token audience validation via RFC 8707 resource indicators

**Strengths:**

* **Best-in-class credential UX:** Prompts stored in VSCode SecretStorage (OS keychain-backed)
* **Full spec compliance:** Implements 2025-06-18 auth spec completely
* **Enterprise-ready:** Built-in support for Microsoft Entra ID, GitHub OAuth

**Pain Points:**

* Complex config for multi-server setups
* Debugging auth failures requires log inspection (`Output` panel)

**Sources:**

* [VS Code MCP Developer Guide](https://code.visualstudio.com/api/extension-guides/ai/mcp)
* [Full MCP Spec Support Blog](https://code.visualstudio.com/blogs/2025/06/12/full-mcp-spec-support)

---

### 6. Cline (VSCode Extension)

**Transport Support:** STDIO, SSE, Streamable HTTP
**Auth Methods:**

* ✅ **Environment Variables:** Standard `env` block
* ✅ **HTTP Headers:** Bearer tokens for SSE/HTTP
* ⚠️ **Naming Convention Divergence:** Uses `streamableHttp` (camelCase) vs. spec's `http`

**Configuration (`cline_mcp_settings.json`):**

```json
{
  "mcpServers": {
    "local-server": {
      "command": "node",
      "args": ["/path/to/server.js"],
      "env": { "API_KEY": "your_key" },
      "alwaysAllow": ["tool1"],
      "disabled": false
    },
    "remote-server": {
      "type": "streamableHttp",  // Non-standard naming
      "url": "https://mcp.example.com",
      "headers": { "Authorization": "Bearer token" },
      "timeout": 60
    }
  }
}
```

**Pain Points:**

* **Type Field Inconsistency:** [Issue #7108](https://github.com/cline/cline/issues/7108)—Cline uses `streamableHttp` while VS Code expects `http`
* No OAuth flow support (static tokens only)
* Permission errors if API keys misconfigured

**Sources:**

* [Cline MCP Configuration](https://docs.cline.bot/mcp/configuring-mcp-servers)
* [GitHub Issue #7108](https://github.com/cline/cline/issues/7108)

---

### 7. Windsurf IDE (Codeium)

**Transport Support:** STDIO, HTTP
**Auth Methods:**

* ✅ **OAuth Authentication:** Built-in flows for managed servers (e.g., Neon Postgres)
* ✅ **Environment Variables:** Standard support
* ✅ **Streamable HTTP:** Recent Wave 3 update added support
* ✅ **SSO (Enterprise):** SAML-based (Okta, Azure AD, Google)

**Configuration (`~/.codeium/windsurf/mcp_config.json`):**

```json
{
  "mcpServers": {
    "neon-postgres": {
      "type": "http",
      "url": "https://mcp.neon.tech",
      "oauth": true  // Triggers interactive OAuth flow
    }
  }
}
```

**Recent Improvements (Wave 3 Update):**

* Fixed OAuth authentication flows for multiple MCP servers
* Improved scope handling
* Replaced SSE → Streamable HTTP transport
* Moved away from hardcoded API keys → OAuth

**Enterprise Features:**

* **Team Admin Controls:** Whitelist approved MCP servers
* **SSO Integration:** SAML providers (Okta, Azure AD, Google)
* **Centralized Governance:** MCP gateway with unified auth, audit logging, rate control

**Pain Points:**

* Earlier versions required hardcoded API keys in `mcp_config.json` (security risk)
* No built-in environment variable expansion (must use system env)

**Sources:**

* [Windsurf MCP Integration](https://docs.windsurf.com/windsurf/cascade/mcp)
* [Windsurf Wave 3 Update](https://substack.com/home/post/p-157302145)

---

### 8. CLI Tools (mcp-cli, mcptools, cli-mcp)

#### **mcp-cli (chrishayuk)**

**Auth Methods:**

* ✅ **OS Keychain Storage:** macOS Keychain, Windows Credential Manager, Linux Secret Service
* ✅ **Token Commands:** `mcp-cli token set brave_search --type bearer`
* ✅ **OAuth 2.0:** PKCE + resource indicators (RFC 7636, RFC 8707)
* ✅ **HashiCorp Vault:** Optional backend
* ✅ **Encrypted Files:** Alternative to keychain

**Token Management:**

```bash
# Bearer token
mcp-cli token set brave_search --type bearer

# OAuth flow
mcp-cli token set notion --oauth
```

**Security Features:**

* Tokens stored under `mcp-cli` service identifier in OS credential store
* Filesystem access can be disabled: `--disable-filesystem`
* Multiple storage backends (keychain, vault, encrypted files)

#### **mcptools (f/mcptools)**

**Auth Methods:**

* ⚠️ **Roadmap Feature:** Authentication support listed but not yet implemented
* ✅ **Server Logs:** `--server-logs` flag for debugging auth issues

**Current Limitations:**

* No built-in token storage
* No OAuth support
* Primarily for MCP server inspection/testing

#### **cli-mcp (zueai)**

**Auth Methods:**

* ✅ **Header Flags:** `--header "x-api-key: YOUR_KEY"`
* ✅ **Bearer Token:** `--bearer "your-token"`
* ✅ **Config-Based Auth:** `Authorization: Bearer` in config file

**Usage Examples:**

```bash
# Custom header
cli-mcp --url https://api.example.com --header "x-ref-api-key: KEY123"

# Bearer token
cli-mcp --url https://api.example.com --bearer "eyJ0eXAi..."
```

**Sources:**

* [mcp-cli GitHub](https://github.com/chrishayuk/mcp-cli)
* [mcptools GitHub](https://github.com/f/mcptools)
* [cli-mcp LobeHub](https://lobehub.com/mcp/zueai-cli-mcp)

---

## Cross-Client Authentication Capabilities Summary

| Client | ENV Vars | OAuth 2.0/2.1 | Token Refresh | Secure Storage | Custom Headers | Spec Compliance |
|--------|----------|---------------|---------------|----------------|----------------|-----------------|
| **Claude Desktop** | ✅ | ✅ (limited) | ⚠️ (implicit) | ❌ (plaintext) | ✅ | High (STDIO) |
| **Cursor** | ✅ | ⚠️ (broken) | ❌ (bug) | ❌ (plaintext) | ✅ | Medium (bugs) |
| **Continue.dev** | ✅ | ❌ (planned) | ❌ | ⚠️ (workspace) | ✅ | Medium (no OAuth) |
| **Zed** | ✅ | ❌ | ❌ | ❌ (plaintext) | ✅ | Low (spec lag) |
| **VS Code** | ✅ | ✅ (full) | ✅ | ✅ (SecretStorage) | ✅ | **Highest** |
| **Cline** | ✅ | ❌ | ❌ | ❌ (plaintext) | ✅ | Medium (naming issues) |
| **Windsurf** | ✅ | ✅ | ⚠️ (improved) | ⚠️ (SSO option) | ✅ | High (recent updates) |
| **mcp-cli** | ✅ | ✅ (PKCE) | ✅ | ✅ (keychain) | ✅ | **Highest** (CLI) |
| **mcptools** | ✅ | ❌ (roadmap) | ❌ | ❌ | ❌ | Low (dev tool) |
| **cli-mcp** | ✅ | ❌ | ❌ | ❌ | ✅ | Medium (basic) |

**Legend:**

* ✅ = Fully supported
* ⚠️ = Partial/buggy support
* ❌ = Not supported

---

## Environment Variable Naming Conventions

### De Facto Standards (observed across ecosystem):

* **Service-Specific Keys:** `<SERVICE>_API_KEY` (e.g., `GITHUB_PERSONAL_ACCESS_TOKEN`, `SUPABASE_TOKEN`)
* **Generic MCP Key:** `MCP_API_KEY` (LiteLLM pattern)
* **Bearer Tokens:** `<SERVICE>_BEARER_TOKEN` or `AUTH_TOKEN`
* **OAuth Credentials:** `<SERVICE>_CLIENT_ID`, `<SERVICE>_CLIENT_SECRET`

### Header Injection Patterns:

* **API Key Header:** `X-API-Key: ${API_KEY}` or `API_Key: ${API_KEY}`
* **Bearer Token:** `Authorization: Bearer ${TOKEN}`
* **Basic Auth:** `Authorization: Basic ${BASE64_CREDENTIALS}`
* **Custom:** Any `<HeaderName>: ${ENV_VAR}` pattern

### Best Practices (per ecosystem):

* **Claude Code:** `${VAR:-default}` expansion syntax
* **Continue.dev:** `${{ secrets.VAR }}` interpolation
* **VS Code:** `${input:VAR}` for prompted secrets
* **LibreChat:** `"${SOME_API_KEY}"` (JSON string interpolation)

---

## OAuth Flow Support Analysis

### Clients with Full OAuth 2.1 Implementation:

1. **VS Code** (official extensions)
   * ✅ Dynamic Client Registration (RFC 7591)
   * ✅ PKCE (RFC 7636)
   * ✅ Resource Indicators (RFC 8707)
   * ✅ Token refresh with rotation
   * ✅ Built-in IdP support (GitHub, Microsoft Entra)

2. **mcp-cli**
   * ✅ PKCE for public clients
   * ✅ Device flow for headless environments
   * ✅ Resource indicators
   * ✅ Secure token storage (OS keychain)

3. **Windsurf** (post-Wave 3)
   * ✅ Interactive OAuth flows
   * ✅ SSO/SAML for enterprise
   * ✅ Managed server OAuth (e.g., Neon)

### Clients with Broken/Incomplete OAuth:

1. **Cursor**
   * ❌ Dynamic client registration bug ([#3734](https://github.com/cursor/cursor/issues/3734))
   * ❌ No token refresh logic
   * ❌ Manual re-auth required on expiry

2. **Claude Desktop**
   * ⚠️ OAuth supported for remote servers but limited documentation
   * ❌ No interactive browser flow for STDIO servers
   * ❌ Token refresh handled opaquely (SDK-dependent)

### Clients with No OAuth Support:

* **Continue.dev:** Feature requested ([#6282](https://github.com/continuedev/continue/issues/6282)), not implemented
* **Zed:** Static tokens only; no OAuth flows
* **Cline:** HTTP bearer tokens only; no OAuth
* **mcptools:** No auth beyond basic headers (development tool)

---

## Token Refresh & Expiration Handling

### Spec Requirements (RFC 6749 + MCP 2025-06-18):

* Servers **MUST** return HTTP 401 on expired/invalid tokens
* Clients **SHOULD** use refresh tokens to obtain new access tokens
* Token lifetimes **SHOULD** be limited (recommended: 1 hour access, 90 days refresh)
* Clock skew tolerance: ±5 minutes

### Client Implementations:

| Client | Access Token Refresh | Refresh Token Rotation | Proactive Refresh | Error Handling |
|--------|---------------------|----------------------|-------------------|----------------|
| **VS Code** | ✅ Automatic | ✅ Supported | ✅ Buffer window | ✅ 401 → re-auth |
| **mcp-cli** | ✅ Automatic | ✅ Supported | ✅ (3600s buffer) | ✅ Device flow fallback |
| **Cursor** | ❌ Manual | ❌ None | ❌ | ⚠️ Marks "Logged out" |
| **Windsurf** | ⚠️ Improved | ⚠️ Partial | ⚠️ | ⚠️ OAuth re-trigger |
| **Others** | ❌ None | ❌ None | ❌ | ⚠️ Manual token update |

### Known Issues:

* **Cursor Bug:** Token expiry → 401 → server marked "Logged out" → user must manually re-authenticate (no automatic refresh)
* **Atlassian MCP Server:** Issues only short-lived OAuth tokens with no refresh capability in preview
* **ContextVar Immutability:** Some Python implementations fail to update auth context after `exchange_refresh_token()` due to immutable ContextVar design

### Best Practice Implementations:

1. **MCP Gateway Registry:** Automated refresh service with 3600s buffer (configurable via `--buffer`)
2. **LiteLLM:** OAuth 2.0 Client Credentials flow with automatic token exchange using `client_id`/`client_secret` from env
3. **Spring AI:** Implements OAuth 2.0 with PKCE + token refresh per 2025-03-26 spec

---

## Secure Credential Storage: Current State & Vulnerabilities

### Critical Security Issue (Trail of Bits, April 2025):

> "Many MCP environments store long-term API keys for third-party services in **plaintext on the local filesystem**, often with **insecure, world-readable permissions**."

**Affected Systems:**

* Official MCP servers: GitLab, Postgres, Google Maps
* Third-party tools: Figma connector, Superargs wrapper
* Most STDIO-based configurations using `env: { API_KEY: "..." }` in JSON configs

### Recommended Credential Storage Hierarchy:

1. **Tier 1 (Best):** OAuth with short-lived tokens (15–60 min)
2. **Tier 2 (Good):** OS keychain/vault (macOS Keychain, Windows DPAPI, Linux Secret Service)
3. **Tier 3 (Acceptable):** Encrypted vault (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault)
4. **Tier 4 (Last Resort):** Environment variables (system-level, not committed to version control)
5. **Tier 5 (Unacceptable):** Plaintext in config files ❌

### Client Storage Mechanisms:

| Client | Primary Storage | Security Rating | Notes |
|--------|----------------|-----------------|-------|
| **mcp-cli** | OS keychain | ⭐⭐⭐⭐⭐ | macOS Keychain, Windows Credential Manager, Linux Secret Service |
| **VS Code** | SecretStorage API | ⭐⭐⭐⭐⭐ | OS keychain-backed |
| **Claude Desktop** | Plaintext JSON | ⭐ | `claude_desktop_config.json` world-readable |
| **Cursor** | Plaintext JSON | ⭐ | No encryption |
| **Continue.dev** | Workspace secrets | ⭐⭐ | Risk if `.continue/secrets` committed |
| **Zed** | Plaintext JSON | ⭐ | `settings.json` |
| **Cline** | Plaintext JSON | ⭐ | `cline_mcp_settings.json` |
| **Windsurf** | Plaintext JSON | ⭐⭐ | Enterprise SSO improves this |

### Best Practices (per [WorkOS](https://workos.com/guide/best-practices-for-mcp-secrets-management), [Infisical](https://infisical.com/blog/managing-secrets-mcp-servers)):

1. **Never hardcode secrets in config files**
2. **Use system vaults:** macOS Keychain, Windows DPAPI, HashiCorp Vault
3. **Inject secrets at runtime:** CLI tools to pass env vars on-the-fly
4. **Implement least privilege:** Fine-grained RBAC, avoid root tokens
5. **Enable TLS/mTLS:** Encrypt secrets in transit
6. **Rotate credentials aggressively:** Minutes/hours for sensitive systems, not days
7. **Audit logging:** Track credential retrieval and usage
8. **Wrapper scripts:** Parse config → retrieve from vault → inject as env vars

### HashiCorp Vault MCP Server Recommendations:

* Run MCP server locally (127.0.0.1) via STDIO to limit exposure
* **Do not use root or shared `VAULT_TOKEN`**
* Create per-user tokens with least-privilege policies
* Enable mTLS between MCP server and Vault backend

---

## Pain Points & Community Complaints (2025)

### 1. **Spec-Implementation Gap**

**Problem:** MCP spec evolved rapidly (March → June → November 2025 updates), but most clients lag behind.

**Evidence:**

* Zed doesn't support `2025-06-18` protocol version
* Cursor OAuth broken despite being "only MCP-native auth protocol"
* Continue.dev lacks OAuth entirely ([Issue #6282](https://github.com/continuedev/continue/issues/6282) open 10+ months)

**Community Sentiment:** "MCP's spec is still evolving. That means much of what's available today is either incomplete, inconsistently implemented, or poorly documented." ([FeatureForm](https://www.featureform.com/post/what-mcp-gets-wrong))

### 2. **Enterprise Adoption Blockers**

**Problem:** Original MCP spec (pre-March 2025) had **zero authentication**, forcing servers to act as OAuth Identity Providers—an unrealistic burden.

**Quotes:**

* "Every server that wants to support authentication is required to operate as a fully-fledged Identity Provider (IdP)." ([ceposta](https://blog.christianposta.com/the-updated-mcp-oauth-spec-is-a-mess/))
* "This requires that the MCP server is now stateful, and has access to all secure tokens. This requires a secure DB, which is an additional piece of infrastructure with high security demands." ([Solo.io](https://www.solo.io/blog/part-two-mcp-authorization-the-hard-way))

**Impact:** Organizations cannot deploy MCP servers remotely without building full OAuth infrastructure.

### 3. **Plaintext Credential Plague**

**Problem:** Most clients store API keys in plaintext JSON configs (world-readable on many systems).

**Security Risks:**

* API key leakage via version control commits
* Filesystem access attacks (malware, insider threats)
* Logs exposing credentials (session IDs in URLs per spec, header leaks)

**Mitigation Status:**

* ✅ **mcp-cli, VS Code:** Use OS keychains
* ❌ **All others:** Plaintext JSON (requires manual wrapper scripts)

**Trail of Bits (April 2025):** "Insecure credential storage plagues MCP... observed in multiple MCP tools, from official servers to third-party connectors."

### 4. **Cursor OAuth Catastrophe**

**Problem:** Cursor's OAuth implementation violates RFC specs and breaks on token expiry.

**Specific Bugs:**

* [#3734](https://github.com/cursor/cursor/issues/3734): Sends `Authorization: Basic` despite declaring `token_endpoint_auth_method: "none"` (spec violation)
* Token refresh missing → access token expires → 401 → server marked "Logged out" → manual re-auth loop

**Community Impact:** "We need Cursor to support OAuth flow for remote MCP servers" ([Forum 91719](https://forum.cursor.com/t/we-need-cursor-to-support-oauth-flow-for-remote-mcp-servers/91719)) - high-upvote request unresolved

### 5. **STDIO vs. HTTP Auth Confusion**

**Problem:** Spec says "STDIO SHOULD NOT use OAuth" but doesn't explain why—leads to developers attempting OAuth over STDIO.

**Root Cause:** Different threat models not clearly communicated:

* STDIO = local process isolation (env vars sufficient)
* HTTP = network exposure (OAuth mandatory)

**Clarification Needed:** Better documentation on **when** to use each transport + auth method.

### 6. **No Standardized Credential Injection**

**Problem:** Each client uses different syntax for secrets:

* Claude Code: `${VAR:-default}`
* Continue.dev: `${{ secrets.VAR }}`
* VS Code: `${input:VAR}`
* LibreChat: `"${VAR}"`

**Impact:** Configuration portability between clients is broken—teams must maintain separate configs per tool.

### 7. **Token Refresh Reliability**

**Problem:** Only 2 clients (VS Code, mcp-cli) implement automatic token refresh correctly.

**Consequences:**

* Long-running AI agents lose access mid-task (Cursor)
* Users must manually re-authenticate during workflows
* Production deployments unstable without refresh token rotation

**Atlassian Example:** MCP server only issues short-lived tokens with no refresh capability in preview—Claude Code can't refresh automatically.

---

## Workarounds & Mitigation Strategies

### For Plaintext Storage Issue:

1. **Wrapper Scripts:** Parse config → retrieve from OS keychain → inject env vars

   ```bash
   #!/bin/bash
   API_KEY=$(security find-generic-password -s "mcp-server" -w)
   export API_KEY
   node /path/to/mcp-server.js
   ```

2. **System Vault Integration:**
   * **macOS:** `security` CLI for Keychain access
   * **Linux:** `secret-tool` (GNOME Keyring) or `kwallet-query` (KDE)
   * **Windows:** PowerShell `Get-Credential` + DPAPI

3. **Infisical/Vault Integration:** Use MCP servers with built-in Vault support (HashiCorp Vault MCP server, AWS Secrets Manager)

### For Cursor OAuth Bugs:

**Short-Term:** Use static Bearer tokens with long expiry (security trade-off)

```json
{
  "mcpServers": {
    "api": {
      "type": "http",
      "url": "https://api.example.com",
      "headers": { "Authorization": "Bearer <long-lived-token>" }
    }
  }
}
```

**Long-Term:** Migrate to VS Code or Windsurf for production OAuth flows

### For Continue.dev OAuth Absence:

**Workaround:** Deploy MCP servers with static API keys in STDIO mode:

```yaml
mcpServers:
  - name: MyService
    command: npx
    args: ["-y", "@my-org/mcp-server"]
    env:
      API_KEY: ${{ secrets.API_KEY }}
```

**Alternative:** Use MCP gateway with OAuth termination (e.g., [Gopher MCP](https://www.gopher.security/))

### For Spec Lag (Zed):

**Workaround:** Run MCP servers in "compatibility mode" using older protocol versions:

```json
{
  "context_servers": {
    "legacy-server": {
      "command": "node",
      "args": ["server.js", "--protocol-version", "2024-11-05"]
    }
  }
}
```

### For Enterprise Deployments:

**Recommendation:** Use MCP gateways/proxies with centralized auth:

* **MCP Gateway Registry:** Unified authentication, audit logging, rate limiting
* **Gopher MCP:** Enterprise security, on-demand MCP servers with OAuth
* **Spring AI MCP:** OAuth 2.0 with PKCE built-in

---

## Recommendations by Use Case

### For Solo Developers (Local Development):

* **Best Client:** Claude Desktop or Continue.dev
* **Auth Method:** Environment variables via OS keychain wrapper
* **Storage:** `~/.zshrc` or `~/.bashrc` exports (not committed to Git)
* **Risk Level:** Low (local-only, no network exposure)

### For Teams (Shared Infrastructure):

* **Best Client:** VS Code with official MCP extensions
* **Auth Method:** OAuth 2.0 with organization IdP (GitHub, Okta, Azure AD)
* **Storage:** VS Code SecretStorage API (synced via Settings Sync)
* **Risk Level:** Medium (requires IdP setup)

### For Enterprises (Multi-Tenant, Compliance):

* **Best Client:** Windsurf (SSO) or VS Code (Microsoft Entra)
* **Auth Method:** SAML SSO + MCP gateway with OAuth termination
* **Storage:** HashiCorp Vault or AWS Secrets Manager
* **Risk Level:** High (requires full security stack: mTLS, audit logging, RBAC)

### For CLI/Automation:

* **Best Tool:** mcp-cli (OS keychain storage, PKCE support)
* **Auth Method:** Device flow for headless environments, Bearer tokens for CI/CD
* **Storage:** OS keychain + CI secret managers (GitHub Secrets, GitLab CI/CD variables)
* **Risk Level:** High (token leakage in logs, environment exposure)

### For Public-Facing AI Agents:

* **Best Architecture:** MCP gateway (e.g., Gopher MCP) with OAuth 2.1
* **Auth Method:** Resource indicators (RFC 8807) + short-lived tokens (15–60 min)
* **Storage:** Ephemeral tokens only, no long-term credential storage
* **Risk Level:** Critical (network-exposed, requires full OAuth + TLS + rate limiting)

---

## Future Outlook & Spec Evolution

### Completed (2025 Spec Updates):

* ✅ OAuth 2.1 standardization (March 2025)
* ✅ Resource indicators (RFC 8807) for audience validation (June 2025)
* ✅ Secure credential collection (November 2025)
* ✅ External OAuth flows (URL mode elicitation)
* ✅ Payment processing capabilities

### Remaining Gaps (Community Requests):

* **Token Refresh Standardization:** Mandatory refresh logic in client spec
* **Credential Storage Spec:** Formal guidance on OS keychain integration
* **STDIO Auth Clarification:** Explicit documentation on env var best practices vs. OAuth
* **Multi-Tenancy Patterns:** Guidance for shared MCP server deployments
* **Rate Limiting Spec:** Standard approach for token bucket, concurrent requests

### Client Roadmaps (Inferred from Issues/Forums):

* **Cursor:** OAuth refresh logic fix (Issue #130765) - no ETA
* **Continue.dev:** OAuth support (Issue #6282) - no timeline
* **Zed:** Migrate to official Rust SDK (community PR in progress)
* **Cline:** Align type field naming with spec (Issue #7108)

---

## References & Sources

### Official Specifications:

* [MCP Authorization Spec (2025-03-26)](https://modelcontextprotocol.io/specification/2025-03-26/basic/authorization)
* [MCP Spec Update (June 2025)](https://auth0.com/blog/mcp-specs-update-all-about-auth/)
* [MCP First Anniversary (November 2025)](https://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/)

### Security Analyses:

* [Trail of Bits: Insecure Credential Storage in MCP](https://blog.trailofbits.com/2025/04/30/insecure-credential-storage-plagues-mcp/)
* [Microsoft: Security Risks in MCP Implementations](https://techcommunity.microsoft.com/blog/microsoft-security-blog/understanding-and-mitigating-security-risks-in-mcp-implementations/4404667)
* [Equixly: MCP Servers - The New Security Nightmare](https://equixly.com/blog/2025/03/29/mcp-server-new-security-nightmare/)

### Implementation Guides:

* [Auth0: Introduction to MCP and Authorization](https://auth0.com/blog/an-introduction-to-mcp-and-authorization/)
* [Stytch: MCP Authentication and Authorization Guide](https://stytch.com/blog/MCP-authentication-and-authorization-guide/)
* [WorkOS: Best Practices for MCP Secrets Management](https://workos.com/guide/best-practices-for-mcp-secrets-management)
* [Infisical: Managing Secrets in MCP Servers](https://infisical.com/blog/managing-secrets-mcp-servers)

### Client Documentation:

* [Claude Code MCP Setup](https://code.claude.com/docs/en/mcp)
* [Cursor MCP Documentation](https://cursor.com/docs/context/mcp)
* [Continue.dev MCP Deep Dive](https://docs.continue.dev/customize/deep-dives/mcp)
* [Zed MCP Documentation](https://zed.dev/docs/ai/mcp)
* [VS Code MCP Developer Guide](https://code.visualstudio.com/api/extension-guides/ai/mcp)
* [Windsurf MCP Integration](https://docs.windsurf.com/windsurf/cascade/mcp)
* [Cline MCP Configuration](https://docs.cline.bot/mcp/configuring-mcp-servers)

### Community Resources:

* [Aaron Parecki: Let's Fix OAuth in MCP](https://aaronparecki.com/2025/04/03/15/oauth-for-model-context-protocol)
* [Christian Posta: MCP Authorization Spec Is a Mess for Enterprise](https://blog.christianposta.com/the-updated-mcp-oauth-spec-is-a-mess/)
* [FeatureForm: What MCP Gets Wrong](https://www.featureform.com/post/what-mcp-gets-wrong)
* [Everything Wrong with MCP (Shrivu Shankar)](https://blog.sshh.io/p/everything-wrong-with-mcp)

### GitHub Issues:

* [Claude Code #1254: ENV vars not passed to MCP servers](https://github.com/anthropics/claude-code/issues/1254)
* [Cursor #3734: OAuth flow broken](https://github.com/cursor/cursor/issues/3734)
* [Cursor Forum: Missing Refresh Token Logic](https://forum.cursor.com/t/missing-refresh-token-logic-for-mcp-oauth/130765)
* [Continue.dev #6282: Implement MCP OAuth](https://github.com/continuedev/continue/issues/6282)
* [Zed #29370: Support 2025-03-26 MCP spec](https://github.com/zed-industries/zed/discussions/29370)
* [Cline #7108: Type field naming inconsistency](https://github.com/cline/cline/issues/7108)

---

## Appendix: Quick Reference Tables

### Environment Variable Patterns by Service:

| Service | ENV Variable Name | Header Pattern |
|---------|------------------|----------------|
| GitHub | `GITHUB_PERSONAL_ACCESS_TOKEN` | `Authorization: Bearer ${TOKEN}` |
| GitLab | `GITLAB_API_TOKEN` | `Private-Token: ${TOKEN}` |
| Supabase | `SUPABASE_TOKEN` | `Authorization: Bearer ${TOKEN}` |
| Brave Search | `BRAVE_API_KEY` | `X-Subscription-Token: ${KEY}` |
| Google Maps | `GOOGLE_MAPS_API_KEY` | `key=${KEY}` (query param) |
| Neon Postgres | OAuth flow | N/A (interactive) |
| Generic MCP | `MCP_API_KEY` | `X-API-Key: ${KEY}` |

### OAuth Grant Types by Use Case:

| Use Case | Grant Type | Flow | Best For |
|----------|-----------|------|----------|
| User-authorized access | Authorization Code | Browser redirect → code → token | SaaS integrations, user data access |
| Machine-to-machine | Client Credentials | Direct token request | Automation, CI/CD, server-to-server |
| Device/CLI auth | Device Flow | Device code → polling → token | Headless environments, smart TVs |
| Token renewal | Refresh Token | Refresh token → new access token | Long-running agents, session maintenance |

### Security Tier Recommendations:

| Data Sensitivity | Minimum Tier | Recommended Storage | Rotation Interval |
|-----------------|-------------|---------------------|-------------------|
| Public APIs (read-only) | Tier 4 | Environment variables | 90 days |
| Internal tools | Tier 3 | Encrypted vault | 30 days |
| User data access | Tier 2 | OS keychain + OAuth | 7 days (access), 90 days (refresh) |
| Financial/PII | Tier 1 | OAuth only (15–60 min tokens) | Continuous (auto-refresh) |
| Compliance (SOC 2, HIPAA) | Tier 1 | OAuth + mTLS + audit logs | Real-time rotation |

---

**Document Metadata:**

* **Author:** AI Research Assistant (Claude Sonnet 4.5)
* **Research Date:** 2025-12-22
* **Sources:** 40+ documentation pages, GitHub issues, security analyses
* **Word Count:** ~8,500
* **Last Updated:** 2025-12-22
