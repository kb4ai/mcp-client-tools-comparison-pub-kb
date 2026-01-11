"""
Git metadata utilities for reproducible file generation.

Provides functions to get git-based timestamps and commit hashes for input files,
enabling byte-identical output across different machines and file systems.

Why git timestamps instead of filesystem timestamps:
- Filesystem timestamps change when files are checked out, copied, or touched
- Git timestamps represent when content was actually committed
- This ensures the same input content produces the same output metadata
- Makes builds reproducible across different machines and CI environments

Usage:
    from git_metadata import get_reproducible_footer

    footer = get_reproducible_footer([
        "projects/*.yaml",
        "README.template.md"
    ])
    # Returns: "Generated: 2024-01-15T10:30:00+00:00 | Source commit: abc1234"
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple


def get_git_root() -> Optional[Path]:
    """Get the root directory of the git repository.

    Returns:
        Path to git root, or None if not in a git repository.
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True
        )
        return Path(result.stdout.strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def expand_globs(patterns: List[str], base_path: Optional[Path] = None) -> List[Path]:
    """Expand glob patterns to list of existing files.

    Args:
        patterns: List of file paths or glob patterns (e.g., "projects/*.yaml")
        base_path: Base directory for relative paths (defaults to git root or cwd)

    Returns:
        List of resolved Path objects for existing files.
    """
    if base_path is None:
        base_path = get_git_root() or Path.cwd()

    files = []
    for pattern in patterns:
        path = Path(pattern)
        if path.is_absolute():
            if '*' in str(path):
                # Handle absolute glob patterns
                parent = path.parent
                while '*' in str(parent):
                    parent = parent.parent
                files.extend(parent.glob(str(path.relative_to(parent))))
            elif path.exists():
                files.append(path)
        else:
            # Relative path or glob
            if '*' in pattern:
                files.extend(base_path.glob(pattern))
            else:
                full_path = base_path / pattern
                if full_path.exists():
                    files.append(full_path)

    return sorted(set(files))


def get_file_commit_date(file_path: Path) -> Optional[str]:
    """Get the commit date of a file's last change.

    Args:
        file_path: Path to the file.

    Returns:
        ISO 8601 timestamp of the commit, or None if not tracked by git.
    """
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", str(file_path)],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()
        return output if output else None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def get_oldest_commit_date(file_paths: List[Path]) -> Optional[str]:
    """Get the oldest commit date among a list of files.

    This represents the "stalest" input, useful for cache invalidation logic.

    Args:
        file_paths: List of file paths to check.

    Returns:
        ISO 8601 timestamp of the oldest commit, or None if no files tracked.
    """
    dates = []
    for path in file_paths:
        date = get_file_commit_date(path)
        if date:
            dates.append(date)

    if not dates:
        return None

    # Sort dates and return oldest
    return sorted(dates)[0]


def get_latest_commit_date(file_paths: List[Path]) -> Optional[str]:
    """Get the latest commit date among a list of files.

    This represents the most recent change to any input file.

    Args:
        file_paths: List of file paths to check.

    Returns:
        ISO 8601 timestamp of the newest commit, or None if no files tracked.
    """
    dates = []
    for path in file_paths:
        date = get_file_commit_date(path)
        if date:
            dates.append(date)

    if not dates:
        return None

    # Sort dates and return newest
    return sorted(dates)[-1]


def get_latest_commit_hash(file_paths: List[Path]) -> Optional[str]:
    """Get the short hash of the latest commit affecting any of the input files.

    Args:
        file_paths: List of file paths to check.

    Returns:
        Short commit hash (7 chars), or None if no files tracked by git.
    """
    if not file_paths:
        return None

    try:
        # Get the latest commit that touched any of these files
        cmd = ["git", "log", "-1", "--format=%h", "--"]
        cmd.extend(str(p) for p in file_paths)

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()
        return output if output else None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def get_reproducible_metadata(
    input_patterns: List[str],
    base_path: Optional[Path] = None
) -> Tuple[Optional[str], Optional[str]]:
    """Get reproducible metadata for a set of input files.

    Args:
        input_patterns: List of file paths or glob patterns.
        base_path: Base directory for relative paths.

    Returns:
        Tuple of (oldest_timestamp, latest_commit_hash).
        Either value may be None if files aren't tracked by git.
    """
    files = expand_globs(input_patterns, base_path)

    if not files:
        return (None, None)

    oldest_date = get_oldest_commit_date(files)
    latest_hash = get_latest_commit_hash(files)

    return (oldest_date, latest_hash)


def get_reproducible_footer(
    input_patterns: List[str],
    base_path: Optional[Path] = None,
    format_style: str = "markdown"
) -> str:
    """Generate a reproducible footer string for generated files.

    Args:
        input_patterns: List of file paths or glob patterns for input files.
        base_path: Base directory for relative paths.
        format_style: Output format - "markdown", "html", or "comment".

    Returns:
        Formatted footer string. If git metadata unavailable, returns
        a warning message instead.

    Examples:
        >>> get_reproducible_footer(["projects/*.yaml"], format_style="markdown")
        "Generated: 2024-01-15T10:30:00+00:00 | Source commit: abc1234"

        >>> get_reproducible_footer(["config.yaml"], format_style="html")
        "<!-- Generated: 2024-01-15T10:30:00+00:00 | Source commit: abc1234 -->"
    """
    oldest_date, latest_hash = get_reproducible_metadata(input_patterns, base_path)

    if oldest_date is None and latest_hash is None:
        warning = "Warning: Could not determine git metadata for input files"
        if format_style == "html":
            return f"<!-- {warning} -->"
        elif format_style == "comment":
            return f"# {warning}"
        return warning

    parts = []
    if oldest_date:
        parts.append(f"Generated: {oldest_date}")
    if latest_hash:
        parts.append(f"Source commit: {latest_hash}")

    content = " | ".join(parts)

    if format_style == "html":
        return f"<!-- {content} -->"
    elif format_style == "comment":
        return f"# {content}"

    return content


def check_uncommitted_changes(file_paths: List[Path]) -> List[Path]:
    """Check if any of the input files have uncommitted changes.

    Args:
        file_paths: List of file paths to check.

    Returns:
        List of paths with uncommitted changes (staged or unstaged).
    """
    uncommitted = []

    for path in file_paths:
        try:
            # Check for uncommitted changes (both staged and unstaged)
            result = subprocess.run(
                ["git", "status", "--porcelain", "--", str(path)],
                capture_output=True,
                text=True,
                check=True
            )
            if result.stdout.strip():
                uncommitted.append(path)
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

    return uncommitted


def warn_uncommitted(
    input_patterns: List[str],
    base_path: Optional[Path] = None,
    output_stream=sys.stderr
) -> bool:
    """Warn if any input files have uncommitted changes.

    Args:
        input_patterns: List of file paths or glob patterns.
        base_path: Base directory for relative paths.
        output_stream: Where to print warnings (default: stderr).

    Returns:
        True if there are uncommitted changes, False otherwise.
    """
    files = expand_globs(input_patterns, base_path)
    uncommitted = check_uncommitted_changes(files)

    if uncommitted:
        print(
            f"Warning: {len(uncommitted)} input file(s) have uncommitted changes.",
            file=output_stream
        )
        print(
            "  Metadata will reflect the last committed state, not current content.",
            file=output_stream
        )
        for path in uncommitted[:5]:  # Show at most 5
            print(f"    - {path}", file=output_stream)
        if len(uncommitted) > 5:
            print(f"    - ... and {len(uncommitted) - 5} more", file=output_stream)
        return True

    return False


if __name__ == "__main__":
    # Demo/test mode
    import argparse

    parser = argparse.ArgumentParser(description="Get git metadata for files")
    parser.add_argument("patterns", nargs="+", help="File paths or glob patterns")
    parser.add_argument("--format", choices=["markdown", "html", "comment"],
                       default="markdown", help="Output format")
    args = parser.parse_args()

    print(f"Patterns: {args.patterns}")
    files = expand_globs(args.patterns)
    print(f"Resolved files: {len(files)}")
    for f in files[:10]:
        print(f"  - {f}")
    if len(files) > 10:
        print(f"  ... and {len(files) - 10} more")

    print()
    warn_uncommitted(args.patterns)
    print()
    footer = get_reproducible_footer(args.patterns, format_style=args.format)
    print(f"Footer: {footer}")
