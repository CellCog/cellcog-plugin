# Changelog

All notable changes to the CellCog plugin will be documented in this file.

## [2.0.0] - 2026-04-14

### Restructured to Open Plugins Standard

Universal plugin for all conformant coding agents — Cursor, Claude Code, OpenCode, and more.

**Breaking changes:**
- Moved all components from `cellcog/` subdirectory to repo root (Open Plugins standard)
- Removed `marketplace.json` (not needed for single-plugin repos)
- Repo renamed from `cellcog-cursor-plugin` to `cellcog-plugin`

**New:**
- Added vendor-neutral manifest at `.plugin/plugin.json`
- Added Claude Code manifest at `.claude-plugin/plugin.json`
- All skills, rules, and commands are now agent-agnostic
- Recovery sections updated to universal format across all 16 skills

**Skills (16):**
- `cellcog` — Core SDK reference (create_chat, file handling, chat modes, timeouts, credits)
- `video-cog` — Video production (marketing, explainers, lipsync, cinematic)
- `image-cog` — Image generation (photos, illustrations, logos, vectors)
- `audio-cog` — Audio (speech, voiceover, sound effects, dialogue, podcasts)
- `music-cog` — Music generation (any genre, 5s to 10min, royalty-free)
- `research-cog` — Deep research with citations
- `docs-cog` — Document generation (PDF, DOCX)
- `slides-cog` — Presentations and slide decks
- `spreadsheets-cog` — Spreadsheets with formulas and charts
- `proto-cog` — UI prototypes and mockups
- `3d-cog` — 3D model generation
- `meme-cog` — Meme generation
- `diagram-cog` — Diagrams (flowcharts, architecture, mind maps)
- `data-cog` — Data analysis and visualization
- `game-cog` — Game development assets and prototypes
- `sticker-cog` — Sticker packs and custom emoji

**Also includes:**
- `/cellcog-setup` command for one-step SDK installation and authentication
- Routing rule for automatic task delegation
- CellCog Python SDK integration (`pip install -U cellcog`)

## [1.0.0] - 2026-04-12

### Initial Release

CellCog plugin for the Cursor marketplace — delegate creative, research, and document tasks to CellCog from within your coding agent.
