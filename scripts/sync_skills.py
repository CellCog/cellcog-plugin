#!/usr/bin/env python3
"""
Sync CellCog skills from the monorepo to the Open Plugins plugin repo.

Reads SKILL.md files from the monorepo's openclaw_skills directory,
strips ClawHub-specific YAML frontmatter fields (keeping only name
and description which all agent tools support), and writes the result
to the plugin repo's skills directory.

This script is the bridge between the golden copy (monorepo) and the
Open Plugins distribution (this repo). The golden copy lives in:
    monorepo/md/cellcog/openclaw_skills/

The plugin repo follows the Open Plugins standard and works with:
    - Cursor (.cursor-plugin/plugin.json)
    - Claude Code (.claude-plugin/plugin.json)
    - OpenCode (.plugin/plugin.json)
    - Any conformant Open Plugins host

The curated skill subset is NOT kept here. It is `plugin_skills` in the release manifest,
monorepo/md/cellcog/distribution/manifest.json (Oct 18 2026: one source of truth for versions and
the subset; runbook: RELEASE.md next to it). This script writes the subset into skills/ AND into
openclaw.plugin.json#skills, and removes a skills/ folder whose skill left the subset.

Usage:
    python3 scripts/sync_skills.py [--source PATH] [--target PATH] [--manifest PATH] [--dry-run | --check]

    --dry-run  show what would be synced without writing files
    --check    exit 1 if skills/ or openclaw.plugin.json differs from what a sync would write (no writes)

Defaults:
    --source:   ../monorepo/md/cellcog/openclaw_skills
    --target:   ./skills
    --manifest: ../monorepo/md/cellcog/distribution/manifest.json

Exit codes: 0 done / in sync, 1 drift (--check), 2 error (missing manifest, source or skill).
"""

import argparse
import json
import os
import re
import shutil
import sys


def load_included_skills(manifest_path: str) -> list[str]:
    """The plugin's skill subset, in manifest order (`plugin_skills` of the release manifest)."""
    if not os.path.isfile(manifest_path):
        print(f"ERROR: release manifest not found: {manifest_path}")
        print("  The plugin skill subset lives in the monorepo at md/cellcog/distribution/manifest.json")
        print("  (`plugin_skills`). Check out the monorepo next to this repo, or pass --manifest PATH.")
        sys.exit(2)
    with open(manifest_path, 'r', encoding='utf-8') as f:
        skills = json.load(f).get('plugin_skills')
    if not isinstance(skills, list) or not skills or not all(isinstance(s, str) and s for s in skills):
        print(f"ERROR: {manifest_path}: `plugin_skills` must be a non-empty list of skill slugs")
        sys.exit(2)
    if len(set(skills)) != len(skills):
        print(f"ERROR: {manifest_path}: `plugin_skills` lists a skill twice")
        sys.exit(2)
    return skills


# Set from the manifest in main(); sync_skill() reads it.
INCLUDED_SKILLS: set[str] = set()

# Content to strip from cellcog skill during sync
# The cross-selling grid references skills not in the plugin
CELLCOG_STRIP_PATTERN = r'## What CellCog Can Do\n\n.*?\n---'

# Lines to strip from cellcog skill body (references to skills not in plugin)
CELLCOG_STRIP_LINES = [
    'install project-management-cellcog for details',
    'install pair-programming-cellcog for details',
    'install coding-agent-cellcog for details',
]


def parse_frontmatter(content: str) -> tuple[dict, str, str]:
    """Parse YAML frontmatter from SKILL.md content.
    
    Returns (frontmatter_dict, frontmatter_raw, body).
    frontmatter_dict has 'name' and 'description' extracted.
    """
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return {}, '', content
    
    raw = match.group(1)
    body = content[match.end():]
    
    fm = {}
    
    # Extract name
    name_match = re.search(r'^name:\s*(.+)$', raw, re.MULTILINE)
    if name_match:
        val = name_match.group(1).strip().strip('"').strip("'")
        fm['name'] = val
    
    # Extract description - handle multi-line quoted strings
    desc_match = re.search(r'^description:\s*"((?:[^"\\]|\\.)*)"\s*$', raw, re.MULTILINE)
    if desc_match:
        fm['description'] = desc_match.group(1).replace('\\"', '"')
    else:
        desc_match = re.search(r"^description:\s*'((?:[^'\\]|\\.)*)'\s*$", raw, re.MULTILINE)
        if desc_match:
            fm['description'] = desc_match.group(1)
        else:
            desc_match = re.search(r'^description:\s*(.+)$', raw, re.MULTILINE)
            if desc_match:
                fm['description'] = desc_match.group(1).strip().strip('"').strip("'")
    
    return fm, raw, body


def build_open_plugins_frontmatter(fm: dict) -> str:
    """Build an Open Plugins-compatible YAML frontmatter with only name and description.
    
    The Open Plugins spec (and Cursor specifically) only supports name and description
    in SKILL.md frontmatter. Unknown fields cause skills to fail silently in Cursor.
    """
    lines = ['---']
    
    if 'name' in fm:
        lines.append(f'name: {fm["name"]}')
    
    if 'description' in fm:
        desc = fm['description']
        # Use quotes if description contains special chars
        if any(c in desc for c in ':{}[],"\'#|>&*!%@`'):
            desc_escaped = desc.replace('"', '\\"')
            lines.append(f'description: "{desc_escaped}"')
        else:
            lines.append(f'description: {desc}')
    
    lines.append('---')
    return '\n'.join(lines) + '\n'


def render_skill(source_path: str, skill_name: str, quiet: bool = False) -> str:
    """The plugin's SKILL.md for one golden skill (Open Plugins frontmatter + transformed body)."""
    source_file = os.path.join(source_path, skill_name, 'SKILL.md')
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()

    fm, raw_fm, body = parse_frontmatter(content)

    if not fm.get('name'):
        if not quiet:
            print(f"  WARN {skill_name}: No name in frontmatter, using directory name")
        fm['name'] = skill_name
    
    # Strip cross-selling grid and excluded skill references from cellcog skill
    if skill_name == 'cellcog':
        body = re.sub(
            r'## What CellCog Can Do\n\n.*?\n---',
            '---',
            body,
            flags=re.DOTALL
        )
        # Remove lines referencing skills not in the plugin
        for strip_line in CELLCOG_STRIP_LINES:
            body = '\n'.join(
                line for line in body.split('\n')
                if strip_line not in line
            )
    
    # Build Open Plugins-compatible content
    open_plugins_frontmatter = build_open_plugins_frontmatter(fm)
    return open_plugins_frontmatter + body


def sync_skill(source_path: str, target_path: str, skill_name: str, dry_run: bool = False) -> bool:
    """Sync a single skill from source to target.

    Returns True if the skill was synced, False if skipped.
    """
    source_file = os.path.join(source_path, skill_name, 'SKILL.md')
    if not os.path.isfile(source_file):
        print(f"  SKIP {skill_name}: No SKILL.md found")
        return False

    if skill_name not in INCLUDED_SKILLS:
        print(f"  SKIP {skill_name}: Not in plugin skill set")
        return False

    plugin_content = render_skill(source_path, skill_name)

    # Write to target
    target_dir = os.path.join(target_path, skill_name)
    target_file = os.path.join(target_dir, 'SKILL.md')

    if dry_run:
        print(f"  SYNC {skill_name} (dry run)")
        return True

    os.makedirs(target_dir, exist_ok=True)
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(plugin_content)

    print(f"  SYNC {skill_name}")
    return True


def stale_skill_dirs(target_path: str) -> list[str]:
    """Skill folders in the plugin whose skill is no longer in the subset (removed by a sync)."""
    if not os.path.isdir(target_path):
        return []
    return sorted(
        d for d in os.listdir(target_path)
        if not d.startswith('.')
        and os.path.isfile(os.path.join(target_path, d, 'SKILL.md'))
        and d not in INCLUDED_SKILLS
    )


def openclaw_manifest_text(manifest_file: str, skills: list[str]) -> tuple[str, str]:
    """(current text, text with `skills` = the subset). OpenClaw loads exactly the folders listed there."""
    with open(manifest_file, 'r', encoding='utf-8') as f:
        current = f.read()
    data = json.loads(current)
    data['skills'] = [f'skills/{s}' for s in skills]
    return current, json.dumps(data, indent=2, ensure_ascii=False) + '\n'


def check(source: str, target: str, skills: list[str], openclaw_file: str) -> int:
    """Read-only drift check: 0 when a sync would write nothing, else 1."""
    drift = []
    for skill in skills:
        target_file = os.path.join(target, skill, 'SKILL.md')
        if not os.path.isfile(target_file):
            drift.append(f"  + {skill} (in the subset, not in the plugin yet)")
            continue
        with open(target_file, 'r', encoding='utf-8') as f:
            if f.read() != render_skill(source, skill, quiet=True):
                drift.append(f"  ~ {skill}")
    for d in stale_skill_dirs(target):
        drift.append(f"  - {d} (left the subset)")
    if os.path.isfile(openclaw_file):
        current, wanted = openclaw_manifest_text(openclaw_file, skills)
        if current != wanted:
            drift.append("  ~ openclaw.plugin.json#skills")
    if drift:
        print(f"DRIFT: {len(drift)} item(s) differ from golden + manifest")
        print('\n'.join(drift))
        return 1
    print("Check: plugin skills match golden and the manifest subset. Clean.")
    return 0


def main():
    parser = argparse.ArgumentParser(description='Sync CellCog skills to Open Plugins plugin repo')
    parser.add_argument('--source', default=None,
                        help='Source skills directory (default: auto-detect from monorepo)')
    parser.add_argument('--target', default=None,
                        help='Target skills directory (default: ./skills)')
    parser.add_argument('--manifest', default=None,
                        help='Release manifest holding plugin_skills (default: ../monorepo/md/cellcog/distribution/manifest.json)')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--dry-run', action='store_true',
                      help='Show what would be synced without writing files')
    mode.add_argument('--check', action='store_true',
                      help='Exit 1 if skills/ or openclaw.plugin.json drifted (no writes)')

    args = parser.parse_args()

    # Auto-detect paths relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    monorepo = os.path.join(os.path.dirname(repo_root), 'monorepo')

    if args.source:
        source = args.source
    else:
        # Try to find monorepo relative to plugin repo
        source = os.path.join(monorepo, 'md', 'cellcog', 'openclaw_skills')

    if args.target:
        target = args.target
    else:
        target = os.path.join(repo_root, 'skills')

    manifest = args.manifest or os.path.join(monorepo, 'md', 'cellcog', 'distribution', 'manifest.json')
    openclaw_file = os.path.join(repo_root, 'openclaw.plugin.json')

    if not os.path.isdir(source):
        print(f"ERROR: Source directory not found: {source}")
        sys.exit(2)

    subset = load_included_skills(manifest)
    INCLUDED_SKILLS.clear()
    INCLUDED_SKILLS.update(subset)
    missing = [s for s in subset if not os.path.isfile(os.path.join(source, s, 'SKILL.md'))]
    if missing:
        print(f"ERROR: plugin_skills names skill(s) with no golden SKILL.md: {', '.join(missing)}")
        sys.exit(2)

    print(f"Source: {source}")
    print(f"Target: {target}")
    print(f"Manifest: {manifest}")
    print(f"Included: {len(INCLUDED_SKILLS)} skills")
    print()

    if args.check:
        sys.exit(check(source, target, subset, openclaw_file))
    
    # Get all skill directories
    skills = sorted([
        d for d in os.listdir(source)
        if os.path.isdir(os.path.join(source, d))
        and not d.startswith('.')
        and os.path.isfile(os.path.join(source, d, 'SKILL.md'))
    ])
    
    print(f"Found {len(skills)} skills in source")
    print()
    
    synced = 0
    skipped = 0
    
    for skill in skills:
        if sync_skill(source, target, skill, dry_run=args.dry_run):
            synced += 1
        else:
            skipped += 1

    for d in stale_skill_dirs(target):
        if args.dry_run:
            print(f"  REMOVE {d} (left the subset, dry run)")
        else:
            shutil.rmtree(os.path.join(target, d))
            print(f"  REMOVE {d} (left the subset)")

    if os.path.isfile(openclaw_file):
        current, wanted = openclaw_manifest_text(openclaw_file, subset)
        if current != wanted:
            if not args.dry_run:
                with open(openclaw_file, 'w', encoding='utf-8') as f:
                    f.write(wanted)
            print(f"  WRITE openclaw.plugin.json#skills ({len(subset)} skills){' (dry run)' if args.dry_run else ''}")

    print()
    print(f"Done: {synced} synced, {skipped} skipped")


if __name__ == '__main__':
    main()
