# Changelog

All notable changes to the CellCog plugin will be documented in this file.

## [2.2.1] - 2026-07-22

### OpenClaw Package Validation Fixes

ClawHub's Plugin Inspector flagged the package (`0 errors, 1 warning` on 2.1.0);
now validates clean (`clawhub package validate .` → PASS, 0 findings).

- **`package-openclaw-entry-missing`**: `openclaw.extensions` used a legacy object
  shape (`{id, kind, skills}`) that the current schema doesn't recognize as an
  entrypoint. Per the OpenClaw SDK entry points contract, `extensions` is now an
  array of entrypoint paths (`["./index.js"]`), backed by a new minimal
  `index.js` (`definePluginEntry`, registers nothing — skills-only plugin).
- Skill directories moved to `openclaw.plugin.json#skills` (the documented
  manifest field: "Skill directories to load, relative to the plugin root").
- **`package-install-metadata-incomplete`**: added `openclaw.install`
  (`clawhubSpec`, `npmSpec`, `defaultChoice: "clawhub"`, `minHostVersion`).
- **`package-npm-pack-unavailable`**: removed `private: true` so the npm
  artifact can be packed; added `index.js` to `files`; declared `openclaw`
  peer dependency.
- Validator `reports/` output gitignored.

## [2.2.0] - 2026-07-22

### Slug Migration Wave 2 (remaining 13 skills)

The 13 remaining ClawHub skills renamed to keyword slugs (`cine-cog` → `cinematic-video-cellcog`,
`insta-cog` → `instagram-reels-tiktok-cellcog`, `tube-cog` → `youtube-video-cellcog`,
`crypto-cog` → `crypto-research-cellcog`, `news-cog` → `news-briefing-cellcog`,
`learn-cog` → `tutoring-education-cellcog`, `story-cog` → `creative-writing-cellcog`,
`think-cog` → `brainstorming-strategy-cellcog`, `travel-cog` → `travel-planning-cellcog`,
`avatar-cog` → `avatar-creation-cellcog`, `code-cog` → `coding-agent-cellcog`,
`cowork-cog` → `pair-programming-cellcog`, `project-cog` → `project-management-cellcog`).
None of these are plugin skills, but the `cellcog` hub skill's cross-references and
`sync_skills.py` strip rules updated to match. All 38 CellCog skills now follow the
`<keyword-phrase>-cellcog` formula.

- Host manifests (`.plugin/`, `.claude-plugin/`, `.cursor-plugin/`) version-bumped
  (they were still at 2.0.1 — missed in the 2.1.0 release)

## [2.1.0] - 2026-07-17

### Keyword Skill Slugs (ClawHub search migration)

All 15 capability skills renamed from short `-cog` slugs to literal-keyword slugs
(`<keyword-phrase>-cellcog`) to match ClawHub's slug-token-first search ranking.
The `cellcog` hub skill is unchanged.

| Old slug | New slug |
|---|---|
| `video-cog` | `video-generation-cellcog` |
| `image-cog` | `image-generation-cellcog` |
| `audio-cog` | `audio-generation-cellcog` |
| `music-cog` | `music-generation-cellcog` |
| `research-cog` | `deep-research-cellcog` |
| `docs-cog` | `pdf-document-generation-cellcog` |
| `slides-cog` | `presentation-slides-cellcog` |
| `spreadsheets-cog` | `excel-spreadsheet-cellcog` |
| `proto-cog` | `ui-prototype-wireframe-cellcog` |
| `3d-cog` | `3d-model-generation-cellcog` |
| `meme-cog` | `meme-generator-cellcog` |
| `diagram-cog` | `diagram-flowchart-cellcog` |
| `data-cog` | `data-analysis-cellcog` |
| `game-cog` | `game-asset-generation-cellcog` |
| `sticker-cog` | `sticker-generator-cellcog` |

- Skill directories, frontmatter `name:` fields, `package.json` skill paths, README, and `sync_skills.py` updated
- Descriptions unchanged (already keyword-optimized in 2.0.1); only leading keyword phrases front-loaded where needed
- Skill H1 titles updated to keyword names

## [2.0.1] - 2026-04-14

### Optimized Skill Descriptions

- Rewrite all 16 skill descriptions for search and agent discovery
- Lead with search-optimized terms (AI [category] powered by CellCog)
- Remove marketing copy, competitive claims, and emotional hooks
- Limit #1 DeepResearch Bench claim to cellcog hub and research-cog only
- Add subcategory keywords to parent skills for broader search coverage
- Added OpenClaw native plugin support (openclaw.plugin.json + package.json)

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
