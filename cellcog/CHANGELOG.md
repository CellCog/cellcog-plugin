# Changelog

All notable changes to the CellCog Cursor plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.1] - 2026-04-12

### Added
- `cellcog` hub skill — SDK reference for create_chat, SHOW_FILE, chat modes, timeouts, credits
- HTTP 426 upgrade guidance in `/cellcog-setup`

### Changed
- Skill footers now reference `/cellcog-setup` and cellcog.ai (previously referenced missing `cellcog` skill)
- `pip install -U cellcog` (upgrade-first) across all install instructions
- Routing rule clarified: "CellCog Python SDK" not ambiguous "cellcog"

### Fixed
- CHANGELOG accuracy: benchmark claims removed from all skills except research-cog (intentional)

## [1.1.0] - 2026-04-12

### Changed
- Consolidated from 38 to 15 focused modality skills
- Updated all skill descriptions to functional, industry-friendly format with "Powered by CellCog." prefix
- Shortened routing rule to ~15 lines
- Removed marketing copy, benchmark claims, and superlatives from skill bodies (except research-cog)
- Softened music-cog licensing language (tied to CellCog ToS)
- Fixed video-cog uniqueness claim
- Aligned marketplace.json description with 15-skill reality

## [1.0.0] - 2026-04-12

### Added
- Initial release of the CellCog Cursor plugin
- 15 capability skills: video, image, audio, music, research, docs, slides, spreadsheets, proto, 3d, meme, diagram, data, game, sticker
- Routing rule for automatic task delegation
- `/cellcog-setup` command for SDK installation
- CellCog logo and MIT license
