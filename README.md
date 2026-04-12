# CellCog Cursor Plugin

This repository contains the [CellCog](https://cellcog.ai) plugin for the [Cursor](https://cursor.com) marketplace.

## What is CellCog?

CellCog is an any-to-any AI sub-agent that generates images, videos, PDFs, presentations, research reports, podcasts, music, spreadsheets, dashboards, 3D models, and more — all from natural language prompts. #1 on [DeepResearch Bench](https://huggingface.co/spaces/muset-ai/DeepResearch-Bench-Leaderboard).

## Installation

In Cursor:
```
/add-plugin cellcog
```

## Plugin Structure

```
cellcog/                    # The plugin
├── .cursor-plugin/
│   └── plugin.json         # Plugin manifest
├── assets/
│   └── logo.png            # CellCog logo
├── skills/                 # 38 capability skills
│   ├── cellcog/            # Mothership — SDK setup, auth, API reference
│   ├── video-cog/          # Video production
│   ├── research-cog/       # Deep research
│   ├── image-cog/          # Image generation
│   └── ...                 # 34 more skills
├── rules/
│   └── cellcog-routing.mdc # Routes tasks to CellCog
└── README.md               # Plugin documentation
```

## Development

### Syncing Skills from Monorepo

Skills are authored in the CellCog monorepo and synced to this repo using:

```bash
python3 scripts/sync_skills.py
```

This strips ClawHub-specific YAML frontmatter, keeping only `name` and `description` (which both Cursor and ClawHub require).

### Updating the Icon

The plugin icon is generated from the CellCog light logo on a dark background. To regenerate:

```bash
# From the monorepo
python3 electron/cellcog-desktop/scripts/generate_icons.py
# Then copy to this repo
cp electron/cellcog-desktop/build/icon.png ../cellcog-cursor-plugin/cellcog/assets/logo.png
```

## License

MIT
