# CellCog Cursor Plugin

This repository contains the [CellCog](https://cellcog.ai) plugin for the [Cursor](https://cursor.com) marketplace.

## What is CellCog?

CellCog is an any-to-any AI sub-agent that generates images, videos, PDFs, presentations, research reports, music, spreadsheets, 3D models, memes, diagrams, prototypes, game assets, stickers, and more — all from natural language prompts.

## Installation

In Cursor:
```
/add-plugin cellcog
```

## Plugin Structure

```
cellcog/                        # The plugin
├── .cursor-plugin/
│   └── plugin.json             # Plugin manifest (v1.0.0)
├── assets/
│   └── logo.png                # CellCog logo (full-bleed, dark bg)
├── skills/                     # 16 curated skills
│   ├── cellcog/                # Core — SDK reference, file handling, chat modes
│   ├── video-cog/              # Video production
│   ├── image-cog/              # Image generation
│   ├── audio-cog/              # Audio, speech, podcasts
│   ├── music-cog/              # Music generation
│   ├── research-cog/           # Deep research
│   ├── docs-cog/               # Document generation
│   ├── slides-cog/             # Presentations
│   ├── spreadsheets-cog/       # Spreadsheets
│   ├── proto-cog/              # UI prototypes
│   ├── 3d-cog/                 # 3D models
│   ├── meme-cog/               # Memes
│   ├── diagram-cog/            # Diagrams
│   ├── data-cog/               # Data analysis
│   ├── game-cog/               # Game development
│   └── sticker-cog/            # Stickers
├── rules/
│   └── cellcog-routing.mdc     # Routes tasks to CellCog
├── commands/
│   └── cellcog-setup.md        # /cellcog-setup (install + auth)
└── README.md                   # Plugin documentation
```

## Development

### Syncing Skills from Monorepo

Skills are authored in the CellCog monorepo (38 skills) and a curated subset of 16 is synced to this repo:

```bash
python3 scripts/sync_skills.py
```

The sync script strips ClawHub-specific YAML frontmatter (keeping only `name` and `description`) and applies an `INCLUDED_SKILLS` whitelist. The `cellcog` core skill also has its cross-selling grid stripped during sync.

### Updating the Icon

The plugin icon is generated from the CellCog light logo on a dark background (full-bleed, 88% logo scale):

```bash
# From the monorepo — regenerate all icons including Cursor
python3 electron/cellcog-desktop/scripts/generate_icons.py

# Copy the Cursor-specific icon (full-bleed, no macOS padding) to this repo
cp electron/cellcog-desktop/build/icon-cursor.png cellcog/assets/logo.png
```

## License

MIT
