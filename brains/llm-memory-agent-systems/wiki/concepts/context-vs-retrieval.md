# context-vs-retrieval

**One-liner:** The choice between stuffing full conversation history into every prompt (context) vs.
extracting durable facts and fetching only the relevant ones per query (retrieval).

## What it is
Two ways to give a stateless LLM access to prior knowledge:
- **Context-stuffing:** store full chat logs and dump them back into each request. Simple, but the
  model receives everything whether relevant or not.
- **Semantic retrieval:** extract the facts that matter from each interaction, store them, and
  retrieve only those relevant to the current message before generating.

This is an *architectural* distinction, not a model-capability one: modern models can retain a
conversation perfectly within a context window — the problem is that each new session starts with an
empty window and zero knowledge of the user.

## Why it matters for agent memory
Context-stuffing breaks down fast in real agents:
- **Token costs explode** as history grows.
- **Retrieval is "dumb"** — the model gets everything, relevant or not.
- **Cross-session memory is impossible** — once the user closes the tab (or switches channel/device),
  the history is gone.

Semantic retrieval fixes all three: it caps prompt size, surfaces only pertinent facts, and persists
across sessions and devices. This is the trade-off that motivates the [[read-write-agent-loop]] and
the systems that implement it.

## Variants / approaches
- **Full-history dump** — append the entire transcript to every prompt.
- **Semantic fact extraction + top-k retrieval** — store extracted facts, fetch the most relevant
  per query (the approach [[mem0]] takes).
- **Retrieval-augmented generation** — the general framework: [[vector-rag]], refined by
  [[hybrid-retrieval]] and graph traversal ([[knowledge-graphs-for-memory]]).
- **Long native context** — just enlarge the window; SOTA-ML surveys' rule of thumb is that past
  ~64k tokens you should prefer retrieval + summarization over "just cranking the window."
- **Hybrid (the 2026 default)** — retrieve ~50K–200K high-precision tokens, then long-context-reason
  over them; route simple queries to RAG and global/sensemaking queries to long context (Self-Route).

## The long-context-vs-RAG verdict
The "RAG is obsolete, just paste everything" thesis (after 1M–10M token windows shipped) was
**empirically rejected** for production by 2025–2026:
- **Lost in the Middle** (Liu et al., TACL 2024): a U-shaped position curve — accuracy is highest when
  relevant info is at the start/end and drops >30% when it sits mid-context.
- **Context Rot** (Chroma, 2025): across 18 frontier models, accuracy degrades as input grows —
  sometimes 30–50% *well before* the window limit — and coherent input degrades attention *more* than
  shuffled. Production economics: a 1M-token request runs ~30–60× slower at ~1,250× the per-query cost
  of RAG.
- **Consensus:** hybrid won; beware the **over-fetching antipattern** (grabbing 30 chunks "because
  there's room"), which reintroduces context rot.

## Which systems use it
- [[mem0]] — extracts semantic facts (not raw transcripts) and retrieves the top-k relevant ones,
  the retrieval side of this trade-off; reports ~7K tokens/query vs. 25K+ for full-context (see
  [[memory-evaluation]]).
- [[gbrain]] — `gbrain search` (raw retrieved pages) vs. `gbrain think` (synthesized cited answer),
  two points on the same trade-off.
- [[letta]] — pins only `system/` files to context and uses **progressive disclosure** to pull in
  the rest on demand, managing the context-vs-retrieval boundary explicitly.
- [[claude-memory]] — applies both sides: a synthesized memory summary (compiled facts) injected each
  session, plus on-demand **RAG search over past chats** (raw retrieval) surfaced as tool calls.

## Open questions
- At what conversation length / cost does retrieval clearly beat context-stuffing? Largely settled in
  favor of **hybrid** (above); the precise routing thresholds are workload-specific.
- Could a long-context architecture demonstrably **defeat context rot** on adversarial mid-context
  benchmarks? That would shift the balance back.
- How does retrieval handle **stale or contradicting** extracted facts vs. a raw transcript that
  carries its own chronology?
- A level up: should the knowledge live in context at all, or be **baked into model weights**? See
  [[in-weights-vs-in-context]].

## Sources
- `raw/articles/memory/Memory Poisoning in AI Agents How Bad Inputs Corrupt Agent Memory.md`
  — "The Problem" section contrasts full-history stuffing with Mem0's semantic retrieval.
- `raw/articles/memory/Introducing The Token-Efficient Memory Algorithm.md`
  — token-efficiency framing (~7K vs 25K+ tokens/query).
- `raw/articles/memory/SOTA ML by July 2025 From Explicit Features to Implicit World Models.md`
  — "long context & memory": retrieval vs. longer windows; the ~64k rule of thumb.
- `raw/articles/memory/LLM Memory and Knowledge: A 2025–2026 Research Map Across Four Threads.md`
  — cross-cutting long-context-vs-RAG debate: Lost-in-the-Middle, Context Rot, hybrid-is-default.
