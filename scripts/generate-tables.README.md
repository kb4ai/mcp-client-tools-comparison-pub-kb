# generate-tables.py

Generates comparison tables and statistics from project YAML files.

## Usage

```bash
# Generate all tables (default)
./scripts/generate-tables.py

# Specific views
./scripts/generate-tables.py --by-category      # Group by category
./scripts/generate-tables.py --by-transport     # Transport support matrix
./scripts/generate-tables.py --by-stars         # Sort by GitHub stars
./scripts/generate-tables.py --reputable-only   # Only official/reputable sources

# Export as JSON
./scripts/generate-tables.py --json
```

## Requirements

* Python 3.6+
* PyYAML: `pip install pyyaml`

## Output Sections

### Summary Statistics

* Total project count
* Reputable source count
* Combined GitHub stars
* Breakdown by category and language

### Overview Table

All projects sorted by stars with columns:

* Project name (linked to repo)
* Stars
* Language
* Category
* Supported transports

### Reputable Sources

Projects from official/known organizations:

* Anthropic/MCP
* Microsoft
* Docker
* Redpanda
* NCC Group
* etc.

### Transport Matrix

Checkbox matrix showing support for:

* stdio
* SSE
* HTTP
* WebSocket
* gRPC

### By Category

Projects grouped into categories:

* cli-client
* http-bridge
* websocket-bridge
* grpc-bridge
* rest-api-bridge
* proxy-aggregator
* enterprise-gateway
* docker-integration
* kubernetes-integration
* openapi-wrapper
* specialized-adapter
* official-tool

## Typical Workflow

```bash
# Update comparisons/auto-generated.md
./scripts/generate-tables.py > comparisons/auto-generated.md

# Generate just the stats
./scripts/generate-tables.py --by-stars | head -30

# Export for further processing
./scripts/generate-tables.py --json > /tmp/projects.json
```
