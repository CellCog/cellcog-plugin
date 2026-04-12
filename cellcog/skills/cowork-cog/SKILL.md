---
name: cowork-cog
description: "CellCog on your machine. Turn any computer into CellCog's workspace — code, debug, refactor, and build directly on the user's machine. Auto-approved for agents, no manual intervention. CellCog Desktop bridge for terminal, file access, and full development workflows. AI pair programming, remote coding agent."
---
# Cowork Cog — CellCog on Your Machine

Co-work turns any machine into CellCog's workspace. CellCog Desktop acts as a bridge: CellCog's cloud agents coordinate with the desktop app to run commands, read files, and write code directly on the user's machine.

All commands are **auto-approved** for SDK/agent users — fully autonomous, no manual approval needed.

## Prerequisites

This skill requires the `cellcog` skill for SDK setup and API calls.

```bash
clawhub install cellcog
```

---

## Why Co-work?

### Your Machine as a Data Source
Your data lives on the user's machine — project files, databases, logs, configs. Instead of uploading everything, enable co-work with a working directory and CellCog agents explore, read, and reason about the data directly. No file size limits, no upload hassle.

### CellCog as Your Coding Powerhouse
CellCog agents are among the most capable coding agents available — deep reasoning paired with real execution. Enable co-work and delegate complex coding tasks: build websites, APIs, fix bugs, refactor codebases, set up infrastructure.

**CellCog itself is built using this exact co-work capability.**

Think of it as a Claude Code or Cursor alternative, backed by CellCog's multi-agent depth and any-to-any engine.

---

## Quick Start

```python
from cellcog import CellCogClient

client = CellCogClient(agent_provider="openclaw")

# 1. Check if desktop app is connected
status = client.get_desktop_status()

# 2. If not connected, get install instructions
if not status["connected"]:
    info = client.get_desktop_download_urls()
    # info contains per-platform URLs + install commands
    # Run the install commands for the user's OS, then:
    # cellcog-desktop --set-api-key <CELLCOG_API_KEY>
    # cellcog-desktop --start

# 3. Create a co-work chat

# OpenClaw agents (fire-and-forget):
result = client.create_chat(
    prompt="Refactor the auth module to use JWT tokens",
    notify_session_key="agent:main:main",  # OpenClaw only
    chat_mode="agent core",
    enable_cowork=True,
    cowork_working_directory="/Users/me/project",
    task_label="refactor-auth",
)

# All other agents (blocks until done):
result = client.create_chat(
    prompt="Refactor the auth module to use JWT tokens",
    chat_mode="agent core",
    enable_cowork=True,
    cowork_working_directory="/Users/me/project",
    task_label="refactor-auth",
)
```

---

## Desktop App Setup

Call `client.get_desktop_download_urls()` — returns download URLs and platform-specific install commands for macOS, Windows, and Linux.

After installation:
```bash
cellcog-desktop --set-api-key <CELLCOG_API_KEY>
cellcog-desktop --start
```

The agent can do all of this programmatically — no human interaction needed beyond providing the API key.

Alternatively, ask your human to download CellCog Desktop from `cellcog.ai/cowork`, open it, and enter their API key.

---

## Desktop CLI Reference

All commands output JSON for easy agent parsing:

| Command | What it does |
|---------|-------------|
| `cellcog-desktop --set-api-key <key>` | Authenticate with API key |
| `cellcog-desktop --status` | Check connection + app state |
| `cellcog-desktop --start` / `--stop` | App lifecycle |
| `cellcog-desktop --logs` | Debug logs |

---

## Chat Mode for Co-work

Use `"agent core"` mode for coding tasks — lightweight context focused on code, terminal, and file operations. Multimedia tools load on demand when needed.

```python
result = client.create_chat(
    prompt="Your coding task",
    chat_mode="agent core",
    enable_cowork=True,
    cowork_working_directory="/Users/me/project",
    task_label="my-task",
)
```

`"agent"` mode also works with co-work but loads all multimedia tools upfront. Use `"agent core"` for faster, more focused coding sessions.

See the **cellcog** skill for complete SDK API reference — delivery modes, `send_message()`, timeouts, and more.

---

## Error Recovery

If the desktop app disconnects, CellCog auto-fails pending commands with a clear message.

To recover:
```bash
cellcog-desktop --stop && cellcog-desktop --start
```

Then send `continue` to the chat:
```python
client.send_message(chat_id="abc123", message="continue")
```

---

## Security

Even with auto-approve, these protections are always active:
- **Blocked paths**: `~/.ssh`, `~/.aws`, credential files are inaccessible
- **Output redaction**: Sensitive data is automatically redacted from command output
- **Per-chat scoping**: Each chat session is scoped to its working directory

---

## What You Can Build

Co-work enables the full spectrum of development tasks:

- **Web development** — Build React apps, APIs, landing pages
- **Bug fixing** — Debug stack traces, fix test failures
- **Refactoring** — Modernize codebases, improve architecture
- **DevOps** — Set up CI/CD, Docker configs, infrastructure
- **Data pipelines** — ETL scripts, database migrations
- **Documentation** — Generate docs from code, README files

For the best coding experience, also install `code-cog`:
```bash
clawhub install code-cog
```

