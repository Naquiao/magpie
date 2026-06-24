# gbrain

**One-liner:** Garry Tan's opinionated self-hosted agent "brain" — markdown-in-git as the system of
record, synced into Postgres for hybrid retrieval over a **self-wiring knowledge graph**, with a
synthesis layer that returns cited answers + gap analysis and a 24/7 "dream cycle" that consolidates.

## Approach
"Search gives you raw pages; the brain gives you the answer." GBrain pairs raw retrieval with a
**synthesis layer** that composes a cited answer across results AND an explicit note on *what the
brain doesn't know yet* (gap analysis: stale pages, uncited claims, contradictions, holes). It runs
as a daemon that ingests, enriches, and consolidates continuously rather than only working inside a
chat session. (Notably, this very brain template — `index.md` + `_meta/sources.md` as the index,
the "what the brain doesn't know yet" habit, the dream-cycle/compounding idea — mirrors GBrain's
design.)

## Architecture
- **Brain repo is the system of record:** knowledge lives as markdown in a git repo; GBrain syncs it
  into Postgres for retrieval (git deletes → DB soft-deletes).
- **Two engines, one contract:** PGLite (Postgres-via-WASM, zero-config, default) up to ~50K pages;
  Postgres + pgvector (Supabase/self-hosted) for shared/large deployments. ~47-op `BrainEngine`
  interface drives both the CLI and the MCP server (30+ tools over stdio/HTTP).
- **Schema packs:** typed page kinds (`gbrain-base-v2`, 15-type taxonomy, default as of v0.41.22)
  thread through every read/write path; brains can author/switch packs.
- **Minions:** a Postgres-native, BullMQ-shaped durable job queue for crash-safe subagents/cron.

## Store / Retrieve / Update / Forget
- **Store:** `gbrain capture` / ingestion lands a page on disk + DB in one move. **Auto-link** fires
  on every page write — extracts entity refs from markdown/wikilinks/typed-link syntax and writes
  typed edges with **zero LLM calls**. See [[knowledge-graphs-for-memory]].
- **Retrieve:** **hybrid search** — vector (HNSW/pgvector) + BM25 keyword + reciprocal-rank fusion +
  source-tier boost + reranker + per-query graph signals. `gbrain search` returns raw ranked pages;
  `gbrain think` runs the same retrieval then synthesizes a cited answer + gap analysis. Multi-hop
  via `gbrain graph-query`. See [[hybrid-retrieval]] and [[read-write-agent-loop]] (brain-first lookup).
- **Update / consolidate:** the cron-driven **dream cycle** runs while you sleep — dedups people
  pages, fixes citations, scores salience, finds contradictions, preps tomorrow's tasks. See
  [[memory-consolidation]] and [[temporal-knowledge-and-decay]].
- **Forget:** git deletes become DB soft-deletes; consolidation merges duplicates.

## Tradeoffs / limits
- Self-hosted on your hardware/DB/keys (privacy + control, but you operate it); ~30-min install.
- Opinionated taxonomy/conventions; large brains need the Postgres engine, not PGLite.
- The graph is deterministic pattern-matching on link syntax (zero LLM) — fast and cheap, but
  edge recall depends on authors actually using wikilink/typed-link syntax.

## Maturity (version, adoption, as-of date)
As-of 2026-06-24: MIT-licensed; default schema pack `gbrain-base-v2` since v0.41.22. Production brain
behind the author's OpenClaw/Hermes deployments (claimed 146,646 pages / 24,585 people / 5,339
companies / 66 cron jobs). Self-reported retrieval benchmark on a 240-page rich-prose corpus:
**P@5 49.1%, R@5 97.9%**, with **+31.4 P@5** from the knowledge graph over its graph-disabled
variant and over BM25+vector-only RAG (BrainBench/`gbrain-evals`); also runs the public LongMemEval
and its own NamedThingBench. See [[memory-evaluation]].

## Sources
- `raw/articles/memory/garrytangbrain Garry's Opinionated OpenClawHermes Agent Brain.md`
  — GBrain README: hybrid search, self-wiring graph, dream cycle, synthesis + gap analysis.
