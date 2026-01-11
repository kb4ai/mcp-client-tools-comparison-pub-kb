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
    ./scripts/generate-decision-tree.py --check-coverage
"""

import sys
import re
from pathlib import Path

import yaml

from git_metadata import get_reproducible_footer, warn_uncommitted

# Add decision_tree package to path
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
DECISION_TREE_DIR = PROJECT_ROOT / "r-and-d" / "decision-tree-generator"
sys.path.insert(0, str(DECISION_TREE_DIR))

from decision_tree import load_tree, render_mermaid, render_mermaid_split, render_html
from decision_tree import check_coverage, generate_coverage_report, get_all_tree_projects

# Paths
TREE_SOURCE = DECISION_TREE_DIR / "examples" / "mcp-tool-chooser.yaml"
OUTPUT_MERMAID = PROJECT_ROOT / "comparisons" / "decision-tree.md"
OUTPUT_UNFOLDABLE = PROJECT_ROOT / "comparisons" / "decision-tree-unfoldable.md"
OUTPUT_HTML = PROJECT_ROOT / "comparisons" / "decision-tree-interactive.html"
PROJECTS_DIR = PROJECT_ROOT / "projects"

# Input patterns for reproducible metadata
INPUT_PATTERNS = [
    "r-and-d/decision-tree-generator/examples/mcp-tool-chooser.yaml"
]


def generate_mermaid_markdown(tree_data: dict, metadata_footer: str = "", split: bool = True) -> str:
    """Generate markdown file with Mermaid decision tree.

    Args:
        tree_data: Tree dict with 'tree' key
        metadata_footer: Reproducible metadata footer string
        split: If True, split into overview + per-category sections (default)
    """
    title = tree_data['tree'].get('title', 'Decision Tree')
    description = tree_data['tree'].get('description', '')

    footer_line = f"\n*{metadata_footer}*" if metadata_footer else ""

    if not split:
        # Single large diagram (legacy mode)
        mermaid = render_mermaid(tree_data, direction='TD')
        return f"""# {title}

{description}

```mermaid
{mermaid.strip()}
```

---
*Auto-generated from `r-and-d/decision-tree-generator/examples/mcp-tool-chooser.yaml`*{footer_line}
"""

    # Split mode: overview + sections
    split_data = render_mermaid_split(tree_data, direction='TD')

    lines = []
    lines.append(f'# {title}')
    lines.append('')
    lines.append(description)
    lines.append('')
    lines.append('## Quick Navigation')
    lines.append('')
    lines.append('Click a category below to jump to its decision tree:')
    lines.append('')

    # Table of contents
    for section in split_data['sections']:
        anchor = section['id']
        lines.append(f'* [{section["condition"]}](#{anchor})')
    lines.append('')

    # Overview diagram
    lines.append('## Overview')
    lines.append('')
    lines.append('```mermaid')
    lines.append(split_data['overview'].strip())
    lines.append('```')
    lines.append('')

    # Individual sections
    for section in split_data['sections']:
        lines.append(f'## {section["condition"]} {{#{section["id"]}}}')
        lines.append('')
        lines.append('```mermaid')
        lines.append(section['mermaid'].strip())
        lines.append('```')
        lines.append('')

    lines.append('---')
    lines.append('')
    lines.append('**Other views:** [Unfoldable Tree](decision-tree-unfoldable.md) | [Full Tables](auto-generated.md)')
    lines.append('')
    lines.append('*Auto-generated from `r-and-d/decision-tree-generator/examples/mcp-tool-chooser.yaml`*')
    if metadata_footer:
        lines.append('')
        lines.append(f'*{metadata_footer}*')

    return '\n'.join(lines)


def generate_html_page(tree_data: dict, metadata_footer: str = "") -> str:
    """Generate standalone HTML page with interactive details tree.

    Args:
        tree_data: Tree dict with 'tree' key
        metadata_footer: Reproducible metadata footer string
    """
    html = render_html(tree_data, full_page=True)
    # Insert metadata footer as HTML comment before closing body tag
    if metadata_footer:
        footer_comment = f"\n<!-- {metadata_footer} -->\n"
        html = html.replace("</body>", f"{footer_comment}</body>")
    return html


def generate_unfoldable_markdown(tree_data: dict, metadata_footer: str = "") -> str:
    """Generate markdown file with embedded HTML <details>/<summary> tree.

    Uses only basic HTML that GitHub renders natively (no <style> tags).

    Args:
        tree_data: Tree dict with 'tree' key
        metadata_footer: Reproducible metadata footer string
    """
    title = tree_data['tree'].get('title', 'Decision Tree')
    description = tree_data['tree'].get('description', '')

    # Generate clean HTML without wrapper classes (GitHub strips most attributes)
    html_fragment = _render_details_tree(tree_data['tree']['root'], is_root=True)

    footer_line = f"\n\n*{metadata_footer}*" if metadata_footer else ""

    return f"""# {title}

{description}

## Interactive Guide

**Click to expand each section** and drill down to find the right tool for your needs.

{html_fragment}

---

**Other views:** [Mermaid Flowchart](decision-tree.md) | [Full comparison tables](auto-generated.md) | [Security analysis](security.md)

*Auto-generated from `r-and-d/decision-tree-generator/examples/mcp-tool-chooser.yaml`*{footer_line}
"""


def _render_details_tree(node: dict, depth: int = 0, is_root: bool = False) -> str:
    """Render node as clean HTML <details>/<summary> for GitHub markdown.

    Uses visual indentation prefix at each level for hierarchy.
    """
    lines = []
    # Visual indent: use box-drawing chars for tree structure
    indent = '│  ' * depth if depth > 0 else ''
    branch = '├─ ' if depth > 0 else ''

    if 'question' in node:
        open_attr = ' open' if is_root else ''
        lines.append(f'<details{open_attr}>')
        if is_root:
            lines.append(f'<summary>🔍 <strong>{node["question"]}</strong></summary>')
        else:
            lines.append(f'<summary>{indent}{branch}❓ {node["question"]}</summary>')
        lines.append('')

        for i, branch_item in enumerate(node.get('branches', [])):
            condition = branch_item['condition']
            next_node = branch_item['next']
            child_indent = '│  ' * (depth + 1)
            is_last = (i == len(node.get('branches', [])) - 1)
            child_branch = '└─ ' if is_last else '├─ '

            if 'leaf' in next_node:
                lines.append(f'<details>')
                lines.append(f'<summary>{child_indent}{child_branch}📌 {condition}</summary>')
                lines.append('')
                lines.append(f'{child_indent}│')
                lines.append(f'{child_indent}└── ✅ **{next_node["leaf"]}**')
                lines.append('')
                lines.append('</details>')
                lines.append('')

            elif 'leaf-structured' in next_node:
                ls = next_node['leaf-structured']
                lines.append(f'<details>')
                lines.append(f'<summary>{child_indent}{child_branch}📌 {condition}</summary>')
                lines.append('')
                lines.append(f'{child_indent}│')
                lines.append(f'{child_indent}├── ✅ **{ls["recommendation"]}**')
                if ls.get('projects'):
                    for proj in ls['projects']:
                        lines.append(f'{child_indent}│   • `{proj}`')
                if ls.get('notes'):
                    lines.append(f'{child_indent}│')
                    lines.append(f'{child_indent}└── *{ls["notes"]}*')
                lines.append('')
                lines.append('</details>')
                lines.append('')

            else:
                lines.append(f'<details>')
                lines.append(f'<summary>{child_indent}{child_branch}📂 {condition}</summary>')
                lines.append('')
                nested = _render_details_tree(next_node, depth + 2)
                lines.append(nested)
                lines.append('</details>')
                lines.append('')

        lines.append('</details>')

    elif 'leaf' in node:
        lines.append(f'{indent}└── ✅ **{node["leaf"]}**')

    elif 'leaf-structured' in node:
        ls = node['leaf-structured']
        lines.append(f'{indent}├── ✅ **{ls["recommendation"]}**')
        if ls.get('projects'):
            for proj in ls['projects']:
                lines.append(f'{indent}│   • `{proj}`')
        if ls.get('notes'):
            lines.append(f'{indent}└── *{ls["notes"]}*')

    return '\n'.join(lines)


def load_projects_from_yaml() -> list:
    """Load all project YAML files and extract org/repo names.

    Returns:
        List of project names in 'org/repo' format
    """
    projects = []

    if not PROJECTS_DIR.exists():
        return projects

    for yaml_file in sorted(PROJECTS_DIR.glob('*.yaml')):
        try:
            with open(yaml_file) as f:
                data = yaml.safe_load(f)

            repo_url = data.get('repo-url', '')
            # Extract org/repo from GitHub URL
            # e.g., "https://github.com/adhikasp/mcp-client-cli" -> "adhikasp/mcp-client-cli"
            match = re.search(r'github\.com/([^/]+/[^/]+)', repo_url)
            if match:
                projects.append(match.group(1))
        except Exception as e:
            print(f"Warning: Failed to parse {yaml_file}: {e}", file=sys.stderr)

    return projects


def run_coverage_check(tree_data: dict, verbose: bool = False) -> bool:
    """Check that all projects in projects/ are covered by the decision tree.

    Args:
        tree_data: Loaded decision tree
        verbose: If True, print covered items too

    Returns:
        True if all projects are covered, False if any are missing
    """
    projects = load_projects_from_yaml()

    if not projects:
        print("No projects found in projects/ directory")
        return True

    lines, all_covered = generate_coverage_report(tree_data, projects, verbose=verbose)

    # Print the report lines
    for line in lines:
        print(line)

    if all_covered:
        print(f"\n✓ All {len(projects)} projects are covered by the decision tree")
    else:
        result = check_coverage(tree_data, projects)
        print(f"\n✗ Coverage: {result['coverage_percent']:.1f}% ({len(result['covered'])}/{len(projects)})")

    return all_covered


def main():
    dry_run = '--dry-run' in sys.argv
    check_only = '--check-coverage' in sys.argv
    verbose = '--verbose' in sys.argv or '-v' in sys.argv

    if not TREE_SOURCE.exists():
        print(f"Error: Tree source not found: {TREE_SOURCE}")
        sys.exit(1)

    print(f"Loading tree from: {TREE_SOURCE}")
    tree_data = load_tree(TREE_SOURCE)

    # If only checking coverage, run check and exit
    if check_only:
        print("\n=== Coverage Check ===")
        all_covered = run_coverage_check(tree_data, verbose=verbose)
        sys.exit(0 if all_covered else 1)

    # Check for uncommitted changes and generate reproducible metadata footer
    warn_uncommitted(INPUT_PATTERNS, PROJECT_ROOT)
    metadata_footer = get_reproducible_footer(INPUT_PATTERNS, PROJECT_ROOT)
    print(f"Metadata: {metadata_footer}")

    # Generate Mermaid markdown
    mermaid_md = generate_mermaid_markdown(tree_data, metadata_footer=metadata_footer)
    if dry_run:
        print("\n=== Mermaid Markdown ===")
        print(mermaid_md[:500] + "...")
    else:
        OUTPUT_MERMAID.write_text(mermaid_md)
        print(f"Generated: {OUTPUT_MERMAID}")

    # Generate unfoldable markdown (HTML <details> in markdown)
    unfoldable_md = generate_unfoldable_markdown(tree_data, metadata_footer=metadata_footer)
    if dry_run:
        print("\n=== Unfoldable Markdown ===")
        print(unfoldable_md[:500] + "...")
    else:
        OUTPUT_UNFOLDABLE.write_text(unfoldable_md)
        print(f"Generated: {OUTPUT_UNFOLDABLE}")

    # Generate standalone HTML page
    html = generate_html_page(tree_data, metadata_footer=metadata_footer)
    if dry_run:
        print("\n=== HTML (first 500 chars) ===")
        print(html[:500] + "...")
    else:
        OUTPUT_HTML.write_text(html)
        print(f"Generated: {OUTPUT_HTML}")

    # Run coverage check (always, after generation)
    print("\n=== Coverage Check ===")
    all_covered = run_coverage_check(tree_data, verbose=verbose)

    if not dry_run:
        if all_covered:
            print("\nDone! Files ready for git commit.")
        else:
            print("\nDone! Files generated but some projects are not in the decision tree.")
            print("Consider updating r-and-d/decision-tree-generator/examples/mcp-tool-chooser.yaml")


if __name__ == '__main__':
    main()
