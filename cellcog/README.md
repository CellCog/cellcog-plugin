# CellCog — Any-to-Any AI Sub-Agent for Cursor

Generate images, videos, PDFs, presentations, research reports, podcasts, music, spreadsheets, dashboards, 3D models, memes, and more — all from natural language prompts inside Cursor.

CellCog orchestrates 21+ foundation models so you can produce rich media deliverables without leaving your IDE. **#1 on [DeepResearch Bench](https://huggingface.co/spaces/muset-ai/DeepResearch-Bench-Leaderboard)** (Apr 2026).

## Quick Start

### 1. Install the Plugin

```
/add-plugin cellcog
```

### 2. Install the CellCog SDK

```bash
pip install cellcog
```

### 3. Set Your API Key

```bash
export CELLCOG_API_KEY="sk_..."
```

Get your key from: https://cellcog.ai/profile?tab=api-keys

### 4. Use CellCog

Ask Cursor to generate any rich media — the plugin automatically routes creative, research, and document tasks to CellCog:

> "Create a 30-second marketing video for our new fitness app"

> "Research quantum computing advances in 2026 and create a PDF report with citations"

> "Generate a brand identity for my coffee shop — logo, color palette, and guidelines"

> "Create an interactive dashboard showing our Q4 sales data"

## What You Can Create

| Category | Skills | Examples |
|----------|--------|---------|
| **Research & Analysis** | `research-cog` `fin-cog` `crypto-cog` `data-cog` `news-cog` | Deep research with citations, stock analysis, market intelligence |
| **Video & Cinema** | `video-cog` `cine-cog` `insta-cog` `tube-cog` `seedance-cog` | Marketing videos, explainers, lipsync, social media |
| **Images & Design** | `image-cog` `brand-cog` `meme-cog` `banana-cog` `3d-cog` `gif-cog` `sticker-cog` | Photos, illustrations, logos, icons, vectors, 3D models |
| **Audio & Music** | `audio-cog` `music-cog` `pod-cog` | Speech, voiceovers, music, podcasts, sound effects |
| **Documents & Slides** | `docs-cog` `slides-cog` `spreadsheets-cog` `resume-cog` `legal-cog` | PDFs, presentations, spreadsheets, resumes, contracts |
| **Apps & Prototypes** | `dash-cog` `game-cog` `proto-cog` `diagram-cog` | Dashboards, games, UI prototypes, flowcharts |
| **Creative** | `comi-cog` `story-cog` `learn-cog` `travel-cog` | Comics, storytelling, education, travel planning |
| **Development** | `code-cog` `cowork-cog` `project-cog` `think-cog` | Coding agent, co-work, knowledge workspaces |

## Chat Modes

| Mode | Best For | Speed |
|------|----------|-------|
| `"agent"` | Most tasks — images, audio, dashboards, spreadsheets | Fast (seconds to minutes) |
| `"agent team"` | Deep research & multi-angled reasoning | Slower (5-60 min) |
| `"agent team max"` | High-stakes work where extra depth justifies cost | Slowest |

## How It Works

CellCog is a **sub-agent** — your Cursor agent offloads complex work to CellCog, which reasons, plans, and executes multi-tool workflows internally. A proprietary agent-to-agent protocol ensures high accuracy, and because these are agent threads (not stateless API calls), every aspect of every generation can be refined through multi-step iteration.

```python
from cellcog import CellCogClient

client = CellCogClient(agent_provider="cursor")
result = client.create_chat(
    prompt="Create a PDF executive summary of Q4 earnings with charts",
    task_label="q4-report",
    chat_mode="agent",
)
print(result["message"])  # Always print the full message
```

## Links

- **Website**: https://cellcog.ai
- **SDK**: https://pypi.org/project/cellcog/
- **API Keys**: https://cellcog.ai/profile?tab=api-keys
- **ClawHub Skills**: https://clawhub.ai (search: cellcog)
- **Support**: https://cellcog.ai/support
