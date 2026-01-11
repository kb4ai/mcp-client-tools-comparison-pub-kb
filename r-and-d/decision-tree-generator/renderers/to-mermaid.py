#!/usr/bin/env python3
"""
Render decision tree YAML to Mermaid flowchart format.

Usage:
    ./renderers/to-mermaid.py examples/laptop-chooser.yaml
    ./renderers/to-mermaid.py examples/mcp-tool-chooser.yaml --direction LR

Output is deterministic - same input always produces identical output.
"""

import sys
import argparse
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


def escape_mermaid(text: str) -> str:
    """Escape special characters for Mermaid labels."""
    # Replace characters that break Mermaid syntax
    text = text.replace('"', "'")
    text = text.replace('<', '‹')
    text = text.replace('>', '›')
    text = text.replace('|', '│')
    text = text.replace('[', '⟦')
    text = text.replace(']', '⟧')
    text = text.replace('{', '⟨')
    text = text.replace('}', '⟩')
    return text


def truncate(text: str, max_len: int = 40) -> str:
    """Truncate text to max length with ellipsis."""
    if len(text) <= max_len:
        return text
    return text[:max_len - 3] + "..."


def generate_node_id(tree_id: str, path: list) -> str:
    """Generate deterministic node ID from path."""
    if not path:
        return f"{tree_id}_root"
    return f"{tree_id}_{'_'.join(map(str, path))}"


def render_node(node: dict, tree_id: str, path: list, lines: list, direction: str) -> None:
    """Recursively render a node and its children."""
    node_id = generate_node_id(tree_id, path)

    if 'question' in node:
        # Decision node - square brackets for questions
        question = escape_mermaid(truncate(node['question']))
        lines.append(f'    {node_id}["{question}"]')

        for i, branch in enumerate(node.get('branches', [])):
            child_path = path + [i]
            child_id = generate_node_id(tree_id, child_path)
            condition = escape_mermaid(truncate(branch['condition'], 25))

            # Render edge with condition label
            lines.append(f'    {node_id} -->|"{condition}"| {child_id}')

            # Recursively render child node
            render_node(branch['next'], tree_id, child_path, lines, direction)

    elif 'leaf' in node:
        # Simple leaf - rounded brackets for recommendations
        leaf = escape_mermaid(truncate(node['leaf'], 50))
        lines.append(f'    {node_id}("{leaf}")')

    elif 'leaf-structured' in node:
        # Structured leaf - show recommendation
        rec = escape_mermaid(truncate(node['leaf-structured']['recommendation'], 50))
        lines.append(f'    {node_id}("{rec}")')


def render_tree(tree_data: dict, direction: str = 'TD') -> str:
    """Render full decision tree to Mermaid format."""
    tree = tree_data['tree']
    tree_id = tree['id'].replace('-', '_')  # Mermaid doesn't like hyphens in IDs
    title = tree.get('title', 'Decision Tree')

    lines = []

    # Header comment (for reproducibility tracking)
    lines.append(f'%% Decision Tree: {title}')
    lines.append(f'%% Generated from: {tree_id}')
    lines.append('')

    # Flowchart declaration
    lines.append(f'flowchart {direction}')

    # Render all nodes
    render_node(tree['root'], tree_id, [], lines, direction)

    # Add newline at end (POSIX compliance)
    lines.append('')

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Render decision tree YAML to Mermaid flowchart'
    )
    parser.add_argument('input_file', help='Input YAML file')
    parser.add_argument(
        '--direction', '-d',
        choices=['TD', 'TB', 'LR', 'RL', 'BT'],
        default='TD',
        help='Flowchart direction (default: TD = top-down)'
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

    output = render_tree(tree_data, args.direction)
    print(output)


if __name__ == '__main__':
    main()
