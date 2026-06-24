# LLM Memory & Agent Systems — Index

Master map of this brain. The compiler keeps this current. Read this first for any query.

## Concepts
- [[context-vs-retrieval]] — full-history stuffing vs. extract-facts-and-retrieve-relevant.
- [[read-write-agent-loop]] — retrieve-before-respond, store-after-learn.
- [[hybrid-retrieval]] — fuse vector + keyword + entity + graph signals (RRF + rerank).
- [[knowledge-graphs-for-memory]] — entities + typed edges for factually-connected retrieval.
- [[memory-consolidation]] — background "dream cycle" / sleep-time reorganization of memory.
- [[temporal-knowledge-and-decay]] — staleness, contradictions, overwrite-vs-keep-both.
- [[memory-evaluation]] — benchmarks/metrics: accuracy vs token cost vs latency.
- [[in-weights-vs-in-context]] — knowledge in model parameters (closed-book) vs. retrieved at inference.
- [[vector-rag]] — retrieval-augmented generation: architectures, enhancements, robustness/poisoning.
- [[parametric-knowledge]] — how/where facts are stored & extracted in transformer weights.
- [[model-editing]] — surgically updating a fact in weights without retraining (ROME, KnowledgeEditor).
- [[llm-compiled-wiki]] — LLM-compiled markdown knowledge base (this brain's own method; Karpathy).
- [[portable-memory]] — model-agnostic memory across Claude/Gemini/Cursor: text + MCP over embeddings.

## Systems
- [[mem0]] — managed/self-hostable semantic memory layer scoped by `user_id`; token-efficient ADD-only.
- [[letta]] — memory-native agents (MemGPT lineage) with a git-versioned memory filesystem.
- [[gbrain]] — self-hosted brain: hybrid retrieval + self-wiring graph + dream cycle + synthesis.

## Comparisons
_(none yet)_

---
See `_meta/sources.md` for the source index and `_meta/open-questions.md` for the backlog.
