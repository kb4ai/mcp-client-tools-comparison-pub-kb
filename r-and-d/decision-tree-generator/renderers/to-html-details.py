#!/usr/bin/env python3
"""
Render decision tree YAML to HTML with nested <details>/<summary> elements.

Usage:
    ./renderers/to-html-details.py examples/laptop-chooser.yaml
    ./renderers/to-html-details.py examples/laptop-chooser.yaml --full-page

Output is deterministic - same input always produces identical output.
"""

import sys
import argparse
from pathlib import Path
from html import escape as html_escape

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


def render_node(node: dict, indent: int = 0, is_root: bool = False) -> list:
    """Recursively render a node to HTML lines."""
    prefix = '  ' * indent
    lines = []

    if 'question' in node:
        # Decision node
        open_attr = ' open' if is_root else ''
        lines.append(f'{prefix}<details{open_attr}>')
        lines.append(f'{prefix}  <summary>{html_escape(node["question"])}</summary>')

        for branch in node.get('branches', []):
            condition = html_escape(branch['condition'])

            if 'leaf' in branch['next']:
                # Leaf directly under branch
                leaf = html_escape(branch['next']['leaf'])
                lines.append(f'{prefix}  <p class="leaf"><strong>{condition}</strong> → {leaf}</p>')

            elif 'leaf-structured' in branch['next']:
                # Structured leaf
                ls = branch['next']['leaf-structured']
                rec = html_escape(ls['recommendation'])
                lines.append(f'{prefix}  <div class="leaf-structured">')
                lines.append(f'{prefix}    <p><strong>{condition}</strong> → {rec}</p>')

                if ls.get('projects'):
                    lines.append(f'{prefix}    <ul class="projects">')
                    for proj in ls['projects']:
                        lines.append(f'{prefix}      <li>{html_escape(proj)}</li>')
                    lines.append(f'{prefix}    </ul>')

                if ls.get('notes'):
                    notes = html_escape(ls['notes'])
                    lines.append(f'{prefix}    <p class="notes"><em>{notes}</em></p>')

                lines.append(f'{prefix}  </div>')

            else:
                # Nested question
                lines.append(f'{prefix}  <details>')
                lines.append(f'{prefix}    <summary>{condition}</summary>')
                child_lines = render_node(branch['next'], indent + 2)
                lines.extend(child_lines)
                lines.append(f'{prefix}  </details>')

        lines.append(f'{prefix}</details>')

    elif 'leaf' in node:
        lines.append(f'{prefix}<p class="leaf">{html_escape(node["leaf"])}</p>')

    elif 'leaf-structured' in node:
        ls = node['leaf-structured']
        rec = html_escape(ls['recommendation'])
        lines.append(f'{prefix}<div class="leaf-structured">')
        lines.append(f'{prefix}  <p>{rec}</p>')

        if ls.get('projects'):
            lines.append(f'{prefix}  <ul class="projects">')
            for proj in ls['projects']:
                lines.append(f'{prefix}    <li>{html_escape(proj)}</li>')
            lines.append(f'{prefix}  </ul>')

        if ls.get('notes'):
            lines.append(f'{prefix}  <p class="notes"><em>{html_escape(ls["notes"])}</em></p>')

        lines.append(f'{prefix}</div>')

    return lines


def render_tree_fragment(tree_data: dict) -> str:
    """Render tree as HTML fragment (just the tree, no page wrapper)."""
    tree = tree_data['tree']
    title = html_escape(tree.get('title', 'Decision Tree'))
    tree_id = tree['id']

    lines = []
    lines.append(f'<!-- Decision Tree: {title} -->')
    lines.append(f'<section class="decision-tree" id="{tree_id}" aria-label="{title}">')

    node_lines = render_node(tree['root'], indent=1, is_root=True)
    lines.extend(node_lines)

    lines.append('</section>')
    lines.append('')

    return '\n'.join(lines)


def render_full_page(tree_data: dict) -> str:
    """Render tree as full HTML page with styling."""
    tree = tree_data['tree']
    title = html_escape(tree.get('title', 'Decision Tree'))

    css = '''
    .decision-tree {
      font-family: system-ui, -apple-system, sans-serif;
      max-width: 800px;
      margin: 2rem auto;
      padding: 1rem;
    }
    .decision-tree details {
      margin-left: 1.25rem;
      padding: 0.25rem 0;
    }
    .decision-tree summary {
      cursor: pointer;
      font-weight: 600;
      padding: 0.25rem;
    }
    .decision-tree summary:hover {
      background: #f0f0f0;
      border-radius: 4px;
    }
    .decision-tree .leaf {
      margin-left: 2.5rem;
      padding: 0.5rem;
      background: #e8f5e9;
      border-radius: 4px;
      border-left: 3px solid #4caf50;
    }
    .decision-tree .leaf-structured {
      margin-left: 2.5rem;
      padding: 0.5rem;
      background: #e3f2fd;
      border-radius: 4px;
      border-left: 3px solid #2196f3;
    }
    .decision-tree .projects {
      margin: 0.25rem 0;
      padding-left: 1.5rem;
    }
    .decision-tree .notes {
      color: #666;
      font-size: 0.9em;
      margin-top: 0.25rem;
    }'''

    fragment = render_tree_fragment(tree_data)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>{css}
  </style>
</head>
<body>
  <h1>{title}</h1>
{fragment}
</body>
</html>
'''


def main():
    parser = argparse.ArgumentParser(
        description='Render decision tree YAML to HTML with <details> elements'
    )
    parser.add_argument('input_file', help='Input YAML file')
    parser.add_argument(
        '--full-page', '-f',
        action='store_true',
        help='Generate full HTML page with styling (default: fragment only)'
    )

    args = parser.parse_args()

    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    with open(input_path) as f:
        tree_data = yaml.safe_load(f)

    if not tree_data or 'tree' not in tree_data:
        print("Error: Invalid tree structure - missing 'tree' key", file=sys.stderr)
        sys.exit(1)

    if args.full_page:
        output = render_full_page(tree_data)
    else:
        output = render_tree_fragment(tree_data)

    print(output)


if __name__ == '__main__':
    main()
