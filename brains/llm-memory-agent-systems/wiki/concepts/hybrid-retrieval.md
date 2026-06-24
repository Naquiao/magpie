# hybrid-retrieval

**One-liner:** Combine multiple retrieval signals — vector similarity, keyword match, entity match,
and graph structure — and fuse them (e.g. reciprocal-rank fusion) plus reranking, instead of relying
on vector search alone.

## What it is
Different queries lean on different signals: "what does Alice think about remote work?" leans on
entity matching; "what meetings did I have last week?" leans on keyword/temporal; semantically
fuzzy questions lean on vectors. Hybrid retrieval runs several scorers in parallel and fuses their
rankings, typically with a reranker on top, so no single signal's blind spot dominates.

## Why it matters for agent memory
Vector-only retrieval returns chunks that are *semantically close* but misses factually-connected or
exactly-named results. Fusing keyword + entity + graph signals raises recall and precision on the
queries agents actually ask, while reranking and rank-fusion keep the top-k clean. It is the
retrieval side of [[context-vs-retrieval]].

## Variants / approaches
- **Full hybrid stack** — [[gbrain]]: vector (HNSW/pgvector) + BM25 keyword + reciprocal-rank fusion
  + source-tier boost + reranker, plus per-query graph signals (adjacency/cross-source/session
  boosts). `--explain` shows per-stage attribution.
- **Multi-signal fusion** — [[mem0]]: semantic + keyword + entity scored in parallel and fused by
  rank scoring; entity linking adds a ranking boost; keyword normalization handles verb conjugation.
- **Graph as a signal** — see [[knowledge-graphs-for-memory]] for the structural component.
- **In the RAG literature** — RAG-Fusion combines results from multiple reformulated queries via
  reciprocal-rank fusion; sparse (BM25) + dense (DPR) hybrids and rerankers are standard. See
  [[vector-rag]] for the broader taxonomy.

## Which systems use it
- [[gbrain]] — vector + BM25 + RRF + reranker + graph signals.
- [[mem0]] — semantic + keyword + entity multi-signal fusion.

## Open questions
- How much of the accuracy gain is fusion vs. the reranker vs. the graph signal? (GBrain attributes
  +31.4 P@5 to the graph specifically; see [[memory-evaluation]].)
- Cost/latency of running multiple scorers per query at production scale.

## Sources
- `raw/articles/memory/garrytangbrain Garry's Opinionated OpenClawHermes Agent Brain.md`
  — hybrid search stack (vector + BM25 + RRF + reranker + graph signals).
- `raw/articles/memory/Introducing The Token-Efficient Memory Algorithm.md`
  — multi-signal retrieval (semantic + keyword + entity), keyword normalization.
- `raw/articles/memory/Retrieval-Augmented Generation A Comprehensive Survey...md`
  — RAG-Fusion (RRF over reformulated queries), sparse/dense/hybrid retrievers, reranking.
