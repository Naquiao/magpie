# claude-memory

**One-liner:** Claude's built-in chat memory (claude.ai / Desktop / Mobile): retrieval-augmented
**search over past chats** plus an auto-synthesized **memory summary** that gives every new
conversation continuity — work-focused, user-inspectable, and exportable to/from other AI tools.

## Approach
Two distinct capabilities turn a stateless chat product into one with continuity:
- **Search past chats** — on request, Claude searches prior conversations via **RAG**, surfaced as
  tool calls in the chat. Scope is bounded: all non-project chats together, or within a single project
  (projects are isolated from each other). Paid plans (Pro/Max/Team/Enterprise).
- **Memory** — Claude auto-generates memory from chat history. Available on all plans (free included).

This is the consumer-product instantiation of the [[read-write-agent-loop]] and the retrieval side of
[[context-vs-retrieval]], distinct from Claude Code's file-based memory or the API.

## Architecture
- **Memory summary:** a background process summarizes conversations and synthesizes key insights
  across chat history (excluding project chats), **refreshed every 24 hours**, and injected as context
  into every new standalone conversation — a scheduled [[memory-consolidation]] pass.
- **Project memory:** each project has its own separate memory space and dedicated summary, so context
  stays scoped and isolated per project.
- **What it captures (work-focused):** role/projects/professional context; communication preferences
  and working style; technical and coding-style preferences; project details and ongoing work.

## Store / Retrieve / Update / Forget
- **Store:** 24-hour background synthesis of conversations into the memory summary (and per-project
  summaries). Users can also tell Claude what to remember directly in a chat, or add custom
  instructions via the Manage memory modal.
- **Retrieve:** the memory summary is auto-loaded into each new standalone conversation (per-project
  for projects); on-demand RAG **search over past chats** runs as a visible tool call, with
  **citations** linking back to the source conversations.
- **Update:** re-synthesized within 24h whenever conversations are created, modified, or deleted;
  in-chat "remember this" edits apply **immediately** to the next conversation without waiting for the
  daily synthesis; the summary is directly viewable and editable.
- **Forget:** **Pause** (keep existing memory but stop using/creating it), **Reset** (permanent,
  irreversible deletion of all memory incl. project memories), **Incognito chats** (never saved to
  history or memory, excluded from search), and deleting a conversation removes it from synthesis
  (within 24h).

## Tradeoffs / limits
- **Portability (a plus):** experimental **import/export of memory between Claude and other AI tools**
  — concrete, productized cross-tool memory portability; see [[portable-memory]].
- Search past chats is **unavailable** under Enterprise customer-managed encryption keys (conversation
  content is encrypted).
- Memory is **work/collaboration-scoped** by design — not a general personal-life store.
- Enterprise: org Owners control a master toggle; disabling it **permanently deletes all users'
  memory**. Synthesis is encrypted at rest, included in data exports; incognito chats are retained
  ≥30 days for safety and remain available to Owners via export. Individual memory edits aren't
  audit-logged.

## Maturity (version, adoption, as-of date)
As-of 2026-06-25 (support article updated 2026-06-15): generally available on web, Claude Desktop, and
Claude Mobile. Search past chats requires a paid plan and is on by default once rolled out; memory
generation is available on all plans and is org-gated on Enterprise. Memory import/export is
experimental and in active development.

## Sources
- `raw/articles/Use Claude’s chat search and memory to build on previous context.md`
  — Anthropic support doc: RAG search over past chats, the 24h memory synthesis, project memory,
  view/edit/pause/reset controls, incognito chats, cross-tool memory import/export, and Enterprise
  owner controls.
