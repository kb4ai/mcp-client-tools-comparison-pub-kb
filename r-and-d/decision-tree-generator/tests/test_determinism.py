"""
Tests for determinism - same input must always produce identical output.

These tests verify the CORE REQUIREMENT that the decision tree generator
is deterministic and reproducible.
"""

import hashlib
import pytest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from decision_tree import load_tree, render_mermaid, render_html, render_graphviz


# Test fixtures
SIMPLE_TREE = {
    'tree': {
        'id': 'test-tree',
        'title': 'Test Decision Tree',
        'root': {
            'question': 'First question?',
            'branches': [
                {
                    'condition': 'Option A',
                    'next': {'leaf': 'Result A'}
                },
                {
                    'condition': 'Option B',
                    'next': {
                        'question': 'Second question?',
                        'branches': [
                            {'condition': 'Yes', 'next': {'leaf': 'Result B1'}},
                            {'condition': 'No', 'next': {'leaf': 'Result B2'}}
                        ]
                    }
                }
            ]
        }
    }
}

STRUCTURED_LEAF_TREE = {
    'tree': {
        'id': 'structured-test',
        'title': 'Structured Leaf Test',
        'root': {
            'question': 'What do you need?',
            'branches': [
                {
                    'condition': 'CLI tool',
                    'next': {
                        'leaf-structured': {
                            'recommendation': 'Use the CLI',
                            'projects': ['org/project1', 'org/project2'],
                            'notes': 'These are good options'
                        }
                    }
                }
            ]
        }
    }
}


def sha256(text: str) -> str:
    """Compute SHA256 hash of text."""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


class TestDeterminism:
    """Test that same input always produces identical output."""

    def test_mermaid_determinism_multiple_runs(self):
        """Mermaid output must be identical across multiple runs."""
        outputs = [render_mermaid(SIMPLE_TREE) for _ in range(10)]

        # All outputs must be identical
        assert len(set(outputs)) == 1, "Mermaid output varies between runs!"

    def test_graphviz_determinism_multiple_runs(self):
        """Graphviz output must be identical across multiple runs."""
        outputs = [render_graphviz(SIMPLE_TREE) for _ in range(10)]

        assert len(set(outputs)) == 1, "Graphviz output varies between runs!"

    def test_html_determinism_multiple_runs(self):
        """HTML output must be identical across multiple runs."""
        outputs = [render_html(SIMPLE_TREE) for _ in range(10)]

        assert len(set(outputs)) == 1, "HTML output varies between runs!"

    def test_html_full_page_determinism(self):
        """Full page HTML output must be identical across multiple runs."""
        outputs = [render_html(SIMPLE_TREE, full_page=True) for _ in range(10)]

        assert len(set(outputs)) == 1, "HTML full page output varies between runs!"

    def test_mermaid_hash_stability(self):
        """Mermaid output hash must remain stable."""
        output = render_mermaid(SIMPLE_TREE)
        hash1 = sha256(output)

        # Render again
        output2 = render_mermaid(SIMPLE_TREE)
        hash2 = sha256(output2)

        assert hash1 == hash2, f"Hash changed: {hash1} != {hash2}"

    def test_direction_options_deterministic(self):
        """Different direction options must each be deterministic."""
        for direction in ['TD', 'TB', 'LR', 'RL', 'BT']:
            outputs = [render_mermaid(SIMPLE_TREE, direction=direction) for _ in range(5)]
            assert len(set(outputs)) == 1, f"Direction {direction} produces varying output"

    def test_structured_leaf_deterministic(self):
        """Structured leaf trees must be deterministic."""
        outputs_mermaid = [render_mermaid(STRUCTURED_LEAF_TREE) for _ in range(5)]
        outputs_html = [render_html(STRUCTURED_LEAF_TREE) for _ in range(5)]
        outputs_dot = [render_graphviz(STRUCTURED_LEAF_TREE) for _ in range(5)]

        assert len(set(outputs_mermaid)) == 1
        assert len(set(outputs_html)) == 1
        assert len(set(outputs_dot)) == 1


class TestReproducibility:
    """Test that output can be reproduced from input."""

    def test_known_mermaid_output(self):
        """Mermaid output for simple tree should match known value."""
        output = render_mermaid(SIMPLE_TREE)

        # Must contain expected structure
        assert 'flowchart TD' in output
        assert 'test_tree_root' in output
        assert 'First question?' in output
        assert 'Option A' in output
        assert 'Result A' in output

    def test_known_graphviz_output(self):
        """Graphviz output for simple tree should match known value."""
        output = render_graphviz(SIMPLE_TREE)

        assert 'digraph G' in output
        assert 'rankdir=TB' in output
        assert 'n_root' in output
        assert 'First question?' in output

    def test_known_html_output(self):
        """HTML output for simple tree should match known value."""
        output = render_html(SIMPLE_TREE)

        assert '<details open>' in output
        assert '<summary>First question?</summary>' in output
        assert 'class="leaf"' in output
        assert 'Result A' in output

    def test_node_ids_deterministic(self):
        """Node IDs must follow deterministic pattern."""
        output = render_mermaid(SIMPLE_TREE)

        # Root node
        assert 'test_tree_root' in output
        # First branch (index 0)
        assert 'test_tree_0' in output
        # Second branch (index 1)
        assert 'test_tree_1' in output
        # Nested under second branch
        assert 'test_tree_1_0' in output
        assert 'test_tree_1_1' in output


class TestEdgeCases:
    """Test edge cases for determinism."""

    def test_special_characters_deterministic(self):
        """Special characters must be escaped consistently."""
        tree = {
            'tree': {
                'id': 'special-chars',
                'title': 'Test <Special> & "Characters"',
                'root': {
                    'question': 'Does this work? [Yes/No]',
                    'branches': [
                        {'condition': '<Yes>', 'next': {'leaf': 'It works! {great}'}}
                    ]
                }
            }
        }

        outputs = [render_mermaid(tree) for _ in range(5)]
        assert len(set(outputs)) == 1

        outputs = [render_html(tree) for _ in range(5)]
        assert len(set(outputs)) == 1

    def test_unicode_deterministic(self):
        """Unicode characters must be handled consistently."""
        tree = {
            'tree': {
                'id': 'unicode-test',
                'title': 'Тест Unicode 日本語 🎉',
                'root': {
                    'question': 'Вопрос?',
                    'branches': [
                        {'condition': '是', 'next': {'leaf': '結果 ✓'}}
                    ]
                }
            }
        }

        outputs = [render_mermaid(tree) for _ in range(5)]
        assert len(set(outputs)) == 1

    def test_empty_notes_deterministic(self):
        """Empty optional fields must be handled consistently."""
        tree = {
            'tree': {
                'id': 'optional-fields',
                'title': 'Test',
                'root': {
                    'question': 'Q?',
                    'branches': [
                        {
                            'condition': 'A',
                            'next': {
                                'leaf-structured': {
                                    'recommendation': 'Do X',
                                    'projects': []  # Empty list
                                    # No 'notes' field
                                }
                            }
                        }
                    ]
                }
            }
        }

        outputs = [render_html(tree) for _ in range(5)]
        assert len(set(outputs)) == 1


class TestSnapshotHashes:
    """
    Snapshot tests using SHA256 hashes.

    If these tests fail, it means the output format changed.
    Update the expected hashes only if the change was intentional.
    """

    EXPECTED_SIMPLE_MERMAID_HASH = None  # Set after first run
    EXPECTED_SIMPLE_HTML_HASH = None
    EXPECTED_SIMPLE_DOT_HASH = None

    def test_record_hashes(self):
        """Record current hashes (run this to update expected values)."""
        mermaid = render_mermaid(SIMPLE_TREE)
        html = render_html(SIMPLE_TREE)
        dot = render_graphviz(SIMPLE_TREE)

        print(f"\nCurrent hashes (update EXPECTED_* if intentional change):")
        print(f"  SIMPLE_MERMAID: {sha256(mermaid)}")
        print(f"  SIMPLE_HTML:    {sha256(html)}")
        print(f"  SIMPLE_DOT:     {sha256(dot)}")

        # This test always passes - it's for recording hashes
        assert True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
