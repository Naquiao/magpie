# memory-evaluation

**One-liner:** Benchmarks and metrics for agent memory — judged on three axes that trade off against
each other: **accuracy**, **cost** (context tokens per query), and **performance** (latency).

## What it is
Evaluating a memory system means more than answer accuracy. [[mem0]] frames the real problem as
balancing accuracy, token cost, and latency *at scale* — optimizing one is easy; balancing all three
under production constraints (limited context, practical token budgets) is the hard part.

## Why it matters for agent memory
Many systems "win" benchmarks by maximizing context window or using frontier models — which inflates
cost without proving the memory layer got better. Smaller benchmarks (LoCoMo, LongMemEval) are
materially gameable this way; larger-scale benchmarks are harder to fake and better reflect
production. Good evaluation is how you tell a real memory improvement from a bigger prompt.

A second blind spot: every standard benchmark scores **end-to-end recall** (did the right answer come
out?), not **what gets stored** in the first place. A pipeline can pass LoCoMo while writing 97.8%
junk to its store (the [[mem0]] audit #4573) — extraction/storage quality is essentially unmeasured by
public benchmarks, and that hand audit may be the only existing public data point on it. See [[memory-curation]].

## Variants / approaches (benchmarks)
- **LoCoMo** — single-hop, multi-hop, open-domain, temporal recall across conversational sessions.
- **LongMemEval** — single/multi-session, knowledge updates, temporal reasoning. Also runnable in
  [[gbrain]] (`gbrain eval longmemeval`).
- **BEAM** — operates at **1M and 10M token scales** across ~10 categories (preference/instruction
  following, temporal reasoning, contradiction resolution, event ordering, …). [[mem0]] calls it the
  most production-relevant because it can't be solved by enlarging the context window.
- **BrainBench / NamedThingBench** — [[gbrain]]'s own retrieval scorecards (P@K, R@K; named-thing
  retrieval families hard-gated in CI).
- **LoCoMo** (Maharana et al., ACL 2024) is the canonical *very-long-term conversational* benchmark
  (persona + temporal-event-graph pipeline); it found long-context LLMs and RAG still lag humans by
  ~56% overall and ~73% on temporal reasoning. Successors: **MemBench**, **MemoryAgentBench**, and
  **MemoryArena** (2026), which couple memory to *actions* — swapping an active-memory agent for a
  long-context-only one dropped task completion from >80% to ~45%.

## Reported numbers (as-of 2026)
- [[mem0]] new algorithm (April 2026): LoCoMo **91.6**, LongMemEval **93.4**, BEAM **64.1** (1M) /
  **48.6** (10M), averaging **<7K tokens/query** vs. 25K+ for full-context. Managed-platform numbers
  include proprietary optimizations beyond the OSS SDK; eval framework is open-source.
- [[gbrain]]: **P@5 49.1%, R@5 97.9%** on a 240-page rich-prose corpus, **+31.4 P@5** from the graph.
- [[mem0]] paper (2025), LoCoMo overall LLM-as-Judge — a rare apples-to-apples table on one corpus:
  full-context **72.9** (but p95 latency 17.1s) > Mem0ᵍ **68.4** > Mem0 **66.9** > Zep **66.0** >
  best RAG ~61 > OpenAI memory **52.9** > A-Mem* **48.4**. Mem0's p95 latency was **1.44s** (~91%
  lower than full-context). Caveat: self-reported by Mem0; baselines are their measurements.
- [[zep]] (self-reported): LoCoMo **94.7%** accuracy @155ms; LongMemEval **90.2%** @162ms. **Metric
  mismatch warning:** Zep's "accuracy" and Mem0's LLM-as-Judge "~66 for Zep" are different
  metrics/harnesses on the same dataset — a vivid example of why cross-vendor numbers don't compare.

## Which systems use it
- [[mem0]] — LoCoMo / LongMemEval / BEAM. [[gbrain]] — BrainBench / NamedThingBench / LongMemEval.

## Open questions
- **What benchmarks actually measure agent memory well?** (Also in `_meta/open-questions.md`.) BEAM's
  10M-scale numbers expose that temporal reasoning, event ordering, and multi-session reasoning are
  unsolved across the field.
- Cross-system numbers aren't directly comparable (different corpora, self-reported, ±1pt judge noise).
- **Storage/extraction quality is unbenchmarked.** Benchmarks measure recall, not whether stored
  memories are worth storing; the [[mem0]] audit (97.8% junk) had to be done by hand. A community
  extraction-quality benchmark is an open gap the audit thread itself flags. See [[memory-curation]].

## Sources
- `raw/articles/memory/Introducing The Token-Efficient Memory Algorithm.md`
  — LoCoMo / LongMemEval / BEAM methodology, results, and the accuracy/cost/latency framing.
- `raw/articles/memory/garrytangbrain Garry's Opinionated OpenClawHermes Agent Brain.md`
  — BrainBench / NamedThingBench / LongMemEval eval framework and P@5/R@5 numbers.
- `raw/articles/memory/LLM Memory and Knowledge: A 2025–2026 Research Map Across Four Threads.md`
  — LoCoMo provenance + human gap, and memory-action benchmarks (MemBench / MemoryArena).
- `raw/papers/Mem0 Building Production-Ready AI Agents with Scalable Long-Term Memory.md`
  — LoCoMo head-to-head (Mem0/Mem0ᵍ vs Zep/OpenAI/RAG/full-context) on F1/BLEU-1/LLM-as-Judge + latency.
- `raw/papers/A-Mem Agentic Memory for LLM Agents.md`
  — LoCoMo + DialSim results vs MemGPT/MemoryBank/ReadAgent across six foundation models.
- `raw/articles/What we found after auditing 10,134 mem0 entries 97.8% were junk · Issue 4573 · mem0aimem0.md`
  — benchmarks measure end-to-end retrieval, not storage quality; a hand audit as the rare data point.
