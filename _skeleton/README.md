# {{BRAIN_NAME}}

A self-compiling knowledge brain (Karpathy-style). You collect sources; an LLM agent writes
the wiki. See `BRAIN.md` for this brain's topic/scope and `AGENTS.md` for how the agent works.

## Daily loop
1. **Dump** sources into `raw/` (papers, web clips, repo summaries, notes). No organizing.
2. **Compile:** from this folder, run your CLI agent and say:
   `compile any new sources in raw/ into the wiki`
3. **Ask:** `ask: <your research question>` → cited answer, optionally rendered to `outputs/`.
4. **Lint** occasionally: `audit the wiki for gaps and contradictions`.

## Setup
- Open this folder as a vault in **Obsidian** (viewing/graph). Optional: Web Clipper + Marp plugins.
- Run a CLI coding agent (Claude Code / Codex) from this folder as the "engine".
- Ingest papers fast: `python scripts/ingest_arxiv.py <arxiv_id>` (see `scripts/`).
