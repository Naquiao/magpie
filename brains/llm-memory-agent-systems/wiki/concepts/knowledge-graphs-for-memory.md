# knowledge-graphs-for-memory

**One-liner:** Represent memory as **entities + typed edges** so retrieval can follow factual
connections (who-works-where, who-invested-in-what), not just semantic similarity.

## What it is
Alongside (or instead of) embedding text into a vector store, the system extracts entities and the
typed relationships between them into a graph. Queries can then traverse edges to reach facts that
vector search alone can't surface, and graph adjacency can boost ranking in [[hybrid-retrieval]].

## Why it matters for agent memory
Vector search returns chunks that are *semantically close*; the graph returns chunks that are
*factually connected*. Questions like "who works at Acme?" or "what did Bob invest in this quarter?"
are graph queries — they depend on relationships, not phrasing. A self-maintaining graph also keeps
memory navigable as it grows, and the structure powers multi-hop reasoning.

A structural side-benefit surfaced in production: in a graph a repeated fact is the *same triple*
(`user → uses → she/her`), so re-extraction updates a timestamp instead of inserting a new row —
preventing the mass-duplication that floods pure vector stores (the [[mem0]] audit found **808 copies**
of one hallucinated fact that paraphrase-dodged a 0.98 cosine gate). The catch: the graph still relies
on an LLM to extract entities/relations, so a *single* wrong triple still gets in — graph prevents 808
copies, not the first bad one. Vector search also hits a hard ceiling on temporal queries (P@1 ≤ 33%
in one evaluation), another reason to add graph traversal. See [[memory-curation]].

## Variants / approaches
- **Deterministic, zero-LLM extraction** — [[gbrain]]: every page write extracts entity refs from
  markdown/wikilink/typed-link syntax and writes typed edges (`attended`, `works_at`, `invested_in`,
  `founded`, `advises`, `mentions`) with no LLM calls; multi-hop traversal via `graph-query`. The
  graph is credited with +31.4 P@5 over a graph-disabled variant.
- **Entity-linking layer over retrieval** — [[mem0]]: entities (proper nouns, quoted text, compound
  noun phrases) are embedded into a separate lookup layer; query entities are matched against it and
  relevant memories get a ranking boost.
- **Full graph store** — Mem0ᵍ ([[mem0]]'s graph variant): a Neo4j directed labeled graph (entities
  as typed nodes, relationships as labeled edges) with conflict detection that marks superseded
  edges **obsolete rather than deleting** them — strongest on temporal/open-domain LoCoMo categories.
- **LLM-linked note graph** — [[a-mem]]: each memory is an atomic note the LLM links to related notes
  (causal/conceptual, beyond cosine similarity), and new notes can rewrite linked notes' attributes.

- **Temporal KG** — [[zep]]/Graphiti: a bi-temporal Context Graph (entity/edge extraction with
  relationship-lifecycle metadata + fact invalidation); hybrid semantic+BM25+graph search.

## Which systems use it
- [[gbrain]] — self-wiring typed-edge graph (deterministic). [[mem0]] — entity-linking lookup layer +
  Mem0ᵍ Neo4j graph. [[a-mem]] — LLM-linked, self-evolving note graph. [[zep]] — bi-temporal Context
  Graph (Graphiti).

## Open questions
- **Deterministic typed-edge extraction (GBrain, zero LLM) vs. LLM-inferred links: precision/recall
  tradeoffs?** (Also in `_meta/open-questions.md`.) GBrain's recall depends on authors using link
  syntax; Mem0's LLM/embedding entity linking may catch more but costs more.
- How well do graph signals hold up at very large scale (millions of pages)?

## Sources
- `raw/articles/memory/garrytangbrain Garry's Opinionated OpenClawHermes Agent Brain.md`
  — self-wiring knowledge graph, typed edges, zero-LLM auto-linking.
- `raw/articles/memory/Introducing The Token-Efficient Memory Algorithm.md`
  — entity linking layer and entity-match ranking boost.
- `raw/articles/memory/Retrieval-Augmented Generation A Comprehensive Survey...md`
  — GraphRAG / KG-RAG: entity-centric graphs + community summarization improve multi-hop recall.
- `raw/papers/Mem0 Building Production-Ready AI Agents with Scalable Long-Term Memory.md`
  — Mem0ᵍ Neo4j graph: entity/relationship extraction, conflict detection, obsolete-marking.
- `raw/papers/A-Mem Agentic Memory for LLM Agents.md`
  — Zettelkasten note graph: LLM link generation + memory evolution.
- `raw/articles/What we found after auditing 10,134 mem0 entries 97.8% were junk · Issue 4573 · mem0aimem0.md`
  — production argument that graph structure prevents mass deduplication (the 808-copy case) but not
  single bad triples; vector P@1 ≤ 33% on temporal queries.
