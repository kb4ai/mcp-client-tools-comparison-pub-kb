"""
Mermaid flowchart renderer for decision trees.
"""

from .loader import generate_node_id


def escape_mermaid(text: str) -> str:
    """Escape special characters for Mermaid labels."""
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


def _render_node(node: dict, tree_id: str, path: list, lines: list) -> None:
    """Recursively render a node and its children."""
    node_id = generate_node_id(tree_id, path)

    if 'question' in node:
        question = escape_mermaid(truncate(node['question']))
        lines.append(f'    {node_id}["{question}"]')

        for i, branch in enumerate(node.get('branches', [])):
            child_path = path + [i]
            child_id = generate_node_id(tree_id, child_path)
            condition = escape_mermaid(truncate(branch['condition'], 25))

            lines.append(f'    {node_id} -->|"{condition}"| {child_id}')
            _render_node(branch['next'], tree_id, child_path, lines)

    elif 'leaf' in node:
        leaf = escape_mermaid(truncate(node['leaf'], 50))
        lines.append(f'    {node_id}("{leaf}")')

    elif 'leaf-structured' in node:
        rec = escape_mermaid(truncate(node['leaf-structured']['recommendation'], 50))
        lines.append(f'    {node_id}("{rec}")')


def render_mermaid(tree_data: dict, direction: str = 'TD') -> str:
    """
    Render decision tree to Mermaid flowchart format.

    Args:
        tree_data: Tree dict with 'tree' key
        direction: Flowchart direction - TD (top-down), LR (left-right), etc.

    Returns:
        Mermaid flowchart as string
    """
    tree = tree_data['tree']
    tree_id = tree['id'].replace('-', '_')
    title = tree.get('title', 'Decision Tree')

    lines = []
    lines.append(f'%% Decision Tree: {title}')
    lines.append(f'%% Generated from: {tree_id}')
    lines.append('')
    lines.append(f'flowchart {direction}')

    _render_node(tree['root'], tree_id, [], lines)

    lines.append('')
    return '\n'.join(lines)


def render_mermaid_split(tree_data: dict, direction: str = 'TD') -> dict:
    """
    Render decision tree as multiple smaller Mermaid diagrams.

    Splits the tree at the root level:
    - 'overview': Root question with first-level children (as clickable links)
    - 'sections': Dict of subtrees, one per first-level branch

    Args:
        tree_data: Tree dict with 'tree' key
        direction: Flowchart direction

    Returns:
        Dict with 'overview' (str) and 'sections' (list of dicts with
        'id', 'title', 'condition', 'mermaid' keys)
    """
    tree = tree_data['tree']
    tree_id = tree['id'].replace('-', '_')
    title = tree.get('title', 'Decision Tree')
    root = tree['root']

    if 'question' not in root:
        # Not a question node, can't split
        return {
            'overview': render_mermaid(tree_data, direction),
            'sections': []
        }

    # Build overview diagram (root + first-level children as terminals)
    overview_lines = []
    overview_lines.append(f'%% Overview: {title}')
    overview_lines.append('')
    overview_lines.append(f'flowchart {direction}')

    root_id = f'{tree_id}_root'
    root_question = escape_mermaid(truncate(root['question']))
    overview_lines.append(f'    {root_id}["{root_question}"]')

    sections = []

    for i, branch in enumerate(root.get('branches', [])):
        condition = branch['condition']
        condition_escaped = escape_mermaid(truncate(condition, 30))
        child_id = f'{tree_id}_{i}'
        section_id = f'section-{i}'

        # In overview, show children as rounded boxes (clickable targets)
        overview_lines.append(f'    {root_id} -->|"{condition_escaped}"| {child_id}')
        overview_lines.append(f'    {child_id}("{condition_escaped}")')
        overview_lines.append(f'    click {child_id} "#{section_id}"')

        # Build subtree diagram for this branch
        subtree_lines = []
        subtree_lines.append(f'%% Subtree: {condition}')
        subtree_lines.append('')
        subtree_lines.append(f'flowchart {direction}')

        _render_node(branch['next'], tree_id, [i], subtree_lines)

        subtree_lines.append('')

        sections.append({
            'id': section_id,
            'index': i,
            'condition': condition,
            'title': condition,
            'mermaid': '\n'.join(subtree_lines)
        })

    overview_lines.append('')

    return {
        'overview': '\n'.join(overview_lines),
        'sections': sections
    }
