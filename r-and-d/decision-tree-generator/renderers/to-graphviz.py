#!/usr/bin/env python3
"""
Render decision tree YAML to Graphviz DOT format.

Usage:
    ./renderers/to-graphviz.py examples/laptop-chooser.yaml
    ./renderers/to-graphviz.py examples/laptop-chooser.yaml | dot -Tsvg > output.svg
    ./renderers/to-graphviz.py examples/laptop-chooser.yaml | dot -Tpng > output.png

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


def escape_dot(text: str) -> str:
    """Escape special characters for DOT labels."""
    text = text.replace('\\', '\\\\')
    text = text.replace('"', '\\"')
    text = text.replace('\n', '\\n')
    return text


def truncate(text: str, max_len: int = 40) -> str:
    """Truncate text to max length with ellipsis."""
    if len(text) <= max_len:
        return text
    return text[:max_len - 3] + "..."


def wrap_text(text: str, width: int = 30) -> str:
    """Wrap text at word boundaries for better node display."""
    words = text.split()
    lines = []
    current_line = []
    current_len = 0

    for word in words:
        if current_len + len(word) + 1 > width and current_line:
            lines.append(' '.join(current_line))
            current_line = [word]
            current_len = len(word)
        else:
            current_line.append(word)
            current_len += len(word) + 1

    if current_line:
        lines.append(' '.join(current_line))

    return '\\n'.join(lines)


def generate_node_id(tree_id: str, path: list) -> str:
    """Generate deterministic node ID from path."""
    if not path:
        return f"n_root"
    return f"n_{'_'.join(map(str, path))}"


def render_node(node: dict, tree_id: str, path: list, nodes: list, edges: list) -> None:
    """Recursively render a node and its children."""
    node_id = generate_node_id(tree_id, path)

    if 'question' in node:
        # Decision node - box shape
        question = escape_dot(wrap_text(node['question'], 25))
        nodes.append(f'    {node_id} [label="{question}" shape=box];')

        for i, branch in enumerate(node.get('branches', [])):
            child_path = path + [i]
            child_id = generate_node_id(tree_id, child_path)
            condition = escape_dot(truncate(branch['condition'], 20))

            # Render edge with condition label
            edges.append(f'    {node_id} -> {child_id} [label="{condition}"];')

            # Recursively render child node
            render_node(branch['next'], tree_id, child_path, nodes, edges)

    elif 'leaf' in node:
        # Simple leaf - ellipse shape (default)
        leaf = escape_dot(wrap_text(node['leaf'], 30))
        nodes.append(f'    {node_id} [label="{leaf}" shape=ellipse style=filled fillcolor=lightgreen];')

    elif 'leaf-structured' in node:
        # Structured leaf
        rec = escape_dot(wrap_text(node['leaf-structured']['recommendation'], 30))
        nodes.append(f'    {node_id} [label="{rec}" shape=ellipse style=filled fillcolor=lightgreen];')


def render_tree(tree_data: dict, rankdir: str = 'TB') -> str:
    """Render full decision tree to Graphviz DOT format."""
    tree = tree_data['tree']
    tree_id = tree['id'].replace('-', '_')
    title = escape_dot(tree.get('title', 'Decision Tree'))

    lines = []
    nodes = []
    edges = []

    # Header comment
    lines.append(f'// Decision Tree: {title}')
    lines.append(f'// Generated from: {tree_id}')
    lines.append('')

    # Graph declaration
    lines.append('digraph G {')
    lines.append(f'    rankdir={rankdir};')
    lines.append('    node [fontname="Helvetica" fontsize=10];')
    lines.append('    edge [fontname="Helvetica" fontsize=9];')
    lines.append('')

    # Render all nodes
    render_node(tree['root'], tree_id, [], nodes, edges)

    # Add nodes section
    lines.append('    // Nodes')
    lines.extend(nodes)
    lines.append('')

    # Add edges section
    lines.append('    // Edges')
    lines.extend(edges)

    lines.append('}')
    lines.append('')  # POSIX newline

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Render decision tree YAML to Graphviz DOT format'
    )
    parser.add_argument('input_file', help='Input YAML file')
    parser.add_argument(
        '--rankdir', '-r',
        choices=['TB', 'BT', 'LR', 'RL'],
        default='TB',
        help='Graph direction (default: TB = top-bottom)'
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

    output = render_tree(tree_data, args.rankdir)
    print(output)


if __name__ == '__main__':
    main()
