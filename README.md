# Magpie - Brain Template

A reusable template for spinning up **multiple** Karpathy-style knowledge brains — one per
topic. You collect raw sources; an LLM agent compiles and maintains the wiki. You rarely
write the wiki by hand.

## The core idea: engine vs config
- **`_skeleton/AGENTS.md`** — the *engine*. Generic compiler/librarian rules. Identical in
  every brain. You don't change this per topic.
- **`_skeleton/BRAIN.md`** — the *config*. Topic, scope, page templates, seed concepts.
  **This is the only file you edit to specialize a brain.**

Swap `BRAIN.md`, keep `AGENTS.md` → a new brain for any topic.

## Layout
```
magpie-template/
├── new-brain.sh        # generator: stamps out a new brain from _skeleton/
├── _skeleton/          # canonical structure copied into each new brain
│   ├── AGENTS.md       # the engine (generic)
│   ├── BRAIN.md        # the config (per-topic; placeholders)
│   ├── raw/            # you dump sources here (append-only)
│   ├── wiki/           # LLM-authored output (+ _meta/ index files)
│   ├── outputs/        # query renders (Marp slides, matplotlib figures)
│   └── scripts/        # ingest_arxiv.py + friends
└── brains/             # your instantiated brains live here
    └── llm-memory-agent-systems/   # worked example (see its BRAIN.md)
```

## Quickstart
```bash
./new-brain.sh "My Topic"          # creates brains/my-topic/
# edit brains/my-topic/BRAIN.md
# open brains/my-topic/ in Obsidian, dump into raw/, run your CLI agent
```

## How a brain runs (per brain)
1. **Ingest** — sources into `raw/` (Obsidian Web Clipper for web; `ingest_arxiv.py` for papers).
2. **Compile** — agent reads `AGENTS.md`+`BRAIN.md`, turns new `raw/` files into wiki pages.
3. **Ask** — query the wiki; get cited answers + gap analysis, rendered to `outputs/`.
4. **Lint** — periodic health checks for gaps/contradictions; file good outputs back in.
