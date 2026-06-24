# temporal-knowledge-and-decay

**One-liner:** How a memory system handles facts that change over time — staleness, contradiction,
and the choice between **overwriting** an old fact vs. **keeping both** and modeling the transition.

## What it is
Most memory systems treat change as replacement: a new fact overwrites the old one. But the
*transition itself* is often the valuable part. [[mem0]]'s example: a user who moves New York → San
Francisco — knowing they moved (and that "your old neighborhood" still points to New York) is worth
more than just storing the current city. Temporal handling is about preserving that history and
reasoning over it without letting stale facts corrupt answers.

## Why it matters for agent memory
Overwriting is lossy: deletes remove information that turns out relevant later, and updates can erase
context from the original fact. Append/ADD-only preserves the full history of state changes, enabling
"when did the user first mention X?" and "what led to their current decision?" — but it grows the
store and makes contradiction/staleness detection necessary. This is the recurring tension behind
the project's open question on contradicting facts (see `_meta/open-questions.md`).

## Variants / approaches
- **ADD-only, keep-both** — [[mem0]]: single-pass extraction that only adds; old and new facts
  coexist as independent records, so the system can reason about evolution. Drove large temporal-
  reasoning and knowledge-update benchmark gains (LoCoMo temporal +29.6; LongMemEval temporal +42.1)
  — but temporal reasoning and event ordering still collapse at 10M-token scale (BEAM).
- **Git versioning** — [[letta]]: every memory change is a commit, so prior states are recoverable;
  defragmentation reorganizes without losing history (see [[memory-consolidation]]).
- **Contradiction/staleness detection** — [[gbrain]]: a `suspected-contradictions` eval + dream-cycle
  pass surface conflicts; `gbrain think` flags stale pages ("nothing added about Alice since April
  22") as part of gap analysis.
- **In-weights editing** — [[model-editing]] (ROME, KnowledgeEditor): update a stale/wrong fact
  directly in model parameters. Orthogonal to the in-context approaches above; see
  [[in-weights-vs-in-context]]. None of the tracked systems use it.
- **Index hot-swapping** — [[vector-rag]]: the original RAG paper (Lewis et al. 2020) updated world
  knowledge simply by swapping the non-parametric index (2016→2018 Wikipedia), no retraining — the
  cleanest illustration of why retrieval beats parametric memory on staleness.
- **Temporal knowledge graphs** — **Zep** (arXiv 2501.13956) builds a *temporal* knowledge graph for
  agent memory (bi-temporal edges that can be invalidated as facts change). The brain still lacks a
  full Zep source — see `_meta/open-questions.md` — but this is the named pointer to ingest.
- **Forgetting curves** — MemoryBank (AAAI 2024) decays memories on an Ebbinghaus schedule (see
  [[memory-consolidation]]).

## Which systems use it
- [[mem0]] — ADD-only history. [[letta]] — git-versioned history. [[gbrain]] — contradiction/staleness flags.

## Open questions
- **How does each system handle contradicting facts and staleness** (compiled-truth + timeline vs
  overwrite vs append)? Candidate first cross-system comparison article. (Also in `_meta/open-questions.md`.)
- Temporal reasoning, event ordering, and multi-session reasoning at large scale are open across the
  field — fact-level and entity-level matching are insufficient (BEAM 10M results).

## Sources
- `raw/articles/memory/Introducing The Token-Efficient Memory Algorithm.md`
  — ADD-only extraction, keep-both facts, temporal benchmark results.
- `raw/articles/memory/garrytangbrain Garry's Opinionated OpenClawHermes Agent Brain.md`
  — contradiction detection + staleness gap analysis.
- `raw/articles/memory/Introducing Context Repositories Git-based Memory for Coding Agents.md`
  — git-versioned memory history.
- `raw/papers/Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.md`
  — index hot-swapping to update knowledge without retraining (Lewis et al. 2020).
- `raw/articles/memory/LLM Memory and Knowledge: A 2025–2026 Research Map Across Four Threads.md`
  — Zep temporal KG, MemoryBank forgetting curve, in-context-editing-beats-parameter-editing.
