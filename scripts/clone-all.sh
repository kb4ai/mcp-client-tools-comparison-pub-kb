#!/usr/bin/env bash
#
# Clone all repositories listed in projects/*.yaml to tmp/
# Requires: yq (https://github.com/mikefarah/yq)
#
# Usage:
#   ./scripts/clone-all.sh           # Clone all repos
#   ./scripts/clone-all.sh --update  # Pull latest for existing repos
#   ./scripts/clone-all.sh --shallow # Shallow clone (faster)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PROJECTS_DIR="$PROJECT_ROOT/projects"
TMP_DIR="$PROJECT_ROOT/tmp"

# Parse arguments
UPDATE_MODE=false
SHALLOW_MODE=false
for arg in "$@"; do
    case $arg in
        --update) UPDATE_MODE=true ;;
        --shallow) SHALLOW_MODE=true ;;
        *) echo "Unknown argument: $arg"; exit 1 ;;
    esac
done

# Check for yq
if ! command -v yq &> /dev/null; then
    echo "Error: yq is required but not installed."
    echo "Install with: brew install yq  OR  pip install yq"
    exit 1
fi

# Create tmp directory
mkdir -p "$TMP_DIR"

# Count files
yaml_files=("$PROJECTS_DIR"/*.yaml)
if [[ ! -e "${yaml_files[0]}" ]]; then
    echo "No YAML files found in $PROJECTS_DIR"
    exit 0
fi

echo "Found ${#yaml_files[@]} project files"
echo "Cloning to: $TMP_DIR"
echo "----------------------------------------"

success_count=0
skip_count=0
fail_count=0

# Increment helper (works with set -e)
incr() { eval "$1=\$((\$$1 + 1))" || true; }

for yaml_file in "${yaml_files[@]}"; do
    # Extract repo URL
    repo_url=$(yq '.repo-url // ""' "$yaml_file")

    if [[ -z "$repo_url" ]]; then
        echo "⚠️  Skipping $yaml_file: no repo-url found"
        incr skip_count
        continue
    fi

    # Extract repo name from URL (owner/repo format)
    # Handle both https://github.com/owner/repo and git@github.com:owner/repo
    repo_path=$(echo "$repo_url" | sed -E 's|.*[:/]([^/]+/[^/]+)(\.git)?$|\1|')
    owner=$(echo "$repo_path" | cut -d/ -f1)
    repo=$(echo "$repo_path" | cut -d/ -f2)

    target_dir="$TMP_DIR/${owner}--${repo}"

    if [[ -d "$target_dir" ]]; then
        if $UPDATE_MODE; then
            echo "📥 Updating $repo_path..."
            if (cd "$target_dir" && git pull --quiet); then
                echo "   ✅ Updated"
                incr success_count
            else
                echo "   ❌ Update failed"
                incr fail_count
            fi
        else
            echo "⏭️  Skipping $repo_path (already exists)"
            incr skip_count
        fi
        continue
    fi

    echo "📦 Cloning $repo_path..."

    clone_args=()
    if $SHALLOW_MODE; then
        clone_args+=(--depth 1)
    fi

    if git clone "${clone_args[@]}" "$repo_url" "$target_dir" 2>/dev/null; then
        # Record the commit hash
        commit=$(cd "$target_dir" && git rev-parse HEAD)
        echo "   ✅ Cloned (commit: ${commit:0:7})"
        incr success_count
    else
        echo "   ❌ Clone failed"
        incr fail_count
    fi
done

echo "----------------------------------------"
echo "Done: $success_count cloned/updated, $skip_count skipped, $fail_count failed"
