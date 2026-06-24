# mem0

**One-liner:** A managed (and self-hostable) memory layer that extracts semantic facts from agent
interactions, stores them scoped to a `user_id`, and retrieves only the relevant ones per query —
optimized for **token efficiency** (high benchmark accuracy at ~7K tokens/query vs. 25K+ for
full-context approaches).

## Approach
Mem0 treats memory as **semantic facts, not transcripts**. Instead of stuffing full chat history
into every prompt (which blows up tokens, retrieves indiscriminately, and dies when a session ends),
an app calls Mem0 to extract durable facts and fetch the handful relevant to the current message.
Mem0 is **model-agnostic** — it sits outside the generation call, so the same pipeline works with
OpenAI, Anthropic, Mistral, Groq, or the Vercel AI SDK. The team frames good memory as solving
**extraction + retrieval + reasoning together** (not just retrieval). See [[context-vs-retrieval]]
for the problem and [[read-write-agent-loop]] for the surrounding loop.

## Architecture
Two SDK calls wrap an otherwise normal LLM request, both scoped by `user_id`:
- `mem0.search(query, { user_id, limit })` → top-k semantically relevant facts, run **before** the LLM call.
- `mem0.add(messages, { user_id })` → extract and persist facts, run **after** the response.

Memory is stored server-side (managed platform or self-hosted), persisting across sessions, devices,
and channels as long as the app resolves a stable `user_id`. Extraction and retrieval run
**asynchronously** so agents don't burn cycles managing context. The architecture is moving toward
**hierarchical memory** where layers (sentence-level, entity-level, and planned behavioral-pattern
matching) are scored in parallel and fused. See [[hybrid-retrieval]] and [[knowledge-graphs-for-memory]].

## Store / Retrieve / Update / Forget
- **Store:** `mem0.add()` extracts semantic facts and discards conversational scaffolding (e.g.
  "User reported missing order #1234", "prefers email over SMS"). As of the April 2026 algorithm,
  **agent-generated facts are first-class** (e.g. "I've booked your flight for March 3"), closing a
  prior blind spot.
- **Retrieve:** **multi-signal** — semantic similarity + keyword matching + entity matching scored
  in parallel and fused by rank scoring; entity linking gives matching memories a ranking boost;
  keyword normalization handles conjugation variants ("attend" vs "attending"). App injects the
  top-k into the system prompt. ~100–200ms.
- **Update:** **single-pass, ADD-only extraction** (April 2026) — one LLM call that only adds; every
  fact is an independent record, so a changed fact lives **alongside** the old one and both survive
  (preserving the full history of state changes). This replaced the old two-pass ADD/UPDATE/DELETE
  reconciliation, which was slow and destroyed context. See [[temporal-knowledge-and-decay]].
- **Forget:** ADD-only deliberately avoids deletion/overwrite to retain history; explicit
  decay/expiry policies are not described by the current sources.

## Tradeoffs / limits
- Retrieval quality depends on Mem0's fact extraction; the app trusts what it extracts.
- ~100–200ms search latency per request (small vs. a 500–2000ms LLM call; can be hidden via
  `Promise.all()`).
- `user_id` **must** come from a trusted auth layer, never a client-supplied value, or memory is
  read/written under the wrong identity.
- ADD-only keeps everything, which aids temporal reasoning but grows the store; the hardest
  long-range tasks (temporal reasoning, event ordering, multi-session reasoning at 10M-token scale)
  remain weak — fact- and entity-level matching aren't enough. Managed-platform benchmark numbers
  include proprietary optimizations not in the OSS SDK. See [[memory-evaluation]].

## Maturity (version, adoption, as-of date)
As-of 2026-06-24: Managed platform (free tier at app.mem0.ai) + **self-hostable via Docker** with an
identical API; OSS SDK on GitHub (`mem0ai`, Node SDK pinned `^2.1.40` in the reference tutorial).
The token-efficient algorithm (April 2026) is live on both platform and SDK and reports LoCoMo 91.6,
LongMemEval 93.4, BEAM 64.1 (1M) / 48.6 (10M) at <7K tokens/query; eval framework is open-source.

## Sources
- `raw/articles/memory/Introducing The Token-Efficient Memory Algorithm.md`
  — single-pass ADD-only extraction, entity linking, multi-signal retrieval, benchmark results.
- `raw/articles/memory/Memory Poisoning in AI Agents How Bad Inputs Corrupt Agent Memory.md`
  — Mem0 + Next.js build tutorial (title promises "memory poisoning" defenses the body never covers;
  see `_meta/open-questions.md`).
