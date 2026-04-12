---
name: cellcog-setup
description: Set up the CellCog Python SDK (install and authenticate)
---

# CellCog Setup

## Step 1: Check if the CellCog Python SDK is installed

```bash
pip show cellcog
```

If installed, skip to **Step 2**. If not found, install it:

```bash
pip install -U cellcog
```

Note: Use the same Python interpreter that Cursor uses. If you're in a virtual environment, make sure it's activated.

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

For persistent setup, add the export to `~/.zshrc` or `~/.bashrc`, or use Cursor's environment settings.

Then re-run the check above.

## Step 3: Verify

```python
import cellcog
print(f"CellCog SDK version: {cellcog.__version__}")

from cellcog import CellCogClient
client = CellCogClient(agent_provider="cursor")
status = client.get_account_status()
print(f"Authenticated as: {status.get('email', 'unknown')}")
print("CellCog is ready to use!")
```

## If the API returns HTTP 426

The CellCog server enforces a minimum SDK version. If you see `sdk_upgrade_required`, upgrade:

```bash
pip install -U cellcog
```

The error response includes the `minimum_version` required.
