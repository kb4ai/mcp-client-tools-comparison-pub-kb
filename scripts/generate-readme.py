#!/usr/bin/env python3
"""
Generate README.md from template and project YAML files.

Usage:
    ./scripts/generate-readme.py              # Generate README.md
    ./scripts/generate-readme.py --dry-run    # Print to stdout instead
"""

import re
import sys
from pathlib import Path
from collections import defaultdict

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)

from git_metadata import get_reproducible_footer, warn_uncommitted


SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
PROJECTS_DIR = PROJECT_ROOT / "projects"
TEMPLATE_FILE = PROJECT_ROOT / "README.template.md"
OUTPUT_FILE = PROJECT_ROOT / "README.md"

# Input patterns for reproducible metadata
INPUT_PATTERNS = [
    "README.template.md",
    "projects/*.yaml"
]


def load_projects():
    """Load all project YAML files."""
    projects = []
    for yaml_file in sorted(PROJECTS_DIR.glob("*.yaml")):
        try:
            with open(yaml_file) as f:
                data = yaml.safe_load(f)
                if data:
                    data['_filename'] = yaml_file.stem
                    projects.append(data)
        except Exception as e:
            print(f"Warning: Could not load {yaml_file}: {e}", file=sys.stderr)
    return projects


def format_stars(stars):
    """Format stars as 1.8k, 882, etc."""
    if stars is None or stars == '':
        return "-"
    if isinstance(stars, str):
        return stars
    if stars >= 1000:
        return f"{stars/1000:.1f}k"
    return str(stars)


def format_org_project_cell(project):
    """Format project name as [org/repo](url) [y](yaml) link."""
    repo_url = project.get('repo-url', '')
    filename = project.get('_filename', '')

    # Extract org/repo from filename (format: owner--repo)
    if filename and '--' in filename:
        parts = filename.split('--', 1)
        org = parts[0]
        repo = parts[1]
        display_name = f"{org}/{repo}"
    else:
        display_name = project.get('name', project.get('_filename', 'Unknown'))

    # Build YAML file link
    yaml_link = f"[y](projects/{filename}.yaml)" if filename else ""

    # Create markdown link with repo URL and YAML link
    if repo_url:
        return f"[{display_name}]({repo_url}) {yaml_link}".strip()
    else:
        return f"{display_name} {yaml_link}".strip()


def get_projects_by_category(projects, category):
    """Get projects filtered by category, sorted by stars descending."""
    filtered = [p for p in projects if p.get('category') == category]
    return sorted(
        filtered,
        key=lambda p: (p.get('stars') is not None, p.get('stars') or 0),
        reverse=True
    )


def generate_stats(projects):
    """Generate ecosystem overview stats table."""
    by_category = defaultdict(int)
    total_stars = 0
    reputable_count = 0

    for p in projects:
        by_category[p.get('category', 'uncategorized')] += 1
        if p.get('stars'):
            total_stars += p.get('stars') or 0
        if p.get('reputable-source'):
            reputable_count += 1

    # Map categories to display names
    category_display = {
        'cli-client': 'CLI Clients',
        'http-bridge': 'Transport Bridges',
        'websocket-bridge': 'Transport Bridges',
        'rest-api-bridge': 'REST API Bridges',
        'enterprise-gateway': 'Enterprise Gateways',
        'specialized-adapter': 'Specialized Adapters',
        'grpc-bridge': 'gRPC Bridge',
        'openapi-to-mcp': 'OpenAPI Converters',
        'mcp-to-openapi': 'MCP to OpenAPI',
        'mcp-framework': 'MCP Frameworks',
    }

    # Aggregate by display category
    display_counts = defaultdict(int)
    for cat, count in by_category.items():
        display_name = category_display.get(cat, cat.replace('-', ' ').title())
        display_counts[display_name] += count

    lines = []
    lines.append("| Category | Projects | Description |")
    lines.append("|----------|----------|-------------|")

    # Order for display
    order = ['CLI Clients', 'Transport Bridges', 'REST API Bridges',
             'Enterprise Gateways', 'Specialized Adapters', 'OpenAPI Converters']

    descriptions = {
        'CLI Clients': 'Command-line interfaces for MCP',
        'Transport Bridges': 'stdio <-> HTTP/SSE/WebSocket',
        'REST API Bridges': 'Expose MCP as REST with OpenAPI',
        'Enterprise Gateways': 'Production infrastructure',
        'Specialized Adapters': 'CLI wrapping, command execution',
        'OpenAPI Converters': 'OpenAPI to/from MCP conversion',
        'gRPC Bridge': 'gRPC/protobuf to MCP',
        'MCP Frameworks': 'Framework libraries',
    }

    for cat in order:
        if cat in display_counts:
            desc = descriptions.get(cat, '')
            lines.append(f"| {cat} | {display_counts[cat]} | {desc} |")

    # Add remaining categories
    for cat, count in sorted(display_counts.items()):
        if cat not in order:
            desc = descriptions.get(cat, '')
            lines.append(f"| {cat} | {count} | {desc} |")

    total = len(projects)
    lines.append(f"| **Total** | **{total}** | All tracked projects |")
    lines.append("")
    lines.append(f"**Top projects:** {total_stars:,}+ combined GitHub stars | {reputable_count} reputable/official sources")

    return "\n".join(lines)


def generate_cli_clients(projects, limit=6):
    """Generate CLI clients table."""
    cli_projects = get_projects_by_category(projects, 'cli-client')[:limit]

    lines = []
    lines.append("| Org/Project | Stars | Language | Key Features |")
    lines.append("|-------------|------:|----------|--------------|")

    for p in cli_projects:
        cell = format_org_project_cell(p)
        stars = format_stars(p.get('stars'))
        lang = p.get('language', '')
        # Get first feature or description snippet
        features = p.get('features', [])
        if features:
            feat = features[0][:50] + '...' if len(features[0]) > 50 else features[0]
        else:
            desc = p.get('description', '')
            feat = desc[:50] + '...' if len(desc) > 50 else desc
        lines.append(f"| {cell} | {stars} | {lang} | {feat} |")

    return "\n".join(lines)


def generate_rest_bridges(projects):
    """Generate REST API bridges table."""
    rest_projects = get_projects_by_category(projects, 'rest-api-bridge')

    lines = []
    lines.append("| Org/Project | Stars | Language | Best For |")
    lines.append("|-------------|------:|----------|----------|")

    for p in rest_projects:
        cell = format_org_project_cell(p)
        stars = format_stars(p.get('stars'))
        lang = p.get('language', '')
        desc = p.get('description', '')[:40]
        if len(p.get('description', '')) > 40:
            desc += '...'
        lines.append(f"| {cell} | {stars} | {lang} | {desc} |")

    return "\n".join(lines)


def generate_transport_bridges(projects, limit=6):
    """Generate transport bridges table."""
    # Include http-bridge, websocket-bridge categories
    bridge_projects = [
        p for p in projects
        if p.get('category') in ('http-bridge', 'websocket-bridge')
    ]
    bridge_projects = sorted(
        bridge_projects,
        key=lambda p: (p.get('stars') is not None, p.get('stars') or 0),
        reverse=True
    )[:limit]

    lines = []
    lines.append("| Org/Project | Stars | Type | Transports |")
    lines.append("|-------------|------:|------|------------|")

    for p in bridge_projects:
        cell = format_org_project_cell(p)
        stars = format_stars(p.get('stars'))
        lang = p.get('language', '')
        # Format transports
        transports = p.get('transports', {})
        enabled = [k for k, v in transports.items() if v]
        trans_str = ', '.join(enabled) if enabled else '-'
        lines.append(f"| {cell} | {stars} | {lang} | {trans_str} |")

    return "\n".join(lines)


def generate_enterprise(projects):
    """Generate enterprise gateways table."""
    enterprise = get_projects_by_category(projects, 'enterprise-gateway')
    # Also include docker and cloud integrations with reputable source
    for p in projects:
        if p.get('reputable-source') and p.get('category') in ('docker-integration', 'cloud-integration'):
            if p not in enterprise:
                enterprise.append(p)

    lines = []
    lines.append("| Org/Project | Organization | Features |")
    lines.append("|-------------|--------------|----------|")

    for p in enterprise:
        cell = format_org_project_cell(p)
        org = p.get('organization', '')
        # Get first feature or description
        features = p.get('features', [])
        if features:
            feat = features[0][:50] + '...' if len(features[0]) > 50 else features[0]
        else:
            feat = p.get('description', '')[:50]
        lines.append(f"| {cell} | {org} | {feat} |")

    return "\n".join(lines)


def generate_grpc_bridge(projects):
    """Generate gRPC bridge table."""
    grpc_projects = get_projects_by_category(projects, 'grpc-bridge')

    lines = []
    lines.append("| Org/Project | Organization | Description |")
    lines.append("|-------------|--------------|-------------|")

    for p in grpc_projects:
        cell = format_org_project_cell(p)
        org = p.get('organization', '')
        desc = p.get('description', '')[:50]
        if len(p.get('description', '')) > 50:
            desc += '...'
        lines.append(f"| {cell} | {org} | {desc} |")

    return "\n".join(lines)


def generate_specialized(projects):
    """Generate specialized adapters table."""
    specialized = get_projects_by_category(projects, 'specialized-adapter')
    # Also include kubernetes integration
    for p in projects:
        if p.get('category') == 'kubernetes-integration':
            if p not in specialized:
                specialized.append(p)

    lines = []
    lines.append("| Org/Project | Type | Description |")
    lines.append("|-------------|------|-------------|")

    for p in specialized:
        cell = format_org_project_cell(p)
        cat = p.get('category', '').replace('-', ' ').title()
        desc = p.get('description', '')[:50]
        if len(p.get('description', '')) > 50:
            desc += '...'
        lines.append(f"| {cell} | {cat} | {desc} |")

    return "\n".join(lines)


def process_template(template, projects):
    """Replace AUTOGEN markers with generated content."""
    generators = {
        'STATS': lambda args: generate_stats(projects),
        'CLI_CLIENTS': lambda args: generate_cli_clients(projects, int(args[0]) if args else 6),
        'REST_BRIDGES': lambda args: generate_rest_bridges(projects),
        'TRANSPORT_BRIDGES': lambda args: generate_transport_bridges(projects, int(args[0]) if args else 6),
        'ENTERPRISE': lambda args: generate_enterprise(projects),
        'GRPC_BRIDGE': lambda args: generate_grpc_bridge(projects),
        'SPECIALIZED': lambda args: generate_specialized(projects),
    }

    # Pattern: <!-- AUTOGEN:NAME:ARG1:ARG2 --> ... <!-- /AUTOGEN:NAME -->
    pattern = r'<!-- AUTOGEN:(\w+)(?::([^>]+))? -->\s*\n?.*?<!-- /AUTOGEN:\1 -->'

    def replacer(match):
        name = match.group(1)
        args_str = match.group(2)
        args = args_str.split(':') if args_str else []

        if name in generators:
            content = generators[name](args)
            return f"<!-- AUTOGEN:{name}{':' + args_str if args_str else ''} -->\n{content}\n<!-- /AUTOGEN:{name} -->"
        else:
            print(f"Warning: Unknown AUTOGEN section: {name}", file=sys.stderr)
            return match.group(0)

    return re.sub(pattern, replacer, template, flags=re.DOTALL)


def main():
    dry_run = '--dry-run' in sys.argv

    if not TEMPLATE_FILE.exists():
        print(f"Error: Template file not found: {TEMPLATE_FILE}")
        sys.exit(1)

    projects = load_projects()
    if not projects:
        print("No project files found in projects/")
        sys.exit(1)

    # Check for uncommitted changes and generate reproducible metadata footer
    warn_uncommitted(INPUT_PATTERNS, PROJECT_ROOT)
    metadata_footer = get_reproducible_footer(INPUT_PATTERNS, PROJECT_ROOT)
    print(f"Metadata: {metadata_footer}")

    template = TEMPLATE_FILE.read_text()
    readme = process_template(template, projects)

    # Add auto-generated header
    header = "<!-- AUTO-GENERATED from README.template.md - Run: ./scripts/generate-readme.py -->\n\n"
    readme = header + readme

    # Add reproducible metadata footer
    readme += f"\n\n---\n\n*{metadata_footer}*\n"

    if dry_run:
        print(readme)
    else:
        OUTPUT_FILE.write_text(readme)
        print(f"Generated {OUTPUT_FILE} from {TEMPLATE_FILE}")
        print(f"  - {len(projects)} projects loaded")


if __name__ == "__main__":
    main()
