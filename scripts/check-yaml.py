#!/usr/bin/env python3
"""
Validate project YAML files against spec.yaml schema.

Usage:
    ./scripts/check-yaml.py                    # Check all files
    ./scripts/check-yaml.py projects/foo.yaml  # Check specific file
    ./scripts/check-yaml.py --strict           # Fail on warnings too
"""

import sys
import re
from pathlib import Path
from datetime import datetime

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)


SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SPEC_FILE = PROJECT_ROOT / "spec.yaml"
PROJECTS_DIR = PROJECT_ROOT / "projects"


def load_spec():
    """Load the YAML spec schema."""
    if not SPEC_FILE.exists():
        print(f"Warning: spec.yaml not found at {SPEC_FILE}")
        return None
    with open(SPEC_FILE) as f:
        return yaml.safe_load(f)


def validate_date(value, field_name):
    """Validate YYYY-MM-DD date format."""
    if not isinstance(value, str):
        return f"{field_name}: expected string, got {type(value).__name__}"
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', value):
        return f"{field_name}: invalid date format '{value}', expected YYYY-MM-DD"
    try:
        datetime.strptime(value, '%Y-%m-%d')
    except ValueError as e:
        return f"{field_name}: invalid date '{value}': {e}"
    return None


def validate_url(value, field_name):
    """Validate URL format."""
    if not isinstance(value, str):
        return f"{field_name}: expected string, got {type(value).__name__}"
    if not re.match(r'^https?://', value):
        return f"{field_name}: invalid URL '{value}', must start with http(s)://"
    return None


def validate_project_yaml(filepath, spec):
    """Validate a single project YAML file."""
    errors = []
    warnings = []

    try:
        with open(filepath) as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return [f"YAML parse error: {e}"], []
    except Exception as e:
        return [f"Error reading file: {e}"], []

    if data is None:
        return ["File is empty"], []

    if not isinstance(data, dict):
        return ["File must contain a YAML mapping (dictionary)"], []

    # Check required fields
    if 'last-update' not in data:
        errors.append("Missing required field: last-update")
    else:
        err = validate_date(data['last-update'], 'last-update')
        if err:
            errors.append(err)

    if 'repo-url' not in data:
        errors.append("Missing required field: repo-url")
    else:
        err = validate_url(data['repo-url'], 'repo-url')
        if err:
            errors.append(err)

    # Validate optional date fields
    date_fields = ['last-commit', 'created']
    for field in date_fields:
        if field in data and data[field]:
            err = validate_date(data[field], field)
            if err:
                errors.append(err)

    # Validate repo-commit format (should be hex string)
    if 'repo-commit' in data and data['repo-commit']:
        commit = data['repo-commit']
        if not isinstance(commit, str):
            errors.append(f"repo-commit: expected string, got {type(commit).__name__}")
        elif not re.match(r'^[a-fA-F0-9]+$', commit):
            warnings.append(f"repo-commit: '{commit}' doesn't look like a git commit hash")

    # Validate category enum
    if spec and 'category' in data:
        valid_categories = spec.get('fields', {}).get('category', {}).get('enum', [])
        if valid_categories and data['category'] not in valid_categories:
            warnings.append(f"category: '{data['category']}' not in known categories: {valid_categories}")

    # Validate numeric fields
    numeric_fields = ['stars', 'forks', 'watchers', 'contributors', 'open-issues']
    for field in numeric_fields:
        if field in data and data[field] is not None:
            if not isinstance(data[field], (int, float)):
                errors.append(f"{field}: expected number, got {type(data[field]).__name__}")

    # Validate boolean fields
    bool_fields = ['reputable-source', 'archived']
    for field in bool_fields:
        if field in data and data[field] is not None:
            if not isinstance(data[field], bool):
                errors.append(f"{field}: expected boolean, got {type(data[field]).__name__}")

    # Validate transports structure
    if 'transports' in data and data['transports']:
        transports = data['transports']
        if not isinstance(transports, dict):
            errors.append(f"transports: expected mapping, got {type(transports).__name__}")
        else:
            for k, v in transports.items():
                if v is not None and not isinstance(v, bool):
                    warnings.append(f"transports.{k}: expected boolean, got {type(v).__name__}")

    # Validate arrays
    array_fields = ['features', 'notes', 'secondary-categories', 'languages']
    for field in array_fields:
        if field in data and data[field] is not None:
            if not isinstance(data[field], list):
                errors.append(f"{field}: expected list, got {type(data[field]).__name__}")

    return errors, warnings


def main():
    args = sys.argv[1:]
    strict = '--strict' in args
    args = [a for a in args if a != '--strict']

    spec = load_spec()

    # Determine which files to check
    if args:
        files = [Path(a) for a in args]
    else:
        if not PROJECTS_DIR.exists():
            print(f"Projects directory not found: {PROJECTS_DIR}")
            print("No files to validate.")
            sys.exit(0)
        files = list(PROJECTS_DIR.glob("*.yaml"))

    if not files:
        print("No YAML files found to validate.")
        sys.exit(0)

    total_errors = 0
    total_warnings = 0

    for filepath in sorted(files):
        errors, warnings = validate_project_yaml(filepath, spec)

        if errors or warnings:
            print(f"\n{filepath}:")
            for err in errors:
                print(f"  ❌ ERROR: {err}")
            for warn in warnings:
                print(f"  ⚠️  WARNING: {warn}")

        total_errors += len(errors)
        total_warnings += len(warnings)

    print(f"\n{'='*50}")
    print(f"Validated {len(files)} file(s)")
    print(f"Errors: {total_errors}, Warnings: {total_warnings}")

    if total_errors > 0:
        sys.exit(1)
    if strict and total_warnings > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
