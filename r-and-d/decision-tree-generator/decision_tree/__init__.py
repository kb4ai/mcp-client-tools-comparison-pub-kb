"""
Decision Tree Generator Library

Deterministic, reproducible decision tree generation from YAML.

Usage:
    from decision_tree import load_tree, render_mermaid, render_html, render_graphviz

    tree = load_tree('my-tree.yaml')
    print(render_mermaid(tree))
    print(render_html(tree, full_page=True))
    print(render_graphviz(tree))

    # Split large trees into multiple smaller diagrams
    from decision_tree import render_mermaid_split
    split = render_mermaid_split(tree)
    print(split['overview'])  # Root + first-level children
    for section in split['sections']:
        print(f"## {section['title']}")
        print(section['mermaid'])
"""

from .loader import load_tree, validate_tree
from .mermaid import render_mermaid, render_mermaid_split
from .graphviz import render_graphviz
from .html_details import render_html
from .coverage import (
    extract_referenced_items,
    find_paths_to_item,
    check_coverage,
    generate_coverage_report,
    get_all_tree_items,
    get_all_tree_projects,
)

__version__ = '0.2.1'
__all__ = [
    'load_tree',
    'validate_tree',
    'render_mermaid',
    'render_mermaid_split',
    'render_graphviz',
    'render_html',
    # Coverage analysis
    'extract_referenced_items',
    'find_paths_to_item',
    'check_coverage',
    'generate_coverage_report',
    'get_all_tree_items',
    'get_all_tree_projects',
]
