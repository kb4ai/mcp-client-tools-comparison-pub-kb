#!/usr/bin/env python3
"""
Standalone test runner that doesn't require pytest.
Runs basic tests for determinism and validation.
"""

import sys
import hashlib
from pathlib import Path

# Add decision_tree to path
sys.path.insert(0, str(Path(__file__).parent))

from decision_tree import (
    load_tree, validate_tree, render_mermaid, render_html, render_graphviz,
    extract_referenced_items, find_paths_to_item, check_coverage,
    generate_coverage_report, get_all_tree_items, get_all_tree_projects,
)


def sha256(text: str) -> str:
    """Compute SHA256 hash of text."""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


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


def test_determinism():
    """Test that same input produces identical output."""
    print("Testing determinism...")

    # Test Mermaid
    outputs = [render_mermaid(SIMPLE_TREE) for _ in range(10)]
    assert len(set(outputs)) == 1, "FAIL: Mermaid output varies!"
    print("  ✓ Mermaid: 10 runs identical")

    # Test Graphviz
    outputs = [render_graphviz(SIMPLE_TREE) for _ in range(10)]
    assert len(set(outputs)) == 1, "FAIL: Graphviz output varies!"
    print("  ✓ Graphviz: 10 runs identical")

    # Test HTML
    outputs = [render_html(SIMPLE_TREE) for _ in range(10)]
    assert len(set(outputs)) == 1, "FAIL: HTML output varies!"
    print("  ✓ HTML: 10 runs identical")

    # Test HTML full page
    outputs = [render_html(SIMPLE_TREE, full_page=True) for _ in range(10)]
    assert len(set(outputs)) == 1, "FAIL: HTML full page output varies!"
    print("  ✓ HTML full page: 10 runs identical")


def test_hash_stability():
    """Test that output hashes remain stable."""
    print("Testing hash stability...")

    mermaid1 = render_mermaid(SIMPLE_TREE)
    mermaid2 = render_mermaid(SIMPLE_TREE)
    assert sha256(mermaid1) == sha256(mermaid2), "FAIL: Mermaid hash changed!"
    print(f"  ✓ Mermaid hash: {sha256(mermaid1)[:16]}...")

    html1 = render_html(SIMPLE_TREE)
    html2 = render_html(SIMPLE_TREE)
    assert sha256(html1) == sha256(html2), "FAIL: HTML hash changed!"
    print(f"  ✓ HTML hash: {sha256(html1)[:16]}...")

    dot1 = render_graphviz(SIMPLE_TREE)
    dot2 = render_graphviz(SIMPLE_TREE)
    assert sha256(dot1) == sha256(dot2), "FAIL: DOT hash changed!"
    print(f"  ✓ DOT hash: {sha256(dot1)[:16]}...")


def test_validation():
    """Test tree validation."""
    print("Testing validation...")

    # Valid tree should pass
    validate_tree(SIMPLE_TREE)
    print("  ✓ Valid tree passes")

    # Missing 'tree' key
    try:
        validate_tree({'not-tree': {}})
        print("  ✗ FAIL: Should reject missing 'tree' key")
    except ValueError:
        print("  ✓ Rejects missing 'tree' key")

    # Missing 'id'
    try:
        validate_tree({'tree': {'root': {'leaf': 'X'}}})
        print("  ✗ FAIL: Should reject missing 'id'")
    except ValueError:
        print("  ✓ Rejects missing 'id'")

    # Missing 'root'
    try:
        validate_tree({'tree': {'id': 'test'}})
        print("  ✗ FAIL: Should reject missing 'root'")
    except ValueError:
        print("  ✓ Rejects missing 'root'")

    # Question without branches
    try:
        validate_tree({'tree': {'id': 'test', 'root': {'question': 'Q?'}}})
        print("  ✗ FAIL: Should reject question without branches")
    except ValueError:
        print("  ✓ Rejects question without branches")


def test_output_content():
    """Test that output contains expected content."""
    print("Testing output content...")

    # Mermaid
    mermaid = render_mermaid(SIMPLE_TREE)
    assert 'flowchart TD' in mermaid, "FAIL: Missing flowchart declaration"
    assert 'First question?' in mermaid, "FAIL: Missing question text"
    assert 'Result A' in mermaid, "FAIL: Missing leaf text"
    print("  ✓ Mermaid contains expected content")

    # Graphviz
    dot = render_graphviz(SIMPLE_TREE)
    assert 'digraph G' in dot, "FAIL: Missing digraph declaration"
    assert 'shape=box' in dot, "FAIL: Missing question shape"
    assert 'shape=ellipse' in dot, "FAIL: Missing leaf shape"
    print("  ✓ Graphviz contains expected content")

    # HTML
    html = render_html(SIMPLE_TREE)
    assert '<details open>' in html, "FAIL: Missing open details"
    assert '<summary>' in html, "FAIL: Missing summary"
    assert 'class="leaf"' in html, "FAIL: Missing leaf class"
    print("  ✓ HTML contains expected content")


def test_example_files():
    """Test loading and rendering example files."""
    print("Testing example files...")

    examples_dir = Path(__file__).parent / 'examples'

    for yaml_file in examples_dir.glob('*.yaml'):
        tree = load_tree(yaml_file)

        # Render all formats
        mermaid = render_mermaid(tree)
        html = render_html(tree)
        dot = render_graphviz(tree)

        # Basic sanity checks
        assert len(mermaid) > 100, f"FAIL: {yaml_file.name} Mermaid too short"
        assert len(html) > 100, f"FAIL: {yaml_file.name} HTML too short"
        assert len(dot) > 100, f"FAIL: {yaml_file.name} DOT too short"

        print(f"  ✓ {yaml_file.name}")


def test_coverage_functions():
    """Test coverage analysis functions."""
    print("Testing coverage functions...")

    # Extract items from simple tree
    root = SIMPLE_TREE['tree']['root']
    items = extract_referenced_items(root)
    assert 'Result A' in items, "FAIL: Missing Result A"
    assert 'Result B1' in items, "FAIL: Missing Result B1"
    assert 'Result B2' in items, "FAIL: Missing Result B2"
    print("  ✓ extract_referenced_items finds all leaves")

    # Paths are correct
    assert items['Result A'][0] == ['Option A'], f"FAIL: Wrong path for Result A: {items['Result A']}"
    assert items['Result B1'][0] == ['Option B', 'Yes'], f"FAIL: Wrong path for Result B1"
    print("  ✓ Paths are correctly extracted")

    # find_paths_to_item
    paths = find_paths_to_item(SIMPLE_TREE, 'Result B2')
    assert len(paths) == 1, "FAIL: Should find one path"
    assert paths[0] == ['Option B', 'No'], "FAIL: Wrong path"
    print("  ✓ find_paths_to_item works")

    # check_coverage - all covered
    required = ['Result A', 'Result B1']
    result = check_coverage(SIMPLE_TREE, required)
    assert result['coverage_percent'] == 100.0, "FAIL: Should be 100% covered"
    assert len(result['missing']) == 0, "FAIL: Should have no missing"
    print("  ✓ check_coverage reports 100% when all covered")

    # check_coverage - some missing
    required = ['Result A', 'Nonexistent']
    result = check_coverage(SIMPLE_TREE, required)
    assert 'Nonexistent' in result['missing'], "FAIL: Should detect missing item"
    assert result['coverage_percent'] == 50.0, "FAIL: Should be 50% covered"
    print("  ✓ check_coverage detects missing items")

    # generate_coverage_report
    required = ['Result A', 'Missing1', 'Missing2']
    lines, all_covered = generate_coverage_report(SIMPLE_TREE, required)
    assert all_covered is False, "FAIL: Should report not all covered"
    warning_lines = [l for l in lines if l.startswith('WARNING')]
    assert len(warning_lines) == 2, f"FAIL: Should have 2 warnings, got {len(warning_lines)}"
    print("  ✓ generate_coverage_report produces warnings")

    # get_all_tree_items
    all_items = get_all_tree_items(SIMPLE_TREE)
    assert isinstance(all_items, set), "FAIL: Should return set"
    assert 'Result A' in all_items, "FAIL: Should contain Result A"
    print("  ✓ get_all_tree_items works")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Decision Tree Generator - Test Suite")
    print("=" * 60)
    print()

    try:
        test_determinism()
        print()
        test_hash_stability()
        print()
        test_validation()
        print()
        test_output_content()
        print()
        test_example_files()
        print()
        test_coverage_functions()
        print()
        print("=" * 60)
        print("ALL TESTS PASSED ✓")
        print("=" * 60)
        return 0
    except AssertionError as e:
        print()
        print(f"TEST FAILED: {e}")
        return 1
    except Exception as e:
        print()
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
