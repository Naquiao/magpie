# read-write-agent-loop

**One-liner:** The agent memory loop of **retrieve-before-respond, store-after-learn** — search a
memory store for relevant facts before the LLM call, then write new facts back after the response.

## What it is
A per-turn cycle wrapped around an LLM generation call:
1. Validate the request (e.g. messages + a stable user identifier).
2. **Search** the memory store for facts relevant to the user's latest message.
3. **Inject** those facts into the system prompt as context.
4. **Generate** the response with the LLM.
5. **Store** the full interaction back so its facts are retrievable later.

The ordering is the point: search must run **before** generation so the model knows what the user
has told it before it decides how to respond — not after. Storage runs **after** so the latest
exchange becomes future context.

## Why it matters for agent memory
It is the minimal architecture that turns a stateless LLM into an agent that remembers across
sessions, devices, and channels — without re-stuffing entire conversation histories into every
prompt. It cleanly separates the **generation** layer from the **memory** layer, so the same loop
works regardless of which model provider generates the answer. See [[context-vs-retrieval]] for the
problem this loop solves.

## Variants / approaches
- **Retrieve-then-generate** (the loop above): facts fetched per turn and injected into the prompt.
- **Graceful degradation:** wrap the search/store calls so a memory failure degrades to stateless
  operation rather than blocking the user's response.
- **Latency hiding:** run memory retrieval in parallel with other async setup (`Promise.all()`) so
  its ~100–200ms overlaps other work.
- **Scoping:** every read and write carries a stable identifier (e.g. `user_id`) drawn from the auth
  layer so memory is isolated per user.

## Which systems use it
- [[mem0]] — implements this loop directly with `mem0.search()` (before the LLM call) and
  `mem0.add()` (after the response), both scoped by `user_id`.
- [[gbrain]] — runs the loop as `signal → search → respond → write → auto-link → sync`, with
  **brain-first lookup** (query local memory before any external API call) and typed-edge
  auto-linking on every write.
- [[letta]] — the agent reads/writes its own git-backed memory files each turn (progressive
  disclosure), with sleep-time reflection persisting learnings asynchronously.

2026 agent-memory surveys formalize this as a **write–manage–read loop** (Du 2026, POMDP framing).
Landmark designs: **Generative Agents** (Park, UIST 2023) — a *memory stream* of natural-language
observations, retrieved by a score combining **recency + importance + relevance**, plus reflection
and planning (its 25-agent Smallville sim showed emergent social behavior; ablating any of
observation/planning/reflection hurt believability); **[[a-mem]]** (NeurIPS 2025) — Zettelkasten
atomic notes that self-link into a living graph; **Memory-R1** (2025) — an RL-trained Memory Manager
(ADD/UPDATE/DELETE/NOOP) that beats Mem0 with only ~152 training examples. See [[memory-consolidation]]
and [[memory-evaluation]].

## Open questions
- How should the loop reconcile a newly stored fact that **contradicts** an older one? (See
  `_meta/open-questions.md` on staleness/contradiction handling.)
- When does injecting retrieved facts into the prompt expose the loop to **memory poisoning** from
  untrusted inputs? (The source's title raises this but its body never addresses it.)

## Sources
- `raw/articles/memory/Memory Poisoning in AI Agents How Bad Inputs Corrupt Agent Memory.md`
  — Next.js + Mem0 tutorial laying out the search-before / store-after sequence explicitly.
- `raw/articles/memory/garrytangbrain Garry's Opinionated OpenClawHermes Agent Brain.md`
  — GBrain's brain-first signal→search→respond→write→auto-link→sync loop.
- `raw/papers/Generative Agents Interactive Simulacra of Human Behavior.md` (arXiv 2304.03442, Park
  et al. 2023) — memory stream + recency/importance/relevance retrieval + reflection.
- `raw/articles/memory/LLM Memory and Knowledge: A 2025–2026 Research Map Across Four Threads.md`
  — Thread 4: write–manage–read loop surveys, Generative Agents, A-MEM, Memory-R1.
