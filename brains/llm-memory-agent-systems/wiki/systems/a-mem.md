# a-mem

**One-liner:** A research agentic-memory system that stores each interaction as a Zettelkasten-style
**atomic note** which the LLM auto-links to related notes and which **evolves** (rewrites its own
attributes) as new memories arrive — agency at the level of memory *organization*, not just retrieval.

## Approach
A-Mem (Xu et al., Rutgers; arXiv 2502.12110, NeurIPS 2025) rejects fixed, predefined memory schemas
(its critique of graph-DB systems like [[mem0]]). Following the **Zettelkasten** method, each memory
is an atomic note with LLM-generated structure, notes link to each other by meaning, and adding a new
note can update older notes — so the memory network continuously refines itself. See
[[memory-consolidation]] (memory evolution) and [[knowledge-graphs-for-memory]] (note graph).

## Architecture
A memory note is `m = {content, timestamp, keywords, tags, contextual-description, embedding, links}`.
Three stages on each write:
1. **Note construction** — an LLM generates keywords, tags, and a contextual description from the raw
   interaction; the concatenation is embedded by a text encoder (all-MiniLM-L6-v2).
2. **Link generation** — retrieve top-k similar notes by cosine similarity, then an LLM decides which
   links to establish (beyond raw similarity — causal/conceptual connections). Notes can belong to
   multiple overlapping "boxes."
3. **Memory evolution** — the new note can trigger an LLM to rewrite the context/keywords/tags of its
   neighbor notes, so old memories update in light of new ones.

## Store / Retrieve / Update / Forget
- **Store:** construct the atomic note (LLM attributes + embedding) and link it in.
- **Retrieve:** embed the query, cosine-rank notes, take top-k (default k=10); memories linked in the
  same box are auto-pulled alongside a hit.
- **Update:** **memory evolution** — the distinctive feature; new notes mutate existing notes'
  descriptions/keywords/tags rather than leaving them static.
- **Forget:** not described (no explicit decay/forget mechanism).

## Tradeoffs / limits
- Several LLM calls per memory op, but cheap in practice (~1,200 tokens/op; 85–93% fewer tokens than
  full-context's ~16.9K; <$0.0003/op; ~1–5s). Retrieval scales well (≈3.7µs at 1M notes).
- Organization quality is bounded by the base LLM; text-only (no multimodal yet).
- Link/evolution rely on LLM judgment, so results vary across foundation models.

## Maturity (version, adoption, as-of date)
As-of 2026-06-24: a research system with two open repos (benchmark eval + a production-ready
`A-mem-sys`). Evaluated on LoCoMo and DialSim across six foundation models, beating MemGPT /
MemoryBank / ReadAgent — strongest on multi-hop and temporal categories. Note the [[mem0]] paper's
independent re-run scored A-Mem lower on its LLM-as-Judge metric (see [[memory-evaluation]]).

## Sources
- `raw/papers/A-Mem Agentic Memory for LLM Agents.md` (arXiv 2502.12110, Xu et al. 2025) — Zettelkasten
  atomic notes, link generation, memory evolution, LoCoMo/DialSim results.
