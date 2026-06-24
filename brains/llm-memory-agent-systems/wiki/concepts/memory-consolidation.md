# memory-consolidation

**One-liner:** Background, off-the-request-path processing that reorganizes, summarizes, dedups, and
reconciles stored memory over time — the "dream cycle" / sleep-time reflection.

## What it is
Memory that is only ever appended degrades: it accumulates duplicates, stale facts, broken
citations, and contradictions. Consolidation is a separate (often scheduled or "sleep-time") pass
that cleans and restructures the store, distinct from the synchronous read-before-respond /
write-after-learn loop ([[read-write-agent-loop]]).

## Why it matters for agent memory
Long-horizon agents accumulate mess faster than any single request can fix. Consolidation is what
keeps a growing memory *usable*: it fights entropy, surfaces higher-order patterns ("this user loves
Thai food" from eight Friday orders), repairs provenance, and flags conflicts before they corrupt
answers. Running it offline keeps the latency-sensitive request path cheap.

## Variants / approaches
- **Scheduled "dream cycle"** — [[gbrain]] runs cron jobs while you sleep: dedup people pages, fix
  citations, score salience, find contradictions, prep tomorrow's tasks.
- **Sleep-time reflection** — [[letta]] runs a background subagent that periodically reviews recent
  conversation history and persists important info into the git memory repo (in a worktree, merged
  back automatically).
- **Defragmentation** — [[letta]] reorganizes the memory filesystem into ~15–25 focused files
  (split large, merge duplicates) with a backup first.
- **Async extraction** — [[mem0]] runs extraction/retrieval asynchronously; its single-pass ADD-only
  design intentionally defers reconciliation, keeping both old and new facts.
- **Reflection** — Generative Agents (Park, UIST 2023) periodically synthesize higher-level insights
  from the memory stream; ablating reflection degraded coherent behavior within ~48 simulated hours.
- **Learned forgetting** — MemoryBank (AAAI 2024) applies an **Ebbinghaus forgetting curve** to decay
  memories over time (vs. the heuristic forget rules elsewhere).
- **Memory evolution** — [[a-mem]]: adding a new note triggers the LLM to **rewrite the attributes
  (context/keywords/tags) of linked existing notes** — consolidation as a continuous side-effect of
  writing, not a separate batch pass.

## Which systems use it
- [[gbrain]] — cron dream cycle. [[letta]] — sleep-time reflection + defragmentation.
  [[mem0]] — async extraction/retrieval. [[a-mem]] — write-triggered memory evolution.

## Open questions
- How aggressive should consolidation be before it destroys recoverable detail? (Letta's ADD-then-
  defrag and Mem0's ADD-only both lean conservative; see [[temporal-knowledge-and-decay]].)
- Can consolidation reliably resolve contradictions, or only flag them? (See `_meta/open-questions.md`.)
- **Episodic→semantic consolidation and learned forgetting remain largely heuristic** — flagged as a
  top open problem across the 2026 agent-memory surveys.

## Sources
- `raw/articles/memory/garrytangbrain Garry's Opinionated OpenClawHermes Agent Brain.md` — dream cycle.
- `raw/articles/memory/Introducing Context Repositories Git-based Memory for Coding Agents.md`
  — sleep-time reflection, memory defragmentation.
- `raw/articles/memory/Context Constitution.md` — sleep-time compute for reflection/organization.
- `raw/articles/memory/Introducing The Token-Efficient Memory Algorithm.md` — async extraction.
- `raw/articles/memory/LLM Memory and Knowledge: A 2025–2026 Research Map Across Four Threads.md`
  — Thread 4: Generative Agents reflection, MemoryBank Ebbinghaus forgetting, consolidation as open problem.
- `raw/papers/Generative Agents Interactive Simulacra of Human Behavior.md` — reflection synthesizes
  higher-level insights; ablation showed it is critical to believable behavior.
- `raw/papers/A-Mem Agentic Memory for LLM Agents.md` — memory evolution (new notes update old ones).
