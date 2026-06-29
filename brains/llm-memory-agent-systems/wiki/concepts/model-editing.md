# model-editing

**One-liner:** Surgically updating or erasing a *specific* fact in a model's weights without full
retraining — the in-weights answer to stale or incorrect knowledge.

## What it is
Methods that change what a model "knows" by directly modifying parameters, targeting three
properties: **reliability** (the edit takes), **locality/specificity** (other facts stay intact),
and **generalization** (the edit holds across paraphrases). Building on [[parametric-knowledge]]
localization:
- **ROME — Rank-One Model Editing** (Meng et al. 2022): use causal tracing to localize a fact to a
  middle-layer feed-forward module, then apply a rank-one weight update to change it. Balances
  specificity and generalization on a counterfactual dataset; treats facts as "localized,
  directly-editable computations."
- **KnowledgeEditor** (De Cao et al. 2021): a trained **hyper-network** predicts weight updates at
  test time under constrained optimization, changing one fact while preserving others; edits
  generalize to paraphrases (especially when trained with paraphrased data). Works on BERT
  (fact-checking) and BART (QA); updates concentrate on surprisingly few components.
- **Knowledge-neuron manipulation** (Dai et al. 2021): update or erase a fact by amplifying/
  suppressing the identified knowledge neurons — no fine-tuning.

## Why it matters for agent memory
Editing is the in-weights counterpart to updating a document in a retrieval store. It directly
addresses the **updateability gap** that the closed-book results expose (see
[[in-weights-vs-in-context]] and the answered item in `_meta/open-questions.md`): if parametric
knowledge could be edited cheaply and reliably, "baking in" knowledge would carry far less staleness
penalty. It contrasts with how the in-context camp handles change in
[[temporal-knowledge-and-decay]] (edit/append documents, not weights).

## Variants / approaches
- **Locate-then-edit** (ROME; **MEMIT**, ICLR 2023, scales the closed-form update to thousands of
  edits across layers) — find the fact's locus, write a weight update.
- **Hyper-network / meta-learned editors** (KnowledgeEditor; **MEND**, ICLR 2022) — learn a model
  that emits the edit.
- **Memory-based editing** (**SERAC**, ICML 2022) — route edited queries to a separate counterfactual
  model; a *non-parametric* editor that doesn't touch base weights.
- **Neuron manipulation** (knowledge neurons) — directly tweak fact-bearing neurons.
- **Null-space editing** (**AlphaEdit**, ICLR 2025 Outstanding Paper) — project updates onto the null
  space of preserved-knowledge keys; the strongest sequential-editing approach as of the 2025–2026
  research map (reportedly retains ~98% of general ability after 3,000 edits), a plug-and-play boost
  to ROME/MEMIT.

## The wall at scale (2024–2026)
Per the 2025–2026 research map, knowledge editing **has hit a wall at lifelong scale**:
- **Sequential/lifelong editing causes gradual then catastrophic forgetting** and model collapse
  (Gupta et al., ACL Findings 2024) — rooted in the superposition limits noted in
  [[parametric-knowledge]].
- **RippleEdits** (Cohen et al., TACL 2024) shows edits fail to propagate to logically-entailed facts
  (accuracy on logical generalization as low as ~20%), and — strikingly — a **simple in-context
  editing baseline beat all parameter-editing methods**.
- A growing line of work argues the future is **in-context / retrieval-based updating, not parameter
  editing** (e.g. arXiv 2503.05212), connecting this concept back to [[vector-rag]] and
  [[temporal-knowledge-and-decay]].

## Which systems use it
- Research-level; **none** of the brain's tracked memory systems ([[mem0]], [[letta]], [[gbrain]])
  edit weights — they all chose in-context/retrieval. Model editing is the alternative path they
  implicitly reject.

## Open questions
- Do single-fact edits scale to **mass / sequential** updates without degrading the model? **Largely
  answered: no** — lifelong editing reliably collapses; AlphaEdit pushes the limit but doesn't remove
  it. Open: whether *any* parameter-editing scheme is safe at true lifelong scale.
- When is editing weights ever preferable to just updating a retrieval corpus? Evaluate on
  RippleEdits/KnowEdit (not rewrite success); for durability/portability prefer in-context updating —
  see [[vector-rag]] and [[portable-memory]].

## Sources
- `raw/papers/Locating and Editing Factual Associations in GPT.md` (arXiv 2202.05262, Meng et al.
  2022) — causal tracing + ROME rank-one editing.
- `raw/papers/Editing Factual Knowledge in Language Models.md` (arXiv 2104.08164, De Cao et al.
  2021) — KnowledgeEditor hyper-network.
- `raw/papers/Knowledge Neurons in Pretrained Transformers.md` (arXiv 2104.08696, Dai et al. 2021)
  — editing/erasing facts via knowledge neurons.
- `raw/articles/memory/LLM Memory and Knowledge: A 2025–2026 Research Map Across Four Threads.md`
  — Thread 3: MEND/SERAC/MEMIT lineage, catastrophic forgetting at scale, AlphaEdit, RippleEdits
  (in-context editing beats parameter editing).
