# llm-compiled-wiki

**One-liner:** Dump raw sources into `raw/`, have an LLM incrementally **compile** them into a
markdown wiki of linked concept/system articles + index files, then query / lint / render against it
— Karpathy's method, and the design this very brain implements.

## What it is
A personal-knowledge-base workflow where the LLM, not the human, owns the wiki (Karpathy, 2026):
- **Ingest:** index source documents (articles, papers, repos, datasets, images) into a `raw/`
  directory — no organizing.
- **Compile:** an LLM incrementally writes/maintains a wiki of `.md` files — summaries of everything
  in `raw/`, backlinks, categorization into concepts, articles, and links between them.
- **Q&A:** ask complex questions against the wiki; the LLM auto-maintains index files and brief
  per-doc summaries and reads the relevant docs — "I thought I had to reach for fancy RAG," but at
  small scale plain index + summaries suffice.
- **Output:** render answers as markdown, Marp slide decks, or matplotlib figures, then **file good
  outputs back into the wiki** so explorations compound.
- **Lint:** periodic LLM health checks — find inconsistencies, impute missing data via web search,
  surface new article candidates.

**Three layers** (Karpathy's gist): **raw sources** (immutable; the LLM reads but never edits — the
source of truth), **the wiki** (LLM-owned markdown: summaries, entity/concept pages, comparisons,
synthesis), and **the schema** (a `CLAUDE.md` / `AGENTS.md` that encodes the conventions and workflows
— the config that makes the LLM a disciplined maintainer rather than a generic chatbot, co-evolved
over time). The defining claim: the wiki is a **persistent, compounding artifact** — knowledge is
*compiled once and kept current*, not re-derived per query like [[vector-rag]], so cross-references,
flagged contradictions, and synthesis already exist before you ask. Two special files navigate it:
**`index.md`** (a content-oriented catalog, read first on any query) and **`log.md`** (an append-only
chronological record of ingests/queries/lints). "Obsidian is the IDE; the LLM is the programmer; the
wiki is the codebase." The idea descends from Vannevar Bush's **Memex** (1945) — associative trails
between documents — with the LLM finally absorbing the maintenance burden that makes humans abandon wikis.

## Why it matters for agent memory
This is the thesis behind this brain (see `BRAIN.md` / `AGENTS.md`). Its central claim is a scale
argument against [[vector-rag]]: at Karpathy's reported **~100 articles / ~400K words**, an LLM
reading auto-maintained index + summary files beats standing up a vector store — the index files
*are* the retrieval layer. It is one concrete operating point on [[context-vs-retrieval]].

## Variants / approaches
- **Pure-files** (this brain; Karpathy's setup): markdown + `[[wikilinks]]` + `index.md` /
  `sources.md`, viewed in Obsidian as the "IDE."
- **Productized / outgrown-files:** [[gbrain]] — the same compile→query→consolidate loop, but backed
  by Postgres hybrid retrieval + a self-wiring graph + a dream cycle once you pass ~hundreds of docs.
- **Standardized / portable:** [[open-knowledge-format]] (Google Cloud OKF) turns the same
  markdown+frontmatter+cross-links shape into a vendor-neutral spec so bundles interoperate across
  producers and agents. Optional tooling at scale: a local hybrid-search CLI/MCP over the markdown
  (e.g. `qmd` — BM25 + vector + LLM rerank) for when plain `index.md` retrieval outgrows itself.

## Open questions
- **Where does the plain-wiki approach stop beating RAG?** (docs? tokens? query type? — the standing
  question in `_meta/open-questions.md`; Karpathy reports fine at ~100 articles.)
- Karpathy floats **synthetic-data generation + fine-tuning** to make the LLM "know" the wiki in its
  weights rather than context — the [[in-weights-vs-in-context]] frontier.

## Sources
- `raw/articles/llm-wiki - Karpathy.md` — Karpathy's full LLM-wiki gist: the three-layer architecture
  (raw / wiki / schema), ingest/query/lint operations, `index.md` vs `log.md`, optional `qmd` search,
  the Memex lineage, and the "compiled-once, kept-current" compounding thesis.
- `raw/articles/memory/karpathy-tweet-llm-knowledge.md` — Karpathy's tweet pointing to the gist: the
  raw→compile→ask→lint→output loop, Obsidian-as-IDE, and the ~100-article / ~400K-word scale claim vs RAG.
