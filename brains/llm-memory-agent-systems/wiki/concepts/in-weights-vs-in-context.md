# in-weights-vs-in-context

**One-liner:** Whether an agent's knowledge lives **baked into model parameters** (in-weights, via
pre-training / fine-tuning) or is **supplied at inference from an external store** (in-context, via
retrieval / RAG) — a foundational choice about *where* memory lives.

## What it is
Two loci for knowledge:
- **In-weights (parametric):** the model "memorizes" facts in its parameters during training and
  recalls them from a natural-language query with **no external context**. Roberts, Raffel &
  Shazeer (2020) operationalized this as **closed-book question answering** — fine-tuning T5 to
  answer open-domain questions without any retrieved documents (the "closed-book exam" metaphor). For
  *where/how* this knowledge actually lives in the weights, see [[parametric-knowledge]]; for
  changing it after training, see [[model-editing]].
- **In-context (non-parametric):** the system retrieves relevant text from an external source and
  places it in the prompt at inference ("open-book"). This is the retrieval side of
  [[context-vs-retrieval]] and the basis of vector RAG / [[hybrid-retrieval]].

## Why it matters for agent memory
The locus of knowledge determines the properties an agent memory system lives or dies by:
- **Updateability:** in-context facts change by editing a document; in-weights facts require
  re-training. Roberts et al. note the max-likelihood objective gives *no guarantee* a model learns
  (or can be made to forget) a specific fact — you can't cleanly add/remove parametric knowledge.
- **Traceability / citations:** open-book systems can indicate *what* they accessed (interpretable);
  the closed-book model "distributes knowledge in an inexplicable way and hallucinates realistic-
  looking answers when it is unsure" — no sources. This is precisely why the systems tracked in this
  brain favor cited retrieval.
- **Cost:** their results were competitive **only at ~11B parameters**, "prohibitively expensive in
  resource-constrained settings."
- **Staleness & reasoning:** the tasks mainly measured "trivia"-style recall, not reasoning; and
  parametric knowledge is frozen at training time. See [[temporal-knowledge-and-decay]].

## Variants / approaches
- **Pure in-weights:** closed-book QA (this paper). Knowledge from unsupervised pre-training on
  unstructured text (T5 on C4), recalled by fine-tuned generation.
- **Boosting parametric recall:** **salient span masking** (SSM, Guu et al. 2020) — pre-training that
  masks named entities/dates — gave a substantial lift; T5.1.1-XXL+SSM reached NQ 35.2 / WQ 42.8 /
  TriviaQA 61.6 (test), beating or matching open-domain *retrieval* baselines on WebQuestions and
  TriviaQA. (Exact-match underrates it: hand-inspection put true NQ accuracy nearer ~57.8.) A
  deeper finding: knowledge must be **augmented during pretraining** to be extractable at all — see
  [[parametric-knowledge]] (Physics of LMs 3.1).
- **Editing in-weights facts:** [[model-editing]] (ROME, KnowledgeEditor) updates a single fact
  without retraining — the most direct attempt to close the updateability gap below.
- **Pure in-context:** RAG / retrieval ([[mem0]], [[gbrain]]); see [[vector-rag]]. SOTA-ML surveys
  note retrieval turns parametric memory into "cache + compute" — fewer hallucinations, easier updates.
- **Token-space learning (a third stance):** [[letta]] rejects both weight updates *and* plain RAG —
  the agent rewrites its own context as durable token-space representations.

## Which systems use it
- In-context / retrieval camp: [[mem0]], [[gbrain]]. Hybrid token-space: [[letta]].
- In-weights exemplar: T5 closed-book QA (this paper) — the parametric baseline the others react to.

## Open questions
- **When is it worth "baking in" knowledge vs. retrieving it?** (Also in `_meta/open-questions.md`.)
  This paper (2020) argues in-weights is viable but costly and uninterpretable — how do those
  conclusions hold against 2026-scale models and modern retrieval?
- Can parametric knowledge be edited/removed reliably to fix the updateability gap? Partly answered:
  [[model-editing]] shows single-fact edits work; whether they scale to mass/sequential updates
  without degradation is still open.

## Sources
- Roberts, Raffel & Shazeer (2020), "How Much Knowledge Can You Pack Into the Parameters of a
  Language Model?" — arXiv [2002.08910](https://arxiv.org/abs/2002.08910) (EMNLP 2020): closed-book
  QA scales with model size, is competitive with retrieval systems, but is expensive, uninterpretable,
  and hard to update. *(The local `raw/papers/2002.08910.{md,pdf}` capture was removed from `raw/`;
  the claims above are retained against the arXiv source — see `_meta/log.md` 2026-06-29 lint.)*
