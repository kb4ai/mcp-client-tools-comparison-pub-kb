#!/usr/bin/env python3
"""
Generate decision tree visualizations from the MCP tool chooser YAML.

Outputs:
  - comparisons/decision-tree.md         (Mermaid flowchart)
  - comparisons/decision-tree-interactive.html  (Interactive HTML)

Usage:
    ./scripts/generate-decision-tree.py
    ./scripts/generate-decision-tree.py --dry-run
"""

import sys
from pathlib import Path

# Add decision_tree package to path
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
DECISION_TREE_DIR = PROJECT_ROOT / "r-and-d" / "decision-tree-generator"
sys.path.insert(0, str(DECISION_TREE_DIR))

from decision_tree import load_tree, render_mermaid, render_html

# Paths
TREE_SOURCE = DECISION_TREE_DIR / "examples" / "mcp-tool-chooser.yaml"
OUTPUT_MERMAID = PROJECT_ROOT / "comparisons" / "decision-tree.md"
OUTPUT_HTML = PROJECT_ROOT / "comparisons" / "decision-tree-interactive.html"


def generate_mermaid_markdown(tree_data: dict) -> str:
    """Generate markdown file with Mermaid decision tree."""
    title = tree_data['tree'].get('title', 'Decision Tree')
    description = tree_data['tree'].get('description', '')
    mermaid = render_mermaid(tree_data, direction='TD')

    return f"""# {title}

{description}

## Interactive Decision Tree

Use this flowchart to find the right MCP ecosystem tool for your needs.

```mermaid
{mermaid.strip()}
```

## How to Use

1. Start at the top: "What's your primary use case?"
2. Follow the arrows based on your answers
3. Arrive at a recommended tool

## Need More Details?

* [Full comparison tables](auto-generated.md)
* [Security analysis](security.md)
* [Authentication guide](authentication.md)

---
*Auto-generated from `r-and-d/decision-tree-generator/examples/mcp-tool-chooser.yaml`*
"""


def generate_html_page(tree_data: dict) -> str:
    """Generate standalone HTML page with interactive details tree."""
    return render_html(tree_data, full_page=True)


def main():
    dry_run = '--dry-run' in sys.argv

    if not TREE_SOURCE.exists():
        print(f"Error: Tree source not found: {TREE_SOURCE}")
        sys.exit(1)

    print(f"Loading tree from: {TREE_SOURCE}")
    tree_data = load_tree(TREE_SOURCE)

    # Generate Mermaid markdown
    mermaid_md = generate_mermaid_markdown(tree_data)
    if dry_run:
        print("\n=== Mermaid Markdown ===")
        print(mermaid_md[:500] + "...")
    else:
        OUTPUT_MERMAID.write_text(mermaid_md)
        print(f"Generated: {OUTPUT_MERMAID}")

    # Generate HTML
    html = generate_html_page(tree_data)
    if dry_run:
        print("\n=== HTML (first 500 chars) ===")
        print(html[:500] + "...")
    else:
        OUTPUT_HTML.write_text(html)
        print(f"Generated: {OUTPUT_HTML}")

    if not dry_run:
        print("\nDone! Files ready for git commit.")


if __name__ == '__main__':
    main()
