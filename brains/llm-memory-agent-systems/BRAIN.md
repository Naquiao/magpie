# BRAIN.md — LLM Memory & Agent Systems

> The ONLY file you edit by hand to specialize this brain. `AGENTS.md` (the engine) reads
> this to know the topic, boundaries, and page shapes. This one is filled in as a worked
> example — copy its shape when you make new brains for other topics.

Created: 2026-06-24
Slug: `llm-memory-agent-systems`

## Topic
State of the art in **memory for LLM agents**: the core approaches (how knowledge is stored,
retrieved, updated, and forgotten), the systems that implement them, and how they compare.

## Scope
**In scope:**
- Memory architectures: working/context, episodic, semantic, procedural memory for agents.
- Retrieval: vector RAG, hybrid (vector + keyword + rerank), graph traversal, RRF.
- Knowledge representation: markdown wikis, entity/knowledge graphs, typed edges.
- Temporal knowledge: staleness, decay, forgetting, consolidation / "dream cycle".
- Agent memory loops: read-before-respond / write-after-learn, background consolidation.
- In-context vs in-weights memory: RAG vs finetuning / continual learning.
- Evaluation: benchmarks and metrics for agent memory.
- Concrete systems (see seed list below).

**Out of scope** (stub in `sources.md`, don't write full articles):
- General LLM pretraining / model architecture not specific to memory.
- Vector-DB infrastructure deep-dives unless tied to a memory system.
- Prompt-engineering tricks with no persistence angle.

## Source taxonomy
- **papers/** → a **concept** page and/or a **system** page.
- **repos/** → a **system** page (read README + key docs).
- **articles/** (incl. these from our chat: GBrain reviews, Karpathy's wiki note) → concept or system.
- **notes/** → usually an **open question** or a new concept seed.
- **images/** → architecture diagrams referenced by pages; not pages themselves.

## Page types
### Concept  (`wiki/concepts/<name>.md`)
```
# <Concept name>
**One-liner:** ...
## What it is
## Why it matters for agent memory
## Variants / approaches
## Which systems use it
## Open questions
## Sources
```
### System  (`wiki/systems/<name>.md`)
```
# <System name>
**One-liner:** ...
## Approach
## Architecture
## Store / Retrieve / Update / Forget   <- the core 4 for THIS topic
## Tradeoffs / limits
## Maturity (version, adoption, as-of date)
## Sources
```
### Comparison  (`wiki/comparisons/<name>.md`)
Cross-system/concept analysis, usually generated from a query (e.g. "how each system handles
stale/contradicting facts"). Always include a "what the brain doesn't know yet" section.

## Seed concepts (pages to grow as sources arrive — topics, not claims)
- `memory-types` (working / episodic / semantic / procedural)
- `context-vs-retrieval`
- `vector-rag`
- `hybrid-retrieval` (vector + keyword + RRF + reranker)
- `knowledge-graphs-for-memory` (entity pages, typed edges)
- `temporal-knowledge-and-decay` (staleness, forgetting)
- `memory-consolidation` (summarization, background "dream cycle")
- `read-write-agent-loop`
- `in-weights-vs-in-context` (finetuning vs RAG)
- `memory-evaluation`

## Seed systems (candidates to track — create/fill from sources, don't assert from memory)
- `mem0` · `zep` (Graphiti) · `letta` (MemGPT) · `cognee` · `gbrain` · `hindsight`

## Naming & conventions
- Files `kebab-case.md`; refer to pages as `[[kebab-case]]`.
- Date every "current state" / maturity claim with an as-of date.
