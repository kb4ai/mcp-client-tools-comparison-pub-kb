# Case Study: Linear MCP Server Authentication with CLI Tools

**Date:** 2025-12-22
**Category:** Authentication, CLI Tools, HTTP Transport
**Servers:** Linear MCP (`https://mcp.linear.app/mcp`)
**Clients Tested:** mcptools (f/mcptools), Claude CLI

## Problem Statement

A user wanted to use mcptools CLI to connect to Linear's MCP server, which requires OAuth authentication. Claude CLI can handle this seamlessly, but mcptools cannot.

## Working Setup (Claude CLI)

Claude CLI handles HTTP MCP with OAuth natively:

```bash
claude mcp add --transport http linear-server https://mcp.linear.app/mcp
```

After OAuth authentication, credentials are stored in `~/.claude/.credentials.json`:

```json
{
  "mcpOAuth": {
    "linear-server|ABCDEF0123456789": {
      "serverName": "linear-server",
      "serverUrl": "https://mcp.linear.app/mcp",
      "clientId": "aBcDeFgH-XyZ012",
      "accessToken": "ABCDEF01-...:TOKEN:xXxXxXxXxXxXxXxX",
      "expiresAt": 1767039278431,
      "refreshToken": "...",
      "scope": ""
    }
  }
}
```

## Failed Attempts with mcptools

### Attempt 1: Direct URL with Bearer token

```bash
mcptools tools https://mcp.linear.app/mcp --headers "Authorization=Bearer <token>"
```

**Result:** `--headers` flag not recognized for `tools` command.

### Attempt 2: Alias with headers

```bash
mcptools alias add linear https://mcp.linear.app/mcp
```

Then manually edited `~/.mcpt/aliases.json`:

```json
{
  "linear": {
    "command": "https://mcp.linear.app/mcp",
    "headers": {
      "Authorization": "Bearer <token>"
    }
  }
}
```

**Result:** `401 Unauthorized` - headers in aliases.json are not read.

### Attempt 3: Config file approach

Created `~/.mcpt/mcp-config.json`:

```json
{
  "mcpServers": {
    "linear": {
      "url": "https://mcp.linear.app/mcp",
      "headers": {
        "Authorization": "Bearer <token>"
      }
    }
  }
}
```

Then:

```bash
mcptools configs alias mcp-linear ~/.mcpt/mcp-config.json '$.mcpServers'
mcptools configs view mcp-linear
```

**Result:** Config shows correctly, but no way to use it with `tools` command.

### Attempt 4: Environment variable

```bash
MCP_HTTP_HEADERS="Authorization=Bearer <token>" mcptools tools https://mcp.linear.app/mcp
```

**Result:** `401 Unauthorized` - env var not recognized.

### Attempt 5: configs set command

According to docs:

```bash
mcp configs set cursor my-api https://api.example.com/mcp --headers "Authorization=Bearer token"
```

**Result:** `configs set` requires a config file alias (like "cursor", "vscode") that doesn't exist on Linux CLI-only setup.

## Root Cause Analysis

mcptools architecture reveals several design decisions that break standalone CLI HTTP auth:

1. **`--headers` flag scope**: Only available in `configs set`, not in `tools`/`call`/`shell` commands
2. **Alias headers**: `aliases.json` supports `headers` field syntactically, but code doesn't read it
3. **Config system**: Designed for IDE configs (Cursor, VSCode, etc.), assumes pre-existing config files
4. **No env var support**: Unlike STDIO servers, HTTP headers can't be passed via env vars

## Implications for Documentation

Our YAML file previously stated:

```yaml
authentication:
  bearer-token: true  # WRONG
  auth-notes:
    - "Auth via env vars and CLI flags"  # MISLEADING
```

This should be:

```yaml
authentication:
  bearer-token: false  # --headers doesn't work for direct commands
  auth-notes:
    - "STDIO: env vars work"
    - "HTTP: headers only configurable via 'configs set', not usable standalone"
    - "LIMITATION: No documented way to pass Authorization headers with direct HTTP commands"
```

## Alternative Solutions

### Option 1: Use wong2/mcp-cli

```bash
npm install -g @anthropic/mcp-cli
mcp-cli connect https://mcp.linear.app/mcp
# Handles OAuth automatically
```

### Option 2: Use sparfenyuk/mcp-proxy as intermediary

```bash
pip install mcp-proxy
mcp-proxy --backend https://mcp.linear.app/mcp \
  --auth-header "Authorization: Bearer <token>" \
  --listen 127.0.0.1:8000

# Then use mcptools with local proxy
mcptools tools http://127.0.0.1:8000
```

### Option 3: Direct curl for testing

```bash
# Extract token from Claude CLI
TOKEN=$(jq -r '.mcpOAuth | to_entries[0].value.accessToken' ~/.claude/.credentials.json)

# Call MCP directly
curl -X POST https://mcp.linear.app/mcp \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

## Lessons Learned

1. **Transport != Auth Support**: A tool supporting HTTP transport doesn't mean it supports HTTP authentication
2. **Test with real servers**: OAuth-protected HTTP MCP servers (Linear, GitHub, etc.) expose auth gaps
3. **IDE-centric design**: Many MCP CLI tools assume IDE integration rather than standalone use
4. **Documentation gap**: "bearer-token: true" should mean "user can actually pass Bearer tokens", not "code mentions Bearer somewhere"

## Proposed Schema Enhancement

Consider adding to spec.yaml:

```yaml
auth-transport-support:
  type: object
  properties:
    stdio-env-vars:
      type: boolean
      description: "Can pass auth via env vars for STDIO"
    http-headers-direct:
      type: boolean
      description: "Can pass headers directly to HTTP commands (not just config)"
    http-oauth-flow:
      type: boolean
      description: "Implements full OAuth flow for HTTP"
    http-bearer-injection:
      type: boolean
      description: "Can inject Bearer tokens to HTTP requests"
```

This would distinguish between:
- **Theoretical support** (code handles Bearer tokens)
- **Practical usability** (user can actually authenticate with HTTP MCP servers)

## Linear MCP Server Notes

Linear MCP server accepts:

* `Authorization: Bearer <token>` header
* Both HTTP and SSE transports
* OAuth 2.1 with dynamic client registration

Reference: https://linear.app/docs/mcp

## Environment

* OS: Linux (Arch)
* mcptools: installed via `go install` at `~/go/bin/mcptools`
* Claude CLI: v2.0.74+
* Linear MCP endpoint: `https://mcp.linear.app/mcp`
