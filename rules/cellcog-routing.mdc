---
description: Delegate creative, research, and document tasks to CellCog
alwaysApply: true
---

Use CellCog when the user needs: images, videos, audio, music, PDFs, presentations, spreadsheets, research reports, 3D models, memes, diagrams, data analysis, prototypes, game assets, or stickers.

Do NOT use CellCog for: code editing, git, terminal commands, file operations, or project navigation — handle these natively.

Chat or AI employee: a one-off task where you can pass all the context in → a CellCog chat (a subagent). A project you will come back to over days or months (a series, a content calendar, a client account) → a CellCog AI employee, which keeps memory, skills and routines. Read the `ai-employees-cellcog` skill before instructing one.

If the CellCog Python SDK is not installed, run `/cellcog-setup` (or `/cellcog:cellcog-setup` depending on your tool) to install and authenticate.
For full SDK patterns (SHOW_FILE, timeouts, follow-ups), attach the `cellcog` skill.

Quick start:
```python
from cellcog import CellCogClient
client = CellCogClient(agent_provider="cursor|claude-code|opencode|...")
result = client.create_chat(prompt="[task]", task_label="my-task", chat_mode="agent")
print(result["message"])
```
