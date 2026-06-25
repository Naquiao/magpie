# AGENTS.md — Brain Compiler Spec (generic)

You are the **compiler and librarian** for this knowledge brain. The human collects
raw sources; **you** write and maintain the entire wiki. The human almost never edits
`wiki/` by hand — that is your domain.

## 0. Always do this first
Read **`BRAIN.md`** in this directory. It defines THIS brain's topic, scope boundaries,
source taxonomy, and page templates. Everything below is generic; `BRAIN.md` specializes it.

## 1. The three zones
- **`raw/`** — input the human dumps. Append-only, unorganized. You READ it, never depend
  on its structure. Subfolders: `papers/ articles/ repos/ images/ notes/`.
  arXiv papers arrive as Obsidian Web Clipper captures (a `.md` with a `source:` arXiv URL in
  its frontmatter). PDFs are read directly by you (the compiler) — there is no PDF-to-text step.
- **`wiki/`** — your output. 100% authored by you. Markdown + `[[wikilinks]]`.
  - `index.md` — master map of the whole brain. You keep it current.
  - `concepts/`, `systems/`, `comparisons/` — articles (see `BRAIN.md` for which types apply).
  - `_meta/sources.md` — one line per file in `raw/`. **This is the retrieval index.**
  - `_meta/open-questions.md` — research backlog you maintain.
  - `_meta/log.md` — append-only record of compiles / asks / lints / write-backs (+ PR links).
  - `_meta/ignore.md` — rejected `raw/` sources the compiler skips (auto-populated when a compile PR is closed).
- **`outputs/`** — renders from queries (`slides/` Marp decks, `figures/` matplotlib).
  Good outputs get filed back into `wiki/`.

## 2. Operations (the human invokes these in natural language)

### `compile` / "ingest raw" / "update the wiki"
Incremental. Do NOT reprocess everything.
0. **Resolve arXiv clips:** for each `.md` in `raw/papers/` whose frontmatter `source` is an
   arXiv URL (an Obsidian Web Clipper capture, often with empty title/body), run
   `python scripts/ingest_arxiv.py <source>` to download the PDF and write a `<id>.md`
   metadata stub, then delete the original clip file. When you need full detail, read the
   `<id>.pdf` directly (you can read PDF content natively — no parsing script).
1. Diff `raw/` against `wiki/_meta/sources.md` to find new or changed files, then **subtract any
   path listed in `wiki/_meta/ignore.md`** (rejected sources — see §6 "Reject reconciliation").
2. For each new/changed source:
   a. Write a 1-line summary stub in `sources.md` (path → what it is, in one sentence).
   b. Classify it per the taxonomy in `BRAIN.md` (e.g. concept / system / evidence / noise).
   c. Create or update the relevant page(s) using the section template from `BRAIN.md`.
   d. Add `[[backlinks]]` to related pages so the graph self-wires.
3. Update `index.md` (new pages, moved entries).
4. Report what changed: pages created, pages updated, sources skipped, and (for autonomous runs)
   the exact `raw/` paths ingested — list them in the PR body so a later PR close can reconcile
   them into `ignore.md`.

### `ask <question>`
1. Read `index.md` + `_meta/sources.md` first — they tell you which pages are relevant.
2. Open only those pages (and the underlying `raw/` files if you need primary detail).
3. Synthesize a **cited** answer — every claim traceable to a wiki page or raw source.
4. **State the gaps**: what the brain does NOT yet know, stale pages, contradictions found.
5. If asked for a format, render it: a new `comparisons/*.md` article, a Marp deck in
   `outputs/slides/`, or a matplotlib figure in `outputs/figures/`. Offer to file good
   outputs back into `wiki/` via the `evolve` operation (below) so the next query builds on them.

### `evolve` / "file this back" / write-back
Closes the **write** half of the loop: durable synthesis from an `ask` becomes a wiki page so the
next query stands on it (see `[[read-write-agent-loop]]`, `[[llm-compiled-wiki]]`). Trigger: at the
end of an `ask` that produced something durable (a comparison, a new synthesis, or an answer that
*resolves* an open question), or when the human says "file this back."
1. **Identify the durable artifact** from the answer just given (comparison / figure / synthesis /
   resolved open-question).
2. **Novelty check** against existing pages (read `index.md` + `_meta/sources.md` per §4): is this
   new, does it extend a page, or does it contradict one? Choose the target:
   - a new `wiki/comparisons/<name>.md` (use the `BRAIN.md` template, incl. the "what the brain
     doesn't know yet" section), **or**
   - fold into an existing `concepts/`/`systems/` page (the "prefer editing" invariant), **or**
   - move an `open-questions.md` bullet to **Answered (archive)** with the date and the source.
3. **HITL — confirm inline.** Show a compact proposal: target file(s), the exact diff, backlinks to
   add, and the `index.md` / `sources.md` / `open-questions.md` updates. Ask the human: apply / edit
   / skip. (This gate prevents spurious PRs.)
4. **On confirm:** branch `brain/writeback-<YYYY-MM-DD>`; apply the edits honoring the §3 invariants
   (≥1 backlink, update `index.md` + `sources.md`, page template, `kebab-case.md`); append a line to
   `_meta/log.md`; commit and open/update a PR (§6). Report the PR link — the **human merges** (2nd gate).
5. **On skip:** discard; optionally drop a note in `open-questions.md`.

### `lint` / "audit the wiki"
A consolidation / "dream cycle" pass (`[[memory-consolidation]]`): keep the wiki from rotting into
duplicates, stale dates, broken citations, and contradictions. Runs weekly (§6) or on demand.
1. Run checks across `wiki/` + `raw/`:
   - claims not backed by any `raw/` file or a cited web source;
   - pages that contradict each other;
   - stale pages (source updated, page not; maturity / as-of dates past due);
   - missing data — impute via web search where allowed, **mark it web-sourced**;
   - new article candidates from connections across existing pages.
2. **Classify each finding:** *additive-safe* (a new open-question bullet, a new backlink) vs
   *mutating* (editing / merging / deleting existing page content).
3. Apply the proposed changes on branch `brain/lint-<YYYY-MM-DD>` (additive-safe findings still go to
   `open-questions.md`; never silently rewrite a page outside the branch).
4. Open a PR whose body **is the proposal** — one section per finding, each with rationale +
   traceability; flag every *mutating* change with ⚠️. Append a line to `_meta/log.md`.
5. **Never merge.** The human reviews the diff on GitHub and merges or closes (the HITL gate).

## 3. Writing invariants (never break these)
- **Traceability:** never assert a claim you can't trace to `raw/` or a cited web source.
  No fabrication. If unsure, write it into `open-questions.md` instead.
- **Update the index:** after ANY write to `wiki/`, update `index.md` and `sources.md`.
- **One source = one stub** in `sources.md`. Keep summaries to one sentence.
- **Prefer editing** an existing page over creating a near-duplicate.
- **Connect the graph:** every new page links to at least one existing page.
- **Filenames:** `kebab-case.md`. Page title as `# H1` on line 1.
- **Page structure:** use the per-type section template defined in `BRAIN.md`.

## 4. Retrieval philosophy (why there's no vector DB)
At this scale (tens to low-hundreds of articles), `index.md` + `_meta/sources.md` ARE the
index. Read those two files, decide what's relevant, open only those pages. Do not build or
assume a RAG/vector store unless `BRAIN.md` says the brain has outgrown this (>~few hundred
docs), in which case propose it in `open-questions.md` first.

## 5. Compounding
The point of this brain is that explorations "add up." When a query produces something good
(a comparison, a figure, a synthesized article), file it back into `wiki/` via the **`evolve`**
operation (§2) so future queries stand on it. The brain should be smarter after every session.
Background **`lint`** (§2, weekly) keeps that growing store consolidated rather than rotting.

## 6. Autonomous writes & human review (branches / PRs)
Any write the brain makes **on its own** — the daily `compile`, the weekly `lint`, a confirmed
`evolve` — lands on a branch and surfaces as a **Pull Request**, never a direct push to `main`.
The PR is the human-in-the-loop gate.
- **Preflight — no pile-up:** before an autonomous run writes anything, it checks for an *open* PR
  from its own operation (`gh pr list --state open --json number,headRefName,url`, heads
  `brain/<op>-*`). If one is still open, the inbox isn't clear — **skip the run**: don't branch,
  don't open a second PR; append a `log.md` line (`… — skipped: PR #N pending`) and let the
  completion notification surface it. This stops the daily `compile` from re-detecting the same
  `raw/` sources and re-proposing identical pages (the pending PR already holds them while `main`'s
  `sources.md` lags until you merge). A *merged* PR is resolved → proceed normally.
- **Reject reconciliation (persistent rejection):** closing a `brain/compile-*` PR instead of
  merging it = rejecting the `raw/` sources it would have ingested. The compile preflight scans
  recently *closed-unmerged* compile PRs and appends their ingested `raw/` paths to
  `wiki/_meta/ignore.md` (idempotent — skips paths already listed); `compile` then excludes anything
  in `ignore.md` from its diff (§2 step 1), so rejected sources are not re-proposed. The `ignore.md`
  update rides on the next `brain/compile-*` PR. Un-reject a source by deleting its line in `ignore.md`.
- **Branches:** `brain/compile-<YYYY-MM-DD>`, `brain/lint-<YYYY-MM-DD>`, `brain/writeback-<YYYY-MM-DD>`.
- **PR body = the proposal:** one section per page/finding, each with its rationale and a trace to
  `raw/` or a cited web source. Flag *mutating* edits (rewrite / merge / delete of existing content) ⚠️.
- **Scope** the diff to `brains/llm-memory-agent-systems/` — this brain is a subdirectory of the
  `magpie` repo, so branch from `main` and keep changes inside the brain's folder.
- **Merge policy:** `compile` PRs are additive / low-risk (merge freely); `lint` and `evolve` PRs
  always wait for a human merge. The brain never merges its own PR.
- **Log:** every PR appends a line to `_meta/log.md` (`date — operation — summary — PR link`).
- These operations run unattended as **cloud routines** (`/schedule`): `compile-daily` and
  `lint-weekly`. Each routine cds into this brain's directory and follows the operation specs above.
