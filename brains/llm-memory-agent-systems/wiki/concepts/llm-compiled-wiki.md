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

## Open questions
- **Where does the plain-wiki approach stop beating RAG?** (docs? tokens? query type? — the standing
  question in `_meta/open-questions.md`; Karpathy reports fine at ~100 articles.)
- Karpathy floats **synthetic-data generation + fine-tuning** to make the LLM "know" the wiki in its
  weights rather than context — the [[in-weights-vs-in-context]] frontier.

## Sources
- `raw/articles/memory/Andrej Karpathy on X "LLM Knowledge Bases...".md`
  — the raw→compile→ask→lint→output loop, Obsidian-as-IDE, the ~100-article / 400K-word scale claim.
