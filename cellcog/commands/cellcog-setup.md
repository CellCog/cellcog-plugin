---
name: cellcog-setup
description: Set up CellCog (install SDK and authenticate)
---

# CellCog Setup

## Step 1: Check if SDK is installed

```bash
pip show cellcog
```

If installed, skip to **Step 2**. If not found, install it:

```bash
pip install cellcog
```

## Step 2: Check authentication

```python
from cellcog import CellCogClient
client = CellCogClient(agent_provider="cursor")
status = client.get_account_status()
print(status)
```

If the status shows `"configured": false` or the command fails with an authentication error, the user needs to set their API key:

1. Get a key from https://cellcog.ai/profile?tab=api-keys
2. Set it in the environment:

```bash
export CELLCOG_API_KEY="sk_..."
```

Then re-run the check above.

## Step 3: Verify

```python
from cellcog import CellCogClient
client = CellCogClient(agent_provider="cursor")
status = client.get_account_status()
print(f"✅ CellCog is ready! Authenticated as: {status.get('email', 'unknown')}")
```

If everything works, CellCog is ready to use. Try asking Cursor to generate an image, create a PDF, or run a research task.
