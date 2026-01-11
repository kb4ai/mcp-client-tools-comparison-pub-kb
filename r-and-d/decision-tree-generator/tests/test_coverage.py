"""
Unit tests for decision tree coverage analysis.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from decision_tree import (
    load_tree,
    extract_referenced_items,
    find_paths_to_item,
    check_coverage,
    generate_coverage_report,
    get_all_tree_items,
    get_all_tree_projects,
)

# Sample tree for testing
SAMPLE_TREE = {
    'tree': {
        'id': 'test-tree',
        'title': 'Test Decision Tree',
        'root': {
            'question': 'What do you need?',
            'branches': [
                {
                    'condition': 'Option A',
                    'next': {
                        'leaf': 'Use tool-a/project'
                    }
                },
                {
                    'condition': 'Option B',
                    'next': {
                        'question': 'More specific?',
                        'branches': [
                            {
                                'condition': 'Sub B1',
                                'next': {
                                    'leaf-structured': {
                                        'recommendation': 'Use B1 tools',
                                        'projects': ['org/b1-main', 'org/b1-alt'],
                                        'notes': 'B1 is recommended'
                                    }
                                }
                            },
                            {
                                'condition': 'Sub B2',
                                'next': {
                                    'leaf': 'Use org/b2-tool'
                                }
                            }
                        ]
                    }
                },
                {
                    'condition': 'Option C',
                    'next': {
                        'leaf-structured': {
                            'recommendation': 'Use C tools',
                            'projects': ['org/c-project'],
                        }
                    }
                }
            ]
        }
    }
}


def test_extract_referenced_items():
    """Test extracting all items from tree."""
    root = SAMPLE_TREE['tree']['root']
    items = extract_referenced_items(root)

    # Should find all leaf texts and project names
    assert 'Use tool-a/project' in items
    assert 'org/b1-main' in items
    assert 'org/b1-alt' in items
    assert 'Use B1 tools' in items
    assert 'Use org/b2-tool' in items
    assert 'org/c-project' in items
    assert 'Use C tools' in items

    # Each item should have path(s)
    assert len(items['org/b1-main']) == 1
    assert items['org/b1-main'][0] == ['Option B', 'Sub B1']


def test_extract_paths_correct():
    """Test that paths are correctly extracted."""
    root = SAMPLE_TREE['tree']['root']
    items = extract_referenced_items(root)

    # Tool A is at root level
    assert items['Use tool-a/project'][0] == ['Option A']

    # B2 is nested
    assert items['Use org/b2-tool'][0] == ['Option B', 'Sub B2']

    # C is at first level
    assert items['org/c-project'][0] == ['Option C']


def test_find_paths_to_item_exact():
    """Test finding paths to exact item match."""
    paths = find_paths_to_item(SAMPLE_TREE, 'org/b1-main')

    assert len(paths) == 1
    assert paths[0] == ['Option B', 'Sub B1']


def test_find_paths_to_item_partial():
    """Test finding paths with partial match."""
    paths = find_paths_to_item(SAMPLE_TREE, 'b1-main')

    # Should find via partial match
    assert len(paths) == 1


def test_find_paths_to_item_not_found():
    """Test that non-existent item returns empty list."""
    paths = find_paths_to_item(SAMPLE_TREE, 'nonexistent/project')

    assert paths == []


def test_check_coverage_all_covered():
    """Test coverage check when all items are covered."""
    required = ['org/b1-main', 'org/b1-alt', 'org/c-project']
    result = check_coverage(SAMPLE_TREE, required)

    assert len(result['missing']) == 0
    assert len(result['covered']) == 3
    assert result['coverage_percent'] == 100.0


def test_check_coverage_some_missing():
    """Test coverage check with missing items."""
    required = ['org/b1-main', 'missing/project', 'org/c-project']
    result = check_coverage(SAMPLE_TREE, required)

    assert 'missing/project' in result['missing']
    assert len(result['missing']) == 1
    assert len(result['covered']) == 2
    assert result['coverage_percent'] < 100


def test_check_coverage_partial_match():
    """Test coverage check with partial name matching."""
    # Use partial name that should match
    required = ['b1-main']  # Should match org/b1-main
    result = check_coverage(SAMPLE_TREE, required)

    # Should be covered via partial match
    assert len(result['covered']) == 1 or len(result['missing']) == 0


def test_generate_coverage_report_no_missing():
    """Test report generation with full coverage."""
    required = ['org/b1-main', 'org/c-project']
    lines, all_covered = generate_coverage_report(SAMPLE_TREE, required)

    assert all_covered is True
    # No WARNING lines for missing items
    warning_lines = [l for l in lines if l.startswith('WARNING')]
    assert len(warning_lines) == 0


def test_generate_coverage_report_with_missing():
    """Test report generation with missing items."""
    required = ['org/b1-main', 'missing/project', 'another/missing']
    lines, all_covered = generate_coverage_report(SAMPLE_TREE, required)

    assert all_covered is False
    # Should have WARNING lines
    warning_lines = [l for l in lines if l.startswith('WARNING')]
    assert len(warning_lines) == 2
    assert any('missing/project' in l for l in warning_lines)
    assert any('another/missing' in l for l in warning_lines)


def test_generate_coverage_report_verbose():
    """Test verbose report includes covered items."""
    required = ['org/b1-main', 'org/c-project']
    lines, all_covered = generate_coverage_report(SAMPLE_TREE, required, verbose=True)

    assert all_covered is True
    # Should include coverage stats and covered items
    assert any('Coverage:' in l for l in lines)
    assert any('org/b1-main' in l for l in lines)


def test_get_all_tree_items():
    """Test getting all items from tree."""
    items = get_all_tree_items(SAMPLE_TREE)

    assert isinstance(items, set)
    assert 'org/b1-main' in items
    assert 'org/c-project' in items


def test_get_all_tree_projects():
    """Test getting only project names (org/repo format)."""
    projects = get_all_tree_projects(SAMPLE_TREE)

    assert isinstance(projects, set)
    # Should only include items with /
    assert 'org/b1-main' in projects
    assert 'org/b1-alt' in projects
    assert 'org/c-project' in projects
    # Should NOT include plain text recommendations
    assert 'Use B1 tools' not in projects
    assert 'Use C tools' not in projects


def test_coverage_with_real_tree():
    """Test coverage with actual mcp-tool-chooser tree."""
    tree_path = Path(__file__).parent.parent / 'examples' / 'mcp-tool-chooser.yaml'
    if not tree_path.exists():
        print(f"Skipping real tree test - {tree_path} not found")
        return

    tree_data = load_tree(tree_path)

    # Get all projects from tree
    projects = get_all_tree_projects(tree_data)
    assert len(projects) > 0

    # All projects in tree should have 100% coverage against themselves
    result = check_coverage(tree_data, list(projects))
    assert result['coverage_percent'] == 100.0


def run_tests():
    """Run all tests and report results."""
    tests = [
        test_extract_referenced_items,
        test_extract_paths_correct,
        test_find_paths_to_item_exact,
        test_find_paths_to_item_partial,
        test_find_paths_to_item_not_found,
        test_check_coverage_all_covered,
        test_check_coverage_some_missing,
        test_check_coverage_partial_match,
        test_generate_coverage_report_no_missing,
        test_generate_coverage_report_with_missing,
        test_generate_coverage_report_verbose,
        test_get_all_tree_items,
        test_get_all_tree_projects,
        test_coverage_with_real_tree,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            print(f"  PASS: {test.__name__}")
            passed += 1
        except Exception as e:
            print(f"  FAIL: {test.__name__}: {e}")
            failed += 1

    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == '__main__':
    print("Running coverage module tests...\n")
    success = run_tests()
    sys.exit(0 if success else 1)
