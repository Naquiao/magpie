# zep

**One-liner:** Agent memory at enterprise scale built on **Graphiti** — an open-source *temporal
knowledge graph* ("Context Graph") that autonomously extracts entities/facts, tracks how they change
over time (bi-temporal model + fact invalidation), and serves a fused semantic + full-text + graph
search.

## Approach
A Context Graph is a temporal knowledge graph of entities, relationships, and facts, each a *triplet*
— two entity nodes plus a relationship edge (e.g. "Kendra –loves→ Adidas shoes"). What distinguishes
it from static KG/RAG is autonomously building the graph **while handling changing relationships and
preserving historical context**. Two layers:
- **Graphiti** — the OSS framework: build/query a single Context Graph per subject locally (entity/
  edge extraction, bi-temporal model, fact invalidation, hybrid retrieval).
- **Zep** — managed enterprise layer on Graphiti: a governed "Context Lake" of millions of Context
  Graphs served in milliseconds via a proprietary Context Graph Engine (SOC 2, HIPAA, BYOC).

Explicitly positioned against Microsoft's GraphRAG ([[vector-rag]]), which Zep argues is built for
*static* documents and lacks real temporal handling. See [[knowledge-graphs-for-memory]] and
[[temporal-knowledge-and-decay]].

## Architecture
- **Episodic processing:** ingests data as discrete *episodes* (unstructured text or structured
  JSON), preserving provenance and allowing incremental entity/relationship extraction.
- **Bi-temporal edges:** graph edges carry temporal metadata recording relationship lifecycles,
  enabling **point-in-time queries**.
- **Custom entity types**; **pluggable backends** (Neo4j, FalkorDB, Amazon Neptune); LLM/embedding
  providers (OpenAI, Azure, Gemini, Anthropic). Parallelizes LLM calls for bulk ingest while
  preserving chronology.
- **Context Block placement:** Zep assembles a per-message **Context Block** of topic-relevant memory.
  Because it refreshes every turn, Zep recommends attaching it as a **trailing message** (a fake tool
  message, or a Claude Opus 4.8 mid-conversation system message) *after* the cache breakpoint rather
  than in the system prompt — preserving prompt caching and cutting token cost up to ~2x on long
  conversations. See [[memory-placement]].

## Store / Retrieve / Update / Forget
- **Store:** episodic ingest → autonomous entity + edge extraction into the Context Graph.
- **Retrieve:** **hybrid search** — vector similarity + BM25 full-text + graph traversal fused into a
  single ranked answer with **no LLM-in-the-loop reranking**; results can be reranked by distance from
  a central node (e.g. "Kendra"). See [[hybrid-retrieval]]. Sub-200ms typical retrieval latency.
- **Update / Forget:** **temporal edge invalidation** — when a fact changes, the old edge is marked
  invalid (not deleted), so history is preserved and contradictions are handled structurally. This is
  the cleanest contradiction-handling model among the brain's systems; see [[temporal-knowledge-and-decay]].

## Tradeoffs / limits
- Graph construction is LLM-heavy; the [[mem0]] paper (a competitor) reports Zep's graph using **600K+
  tokens** with **slow async construction** that delayed correct retrieval — treat as a rival's
  measurement, in tension with Zep's own sub-200ms *retrieval* latency claim.
- Enterprise governance/scale features live in managed Zep, not OSS Graphiti.

## Maturity (version, adoption, as-of date)
As-of 2026-06-24: Graphiti is open-source; Zep is a managed enterprise product (SOC 2, HIPAA, BYOC).
**Self-reported** benchmarks: LoCoMo **94.7% accuracy @ 155ms**, LongMemEval **90.2% @ 162ms**.
Note a metric mismatch with the [[mem0]] paper, which scored Zep at LoCoMo LLM-as-Judge ~66 as a
baseline — different metrics/harnesses, not directly comparable. See [[memory-evaluation]].

## Sources
- `raw/articles/Zep Documentation — agent memory at enterprise scale.md` — Graphiti/Zep overview:
  Context Graphs, bi-temporal model, fact invalidation, hybrid search, GraphRAG comparison, benchmarks.
- `raw/papers/Mem0 Building Production-Ready AI Agents with Scalable Long-Term Memory.md`
  — competitor-reported Zep numbers (LoCoMo baseline, token/latency critique).
- `raw/articles/Where to place agent memory in the prompt to cut token costs up to 2x.md`
  — Zep's Context Block placement technique (trailing message / Opus 4.8 mid-conversation system
  message) for prompt-cache-preserving cost savings. See [[memory-placement]].
