# Open Questions / Research Backlog

Maintained by the compiler during `lint`, and by you whenever something nags.

## Active
- At what scale does a plain markdown wiki + index files stop beating vector RAG?
  (Karpathy: fine at ~100 articles. Where's the breaking point — docs? tokens? query type?)
  Now sourced: [[llm-compiled-wiki]] (Karpathy, ~100 articles / ~400K words) vs. [[vector-rag]];
  [[gbrain]] is the productized "outgrown-files" answer. Breaking point still unquantified.
- How does each system handle **contradicting** facts and **staleness**? (compiled-truth +
  timeline vs overwrite vs append). Candidate first comparison article.
- Deterministic entity-edge extraction (GBrain, "zero LLM calls") vs LLM-inferred links:
  precision/recall tradeoffs? (Now have both sides — [[gbrain]] zero-LLM typed edges vs [[mem0]]
  LLM/embedding entity linking — but no head-to-head numbers. See [[knowledge-graphs-for-memory]].)
- What benchmarks actually measure agent memory well? (gather candidates, don't assume.) Started:
  see [[memory-evaluation]] (LoCoMo/LongMemEval/BEAM/BrainBench).
- In-weights (finetune) vs in-context memory: when is it worth "baking in" the knowledge?
  ([[letta]] argues for *neither* finetuning nor plain RAG but "token-space learning" — agents
  rewriting their own context.) Page now exists: [[in-weights-vs-in-context]], grounded in
  Roberts et al. 2020 (closed-book QA: viable but costly, uninterpretable, hard to update). Still
  open: how those 2020 conclusions hold at 2026 model scale, and whether model editing fixes the
  updateability gap.
- **Memory poisoning** — the Mem0 clipping's title/description promise guardrails, scoring, and
  policies against bad inputs corrupting agent memory, but its body is a pure build tutorial and
  never covers them. Need a real source on memory-poisoning attacks and defenses before writing a
  `concepts/memory-poisoning` page (don't assert from the title alone). **Partial coverage now:**
  [[vector-rag]] documents *corpus-poisoning* attacks (BadRAG, TrojanRAG) and mitigations from the
  RAG survey. Still missing: poisoning of *agent-written* memory (the Mem0 guardrails/scoring/policies
  the clipping promised) — distinct from poisoning a static retrieval corpus.
- **Temporal reasoning at scale is unsolved field-wide** — [[mem0]]'s BEAM 10M results show temporal
  reasoning, event ordering, and multi-session reasoning collapse; fact/entity-level matching isn't
  enough. What representations close this? See [[temporal-knowledge-and-decay]].
- **Benchmark gaming** — [[mem0]] notes LoCoMo/LongMemEval can be inflated by bigger context windows
  or frontier models without the memory layer improving. How much of any reported gain is the memory
  system vs. the harness? Cross-system numbers aren't directly comparable.
- **Candidate first comparison article:** how [[mem0]] / [[letta]] / [[gbrain]] each handle
  Store/Retrieve/Update/Forget side by side (all three system pages now exist).
- **Does model editing scale?** Largely answered (**no**): per the 2025–2026 research map, lifelong
  parameter editing causes catastrophic forgetting; AlphaEdit (null-space) pushes the limit but
  doesn't remove it, and RippleEdits found in-context editing beats parameter editing. Folded into
  [[model-editing]]. Still open: whether *any* parameter-editing scheme is safe at true lifelong scale.
- **Ingest Zep / Graphiti.** [[gbrain]] / [[mem0]] / [[letta]] are covered, but **Zep** (temporal
  knowledge graph, arXiv 2501.13956) — a seed system and arguably the most relevant one for the
  contradicting-facts question — still has no source. Ingest the Zep paper for a full `systems/zep.md`.
- **Agent-memory write-path security.** Beyond corpus poisoning ([[vector-rag]]), the 2026 map points
  to SSGM (stability/safety-governed memory) and memory-security surveys — candidates to ground the
  still-open *agent-written-memory* poisoning gap above.

## Answered (archive)
- **Mem0 update/forget semantics** (asked 2026-06-24) — answered same day by
  `Introducing The Token-Efficient Memory Algorithm.md`: Mem0 uses **single-pass ADD-only**
  extraction — every fact is an independent record, changed facts coexist with old ones (no
  overwrite/delete), preserving full state history. No explicit decay/expiry policy described.
  Folded into the [[mem0]] Store/Update/Forget section.
- **Portable cross-workspace project memory** (asked 2026-06-24; from `notes/Memory In Action by
  Naquiao.md`) — answered by the 2025–2026 research map: keep durable memory **external + textual**
  (embeddings are model-specific; weight editing is non-portable) and surface it over **MCP**, the
  model-agnostic standard adopted across Claude/Gemini/Cursor; re-embed locally as a disposable index.
  Page: [[portable-memory]].
- **Long-context vs. RAG** (cross-cutting) — answered: long context does *not* obviate retrieval
  (Lost-in-the-Middle, Context Rot); **hybrid** (retrieve-then-long-context-reason) is the 2026
  default. Folded into [[context-vs-retrieval]].
