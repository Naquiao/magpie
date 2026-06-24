# letta

**One-liner:** A "memory-native" agent platform (MemGPT lineage) whose Letta Code harness gives agents a **git-versioned memory filesystem** they own and edit, so they learn by managing their own context rather than by updating model weights.

## Approach
Letta's thesis is **experiential AI**: agents that improve by learning from their own experience.
Instead of fine-tuning weights, Letta agents build durable **token-space representations** of who
they are and what they know, and actively manage their own context. The **Context Constitution** (a
living document written directly to the agents, published on GitHub) codifies the principles: how
context forms identity/memory/continuity, how to treat context as a scarce resource, and how to
self-improve in token-space (an in-context-vs-in-weights stance — see [[context-vs-retrieval]]).

## Architecture
**Context Repositories** are the memory substrate: a git-backed filesystem the Letta Code agent
clones locally, so it can use its full terminal/coding abilities (bash, scripts, subagents) to
manage memory. Key pieces:
- **Progressive disclosure** — the filetree is always in the system prompt; folder/file names are
  navigational signals; each memory file carries YAML frontmatter describing its contents (same
  shape as Anthropic `SKILL.md`). A `system/` directory designates files always fully loaded.
- **Memory swarms** — because memory is git-backed, subagents work in isolated **git worktrees**,
  process memory concurrently, and merge back via standard git conflict resolution (breaking the
  historical single-threaded limit on memory formation).
- **Sleep-time compute** — background subagents reflect and reorganize memory off the main thread.

## Store / Retrieve / Update / Forget
- **Store:** agent writes to memory files; every change is a git commit with an informative message.
- **Retrieve:** progressive disclosure — filetree + frontmatter descriptions guide the agent to
  `read` the right files; `system/` files are always pinned to context. See [[read-write-agent-loop]].
- **Update:** agents rewrite their own context and system prompts; **memory reflection** (sleep-time)
  periodically persists important info from recent conversation history into the repo. See
  [[memory-consolidation]].
- **Forget:** **memory defragmentation** backs up the filesystem, then a subagent reorganizes it —
  splitting large files, merging duplicates, restructuring into ~15–25 focused files. Git history
  retains prior versions, so "forgetting" is reorganization, not destruction. See
  [[temporal-knowledge-and-decay]].

## Tradeoffs / limits
- File/git-based memory is universal and inspectable but pushes management work onto the agent
  (it must curate its own hierarchy and frontmatter).
- Git worktrees enable concurrent memory writes but add merge/conflict-resolution complexity.
- Letta argues memory capability has stalled industry-wide as labs prioritize coding benchmarks —
  i.e. the surrounding model layer is not optimized for this; an explicit motivation, not a result.

## Maturity (version, adoption, as-of date)
As-of 2026-06-24: Letta Code installs via `npm install -g @letta-ai/letta-code`. Context
Repositories enabled per-agent with `/memfs` (detaches the older `memory(...)` tool and syncs
existing memory blocks into the git filesystem); the prior approach was MemGPT-style memory tools /
virtual filesystem ops. Context Constitution is at its first public version (2026-04-02). Adoption
numbers not established by the current sources.

## Lineage — MemGPT
Letta is the MemGPT team's company. **MemGPT** (Packer et al. 2023) introduced **virtual context
management**: borrowing the OS memory-hierarchy idea, the LLM treats its context window as "RAM" and
an external store as "disk," and uses function calls to page information in and out — giving the
appearance of unbounded memory for long conversations and document analysis beyond the context
window. Context Repositories generalize this from MemGPT-style memory tools to a full git-backed
filesystem (see Next steps below / [[read-write-agent-loop]]).

## Sources
- `raw/papers/MemGPT Towards LLMs as Operating Systems.md` (arXiv 2310.08560, Packer et al. 2023)
  — OS-inspired virtual context management; the origin of the Letta approach.
- `raw/articles/memory/Introducing Context Repositories Git-based Memory for Coding Agents.md`
  — git-backed memory filesystem, progressive disclosure, memory swarms/defrag.
- `raw/articles/memory/Context Constitution.md`
  — principles governing how Letta agents manage context to learn from experience.
