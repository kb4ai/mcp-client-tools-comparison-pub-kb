#!/usr/bin/env python3
"""
Generate comparison tables from project YAML files.

Usage:
    ./scripts/generate-tables.py                    # Generate all tables
    ./scripts/generate-tables.py --by-category      # Group by category
    ./scripts/generate-tables.py --by-transport     # Group by transport
    ./scripts/generate-tables.py --by-stars         # Sort by stars
    ./scripts/generate-tables.py --reputable-only   # Only reputable sources
    ./scripts/generate-tables.py --auth             # Authentication matrix only
    ./scripts/generate-tables.py --enterprise-auth  # Enterprise auth features
    ./scripts/generate-tables.py --installation     # Installation methods
    ./scripts/generate-tables.py --json             # Output as JSON
"""

import sys
import json
from pathlib import Path
from collections import defaultdict

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)


SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
PROJECTS_DIR = PROJECT_ROOT / "projects"


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


def format_transports(transports):
    """Format transports dict as compact string."""
    if not transports:
        return ""
    enabled = [k for k, v in transports.items() if v]
    return ", ".join(enabled)


def generate_overview_table(projects):
    """Generate main overview table sorted by stars."""
    # Sort by stars (descending), None values last
    sorted_projects = sorted(
        projects,
        key=lambda p: (p.get('stars') is not None, p.get('stars') or 0),
        reverse=True
    )

    lines = []
    lines.append("## Overview: All Projects by Stars")
    lines.append("")
    lines.append("| Project | Stars | Language | Category | Transports |")
    lines.append("|---------|------:|----------|----------|------------|")

    for p in sorted_projects:
        name = p.get('name', p.get('_filename', 'Unknown'))
        repo_url = p.get('repo-url', '')
        stars = p.get('stars', '')
        if stars == '':
            stars = '?'
        lang = p.get('language', '')
        category = p.get('category', '')
        transports = format_transports(p.get('transports', {}))

        # Make name a link
        if repo_url:
            name_cell = f"[{name}]({repo_url})"
        else:
            name_cell = name

        lines.append(f"| {name_cell} | {stars} | {lang} | {category} | {transports} |")

    return "\n".join(lines)


def generate_by_category(projects):
    """Generate tables grouped by category."""
    by_category = defaultdict(list)
    for p in projects:
        cat = p.get('category', 'uncategorized')
        by_category[cat].append(p)

    lines = []
    lines.append("## Projects by Category")
    lines.append("")

    for category in sorted(by_category.keys()):
        cat_projects = sorted(
            by_category[category],
            key=lambda p: (p.get('stars') is not None, p.get('stars') or 0),
            reverse=True
        )

        lines.append(f"### {category.replace('-', ' ').title()}")
        lines.append("")
        lines.append("| Project | Stars | Language | Description |")
        lines.append("|---------|------:|----------|-------------|")

        for p in cat_projects:
            name = p.get('name', p.get('_filename', 'Unknown'))
            repo_url = p.get('repo-url', '')
            stars = p.get('stars', '?')
            lang = p.get('language', '')
            desc = p.get('description', '')[:60]
            if len(p.get('description', '')) > 60:
                desc += '...'

            if repo_url:
                name_cell = f"[{name}]({repo_url})"
            else:
                name_cell = name

            lines.append(f"| {name_cell} | {stars} | {lang} | {desc} |")

        lines.append("")

    return "\n".join(lines)


def generate_transport_matrix(projects):
    """Generate transport support matrix."""
    lines = []
    lines.append("## Transport Support Matrix")
    lines.append("")
    lines.append("| Project | stdio | SSE | HTTP | WebSocket | gRPC |")
    lines.append("|---------|:-----:|:---:|:----:|:---------:|:----:|")

    sorted_projects = sorted(
        projects,
        key=lambda p: (p.get('stars') is not None, p.get('stars') or 0),
        reverse=True
    )

    for p in sorted_projects:
        name = p.get('name', p.get('_filename', 'Unknown'))
        repo_url = p.get('repo-url', '')
        transports = p.get('transports', {})

        if repo_url:
            name_cell = f"[{name}]({repo_url})"
        else:
            name_cell = name

        def check(t):
            return "✓" if transports.get(t) else ""

        lines.append(f"| {name_cell} | {check('stdio')} | {check('sse')} | {check('http')} | {check('websocket')} | {check('grpc')} |")

    return "\n".join(lines)


def generate_reputable_sources(projects):
    """Generate table of reputable/official sources."""
    reputable = [p for p in projects if p.get('reputable-source')]

    lines = []
    lines.append("## Reputable/Official Sources")
    lines.append("")
    lines.append("| Project | Organization | Category | Description |")
    lines.append("|---------|--------------|----------|-------------|")

    for p in sorted(reputable, key=lambda p: p.get('organization', '')):
        name = p.get('name', p.get('_filename', 'Unknown'))
        repo_url = p.get('repo-url', '')
        org = p.get('organization', '')
        category = p.get('category', '')
        desc = p.get('description', '')[:50]
        if len(p.get('description', '')) > 50:
            desc += '...'

        if repo_url:
            name_cell = f"[{name}]({repo_url})"
        else:
            name_cell = name

        lines.append(f"| {name_cell} | {org} | {category} | {desc} |")

    return "\n".join(lines)


def generate_authentication_matrix(projects):
    """Generate authentication support matrix."""
    lines = []
    lines.append("## Authentication Support Matrix")
    lines.append("")
    lines.append("Projects with documented authentication capabilities:")
    lines.append("")
    lines.append("| Project | OAuth 2.0 | PKCE | Bearer | API Key | Headers | Keychain | Notes |")
    lines.append("|---------|:---------:|:----:|:------:|:-------:|:-------:|:--------:|-------|")

    # Filter to projects with authentication data
    auth_projects = [p for p in projects if p.get('authentication')]

    sorted_projects = sorted(
        auth_projects,
        key=lambda p: (p.get('stars') is not None, p.get('stars') or 0),
        reverse=True
    )

    for p in sorted_projects:
        name = p.get('name', p.get('_filename', 'Unknown'))
        repo_url = p.get('repo-url', '')
        auth = p.get('authentication', {})

        if repo_url:
            name_cell = f"[{name}]({repo_url})"
        else:
            name_cell = name

        def check(field):
            val = auth.get(field)
            if val is True:
                return "✓"
            elif val is False:
                return "✗"
            return ""

        # Extract first auth note (truncated)
        notes = auth.get('auth-notes', [])
        note = notes[0][:30] + '...' if notes and len(notes[0]) > 30 else (notes[0] if notes else '')

        # Check for keychain/secure storage in notes
        keychain = "✓" if any('keychain' in str(n).lower() for n in notes) else ""

        lines.append(
            f"| {name_cell} | "
            f"{check('oauth2')} | "
            f"{check('oauth2-pkce')} | "
            f"{check('bearer-token')} | "
            f"{check('api-key')} | "
            f"{check('custom-header')} | "
            f"{keychain} | "
            f"{note} |"
        )

    if not auth_projects:
        lines.append("| *No projects with auth data* | | | | | | | |")

    return "\n".join(lines)


def generate_enterprise_auth_table(projects):
    """Generate table of enterprise authentication features."""
    # Filter to projects with enterprise features
    enterprise = [
        p for p in projects
        if p.get('authentication', {}).get('entra-id')
        or p.get('authentication', {}).get('rbac')
        or p.get('authentication', {}).get('multi-tenant')
        or p.get('authentication', {}).get('auth-bridging')
        or p.get('authentication', {}).get('oidc')
    ]

    if not enterprise:
        return ""

    lines = []
    lines.append("## Enterprise Authentication Features")
    lines.append("")
    lines.append("| Project | Entra ID | RBAC | Multi-Tenant | Auth Bridging | OIDC |")
    lines.append("|---------|:--------:|:----:|:------------:|:-------------:|:----:|")

    for p in sorted(enterprise, key=lambda x: x.get('organization', '')):
        name = p.get('name', p.get('_filename', 'Unknown'))
        repo_url = p.get('repo-url', '')
        auth = p.get('authentication', {})

        if repo_url:
            name_cell = f"[{name}]({repo_url})"
        else:
            name_cell = name

        def check(field):
            return "✓" if auth.get(field) else ""

        lines.append(
            f"| {name_cell} | "
            f"{check('entra-id')} | "
            f"{check('rbac')} | "
            f"{check('multi-tenant')} | "
            f"{check('auth-bridging')} | "
            f"{check('oidc')} |"
        )

    return "\n".join(lines)


def generate_installation_methods_table(projects):
    """Generate table of available installation methods."""
    # Filter to projects with installation data
    install_projects = [p for p in projects if p.get('installation')]

    if not install_projects:
        return ""

    lines = []
    lines.append("## Installation Methods")
    lines.append("")
    lines.append("| Project | npm | pip | brew | docker | go install |")
    lines.append("|---------|:---:|:---:|:----:|:------:|:----------:|")

    sorted_projects = sorted(
        install_projects,
        key=lambda p: (p.get('stars') is not None, p.get('stars') or 0),
        reverse=True
    )

    for p in sorted_projects:
        name = p.get('name', p.get('_filename', 'Unknown'))
        repo_url = p.get('repo-url', '')
        install = p.get('installation', {})

        if repo_url:
            name_cell = f"[{name}]({repo_url})"
        else:
            name_cell = name

        def check_install(method):
            return "✓" if install.get(method) else ""

        lines.append(
            f"| {name_cell} | "
            f"{check_install('npm')} | "
            f"{check_install('pip')} | "
            f"{check_install('brew')} | "
            f"{check_install('docker')} | "
            f"{check_install('go-install')} |"
        )

    return "\n".join(lines)


def generate_stats(projects):
    """Generate summary statistics."""
    total = len(projects)
    by_category = defaultdict(int)
    by_language = defaultdict(int)
    reputable_count = 0
    has_stars = 0
    total_stars = 0

    for p in projects:
        by_category[p.get('category', 'uncategorized')] += 1
        by_language[p.get('language', 'unknown')] += 1
        if p.get('reputable-source'):
            reputable_count += 1
        if p.get('stars'):
            has_stars += 1
            total_stars += p.get('stars') or 0

    lines = []
    lines.append("## Summary Statistics")
    lines.append("")
    lines.append(f"- **Total projects:** {total}")
    lines.append(f"- **Reputable sources:** {reputable_count}")
    lines.append(f"- **Combined stars:** {total_stars:,} (from {has_stars} projects with star data)")
    lines.append("")
    lines.append("### By Category")
    lines.append("")
    for cat, count in sorted(by_category.items(), key=lambda x: -x[1]):
        lines.append(f"- {cat}: {count}")
    lines.append("")
    lines.append("### By Language")
    lines.append("")
    for lang, count in sorted(by_language.items(), key=lambda x: -x[1]):
        if lang:
            lines.append(f"- {lang}: {count}")

    return "\n".join(lines)


def main():
    args = set(sys.argv[1:])

    projects = load_projects()
    if not projects:
        print("No project files found in projects/")
        sys.exit(1)

    if '--json' in args:
        print(json.dumps(projects, indent=2, default=str))
        return

    output_parts = []

    if '--by-category' in args:
        output_parts.append(generate_by_category(projects))
    elif '--by-transport' in args:
        output_parts.append(generate_transport_matrix(projects))
    elif '--reputable-only' in args:
        output_parts.append(generate_reputable_sources(projects))
    elif '--by-stars' in args:
        output_parts.append(generate_overview_table(projects))
    elif '--auth' in args:
        output_parts.append(generate_authentication_matrix(projects))
    elif '--enterprise-auth' in args:
        output_parts.append(generate_enterprise_auth_table(projects))
    elif '--installation' in args:
        output_parts.append(generate_installation_methods_table(projects))
    else:
        # Generate all sections
        output_parts.append(generate_stats(projects))
        output_parts.append("")
        output_parts.append(generate_overview_table(projects))
        output_parts.append("")
        output_parts.append(generate_authentication_matrix(projects))
        output_parts.append("")
        enterprise_auth = generate_enterprise_auth_table(projects)
        if enterprise_auth:
            output_parts.append(enterprise_auth)
            output_parts.append("")
        output_parts.append(generate_reputable_sources(projects))
        output_parts.append("")
        output_parts.append(generate_transport_matrix(projects))
        output_parts.append("")
        installation = generate_installation_methods_table(projects)
        if installation:
            output_parts.append(installation)
            output_parts.append("")
        output_parts.append(generate_by_category(projects))

    print("\n".join(output_parts))


if __name__ == "__main__":
    main()
