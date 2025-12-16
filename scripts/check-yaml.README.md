# check-yaml.py

Validates project YAML files against the `spec.yaml` schema.

## Usage

```bash
# Check all files in projects/
./scripts/check-yaml.py

# Check specific file(s)
./scripts/check-yaml.py projects/sparfenyuk--mcp-proxy.yaml

# Strict mode: fail on warnings too
./scripts/check-yaml.py --strict
```

## Requirements

* Python 3.6+
* PyYAML: `pip install pyyaml`

## Validation Checks

### Required Fields

* `last-update`: Must be present, YYYY-MM-DD format
* `repo-url`: Must be present, valid URL format

### Type Validation

* Date fields (`last-update`, `last-commit`, `created`): YYYY-MM-DD format
* URL fields (`repo-url`): Must start with http(s)://
* Numeric fields (`stars`, `forks`, etc.): Must be numbers
* Boolean fields (`reputable-source`, `archived`): Must be true/false
* Array fields (`features`, `notes`): Must be lists
* `transports`: Must be a mapping with boolean values

### Warnings (non-fatal)

* Unknown category values
* `repo-commit` that doesn't look like a git hash

## Exit Codes

* `0`: All validations passed
* `1`: Errors found (or warnings in strict mode)
