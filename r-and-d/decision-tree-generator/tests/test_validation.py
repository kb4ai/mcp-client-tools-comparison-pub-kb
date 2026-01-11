"""
Tests for tree validation.
"""

import pytest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from decision_tree import load_tree, validate_tree


class TestValidation:
    """Test tree structure validation."""

    def test_valid_simple_tree(self):
        """Valid simple tree should pass validation."""
        tree = {
            'tree': {
                'id': 'test',
                'title': 'Test',
                'root': {
                    'question': 'Q?',
                    'branches': [
                        {'condition': 'A', 'next': {'leaf': 'Result'}}
                    ]
                }
            }
        }
        # Should not raise
        validate_tree(tree)

    def test_missing_tree_key(self):
        """Missing 'tree' key should fail."""
        with pytest.raises(ValueError, match="Missing 'tree' key"):
            validate_tree({'not-tree': {}})

    def test_missing_id(self):
        """Missing 'id' should fail."""
        with pytest.raises(ValueError, match="missing required 'id'"):
            validate_tree({
                'tree': {
                    'title': 'Test',
                    'root': {'leaf': 'X'}
                }
            })

    def test_missing_root(self):
        """Missing 'root' should fail."""
        with pytest.raises(ValueError, match="missing required 'root'"):
            validate_tree({
                'tree': {
                    'id': 'test',
                    'title': 'Test'
                }
            })

    def test_node_must_have_one_type(self):
        """Node must have exactly one of: question, leaf, leaf-structured."""
        # No type
        with pytest.raises(ValueError, match="must have exactly one of"):
            validate_tree({
                'tree': {
                    'id': 'test',
                    'root': {'invalid': 'field'}
                }
            })

        # Multiple types
        with pytest.raises(ValueError, match="must have exactly one of"):
            validate_tree({
                'tree': {
                    'id': 'test',
                    'root': {
                        'question': 'Q?',
                        'leaf': 'X'  # Can't have both!
                    }
                }
            })

    def test_question_needs_branches(self):
        """Question node must have branches."""
        with pytest.raises(ValueError, match="missing 'branches'"):
            validate_tree({
                'tree': {
                    'id': 'test',
                    'root': {'question': 'Q?'}  # No branches
                }
            })

    def test_branch_needs_condition(self):
        """Branch must have condition."""
        with pytest.raises(ValueError, match="missing 'condition'"):
            validate_tree({
                'tree': {
                    'id': 'test',
                    'root': {
                        'question': 'Q?',
                        'branches': [
                            {'next': {'leaf': 'X'}}  # No condition
                        ]
                    }
                }
            })

    def test_branch_needs_next(self):
        """Branch must have next."""
        with pytest.raises(ValueError, match="missing 'next'"):
            validate_tree({
                'tree': {
                    'id': 'test',
                    'root': {
                        'question': 'Q?',
                        'branches': [
                            {'condition': 'A'}  # No next
                        ]
                    }
                }
            })

    def test_nested_validation(self):
        """Validation must recurse into nested nodes."""
        # Invalid node deep in tree
        with pytest.raises(ValueError, match="must have exactly one of"):
            validate_tree({
                'tree': {
                    'id': 'test',
                    'root': {
                        'question': 'Q1?',
                        'branches': [
                            {
                                'condition': 'A',
                                'next': {
                                    'question': 'Q2?',
                                    'branches': [
                                        {
                                            'condition': 'B',
                                            'next': {'invalid': 'X'}  # Bad node!
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                }
            })


class TestLoader:
    """Test tree loading."""

    def test_load_from_dict(self):
        """Should load from dict directly."""
        tree_data = {
            'tree': {
                'id': 'test',
                'root': {'leaf': 'X'}
            }
        }
        loaded = load_tree(tree_data)
        assert loaded == tree_data

    def test_load_from_yaml_string(self):
        """Should load from YAML string."""
        yaml_str = """
tree:
  id: test
  root:
    leaf: Result
"""
        loaded = load_tree(yaml_str)
        assert loaded['tree']['id'] == 'test'
        assert loaded['tree']['root']['leaf'] == 'Result'

    def test_load_validates(self):
        """Loading should validate the tree."""
        with pytest.raises(ValueError):
            load_tree({'tree': {'id': 'test'}})  # Missing root


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
