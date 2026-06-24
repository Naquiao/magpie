# parametric-knowledge

**One-liner:** How factual knowledge is stored in and extracted from a transformer's weights — where
it lives (largely feed-forward layers), how it's encoded, and why *memorizing* text doesn't
guarantee the knowledge is *extractable*.

## What it is
The mechanistic substrate of the in-weights side of [[in-weights-vs-in-context]]. Several lines of
work locate and characterize parametric knowledge:
- **FFN as key-value memories** (Geva et al. 2021): feed-forward layers — two-thirds of a model's
  parameters — act as key-value memories. Each *key* correlates with textual patterns in training
  data; each *value* induces a distribution over the output vocabulary. Lower layers capture shallow
  patterns, upper layers more semantic ones; outputs are compositions refined through the residual
  stream.
- **Knowledge neurons** (Dai et al. 2021): specific neurons in pretrained transformers express
  particular relational facts, identifiable via a knowledge-attribution method over cloze tasks;
  neuron activation correlates with whether a fact is expressed.
- **Causal localization** (Meng et al. 2022, ROME): causal tracing shows factual associations are
  mediated by **middle-layer feed-forward modules** at subject-token positions.

## Why it matters for agent memory
This explains the properties that pushed agent-memory systems toward retrieval: parametric knowledge
is distributed and opaque (hard to cite), but also localizable — which is what makes [[model-editing]]
possible. Crucially, **memorization ≠ extraction**: Allen-Zhu & Li ("Physics of Language Models 3.1",
2023) show on a controlled biography dataset that a model can reproduce training text verbatim yet
score **~0% on QA** about it, *regardless of model size or fine-tuning*, unless the pretraining data
was **knowledge-augmented** (paraphrasing, sentence permutation, multiple rewrites). Augmentation
makes the model encode attributes (nearly linearly) on the **entity-name tokens**, which is what
enables later extraction; even adding diverse "celebrity" data lifts extraction for non-augmented
"minority" entities. Encoder/MLM models (BERT) extract worse than autoregressive ones.

## How much, and how localized (2023–2026 update)
- **Capacity law:** Allen-Zhu & Li's "Physics of LMs 3.3" (ICLR 2025) is the field's quantitative
  anchor — LMs store **~2 bits of knowledge per parameter** (even quantized to int8), so a 7B model
  holds ~14B bits, more than English Wikipedia + textbooks combined.
- **The localization critique (central debate):** the clean "locate-then-edit" picture is
  destabilized. Hase et al. ("Does Localization Inform Editing?", NeurIPS 2023) found edit success is
  **essentially uncorrelated** with where causal tracing localizes a fact (ρ ≈ −0.13 at one GPT-J
  layer) — *which* layer you edit predicts success better than where the fact "is." Superposition
  work (arXiv 2408.07413) shows facts are stored *nearly* (not perfectly) orthogonally, and Yao et
  al.'s "Knowledge Circuits" (NeurIPS 2024) recast knowledge as sparse subgraphs spanning MLPs +
  attention, not isolated weights. See the consequences for [[model-editing]].

## Variants / approaches (localization methods)
- Causal tracing / causal mediation (ROME).
- Knowledge-attribution / integrated-gradients over neurons (knowledge neurons).
- Linear probing of hidden states (Physics 3.1's P-/Q-probing); linear-representation hypothesis
  (Park et al., ICML 2024) and its challenges (irreducible multi-dimensional features).

## Which systems use it
- This concerns base LMs, not the brain's retrieval systems. It underpins [[letta]]'s argument for
  *token-space* learning over weight updates, and it is the precondition for [[model-editing]].

## Open questions
- How localized vs. distributed is a given fact, really? Largely *not* cleanly localizable: edit
  success ≠ tracing location (Hase 2023), and superposition/knowledge-circuits suggest distributed,
  entangled storage. Reconciling the ~2 bits/param law with distributed circuits is open.
- Whether interpretability (SAEs, causal tracing) recovers *verifiable, behavior-causing* mechanisms
  is itself now contested (Sharkey et al. 2025 open-problems survey).
- Does the "augmentation enables extraction" result transfer to web-scale pretraining as cleanly as
  it does on synthetic biographies?

## Sources
- `raw/articles/memory/Physics of Language Models Part 3.1, Knowledge Storage and Extraction.md`
  — memorization vs. extraction; knowledge augmentation; entity-name encoding (probing).
- `raw/papers/Transformer Feed-Forward Layers Are Key-Value Memories.md` (arXiv 2012.14913, Geva et
  al. 2021) — FFN layers as key-value memories.
- `raw/papers/Knowledge Neurons in Pretrained Transformers.md` (arXiv 2104.08696, Dai et al. 2021)
  — knowledge neurons and attribution.
- `raw/papers/Locating and Editing Factual Associations in GPT.md` (arXiv 2202.05262, Meng et al.
  2022) — causal localization to mid-layer FFN.
- `raw/articles/memory/LLM Memory and Knowledge: A 2025–2026 Research Map Across Four Threads.md`
  — Thread 1: the ~2 bits/param capacity law, Hase's localization critique, superposition, knowledge
  circuits, linear-representation hypothesis.
