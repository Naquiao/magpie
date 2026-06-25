# portable-memory

**One-liner:** Making agent memory portable across models and clients (Claude / Gemini / Cursor) —
why natural-language / structured stores surfaced over **MCP** beat both raw-embedding stores and
weight editing.

## What it is
The problem of a durable memory layer that follows a user/project across LLM providers and tools,
rather than being locked to one model. Three structural facts (per the 2025–2026 research map) decide
the design:
- **Embeddings are model-specific.** A vector from one embedding model isn't interpretable by
  another; switching LLM/embedding providers invalidates the index. Natural-language memories are
  universal — any model can read them, and they can be **re-embedded on demand** for whatever
  retrieval stack is in use.
- **Weight-level approaches are inherently non-portable.** Parametric knowledge and
  [[model-editing]] modify one model's parameters; they cannot transfer across models and fail at
  lifelong scale anyway. A strong argument for keeping durable memory *external and textual*.
- **MCP (Model Context Protocol)** — Anthropic's open, JSON-RPC, model-agnostic standard (Nov 2024),
  adopted across OpenAI/Google/Cursor/Cline through 2025–2026 — separates the LLM host from tool/data
  servers (Tools/Resources/Prompts). "Memory" is now a recognized MCP server category for persistent
  cross-session storage: one memory server can back any compliant client.

## Why it matters for agent memory
It is the sourced answer to this brain's open question on **portable cross-workspace project
memory** (from `notes/Memory In Action by Naquiao.md`): keep the source of truth as human-readable
text (optionally graph-structured), expose it over MCP, and treat embeddings as a *disposable local
index*. This sidesteps both raw-embedding lock-in and weight-editing fragility, and keeps memory
auditable and editable. It is the portability lens on [[context-vs-retrieval]] and
[[in-weights-vs-in-context]].

## Variants / approaches
- **Text store + MCP server (recommended):** atomic notes/facts (A-MEM / Mem0 style), optional graph
  structure, re-embedded locally for retrieval; see [[knowledge-graphs-for-memory]], [[vector-rag]].
- **Git repo as portable substrate:** markdown-in-git ([[llm-compiled-wiki]], [[gbrain]]) moves with
  the project across machines and clients.
- **Standardized portable format (OKF):** [[open-knowledge-format]] turns the at-rest knowledge into a
  vendor-neutral markdown+frontmatter spec — the on-disk complement to MCP's transport, so a bundle
  written by one producer is consumable by any agent without translation.
- **Raw-vector store (limited):** acceptable *only* if a single target model and a stable embedding
  provider are guaranteed — otherwise the index is non-portable.
- **Weight editing (non-portable):** reserve for single-model, bounded-edit research use.

## Which systems use it
- [[gbrain]] — markdown-in-git system of record + MCP server (30+ tools), re-embeds into Postgres.
- [[letta]] — MCP connectors over a git-backed memory filesystem.
- [[mem0]] — model-agnostic text-fact store; ships an MCP/OpenMemory surface for cross-tool memory.
- [[claude-memory]] — ships experimental **memory import/export between Claude and other AI tools**,
  the portability thesis productized for a consumer assistant.

## Open questions
- **Embedding-space standardization** would shrink the portability penalty of vector stores — does it
  ever arrive?
- MCP's 2026 roadmap items (stateful-session scaling, task lifecycles, governance) are unresolved.

## Sources
- `raw/articles/memory/LLM Memory and Knowledge: A 2025–2026 Research Map Across Four Threads.md`
  — "Implications for Portable, Model-Agnostic Memory": embeddings non-portable, weight editing
  non-portable, MCP as the model-agnostic integration layer, text-store + MCP design recommendation.
- `raw/articles/How the Open Knowledge Format can improve data sharing.md`
  — OKF: a vendor-neutral, portable knowledge format, the at-rest complement to MCP. See [[open-knowledge-format]].
- `raw/articles/Use Claude’s chat search and memory to build on previous context.md`
  — Claude's experimental cross-tool memory import/export. See [[claude-memory]].
