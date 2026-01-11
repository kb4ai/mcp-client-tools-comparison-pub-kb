"""
Decision tree YAML loader and validator.
"""

from pathlib import Path
from typing import Union

try:
    import yaml
except ImportError:
    yaml = None


def load_tree(source: Union[str, Path, dict]) -> dict:
    """
    Load a decision tree from YAML file, string, or dict.

    Args:
        source: Path to YAML file, YAML string, or dict with tree structure

    Returns:
        Validated tree dict with 'tree' key

    Raises:
        ValueError: If tree structure is invalid
        ImportError: If PyYAML not installed
    """
    if yaml is None:
        raise ImportError("PyYAML not installed. Run: pip install pyyaml")

    if isinstance(source, dict):
        tree_data = source
    elif isinstance(source, Path) or (isinstance(source, str) and Path(source).exists()):
        with open(source) as f:
            tree_data = yaml.safe_load(f)
    else:
        # Assume it's a YAML string
        tree_data = yaml.safe_load(source)

    validate_tree(tree_data)
    return tree_data


def validate_tree(tree_data: dict) -> None:
    """
    Validate tree structure.

    Args:
        tree_data: Dict to validate

    Raises:
        ValueError: If structure is invalid
    """
    if not tree_data:
        raise ValueError("Empty tree data")

    if 'tree' not in tree_data:
        raise ValueError("Missing 'tree' key in tree data")

    tree = tree_data['tree']

    if 'id' not in tree:
        raise ValueError("Tree missing required 'id' field")

    if 'root' not in tree:
        raise ValueError("Tree missing required 'root' field")

    _validate_node(tree['root'], path=[])


def _validate_node(node: dict, path: list) -> None:
    """Recursively validate node structure."""
    path_str = '/'.join(map(str, path)) if path else 'root'

    if not isinstance(node, dict):
        raise ValueError(f"Node at {path_str} must be a dict")

    has_question = 'question' in node
    has_leaf = 'leaf' in node
    has_leaf_structured = 'leaf-structured' in node

    # Must have exactly one of: question, leaf, leaf-structured
    node_types = sum([has_question, has_leaf, has_leaf_structured])
    if node_types != 1:
        raise ValueError(
            f"Node at {path_str} must have exactly one of: question, leaf, leaf-structured"
        )

    if has_question:
        if 'branches' not in node:
            raise ValueError(f"Question node at {path_str} missing 'branches'")

        for i, branch in enumerate(node['branches']):
            if 'condition' not in branch:
                raise ValueError(f"Branch {i} at {path_str} missing 'condition'")
            if 'next' not in branch:
                raise ValueError(f"Branch {i} at {path_str} missing 'next'")

            _validate_node(branch['next'], path + [i])


def generate_node_id(tree_id: str, path: list, sep: str = '_') -> str:
    """
    Generate deterministic node ID from tree ID and branch path.

    Args:
        tree_id: The tree's unique identifier
        path: List of branch indices from root
        sep: Separator character (default '_' for most formats)

    Returns:
        Deterministic ID like "mytree_0_1_0"
    """
    safe_id = tree_id.replace('-', sep)
    if not path:
        return f"{safe_id}{sep}root"
    return f"{safe_id}{sep}{sep.join(map(str, path))}"
