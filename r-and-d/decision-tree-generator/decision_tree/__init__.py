"""
Decision Tree Generator Library

Deterministic, reproducible decision tree generation from YAML.

Usage:
    from decision_tree import load_tree, render_mermaid, render_html, render_graphviz

    tree = load_tree('my-tree.yaml')
    print(render_mermaid(tree))
    print(render_html(tree, full_page=True))
    print(render_graphviz(tree))
"""

from .loader import load_tree, validate_tree
from .mermaid import render_mermaid
from .graphviz import render_graphviz
from .html_details import render_html

__version__ = '0.1.0'
__all__ = [
    'load_tree',
    'validate_tree',
    'render_mermaid',
    'render_graphviz',
    'render_html',
]
