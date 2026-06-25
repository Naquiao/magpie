# Ignore list — rejected sources

Sources the `compile` operation must **skip**. Closing (not merging) a `brain/compile-*` PR rejects
the `raw/` sources it would have ingested — but those files are still in `raw/`, so without this
list the next compile would re-propose them. Entries are added **automatically** by the compile
preflight when it finds a compile PR that was closed unmerged (see `AGENTS.md` §6, "Reject
reconciliation"). The file is human-editable at any time.

To **un-reject** a source: delete its line. The next compile will reconsider it.

**Format** (one per line):

```
raw/<path> — rejected <YYYY-MM-DD> — <PR #N | manual> — <reason, optional>
```

A source whose file later changes materially is still skipped while its line is here; remove the
line if you want the new version reconsidered.

---

<!-- entries below — none yet -->
