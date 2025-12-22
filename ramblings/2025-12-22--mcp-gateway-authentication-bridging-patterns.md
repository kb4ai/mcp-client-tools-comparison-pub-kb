# MCP Gateway Authentication Bridging: Technical Patterns & Implementation

## Executive Summary

**Core Problem:** MCP servers expose tools to AI agents but lack uniform authentication, especially for stdio-based servers. Gateways bridge this gap by adding OAuth/JWT auth to unauthenticated backends, transforming tokens, managing sessions, and enforcing zero-trust policies.

**Key Insight:** Gateway-based authorization is the emergent enterprise pattern—centralizing policy, transforming tokens into narrowly-scoped credentials, creating audit boundaries, and enabling sequence-aware authorization beyond per-request validation.

**Critical Standards:**

* OAuth 2.1 (RFC 8693 token exchange, RFC 7591 dynamic client registration, RFC 9728 protected resource metadata)
* PKCE mandatory (S256 challenge method)
* JWT validation via JWKS endpoints with 24h cache
* WWW-Authenticate headers for 401 responses with resource_metadata parameter

---

## 1. Gateway Architecture Patterns

### 1.1 Microsoft mcp-gateway (Kubernetes-Native)

**Architecture:** Envoy-based reverse proxy with session-aware stateful routing.

**Session Management:**

* `session_id` parameter ensures consistent routing to same MCP server instance
* Distributed session store for production multi-instance deployments
* Preserves conversational state across multiple requests

**Dual-Plane Authentication:**

* **Data Plane:** Bearer token validation for `/adapters/{name}/mcp` and `/mcp` endpoints
* **Control Plane:** Token validation for management APIs (`/adapters`, `/tools` CRUD)

**Entra ID Integration:**

* App registration with application roles: `mcp.admin` (write), `mcp.engineer` (read)
* Role claims extracted from tokens during validation
* Read access: resource creator + assigned roles + `mcp.admin`
* Write access: resource creator OR `mcp.admin`

**Backend Bridge:**

* Gateway validates client tokens (Entra ID) before routing
* No credential forwarding to backend servers documented
* Gateway acts as authentication termination point

**Deployment:** Requires Entra ID client ID parameter, uses Managed Identity for credential-less authentication.

---

### 1.2 Lasso Security mcp-gateway (Security-Centric)

**Architecture:** Plugin-based gateway with interceptors for request/response sanitization.

**Security Plugins:**

* **Basic:** Token masking (Azure secrets, GitHub tokens, AWS keys, JWT, etc.)
* **Presidio:** PII detection (credit cards, emails, SSNs, phone numbers, IPs)
* **Lasso:** Comprehensive AI safety (prompt injection, data leakage detection)

**Audit Logging (Xetrack):**

* Structured logging to SQLite/DuckDB
* Tracked events: server name, capability, request/response content, timestamps, errors
* Configurable DB/log paths for compliance

**Security Scanner:**

* Pre-deployment analysis of MCP servers
* Reputation scoring via marketplace/GitHub data
* Automatic blocking below threshold (score: 30)
* Tool description scanning for hidden instructions, sensitive patterns, malicious actions

**Authentication:**

* Reads server configs from `mcp.json`/`claude_desktop_config.json`
* Passes environment variables (e.g., `LASSO_API_KEY`) to plugins
* No native auth mechanism—delegates to configured servers

**Monitoring:**

* Always-on monitoring of MCP interactions
* Real-time threat mitigation (prompt injection, sensitive data exposure)
* Integration with ELK, Prometheus, Grafana

---

### 1.3 Red Hat MCP Gateway (Envoy + Kuadrant)

**Architecture:** Envoy-based gateway with Kuadrant AuthPolicy for policy enforcement.

**Three Advanced Auth Capabilities:**

#### 1.3.1 Identity-Based Tool Filtering

* External authorization (Authorino) validates OAuth2 tokens
* Extracts permissions from IdP (Keycloak)
* Creates **signed JWT "wristband"** with permitted tools
* Injects as `x-authorized-tools` header
* MCP Broker validates JWT signature and filters tool list
* Permissions stored as Keycloak client roles (server = resource, tool = role)

**Data Flow:**

1. Gateway validates OAuth2 token
2. Authorino creates permission wristband (signed JWT)
3. Broker filters tools based on wristband contents
4. Router tags requests with `x-mcp-toolname` headers
5. AuthPolicy exchanges tokens or retrieves PATs from Vault

#### 1.3.2 OAuth2 Token Exchange (RFC 8693)

* Exchanges broad access tokens for narrowly-scoped alternatives
* Target server specified as audience parameter
* Prevents lateral movement (each backend gets server-specific token)
* Authorization verification ensures user has tool permissions

**Token Exchange Flow:**

1. Original token validation & extraction
2. Token exchange request to IdP with target audience
3. Issuance of restricted-scope token with specific audience claim
4. Backend receives credentials valid only for its purpose

#### 1.3.3 HashiCorp Vault Integration

* Retrieves PATs/API keys for OAuth-unsupported services (e.g., GitHub MCP)
* Query path: `username + target server hostname`
* Per-user, per-service credential management
* Fallback logic: Vault retrieval → OAuth2 token exchange

**AuthPolicy Configuration (Kuadrant):**

* JWT validation against IdP issuance endpoints
* OPA (Open Policy Agent) expressions for permission extraction
* HTTP calls to Vault or token exchange endpoints
* Header injection (wristbands, scoped tokens, retrieved credentials)

**Defense in Depth:** Gateway auth → tool-level authz → cryptographic verification → token scoping

---

### 1.4 sparfenyuk/mcp-proxy (Python Transport Bridge)

**Architecture:** stdio ↔ SSE transport bridge.

**Authentication Support:**

* `--api-access-token` flag: Authorization header to SSE server
* Environment variable: `API_ACCESS_TOKEN`
* Example: `mcp-proxy --api-access-token YOUR_TOKEN http://localhost:8080/sse`

**Enhanced Fork (secure-mcp-proxy):**

* `MCP_PROXY_API_TOKEN` environment variable
* Per-server authentication configuration
* Public endpoints when token unset

**Features:**

* v0.8.0+: Single instance proxies multiple STDIO servers
* Supports stdio→SSE and SSE→stdio modes

---

### 1.5 TBXark/mcp-proxy (Go Multi-Server Aggregator)

**Architecture:** Aggregates multiple MCP resource servers through single HTTP server.

**Auth Token Hierarchy:**

* **Proxy-level default:** `mcpProxy.options.authTokens`
* **Server-specific override:** `mcpServers.<server>.options.authTokens`
* Server-specific tokens take precedence

**Implementation (client.go):**

```go
if clientConfig.Options != nil && len(clientConfig.Options.AuthTokens) > 0 {
    srv.tokens = clientConfig.Options.AuthTokens
}
```

**Supported Transports:** stdio, SSE, streamable-HTTP

**Config Converter:** https://tbxark.github.io/mcp-proxy (converts proxy config → Claude config)

---

### 1.6 open-webui/mcpo (MCP-to-OpenAPI Proxy)

**Architecture:** MCP-to-OpenAPI proxy server with OAuth 2.1 support.

**OAuth 2.1 Features:**

* Full OAuth 2.0 support with dynamic client registration
* Defaults to dynamic client registration (minimal config needed)
* Streamable HTTP only (multi-tenant web constraints)

**Configuration:**

* `server_url`, `client_metadata` (client_name, redirect_uris)
* Avoid setting scope/endpoints—auto-discovered from server OAuth metadata
* Dynamic registration flow handles discovery

**Open WebUI Integration:**

* Streamable HTTP only (no stdio/SSE in browser sandbox)
* **CRITICAL:** `WEBUI_SECRET_KEY` required—tokens break on container restart without it
* Per-user authentication supported
* Native MCP support (June 2025 spec compliance)

**Auth Mechanisms:**

* OAuth 2.1 with PKCE
* Dynamic Client Registration (DCR)
* Custom header auth
* Mixed auth modes

**Multi-User Session Handling:**

* Each user authenticates individually
* Session-aware routing per user
* Token encryption requires persistent secret key

---

### 1.7 Apache APISIX mcp-bridge Plugin

**Architecture:** stdio → HTTP SSE bridge with API gateway integration.

**Transport Bridge:**

* Launches subprocess, takes over stdio channel
* Transforms HTTP SSE requests → MCP protocol calls
* Pushes responses back via SSE

**Authentication Integration:**

* OAuth 2.0, JWT, OIDC plugins
* Rate limiting plugins
* Traffic control integration

**Session Management Limitations:**

* Sessions NOT shared across APISIX instances (prototype)
* Requires sticky session on load balancer for multi-node clusters
* Future: session sharing, event-driven architecture

---

### 1.8 Supergateway (supercorp-ai)

**Architecture:** Bidirectional stdio ↔ SSE ↔ Streamable HTTP bridge.

**Auth Header Injection:**

* `--oauth2Bearer`: Adds `Authorization: Bearer <token>` header
* `--header`: Custom headers (repeatable flag)
* Example:
  ```bash
  npx -y supergateway \
    --sse "https://mcp-server.example.com" \
    --oauth2Bearer "some-access-token" \
    --header "X-My-Header: value"
  ```

**Transport Modes:**

* stdio→SSE: Exposes local servers remotely
* SSE→stdio: Wraps remote servers for local clients
* Streamable HTTP→stdio

**Header Preservation:** Headers preserved across transport conversions.

**Use Case:** Clients without custom header support use supergateway to inject auth headers, then present stdio to client.

---

### 1.9 ContextForge MCP Gateway (IBM)

**Architecture:** MCP-native proxy, registry, federation layer.

**Features:**

* Transport bridge: stdio ⇆ HTTP
* Single entry point for multiple FastMCP servers
* Auth + token management: Bearer tokens or OAuth providers
* Health checks, server discovery

**MCP Gateway Wrapper:**

* Re-publishes gateway tools over stdin/stdout
* Connects securely to gateway via SSE + JWT
* For clients unable to open SSE streams or attach JWT headers

---

### 1.10 Pomerium (Zero-Trust MCP)

**Architecture:** Zero-trust access proxy with identity-based authorization.

**Token Translation Layer:**

1. Validate external identity tokens (OAuth from IdP)
2. Issue short-lived, scoped JWTs per request context
3. Inject signed identity into request headers
4. Backend trusts Pomerium's signed identity (not raw tokens)

**Zero-Trust Evaluation:**

* User identity, role, time, geo-origin, action type, request path, session attributes, device posture
* Every request re-evaluated (no static credentials)

**Identity Assertion:**

* MCP servers receive authenticated user context via headers
* Request-specific authorization metadata
* Cryptographically signed claims

**Configuration:**

* Vanilla HTTP MCP: Direct policy enforcement
* Upstream OAuth2: External OAuth + Pomerium authz layer

**Benefit:** No raw tokens exposed to agents, no credential sprawl, full audit logging.

---

### 1.11 Cloudflare MCP Server Portals (Zero-Trust)

**Architecture:** Centralized gateway with Cloudflare Access integration.

**Authentication:**

* Cloudflare Access prompts corporate IdP auth on connection
* Access policies enforce server authorization
* OAuth server linked to domain's Access Application

**Zero-Trust Enforcement:**

* Multi-factor authentication
* Device posture checks
* Geographic restrictions
* Role-based server/tool access

**Visibility:**

* All MCP request logs aggregated centrally
* Comprehensive audit trails

**Least Privilege:** Admins curate servers before Portal exposure, users access only authorized servers/tools.

---

## 2. Authentication Bridging Patterns

### 2.1 OAuth for stdio Servers

**Specification:** MCP spec states stdio SHOULD NOT use OAuth—retrieve credentials from environment instead.

**Bridge Solutions:**

* **Supergateway:** Inject OAuth headers, expose as stdio
* **APISIX mcp-bridge:** Convert stdio→HTTP SSE, apply OAuth plugins
* **ContextForge Wrapper:** SSE + JWT to stdio conversion

**Pattern:** Gateway handles OAuth, presents credential-injected stdio to client.

---

### 2.2 Session-Based OAuth (Backend-for-Frontend)

**Pattern (Den Delimarsky):** MCP server acts as confidential OAuth client (not public client).

**Flow:**

1. Client requests authorization from MCP server
2. Server generates session ID, redirects to Entra ID
3. Entra ID returns auth code to server (not client)
4. Server exchanges code for access token, caches with session mapping
5. Client receives temporary auth code, exchanges for JWT session token
6. Subsequent requests include session JWT as bearer token

**Dual PKCE Validation:**

* Client provides code challenge/verifier for MCP server
* Server generates separate PKCE for Entra ID
* Both validated independently

**Security:** Access tokens remain server-side, clients receive session indicators.

**Future:** Clients support `WWW-Authenticate` header parsing for OIDC discovery, enabling autonomous browser-based flows.

---

### 2.3 Token Exchange (RFC 8693)

**Use Case:** Replace broad OAuth tokens with narrowly-scoped tokens per backend.

**Implementation:**

* Gateway validates incoming token
* Calls IdP token exchange endpoint with target audience (server hostname)
* IdP issues new token with restricted scope/audience
* Gateway forwards scoped token to backend

**Benefits:**

* Least privilege (each backend gets minimal access)
* Prevents lateral movement
* Standards-based (Keycloak, Auth0, Okta support)

**Delegation vs. Impersonation:**

* **Delegation:** Acting party distinguishable from user (preserves subject, audit trail)
* **Impersonation:** Acting party assumes user identity

**Note:** Few IdPs support delegated tokens (Keycloak does).

---

### 2.4 Vault Credential Retrieval

**Use Case:** Backends without OAuth support (GitHub PATs, API keys).

**Pattern:**

* Gateway queries Vault: `{username}/{target_hostname}`
* Retrieves per-user, per-service credentials
* Injects into request headers/environment
* Fallback: OAuth token exchange if Vault empty

**Benefits:**

* Centralized secret management
* Credential rotation without code changes
* Audit trails of credential access

---

### 2.5 Wristband Pattern (Cryptographic Tool Filtering)

**Pattern (Red Hat/Authorino):**

1. Authorino validates OAuth2 token
2. Extracts user permissions from IdP
3. Creates signed JWT "wristband" with permitted tools
4. Injects as `x-authorized-tools` header
5. Broker validates signature, filters tools

**Benefits:**

* Prevents unauthorized tool discovery
* Cryptographic verification (no DB lookups)
* Transparent to clients

---

## 3. OAuth 2.1 Flows for MCP

### 3.1 Authorization Code + PKCE (User-Scoped)

**When:** User-specific data access required.

**Flow:**

1. Client queries MCP server for protected resource metadata (`/.well-known/oauth-protected-resource`)
2. Registers via dynamic client registration (DCR) with authz server, obtains `client_id`
3. User invokes tool → client launches authorization code + PKCE flow
4. User authenticates & consents
5. Client exchanges auth code + PKCE verifier for access token
6. Token attached to subsequent MCP requests

**PKCE Requirements:**

* `code_challenge_methods_supported` MUST include `S256`
* Clients MUST refuse to proceed if PKCE unsupported
* Challenge on authorize, verifier on token exchange

**Resource Indicators (RFC 8707):**

* Tokens scoped per server (prevent reuse across servers)
* `resource` parameter specifies target MCP server in token request

**Security:**

* Never allow credentials into LLM context/prompts/traces
* Short token lifetimes (minutes/hours, not days)

---

### 3.2 Client Credentials (System-Scoped)

**When:** Non-user-dependent operations.

**Requirements:**

* Vault storage for secrets
* Regular rotation
* Least-privilege scoping per service/environment

---

### 3.3 Dynamic Client Registration (DCR, RFC 7591)

**Why:** Clients cannot know all MCP servers in advance—manual registration creates friction.

**Flow:**

1. Client POSTs metadata (redirect URIs, grant types) to registration endpoint (`/register`)
2. Authz server issues `client_id` (+ optional secret/registration token)

**Best Practices:**

* Rate-limit registration endpoints (prevent DoS)
* Apply policies for dynamic clients: enforce PKCE, set token lifetime, disable refresh tokens
* Lightweight bot/abuse detection

**Provider Support:** Auth0, Okta, ForgeRock, Keycloak, Cloudflare.

---

## 4. Discovery & Metadata Endpoints

### 4.1 Protected Resource Metadata (RFC 9728)

**Endpoint:** `/.well-known/oauth-protected-resource`

**Required Field:** `authorization_servers` (array of authz server URLs)

**Discovery Methods:**

* WWW-Authenticate header on 401/403 with `resource_metadata` parameter
* Fetching well-known URI

**MCP Requirement:** Servers MUST implement RFC 9728, clients MUST use it for authz server discovery.

---

### 4.2 Authorization Server Metadata

**Endpoints:**

* OAuth 2.0: `/.well-known/oauth-authorization-server` (RFC 8414)
* OpenID Connect: `/.well-known/openid-configuration`

**Required Fields:**

* `registration_endpoint` (for DCR)
* `code_challenge_methods_supported: ["S256"]` (PKCE)
* Standard endpoints: `authorization_endpoint`, `token_endpoint`, `jwks_uri`

**Client Behavior:** Fetch both endpoints (servers vary), extract required info.

---

### 4.3 WWW-Authenticate Header Pattern

**Trigger:** 401 Unauthorized or 403 Forbidden responses.

**Format:**

```http
WWW-Authenticate: Bearer realm="https://example.com", resource_metadata="https://example.com/.well-known/oauth-protected-resource"
```

**Client Flow:**

1. Attempt request without token
2. Receive 401 with WWW-Authenticate header
3. Parse `resource_metadata` URL
4. Fetch protected resource metadata
5. Extract authz server URL
6. Perform DCR + OAuth flow
7. Retry with access token

**Fallback:** If WWW-Authenticate parsing fails (CORS issues), default to `/.well-known/oauth-authorization-server`.

---

## 5. JWT Validation

### 5.1 JWKS Endpoint Integration

**Pattern:** Verifier fetches public keys from JSON Web Key Set endpoint, enables automatic key rotation.

**Implementation (FastMCP):**

```python
JWTVerifier(
    jwks_uri="https://your-tenant.auth0.com/.well-known/jwks.json",
    issuer="https://your-tenant.auth0.com/",
    audience="your-api-identifier"
)
```

**Traefik Hub:**

```yaml
jwksUrl: "https://your-tenant.auth0.com/.well-known/jwks.json"
```

**Validation Steps:**

1. Verify signature using JWKS public keys
2. Check issuer matches auth server
3. Verify audience/resource matches service
4. Ensure token not expired
5. Reject with 401/403 if any check fails

---

### 5.2 Token Caching

**Best Practice:** Cache JWKS public keys for 24 hours (reduce HTTP calls, instantaneous verification).

**Retry Mechanism (MuleSoft):**

* On JWKS fetch failure: asynchronous retries with exponential backoff
* Continue until new JWKS obtained and cached

---

### 5.3 Node.js Implementation (jose library)

```javascript
import { createRemoteJWKSet, jwtVerify } from 'jose';

const JWKS = createRemoteJWKSet(new URL('https://auth.example.com/.well-known/jwks.json'));

const { payload } = await jwtVerify(token, JWKS, {
  issuer: 'https://auth.example.com',
  audience: 'your-api'
});
```

**On Failure:** Return 401 with WWW-Authenticate headers pointing to OAuth protected resource metadata.

---

## 6. Rate Limiting & Multi-Tenancy

### 6.1 Rate Limiting Patterns

**Why:** AI agents invoke tools faster than humans—unthrottled requests overwhelm servers.

**Tiers:**

* Per-user limits
* Per-tenant limits
* Global circuit breakers

**Example (Zapier MCP Gateway):**

* Free tier: 80 calls/hour, 160/day, 300/month
* Built-in auth & rate limiting

**Azure APIM:** Quota enforcement per client/subscription, rate limits per time period.

---

### 6.2 Multi-Tenant Architecture

**Isolated Workspaces:**

* Different groups get isolated tool catalogs
* Role-based access per tenant
* Policy boundaries per workspace
* Shared gateway centralizes observability/compliance

**IBM ContextForge Limitation:** NOT multi-tenant ready—requires custom implementation of:

* User isolation & data segregation
* RBAC
* Resource cleanup/lifecycle management
* Input validation
* Audit logging
* Team/org management

**Access Policies:** Per-user, per-tenant, version control, structured config (no logic in agents).

---

### 6.3 Authentication & Multi-Tenancy

**JWT with Tenant Claims:** Extract tenant ID from token, enforce tenant-scoped access.

**Keycloak RBAC:** Multi-tenant with tenant-specific roles, MCP server OAuth integration.

**Traefik Hub TBAC:** Task-Based Access Control policies with JWT middleware.

---

## 7. Security Best Practices

### 7.1 Token Management

* **Scope tokens per server:** Resource Indicators (RFC 8707)
* **Short lifetimes:** Minutes/hours (not days)
* **Never expose to LLM:** No credentials in context/prompts/traces
* **Cache validation:** JWKS keys 24h, tokens with sensible TTL
* **Aggressive rotation:** Secrets, certificates, keys

---

### 7.2 Credential Storage

* **Vault/secrets manager:** No hard-coding
* **Least privilege scopes:** Per service/environment
* **Separate credentials:** Dev/stage/prod isolation
* **Dynamic credentials:** Just-in-time provisioning, auto-rotation

---

### 7.3 Zero-Trust Principles

* **Continuous validation:** Every request re-evaluated
* **Context-aware authorization:** Identity, time, geo, device posture, action type
* **Defense in depth:** Gateway auth → tool authz → crypto verification → token scoping
* **Least privilege:** Curate servers before exposure, scope access per user/tool
* **No standing privilege:** Short-lived credentials, human-in-the-loop constructs

---

### 7.4 Audit & Monitoring

* **Comprehensive logging:** Tool calls, prompt executions, resource reads
* **Structured JSON logs:** Integration with ELK, Prometheus, Grafana
* **Immutable logs:** Cryptographically signed (Lasso)
* **Forensic traceability:** Every prompt, output, decision point
* **SIEM integration:** Central logging, anomaly detection
* **Rate limit monitoring:** Token issuance anomalies, abuse detection

---

### 7.5 Defense Layers (Traefik Hub)

* **Multiple gates:** API Gateway → MCP Gateway → Backend
* **Policy per layer:** Auth middleware, rate limiting, API policies
* **Bypass resilience:** Attack bypassing one gate caught by next

---

## 8. Enterprise Deployment Patterns

### 8.1 Azure API Management (APIM)

**Use Case:** Central security gateway for MCP servers with Entra ID integration.

**Architecture:**

* APIM as OAuth 2.0 gateway between Claude/agents and MCP servers
* Entra ID handles identity & access control
* Enforce enterprise IAM requirements without backend custom logic

**Required Resources:**

* Azure API Management (Developer/Basic/Standard/Premium tier)
* Azure Function App (Python 3.11, Flex Consumption)
* Azure Storage Account
* Azure Entra ID app registration

**Authentication Methods:**

* OAuth 2.0 with Entra ID
* JWT validation via `validate-azure-ad-token` policy
* Bearer tokens in Authorization header

**Policy Configuration:**

* Authentication/authorization policies apply to all MCP server operations
* Rate limiting & quota enforcement per client/subscription
* IP filtering
* Caching to reduce backend load

**Private MCP Registry (Azure API Center):**

* Centralized location for managing MCP servers
* Discovery portal for users
* Route all MCP traffic through APIM (governance)

**Getting Started:** GitHub samples for remote MCP server with Azure Functions, MCP Inspector/VS Code for testing.

---

### 8.2 Kubernetes Deployment (Microsoft mcp-gateway)

**Architecture:** Envoy-based reverse proxy in Kubernetes.

**Features:**

* Session-aware stateful routing (session_id parameter)
* Distributed session store for multi-instance deployments
* Horizontal scaling with Kubernetes
* Managed Identity for credential-less auth

**Auth Integration:**

* Entra ID app registration with application roles
* Bearer token validation on data/control planes
* RBAC via role claims

---

### 8.3 Gateway-Based Authorization Pattern (Emerging)

**Why:** Centralize policy, transform tokens, create audit boundaries, enable sequence-aware authorization.

**Components:**

* **Gateway:** Token validation, transformation, routing
* **Token Exchange Service:** RFC 8693 implementation
* **Identity Provider:** Keycloak, Auth0, Okta
* **Policy Engine:** OPA, Kuadrant Authorino
* **Secrets Manager:** HashiCorp Vault

**Data Flow:**

1. User authenticates with IdP (OAuth)
2. Gateway validates token
3. Token exchange service creates scoped token for target backend
4. Policy engine enforces tool-level permissions
5. Vault provides credentials for OAuth-unsupported backends
6. Gateway injects scoped token/credentials into request
7. Backend receives minimal-privilege credentials
8. All actions audited centrally

---

### 8.4 High Availability & Resilience

**Recommendations:**

* Circuit breakers for backend failures
* Graceful degradation under auth constraints
* Test agents with authorization failures
* Multi-region deployments
* Health checks & server discovery
* Load balancer sticky sessions (for non-distributed session stores)

---

## 9. Implementation Examples

### 9.1 Kuadrant AuthPolicy (Red Hat MCP Gateway)

```yaml
apiVersion: authorino.kuadrant.io/v1beta2
kind: AuthPolicy
metadata:
  name: mcp-gateway-auth
spec:
  targetRef:
    group: gateway.networking.k8s.io
    kind: HTTPRoute
    name: mcp-route
  authentication:
    "jwt-validation":
      jwt:
        issuerUrl: "https://auth.example.com"
  authorization:
    "opa-policy":
      opa:
        rego: |
          allow {
            input.auth.identity.groups[_] == "mcp.engineer"
          }
  response:
    "tool-wristband":
      wristband:
        issuer: "https://gateway.example.com"
        customClaims:
          tools:
            selector: "auth.authorization.opa-policy.allowed_tools"
        signingKeyRefs:
          - name: wristband-signing-key
            algorithm: ES256
    "vault-pats":
      http:
        url: "https://vault.example.com/v1/kv/data/{auth.identity.username}/{request.host}"
        method: GET
        headers:
          "X-Vault-Token":
            valueFrom:
              secretKeyRef:
                name: vault-token
                key: token
```

---

### 9.2 FastMCP JWT Validation

```python
from fastmcp import FastMCP
from fastmcp.auth import JWTVerifier

verifier = JWTVerifier(
    jwks_uri="https://auth.example.com/.well-known/jwks.json",
    issuer="https://auth.example.com",
    audience="mcp-api"
)

mcp = FastMCP("MySecureServer", auth=verifier)

@mcp.tool()
def protected_tool(query: str) -> str:
    """Only accessible with valid JWT"""
    return f"Processed: {query}"
```

---

### 9.3 Token Exchange Request (RFC 8693)

```http
POST /oauth/token HTTP/1.1
Host: auth.example.com
Content-Type: application/x-www-form-urlencoded

grant_type=urn:ietf:params:oauth:grant-type:token-exchange
&subject_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
&subject_token_type=urn:ietf:params:oauth:token-type:access_token
&requested_token_type=urn:ietf:params:oauth:token-type:access_token
&audience=https://backend-mcp-server.example.com
&scope=mcp:tools mcp:read
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "issued_token_type": "urn:ietf:params:oauth:token-type:access_token",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

---

### 9.4 Dynamic Client Registration (RFC 7591)

```http
POST /register HTTP/1.1
Host: auth.example.com
Content-Type: application/json

{
  "client_name": "MCP Client for AgentX",
  "redirect_uris": ["http://localhost:8080/callback"],
  "grant_types": ["authorization_code"],
  "response_types": ["code"],
  "token_endpoint_auth_method": "none",
  "application_type": "native"
}
```

**Response:**

```json
{
  "client_id": "generated-client-id-12345",
  "client_name": "MCP Client for AgentX",
  "redirect_uris": ["http://localhost:8080/callback"],
  "grant_types": ["authorization_code"],
  "response_types": ["code"],
  "token_endpoint_auth_method": "none"
}
```

---

### 9.5 WWW-Authenticate Header Response

```http
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer realm="https://mcp.example.com", resource_metadata="https://mcp.example.com/.well-known/oauth-protected-resource"
Content-Type: application/json

{
  "error": "unauthorized",
  "message": "Missing or invalid access token"
}
```

---

## 10. Key Takeaways

* **stdio + OAuth = Gateway Bridge:** stdio servers SHOULD NOT use OAuth spec—gateways inject auth headers and expose stdio to clients.
* **Token Exchange (RFC 8693):** Replace broad tokens with narrowly-scoped backend tokens—prevents lateral movement.
* **Dynamic Client Registration (RFC 7591):** MCP clients register dynamically with authz servers—eliminates manual config.
* **Wristband Pattern:** Signed JWT with permitted tools injected as header—cryptographic filtering without DB lookups.
* **Session-Based OAuth (BFF):** MCP server acts as confidential client, issues session JWTs to clients—access tokens stay server-side.
* **Vault Fallback:** OAuth-unsupported backends get PATs/API keys from Vault—centralized secret management.
* **PKCE Mandatory:** S256 challenge method required—clients refuse to proceed if unsupported.
* **JWT Validation:** JWKS endpoints with 24h cache—automatic key rotation, verify issuer/audience/expiration.
* **Rate Limiting:** Per-user, per-tenant, global circuit breakers—AI agents overwhelm servers without throttling.
* **Zero-Trust Evaluation:** Every request re-validated—identity, time, geo, device posture, action type.
* **Multi-Tenant Isolation:** Separate tool catalogs, RBAC per tenant, policy boundaries—centralized observability.
* **Audit Everywhere:** Structured JSON logs, immutable cryptographic signing, SIEM integration—forensic traceability.
* **Defense in Depth:** Gateway auth → tool authz → crypto verification → token scoping—multiple security layers.
* **Gateway-Based Authorization:** Emergent enterprise pattern—centralize policy, transform tokens, create audit boundaries, enable sequence-aware authorization.

---

## 11. Sources

### Microsoft mcp-gateway

* [Using Microsoft Entra ID To Authenticate With MCP Servers Via Sessions · Den Delimarsky](https://den.dev/blog/mcp-server-auth-entra-id-session/)
* [MCP Gateway | mcp-gateway](https://microsoft.github.io/mcp-gateway/)
* [Building Claude-Ready Entra ID-Protected MCP Servers with Azure API Management - Microsoft for Developers](https://developer.microsoft.com/blog/claude-ready-secure-mcp-apim)
* [GitHub - microsoft/mcp-gateway](https://github.com/microsoft/mcp-gateway)
* [Secure Remote MCP Servers With Entra ID And Azure API Management · Den Delimarsky](https://den.dev/blog/remote-mcp-server/)
* [Using Microsoft Entra ID To Authenticate With Model Context Protocol Servers · Den Delimarsky](https://den.dev/blog/auth-modelcontextprotocol-entra-id/)
* [Secure MCP servers with Microsoft Entra authentication - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/configure-authentication-mcp-server-vscode)

### Lasso Security mcp-gateway

* [Why MCP Agents Are the Next Cybersecurity Battleground](https://www.lasso.security/blog/why-mcp-agents-are-the-next-cyber-battleground)
* [The MCP Gateway: Enabling Secure and Scalable Enterprise AI Integration](https://www.infracloud.io/blogs/mcp-gateway/)
* [GitHub - lasso-security/mcp-gateway](https://github.com/lasso-security/mcp-gateway)
* [Centralizing AI Tool Access with the MCP Gateway](https://research.aimultiple.com/mcp-gateway/)
* [Lasso Launches Open Source MCP Security Gateway](https://www.lasso.security/resources/lasso-releases-first-open-source-security-gateway-for-mcp)

### sparfenyuk/mcp-proxy & TBXark/mcp-proxy

* [mcp-proxy MCP Server](https://mcp.so/server/mcp-proxy/sparfenyuk)
* [GitHub - sparfenyuk/mcp-proxy](https://github.com/sparfenyuk/mcp-proxy)
* [GitHub - gws8820/secure-mcp-proxy](https://github.com/gws8820/secure-mcp-proxy)
* [GitHub - TBXark/mcp-proxy](https://github.com/TBXark/mcp-proxy)
* [mcp-proxy](https://tbxark.github.io/mcp-proxy/)

### open-webui/mcpo

* [GitHub - open-webui/mcpo](https://github.com/open-webui/mcpo)
* [feat: Enable per-user authentication in MCP · Discussion #14121](https://github.com/open-webui/open-webui/discussions/14121)
* [Model Context Protocol (MCP) | Open WebUI](https://docs.openwebui.com/features/mcp/)
* [feat: Support OAuth 2.1 Client to Server Auth Flow · Issue #226](https://github.com/open-webui/mcpo/issues/226)
* [Native MCP Server & Tool Management · Discussion #16238](https://github.com/open-webui/open-webui/discussions/16238)

### Gateway Auth Patterns & OAuth

* [Authorization - Model Context Protocol](https://modelcontextprotocol.io/specification/2025-03-26/basic/authorization)
* [Advanced authentication and authorization for MCP Gateway | Red Hat Developer](https://developers.redhat.com/articles/2025/12/12/advanced-authentication-authorization-mcp-gateway)
* [Part Two: MCP Authorization The Hard Way | Solo.io](https://www.solo.io/blog/part-two-mcp-authorization-the-hard-way)
* [From stdio to HTTP SSE: Host Your MCP Server with APISIX API Gateway | Apache APISIX](https://apisix.apache.org/blog/2025/04/21/host-mcp-server-with-api-gateway/)
* [MCP Authorization the Easy Way – agentgateway](https://agentgateway.dev/blog/2025-08-12-mcp-authorization-following-the-spec/)
* [MCP authentication and authorization implementation guide](https://stytch.com/blog/MCP-authentication-and-authorization-guide/)
* [Azure API Management Your Auth Gateway For MCP Servers | Microsoft Community Hub](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
* [OAuth for MCP - Emerging Enterprise Patterns for Agent Authorization](https://blog.gitguardian.com/oauth-for-mcp-emerging-enterprise-patterns-for-agent-authorization/)
* [🔧 ContextForge Gateway - ContextForge MCP Workshop](https://contextforge-org.github.io/mcp-workshop/mcp-gateway/)

### Azure API Management

* [Overview of MCP servers in Azure API Management | Microsoft Learn](https://learn.microsoft.com/en-us/azure/api-management/mcp-server-overview)
* [Connect and govern existing MCP server in Azure API Management | Microsoft Learn](https://learn.microsoft.com/en-us/azure/api-management/expose-existing-mcp-server)
* [Secure access to MCP servers in Azure API Management | Microsoft Learn](https://learn.microsoft.com/en-us/azure/api-management/secure-mcp-servers)
* [Deployment Guide-Copilot Studio agent with MCP Server exposed by API Management using OAuth 2.0 | Microsoft Community Hub](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/deployment-guide-copilot-studio-agent-with-mcp-server-exposed-by-api-management-/4462432)
* [MCP Registry with Azure API Center](https://techcommunity.microsoft.com/blog/integrationsonazureblog/build-secure-launch-your-private-mcp-registry-with-azure-api-center-/4438016)
* [GitHub - Azure-Samples/remote-mcp-apim-functions-python](https://github.com/Azure-Samples/remote-mcp-apim-functions-python)

### Zero-Trust MCP

* [Zero Trust Architecture for MCP Servers Using Pomerium - OpenAI Developer Community](https://community.openai.com/t/zero-trust-architecture-for-mcp-servers-using-pomerium/1288157)
* [MCP Security: Zero Trust Access for Agentic AI | Pomerium](https://www.pomerium.com/blog/secure-access-for-mcp)
* [Design MCP Authorization to Securely Expose APIs | Curity](https://curity.io/resources/learn/design-mcp-authorization-apis/)
* [Understanding and mitigating security risks in MCP implementations | Microsoft Community Hub](https://techcommunity.microsoft.com/blog/microsoft-security-blog/understanding-and-mitigating-security-risks-in-mcp-implementations/4404667)
* [Securing the AI Revolution: Introducing Cloudflare MCP Server Portals](https://blog.cloudflare.com/zero-trust-mcp-server-portals/)
* [Zero Trust for AI: Securing MCP Servers ebook](https://solutions.cerbos.dev/zero-trust-for-ai-securing-mcp-servers)
* [Securing MCP Servers: A Comprehensive Guide](https://www.infracloud.io/blogs/securing-mcp-servers/)
* [What is MCP Server Authentication?](https://www.truefoundry.com/blog/mcp-server-authentication)
* [MCP Servers: Bridging AI to Reality & The Critical Need for Security](https://www.noports.com/blog/mcp-servers-dangers)

### Rate Limiting & Multi-Tenancy

* [How API Gateways Enhance MCP Servers - API7.ai](https://api7.ai/learning-center/api-gateway-guide/api-gateway-enhance-mcp-server)
* [ContextForge MCP Gateway: the MCP router for AI agents](https://www.startuphub.ai/ai-news/artificial-intelligence/2025/contextforge-mcp-gateway-the-mcp-router-for-ai-agents/)
* [Building Multi-User AI Agents with an MCP Server](https://bix-tech.com/building-multi-user-ai-agents-with-an-mcp-server-architecture-security-and-a-practical-blueprint/)
* [mcp-context-forge/SECURITY.md](https://github.com/IBM/mcp-context-forge/blob/main/SECURITY.md)
* [MCP API Gateway Explained | Gravitee](https://www.gravitee.io/blog/mcp-api-gateway-explained-protocols-caching-and-remote-server-integration)
* [MCP Gateway Best Practices | Traefik Hub](https://doc.traefik.io/traefik-hub/mcp-gateway/guides/mcp-gateway-best-practices)

### stdio/SSE/HTTP Bridging

* [GitHub - supercorp-ai/supergateway](https://github.com/supercorp-ai/supergateway)
* [Converting SSE to STDIO via the MCP Gateway | Niklas Heidloff](https://heidloff.net/article/mcp-gateway/)
* [SSE Transport | MCP Framework](https://mcp-framework.com/docs/Transports/sse/)
* [GitHub - sub-arjun/OMNIgateway](https://github.com/sub-arjun/OMNIgateway)
* [Question: How to authorise a client with Bearer header with SSE? · Issue #431](https://github.com/modelcontextprotocol/python-sdk/issues/431)
* [GitHub - acehoss/mcp-gateway](https://github.com/acehoss/mcp-gateway)

### Token Exchange & Vault

* [Token Delegation and MCP server orchestration for multi-user AI systems - DEV Community](https://dev.to/stacklok/token-delegation-and-mcp-server-orchestration-for-multi-user-ai-systems-3gbi)
* [GitHub - RockSolidKnowledge/TokenExchange](https://github.com/RockSolidKnowledge/TokenExchange)
* [RFC 8693 - OAuth 2.0 Token Exchange](https://datatracker.ietf.org/doc/html/rfc8693)
* [RFC 8693 OAuth 2.0 Token Exchange - Authlete](https://www.authlete.com/developers/token_exchange/)
* [Enterprise-Ready MCP • Aaron Parecki](https://aaronparecki.com/2025/05/12/27/enterprise-ready-mcp)
* [Add support for Token Exchange RFC 8693 · Issue #1985](https://github.com/jlowin/fastmcp/issues/1985)
* [GitHub - damienbod/OAuthGrantExchangeOidcDownstreamApi](https://github.com/damienbod/OAuthGrantExchangeOidcDownstreamApi)
* [Token exchange | Nimbus OAuth SDK](https://connect2id.com/products/nimbus-oauth-openid-connect-sdk/examples/oauth/token-exchange)
* [GitHub - rccyx/vault-mcp](https://github.com/rccyx/vault-mcp)
* [Secure AI agent authentication using HashiCorp Vault | HashiCorp Developer](https://developer.hashicorp.com/validated-patterns/vault/ai-agent-identity-with-hashicorp-vault)
* [Use gateways to expose an integration | HashiCorp Cloud Platform](https://developer.hashicorp.com/hcp/docs/vault-secrets/auto-rotation/gateways)
* [Vault MCP Server | HashiCorp Developer](https://developer.hashicorp.com/vault/docs/mcp-server/overview)
* [Best practices for MCP secrets management — WorkOS Guides](https://workos.com/guide/best-practices-for-mcp-secrets-management)

### PKCE & Dynamic Client Registration

* [MCP and OAuth Dynamic Client Registration](https://stytch.com/blog/mcp-oauth-dynamic-client-registration/)
* [Example Securing AI Agent Access with OAuth in MCP](https://stytch.com/blog/oauth-for-mcp-explained-with-a-real-world-example/)
* [Dynamic Client Registration (DCR) in MCP — WorkOS](https://workos.com/blog/dynamic-client-registration-dcr-mcp-oauth)
* [Implementing MCP Authorization for APIs | Curity](https://curity.io/resources/learn/implementing-mcp-authorization-apis/)
* [MCP OAuth 2.1 - A Complete Guide - DEV Community](https://dev.to/composiodev/mcp-oauth-21-a-complete-guide-3g91)
* [What is Dynamic Client Registration in OAuth?](https://www.scalekit.com/blog/dynamic-client-registration-oauth2)
* [Dynamic Client Registration 101](https://www.descope.com/learn/post/dynamic-client-registration)

### WWW-Authenticate & Discovery

* [Clients should support `WWW-Authenticate` · Issue #195](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/195)
* [MCP | Better Auth](https://www.better-auth.com/docs/plugins/mcp)
* [Diving Into the MCP Authorization Specification](https://www.descope.com/blog/post/mcp-auth-spec)
* [Mcpjam](https://www.mcpjam.com/blog/mcp-oauth-guide)
* [Treat the MCP server as an OAuth resource server · Issue #205](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/205)
* [Getting Started with MCP Gateway | Traefik Hub](https://doc.traefik.io/traefik-hub/mcp-gateway/guides/getting-started)
* [OIDC Setup | mcp-auth/docs](https://deepwiki.com/mcp-auth/docs/5.1.1-oidc-setup)

### JWT & JWKS Validation

* [JWT Validation Policy | MuleSoft](https://docs.mulesoft.com/gateway/latest/policies-included-jwt-validation)
* [Token Verification - FastMCP](https://gofastmcp.com/servers/auth/token-verification)
* [Secure your MCP server with OAuth 2.1: Step-by-step guide](https://www.scalekit.com/blog/implement-oauth-for-mcp-servers)
* [Faster JWT Key Rotation in API Gateway | Akamai Blog](https://www.akamai.com/blog/news/verify-jwt-with-json-web-key-set-jwks-in-api-gateway)
* [Verify JWTs using an Application Load Balancer - ELB](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/listener-verify-jwt.html)
* [Getting Authentication Right is Critical to Running MCP Servers - DEV Community](https://dev.to/stacklok/getting-authentication-right-is-critical-to-running-mcp-servers-39fk)

### Envoy & Kuadrant

* [GitHub - kagenti/mcp-gateway](https://github.com/kagenti/mcp-gateway)
* [authorino/docs/user-guides/envoy-jwt-authn-and-authorino.md](https://github.com/Kuadrant/authorino/blob/main/docs/user-guides/envoy-jwt-authn-and-authorino.md)
* [Reusing Envoy built-in authentication filter result - Kuadrant](https://docs.kuadrant.io/0.11.0/authorino/docs/user-guides/envoy-jwt-authn-and-authorino/)
* [User guide: Mixing Envoy built-in filter for auth and Authorino - Kuadrant](https://docs.kuadrant.io/dev/authorino/docs/user-guides/envoy-jwt-authn-and-authorino/)
* [authorino/docs/user-guides/opa-authorization.md](https://github.com/Kuadrant/authorino/blob/main/docs/user-guides/opa-authorization.md)
* [User guide: OpenID Connect (OIDC) and RBAC with Authorino and Keycloak - Kuadrant](https://docs.kuadrant.io/1.2.x/authorino/docs/user-guides/oidc-rbac/)

### Session Management & STDIO OAuth

* [Let's fix OAuth in MCP • Aaron Parecki](https://aaronparecki.com/2025/04/03/15/oauth-for-model-context-protocol)
* [How to using the mcp bridge and set up the ai gatway to host mcp servers? · Discussion #12177](https://github.com/apache/apisix/discussions/12177)
* [MCP authentication and authorization servers](https://stytch.com/blog/mcp-authentication-and-authorization-servers/)
* [MCP Architecture: Components, Lifecycle & Client-Server Tutorial | Obot AI](https://obot.ai/resources/learning-center/mcp-architecture/)
* [MCP Session Management | Puppeteer MCP](https://williamzujkowski.github.io/puppeteer-mcp/architecture/session-management/)
* [An Introduction to MCP and Authorization | Auth0](https://auth0.com/blog/an-introduction-to-mcp-and-authorization/)
