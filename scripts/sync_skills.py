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

Usage:
    python3 scripts/sync_skills.py [--source PATH] [--target PATH] [--dry-run]

Defaults:
    --source: ../monorepo/md/cellcog/openclaw_skills
    --target: ./skills
"""

import argparse
import os
import re
import shutil
import sys


# Skills to INCLUDE in the Open Plugins plugin (curated subset of 38 ClawHub skills)
# Only high-level modality skills — no niche/marketing variants
INCLUDED_SKILLS = {
    'cellcog',            # Core skill — SDK reference, file handling, chat modes, timeouts
    'video-cog',          # Video production (covers cinematic, social, YouTube, lipsync)
    'image-cog',          # Image generation (covers branding, vectors, photos)
    'audio-cog',          # Speech, SFX, dialogue, podcasts
    'music-cog',          # Music generation
    'research-cog',       # Deep research (covers finance, crypto, news)
    'docs-cog',           # Documents (covers resumes, legal)
    'slides-cog',         # Presentations
    'spreadsheets-cog',   # Spreadsheets
    'proto-cog',          # Prototypes, UI mockups
    '3d-cog',             # 3D models
    'meme-cog',           # Memes
    'diagram-cog',        # Diagrams
    'data-cog',           # Data analysis
    'game-cog',           # Game development
    'sticker-cog',        # Stickers
}

# Content to strip from cellcog skill during sync
# The cross-selling grid references skills not in the plugin
CELLCOG_STRIP_PATTERN = r'## What CellCog Can Do\n\n.*?\n---'

# Lines to strip from cellcog skill body (references to skills not in plugin)
CELLCOG_STRIP_LINES = [
    'install project-cog for details',
    'install cowork-cog for details',
    'install code-cog for details',
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
    
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    fm, raw_fm, body = parse_frontmatter(content)
    
    if not fm.get('name'):
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
    plugin_content = open_plugins_frontmatter + body
    
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


def main():
    parser = argparse.ArgumentParser(description='Sync CellCog skills to Open Plugins plugin repo')
    parser.add_argument('--source', default=None,
                        help='Source skills directory (default: auto-detect from monorepo)')
    parser.add_argument('--target', default=None,
                        help='Target skills directory (default: ./skills)')
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
        target = os.path.join(repo_root, 'skills')
    
    if not os.path.isdir(source):
        print(f"ERROR: Source directory not found: {source}")
        sys.exit(1)
    
    print(f"Source: {source}")
    print(f"Target: {target}")
    print(f"Included: {len(INCLUDED_SKILLS)} skills")
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
