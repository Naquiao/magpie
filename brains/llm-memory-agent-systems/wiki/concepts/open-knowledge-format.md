# open-knowledge-format

**One-liner:** OKF — an open spec (Google Cloud, v0.1, June 2026) that formalizes the
[[llm-compiled-wiki]] pattern into a portable, vendor-neutral format: a directory of markdown files +
YAML frontmatter that any producer can write and any agent can consume without a translation layer.

## What it is
A standard for representing the metadata, context, and curated knowledge that agentic systems need,
explicitly generalizing Karpathy's LLM-wiki gist into an interoperable format. An OKF **bundle** is a
directory of markdown files, each representing one **concept** (a table, dataset, metric, runbook,
API, …); the file path *is* the concept's identity. Each file has YAML frontmatter for the few
queryable structured fields and a markdown body for everything else.
- **"Just markdown, just files, just YAML frontmatter"** — readable in any editor, renderable on
  GitHub, shippable as a tarball, hostable in any git repo. No SDK, no runtime, no required service.
- Concepts cross-link with normal markdown links, turning the directory into a **graph** richer than
  the filesystem hierarchy (see [[knowledge-graphs-for-memory]]).
- Optional `index.md` files (progressive disclosure as an agent navigates the hierarchy) and `log.md`
  files (chronological change history) — the same two special files as the [[llm-compiled-wiki]] method.
- Frontmatter fields: **`type`** (the only required field), plus `title`, `description`, `resource`,
  `tags`, `timestamp`.

## Why it matters for agent memory
It targets the portability/interop gap in [[portable-memory]]: every team's wiki, every vendor
catalog, and every agent "brain" already look alike (markdown + frontmatter + cross-links) but none
are designed to cooperate, so knowledge stays siloed and every agent builder re-solves context
assembly from scratch. OKF makes the *at-rest* knowledge format a shared contract — complementary to
**MCP**, which standardizes the *transport*. Three design principles:
1. **Minimally opinionated** — requires only a `type` field; the rest of the content model is the
   producer's choice. The spec defines the interoperability surface, not the schema.
2. **Producer/consumer independence** — a human-authored bundle can be read by an agent; an
   LLM-synthesized bundle queried by another; a pipeline export browsed in a visualizer. The format
   is the contract; tooling at each end is independently swappable.
3. **Format, not platform** — no proprietary cloud, model, or account required to read/write/serve.

## Variants / approaches
- **Producer reference impl:** an enrichment agent that walks a BigQuery dataset, drafts an OKF
  concept doc per table/view, then runs a second LLM pass crawling authoritative docs to add
  citations, schemas, and join paths.
- **Consumer reference impl:** a single self-contained static HTML visualizer that renders any bundle
  as an interactive graph (no backend, no install, no data leaves the page).
- **Sample bundles:** GA4 e-commerce, Stack Overflow, and Bitcoin public datasets, committed as
  living conformant examples.
- Google Cloud's Knowledge Catalog was updated to ingest OKF and serve it to its agents.

## Which systems use it
- The [[llm-compiled-wiki]] pattern (Karpathy) is the direct ancestor; OKF is its standardization.
  This brain is itself an instance of that pattern (markdown + frontmatter + `index.md`/wikilinks) and
  is already close to OKF-shaped.
- Adjacent conventions OKF generalizes: Obsidian vaults wired to coding agents, the AGENTS.md /
  CLAUDE.md family of convention files, and "metadata as code" repos inside data teams.

## Open questions
- Does a shared knowledge *format* actually win multi-vendor adoption, or stay a Google-published
  spec? (Its value scales with how many parties speak it, not who owns it.)
- How does OKF interoperate with MCP memory servers in practice — is OKF the on-disk format an MCP
  "memory" server exposes? (See [[portable-memory]].)
- v0.1 is deliberately minimal; what does real agent use reveal it's missing?

## Sources
- `raw/articles/How the Open Knowledge Format can improve data sharing.md`
  — Google Cloud Data Cloud team (Sam McVeety, Amir Hormati), 2026-06-12: OKF v0.1 spec, bundle/concept
  design, the three principles, reference producer/consumer + sample bundles; repo at
  github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf.
