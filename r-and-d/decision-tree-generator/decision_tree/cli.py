"""
Command-line interface for decision tree renderers.

These functions are entry points for pip-installed commands:
  dt-mermaid  - Render to Mermaid
  dt-graphviz - Render to Graphviz DOT
  dt-html     - Render to HTML
"""

import sys
import argparse
from pathlib import Path

from .loader import load_tree
from .mermaid import render_mermaid
from .graphviz import render_graphviz
from .html_details import render_html


def mermaid_main():
    """Entry point for dt-mermaid command."""
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
    parser.add_argument(
        '--output', '-o',
        help='Output file (default: stdout)'
    )

    args = parser.parse_args()

    try:
        tree = load_tree(Path(args.input_file))
        output = render_mermaid(tree, direction=args.direction)

        if args.output:
            Path(args.output).write_text(output)
        else:
            print(output)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def graphviz_main():
    """Entry point for dt-graphviz command."""
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
    parser.add_argument(
        '--output', '-o',
        help='Output file (default: stdout)'
    )

    args = parser.parse_args()

    try:
        tree = load_tree(Path(args.input_file))
        output = render_graphviz(tree, rankdir=args.rankdir)

        if args.output:
            Path(args.output).write_text(output)
        else:
            print(output)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def html_main():
    """Entry point for dt-html command."""
    parser = argparse.ArgumentParser(
        description='Render decision tree YAML to HTML with <details> elements'
    )
    parser.add_argument('input_file', help='Input YAML file')
    parser.add_argument(
        '--full-page', '-f',
        action='store_true',
        help='Generate full HTML page with styling (default: fragment only)'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output file (default: stdout)'
    )

    args = parser.parse_args()

    try:
        tree = load_tree(Path(args.input_file))
        output = render_html(tree, full_page=args.full_page)

        if args.output:
            Path(args.output).write_text(output)
        else:
            print(output)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
