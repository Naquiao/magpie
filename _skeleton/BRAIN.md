# BRAIN.md — {{BRAIN_NAME}}

> This is the ONLY file you edit by hand to specialize a brain. `AGENTS.md` (the engine)
> reads this to know the topic, boundaries, and page shapes. Fill in every `{{...}}` and
> the TODO sections, then start dumping sources into `raw/`.

Created: {{DATE}}
Slug: `{{BRAIN_SLUG}}`

## Topic
One line describing what this brain is about.
> TODO: e.g. "State of the art in X: the main approaches, the systems that implement them,
> and how they compare."

## Scope
**In scope** (the agent should ingest and write about):
- TODO bullet
- TODO bullet

**Out of scope** (ignore or just leave a stub in `sources.md`; do NOT write articles):
- TODO bullet
- TODO bullet

> Tight boundaries keep the wiki from sprawling. When in doubt, the agent asks before
> creating a new top-level area.

## Source taxonomy
How to classify what lands in `raw/`. The agent uses this during `compile`.
- **papers/** → research papers. Usually map to a **concept** page and/or update a **system** page.
- **articles/** → blog posts, docs, news. Map to whichever concept/system they discuss.
- **repos/** → codebases. Map to a **system** page.
- **notes/** → your own thoughts/voice notes. May seed an **open question** or a concept.
- **images/** → diagrams referenced by pages. Not pages themselves.

## Page types for this brain
Define what kinds of articles exist and their section template. Defaults below — edit freely.

### Concept  (`wiki/concepts/<name>.md`)
A reusable idea, technique, or category.
```
# <Concept name>
**One-liner:** ...
## What it is
## Why it matters
## Variants / approaches
## Open questions
## Sources
```

### System  (`wiki/systems/<name>.md`)
A concrete product/library/implementation.
```
# <System name>
**One-liner:** ...
## Approach
## Architecture
## How it does <the core thing for this topic>
## Tradeoffs / limits
## Maturity (version, adoption, as-of date)
## Sources
```

### Comparison  (`wiki/comparisons/<name>.md`)
Cross-cutting analysis across multiple concepts/systems. Usually generated from a query.

## Seed concepts (optional bootstrap)
Page titles to create as the brain fills up. These are TOPICS, not claims — the agent fills
them from `raw/`.
- TODO
- TODO

## Naming & conventions
- Files: `kebab-case.md`. Refer to pages as `[[kebab-case]]`.
- Date any maturity/"current state" claim with an as-of date.
