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

## Variants / approaches
- **Deterministic, zero-LLM extraction** — [[gbrain]]: every page write extracts entity refs from
  markdown/wikilink/typed-link syntax and writes typed edges (`attended`, `works_at`, `invested_in`,
  `founded`, `advises`, `mentions`) with no LLM calls; multi-hop traversal via `graph-query`. The
  graph is credited with +31.4 P@5 over a graph-disabled variant.
- **Entity-linking layer over retrieval** — [[mem0]]: entities (proper nouns, quoted text, compound
  noun phrases) are embedded into a separate lookup layer; query entities are matched against it and
  relevant memories get a ranking boost.

## Which systems use it
- [[gbrain]] — self-wiring typed-edge graph (deterministic). [[mem0]] — entity-linking lookup layer.

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
