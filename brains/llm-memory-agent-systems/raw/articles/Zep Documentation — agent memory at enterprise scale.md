---
title: "Zep Documentation — agent memory at enterprise scale"
source: "https://help.getzep.com/graphiti/getting-started/overview"
author:
published:
created: 2026-06-24
description: "Graphiti builds temporal knowledge graphs — Context Graphs — for AI agents, fusing semantic, full-text, and graph search over evolving entities, facts, and relationships."
tags:
  - "clippings"
---
What is a Context Graph?

Graphiti helps you create and query Context Graphs that evolve over time. A Context Graph is a temporal knowledge graph — a graph of entities, relationships, and facts, such as *“Kendra loves Adidas shoes.”* Each fact is a *“triplet”* represented by two entities, or nodes (*”Kendra”, “Adidas shoes”*), and their relationship, or edge (*”loves”*).

Knowledge Graphs have been explored extensively for information retrieval. What makes Graphiti unique is its ability to autonomously build a Context Graph while handling changing relationships and maintaining historical context.

![graphiti intro slides](https://files.buildwithfern.com/zep.docs.buildwithfern.com/2026-06-19T15:17:32.049Z/images/graphiti-graph-intro.gif)

graphiti intro slides

Graphiti builds dynamic, temporally-aware knowledge graphs — Context Graphs — that represent complex, evolving relationships between entities over time. It ingests both unstructured and structured data, and the resulting graph may be queried using a fusion of time, full-text, semantic, and graph algorithm approaches.

With Graphiti, you can build LLM applications such as:

- Assistants that learn from user interactions, fusing personal knowledge with dynamic data from business systems like CRMs and billing platforms.
- Agents that autonomously execute complex tasks, reasoning with state changes from multiple dynamic sources.

Graphiti supports a wide range of applications in sales, customer service, health, finance, and more, enabling long-term recall and state-based reasoning for both assistants and agents.

## Graphiti and Zep

Graphiti is the open-source temporal knowledge graph framework. Use it to build and query a single Context Graph per subject locally — entity and edge extraction, the bi-temporal model, fact invalidation, and hybrid retrieval.

[Zep](https://www.getzep.com/) is agent memory at enterprise scale, built on Graphiti: a governed Context Lake of millions of Context Graphs served in milliseconds on top of Zep’s proprietary Context Graph Engine. Use Zep when you need agent memory at scale — managed extraction, retrieval, storage, and governance at sub-200ms latency, with SOC 2, HIPAA, and BYOC.

## Why Graphiti?

We were intrigued by Microsoft’s GraphRAG, which expanded on RAG text chunking by using a graph to better model a document corpus and making this representation available via semantic and graph search techniques. However, GraphRAG did not address our core problem: It’s primarily designed for static documents and doesn’t inherently handle temporal aspects of data.

Graphiti is designed from the ground up to handle constantly changing information, hybrid semantic and graph search, and scale:

- **Temporal Awareness:** Tracks changes in facts and relationships over time, enabling point-in-time queries. Graph edges include temporal metadata to record relationship lifecycles.
- **Episodic Processing:** Ingests data as discrete episodes, maintaining data provenance and allowing incremental entity and relationship extraction.
- **Custom Entity Types:** Supports defining domain-specific entity types, enabling more precise knowledge representation for specialized applications.
- **Hybrid Search:** Combines vector similarity, BM25 full-text, and graph traversal into a single ranked answer, with no LLM-in-the-loop reranking. Results can be reranked by distance from a central node e.g. “Kendra”.
- **Pluggable Backends:** Runs on Neo4j, FalkorDB, or Amazon Neptune, with LLM and embedding providers including OpenAI, Azure OpenAI, Gemini, and Anthropic.
- **Scalable:** Designed for processing large datasets, with parallelization of LLM calls for bulk processing while preserving the chronology of events.
- **Supports Varied Sources:** Can ingest both unstructured text and structured JSON data.

**Performance:** On the LoCoMo benchmark, Graphiti-based retrieval reaches 94.7% accuracy at 155ms retrieval latency. On LongMemEval, it reaches 90.2% accuracy at 162ms. See the [LoCoMo](https://arxiv.org/abs/2402.17753) and [LongMemEval](https://arxiv.org/abs/2410.10813) papers.

| Aspect | GraphRAG | Graphiti |
| --- | --- | --- |
| **Primary Use** | Static document summarization | Dynamic data management |
| **Data Handling** | Batch-oriented processing | Continuous, incremental updates |
| **Knowledge Structure** | Entity clusters & community summaries | Episodic data, semantic entities, communities |
| **Retrieval Method** | Sequential LLM summarization | Hybrid semantic, keyword, and graph-based search |
| **Adaptability** | Low | High |
| **Temporal Handling** | Basic timestamp tracking | Explicit bi-temporal tracking |
| **Contradiction Handling** | LLM-driven summarization judgments | Temporal edge invalidation |
| **Query Latency** | Seconds to tens of seconds | Sub-200ms typical retrieval latency |
| **Custom Entity Types** | No | Yes, customizable |
| **Scalability** | Moderate | High, optimized for large datasets |

Graphiti is specifically designed to address the challenges of dynamic and frequently updated datasets, making it particularly suitable for applications requiring real-time interaction and precise historical queries.

![graphiti demo slides](https://files.buildwithfern.com/zep.docs.buildwithfern.com/2026-06-19T15:17:32.049Z/images/graphiti-intro-slides-stock-2.gif)

graphiti demo slides