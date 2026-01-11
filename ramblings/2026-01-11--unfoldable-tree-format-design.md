# Unfoldable Tree Format Design

Date: 2026-01-11

## The Problem

GitHub renders `<details>/<summary>` HTML natively, but nested elements appear **flat** - no visual indication of hierarchy depth. Users lose context of where they are in the decision tree.

## The Solution: Box-Drawing Characters + Emoji Icons

Use Unicode box-drawing characters as visual prefixes in `<summary>` lines:

```
│  ├─ 📂 CLI - Interactive command-line usage
│  │  ├─ ❓ Do you need LLM integration (chat with AI)?
│  │  │  ├─ 📂 Yes - Chat interface with LLM
│  │  │  │  ├─ ❓ Which LLM provider?
│  │  │  │  │  ├─ 📌 OpenAI-compatible (OpenAI, Groq, local)
│  │  │  │  │  └─ 📌 Multiple providers / flexible
```

## Box-Drawing Characters

| Character | Unicode | Purpose |
|-----------|---------|---------|
| `│` | U+2502 | Vertical line - shows depth continuation |
| `├` | U+251C | Branch - item with siblings below |
| `└` | U+2514 | Last branch - final item in group |
| `─` | U+2500 | Horizontal line - connects to text |

### Indentation Pattern

```python
# Each depth level adds "│  " (vertical + 2 spaces)
depth_0: ""
depth_1: "│  "
depth_2: "│  │  "
depth_3: "│  │  │  "

# Branch connector depends on position
middle_item: "├─ "
last_item:   "└─ "
```

## Emoji Icons

| Icon | Meaning | Used For |
|------|---------|----------|
| 🔍 | Search/explore | Root question |
| ❓ | Question | Decision nodes |
| 📂 | Folder/category | Branches leading to more questions |
| 📌 | Pin/bookmark | Leaf nodes (final answers) |
| ✅ | Checkmark | Recommendations |

### Icon Placement Rules

```
🔍 Root question (only one, at top)
├─ 📂 Category branch (leads to more decisions)
│  ├─ ❓ Sub-question
│  │  ├─ 📌 Leaf answer
│  │  └─ 📌 Another leaf
│  └─ 📂 Another category
└─ 📂 Final top-level category
```

## Implementation

```python
def _render_details_tree(node: dict, depth: int = 0, is_root: bool = False) -> str:
    indent = '│  ' * depth if depth > 0 else ''

    # Choose branch connector based on position
    is_last = ...  # determined by loop index
    branch = '└─ ' if is_last else '├─ '

    # Choose icon based on node type
    if is_root:
        icon = '🔍'
    elif 'question' in node:
        icon = '❓'
    elif has_children:
        icon = '📂'
    else:
        icon = '📌'

    return f'<summary>{indent}{branch}{icon} {text}</summary>'
```

## Why This Works on GitHub

1. **No CSS needed** - Box-drawing chars are plain text, render in any font
2. **Monospace-friendly** - Characters align properly in GitHub's markdown renderer
3. **Copy-pasteable** - Structure survives copy/paste operations
4. **Accessible** - Screen readers can interpret the text
5. **Universal** - Works in any browser, no JavaScript required

## Before vs After

### Before (flat):
```
<details><summary>CLI usage</summary>
<details><summary>Need LLM?</summary>
<details><summary>Yes</summary>
Recommendation...
</details>
</details>
</details>
```
All summaries appear at same visual level when expanded.

### After (with tree structure):
```
<details><summary>🔍 CLI usage</summary>
<details><summary>│  ├─ ❓ Need LLM?</summary>
<details><summary>│  │  └─ 📌 Yes</summary>
│  │     └── ✅ **Use mcp-cli**
</details>
</details>
</details>
```
Visual hierarchy is immediately clear.

## Files

* Generator: `scripts/generate-decision-tree.py`
* Output: `comparisons/decision-tree-unfoldable.md`
* Library: `r-and-d/decision-tree-generator/`

## References

* [Unicode Box Drawing](https://en.wikipedia.org/wiki/Box-drawing_character)
* [HTML details element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/details)
* Git tag: `v0.2.0-decision-tree`
