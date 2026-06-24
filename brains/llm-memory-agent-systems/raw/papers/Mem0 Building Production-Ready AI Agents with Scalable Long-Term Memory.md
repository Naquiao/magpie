---
title: "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory"
source: "https://arxiv.org/html/2504.19413v1"
author:
published:
created: 2026-06-24
description:
tags:
  - "clippings"
---
Prateek Chhikara Dev Khant Saket Aryan Taranjeet Singh and Deshraj Yadav  
[research@mem0.ai](mailto:research@mem0.ai)

###### Abstract

Large Language Models (LLMs) have demonstrated remarkable prowess in generating contextually coherent responses, yet their fixed context windows pose fundamental challenges for maintaining consistency over prolonged multi-session dialogues. We introduce Mem0, a scalable memory-centric architecture that addresses this issue by dynamically extracting, consolidating, and retrieving salient information from ongoing conversations. Building on this foundation, we further propose an enhanced variant that leverages graph-based memory representations to capture complex relational structures among conversational elements. Through comprehensive evaluations on the LOCOMO benchmark, we systematically compare our approaches against six baseline categories: (i) established memory-augmented systems, (ii) retrieval-augmented generation (RAG) with varying chunk sizes and $k$ -values, (iii) a full-context approach that processes the entire conversation history, (iv) an open-source memory solution, (v) a proprietary model system, and (vi) a dedicated memory management platform. Empirical results demonstrate that our methods consistently outperform all existing memory systems across four question categories: single-hop, temporal, multi-hop, and open-domain. Notably, Mem0 achieves 26% relative improvements in the LLM-as-a-Judge metric over OpenAI, while Mem0 with graph memory achieves around 2% higher overall score than the base Mem0 configuration. Beyond accuracy gains, we also markedly reduce computational overhead compared to the full-context approach. In particular, Mem0 attains a 91% lower p95 latency and saves more than 90% token cost, thereby offering a compelling balance between advanced reasoning capabilities and practical deployment constraints. Our findings highlight the critical role of structured, persistent memory mechanisms for long-term conversational coherence, paving the way for more reliable and efficient LLM-driven AI agents.

Code can be found at: [https://mem0.ai/research](https://mem0.ai/research)

## 1 Introduction

Human memory is a *foundation of intelligence* —it shapes our identity, guides decision-making, and enables us to learn, adapt, and form meaningful relationships [^5]. Among its many roles, memory is essential for communication: we recall past interactions, infer preferences, and construct evolving mental models of those we engage with [^2]. This ability to retain and retrieve information over extended periods enables coherent, contextually rich exchanges that span days, weeks, or even months. AI agents, powered by large language models (LLMs), have made remarkable progress in generating fluent, contextually appropriate responses [^26] [^29]. However, these systems are fundamentally limited by their reliance on fixed context windows, which severely restrict their ability to maintain coherence over extended interactions [^3] [^13]. This limitation stems from LLMs’ lack of persistent memory mechanisms that can extend beyond their finite context windows. While humans naturally accumulate and organize experiences over time, forming a continuous narrative of interactions, AI systems cannot inherently persist information across separate sessions or after context overflow. The absence of persistent memory creates a fundamental disconnect in human-AI interaction. Without memory, AI agents forget user preferences, repeat questions, and contradict previously established facts. Consider a simple example illustrated in Figure 1, where a user mentions being vegetarian and avoiding dairy products in an initial conversation. In a subsequent session, when the user asks about dinner recommendations, a system without persistent memory might suggest chicken, completely contradicting the established dietary preferences. In contrast, a system with persistent memory would maintain this critical user information across sessions and suggest appropriate vegetarian, dairy-free options. This common scenario highlights how memory failures can fundamentally undermine user experience and trust.

Beyond conversational settings, memory mechanisms have been shown to dramatically enhance agent performance in interactive environments [^15] [^20]. Agents equipped with memory of past experiences can better anticipate user needs, learn from previous mistakes, and generalize knowledge across tasks [^4]. Research demonstrates that memory-augmented agents improve decision-making by leveraging causal relationships between actions and outcomes, leading to more effective adaptation in dynamic scenarios [^18]. Hierarchical memory architectures [^17] [^19] and agentic memory systems capable of autonomous evolution [^25] have further shown that memory enables more coherent, long-term reasoning across multiple dialogue sessions.

![Refer to caption](https://arxiv.org/html/2504.19413v1/extracted/6393986/figures/main_figure.png)

Figure 1: Illustration of memory importance in AI agents. Left: Without persistent memory, the system forgets critical user information (vegetarian, dairy-free preferences) between sessions, resulting in inappropriate recommendations. Right: With effective memory, the system maintains these dietary preferences across interactions, enabling contextually appropriate suggestions that align with previously established constraints.

Unlike humans, who dynamically integrate new information and revise outdated beliefs, LLMs effectively “reset" once information falls outside their context window [^27] [^24]. Even as models like OpenAI’s GPT-4 (128K tokens) [^10], o1 (200K context) [^11], Anthropic’s Claude 3.7 Sonnet (200K tokens) [^1], and Google’s Gemini (at least 10M tokens) [^23] push the boundaries of context length, these improvements merely delay rather than solve the fundamental limitation. In practical applications, even these extended context windows prove insufficient for two critical reasons. First, as meaningful human-AI relationships develop over weeks or months, conversation history inevitably exceeds even the most generous context limits. Second, and perhaps more importantly, real-world conversations rarely maintain thematic continuity. A user might mention dietary preferences (being vegetarian), then engage in hours of unrelated discussion about programming tasks, before returning to food-related queries about dinner options. In such scenarios, a full-context approach would need to reason through mountains of irrelevant information, with the critical dietary preferences potentially buried among thousands of tokens of coding discussions. Moreover, simply presenting longer contexts does not ensure effective retrieval or utilization of past information, as attention mechanisms degrade over distant tokens [^7] [^16]. This limitation is particularly problematic in high-stakes domains such as healthcare, education, and enterprise support, where maintaining continuity and trust is crucial [^8]. To address these challenges, AI agents must adopt memory systems that go beyond static context extension. A robust AI memory should selectively store important information, consolidate related concepts, and retrieve relevant details when needed— *mirroring human cognitive processes* [^9]. By integrating such mechanisms, we can develop AI agents that maintain consistent personas, track evolving user preferences, and build upon prior exchanges. This shift will transform AI from transient, forgetful responders into reliable, long-term collaborators, fundamentally redefining the future of conversational intelligence.

In this paper, we address a fundamental limitation in AI systems: their inability to maintain coherent reasoning across extended conversations across different sessions, which severely restricts meaningful long-term interactions with users. We introduce Mem0 (pronounced as *mem-zero*), a novel memory architecture that dynamically captures, organizes, and retrieves salient information from ongoing conversations. Building on this foundation, we develop $\texttt{Mem0}^{\tiny g}$, which enhances the base architecture with graph-based memory representations to better model complex relationships between conversational elements. Our experimental results on the LOCOMO benchmark demonstrate that our approaches consistently outperform existing memory systems—including memory-augmented architectures, retrieval-augmented generation (RAG) methods, and both open-source and proprietary solutions—across diverse question types, while simultaneously requiring significantly lower computational resources. Latency measurements further reveal that Mem0 operates with 91% lower response times than full-context approaches, striking an optimal balance between sophisticated reasoning capabilities and practical deployment constraints. These contributions represent a meaningful step toward AI systems that can maintain coherent, context-aware conversations over extended durations—mirroring human communication patterns and opening new possibilities for applications in personal tutoring, healthcare, and personalized assistance.

## 2 Proposed Methods

We introduce two memory architectures for AI agents. (1) Mem0 implements a novel paradigm that extracts, evaluates, and manages salient information from conversations through dedicated modules for memory extraction and updation. The system processes a pair of messages between either two user participants or a user and an assistant. (2) $\texttt{Mem0}^{\tiny g}$ extends this foundation by incorporating graph-based memory representations, where memories are stored as directed labeled graphs with entities as nodes and relationships as edges. This structure enables a deeper understanding of the connections between entities. By explicitly modeling both entities and their relationships, $\texttt{Mem0}^{\tiny g}$ supports more advanced reasoning across interconnected facts, especially for queries that require navigating complex relational paths across multiple memories.

### 2.1 Mem0

Our architecture follows an incremental processing paradigm, enabling it to operate seamlessly within ongoing conversations. As illustrated in Figure 2, the complete pipeline architecture consists of two phases: extraction and update.

![Refer to caption](https://arxiv.org/html/2504.19413v1/extracted/6393986/figures/mem0_pipeline.png)

Figure 2: Architectural overview of the Mem0 system showing extraction and update phase. The extraction phase processes messages and historical context to create new memories. The update phase evaluates these extracted memories against similar existing ones, applying appropriate operations through a Tool Call mechanism. The database serves as the central repository, providing context for processing and storing updated memories.

The extraction phase initiates upon ingestion of a new message pair $(m_{t-1},m_{t})$, where $m_{t}$ represents the current message and $m_{t-1}$ the preceding one. This pair typically consists of a user message and an assistant response, capturing a complete interaction unit. To establish appropriate context for memory extraction, the system employs two complementary sources: (1) a conversation summary $S$ retrieved from the database that encapsulates the semantic content of the entire conversation history, and (2) a sequence of recent messages $\{m_{t-m},m_{t-m+1},...,m_{t-2}\}$ from the conversation history, where $m$ is a hyperparameter controlling the recency window. To support context-aware memory extraction, we implement an asynchronous summary generation module that periodically refreshes the conversation summary. This component operates independently of the main processing pipeline, ensuring that memory extraction consistently benefits from up-to-date contextual information without introducing processing delays. While $S$ provides global thematic understanding across the entire conversation, the recent message sequence offers granular temporal context that may contain relevant details not consolidated in the summary. This dual contextual information, combined with the new message pair, forms a comprehensive prompt $P=(S,\{m_{t-m},...,m_{t-2}\},m_{t-1},m_{t})$ for an extraction function $\phi$ implemented via an LLM. The function $\phi(P)$ then extracts a set of salient memories $\Omega=\{\omega_{1},\omega_{2},...,\omega_{n}\}$ specifically from the new exchange while maintaining awareness of the conversation’s broader context, resulting in candidate facts for potential inclusion in the knowledge base.

Following extraction, the update phase evaluates each candidate fact against existing memories to maintain consistency and avoid redundancy. This phase determines the appropriate memory management operation for each extracted fact $\omega_{i}\in\Omega$. Algorithm 1, mentioned in Appendix B, illustrates this process. For each fact, the system first retrieves the top $s$ semantically similar memories using vector embeddings from the database. These retrieved memories, along with the candidate fact, are then presented to the LLM through a function-calling interface we refer to as a ‘tool call.’ The LLM itself determines which of four distinct operations to execute: ADD for creation of new memories when no semantically equivalent memory exists; UPDATE for augmentation of existing memories with complementary information; DELETE for removal of memories contradicted by new information; and NOOP when the candidate fact requires no modification to the knowledge base. Rather than using a separate classifier, we leverage the LLM’s reasoning capabilities to directly select the appropriate operation based on the semantic relationship between the candidate fact and existing memories. Following this determination, the system executes the provided operations, thereby maintaining knowledge base coherence and temporal consistency.

In our experimental evaluation, we configured the system with ‘ $m$ ’ = 10 previous messages for contextual reference and ‘ $s$ ’ = 10 similar memories for comparative analysis. All language model operations utilized GPT-4o-mini as the inference engine. The vector database employs dense embeddings to facilitate efficient similarity search during the update phase.

### 2.2 Mem0gsuperscriptMem0𝑔\\texttt{Mem0}^{\\tiny g}Mem0 start\_POSTSUPERSCRIPT italic\_g end\_POSTSUPERSCRIPT

The $\texttt{Mem0}^{\tiny g}$ pipeline, illustrated in Figure 3, implements a graph-based memory approach that effectively captures, stores, and retrieves contextual information from natural language interactions [^28]. In this framework, memories are represented as a directed labeled graph $G=(V,E,L)$, where:

- Nodes $V$ represent entities (e.g., Alice, San\_Francisco)
- Edges $E$ represent relationships between entities (e.g., lives\_in)
- Labels $L$ assign semantic types to nodes (e.g., Alice - Person, San\_Francisco - City)

Each entity node $v\in V$ contains three components: (1) an entity type classification that categorizes the entity (e.g., Person, Location, Event), (2) an embedding vector $e_{v}$ that captures the entity’s semantic meaning, and (3) metadata including a creation timestamp $t_{v}$. Relationships in our system are structured as triplets in the form $(v_{s},r,v_{d})$, where $v_{s}$ and $v_{d}$ are source and destination entity nodes, respectively, and $r$ is the labeled edge connecting them.

![Refer to caption](https://arxiv.org/html/2504.19413v1/extracted/6393986/figures/mem0p_pipeline.png)

Figure 3: Graph-based memory architecture of Mem0 g superscript 𝑔 \\texttt{Mem0}^{\\tiny g} Mem0 start\_POSTSUPERSCRIPT italic\_g end\_POSTSUPERSCRIPT illustrating entity extraction and update phase. The extraction phase uses LLMs to convert conversation messages into entities and relation triplets. The update phase employs conflict detection and resolution mechanisms when integrating new information into the existing knowledge graph.

The extraction process employs a two-stage pipeline leveraging LLMs to transform unstructured text into structured graph representations. First, an entity extractor module processes the input text to identify a set of entities along with their corresponding types. In our framework, entities represent the key information elements in conversations—including people, locations, objects, concepts, events, and attributes that merit representation in the memory graph. The entity extractor identifies these diverse information units by analyzing the semantic importance, uniqueness, and persistence of elements in the conversation. For instance, in a conversation about travel plans, entities might include destinations (cities, countries), transportation modes, dates, activities, and participant preferences—essentially any discrete information that could be relevant for future reference or reasoning.

Next, a relationship generator component derives meaningful connections between these entities, establishing a set of relationship triplets that capture the semantic structure of the information. This LLM-based module analyzes the extracted entities and their context within the conversation to identify semantically significant connections. It works by examining linguistic patterns, contextual cues, and domain knowledge to determine how entities relate to one another. For each potential entity pair, the generator evaluates whether a meaningful relationship exists and, if so, classifies this relationship with an appropriate label (e.g., ‘lives\_in’, ‘prefers’, ‘owns’, ‘happened\_on’). The module employs prompt engineering techniques that guide the LLM to reason about both explicit statements and implicit information in the dialogue, resulting in relationship triplets that form the edges in our memory graph and enable complex reasoning across interconnected information. When integrating new information, $\texttt{Mem0}^{\tiny g}$ employs a sophisticated storage and update strategy. For each new relationship triple, we compute embeddings for both source and destination entities, then search for existing nodes with semantic similarity above a defined threshold ‘ $t$ ’. Based on node existence, the system may create both nodes, create only one node, or use existing nodes before establishing the relationship with appropriate metadata. To maintain a consistent knowledge graph, we implement a conflict detection mechanism that identifies potentially conflicting existing relationships when new information arrives. An LLM-based update resolver determines if certain relationships should be obsolete, marking them as invalid rather than physically removing them to enable temporal reasoning.

The memory retrieval functionality in $\texttt{Mem0}^{\tiny g}$ implements a dual-approach strategy for optimal information access. The entity-centric method first identifies key entities within a query, then leverages semantic similarity to locate corresponding nodes in the knowledge graph. It systematically explores both incoming and outgoing relationships from these anchor nodes, constructing a comprehensive subgraph that captures relevant contextual information. Complementing this, the semantic triplet approach takes a more holistic view by encoding the entire query as a dense embedding vector. This query representation is then matched against textual encodings of each relationship triplet in the knowledge graph. The system calculates fine-grained similarity scores between the query and all available triplets, returning only those that exceed a configurable relevance threshold, ranked in order of decreasing similarity. This dual retrieval mechanism enables $\texttt{Mem0}^{\tiny g}$ to handle both targeted entity-focused questions and broader conceptual queries with equal effectiveness.

From an implementation perspective, the system utilizes Neo4j <sup>1</sup> as the underlying graph database. LLM-based extractors and update module leverage GPT-4o-mini with function calling capabilities, allowing for structured extraction of information from unstructured text. By combining graph-based representations with semantic embeddings and LLM-based information extraction, $\texttt{Mem0}^{\tiny g}$ achieves both the structural richness needed for complex reasoning and the semantic flexibility required for natural language understanding.

## 3 Experimental Setup

### 3.1 Dataset

The LOCOMO [^14] dataset is designed to evaluate long-term conversational memory in dialogue systems. It comprises 10 extended conversations, each containing approximately 600 dialogues and 26000 tokens on average, distributed across multiple sessions. Each conversation captures two individuals discussing daily experiences or past events. Following these multi-session dialogues, each conversation is accompanied by 200 questions on an average with corresponding ground truth answers. These questions are categorized into multiple types: single-hop, multi-hop, temporal, and open-domain. The dataset originally included an adversarial question category, which was designed to test systems’ ability to recognize unanswerable questions. However, this category was excluded from our evaluation because ground truth answers were unavailable, and the expected behavior for this question type is that the agent should recognize them as unanswerable.

### 3.2 Evaluation Metrics

Our evaluation framework implements a comprehensive approach to assess long-term memory capabilities in dialogue systems, considering both response quality and operational efficiency. We categorize our metrics into two distinct groups that together provide a holistic understanding of system performance.

#### (1) Performance Metrics

Previous research in conversational AI [^6] [^22] [^21] has predominantly relied on lexical similarity metrics such as F1 Score (F <sub>1</sub>) and BLEU-1 (B <sub>1</sub>). However, these metrics exhibit significant limitations when evaluating factual accuracy in conversational contexts. Consider a scenario where the ground truth answer is ‘Alice was born in March’ and a system generates ‘Alice is born in July.’ Despite containing a critical factual error regarding the birth month, traditional metrics would assign relatively high scores due to lexical overlap in the remaining tokens (‘Alice,’ ‘born,’ etc.). This fundamental limitation can lead to misleading evaluations that fail to capture semantic correctness. To address these shortcomings, we use LLM-as-a-Judge (J) as a complementary evaluation metric. This approach leverages a separate, more capable LLM to assess response quality across multiple dimensions, including factual accuracy, relevance, completeness, and contextual appropriateness. The judge model analyzes the question, ground truth answer and the generated answer, providing a more nuanced evaluation that aligns better with human judgment. Due to the stochastic nature of J evaluations, we conducted 10 independent runs for each method on the entire dataset and report the mean scores along with $\pm$ 1 standard deviation. More details about the J is present in Appendix A.

#### (2) Deployment Metrics

Beyond response quality, practical deployment considerations are crucial for real-world applications of long-term memory in AI agents. We systematically track Token Consumption, using ‘cl100k\_base’ encoding from tiktoken, measuring the number of tokens extracted during retrieval that serve as context for answering queries. For our memory-based models, these tokens represent the memories retrieved from the knowledge base, while for RAG-based models, they correspond to the total number of tokens in the retrieved text chunks. This distinction is important as it directly affects operational costs and system efficiency—whether processing concise memory facts or larger raw text segments. We further monitor Latency, (i) *search latency*: which captures the total time required to search the memory (in memory-based solutions) or chunk (in RAG-based solutions) and (ii) *total latency:* time to generate appropriate responses, consisting of both retrieval time (accessing memories or chunks) and answer generation time using the LLM.

The relationship between these metrics reveals important trade-offs in system design. For instance, more sophisticated memory architectures might achieve higher factual accuracy but at the cost of increased token consumption and latency. Our multi-dimensional evaluation methodology enables researchers and practitioners to make informed decisions based on their specific requirements, whether prioritizing response quality for critical applications or computational efficiency for real-time deployment scenarios.

### 3.3 Baselines

To comprehensively evaluate our approach, we compare against six distinct categories of baselines that represent the current state of conversational memory systems. These diverse baselines collectively provide a robust framework for evaluating the effectiveness of different memory architectures across various dimensions, including factual accuracy, computational efficiency, and scalability to extended conversations. Where applicable, unless otherwise specified, we set the temperature to 0 to ensure the runs are as reproducible as possible.

#### Established LOCOMO Benchmarks

We first establish a comparative foundation by evaluating previously benchmarked methods on the LOCOMO dataset. These include five established approaches: LoCoMo [^14], ReadAgent [^12], MemoryBank [^30], MemGPT [^17], and A-Mem [^25]. These established benchmarks not only provide direct comparison points with published results but also represent the evolution of conversational memory architectures across different algorithmic paradigms. For our evaluation, we select the metrics where gpt-4o-mini was used for the evaluation. More details about these benchmarks are mentioned in Appendix C.

#### Open-Source Memory Solutions

Our second category consists of promising open-source memory architectures such as LangMem <sup>2</sup> (Hot Path) that have demonstrated effectiveness in related conversational tasks but have not yet been evaluated on the LOCOMO dataset. By adapting these systems to our evaluation framework, we broaden the comparative landscape and identify potential alternative approaches that may offer competitive performance. We initialized the LLM with gpt-4o-mini and used text-embedding-small-3 as the embedding model.

#### Retrieval-Augmented Generation (RAG)

As a baseline, we treat the entire conversation history as a document collection and apply a standard RAG pipeline. We first segment each conversation into fixed-length chunks (128, 256, 512, 1024, 2048, 4096, and 8192 tokens), where 8192 is the maximum chunk size supported by our embedding model. All chunks are embedded using OpenAI’s text-embedding-small-3 to ensure consistent vector quality across configurations. At query time, we retrieve the top $k$ chunks by semantic similarity and concatenate them as context for answer generation. Throughout our experiments we set $k$ $\in$ {1,2}: with $k$ =1 only the single most relevant chunk is used, and with $k$ =2 the two most relevant chunks (up to 16384 tokens) are concatenated. We avoid $k>2$ since the average conversation length (26000 tokens) would be fully covered, negating the benefits of selective retrieval. By varying chunk size and $k$, we systematically evaluate RAG performance on long-term conversational memory tasks.

#### Full-Context Processing

We adopt a straightforward approach by passing the entire conversation history within the context window of the LLM. This method leverages the model’s inherent ability to process sequential information without additional architectural components. While conceptually simple, this approach faces practical limitations as conversation length increases, eventually increasing token cost and latency. Nevertheless, it establishes an important reference point for understanding the value of more sophisticated memory mechanisms compared to direct processing of available context.

#### Proprietary Models

We evaluate OpenAI’s memory <sup>3</sup> feature available in their ChatGPT interface, specifically using gpt-4o-mini for consistency. We ingest entire LOCOMO conversations with a prompt (see Appendix A) into single chat sessions, prompting memory generation with timestamps, participant names, and conversation text. These generated memories are then used as complete context for answering questions about each conversation, intentionally granting the OpenAI approach privileged access to all memories rather than only question-relevant ones. This methodology accommodates the lack of external API access for selective memory retrieval in OpenAI’s system for benchmarking.

#### Memory Providers

We incorporate Zep [^18], a memory management platform designed for AI agents. Using their platform version, we conduct systematic evaluations across the LOCOMO dataset, maintaining temporal fidelity by preserving timestamp information alongside conversational content. This temporal anchoring ensures that time-sensitive queries can be addressed through appropriately contextualized memory retrieval, particularly important for evaluating questions that require chronological awareness. This baseline represents an important commercial implementation of memory management specifically engineered for AI agents.

Table 1: Performance comparison of memory-enabled systems across different question types in the LOCOMO dataset. Evaluation metrics include F1 score (F <sub>1</sub>), BLEU-1 (B <sub>1</sub>), and LLM-as-a-Judge score (J), with higher values indicating better performance. $\text{A-Mem}^{*}$ represents results from our re-run of A-Mem to generate LLM-as-a-Judge scores by setting temperature as 0. $\texttt{Mem0}^{\tiny g}$ indicates our proposed architecture enhanced with graph memory. Bold denotes the best performance for each metric across all methods. ($\uparrow$) represents higher score is better.

<table><tbody><tr><th rowspan="2">Method</th><td colspan="3">Single Hop</td><td colspan="3">Multi-Hop</td><td colspan="3">Open Domain</td><td colspan="3">Temporal</td></tr><tr><td>F <sub>1</sub> <math><semantics><mo>↑</mo> <ci>↑</ci> <annotation>\uparrow</annotation> <annotation>↑</annotation></semantics></math></td><td>B <sub>1</sub> <math><semantics><mo>↑</mo> <ci>↑</ci> <annotation>\uparrow</annotation> <annotation>↑</annotation></semantics></math></td><td>J <math><semantics><mo>↑</mo> <ci>↑</ci> <annotation>\uparrow</annotation> <annotation>↑</annotation></semantics></math></td><td>F <sub>1</sub> <math><semantics><mo>↑</mo> <ci>↑</ci> <annotation>\uparrow</annotation> <annotation>↑</annotation></semantics></math></td><td>B <sub>1</sub> <math><semantics><mo>↑</mo> <ci>↑</ci> <annotation>\uparrow</annotation> <annotation>↑</annotation></semantics></math></td><td>J <math><semantics><mo>↑</mo> <ci>↑</ci> <annotation>\uparrow</annotation> <annotation>↑</annotation></semantics></math></td><td>F <sub>1</sub> <math><semantics><mo>↑</mo> <ci>↑</ci> <annotation>\uparrow</annotation> <annotation>↑</annotation></semantics></math></td><td>B <sub>1</sub> <math><semantics><mo>↑</mo> <ci>↑</ci> <annotation>\uparrow</annotation> <annotation>↑</annotation></semantics></math></td><td>J <math><semantics><mo>↑</mo> <ci>↑</ci> <annotation>\uparrow</annotation> <annotation>↑</annotation></semantics></math></td><td>F <sub>1</sub> <math><semantics><mo>↑</mo> <ci>↑</ci> <annotation>\uparrow</annotation> <annotation>↑</annotation></semantics></math></td><td>B <sub>1</sub> <math><semantics><mo>↑</mo> <ci>↑</ci> <annotation>\uparrow</annotation> <annotation>↑</annotation></semantics></math></td><td>J <math><semantics><mo>↑</mo> <ci>↑</ci> <annotation>\uparrow</annotation> <annotation>↑</annotation></semantics></math></td></tr><tr><th>LoCoMo</th><td>25.02</td><td>19.75</td><td>–</td><td>12.04</td><td>11.16</td><td>–</td><td>40.36</td><td>29.05</td><td>–</td><td>18.41</td><td>14.77</td><td>–</td></tr><tr><th>ReadAgent</th><td>9.15</td><td>6.48</td><td>–</td><td>5.31</td><td>5.12</td><td>–</td><td>9.67</td><td>7.66</td><td>–</td><td>12.60</td><td>8.87</td><td>–</td></tr><tr><th>MemoryBank</th><td>5.00</td><td>4.77</td><td>–</td><td>5.56</td><td>5.94</td><td>–</td><td>6.61</td><td>5.16</td><td>–</td><td>9.68</td><td>6.99</td><td>–</td></tr><tr><th>MemGPT</th><td>26.65</td><td>17.72</td><td>–</td><td>9.15</td><td>7.44</td><td>–</td><td>41.04</td><td>34.34</td><td>–</td><td>25.52</td><td>19.44</td><td>–</td></tr><tr><th>A-Mem</th><td>27.02</td><td>20.09</td><td>–</td><td>12.14</td><td>12.00</td><td>–</td><td>44.65</td><td>37.06</td><td>–</td><td>45.85</td><td>36.67</td><td>–</td></tr><tr><th>A-Mem*</th><td>20.76</td><td>14.90</td><td>39.79 ± 0.38</td><td>9.22</td><td>8.81</td><td>18.85 ± 0.31</td><td>33.34</td><td>27.58</td><td>54.05 ± 0.22</td><td>35.40</td><td>31.08</td><td>49.91 ± 0.31</td></tr><tr><th>LangMem</th><td>35.51</td><td>26.86</td><td>62.23 ± 0.75</td><td>26.04</td><td>22.32</td><td>47.92 ± 0.47</td><td>40.91</td><td>33.63</td><td>71.12 ± 0.20</td><td>30.75</td><td>25.84</td><td>23.43 ± 0.39</td></tr><tr><th>Zep</th><td>35.74</td><td>23.30</td><td>61.70 ± 0.32</td><td>19.37</td><td>14.82</td><td>41.35 ± 0.48</td><td>49.56</td><td>38.92</td><td>76.60 ± 0.13</td><td>42.00</td><td>34.53</td><td>49.31 ± 0.50</td></tr><tr><th>OpenAI</th><td>34.30</td><td>23.72</td><td>63.79 ± 0.46</td><td>20.09</td><td>15.42</td><td>42.92 ± 0.63</td><td>39.31</td><td>31.16</td><td>62.29 ± 0.12</td><td>14.04</td><td>11.25</td><td>21.71 ± 0.20</td></tr><tr><th>Mem0</th><td>38.72</td><td>27.13</td><td>67.13 ± 0.65</td><td>28.64</td><td>21.58</td><td>51.15 ± 0.31</td><td>47.65</td><td>38.72</td><td>72.93 ± 0.11</td><td>48.93</td><td>40.51</td><td>55.51 ± 0.34</td></tr><tr><th><math><semantics><msup><mtext>Mem0</mtext> <mi>g</mi></msup> <apply><csymbol>superscript</csymbol> <ci><mtext>Mem0</mtext></ci> <ci>𝑔</ci></apply> <annotation>\texttt{Mem0}^{\tiny g}</annotation> <annotation>Mem0 start_POSTSUPERSCRIPT italic_g end_POSTSUPERSCRIPT</annotation></semantics></math></th><td>38.09</td><td>26.03</td><td>65.71 ± 0.45</td><td>24.32</td><td>18.82</td><td>47.19 ± 0.67</td><td>49.27</td><td>40.30</td><td>75.71 ± 0.21</td><td>51.55</td><td>40.28</td><td>58.13 ± 0.44</td></tr></tbody></table>

## 4 Evaluation Results, Analysis and Discussion.

### 4.1 Performance Comparison Across Memory-Enabled Systems

Table 1 reports F <sub>1</sub>, B <sub>1</sub> and J scores for our two architectures—Mem0 and $\texttt{Mem0}^{\tiny g}$ —against a suite of competitive baselines, as mentioned in Section 3, on single-hop, multi-hop, open-domain, and temporal questions. Overall, both of our models set new state-of-the-art marks in all the three evaluation metrics for most question types.

#### Single-Hop Question Performance

Single-hop queries involve locating a single factual span contained within one dialogue turn. Leveraging its dense memories in natural language text, Mem0 secures the strongest results:F <sub>1</sub> =38.72, B <sub>1</sub> =27.13, and J=67.13. Augmenting the natural language memories with graph memory ($\texttt{Mem0}^{\tiny g}$) yields marginal performance drop compared to Mem0, indicating that relational structure provides limited utility when the retrieval target occupies a single turn. Among the existing baselines, the full-context OpenAI run attains the next-best J score, reflecting the benefits of retaining the entire conversation in context, while LangMem and Zep both score around 8% relatively less against our models on J score. Previous LOCOMO benchmarks such as A-mem lag by more than 25 points in J, underscoring the necessity of fine-grained, structured memory indexing even for simple retrieval tasks.

#### Multi-Hop Question Performance

Multi-hop queries require synthesizing information dispersed across multiple conversation sessions, posing significant challenges in memory integration and retrieval. Mem0 clearly outperforms other methods with an F <sub>1</sub> score of 28.64 and a J score of 51.15, reflecting its capability to efficiently retrieve and integrate disparate information stored across sessions. Interestingly, the addition of graph memory in $\texttt{Mem0}^{\tiny g}$ does not provide performance gains here, indicating potential inefficiencies or redundancies in structured graph representations for complex integrative tasks compared to dense natural language memory alone. Baselines like LangMem show competitive performances, but their scores substantially trail those of Mem0, emphasizing the advantage of our refined memory indexing and retrieval mechanisms for complex query processing.

#### Open-Domain Performance

In open-domain settings, the baseline Zep achieves the highest F <sub>1</sub> (49.56) and J (76.60) scores, edging out our methods by a narrow margin. In particular, Zep’s J score of 76.60 surpasses $\texttt{Mem0}^{\tiny g}$ ’s 75.71 by just 0.89 percentage points and outperforms Mem0’s 72.93 by 3.67 points, highlighting a consistent, if slight, advantage in integrating conversational memory with external knowledge. $\texttt{Mem0}^{\tiny g}$ remains a strong runner-up, with a J of 75.71 reflecting high factual retrieval precision, while Mem0 follows with 72.93, demonstrating robust coherence. These results underscore that although structured relational memories (as in Mem0 and $\texttt{Mem0}^{\tiny g}$) substantially improve open-domain retrieval, Zep maintains a small but meaningful lead.

#### Temporal Reasoning Performance

Temporal reasoning tasks hinge on accurate modeling of event sequences, their relative ordering, and durations within conversational history. Our architectures demonstrate substantial improvements across all metrics, with $\texttt{Mem0}^{\tiny g}$ achieving the highest F <sub>1</sub> (51.55) and J (58.13), suggesting that structured relational representations in addition to natural language memories significantly aid in temporally grounded judgments. Notably, the base variant, Mem0, also provide a decent J score (55.51), suggesting that natural language alone can aid in temporally grounded judgments. Among baselines, OpenAI notably underperforms, with scores below 15%, primarily due to missing timestamps in most generated memories despite explicit prompting in the OpenAI ChatGPT to extract memories with timestamps. Other baselines such as A-Mem achieve respectable results, yet our models clearly advance the state-of-the-art, emphasizing the critical advantage of accurately leveraging both natural language contextualization and structured graph representations for temporal reasoning.

### 4.2 Cross-Category Analysis

The comprehensive evaluation across diverse question categories reveals that our proposed architectures, Mem0 and $\texttt{Mem0}^{\tiny g}$, consistently achieve superior performance compared to baseline systems. For single-hop queries, Mem0 demonstrates particularly strong performance, benefiting from its efficient dense natural language memory structure. Although graph-based representations in $\texttt{Mem0}^{\tiny g}$ slightly lag behind in lexical overlap metrics for these simpler queries, they significantly enhance semantic coherence, as demonstrated by competitive J scores. This indicates that graph structures are more beneficial in scenarios involving nuanced relational context rather than straightforward retrieval. For multi-hop questions, Mem0 exhibits clear advantages by effectively synthesizing dispersed information across multiple sessions, confirming that natural language memories provide sufficient representational richness for these integrative tasks. Surprisingly, the expected relational advantages of $\texttt{Mem0}^{\tiny g}$ do not translate into better outcomes here, suggesting potential overhead or redundancy when navigating more intricate graph structures in multi-step reasoning scenarios.

Table 2: Performance comparison of various baselines with proposed methods. Latency measurements show p50 (median) and p95 (95th percentile) values in seconds for both search time (time taken to fetch memories/chunks) and total time (time to generate the complete response). Overall LLM-as-a-Judge score ($\mathrm{J}$) represents the quality metric of the generated responses on the entire LOCOMO dataset.

<table><tbody><tr><td rowspan="3">Method</td><td colspan="2"></td><td colspan="4">Latency (seconds)</td><td rowspan="3">Overall <math><semantics><mi>J</mi> <ci>J</ci> <annotation>\mathrm{J}</annotation> <annotation>roman_J</annotation></semantics></math></td></tr><tr><td colspan="2"></td><td colspan="2">Search</td><td colspan="2">Total</td></tr><tr><td>K</td><td>chunk size /memory tokens</td><td>p50</td><td>p95</td><td>p50</td><td>p95</td></tr><tr><td rowspan="14">RAG</td><td rowspan="7">1</td><td>128</td><td>0.281</td><td>0.823</td><td>0.774</td><td>1.825</td><td>47.77 <math><semantics><mo>±</mo> <csymbol>plus-or-minus</csymbol> <annotation>\pm</annotation> <annotation>±</annotation></semantics></math> 0.23%</td></tr><tr><td>256</td><td>0.251</td><td>0.710</td><td>0.745</td><td>1.628</td><td>50.15 <math><semantics><mo>±</mo> <csymbol>plus-or-minus</csymbol> <annotation>\pm</annotation> <annotation>±</annotation></semantics></math> 0.16%</td></tr><tr><td>512</td><td>0.240</td><td>0.639</td><td>0.772</td><td>1.710</td><td>46.05 <math><semantics><mo>±</mo> <csymbol>plus-or-minus</csymbol> <annotation>\pm</annotation> <annotation>±</annotation></semantics></math> 0.14%</td></tr><tr><td>1024</td><td>0.240</td><td>0.723</td><td>0.821</td><td>1.957</td><td>40.74 <math><semantics><mo>±</mo> <csymbol>plus-or-minus</csymbol> <annotation>\pm</annotation> <annotation>±</annotation></semantics></math> 0.17%</td></tr><tr><td>2048</td><td>0.255</td><td>0.752</td><td>0.996</td><td>2.182</td><td>37.93 <math><semantics><mo>±</mo> <csymbol>plus-or-minus</csymbol> <annotation>\pm</annotation> <annotation>±</annotation></semantics></math> 0.12%</td></tr><tr><td>4096</td><td>0.254</td><td>0.719</td><td>1.093</td><td>2.711</td><td>36.84 <math><semantics><mo>±</mo> <csymbol>plus-or-minus</csymbol> <annotation>\pm</annotation> <annotation>±</annotation></semantics></math> 0.17%</td></tr><tr><td>8192</td><td>0.279</td><td>0.838</td><td>1.396</td><td>4.416</td><td>44.53 <math><semantics><mo>±</mo> <csymbol>plus-or-minus</csymbol> <annotation>\pm</annotation> <annotation>±</annotation></semantics></math> 0.13%</td></tr><tr><td rowspan="7">2</td><td>128</td><td>0.267</td><td>0.624</td><td>0.766</td><td>1.829</td><td>59.56 <math><semantics><mo>±</mo> <csymbol>plus-or-minus</csymbol> <annotation>\pm</annotation> <annotation>±</annotation></semantics></math> 0.19%</td></tr><tr><td>256</td><td>0.255</td><td>0.699</td><td>0.802</td><td>1.907</td><td>60.97 <math><semantics><mo>±</mo> <csymbol>plus-or-minus</csymbol> <annotation>\pm</annotation> <annotation>±</annotation></semantics></math> 0.20%</td></tr><tr><td>512</td><td>0.247</td><td>0.746</td><td>0.829</td><td>1.729</td><td>58.19 <math><semantics><mo>±</mo> <csymbol>plus-or-minus</csymbol> <annotation>\pm</annotation> <annotation>±</annotation></semantics></math> 0.18%</td></tr><tr><td>1024</td><td>0.238</td><td>0.702</td><td>0.860</td><td>1.850</td><td>50.68 <math><semantics><mo>±</mo> <csymbol>plus-or-minus</csymbol> <annotation>\pm</annotation> <annotation>±</annotation></semantics></math> 0.13%</td></tr><tr><td>2048</td><td>0.261</td><td>0.829</td><td>1.101</td><td>2.791</td><td>48.57 <math><semantics><mo>±</mo> <csymbol>plus-or-minus</csymbol> <annotation>\pm</annotation> <annotation>±</annotation></semantics></math> 0.22%</td></tr><tr><td>4096</td><td>0.266</td><td>0.944</td><td>1.451</td><td>4.822</td><td>51.79 <math><semantics><mo>±</mo> <csymbol>plus-or-minus</csymbol> <annotation>\pm</annotation> <annotation>±</annotation></semantics></math> 0.15%</td></tr><tr><td>8192</td><td>0.288</td><td>1.124</td><td>2.312</td><td>9.942</td><td>60.53 <math><semantics><mo>±</mo> <csymbol>plus-or-minus</csymbol> <annotation>\pm</annotation> <annotation>±</annotation></semantics></math> 0.16%</td></tr><tr><td>Full-context</td><td></td><td>26031</td><td>-</td><td>-</td><td>9.870</td><td>17.117</td><td>72.90 <math><semantics><mo>±</mo> <csymbol>plus-or-minus</csymbol> <annotation>\pm</annotation> <annotation>±</annotation></semantics></math> 0.19%</td></tr><tr><td>A-Mem</td><td></td><td>2520</td><td>0.668</td><td>1.485</td><td>1.410</td><td>4.374</td><td>48.38 <math><semantics><mo>±</mo> <csymbol>plus-or-minus</csymbol> <annotation>\pm</annotation> <annotation>±</annotation></semantics></math> 0.15%</td></tr><tr><td>LangMem</td><td></td><td>127</td><td>17.99</td><td>59.82</td><td>18.53</td><td>60.40</td><td>58.10 <math><semantics><mo>±</mo> <csymbol>plus-or-minus</csymbol> <annotation>\pm</annotation> <annotation>±</annotation></semantics></math> 0.21%</td></tr><tr><td>Zep</td><td></td><td>3911</td><td>0.513</td><td>0.778</td><td>1.292</td><td>2.926</td><td>65.99 <math><semantics><mo>±</mo> <csymbol>plus-or-minus</csymbol> <annotation>\pm</annotation> <annotation>±</annotation></semantics></math> 0.16%</td></tr><tr><td>OpenAI</td><td></td><td>4437</td><td>-</td><td>-</td><td>0.466</td><td>0.889</td><td>52.90 <math><semantics><mo>±</mo> <csymbol>plus-or-minus</csymbol> <annotation>\pm</annotation> <annotation>±</annotation></semantics></math> 0.14%</td></tr><tr><td>Mem0</td><td></td><td>1764</td><td>0.148</td><td>0.200</td><td>0.708</td><td>1.440</td><td>66.88 <math><semantics><mo>±</mo> <csymbol>plus-or-minus</csymbol> <annotation>\pm</annotation> <annotation>±</annotation></semantics></math> 0.15%</td></tr><tr><td><math><semantics><msup><mtext>Mem0</mtext> <mi>g</mi></msup> <apply><csymbol>superscript</csymbol> <ci><mtext>Mem0</mtext></ci> <ci>𝑔</ci></apply> <annotation>\texttt{Mem0}^{\tiny g}</annotation> <annotation>Mem0 start_POSTSUPERSCRIPT italic_g end_POSTSUPERSCRIPT</annotation></semantics></math></td><td></td><td>3616</td><td>0.476</td><td>0.657</td><td>1.091</td><td>2.590</td><td>68.44 <math><semantics><mo>±</mo> <csymbol>plus-or-minus</csymbol> <annotation>\pm</annotation> <annotation>±</annotation></semantics></math> 0.17%</td></tr></tbody></table>

In temporal reasoning, $\texttt{Mem0}^{\tiny g}$ substantially outperforms other methods, validating that structured relational graphs excel in capturing chronological relationships and event sequences. The presence of explicit relational context significantly enhances $\texttt{Mem0}^{\tiny g}$ ’s temporal coherence, outperforming Mem0’s dense memory storage and highlighting the importance of precise relational representations when tracking temporally sensitive information. Open-domain performance further reinforces the value of relational modeling. $\texttt{Mem0}^{\tiny g}$, benefiting from the relational clarity of graph-based memory, closely competes with the top-performing baseline (Zep). This competitive result underscores $\texttt{Mem0}^{\tiny g}$ ’s robustness in integrating external knowledge through relational clarity, suggesting an optimal synergy between structured memory and open-domain information synthesis.

Overall, our analysis indicates complementary strengths of Mem0 and $\texttt{Mem0}^{\tiny g}$ across various task demands: dense, natural-language-based memory offers significant efficiency for simpler queries, while explicit relational modeling becomes essential for tasks demanding nuanced temporal and contextual integration. These findings reinforce the importance of adaptable memory structures tailored to specific reasoning contexts in AI agent deployments.

![Refer to caption](https://arxiv.org/html/2504.19413v1/extracted/6393986/figures/latency_search.png)

(a) Comparison of search latency at p50 (median) and p95 (95th percentile) across different memory methods ( Mem0, g superscript 𝑔 \\texttt{Mem0}^{\\tiny g} Mem0 start\_POSTSUPERSCRIPT italic\_g end\_POSTSUPERSCRIPT, best RAG variant, Zep, LangMem, and A-Mem). The bar heights represent J scores (left axis), while the line plots show search latency in seconds (right axis scaled in log).

### 4.3 Performance Comparison of Mem0 and Mem0gsuperscriptMem0𝑔\\texttt{Mem0}^{\\tiny g}Mem0 start\_POSTSUPERSCRIPT italic\_g end\_POSTSUPERSCRIPT Against RAG Approaches and Full-Context Model

Comparisons in Table 2, focusing on the ‘Overall J’ column, reveal that both Mem0 and $\texttt{Mem0}^{\tiny g}$ consistently outperform all RAG configurations, which vary chunk sizes (128–8192 tokens) and retrieve either one ($k$ =1) or two ($k$ =2) chunks. Even the strongest RAG approach peaks at around 61% in the J metric, whereas Mem0 reaches 67%—about a 10% relative improvement—and $\texttt{Mem0}^{\tiny g}$ reaches over 68%, achieving around a 12% relative gain. These advances underscore the advantage of capturing only the most salient facts in memory, rather than retrieving large chunk of original text. By converting the conversation history into concise, structured representations, Mem0 and $\texttt{Mem0}^{\tiny g}$ mitigate noise and surface more precise cues to the LLM, leading to better answers as evaluated by an external LLM (J).

Despite these improvements, a full-context method that ingests a chunk of roughly 26,000 tokens still achieves the highest J score (approximately 73%). However, as shown in Figure 4(b), it also incurs a very high total p95 latency—around 17 seconds—since the model must read the entire conversation on every query. By contrast, Mem0 and $\texttt{Mem0}^{\tiny g}$ significantly reduce token usage and thus achieve lower p95 latencies of around 1.44 seconds (a 92% reduction) and 2.6 seconds (a 85% reduction), respectively over full-context approach. Although the full-context approach can provide a slight accuracy edge, the memory-based systems offer a more practical trade-off, maintaining near-competitive quality while imposing only a fraction of the token and latency cost. As conversation length increases, full-context approaches suffer from exponential growth in computational overhead (evident in Table 2 where total p95 latency increases significantly with larger $k$ values or chunk sizes). This increase in input chunks leads to longer response times and higher token consumption costs. In contrast, memory-focused approaches like Mem0 and $\texttt{Mem0}^{\tiny g}$ maintain consistent performance regardless of conversation length, making them substantially more viable for production-scale deployments where efficiency and responsiveness are critical.

### 4.4 Latency Analysis

Table 2 provides a comprehensive performance comparison of various retrieval and memory methodologies, presenting median (p50) and tail (p95) latencies for both the search phase and total response generation across the LOCOMO dataset. Our analysis reveals distinct performance patterns governed by architectural choices. Memory-centric architectures demonstrate different performance characteristics. A-Mem, despite its larger memory store, incurs substantial search overhead (p50: 0.668s), resulting in total median latencies of 1.410s. LangMem exhibits even higher search latencies (p50: 17.99s, p95: 59.82s), rendering it impractical for interactive applications. Zep achieves moderate performance (p50 total: 1.292s). The full-context baseline, which processes the entire conversation history without retrieval, fundamentally differs from retrieval-based approaches. By passing the entire conversation context (26000 tokens) directly to the LLM, it eliminates search overhead but incurs extreme total latencies (p50: 9.870s, p95: 17.117s). Similarly, the OpenAI implementation does not perform memory search, as it processes manually extracted memories from their playground. While this approach achieves impressive response generation times (p50: 0.466s, p95: 0.889s), it requires pre-extraction of relevant context, which is not reflected in the reported metrics.

Our proposed Mem0 approach achieves the lowest search latency among all methods (p50: 0.148s, p95: 0.200s) as illustrated in Figure 4(a). This efficiency stems from our selective memory retrieval mechanism and infra improvements that dynamically identifies and retrieves only the most salient information rather than fixed-size chunks. Consequently, Mem0 maintains the lowest total median latency (0.708s) with remarkably contained p95 values (1.440s), making it particularly suitable for latency-sensitive applications such as interactive AI agents. The graph-enhanced $\texttt{Mem0}^{\tiny g}$ variant introduces additional relational modeling capabilities at a moderate latency cost, with search times (0.476s) still outperforming all existing memory solutions and baselines. Despite this increase, $\texttt{Mem0}^{\tiny g}$ maintains competitive total latencies (p50: 1.091s, p95: 2.590s) while achieving the highest J score (68.44%) across all methods—trailing only the computationally prohibitive full-context approach. This performance profile demonstrates our methods’ ability to balance response quality and computational efficiency, offering a compelling solution for production AI agents where both factors are critical constraints.

### 4.5 Memory System Overhead: Token Analysis and Construction Time

We measure the average token budget required to materialise each system’s long-term memory store. Mem0 encodes complete dialogue turns in a natural language representation and therefore occupies only 7k tokens per conversation on an average. Where as $\texttt{Mem0}^{\tiny g}$ roughly doubles the footprint to 14k tokens, due to the introduction of graph memories which includes nodes and corresponding relationships. In stark contrast, Zep’s memory graph consumes in excess of 600k tokens. The inflation arises from Zep’s design choice to cache a full abstractive summary at every node while also storing facts on the connecting edges, leading to extensive redundancy across the graph. For perspective, supplying the *entire* raw conversation context to the language model—without any memory abstraction—amounts to roughly 26k tokens on average, 20 times less relative to Zep’s graph. Beyond token inefficiency, our experiments revealed significant operational bottlenecks with Zep. After adding memories to Zep’s system, we observed that immediate memory retrieval attempts often failed to answer our queries correctly. Interestingly, re-running identical searches after a delay of several hours yielded considerably better results. This latency suggests that Zep’s graph construction involves multiple asynchronous LLM calls and extensive background processing, making the memory system impractical for real-time applications. In contrast, Mem0 graph construction completes in under a minute even in worst-case scenarios, allowing users to immediately leverage newly added memories for query responses.

These findings highlight that Zep not only replicates identical knowledge fragments across multiple nodes, but also introduces significant operational delays. Our architectures—Mem0 and $\texttt{Mem0}^{\tiny g}$ —preserve the same information at a fraction of the token cost and with substantially faster memory availability, offering a more memory-efficient and operationally responsive representation.

## 5 Conclusion and Future Work

We have introduced Mem0 and $\texttt{Mem0}^{\tiny g}$, two complementary memory architectures that overcome the intrinsic limitations of fixed context windows in LLMs. By dynamically extracting, consolidating, and retrieving compact memory representations, Mem0 achieves state-of-the-art performance across single-hop and multi-hop reasoning, while $\texttt{Mem0}^{\tiny g}$ ’s graph-based extensions unlock significant gains in temporal and open-domain tasks. On the LOCOMO benchmark, our methods deliver 5%, 11%, and 7% relative improvements in single-hop, temporal, and multi-hop reasoning question types over best performing methods in respective question type and reduce p95 latency by over 91% compared to full-context baselines—demonstrating a powerful balance between precision and responsiveness. Mem0’s dense memory pipeline excels at rapid retrieval for straightforward queries, minimizing token usage and computational overhead. In contrast, $\texttt{Mem0}^{\tiny g}$ ’s structured graph representations provide nuanced relational clarity, enabling complex event sequencing and rich context integration without sacrificing practical efficiency. Together, they form a versatile memory toolkit that adapts to diverse conversational demands while remaining deployable at scale.

Future research directions include optimizing graph operations to reduce the latency overhead in $\texttt{Mem0}^{\tiny g}$, exploring hierarchical memory architectures that blend efficiency with relational representation, and developing more sophisticated memory consolidation mechanisms inspired by human cognitive processes. Additionally, extending our memory frameworks to domains beyond conversational scenarios, such as procedural reasoning and multimodal interactions, would further validate their broader applicability. By addressing the fundamental limitations of fixed context windows, our work represents a significant advancement toward conversational AI systems capable of maintaining coherent, contextually rich interactions over extended periods, much like their human counterparts.

## 6 Acknowledgments

We would like to express our sincere gratitude to Harsh Agarwal, Shyamal Anadkat, Prithvijit Chattopadhyay, Siddesh Choudhary, Rishabh Jain, and Vaibhav Pandey for their invaluable insights and thorough reviews of early drafts. Their constructive comments and detailed suggestions helped refine the manuscript, enhancing both its clarity and overall quality. We deeply appreciate their generosity in dedicating time and expertise to this work.

## References

## Appendix

## Appendix A Prompts

In developing our LLM-as-a-Judge prompt, we adapt elements from the prompt released by [^17].

EqBox s O!htbp m floatplacement=#2, IfBooleanTF=#1float\*,width=float, title=#3,

\[!htbp\]Prompt Template for LLM as a Judge Your task is to label an answer to a question as "CORRECT" or "WRONG". You will be given the following data: (1) a question (posed by one user to another user), (2) a ‘gold’ (ground truth) answer, (3) a generated answer which you will score as CORRECT/WRONG.

The point of the question is to ask about something one user should know about the other user based on their prior conversations. The gold answer will usually be a concise and short answer that includes the referenced topic, for example:

Question: Do you remember what I got the last time I went to Hawaii?

Gold answer: A shell necklace

The generated answer might be much longer, but you should be generous with your grading - as long as it touches on the same topic as the gold answer, it should be counted as CORRECT.

For time related questions, the gold answer will be a specific date, month, year, etc. The generated answer might be much longer or use relative time references (like ‘last Tuesday’ or ‘next month’), but you should be generous with your grading - as long as it refers to the same date or time period as the gold answer, it should be counted as CORRECT. Even if the format differs (e.g., ‘May 7th’ vs ‘7 May’), consider it CORRECT if it’s the same date.

Now it’s time for the real question:

Question: {question}

Gold answer: {gold\_answer}

Generated answer: {generated\_answer}

First, provide a short (one sentence) explanation of your reasoning, then finish with CORRECT or WRONG. Do NOT include both CORRECT and WRONG in your response, or it will break the evaluation script.

Just return the label CORRECT or WRONG in a json format with the key as "label".

\[!htbp\]Prompt Template for Results Generation (Mem0) You are an intelligent memory assistant tasked with retrieving accurate information from conversation memories.

\# CONTEXT:

You have access to memories from two speakers in a conversation. These memories contain timestamped information that may be relevant to answering the question.

\# INSTRUCTIONS:

1\. Carefully analyze all provided memories from both speakers

2\. Pay special attention to the timestamps to determine the answer

3\. If the question asks about a specific event or fact, look for direct evidence in the memories

4\. If the memories contain contradictory information, prioritize the most recent memory

5\. If there is a question about time references (like "last year", "two months ago", etc.), calculate the actual date based on the memory timestamp. For example, if a memory from 4 May 2022 mentions "went to India last year," then the trip occurred in 2021.

6\. Always convert relative time references to specific dates, months, or years. For example, convert "last year" to "2022" or "two months ago" to "March 2023" based on the memory timestamp. Ignore the reference while answering the question.

7\. Focus only on the content of the memories from both speakers. Do not confuse character names mentioned in memories with the actual users who created those memories.

8\. The answer should be less than 5-6 words.

\# APPROACH (Think step by step):

1\. First, examine all memories that contain information related to the question

2\. Examine the timestamps and content of these memories carefully

3\. Look for explicit mentions of dates, times, locations, or events that answer the question

4\. If the answer requires calculation (e.g., converting relative time references), show your work

5\. Formulate a precise, concise answer based solely on the evidence in the memories

6\. Double-check that your answer directly addresses the question asked

7\. Ensure your final answer is specific and avoids vague time references

Memories for user {speaker\_1\_user\_id}:

{speaker\_1\_memories}

Memories for user {speaker\_2\_user\_id}:

{speaker\_2\_memories}

Question: {question}

Answer:

\[!htbp\]Prompt Template for Results Generation ($\texttt{Mem0}^{\tiny g}$) (same as previous)

\# APPROACH (Think step by step):

1\. First, examine all memories that contain information related to the question

2\. Examine the timestamps and content of these memories carefully

3\. Look for explicit mentions of dates, times, locations, or events that answer the question

4\. If the answer requires calculation (e.g., converting relative time references), show your work

5\. Analyze the knowledge graph relations to understand the user’s knowledge context

6\. Formulate a precise, concise answer based solely on the evidence in the memories

7\. Double-check that your answer directly addresses the question asked

8\. Ensure your final answer is specific and avoids vague time references

Memories for user {speaker\_1\_user\_id}:

{speaker\_1\_memories}

Relations for user {speaker\_1\_user\_id}:

{speaker\_1\_graph\_memories}

Memories for user {speaker\_2\_user\_id}:

{speaker\_2\_memories}

Relations for user {speaker\_2\_user\_id}:

{speaker\_2\_graph\_memories}

Question: {question}

Answer:

\[!htbp\]Prompt Template for OpenAI ChatGPT Can you please extract relevant information from this conversation and create memory entries for each user mentioned? Please store these memories in your knowledge base in addition to the timestamp provided for future reference and personalized interactions.

(1:56 pm on 8 May, 2023) Caroline: Hey Mel! Good to see you! How have you been?

(1:56 pm on 8 May, 2023) Melanie: Hey Caroline! Good to see you! I’m swamped with the kids & work. What’s up with you? Anything new?

(1:56 pm on 8 May, 2023) Caroline: I went to a LGBTQ support group yesterday and it was so powerful.

...

## Appendix B Algorithm

Algorithm 1 Memory Management System: Update Operations

Input: Set of retrieved memories $F$, Existing memory store $M=\{m_{1},m_{2},\ldots,m_{n}\}$

Output: Updated memory store $M^{\prime}$

procedure UpdateMemory($F,M$)

for each fact $f\in F$ do

$operation\leftarrow\textsc{ClassifyOperation}(f,M)$ $\triangleright$ Execute appropriate operation based on classification

if $operation=\text{ADD}$ then

 $id\leftarrow\text{GenerateUniqueID}()$

$M\leftarrow M\cup\{(id,f,\text{"ADD"})\}$ $\triangleright$ Add new fact with unique identifier

else if $operation=\text{UPDATE}$ then

 $m_{i}\leftarrow\text{FindRelatedMemory}(f,M)$

if $\text{InformationContent}(f)>\text{InformationContent}(m_{i})$ then

$M\leftarrow(M\setminus\{m_{i}\})\cup\{(id_{i},f,\text{"UPDATE"})\}$ $\triangleright$ Replace with richer information

end if

else if $operation=\text{DELETE}$ then

 $m_{i}\leftarrow\text{FindContradictedMemory}(f,M)$

$M\leftarrow M\setminus\{m_{i}\}$ $\triangleright$ Remove contradicted information

else if $operation=\text{NOOP}$ then

No operation performed $\triangleright$ Fact already exists or is irrelevant

end if

end for

return $M$

end procedure

function ClassifyOperation($f,M$)

if $\lnot\text{SemanticallySimilar}(f,M)$ then

return ADD $\triangleright$ New information not present in memory

else if $\text{Contradicts}(f,M)$ then

return DELETE $\triangleright$ Information conflicts with existing memory

else if $\text{Augments}(f,M)$ then

return UPDATE $\triangleright$ Enhances existing information in memory

else

return NOOP $\triangleright$ No change required

end if

end function

## Appendix C Selected Baselines

#### LoCoMo

The LoCoMo framework implements a sophisticated memory pipeline that enables LLM agents to maintain coherent, long-term conversations. At its core, the system divides memory into short-term and long-term components. After each conversation session, agents generate summaries (stored as short-term memory) that distill key information from that interaction. Simultaneously, individual conversation turns are transformed into ‘observations’ - factual statements about each speaker’s persona and life events that are stored in long-term memory with references to the specific dialog turns that produced them. When generating new responses, agents leverage both the most recent session summary and selectively retrieve relevant observations from their long-term memory. This dual-memory approach is further enhanced by incorporating a temporal event graph that tracks causally connected life events occurring between conversation sessions. By conditioning responses on retrieved memories, current conversation context, persona information, and intervening life events, the system enables agents to maintain consistent personalities and recall important details across conversations spanning hundreds of turns and dozens of sessions.

#### ReadAgent

ReadAgent addresses the fundamental limitations of LLMs by emulating how humans process lengthy texts through a sophisticated three-stage pipeline. First, in Episode Pagination, the system intelligently segments text at natural cognitive boundaries rather than arbitrary cutoffs. Next, during Memory Gisting, it distills each segment into concise summaries that preserve essential meaning while drastically reducing token count—similar to how human memory retains the substance of information without verbatim recall. Finally, when tasked with answering questions, the Interactive Lookup mechanism examines these gists and strategically retrieves only the most relevant original text segments for detailed processing. This human-inspired approach enables LLMs to effectively manage documents up to 20 times longer than their normal context windows. By balancing global understanding through gists with selective attention to details, ReadAgent achieves both computational efficiency and improved comprehension, demonstrating that mimicking human cognitive processes can significantly enhance AI text processing capabilities.

#### MemoryBank

The MemoryBank system enhances LLMs with long-term memory through a sophisticated three-part pipeline. At its core, the Memory Storage component warehouses detailed conversation logs, hierarchical event summaries, and evolving user personality profiles. When a new interaction occurs, the Memory Retrieval mechanism employs a dual-tower dense retrieval model to extract contextually relevant past information. The Memory Updating component, provides a human-like forgetting mechanism where memories strengthen when recalled and naturally decay over time if unused. This comprehensive approach enables AI companions to recall pertinent information, maintain contextual awareness across extended interactions, and develop increasingly accurate user portraits, resulting in more personalized and natural long-term conversations.

#### MemGPT

The MemGPT system introduces an operating system-inspired approach to overcome the context window limitations inherent in LLMs. At its core, MemGPT employs a sophisticated memory management pipeline consisting of three key components: a hierarchical memory system, self-directed memory operations, and an event-based control flow mechanism. The system divides available memory into ‘main context’ (analogous to RAM in traditional operating systems) and ‘external context’ (analogous to disk storage). The main context—which is bound by the LLM’s context window—contains system instructions, recent conversation history, and working memory that can be modified by the model. The external context stores unlimited information outside the model’s immediate context window, including complete conversation histories and archival data. When the LLM needs information not present in main context, it can initiate function calls to search, retrieve, or modify content across these memory tiers, effectively ‘paging’ relevant information in and out of its limited context window. This OS-inspired architecture enables MemGPT to maintain conversational coherence over extended interactions, manage documents that exceed standard context limits, and perform multi-hop information retrieval tasks—all while operating with fixed-context models. The system’s ability to intelligently manage its own memory resources provides the illusion of infinite context, significantly extending what’s possible with current LLM technology.

#### A-Mem

The A-Mem model introduces an agentic memory system designed for LLM agents. This system dynamically structures and evolves memories through interconnected notes. Each note captures interactions enriched with structured attributes like keywords, contextual descriptions, and tags generated by the LLM. Upon creating a new memory, A-MEM uses semantic embeddings to retrieve relevant existing notes, then employs an LLM-driven approach to establish meaningful links based on similarities and shared attributes. Crucially, the memory evolution mechanism updates existing notes dynamically, refining their contextual information and attributes whenever new relevant memories are integrated. Thus, memory structure continually evolves, allowing richer and contextually deeper connections among memories. Retrieval from memory is conducted through semantic similarity, providing relevant historical context during agent interactions

[^1]: Anthropic. Model card and evaluations for claude models. Technical report, Anthropic, February 2025. URL [https://www.anthropic.com/news/claude-3-7-sonnet](https://www.anthropic.com/news/claude-3-7-sonnet).

[^2]: Jan Assmann. Communicative and cultural memory. In *Cultural memories: The geographical point of view*, pages 15–27. Springer, 2011.

[^3]: Aydar Bulatov, Yury Kuratov, and Mikhail Burtsev. Recurrent memory transformer. *Advances in Neural Information Processing Systems*, 35:11079–11091, 2022.

[^4]: Prateek Chhikara, Jiarui Zhang, Filip Ilievski, Jonathan Francis, and Kaixin Ma. Knowledge-enhanced agents for interactive text games. In *Proceedings of the 12th Knowledge Capture Conference 2023*, pages 157–165, 2023.

[^5]: Fergus IM Craik and Janine M Jennings. Human memory. 1992.

[^6]: Gaurav Goswami. Dissecting the metrics: How different evaluation approaches yield diverse results for conversational ai. *Authorea Preprints*, 2025.

[^7]: Tianyu Guo, Druv Pai, Yu Bai, Jiantao Jiao, Michael Jordan, and Song Mei. Active-dormant attention heads: Mechanistically demystifying extreme-token phenomena in llms. In *NeurIPS 2024 Workshop on Mathematics of Modern Machine Learning*, 2024.

[^8]: Kostas Hatalis, Despina Christou, Joshua Myers, Steven Jones, Keith Lambert, Adam Amos-Binks, Zohreh Dannenhauer, and Dustin Dannenhauer. Memory matters: The need to improve long-term memory in llm-agents. In *Proceedings of the AAAI Symposium Series*, volume 2, pages 277–280, 2023.

[^9]: Zihong He, Weizhe Lin, Hao Zheng, Fan Zhang, Matt W Jones, Laurence Aitchison, Xuhai Xu, Miao Liu, Per Ola Kristensson, and Junxiao Shen. Human-inspired perspectives: A survey on ai long-term memory. *arXiv preprint arXiv:2411.00489*, 2024.

[^10]: Aaron Hurst, Adam Lerer, Adam P Goucher, Adam Perelman, Aditya Ramesh, Aidan Clark, AJ Ostrow, Akila Welihinda, Alan Hayes, Alec Radford, et al. Gpt-4o system card. *arXiv preprint arXiv:2410.21276*, 2024.

[^11]: Aaron Jaech, Adam Kalai, Adam Lerer, Adam Richardson, Ahmed El-Kishky, Aiden Low, Alec Helyar, Aleksander Madry, Alex Beutel, Alex Carney, et al. Openai o1 system card. *arXiv preprint arXiv:2412.16720*, 2024.

[^12]: Kuang-Huei Lee, Xinyun Chen, Hiroki Furuta, John Canny, and Ian Fischer. A human-inspired reading agent with gist memory of very long contexts. In *International Conference on Machine Learning*, pages 26396–26415. PMLR, 2024.

[^13]: Lei Liu, Xiaoyan Yang, Yue Shen, Binbin Hu, Zhiqiang Zhang, Jinjie Gu, and Guannan Zhang. Think-in-memory: Recalling and post-thinking enable llms with long-term memory. *arXiv preprint arXiv:2311.08719*, 2023.

[^14]: Adyasha Maharana, Dong-Ho Lee, Sergey Tulyakov, Mohit Bansal, Francesco Barbieri, and Yuwei Fang. Evaluating very long-term conversational memory of llm agents. In *Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pages 13851–13870, 2024.

[^15]: Bodhisattwa Prasad Majumder, Bhavana Dalvi Mishra, Peter Jansen, Oyvind Tafjord, Niket Tandon, Li Zhang, Chris Callison-Burch, and Peter Clark. Clin: A continually learning language agent for rapid task adaptation and generalization. In *First Conference on Language Modeling*.

[^16]: Elliot Nelson, Georgios Kollias, Payel Das, Subhajit Chaudhury, and Soham Dan. Needle in the haystack for memory based large language models. *arXiv preprint arXiv:2407.01437*, 2024.

[^17]: Charles Packer, Vivian Fang, Shishir\_G Patil, Kevin Lin, Sarah Wooders, and Joseph\_E Gonzalez. Memgpt: Towards llms as operating systems. 2023.

[^18]: Preston Rasmussen, Pavlo Paliychuk, Travis Beauvais, Jack Ryan, and Daniel Chalef. Zep: A temporal knowledge graph architecture for agent memory. *arXiv preprint arXiv:2501.13956*, 2025.

[^19]: Parth Sarthi, Salman Abdullah, Aditi Tuli, Shubh Khanna, Anna Goldie, and Christopher D Manning. Raptor: Recursive abstractive processing for tree-organized retrieval. In *The Twelfth International Conference on Learning Representations*, 2024.

[^20]: Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. Reflexion: Language agents with verbal reinforcement learning. *Advances in Neural Information Processing Systems*, 36:8634–8652, 2023.

[^21]: Prabhjot Singh, Prateek Chhikara, and Jasmeet Singh. An ensemble approach for extractive text summarization. In *2020 International Conference on Emerging Trends in Information Technology and Engineering (ic-ETITE)*, pages 1–7. IEEE, 2020.

[^22]: Arpita Soni, Rajeev Arora, Anoop Kumar, and Dheerendra Panwar. Evaluating domain coverage in low-resource generative chatbots: A comparative study of open-domain and closed-domain approaches using bleu scores. In *2024 International Conference on Electrical Electronics and Computing Technologies (ICEECT)*, volume 1, pages 1–6. IEEE, 2024.

[^23]: Gemini Team, Petko Georgiev, Ving Ian Lei, Ryan Burnell, Libin Bai, Anmol Gulati, Garrett Tanzer, Damien Vincent, Zhufeng Pan, Shibo Wang, et al. Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context. *arXiv preprint arXiv:2403.05530*, 2024.

[^24]: Joan C Timoneda and Sebastián Vallejo Vera. Memory is all you need: Testing how model memory affects llm performance in annotation tasks. *arXiv preprint arXiv:2503.04874*, 2025.

[^25]: Wujiang Xu, Zujie Liang, Kai Mei, Hang Gao, Juntao Tan, and Yongfeng Zhang. A-mem: Agentic memory for llm agents. *arXiv preprint arXiv:2502.12110*, 2025.

[^26]: Yangyang Yu, Haohang Li, Zhi Chen, Yuechen Jiang, Yang Li, Denghui Zhang, Rong Liu, Jordan W Suchow, and Khaldoun Khashanah. Finmem: A performance-enhanced llm trading agent with layered memory and character design. In *Proceedings of the AAAI Symposium Series*, volume 3, pages 595–597, 2024.

[^27]: Jiarui Zhang. Guided profile generation improves personalization with large language models. In *Findings of the Association for Computational Linguistics: EMNLP 2024*, pages 4005–4016, 2024.

[^28]: Jiarui Zhang, Filip Ilievski, Kaixin Ma, Jonathan Francis, and Alessandro Oltramari. A study of zero-shot adaptation with commonsense knowledge. In *AKBC*, 2022.

[^29]: Zeyu Zhang, Xiaohe Bo, Chen Ma, Rui Li, Xu Chen, Quanyu Dai, Jieming Zhu, Zhenhua Dong, and Ji-Rong Wen. A survey on the memory mechanism of large language model based agents. *arXiv preprint arXiv:2404.13501*, 2024.

[^30]: Wanjun Zhong, Lianghong Guo, Qiqi Gao, He Ye, and Yanlin Wang. Memorybank: Enhancing large language models with long-term memory. In *Proceedings of the AAAI Conference on Artificial Intelligence*, volume 38, pages 19724–19731, 2024.