"""
HTML <details>/<summary> renderer for decision trees.
"""

from html import escape as html_escape


def _render_node(node: dict, indent: int = 0, is_root: bool = False) -> list:
    """Recursively render a node to HTML lines."""
    prefix = '  ' * indent
    lines = []

    if 'question' in node:
        open_attr = ' open' if is_root else ''
        lines.append(f'{prefix}<details{open_attr}>')
        lines.append(f'{prefix}  <summary>{html_escape(node["question"])}</summary>')

        for branch in node.get('branches', []):
            condition = html_escape(branch['condition'])

            if 'leaf' in branch['next']:
                leaf = html_escape(branch['next']['leaf'])
                lines.append(f'{prefix}  <p class="leaf"><strong>{condition}</strong> → {leaf}</p>')

            elif 'leaf-structured' in branch['next']:
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
                lines.append(f'{prefix}  <details>')
                lines.append(f'{prefix}    <summary>{condition}</summary>')
                child_lines = _render_node(branch['next'], indent + 2)
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


DEFAULT_CSS = '''
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


def render_html(tree_data: dict, full_page: bool = False, css: str = None) -> str:
    """
    Render decision tree to HTML with <details>/<summary> elements.

    Args:
        tree_data: Tree dict with 'tree' key
        full_page: If True, generate full HTML page with styling
        css: Custom CSS (only used with full_page=True)

    Returns:
        HTML string
    """
    tree = tree_data['tree']
    title = html_escape(tree.get('title', 'Decision Tree'))
    tree_id = tree['id']

    lines = []
    lines.append(f'<!-- Decision Tree: {title} -->')
    lines.append(f'<section class="decision-tree" id="{tree_id}" aria-label="{title}">')

    node_lines = _render_node(tree['root'], indent=1, is_root=True)
    lines.extend(node_lines)

    lines.append('</section>')
    lines.append('')

    fragment = '\n'.join(lines)

    if not full_page:
        return fragment

    used_css = css or DEFAULT_CSS

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>{used_css}
  </style>
</head>
<body>
  <h1>{title}</h1>
{fragment}
</body>
</html>
'''
