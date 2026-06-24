# vector-rag

**One-liner:** Retrieval-Augmented Generation — condition LLM generation on documents fetched at
inference from an external corpus; the canonical **in-context, non-parametric** memory approach.

## What it is
The term and framing come from Lewis et al. (2020), who combined **parametric memory** (a pretrained
seq2seq generator, BART) with **non-parametric memory** (a dense vector index of Wikipedia accessed
by a DPR retriever), trained end-to-end. They proposed two variants: **RAG-Sequence** (one retrieved
doc conditions the whole output) and **RAG-Token** (a different doc can be drawn per token), and set
SOTA on open NQ/WebQuestions/CuratedTrec/TriviaQA with generations rated more factual and specific
than parametric-only BART.

A RAG system has a **query encoder**, a **retriever**, and a **generator**. Formally it models
`P(y|x) ≈ Σ_i P(y|x,d_i)·P(d_i|x)` over the top-k retrieved documents — one term for the retriever's
relevance score, one for the generator conditioned on each document. Retrievers may be **sparse**
(BM25), **dense** (DPR), **hybrid**, or **generative**; the generator is a pretrained transformer
(T5/BART/GPT). It is the retrieval side of [[context-vs-retrieval]] and the foundation under
[[hybrid-retrieval]].

## Why it matters for agent memory
RAG directly attacks the limits of [[in-weights-vs-in-context]] / [[parametric-knowledge]]: static
parametric knowledge causes factual inconsistency, staleness, and domain inflexibility. Retrieval
adds **transparency** (you can cite the evidence), **factual grounding**, and **updatability** (edit
the corpus, not the weights). The cost is new failure modes — retrieval noise, grounding
mismatch/hallucination, latency. Lewis et al. demonstrated updatability concretely with **index
hot-swapping**: replacing the 2016 Wikipedia index with a 2018 one corrected answers about world
leaders with *no retraining* — the non-parametric memory is human-readable and human-writable. See
[[temporal-knowledge-and-decay]].

## Variants / approaches (taxonomy from the RAG survey, Sharma 2025)
- **Retriever-centric:** query rewriting/decomposition (RQ-RAG), reciprocal-rank fusion over
  reformulated queries (RAG-Fusion), granularity control (LongRAG, FILCO), graph retrieval
  (GraphRAG, KG-RAG — see [[knowledge-graphs-for-memory]]).
- **Generator-centric:** faithfulness-aware decoding (SELF-RAG self-critique), context compression
  (FiD-Light, xRAG).
- **Hybrid (tightly coupled):** iterative/multi-round (IM-RAG), dynamic retrieval triggering on
  uncertainty (FLARE, DRAGIN), corrective retrieval (CRAG).
- **Robustness/security-oriented:** the part most relevant to **memory poisoning** — adversarial
  **corpus poisoning** attacks (BadRAG, TrojanRAG) plant semantic backdoors via poisoned passages
  that trigger target behaviors even with an unmodified base model. Mitigations: noise-adaptive
  training (RAAT), hallucination benchmarks (RAGTruth), context filtering (FILCO). This is the first
  real coverage in the brain of the memory-poisoning question raised in `_meta/open-questions.md`.

## Lineage & 2025–26 frontier
- **Lineage:** kNN-LM (2020) → REALM / DPR (2020) → RAG (Lewis 2020) → RETRO (retrieve from trillions
  of tokens, 2022) → FiD / Atlas.
- **Agentic RAG** ("the model decides when/what/how to retrieve"): Self-RAG (reflection tokens for
  on-demand retrieval + self-critique), RL-trained search agents (Search-R1).
- **Self-correcting:** CRAG — a lightweight retrieval evaluator triggers correct/incorrect/ambiguous
  actions with web-search fallback.
- **GraphRAG** (Microsoft, 2024): entity KG + community summarization for global "sensemaking";
  reports 72–83% comprehensiveness win over vector RAG. **HippoRAG** (NeurIPS 2024): Personalized
  PageRank over a KG for single-step multi-hop, ~20% better and far cheaper than iterative retrieval.
- **Late-interaction / multi-vector:** the ColBERT family (caveat: weaker on long narrative queries).

## Which systems use it
- [[mem0]] and [[gbrain]] are retrieval-based memory systems building on these ideas (Mem0's
  multi-signal fusion, GBrain's hybrid stack); both extend RAG with entity/graph signals.

## Open questions
- Recurring trade-offs: retrieval precision vs. generation flexibility; efficiency vs. faithfulness;
  modularity vs. coordination.
- Survey's open frontiers: adaptive retrieval, real-time integration, structured multi-hop
  reasoning, privacy-preserving and federated retrieval, and robustness to corpus poisoning.

## Sources
- `raw/papers/Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.md` (arXiv 2005.11401,
  Lewis et al. 2020) — the original RAG paper: parametric + non-parametric memory, RAG-Sequence /
  RAG-Token, index hot-swapping for knowledge updates.
- `raw/articles/memory/Retrieval-Augmented Generation A Comprehensive Survey of Architectures, Enhancements, and Robustness Frontiers.md`
  (arXiv 2506.00054, Sharma 2025) — RAG formulation, architecture taxonomy, robustness/poisoning.
- `raw/articles/memory/SOTA ML by July 2025 From Explicit Features to Implicit World Models.md`
  — retrieval as "cache + compute" (RETRO), fewer hallucinations / easier updates than long context.
- `raw/articles/memory/LLM Memory and Knowledge: A 2025–2026 Research Map Across Four Threads.md`
  — Thread 2: retrieval lineage (kNN-LM/REALM/DPR/RETRO/Atlas), agentic RAG, Self-RAG/CRAG, GraphRAG,
  HippoRAG, ColBERT late-interaction.
