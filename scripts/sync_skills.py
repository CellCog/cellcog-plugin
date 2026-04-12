#!/usr/bin/env python3
"""
Sync CellCog skills from the monorepo to the Cursor plugin repo.

Reads SKILL.md files from the monorepo's openclaw_skills directory,
strips ClawHub-specific YAML frontmatter fields (keeping only name
and description which both Cursor and ClawHub support), and writes
the result to the plugin repo's skills directory.

Usage:
    python3 scripts/sync_skills.py [--source PATH] [--target PATH] [--dry-run]

Defaults:
    --source: ../monorepo/md/cellcog/openclaw_skills
    --target: ./cellcog/skills
"""

import argparse
import os
import re
import shutil
import sys


# Skills to exclude from the Cursor plugin entirely
EXCLUDED_SKILLS = set()
# Note: We include all skills including cellcog and cowork-cog.
# The cellcog skill content itself handles platform-specific messaging.


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


def build_cursor_frontmatter(fm: dict) -> str:
    """Build a Cursor-compatible YAML frontmatter with only name and description."""
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


def sync_skill(source_path: str, target_path: str, skill_name: str, dry_run: bool = False) -> bool:
    """Sync a single skill from source to target.
    
    Returns True if the skill was synced, False if skipped.
    """
    source_file = os.path.join(source_path, skill_name, 'SKILL.md')
    if not os.path.isfile(source_file):
        print(f"  SKIP {skill_name}: No SKILL.md found")
        return False
    
    if skill_name in EXCLUDED_SKILLS:
        print(f"  SKIP {skill_name}: Excluded")
        return False
    
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    fm, raw_fm, body = parse_frontmatter(content)
    
    if not fm.get('name'):
        print(f"  WARN {skill_name}: No name in frontmatter, using directory name")
        fm['name'] = skill_name
    
    # Build Cursor-compatible content
    cursor_frontmatter = build_cursor_frontmatter(fm)
    cursor_content = cursor_frontmatter + body
    
    # Write to target
    target_dir = os.path.join(target_path, skill_name)
    target_file = os.path.join(target_dir, 'SKILL.md')
    
    if dry_run:
        print(f"  SYNC {skill_name} (dry run)")
        return True
    
    os.makedirs(target_dir, exist_ok=True)
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(cursor_content)
    
    print(f"  SYNC {skill_name}")
    return True


def main():
    parser = argparse.ArgumentParser(description='Sync CellCog skills to Cursor plugin')
    parser.add_argument('--source', default=None,
                        help='Source skills directory (default: auto-detect from monorepo)')
    parser.add_argument('--target', default=None,
                        help='Target skills directory (default: ./cellcog/skills)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be synced without writing files')
    
    args = parser.parse_args()
    
    # Auto-detect paths relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    
    if args.source:
        source = args.source
    else:
        # Try to find monorepo relative to plugin repo
        monorepo = os.path.join(os.path.dirname(repo_root), 'monorepo')
        source = os.path.join(monorepo, 'md', 'cellcog', 'openclaw_skills')
    
    if args.target:
        target = args.target
    else:
        target = os.path.join(repo_root, 'cellcog', 'skills')
    
    if not os.path.isdir(source):
        print(f"ERROR: Source directory not found: {source}")
        sys.exit(1)
    
    print(f"Source: {source}")
    print(f"Target: {target}")
    print(f"Excluded: {EXCLUDED_SKILLS or 'none'}")
    print()
    
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
    
    print()
    print(f"Done: {synced} synced, {skipped} skipped")


if __name__ == '__main__':
    main()
