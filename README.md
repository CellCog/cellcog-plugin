# CellCog — Any-to-Any AI Sub-Agent Plugin

Generate images, videos, PDFs, presentations, research reports, music, spreadsheets, 3D models, memes, diagrams, prototypes, game assets, stickers, and more — all from natural language prompts inside your coding agent.

CellCog orchestrates 21+ foundation models so you can produce rich media deliverables without leaving your IDE.

**Works with:** [Cursor](https://cursor.com) · [Claude Code](https://code.claude.com) · [OpenClaw](https://openclaw.ai) · [OpenCode](https://opencode.ai) · Any [Open Plugins](https://open-plugins.com) conformant tool

## Quick Start

### 1. Install the Plugin

**Cursor:**
```
/add-plugin cellcog
```

**Claude Code:**
```bash
claude plugin install https://github.com/CellCog/cellcog-plugin
```

**OpenClaw:**
```bash
openclaw plugins install https://github.com/CellCog/cellcog-plugin
```

**Other tools:** Clone or point your tool's plugin loader at this repo.

### 2. Install the CellCog Python SDK

```bash
pip install -U cellcog
export CELLCOG_API_KEY="sk_..."  # Get from https://cellcog.ai/profile?tab=api-keys
```

Or run `/cellcog-setup` (or `/cellcog:cellcog-setup`) for guided installation.

### 3. Use CellCog

Ask your coding agent to generate any rich media — the plugin automatically routes tasks to CellCog:

> "Create a 30-second marketing video for our new fitness app"

> "Research quantum computing advances in 2026 with citations"

> "Design logo concepts and a one-pager PDF for my coffee shop"

## Remote MCP connector (Claude web, Desktop, Cowork, Claude Code, Cursor)

The plugin also references CellCog's remote MCP server, so once it is installed the CellCog connector is available on every Claude surface. On first use you sign in with your own CellCog account (OAuth); no API key, nothing to install in a sandbox.

- **Claude web / Desktop:** Settings > Connectors > Add custom connector > `https://cellcog.ai/mcp`
- **Claude Code:** `claude mcp add --transport http cellcog https://cellcog.ai/mcp`
- **Cursor and other MCP clients:** add `https://cellcog.ai/mcp` as a remote (streamable HTTP) server; sign in when asked
- **Team / Enterprise admins:** distribute this plugin org-wide from Organization settings > Plugins: add it to your organization's own (private) marketplace as a `github` source `CellCog/cellcog-plugin`, or upload the plugin ZIP directly; every member still signs in as themselves and is billed on their own account. Claude Code users can also run `claude plugin marketplace add CellCog/cellcog-plugin` (this repo ships a `.claude-plugin/marketplace.json`).

Tools: `cellcog_create_chat`, `cellcog_send_message`, `cellcog_request_upload` (an upload window for files on your computer), `cellcog_get_status`, `cellcog_get_result` (files come back as links that stay valid for 30 days and render inline in Claude web and Desktop), `cellcog_list_chats`, `cellcog_account`. Manage or disconnect connected apps at https://cellcog.ai/profile?tab=api-keys.

## Skills

| Skill | What It Does |
|-------|-------------|
| `video-generation-cellcog` | Video production — marketing, explainers, lipsync, cinematic |
| `image-generation-cellcog` | Image generation — photos, illustrations, logos, vectors |
| `audio-generation-cellcog` | Speech, voiceover, sound effects, dialogue, podcasts |
| `music-generation-cellcog` | Original music — any genre, any duration, royalty-free |
| `deep-research-cellcog` | Deep research with citations |
| `pdf-document-generation-cellcog` | PDF and document generation |
| `presentation-slides-cellcog` | Presentations and slide decks |
| `excel-spreadsheet-cellcog` | Spreadsheets with formulas and charts |
| `ui-prototype-wireframe-cellcog` | UI prototypes and mockups |
| `3d-model-generation-cellcog` | 3D model generation |
| `meme-generator-cellcog` | Meme generation |
| `diagram-flowchart-cellcog` | Flowcharts, architecture, mind maps |
| `data-analysis-cellcog` | Data analysis and visualization |
| `game-asset-generation-cellcog` | Game assets, GDDs, playable prototypes |
| `sticker-generator-cellcog` | Sticker packs and custom emoji |
| `cellcog` | SDK reference — create_chat, files, modes, timeouts, credits |


## Plugin Structure

This plugin follows the [Open Plugins](https://open-plugins.com) standard for cross-tool compatibility.

```
cellcog-plugin/
├── .plugin/plugin.json           # Vendor-neutral manifest (Open Plugins)
├── .cursor-plugin/plugin.json    # Cursor manifest
├── .claude-plugin/plugin.json    # Claude Code manifest
├── openclaw.plugin.json          # OpenClaw manifest
├── package.json                  # OpenClaw package metadata
├── assets/logo.png               # Plugin logo
├── skills/                       # 16 curated skills
├── rules/cellcog-routing.mdc     # Auto-routes tasks to CellCog
├── commands/cellcog-setup.md     # /cellcog-setup (install + auth)
├── CHANGELOG.md
├── LICENSE
└── README.md
```

## Links

- **Website**: https://cellcog.ai
- **SDK**: https://pypi.org/project/cellcog/
- **API Keys**: https://cellcog.ai/profile?tab=api-keys
- **Open Plugins Spec**: https://open-plugins.com

## License

MIT
