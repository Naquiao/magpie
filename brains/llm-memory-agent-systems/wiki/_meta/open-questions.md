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
  **Update (audit #4573):** the [[mem0]] audit documents *accidental self-poisoning* — a hallucinated
  fact recalled into context and re-extracted amplifies into 808 copies — plus security leaks (IPs,
  chat IDs, config values reaching the store). That's the feedback-loop failure mode; *adversarial*
  agent-written-memory poisoning is still ungrounded. See [[memory-curation]].
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
- **Cross-vendor benchmark numbers don't compare.** Same dataset (LoCoMo), incompatible metrics:
  [[zep]] self-reports **94.7% accuracy**; the [[mem0]] paper scores Zep at **LLM-as-Judge ~66**.
  Need a neutral, single-harness evaluation across [[mem0]]/[[zep]]/[[a-mem]]/[[letta]] before
  trusting any ranking. See [[memory-evaluation]].
- **Agent-memory write-path security.** Beyond corpus poisoning ([[vector-rag]]), the 2026 map points
  to SSGM (stability/safety-governed memory) and memory-security surveys — candidates to ground the
  still-open *agent-written-memory* poisoning gap above.
- **Storage/extraction quality has no benchmark.** The [[mem0]] audit (#4573) found **97.8%** of
  10,134 production entries were junk, yet every standard benchmark (LoCoMo/LongMemEval/BEAM) scores
  end-to-end *recall*, not whether what's stored is worth storing — the audit thread itself calls a
  community extraction-quality benchmark a gap. Now partially framed by the new [[memory-curation]]
  page (selective addition + history-based deletion, sourced from Xiong et al. 2025). Related sub-gaps
  the thread raises: **provenance** is severed once a fact is extracted (can't adjudicate
  contradictions by recency/reliability), and **recall quality** (right memory at the right time)
  stays unmeasured even when storage is clean. See [[memory-evaluation]].
- **Memory placement is a cost lever, not just a correctness one.** [[memory-placement]] (Zep, 2026):
  putting the fresh memory block in the system prompt breaks prompt caching and re-bills the whole
  history each turn (~2x cost at 54 turns). Open: how this trades against cache TTL expiry under
  bursty traffic, and whether trailing placement weakens instruction-following vs. authoritative
  system-prompt context.
- **LINT 2026-06-29 — verify a borderline editing claim.** [[model-editing]] states KnowledgeEditor
  (De Cao et al. 2021) "updates concentrate on surprisingly few components." The local raw capture is
  an abstract-only stub and neither it nor the 2025–2026 research map clearly supports the *few
  components* claim. Check against arXiv [2104.08164](https://arxiv.org/abs/2104.08164) and either
  ground it or soften the wording.
- **LINT 2026-06-29 — re-verify system version/benchmark currency (needs-verification, web-sourced).**
  A web pass during lint returned inconsistent results, so nothing was changed. Re-check against the
  vendors' own changelogs: [[mem0]] SDK pin (`^2.1.40`) and its LoCoMo/LongMemEval/BEAM numbers,
  [[zep]] benchmark numbers, and [[gbrain]]'s version (`v0.41.22` could not be confirmed; one source
  suggested `v0.38.x`). Update the affected Maturity blocks once a primary source confirms each fact.
- **LINT 2026-06-29 — two comparison pages are now ripe to draft.** All underlying system pages +
  sources now exist for (a) a Store/Retrieve/Update/Forget comparison across
  [[mem0]]/[[letta]]/[[gbrain]]/[[zep]] and (b) a contradiction-&-staleness handling comparison —
  both long-listed above. Promote them from "candidate" to a `wiki/comparisons/*.md` draft (via an
  `evolve`/`ask`, not a lint run).

## Answered (archive)
- **LINT — removed source `2002.08910`** (raised by lint; resolved 2026-06-29) — `raw/papers/2002.08910.{md,pdf}`
  (Roberts et al. 2020, closed-book QA) had been deleted from `raw/` but was still cited by
  [[in-weights-vs-in-context]] and `sources.md`. **Decision: keep, re-cite arXiv** — the claims are
  well-established and arXiv-citable. The page's `## Sources` now points at arXiv
  [2002.08910](https://arxiv.org/abs/2002.08910) and the dead path was dropped from `sources.md`.
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
- **Zep coverage** (asked 2026-06-24) — answered: a primary Zep/Graphiti doc was ingested →
  [[zep]] now exists (bi-temporal Context Graph, fact invalidation, hybrid search). The old
  "no Zep source" gap is closed; what remains is the cross-vendor metric question above.
