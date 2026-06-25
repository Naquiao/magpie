# memory-curation

**One-liner:** Treat what an agent *stores* as a curation problem, not a logging problem — selective
addition plus history-based deletion beat hoarding, because "experience-following" makes the quality
of stored memories propagate into future behavior.

## What it is
A write-side discipline for agent memory: deciding which experiences are worth keeping and actively
pruning the rest, rather than storing every interaction. It rests on one empirical behavioral law
and two control levers (Xiong et al. 2025, "How Memory Management Impacts LLM Agents", arXiv 2505.16067):
- **Experience-following:** high *input* similarity between the current task and a retrieved memory
  yields high *output* similarity between their executions. Stored examples act as few-shot
  demonstrations — so a correct memory accelerates the agent, and an erroneous one propagates as a
  repeating error ("bad memories don't just linger, they create a propagating error feedback loop").
- **Selective addition:** "simply storing every experience leads to significantly worse outcomes."
  Across three agents (electronic health records, the AgentDriver autonomous-driving agent, and a
  network-security agent), an *add-all* policy did **worse than adding no memory at all**; strict
  evaluation + filtering before storage gave an average **+10%** performance boost.
- **Improvement through deletion:** memories with high input similarity but consistently *low* output
  similarity ("misaligned experience replay") drag performance down. **History-based deletion** —
  pruning entries with repeatedly low utility — gave the best long-term boost while keeping the
  store bounded.

## Why it matters for agent memory
It reframes "more memory = better" as false. Memory is a curated knowledge base whose value is set
by its *worst* entries, not its size: because of experience-following, a bad memory doesn't sit
inert — it gets retrieved and replayed. This is the conceptual case for a **write-time quality gate**
in the [[read-write-agent-loop]] (the "store" step needs a filter, not just an append) and for
treating deletion as a first-class operation alongside [[temporal-knowledge-and-decay]] and
[[memory-consolidation]].

## Variants / approaches
- **Evaluation-gated addition:** score a candidate against strict criteria before storing; reject
  low-value ones (Xiong et al.).
- **History-based deletion:** track per-memory utility over time and prune persistently misaligned
  entries (the study's best performer) — vs. random or pure similarity-based deletion.
- **A write-time quality gate / `REJECT` action:** the [[mem0]] audit (#4573) argues the
  ADD/UPDATE/DELETE/NONE decision set lacks a "this isn't worth storing" verb; a fifth action or a
  pre-storage scorer would serve as the gate. Two philosophies clash: *store-everything-then-subtract*
  (keep raw data, let reranker/TTL/decay filter over time — "better to have something you can delete
  than something missing you'll never know about") vs. *reject-at-ingestion* (NONE-by-default — "a
  missed fact can be re-extracted later, a duplicate pollutes every future session").
- **Typed-taxonomy gate:** require every memory to declare a type (identity/event/insight/directive);
  transient state has no valid type and structurally cannot be stored (Engram's three-tier write gate).
- **Feedback-loop prevention:** don't re-extract recalled memories, or hallucinations amplify — see
  the 808-copy "User prefers Vim" case in [[mem0]].

## Which systems use it
- [[mem0]] — the audit (#4573) is the field's starkest real-world confirmation: **97.8% of 10,134
  production entries were junk**, and recall improved immediately after pruning. The community fixes
  it spawned (NONE-by-default decision prompt, negative few-shot extraction, cosine-dedup gate,
  three-tier write gates) are all memory-curation mechanisms.
- Stanford **Generative Agents**, LangMem, [[letta]] — cited in the audit as frameworks that *score
  candidates before storage*, unlike mem0's straight-to-store default. See [[read-write-agent-loop]].
- [[gbrain]] — salience scoring + contradiction pruning in the dream cycle ([[memory-consolidation]])
  is curation run offline.

## Open questions
- **Where should the gate live** — message-level pre-filter, extraction prompt, decision step, or
  post-hoc decay? (The audit thread debates all four; none alone is sufficient.)
- **Store-everything-then-subtract vs. reject-at-ingestion** — the former preserves the audit data
  that makes tuning possible; the latter never pollutes recall. Unresolved tradeoff.
- How to *measure* curation quality directly — existing benchmarks score end-to-end recall, not
  whether what's stored is worth storing. See [[memory-evaluation]].

## Sources
- `raw/articles/Smarter Memories, Stronger Agents How Selective Recall Boosts LLM Performance.md`
  — HBS AI Institute summary of Xiong et al. 2025 (arXiv 2505.16067): experience-following, selective
  addition (add-all worse than no memory; +10% from filtering), history-based deletion.
- `raw/articles/What we found after auditing 10,134 mem0 entries 97.8% were junk · Issue 4573 · mem0aimem0.md`
  — production audit confirming "indiscriminate storage worse than no memory"; the missing write-time
  quality gate, the proposed REJECT action, and feedback-loop prevention.
