# Decision Tree Generator R&D

Research and development for **deterministic, reproducible** decision tree generation from structured YAML data.

## Concept

Given a YAML file describing decision criteria and outcomes, generate:

1. **Canonical representation** (normalized YAML or TTL/RDF)
2. **Visual representations**:
   - Mermaid diagrams (for markdown/GitHub)
   - Graphviz DOT (for high-quality SVG/PNG)
   - HTML with nested `<details>/<summary>` (interactive drill-down)

## Key Principles

* **Deterministic** - Same input YAML always produces identical output
* **Reproducible** - No randomness, timestamps, or environment-dependent values
* **Single source of truth** - Decision logic lives in YAML, renderers are pure transformations
* **Format agnostic** - Core tree structure can be serialized to any format

## Directory Structure

```
r-and-d/decision-tree-generator/
├── README.md              # This file
├── spec/
│   ├── schema.yaml        # Decision tree YAML schema
│   └── design.md          # Design document
├── examples/
│   ├── mcp-tool-chooser.yaml    # MCP ecosystem tool selector
│   └── laptop-chooser.yaml      # Simple example
├── renderers/
│   ├── to-mermaid.py      # YAML → Mermaid flowchart
│   ├── to-graphviz.py     # YAML → DOT format
│   ├── to-html-details.py # YAML → HTML <details> tree
│   └── to-yaml-normalized.py    # YAML → canonical YAML
└── output/                # Generated files (gitignored)
```

## Usage (Planned)

```bash
# Generate all formats
./renderers/to-mermaid.py examples/mcp-tool-chooser.yaml > output/mcp-chooser.md
./renderers/to-graphviz.py examples/mcp-tool-chooser.yaml | dot -Tsvg > output/mcp-chooser.svg
./renderers/to-html-details.py examples/mcp-tool-chooser.yaml > output/mcp-chooser.html
```

## Decision Tree YAML Format

```yaml
tree:
  id: mcp-tool-chooser
  title: "Choose an MCP Tool"
  root:
    question: "What do you need?"
    branches:
      - condition: "CLI interface"
        next:
          question: "LLM integration needed?"
          branches:
            - condition: "Yes"
              leaf: "Use chrishayuk/mcp-cli or adhikasp/mcp-client-cli"
            - condition: "No"
              leaf: "Use f/mcptools"
      - condition: "REST API exposure"
        leaf: "Use SecretiveShell/MCP-Bridge or acehoss/mcp-gateway"
```

## Application to MCP Comparison

This R&D aims to auto-generate decision trees FROM the `projects/*.yaml` data:

1. Parse project YAML files
2. Extract categories, features, transports
3. Build decision tree based on user goals
4. Render as interactive guide in README or separate page

## Status

🚧 **R&D Phase** - Exploring approaches

## References

* [Mermaid Flowchart Syntax](https://mermaid.js.org/syntax/flowchart.html)
* [Graphviz DOT Language](https://graphviz.org/doc/info/lang.html)
* HTML `<details>` element for progressive disclosure
