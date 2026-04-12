---
name: cellcog
description: "CellCog SDK patterns and reference. How to use create_chat, file handling (SHOW_FILE/GENERATE_FILE), chat modes, timeouts, and credits. Attach this skill for cross-cutting SDK guidance."
---

# CellCog — SDK Reference for Cursor

## Quick Start

```python
from cellcog import CellCogClient

client = CellCogClient(agent_provider="cursor")
result = client.create_chat(
    prompt="Your task description here",
    task_label="my-task",
    chat_mode="agent",
    timeout=1800,  # 30 min default. Use 3600 for complex jobs.
)
print(result["message"])  # Always print the full message
```

## Response Shape

Every SDK method returns:
```python
{
    "chat_id": str,        # CellCog chat ID
    "is_operating": bool,  # True = still working, False = done
    "status": str,         # "completed" | "timeout" | "operating"
    "message": str,        # THE printable message — always print in full
}
```

## File Handling

**Send files to CellCog** — wrap paths in SHOW_FILE tags (absolute paths required):
```python
prompt = """
Analyze this data:
<SHOW_FILE>/path/to/sales.csv</SHOW_FILE>
"""
```

**Request output files** — use GENERATE_FILE tags:
```python
prompt = """
Create a PDF report:
<GENERATE_FILE>/workspace/reports/q4_analysis.pdf</GENERATE_FILE>
"""
```

## Chat Modes

| Mode | Best For | Speed |
|------|----------|-------|
| `"agent"` | Most tasks — images, audio, dashboards, spreadsheets | Fast |
| `"agent team"` | Deep research, multi-angled reasoning | Slower (5-60 min) |
| `"agent team max"` | High-stakes work, maximum depth | Slowest |

## Follow-Up Messages

```python
result = client.send_message(
    chat_id="abc123",
    message="Now create a PDF summary of the findings",
)
```

## Long-Running Jobs

For complex tasks (videos, deep research), increase the timeout:
```python
result = client.create_chat(
    prompt="Create a 3-minute cinematic video...",
    task_label="video-project",
    chat_mode="agent team",
    timeout=3600,  # 60 minutes
)
```

If a call times out, CellCog is still working. Resume with:
```python
result = client.wait_for_completion(chat_id="abc123", timeout=1800)
```

## Credits

CellCog orchestrates 21+ foundation models. Credit consumption varies by task complexity and is reported in every response. Check your balance at https://cellcog.ai/profile.

## If CellCog is not installed

Run `/cellcog-setup` to install and authenticate, or manually:
```bash
pip install -U cellcog
export CELLCOG_API_KEY="sk_..."  # Get from https://cellcog.ai/profile?tab=api-keys
```
