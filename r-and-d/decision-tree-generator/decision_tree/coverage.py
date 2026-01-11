"""
Decision tree coverage analysis.

Finds all paths leading to each item in a decision tree,
and identifies items not covered by the tree.
"""

from typing import List, Dict, Set, Tuple, Optional


def extract_referenced_items(node: dict, path: List[str] = None) -> Dict[str, List[List[str]]]:
    """
    Extract all items referenced in leaf nodes and their paths.

    Args:
        node: Decision tree node
        path: Current path of conditions leading to this node

    Returns:
        Dict mapping item names to list of paths (each path is list of conditions)
    """
    if path is None:
        path = []

    items = {}

    if 'question' in node:
        for branch in node.get('branches', []):
            condition = branch['condition']
            child_path = path + [condition]
            child_items = extract_referenced_items(branch['next'], child_path)

            # Merge child items
            for item, paths in child_items.items():
                if item not in items:
                    items[item] = []
                items[item].extend(paths)

    elif 'leaf' in node:
        # Simple leaf - extract item name from text
        leaf_text = node['leaf']
        items[leaf_text] = [path.copy()]

    elif 'leaf-structured' in node:
        # Structured leaf - extract project names
        ls = node['leaf-structured']
        for project in ls.get('projects', []):
            if project not in items:
                items[project] = []
            items[project].append(path.copy())

        # Also track the recommendation text
        rec = ls.get('recommendation', '')
        if rec:
            if rec not in items:
                items[rec] = []
            items[rec].append(path.copy())

    return items


def find_paths_to_item(tree_data: dict, item: str) -> List[List[str]]:
    """
    Find all paths in the decision tree that lead to a specific item.

    Args:
        tree_data: Tree dict with 'tree' key
        item: Item name to search for (project name, recommendation text, etc.)

    Returns:
        List of paths, where each path is a list of condition strings
    """
    root = tree_data['tree']['root']
    all_items = extract_referenced_items(root)

    # Exact match
    if item in all_items:
        return all_items[item]

    # Partial match (item contained in key)
    for key, paths in all_items.items():
        if item in key or key in item:
            return paths

    return []


def check_coverage(tree_data: dict, required_items: List[str]) -> Dict[str, any]:
    """
    Check which required items are covered by the decision tree.

    Args:
        tree_data: Tree dict with 'tree' key
        required_items: List of item names that should be reachable

    Returns:
        Dict with:
            'covered': Dict[item, List[paths]] - items found with their paths
            'missing': List[item] - items not found in tree
            'tree_items': Set[str] - all items referenced in tree
    """
    root = tree_data['tree']['root']
    tree_items_dict = extract_referenced_items(root)
    tree_items = set(tree_items_dict.keys())

    covered = {}
    missing = []

    for item in required_items:
        # Try exact match first
        if item in tree_items_dict:
            covered[item] = tree_items_dict[item]
            continue

        # Try partial match (item as substring)
        found = False
        for tree_item, paths in tree_items_dict.items():
            if item in tree_item or tree_item in item:
                covered[item] = paths
                found = True
                break

        if not found:
            missing.append(item)

    return {
        'covered': covered,
        'missing': missing,
        'tree_items': tree_items,
        'coverage_percent': len(covered) / len(required_items) * 100 if required_items else 100
    }


def format_path(path: List[str], separator: str = ' → ') -> str:
    """Format a path as a readable string."""
    if not path:
        return "(root)"
    return separator.join(path)


def generate_coverage_report(
    tree_data: dict,
    required_items: List[str],
    verbose: bool = False
) -> Tuple[List[str], bool]:
    """
    Generate a coverage report with warning lines.

    Args:
        tree_data: Tree dict with 'tree' key
        required_items: List of item names that should be reachable
        verbose: If True, also report covered items

    Returns:
        Tuple of (list of report lines, all_covered bool)
    """
    result = check_coverage(tree_data, required_items)
    lines = []

    if result['missing']:
        for item in sorted(result['missing']):
            lines.append(f"WARNING: Item not in decision tree: {item}")

    if verbose:
        lines.append("")
        lines.append(f"Coverage: {result['coverage_percent']:.1f}% ({len(result['covered'])}/{len(required_items)})")
        lines.append("")
        lines.append("Covered items:")
        for item, paths in sorted(result['covered'].items()):
            path_str = format_path(paths[0]) if paths else "(unknown)"
            lines.append(f"  ✓ {item}")
            lines.append(f"    Path: {path_str}")

    all_covered = len(result['missing']) == 0

    return lines, all_covered


def get_all_tree_items(tree_data: dict) -> Set[str]:
    """Get all items (projects, recommendations) referenced in the tree."""
    root = tree_data['tree']['root']
    items_dict = extract_referenced_items(root)
    return set(items_dict.keys())


def get_all_tree_projects(tree_data: dict) -> Set[str]:
    """Get all project names (org/repo format) referenced in the tree."""
    all_items = get_all_tree_items(tree_data)
    # Filter to items that look like project names (contain /)
    return {item for item in all_items if '/' in item}
