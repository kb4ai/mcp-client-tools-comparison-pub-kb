"""
Graphviz DOT renderer for decision trees.
"""

from .loader import generate_node_id


def escape_dot(text: str) -> str:
    """Escape special characters for DOT labels."""
    text = text.replace('\\', '\\\\')
    text = text.replace('"', '\\"')
    text = text.replace('\n', '\\n')
    return text


def truncate(text: str, max_len: int = 40) -> str:
    """Truncate text with ellipsis."""
    if len(text) <= max_len:
        return text
    return text[:max_len - 3] + "..."


def wrap_text(text: str, width: int = 30) -> str:
    """Wrap text at word boundaries."""
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


def _render_node(node: dict, tree_id: str, path: list, nodes: list, edges: list) -> None:
    """Recursively render a node and its children."""
    node_id = generate_node_id(tree_id, path, sep='_')
    # Use shorter IDs for graphviz
    short_id = f"n_{'_'.join(map(str, path))}" if path else "n_root"

    if 'question' in node:
        question = escape_dot(wrap_text(node['question'], 25))
        nodes.append(f'    {short_id} [label="{question}" shape=box];')

        for i, branch in enumerate(node.get('branches', [])):
            child_path = path + [i]
            child_short = f"n_{'_'.join(map(str, child_path))}"
            condition = escape_dot(truncate(branch['condition'], 20))

            edges.append(f'    {short_id} -> {child_short} [label="{condition}"];')
            _render_node(branch['next'], tree_id, child_path, nodes, edges)

    elif 'leaf' in node:
        leaf = escape_dot(wrap_text(node['leaf'], 30))
        nodes.append(f'    {short_id} [label="{leaf}" shape=ellipse style=filled fillcolor=lightgreen];')

    elif 'leaf-structured' in node:
        rec = escape_dot(wrap_text(node['leaf-structured']['recommendation'], 30))
        nodes.append(f'    {short_id} [label="{rec}" shape=ellipse style=filled fillcolor=lightgreen];')


def render_graphviz(tree_data: dict, rankdir: str = 'TB') -> str:
    """
    Render decision tree to Graphviz DOT format.

    Args:
        tree_data: Tree dict with 'tree' key
        rankdir: Graph direction - TB (top-bottom), LR (left-right), etc.

    Returns:
        DOT format string
    """
    tree = tree_data['tree']
    tree_id = tree['id'].replace('-', '_')
    title = escape_dot(tree.get('title', 'Decision Tree'))

    lines = []
    nodes = []
    edges = []

    lines.append(f'// Decision Tree: {title}')
    lines.append(f'// Generated from: {tree_id}')
    lines.append('')
    lines.append('digraph G {')
    lines.append(f'    rankdir={rankdir};')
    lines.append('    node [fontname="Helvetica" fontsize=10];')
    lines.append('    edge [fontname="Helvetica" fontsize=9];')
    lines.append('')

    _render_node(tree['root'], tree_id, [], nodes, edges)

    lines.append('    // Nodes')
    lines.extend(nodes)
    lines.append('')
    lines.append('    // Edges')
    lines.extend(edges)
    lines.append('}')
    lines.append('')

    return '\n'.join(lines)
