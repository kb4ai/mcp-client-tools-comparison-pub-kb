"""
Tests for individual renderers.
"""

import pytest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from decision_tree import render_mermaid, render_html, render_graphviz


SAMPLE_TREE = {
    'tree': {
        'id': 'sample-tree',
        'title': 'Sample Decision Tree',
        'root': {
            'question': 'First question?',
            'branches': [
                {'condition': 'Yes', 'next': {'leaf': 'Do this'}},
                {'condition': 'No', 'next': {'leaf': 'Do that'}}
            ]
        }
    }
}


class TestMermaidRenderer:
    """Test Mermaid renderer."""

    def test_basic_output(self):
        """Should produce valid Mermaid syntax."""
        output = render_mermaid(SAMPLE_TREE)

        assert output.startswith('%% Decision Tree:')
        assert 'flowchart TD' in output

    def test_direction_td(self):
        """TD direction should be included."""
        output = render_mermaid(SAMPLE_TREE, direction='TD')
        assert 'flowchart TD' in output

    def test_direction_lr(self):
        """LR direction should be included."""
        output = render_mermaid(SAMPLE_TREE, direction='LR')
        assert 'flowchart LR' in output

    def test_question_nodes_square_brackets(self):
        """Question nodes should use square brackets."""
        output = render_mermaid(SAMPLE_TREE)
        assert '["First question?"]' in output

    def test_leaf_nodes_round_brackets(self):
        """Leaf nodes should use round brackets."""
        output = render_mermaid(SAMPLE_TREE)
        assert '("Do this")' in output
        assert '("Do that")' in output

    def test_edges_have_conditions(self):
        """Edges should have condition labels."""
        output = render_mermaid(SAMPLE_TREE)
        assert '-->|"Yes"|' in output
        assert '-->|"No"|' in output

    def test_ends_with_newline(self):
        """Output should end with newline (POSIX)."""
        output = render_mermaid(SAMPLE_TREE)
        assert output.endswith('\n')


class TestGraphvizRenderer:
    """Test Graphviz DOT renderer."""

    def test_basic_output(self):
        """Should produce valid DOT syntax."""
        output = render_graphviz(SAMPLE_TREE)

        assert output.startswith('//')
        assert 'digraph G {' in output
        assert output.rstrip().endswith('}')

    def test_rankdir_tb(self):
        """TB rankdir should be included."""
        output = render_graphviz(SAMPLE_TREE, rankdir='TB')
        assert 'rankdir=TB' in output

    def test_rankdir_lr(self):
        """LR rankdir should be included."""
        output = render_graphviz(SAMPLE_TREE, rankdir='LR')
        assert 'rankdir=LR' in output

    def test_question_nodes_box_shape(self):
        """Question nodes should be boxes."""
        output = render_graphviz(SAMPLE_TREE)
        assert 'shape=box' in output

    def test_leaf_nodes_ellipse_shape(self):
        """Leaf nodes should be ellipses."""
        output = render_graphviz(SAMPLE_TREE)
        assert 'shape=ellipse' in output

    def test_leaf_nodes_green_fill(self):
        """Leaf nodes should have green fill."""
        output = render_graphviz(SAMPLE_TREE)
        assert 'fillcolor=lightgreen' in output


class TestHtmlRenderer:
    """Test HTML <details> renderer."""

    def test_basic_output(self):
        """Should produce valid HTML structure."""
        output = render_html(SAMPLE_TREE)

        assert '<!-- Decision Tree:' in output
        assert '<section class="decision-tree"' in output
        assert '</section>' in output

    def test_root_details_open(self):
        """Root details should be open."""
        output = render_html(SAMPLE_TREE)
        assert '<details open>' in output

    def test_summary_contains_question(self):
        """Summary should contain question text."""
        output = render_html(SAMPLE_TREE)
        assert '<summary>First question?</summary>' in output

    def test_leaf_class(self):
        """Leaves should have leaf class."""
        output = render_html(SAMPLE_TREE)
        assert 'class="leaf"' in output

    def test_full_page_doctype(self):
        """Full page should have DOCTYPE."""
        output = render_html(SAMPLE_TREE, full_page=True)
        assert '<!DOCTYPE html>' in output

    def test_full_page_has_style(self):
        """Full page should have style block."""
        output = render_html(SAMPLE_TREE, full_page=True)
        assert '<style>' in output
        assert '.decision-tree' in output

    def test_full_page_has_title(self):
        """Full page should have title."""
        output = render_html(SAMPLE_TREE, full_page=True)
        assert '<title>Sample Decision Tree</title>' in output


class TestStructuredLeaf:
    """Test structured leaf rendering."""

    STRUCTURED_TREE = {
        'tree': {
            'id': 'struct-test',
            'title': 'Test',
            'root': {
                'question': 'Q?',
                'branches': [
                    {
                        'condition': 'A',
                        'next': {
                            'leaf-structured': {
                                'recommendation': 'Use tool X',
                                'projects': ['org/project1', 'org/project2'],
                                'notes': 'Additional info here'
                            }
                        }
                    }
                ]
            }
        }
    }

    def test_mermaid_shows_recommendation(self):
        """Mermaid should show recommendation text."""
        output = render_mermaid(self.STRUCTURED_TREE)
        assert 'Use tool X' in output

    def test_html_shows_projects(self):
        """HTML should show project list."""
        output = render_html(self.STRUCTURED_TREE)
        assert 'org/project1' in output
        assert 'org/project2' in output
        assert '<ul class="projects">' in output

    def test_html_shows_notes(self):
        """HTML should show notes."""
        output = render_html(self.STRUCTURED_TREE)
        assert 'Additional info here' in output
        assert 'class="notes"' in output


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
