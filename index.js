// OpenClaw runtime entrypoint for the CellCog plugin.
//
// This plugin ships skills only (declared in openclaw.plugin.json#skills) —
// it registers no runtime tools, channels, or providers. This entry exists to
// satisfy the OpenClaw package entrypoint contract (package.json#openclaw.extensions);
// skill loading is handled by the manifest, not this file.
import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";

export default definePluginEntry({
  id: "cellcog",
  name: "CellCog",
  description:
    "Any-to-any AI sub-agent — generate images, videos, PDFs, presentations, research reports, music, spreadsheets, 3D models, memes, diagrams, prototypes, game assets, and stickers from natural language prompts.",
  register() {
    // Skills-only plugin: nothing to register at runtime.
  },
});
