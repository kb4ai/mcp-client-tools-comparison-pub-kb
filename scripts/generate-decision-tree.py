#!/usr/bin/env python3
"""
Generate decision tree visualizations from the MCP tool chooser YAML.

Outputs:
  - comparisons/decision-tree.md              (Mermaid flowchart)
  - comparisons/decision-tree-unfoldable.md   (HTML <details> in markdown)
  - comparisons/decision-tree-interactive.html (Standalone HTML page)

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
OUTPUT_UNFOLDABLE = PROJECT_ROOT / "comparisons" / "decision-tree-unfoldable.md"
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


def generate_unfoldable_markdown(tree_data: dict) -> str:
    """Generate markdown file with embedded HTML <details>/<summary> tree.

    Uses only basic HTML that GitHub renders natively (no <style> tags).
    """
    title = tree_data['tree'].get('title', 'Decision Tree')
    description = tree_data['tree'].get('description', '')

    # Generate clean HTML without wrapper classes (GitHub strips most attributes)
    html_fragment = _render_details_tree(tree_data['tree']['root'], is_root=True)

    return f"""# {title}

{description}

## Interactive Guide

**Click to expand each section** and drill down to find the right tool for your needs.

{html_fragment}

---

**Other views:** [Mermaid Flowchart](decision-tree.md) | [Full comparison tables](auto-generated.md) | [Security analysis](security.md)

*Auto-generated from `r-and-d/decision-tree-generator/examples/mcp-tool-chooser.yaml`*
"""


def _render_details_tree(node: dict, is_root: bool = False) -> str:
    """Render node as clean HTML <details>/<summary> for GitHub markdown."""
    lines = []

    if 'question' in node:
        open_attr = ' open' if is_root else ''
        lines.append(f'<details{open_attr}>')
        lines.append(f'<summary><strong>{node["question"]}</strong></summary>')
        lines.append('')  # Blank line for markdown parsing

        for branch in node.get('branches', []):
            condition = branch['condition']
            next_node = branch['next']

            if 'leaf' in next_node:
                # Simple leaf - render as blockquote
                lines.append(f'<details>')
                lines.append(f'<summary>{condition}</summary>')
                lines.append('')
                lines.append(f'> ✅ **{next_node["leaf"]}**')
                lines.append('')
                lines.append('</details>')
                lines.append('')

            elif 'leaf-structured' in next_node:
                # Structured leaf with projects and notes
                ls = next_node['leaf-structured']
                lines.append(f'<details>')
                lines.append(f'<summary>{condition}</summary>')
                lines.append('')
                lines.append(f'> ✅ **{ls["recommendation"]}**')
                if ls.get('projects'):
                    lines.append('>')
                    for proj in ls['projects']:
                        lines.append(f'> - `{proj}`')
                if ls.get('notes'):
                    lines.append('>')
                    lines.append(f'> *{ls["notes"]}*')
                lines.append('')
                lines.append('</details>')
                lines.append('')

            else:
                # Nested question
                lines.append(f'<details>')
                lines.append(f'<summary>{condition}</summary>')
                lines.append('')
                nested = _render_details_tree(next_node)
                lines.append(nested)
                lines.append('</details>')
                lines.append('')

        lines.append('</details>')

    elif 'leaf' in node:
        lines.append(f'> ✅ **{node["leaf"]}**')

    elif 'leaf-structured' in node:
        ls = node['leaf-structured']
        lines.append(f'> ✅ **{ls["recommendation"]}**')
        if ls.get('projects'):
            lines.append('>')
            for proj in ls['projects']:
                lines.append(f'> - `{proj}`')
        if ls.get('notes'):
            lines.append('>')
            lines.append(f'> *{ls["notes"]}*')

    return '\n'.join(lines)


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

    # Generate unfoldable markdown (HTML <details> in markdown)
    unfoldable_md = generate_unfoldable_markdown(tree_data)
    if dry_run:
        print("\n=== Unfoldable Markdown ===")
        print(unfoldable_md[:500] + "...")
    else:
        OUTPUT_UNFOLDABLE.write_text(unfoldable_md)
        print(f"Generated: {OUTPUT_UNFOLDABLE}")

    # Generate standalone HTML page
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
