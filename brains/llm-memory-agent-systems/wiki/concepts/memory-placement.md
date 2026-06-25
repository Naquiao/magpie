# memory-placement

**One-liner:** *Where* you put the freshly-retrieved memory block in the prompt is a cost decision:
in the system prompt it breaks prompt caching and re-bills the whole history every turn; as a
trailing message after the cache breakpoint it keeps the cache and cuts token cost up to ~2x (Zep, 2026).

## What it is
Agent memory is most useful when refreshed every turn (the [[read-write-agent-loop]] "inject" step),
but a block that changes every turn interacts badly with **prompt caching**. The rule that matters:
caching matches the request *prefix* and holds only up to the first token that differs from the
previous request.
- **System-prompt placement (the expensive default):** the memory/context block sits at the front,
  and it's re-retrieved each turn, so the prefix diverges near the top — the entire conversation
  history below it falls out of cache and is re-processed at full input price every turn. History is
  also the part that *grows*, so per-turn cost keeps rising.
- **Trailing-message placement (the fix):** attach the memory as the **last** message, after the
  history, with the cache breakpoint on the latest user message just before it. The system prompt,
  tools, and full history read from cache; only the previous reply, the new user message, and one
  fresh memory block are paid at full price each turn — a roughly *constant* cost that doesn't grow
  with the conversation.

## Why it matters for agent memory
It's the economic counterpart to the token-efficiency arguments in [[context-vs-retrieval]] and
[[memory-evaluation]]: the same context block and the same model output can cost ~2x more purely from
placement. On Claude Opus 4.8, fresh input is $5/Mtok while a cache read is $0.50 (a 90% discount;
cache writes carry a 1.25× premium, paid once; default 5-minute TTL), so keeping the long history in
cache is where the savings come from. The longer an agent runs, the more placement is worth.

## Variants / approaches
- **Fake tool message:** carry the memory in a tool-role message at the end of the request — works on
  any modern API/provider.
- **Mid-conversation system message:** Claude Opus 4.8 supports this natively — authoritative
  per-turn context appended right after the cache breakpoint without disturbing the cached prefix.
  Same placement, now a first-class API feature.
- **System-prompt placement:** simplest, and fine for short or single-shot interactions, but the cost
  penalty compounds with conversation length.

## Evidence (as-of 2026)
Zep's experiment: one agent, ~12k-token static prompt (persona + ops manual + ~12 tool schemas), a
Zep user seeded with prior conversations; the same scripted conversation replayed twice with
**identical** Context Blocks and identical model replies, so placement is the only variable. Total
cost on Claude Opus 4.8 at 18 / 36 / 54 turns was **1.3× / 1.6× / 1.9×** cheaper with trailing
placement — "up to 2x at the lengths tested, and still climbing," because system-prompt placement
re-processes a longer history each turn while trailing placement reads it from cache. Experiment code:
github.com/getzep/zep/tree/main/examples/python/claude-prompt-caching-example.

## Which systems use it
- [[zep]] — assembles a per-message **Context Block** and documents appending it as a trailing context
  message (a fake tool message, or an Opus 4.8 mid-conversation system message) rather than in the
  system prompt.
- Applies to any system that injects retrieved memory per turn — [[mem0]], [[letta]],
  [[claude-memory]] — wherever a fresh block meets a cached history.

## Open questions
- How does this trade against **memory recency** when the cache TTL (default 5 min) expires between
  turns — does bursty/low-frequency traffic erase the savings?
- Does trailing placement weaken instruction-following vs. authoritative system-prompt context (the
  reason the "natural" placement exists)? Opus 4.8 mid-conversation system messages are pitched as the
  answer; unverified here.

## Sources
- `raw/articles/Where to place agent memory in the prompt to cut token costs up to 2x.md`
  — Zep blog (Jack Ryan), 2026-06-24: prefill/KV-cache mechanics, why system-prompt placement breaks
  the cache, the trailing fake-tool-message fix, Opus 4.8 mid-conversation system messages, and the
  1.3/1.6/1.9× cost experiment.
