# Reproducible Generation Guidelines

This document explains the reproducible metadata system used by our generation scripts to ensure byte-identical output across different machines and environments.

## Why Git Timestamps Instead of Filesystem Timestamps?

Filesystem timestamps are unreliable for reproducibility:

* They change when files are checked out (git clone sets them to checkout time)
* They change when files are copied or moved between systems
* They change when touched or modified even without content changes
* They vary across CI environments, containers, and developer machines

Git timestamps represent when content was actually committed:

* They are stored in the repository history, immutable for a given commit
* The same commit hash always has the same timestamp, globally
* Anyone cloning the repository gets the same metadata
* Works identically in CI pipelines, Docker containers, and developer machines

## Footer Format

Each generated file includes a metadata footer at the bottom:

```
Generated: 2024-01-15T10:30:00+00:00 | Source commit: abc1234
```

Components:

* **Generated**: ISO 8601 timestamp of the oldest input file's last commit
  * Using the oldest ensures the footer changes when ANY input changes
  * This is the "stalest" timestamp - if inputs are newer, we regenerate
* **Source commit**: Short hash of the latest commit affecting any input file
  * Identifies the exact source state used for generation
  * Makes it trivial to trace what inputs produced this output

## How the Utility Works

The `scripts/git_metadata.py` module provides:

```python
from git_metadata import get_reproducible_footer, warn_uncommitted

# Get footer string for a set of input files/globs
footer = get_reproducible_footer([
    "projects/*.yaml",
    "README.template.md"
])

# Check if any inputs have uncommitted changes (outputs warning to stderr)
warn_uncommitted(INPUT_PATTERNS, PROJECT_ROOT)
```

Key functions:

* `get_reproducible_footer(patterns, base_path)` - Main entry point
* `get_oldest_commit_date(files)` - Finds oldest timestamp among files
* `get_latest_commit_hash(files)` - Gets most recent commit affecting any file
* `expand_globs(patterns, base_path)` - Resolves glob patterns to file list
* `warn_uncommitted(patterns, base_path)` - Warns if inputs have local changes

## Adding to New Generation Scripts

1. Import the utility at the top of your script:

```python
from git_metadata import get_reproducible_footer, warn_uncommitted
```

2. Define your input patterns:

```python
INPUT_PATTERNS = [
    "path/to/input.yaml",
    "another/dir/*.yaml"
]
```

3. In your main function, before generating output:

```python
# Warn about uncommitted changes (outputs to stderr)
warn_uncommitted(INPUT_PATTERNS, PROJECT_ROOT)

# Get the metadata footer string
metadata_footer = get_reproducible_footer(INPUT_PATTERNS, PROJECT_ROOT)
```

4. Append the footer to your output:

For markdown:

```python
output += f"\n\n---\n\n*{metadata_footer}*\n"
```

For HTML:

```python
html = html.replace("</body>", f"\n<!-- {metadata_footer} -->\n</body>")
```

## Benefits

1. **Cache-friendly**: Same inputs = same output = same checksums
   * Build systems can skip regeneration when output unchanged
   * Git diffs are clean when regenerating without input changes

2. **Reproducible builds**: Anyone anywhere produces identical output
   * CI builds match local builds
   * Docker builds match native builds
   * Yesterday's checkout produces same output as today's

3. **Traceable**: Footer links output back to source
   * Can verify which commit generated a file
   * Can bisect issues to specific input changes

4. **Self-documenting**: Generated files show their provenance
   * Readers know the file is generated, not hand-written
   * Can check if regeneration is needed

## Edge Cases Handled

* **Uncommitted changes**: Warns to stderr, uses last committed state
* **Missing git**: Returns warning message instead of metadata
* **Untracked files**: Not included in metadata (can't determine timestamp)
* **Empty patterns**: Returns warning message

## Example Scripts Using This System

* `scripts/generate-decision-tree.py` - Decision tree visualizations
* `scripts/generate-tables.py` - Comparison tables
* `scripts/generate-readme.py` - Main README from template

Each defines its own `INPUT_PATTERNS` appropriate to its inputs.
