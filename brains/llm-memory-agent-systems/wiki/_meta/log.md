# Log — append-only

Chronological record of everything the brain does to itself: `compile`, `evolve` (write-back),
and `lint` runs. The `log.md` from `[[llm-compiled-wiki]]` (Karpathy's method) that the brain
previously lacked. **Append only — never edit or delete past lines.**

Format (one line per run, newest at the bottom):

```
YYYY-MM-DD — <operation> — <one-line summary> — <PR link or "interactive">
```

`<operation>` is one of: `compile` · `ask` · `evolve` · `lint` · `meta`.

---

- 2026-06-25 — meta — Closed the write half of the loop: added `evolve` (write-back) and refined `lint` to PR-based HITL in `AGENTS.md`; created this log; set up `compile-daily` + `lint-weekly` cloud routines. — interactive
