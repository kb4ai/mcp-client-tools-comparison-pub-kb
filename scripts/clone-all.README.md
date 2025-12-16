# clone-all.sh

Clones all repositories listed in `projects/*.yaml` to the `tmp/` directory.

## Usage

```bash
# Clone all repos (skip existing)
./scripts/clone-all.sh

# Update existing repos (git pull)
./scripts/clone-all.sh --update

# Shallow clone (faster, less disk space)
./scripts/clone-all.sh --shallow
```

## Requirements

* bash
* git
* yq (YAML processor): `brew install yq` or `pip install yq`

## Behavior

1. Reads `repo-url` from each `projects/*.yaml` file
2. Creates `tmp/` directory if it doesn't exist
3. Clones each repo to `tmp/{owner}--{repo}/`
4. Skips repos that already exist (unless `--update`)

## Output Structure

```
tmp/
├── sparfenyuk--mcp-proxy/
├── chrishayuk--mcp-cli/
├── f--mcptools/
└── ...
```

## Options

| Flag | Description |
|------|-------------|
| `--update` | Pull latest changes for existing repos |
| `--shallow` | Use `--depth 1` for faster cloning |

## Exit Codes

* `0`: Success (some repos may have been skipped)
* `1`: Fatal error (e.g., yq not installed)
