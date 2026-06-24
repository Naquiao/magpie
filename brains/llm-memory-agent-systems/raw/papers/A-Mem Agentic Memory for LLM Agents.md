---
title: "A-Mem: Agentic Memory for LLM Agents"
source: "https://arxiv.org/html/2502.12110v11"
author:
published:
created: 2026-06-24
description:
tags:
  - "clippings"
---
Wujiang Xu <sup>1</sup>, Zujie Liang <sup>2</sup>, Kai Mei <sup>1</sup>, Hang Gao <sup>1</sup>, Juntao Tan <sup>1</sup>, Yongfeng Zhang <sup>1,3</sup>  
<sup>1</sup> Rutgers University    <sup>2</sup> Independent Researcher    <sup>3</sup> AIOS Foundation     
[wujiang.xu@rutgers.edu](mailto:wujiang.xu@rutgers.edu)

###### Abstract

While large language model (LLM) agents can effectively use external tools for complex real-world tasks, they require memory systems to leverage historical experiences. Current memory systems enable basic storage and retrieval but lack sophisticated memory organization, despite recent attempts to incorporate graph databases. Moreover, these systems’ fixed operations and structures limit their adaptability across diverse tasks. To address this limitation, this paper proposes a novel agentic memory system for LLM agents that can dynamically organize memories in an agentic way. Following the basic principles of the Zettelkasten method, we designed our memory system to create interconnected knowledge networks through dynamic indexing and linking. When a new memory is added, we generate a comprehensive note containing multiple structured attributes, including contextual descriptions, keywords, and tags. The system then analyzes historical memories to identify relevant connections, establishing links where meaningful similarities exist. Additionally, this process enables memory evolution – as new memories are integrated, they can trigger updates to the contextual representations and attributes of existing historical memories, allowing the memory network to continuously refine its understanding. Our approach combines the structured organization principles of Zettelkasten with the flexibility of agent-driven decision making, allowing for more adaptive and context-aware memory management. Empirical experiments on six foundation models show superior improvement against existing SOTA baselines.

Code for Benchmark Evaluation:  
[https://github.com/WujiangXu/AgenticMemory](https://github.com/WujiangXu/AgenticMemory)

Code for Production-ready Agentic Memory:  
[https://github.com/WujiangXu/A-mem-sys](https://github.com/WujiangXu/A-mem-sys)

## 1 Introduction

Large Language Model (LLM) agents have demonstrated remarkable capabilities in various tasks, with recent advances enabling them to interact with environments, execute tasks, and make decisions autonomously [^23] [^33] [^7]. They integrate LLMs with external tools and delicate workflows to improve reasoning and planning abilities. Though LLM agent has strong reasoning performance, it still needs a memory system to provide long-term interaction ability with the external environment [^35].

Existing memory systems [^25] [^39] [^28] [^21] for LLM agents provide basic memory storage functionality. These systems require agent developers to predefine memory storage structures, specify storage points within the workflow, and establish retrieval timing. Meanwhile, to improve structured memory organization, Mem0 [^8], following the principles of RAG [^9] [^18] [^30], incorporates graph databases for storage and retrieval processes. While graph databases provide structured organization for memory systems, their reliance on predefined schemas and relationships fundamentally limits their adaptability. This limitation manifests clearly in practical scenarios - when an agent learns a novel mathematical solution, current systems can only categorize and link this information within their preset framework, unable to forge innovative connections or develop new organizational patterns as knowledge evolves. Such rigid structures, coupled with fixed agent workflows, severely restrict these systems’ ability to generalize across new environments and maintain effectiveness in long-term interactions. The challenge becomes increasingly critical as LLM agents tackle more complex, open-ended tasks, where flexible knowledge organization and continuous adaptation are essential. Therefore, how to design a flexible and universal memory system that supports LLM agents’ long-term interactions remains a crucial challenge.

![Refer to caption](https://arxiv.org/html/2502.12110v11/x3.png)

Figure 1: Traditional memory systems require predefined memory access patterns specified in the workflow, limiting their adaptability to diverse scenarios. Contrastly, our A-Mem enhances the flexibility of LLM agents by enabling dynamic memory operations.

In this paper, we introduce a novel agentic memory system, named as A-Mem, for LLM agents that enables dynamic memory structuring without relying on static, predetermined memory operations. Our approach draws inspiration from the Zettelkasten method [^15] [^1], a sophisticated knowledge management system that creates interconnected information networks through atomic notes and flexible linking mechanisms. Our system introduces an agentic memory architecture that enables autonomous and flexible memory management for LLM agents. For each new memory, we construct comprehensive notes, which integrates multiple representations: structured textual attributes including several attributes and embedding vectors for similarity matching. Then A-Mem analyzes the historical memory repository to establish meaningful connections based on semantic similarities and shared attributes. This integration process not only creates new links but also enables dynamic evolution when new memories are incorporated, they can trigger updates to the contextual representations of existing memories, allowing the entire memories to continuously refine and deepen its understanding over time. The contributions are summarized as:

We present A-Mem, an agentic memory system for LLM agents that enables autonomous generation of contextual descriptions, dynamic establishment of memory connections, and intelligent evolution of existing memories based on new experiences. This system equips LLM agents with long-term interaction capabilities without requiring predetermined memory operations.

We design an agentic memory update mechanism where new memories automatically trigger two key operations: link generation and memory evolution. Link generation automatically establishes connections between memories by identifying shared attributes and similar contextual descriptions. Memory evolution enables existing memories to dynamically adapt as new experiences are analyzed, leading to the emergence of higher-order patterns and attributes.

We conduct comprehensive evaluations of our system using a long-term conversational dataset, comparing performance across six foundation models using six distinct evaluation metrics, demonstrating significant improvements. Moreover, we provide T-SNE visualizations to illustrate the structured organization of our agentic memory system.

## 2 Related Work

### 2.1 Memory for LLM Agents

Prior works on LLM agent memory systems have explored various mechanisms for memory management and utilization [^23] [^21] [^8] [^39]. Some approaches complete interaction storage, which maintains comprehensive historical records through dense retrieval models [^39] or read-write memory structures [^24]. Moreover, MemGPT [^25] leverages cache-like architectures to prioritize recent information. Similarly, SCM [^32] proposes a Self-Controlled Memory framework that enhances LLMs’ capability to maintain long-term memory through a memory stream and controller mechanism. However, these approaches face significant limitations in handling diverse real-world tasks. While they can provide basic memory functionality, their operations are typically constrained by predefined structures and fixed workflows. These constraints stem from their reliance on rigid operational patterns, particularly in memory writing and retrieval processes. Such inflexibility leads to poor generalization in new environments and limited effectiveness in long-term interactions. Therefore, designing a flexible and universal memory system that supports agents’ long-term interactions remains a crucial challenge.

### 2.2 Retrieval-Augmented Generation

Retrieval-Augmented Generation (RAG) has emerged as a powerful approach to enhance LLMs by incorporating external knowledge sources [^18] [^6] [^10]. The standard RAG [^37] [^34] process involves indexing documents into chunks, retrieving relevant chunks based on semantic similarity, and augmenting the LLM’s prompt with this retrieved context for generation. Advanced RAG systems [^20] [^12] have evolved to include sophisticated pre-retrieval and post-retrieval optimizations. Building upon these foundations, recent researches has introduced agentic RAG systems that demonstrate more autonomous and adaptive behaviors in the retrieval process. These systems can dynamically determine when and what to retrieve [^4] [^14], generate hypothetical responses to guide retrieval, and iteratively refine their search strategies based on intermediate results [^31] [^29].

However, while agentic RAG approaches demonstrate agency in the retrieval phase by autonomously deciding when and what to retrieve [^4] [^14] [^38], our agentic memory system exhibits agency at a more fundamental level through the autonomous evolution of its memory structure. Inspired by the Zettelkasten method, our system allows memories to actively generate their own contextual descriptions, form meaningful connections with related memories, and evolve both their content and relationships as new experiences emerge. This fundamental distinction in agency between retrieval versus storage and evolution distinguishes our approach from agentic RAG systems, which maintain static knowledge bases despite their sophisticated retrieval mechanisms.

## 3 Methodolodgy

Our proposed agentic memory system draws inspiration from the Zettelkasten method, implementing a dynamic and self-evolving memory system that enables LLM agents to maintain long-term memory without predetermined operations. The system’s design emphasizes atomic note-taking, flexible linking mechanisms, and continuous evolution of knowledge structures.

![Refer to caption](https://arxiv.org/html/2502.12110v11/x5.png)

Figure 2: Our A-Mem architecture comprises three integral parts in memory storage. During note construction, the system processes new interaction memories and stores them as notes with multiple attributes. The link generation process first retrieves the most relevant historical memories and then employs an LLM to determine whether connections should be established between them. The concept of a ’box’ describes that related memories become interconnected through their similar contextual descriptions, analogous to the Zettelkasten method. However, our approach allows individual memories to exist simultaneously within multiple different boxes. During the memory retrieval stage, we extract query embeddings using a text encoding model and search the memory database for relevant matches. When related memory is retrieved, similar memories that are linked within the same box are also automatically accessed.

### 3.1 Note Construction

Building upon the Zettelkasten method’s principles of atomic note-taking and flexible organization, we introduce an LLM-driven approach to memory note construction. When an agent interacts with its environment, we construct structured memory notes that capture both explicit information and LLM-generated contextual understanding. Each memory note $m_{i}$ in our collection $\mathcal{M}=\{m_{1},m_{2},...,m_{N}\}$ is represented as:

$$
m_{i}=\{c_{i},t_{i},K_{i},G_{i},X_{i},e_{i},L_{i}\}
$$

where $c_{i}$ represents the original interaction content, $t_{i}$ is the timestamp of the interaction, $K_{i}$ denotes LLM-generated keywords that capture key concepts, $G_{i}$ contains LLM-generated tags for categorization, $X_{i}$ represents the LLM-generated contextual description that provides rich semantic understanding, and $L_{i}$ maintains the set of linked memories that share semantic relationships. To enrich each memory note with meaningful context beyond its basic content and timestamp, we leverage an LLM to analyze the interaction and generate these semantic components. The note construction process involves prompting the LLM with carefully designed templates $P_{s1}$:

$$
K_{i},G_{i},X_{i}\leftarrow\text{LLM}(c_{i}\;\Vert t_{i}\;\Vert P_{s1})
$$

Following the Zettelkasten principle of atomicity, each note captures a single, self-contained unit of knowledge. To enable efficient retrieval and linking, we compute a dense vector representation via a text encoder [^27] that encapsulates all textual components of the note:

$$
e_{i}=f_{\text{enc}}[\;\text{concat}(c_{i},K_{i},G_{i},X_{i})\;]
$$

By using LLMs to generate enriched components, we enable autonomous extraction of implicit knowledge from raw interactions. The multi-faceted note structure ($K_{i}$, $G_{i}$, $X_{i}$) creates rich representations that capture different aspects of the memory, facilitating nuanced organization and retrieval. Additionally, the combination of LLM-generated semantic components with dense vector representations provides both context and computationally efficient similarity matching.

### 3.2 Link Generation

Our system implements an autonomous link generation mechanism that enables new memory notes to form meaningful connections without predefined rules. When the constrctd memory note $m_{n}$ is added to the system, we first leverage its semantic embedding for similarity-based retrieval. For each existing memory note $m_{j}\in\mathcal{M}$, we compute a similarity score:

$$
s_{n,j}=\frac{e_{n}\cdot e_{j}}{|e_{n}||e_{j}|}
$$

The system then identifies the top- $k$ most relevant memories:

$$
\mathcal{M}_{\text{near}}^{n}=\{m_{j}|\;\text{rank}(s_{n,j})\leq k,m_{j}\in\mathcal{M}\}
$$

Based on these candidate nearest memories, we prompt the LLM to analyze potential connections based on their potential common attributes. Formally, the link set of memory $m_{n}$ update like:

$$
L_{i}\leftarrow\text{LLM}(m_{n}\;\Vert\mathcal{M}_{\text{near}}^{n}\;\Vert P_{s2})
$$

Each generated link $l_{i}$ is structured as: $L_{i}=\{m_{i},...,m_{k}\}$. By using embedding-based retrieval as an initial filter, we enable efficient scalability while maintaining semantic relevance. A-Mem can quickly identify potential connections even in large memory collections without exhaustive comparison. More importantly, the LLM-driven analysis allows for nuanced understanding of relationships that goes beyond simple similarity metrics. The language model can identify subtle patterns, causal relationships, and conceptual connections that might not be apparent from embedding similarity alone. We implements the Zettelkasten principle of flexible linking while leveraging modern language models. The resulting network emerges organically from memory content and context, enabling natural knowledge organization.

### 3.3 Memory Evolution

After creating links for the new memory, A-Mem evolves the retrieved memories based on their textual information and relationships with the new memory. For each memory $m_{j}$ in the nearest neighbor set $\mathcal{M}_{\text{near}}^{n}$, the system determines whether to update its context, keywords, and tags. This evolution process can be formally expressed as:

$$
m_{j}^{*}\leftarrow\text{LLM}(m_{n}\;\Vert\mathcal{M}_{\text{near}}^{n}\setminus m_{j}\;\Vert m_{j}\;\Vert P_{s3})
$$

The evolved memory $m_{j}^{*}$ then replaces the original memory $m_{j}$ in the memory set $\mathcal{M}$. This evolutionary approach enables continuous updates and new connections, mimicking human learning processes. As the system processes more memories over time, it develops increasingly sophisticated knowledge structures, discovering higher-order patterns and concepts across multiple memories. This creates a foundation for autonomous memory learning where knowledge organization becomes progressively richer through the ongoing interaction between new experiences and existing memories.

### 3.4 Retrieve Relative Memory

In each interaction, our A-Mem performs context-aware memory retrieval to provide the agent with relevant historical information. Given a query text $q$ from the current interaction, we first compute its dense vector representation using the same text encoder used for memory notes:

$$
e_{q}=f_{\text{enc}}(q)
$$

The system then computes similarity scores between the query embedding and all existing memory notes in $\mathcal{M}$ using cosine similarity:

$$
s_{q,i}=\frac{e_{q}\cdot e_{i}}{|e_{q}||e_{i}|},\text{where}\;e_{i}\in m_{i},\;\forall m_{i}\in\mathcal{M}
$$

Then we retrieve the k most relevant memories from the historical memory storage to construct a contextually appropriate prompt.

$$
\mathcal{M}_{\text{retrieved}}=\{m_{i}|\text{rank}(s_{q,i})\leq k,m_{i}\in\mathcal{M}\}
$$

These retrieved memories provide relevant historical context that helps the agent better understand and respond to the current interaction. The retrieved context enriches the agent’s reasoning process by connecting the current interaction with related past experiences stored in the memory system.

## 4 Experiment

### 4.1 Dataset and Evaluation

To evaluate the effectiveness of instruction-aware recommendation in long-term conversations, we utilize the LoCoMo dataset [^22], which contains significantly longer dialogues compared to existing conversational datasets [^36] [^13]. While previous datasets contain dialogues with around 1K tokens over 4-5 sessions, LoCoMo features much longer conversations averaging 9K tokens spanning up to 35 sessions, making it particularly suitable for evaluating models’ ability to handle long-range dependencies and maintain consistency over extended conversations. The LoCoMo dataset comprises diverse question types designed to comprehensively evaluate different aspects of model understanding: (1) single-hop questions answerable from a single session; (2) multi-hop questions requiring information synthesis across sessions; (3) temporal reasoning questions testing understanding of time-related information; (4) open-domain knowledge questions requiring integration of conversation context with external knowledge; and (5) adversarial questions assessing models’ ability to identify unanswerable queries. In total, LoCoMo contains 7,512 question-answer pairs across these categories. Besides, we use a new dataset, named DialSim [^16], to evaluate the effectiveness of our memory system. It is question-answering dataset derived from long-term multi-party dialogues. The dataset is derived from popular TV shows (Friends, The Big Bang Theory, and The Office), covering 1,300 sessions spanning five years, containing approximately 350,000 tokens, and including more than 1,000 questions per session from refined fan quiz website questions and complex questions generated from temporal knowledge graphs.

For comparison baselines, we compare to LoCoMo [^22], ReadAgent [^17], MemoryBank [^39] and MemGPT [^25]. The detailed introduction of baselines can be found in Appendix A.1 For evaluation, we employ two primary metrics: the F1 score to assess answer accuracy by balancing precision and recall, and BLEU-1 [^26] to evaluate generated response quality by measuring word overlap with ground truth responses. Also, we report the average token length for answering one question. Besides reporting experiment results with four additional metrics (ROUGE-L, ROUGE-2, METEOR, and SBERT Similarity), we also present experimental outcomes using different foundation models including DeepSeek-R1-32B [^11], Claude 3.0 Haiku [^2], and Claude 3.5 Haiku [^3] in Appendix A.3.

### 4.2 Implementation Details

For all baselines and our proposed method, we maintain consistency by employing identical system prompts as detailed in Appendix B. The deployment of Qwen-1.5B/3B and Llama 3.2 1B/3B models is accomplished through local instantiation using Ollama <sup>1</sup>, with LiteLLM <sup>2</sup> managing structured output generation. For GPT models, we utilize the official structured output API. In our memory retrieval process, we primarily employ $k$ =10 for top- $k$ memory selection to maintain computational efficiency, while adjusting this parameter for specific categories to optimize performance. The detailed configurations of $k$ can be found in Appendix A.5. For text embedding, we implement the all-minilm-l6-v2 model across all experiments.

Table 1: Experimental results on LoCoMo dataset of QA tasks across five categories (Multi Hop, Temporal, Open Domain, Single Hop, and Adversial) using different methods. Results are reported in F1 and BLEU-1 (%) scores. The best performance is marked in bold, and our proposed method A-Mem (highlighted in gray) demonstrates competitive performance across six foundation language models.

<table><tbody><tr><td colspan="2" rowspan="3">Model</td><td rowspan="3">Method</td><td colspan="10">Category</td><td colspan="3">Average</td></tr><tr><td colspan="2">Multi Hop</td><td colspan="2">Temporal</td><td colspan="2">Open Domain</td><td colspan="2">Single Hop</td><td colspan="2">Adversial</td><td colspan="2">Ranking</td><td>Token</td></tr><tr><td>F1</td><td>BLEU</td><td>F1</td><td>BLEU</td><td>F1</td><td>BLEU</td><td>F1</td><td>BLEU</td><td>F1</td><td>BLEU</td><td>F1</td><td>BLEU</td><td>Length</td></tr><tr><td rowspan="10"><p></p><p>GPT</p><p></p></td><td rowspan="5"><p></p><p>4o-mini</p><p></p></td><td>LoCoMo</td><td>25.02</td><td>19.75</td><td>18.41</td><td>14.77</td><td>12.04</td><td>11.16</td><td>40.36</td><td>29.05</td><td>69.23</td><td>68.75</td><td>2.4</td><td>2.4</td><td>16,910</td></tr><tr><td>ReadAgent</td><td>9.15</td><td>6.48</td><td>12.60</td><td>8.87</td><td>5.31</td><td>5.12</td><td>9.67</td><td>7.66</td><td>9.81</td><td>9.02</td><td>4.2</td><td>4.2</td><td>643</td></tr><tr><td>MemoryBank</td><td>5.00</td><td>4.77</td><td>9.68</td><td>6.99</td><td>5.56</td><td>5.94</td><td>6.61</td><td>5.16</td><td>7.36</td><td>6.48</td><td>4.8</td><td>4.8</td><td>432</td></tr><tr><td>MemGPT</td><td>26.65</td><td>17.72</td><td>25.52</td><td>19.44</td><td>9.15</td><td>7.44</td><td>41.04</td><td>34.34</td><td>43.29</td><td>42.73</td><td>2.4</td><td>2.4</td><td>16,977</td></tr><tr><td>A-Mem</td><td>27.02</td><td>20.09</td><td>45.85</td><td>36.67</td><td>12.14</td><td>12.00</td><td>44.65</td><td>37.06</td><td>50.03</td><td>49.47</td><td>1.2</td><td>1.2</td><td>2,520</td></tr><tr><td rowspan="5"><p></p><p>4o</p><p></p></td><td>LoCoMo</td><td>28.00</td><td>18.47</td><td>9.09</td><td>5.78</td><td>16.47</td><td>14.80</td><td>61.56</td><td>54.19</td><td>52.61</td><td>51.13</td><td>2.0</td><td>2.0</td><td>16,910</td></tr><tr><td>ReadAgent</td><td>14.61</td><td>9.95</td><td>4.16</td><td>3.19</td><td>8.84</td><td>8.37</td><td>12.46</td><td>10.29</td><td>6.81</td><td>6.13</td><td>4.0</td><td>4.0</td><td>805</td></tr><tr><td>MemoryBank</td><td>6.49</td><td>4.69</td><td>2.47</td><td>2.43</td><td>6.43</td><td>5.30</td><td>8.28</td><td>7.10</td><td>4.42</td><td>3.67</td><td>5.0</td><td>5.0</td><td>569</td></tr><tr><td>MemGPT</td><td>30.36</td><td>22.83</td><td>17.29</td><td>13.18</td><td>12.24</td><td>11.87</td><td>60.16</td><td>53.35</td><td>34.96</td><td>34.25</td><td>2.4</td><td>2.4</td><td>16,987</td></tr><tr><td>A-Mem</td><td>32.86</td><td>23.76</td><td>39.41</td><td>31.23</td><td>17.10</td><td>15.84</td><td>48.43</td><td>42.97</td><td>36.35</td><td>35.53</td><td>1.6</td><td>1.6</td><td>1,216</td></tr><tr><td rowspan="10"><p></p><p>Qwen2.5</p><p></p></td><td rowspan="5"><p></p><p>1.5b</p><p></p></td><td>LoCoMo</td><td>9.05</td><td>6.55</td><td>4.25</td><td>4.04</td><td>9.91</td><td>8.50</td><td>11.15</td><td>8.67</td><td>40.38</td><td>40.23</td><td>3.4</td><td>3.4</td><td>16,910</td></tr><tr><td>ReadAgent</td><td>6.61</td><td>4.93</td><td>2.55</td><td>2.51</td><td>5.31</td><td>12.24</td><td>10.13</td><td>7.54</td><td>5.42</td><td>27.32</td><td>4.6</td><td>4.6</td><td>752</td></tr><tr><td>MemoryBank</td><td>11.14</td><td>8.25</td><td>4.46</td><td>2.87</td><td>8.05</td><td>6.21</td><td>13.42</td><td>11.01</td><td>36.76</td><td>34.00</td><td>2.6</td><td>2.6</td><td>284</td></tr><tr><td>MemGPT</td><td>10.44</td><td>7.61</td><td>4.21</td><td>3.89</td><td>13.42</td><td>11.64</td><td>9.56</td><td>7.34</td><td>31.51</td><td>28.90</td><td>3.4</td><td>3.4</td><td>16,953</td></tr><tr><td>A-Mem</td><td>18.23</td><td>11.94</td><td>24.32</td><td>19.74</td><td>16.48</td><td>14.31</td><td>23.63</td><td>19.23</td><td>46.00</td><td>43.26</td><td>1.0</td><td>1.0</td><td>1,300</td></tr><tr><td rowspan="5"><p></p><p>3b</p><p></p></td><td>LoCoMo</td><td>4.61</td><td>4.29</td><td>3.11</td><td>2.71</td><td>4.55</td><td>5.97</td><td>7.03</td><td>5.69</td><td>16.95</td><td>14.81</td><td>3.2</td><td>3.2</td><td>16,910</td></tr><tr><td>ReadAgent</td><td>2.47</td><td>1.78</td><td>3.01</td><td>3.01</td><td>5.57</td><td>5.22</td><td>3.25</td><td>2.51</td><td>15.78</td><td>14.01</td><td>4.2</td><td>4.2</td><td>776</td></tr><tr><td>MemoryBank</td><td>3.60</td><td>3.39</td><td>1.72</td><td>1.97</td><td>6.63</td><td>6.58</td><td>4.11</td><td>3.32</td><td>13.07</td><td>10.30</td><td>4.2</td><td>4.2</td><td>298</td></tr><tr><td>MemGPT</td><td>5.07</td><td>4.31</td><td>2.94</td><td>2.95</td><td>7.04</td><td>7.10</td><td>7.26</td><td>5.52</td><td>14.47</td><td>12.39</td><td>2.4</td><td>2.4</td><td>16,961</td></tr><tr><td>A-Mem</td><td>12.57</td><td>9.01</td><td>27.59</td><td>25.07</td><td>7.12</td><td>7.28</td><td>17.23</td><td>13.12</td><td>27.91</td><td>25.15</td><td>1.0</td><td>1.0</td><td>1,137</td></tr><tr><td rowspan="10"><p></p><p>Llama 3.2</p><p></p></td><td rowspan="5"><p></p><p>1b</p><p></p></td><td>LoCoMo</td><td>11.25</td><td>9.18</td><td>7.38</td><td>6.82</td><td>11.90</td><td>10.38</td><td>12.86</td><td>10.50</td><td>51.89</td><td>48.27</td><td>3.4</td><td>3.4</td><td>16,910</td></tr><tr><td>ReadAgent</td><td>5.96</td><td>5.12</td><td>1.93</td><td>2.30</td><td>12.46</td><td>11.17</td><td>7.75</td><td>6.03</td><td>44.64</td><td>40.15</td><td>4.6</td><td>4.6</td><td>665</td></tr><tr><td>MemoryBank</td><td>13.18</td><td>10.03</td><td>7.61</td><td>6.27</td><td>15.78</td><td>12.94</td><td>17.30</td><td>14.03</td><td>52.61</td><td>47.53</td><td>2.0</td><td>2.0</td><td>274</td></tr><tr><td>MemGPT</td><td>9.19</td><td>6.96</td><td>4.02</td><td>4.79</td><td>11.14</td><td>8.24</td><td>10.16</td><td>7.68</td><td>49.75</td><td>45.11</td><td>4.0</td><td>4.0</td><td>16,950</td></tr><tr><td>A-Mem</td><td>19.06</td><td>11.71</td><td>17.80</td><td>10.28</td><td>17.55</td><td>14.67</td><td>28.51</td><td>24.13</td><td>58.81</td><td>54.28</td><td>1.0</td><td>1.0</td><td>1,376</td></tr><tr><td rowspan="5"><p></p><p>3b</p><p></p></td><td>LoCoMo</td><td>6.88</td><td>5.77</td><td>4.37</td><td>4.40</td><td>10.65</td><td>9.29</td><td>8.37</td><td>6.93</td><td>30.25</td><td>28.46</td><td>2.8</td><td>2.8</td><td>16,910</td></tr><tr><td>ReadAgent</td><td>2.47</td><td>1.78</td><td>3.01</td><td>3.01</td><td>5.57</td><td>5.22</td><td>3.25</td><td>2.51</td><td>15.78</td><td>14.01</td><td>4.2</td><td>4.2</td><td>461</td></tr><tr><td>MemoryBank</td><td>6.19</td><td>4.47</td><td>3.49</td><td>3.13</td><td>4.07</td><td>4.57</td><td>7.61</td><td>6.03</td><td>18.65</td><td>17.05</td><td>3.2</td><td>3.2</td><td>263</td></tr><tr><td>MemGPT</td><td>5.32</td><td>3.99</td><td>2.68</td><td>2.72</td><td>5.64</td><td>5.54</td><td>4.32</td><td>3.51</td><td>21.45</td><td>19.37</td><td>3.8</td><td>3.8</td><td>16,956</td></tr><tr><td>A-Mem</td><td>17.44</td><td>11.74</td><td>26.38</td><td>19.50</td><td>12.53</td><td>11.83</td><td>28.14</td><td>23.87</td><td>42.04</td><td>40.60</td><td>1.0</td><td>1.0</td><td>1,126</td></tr></tbody></table>

### 4.3 Empricial Results

Performance Analysis. In our empirical evaluation, we compared A-Mem with four competitive baselines including LoCoMo [^22], ReadAgent [^17], MemoryBank [^39], and MemGPT [^25] on the LoCoMo dataset. For non-GPT foundation models, our A-Mem consistently outperforms all baselines across different categories, demonstrating the effectiveness of our agentic memory approach. For GPT-based models, while LoCoMo and MemGPT show strong performance in certain categories like Open Domain and Adversial tasks due to their robust pre-trained knowledge in simple fact retrieval, our A-Mem demonstrates superior performance in Multi-Hop tasks achieves at least two times better performance that require complex reasoning chains. In addition to experiments on the LoCoMo dataset, we also compare our method on the DialSim dataset against LoCoMo and MemGPT. A-Mem consistently outperforms all baselines across evaluation metrics, achieving an F1 score of 3.45 (a 35% improvement over LoCoMo’s 2.55 and 192% higher than MemGPT’s 1.18). The effectiveness of A-Mem stems from its novel agentic memory architecture that enables dynamic and structured memory management. Unlike traditional approaches that use static memory operations, our system creates interconnected memory networks through atomic notes with rich contextual descriptions, enabling more effective multi-hop reasoning. The system’s ability to dynamically establish connections between memories based on shared attributes and continuously update existing memory descriptions with new contextual information allows it to better capture and utilize the relationships between different pieces of information.

Table 2: Comparison of different memory mechanisms across multiple evaluation metrics on DialSim [^16]. Higher scores indicate better performance, with A-Mem showing superior results across all metrics.

| Method | F1 | BLEU-1 | ROUGE-L | ROUGE-2 | METEOR | SBERT Similarity |
| --- | --- | --- | --- | --- | --- | --- |
| LoCoMo | 2.55 | 3.13 | 2.75 | 0.90 | 1.64 | 15.76 |
| MemGPT | 1.18 | 1.07 | 0.96 | 0.42 | 0.95 | 8.54 |
| A-Mem | 3.45 | 3.37 | 3.54 | 3.60 | 2.05 | 19.51 |

Cost-Efficiency Analysis. A-Mem demonstrates significant computational and cost efficiency alongside strong performance. The system requires approximately 1,200 tokens per memory operation, achieving an 85-93% reduction in token usage compared to baseline methods (LoCoMo and MemGPT with 16,900 tokens) through our selective top-k retrieval mechanism. This substantial token reduction directly translates to lower operational costs, with each memory operation costing less than $0.0003 when using commercial API services—making large-scale deployments economically viable. Processing times average 5.4 seconds using GPT-4o-mini and only 1.1 seconds with locally-hosted Llama 3.2 1B on a single GPU. Despite requiring multiple LLM calls during memory processing, A-Mem maintains this cost-effective resource utilization while consistently outperforming baseline approaches across all foundation models tested, particularly doubling performance on complex multi-hop reasoning tasks. This balance of low computational cost and superior reasoning capability highlights A-Mem’s practical advantage for deployment in the real world.

Table 3: An ablation study was conducted to evaluate our proposed method against the GPT-4o-mini base model. The notation ’w/o’ indicates experiments where specific modules were removed. The abbreviations LG and ME denote the link generation module and memory evolution module, respectively.

<table><tbody><tr><td rowspan="3">Method</td><td colspan="10">Category</td></tr><tr><td colspan="2">Multi Hop</td><td colspan="2">Temporal</td><td colspan="2">Open Domain</td><td colspan="2">Single Hop</td><td colspan="2">Adversial</td></tr><tr><td>F1</td><td>BLEU-1</td><td>F1</td><td>BLEU-1</td><td>F1</td><td>BLEU-1</td><td>F1</td><td>BLEU-1</td><td>F1</td><td>BLEU-1</td></tr><tr><td>w/o LG & ME</td><td>9.65</td><td>7.09</td><td>24.55</td><td>19.48</td><td>7.77</td><td>6.70</td><td>13.28</td><td>10.30</td><td>15.32</td><td>18.02</td></tr><tr><td>w/o ME</td><td>21.35</td><td>15.13</td><td>31.24</td><td>27.31</td><td>10.13</td><td>10.85</td><td>39.17</td><td>34.70</td><td>44.16</td><td>45.33</td></tr><tr><td>A-Mem</td><td>27.02</td><td>20.09</td><td>45.85</td><td>36.67</td><td>12.14</td><td>12.00</td><td>44.65</td><td>37.06</td><td>50.03</td><td>49.47</td></tr></tbody></table>

### 4.4 Ablation Study

To evaluate the effectiveness of the Link Generation (LG) and Memory Evolution (ME) modules, we conduct the ablation study by systematically removing key components of our model. When both LG and ME modules are removed, the system exhibits substantial performance degradation, particularly in Multi Hop reasoning and Open Domain tasks. The system with only LG active (w/o ME) shows intermediate performance levels, maintaining significantly better results than the version without both modules, which demonstrates the fundamental importance of link generation in establishing memory connections. Our full model, A-Mem, consistently achieves the best performance across all evaluation categories, with particularly strong results in complex reasoning tasks. These results reveal that while the link generation module serves as a critical foundation for memory organization, the memory evolution module provides essential refinements to the memory structure. The ablation study validates our architectural design choices and highlights the complementary nature of these two modules in creating an effective memory system.

![Refer to caption](https://arxiv.org/html/2502.12110v11/x6.png)

(a) Multi Hop

### 4.5 Hyperparameter Analysis

We conducted extensive experiments to analyze the impact of the memory retrieval parameter k, which controls the number of relevant memories retrieved for each interaction. As shown in Figure 3, we evaluated performance across different k values (10, 20, 30, 40, 50) on five categories of tasks using GPT-4o-mini as our base model. The results reveal an interesting pattern: while increasing k generally leads to improved performance, this improvement gradually plateaus and sometimes slightly decreases at higher values. This trend is particularly evident in Multi Hop and Open Domain tasks. The observation suggests a delicate balance in memory retrieval - while larger k values provide richer historical context for reasoning, they may also introduce noise and challenge the model’s capacity to process longer sequences effectively. Our analysis indicates that moderate k values strike an optimal balance between context richness and information processing efficiency.

Table 4: Comparison of memory usage and retrieval time across different memory methods and scales.

<table><tbody><tr><td>Memory Size</td><td>Method</td><td>Memory Usage (MB)</td><td>Retrieval Time (<math><semantics><mrow><mi>μ</mi> <mo></mo><mtext>s</mtext></mrow> <annotation>\mu\text{s}</annotation></semantics></math>)</td></tr><tr><td rowspan="3">1,000</td><td>A-Mem</td><td>1.46</td><td>0.31 0.30</td></tr><tr><td>MemoryBank <sup><a href="#fn:39">39</a></sup></td><td>1.46</td><td>0.24 0.20</td></tr><tr><td>ReadAgent <sup><a href="#fn:17">17</a></sup></td><td>1.46</td><td>43.62 8.47</td></tr><tr><td rowspan="3">10,000</td><td>A-Mem</td><td>14.65</td><td>0.38 0.25</td></tr><tr><td>MemoryBank <sup><a href="#fn:39">39</a></sup></td><td>14.65</td><td>0.26 0.13</td></tr><tr><td>ReadAgent <sup><a href="#fn:17">17</a></sup></td><td>14.65</td><td>484.45 93.86</td></tr><tr><td rowspan="3">100,000</td><td>A-Mem</td><td>146.48</td><td>1.40 0.49</td></tr><tr><td>MemoryBank <sup><a href="#fn:39">39</a></sup></td><td>146.48</td><td>0.78 0.26</td></tr><tr><td>ReadAgent <sup><a href="#fn:17">17</a></sup></td><td>146.48</td><td>6,682.22 111.63</td></tr><tr><td rowspan="3">1,000,000</td><td>A-Mem</td><td>1464.84</td><td>3.70 0.74</td></tr><tr><td>MemoryBank <sup><a href="#fn:39">39</a></sup></td><td>1464.84</td><td>1.91 0.31</td></tr><tr><td>ReadAgent <sup><a href="#fn:17">17</a></sup></td><td>1464.84</td><td>120,069.68 1,673.39</td></tr></tbody></table>

### 4.6 Scaling Analysis

To evaluate storage costs with accumulating memory, we examined the relationship between storage size and retrieval time across our A-Mem system and two baseline approaches: MemoryBank [^39] and ReadAgent [^17]. We evaluated these three memory systems with identical memory content across four scale points, increasing the number of entries by a factor of 10 at each step (from 1,000 to 10,000, 100,000, and finally 1,000,000 entries). The experimental results reveal key insights about our A-Mem system’s scaling properties: In terms of space complexity, all three systems exhibit identical linear memory usage scaling ($O(N)$), as expected for vector-based retrieval systems. This confirms that A-Mem introduces no additional storage overhead compared to baseline approaches. For retrieval time, A-Mem demonstrates excellent efficiency with minimal increases as memory size grows. Even when scaling to 1 million memories, A-Mem’s retrieval time increases only from 0.31 $\mu\text{s}$ to 3.70 $\mu\text{s}$, representing exceptional performance. While MemoryBank shows slightly faster retrieval times, A-Mem maintains comparable performance while providing richer memory representations and functionality. Based on our space complexity and retrieval time analysis, we conclude that A-Mem’s retrieval mechanisms maintain excellent efficiency even at large scales. The minimal growth in retrieval time across memory sizes addresses concerns about efficiency in large-scale memory systems, demonstrating that A-Mem provides a highly scalable solution for long-term conversation management. This unique combination of efficiency, scalability, and enhanced memory capabilities positions A-Mem as a significant advancement in building powerful and long-term memory mechanism for LLM Agents.

### 4.7 Memory Analysis

We present the t-SNE visualization in Figure 4 of memory embeddings to demonstrate the structural advantages of our agentic memory system. Analyzing two dialogues sampled from long-term conversations in LoCoMo [^22], we observe that A-Mem (shown in blue) consistently exhibits more coherent clustering patterns compared to the baseline system (shown in red). This structural organization is particularly evident in Dialogue 2, where well-defined clusters emerge in the central region, providing empirical evidence for the effectiveness of our memory evolution mechanism and contextual description generation. In contrast, the baseline memory embeddings display a more dispersed distribution, demonstrating that memories lack structural organization without our link generation and memory evolution components. These visualization results validate that A-Mem can autonomously maintain meaningful memory structures through dynamic evolution and linking mechanisms. More results can be seen in Appendix A.4.

![Refer to caption](https://arxiv.org/html/2502.12110v11/x11.png)

(a) Dialogue 1

## 5 Conclusions

In this work, we introduced A-Mem, a novel agentic memory system that enables LLM agents to dynamically organize and evolve their memories without relying on predefined structures. Drawing inspiration from the Zettelkasten method, our system creates an interconnected knowledge network through dynamic indexing and linking mechanisms that adapt to diverse real-world tasks. The system’s core architecture features autonomous generation of contextual descriptions for new memories and intelligent establishment of connections with existing memories based on shared attributes. Furthermore, our approach enables continuous evolution of historical memories by incorporating new experiences and developing higher-order attributes through ongoing interactions. Through extensive empirical evaluation across six foundation models, we demonstrated that A-Mem achieves superior performance compared to existing state-of-the-art baselines in long-term conversational tasks. Visualization analysis further validates the effectiveness of our memory organization approach. These results suggest that agentic memory systems can significantly enhance LLM agents’ ability to utilize long-term knowledge in complex environments.

## 6 Limitations

While our agentic memory system achieves promising results, we acknowledge several areas for potential future exploration. First, although our system dynamically organizes memories, the quality of these organizations may still be influenced by the inherent capabilities of the underlying language models. Different LLMs might generate slightly different contextual descriptions or establish varying connections between memories. Additionally, while our current implementation focuses on text-based interactions, future work could explore extending the system to handle multimodal information, such as images or audio, which could provide richer contextual representations.

## References

## APPENDIX

## Appendix A Experiment

### A.1 Detailed Baselines Introduction

LoCoMo [^22] takes a direct approach by leveraging foundation models without memory mechanisms for question answering tasks. For each query, it incorporates the complete preceding conversation and questions into the prompt, evaluating the model’s reasoning capabilities.

ReadAgent [^17] tackles long-context document processing through a sophisticated three-step methodology: it begins with episode pagination to segment content into manageable chunks, followed by memory gisting to distill each page into concise memory representations, and concludes with interactive look-up to retrieve pertinent information as needed.

MemoryBank [^39] introduces an innovative memory management system that maintains and efficiently retrieves historical interactions. The system features a dynamic memory updating mechanism based on the Ebbinghaus Forgetting Curve theory, which intelligently adjusts memory strength according to time and significance. Additionally, it incorporates a user portrait building system that progressively refines its understanding of user personality through continuous interaction analysis.

MemGPT [^25] presents a novel virtual context management system drawing inspiration from traditional operating systems’ memory hierarchies. The architecture implements a dual-tier structure: a main context (analogous to RAM) that provides immediate access during LLM inference, and an external context (analogous to disk storage) that maintains information beyond the fixed context window.

### A.2 Evaluation Metric

The F1 score represents the harmonic mean of precision and recall, offering a balanced metric that combines both measures into a single value. This metric is particularly valuable when we need to balance between complete and accurate responses:

$$
\text{F1}=2\cdot\frac{\text{precision}\cdot\text{recall}}{\text{precision}+\text{recall}}
$$

where

$$
\text{precision}=\frac{\text{true positives}}{\text{true positives}+\text{false positives}}
$$
 
$$
\text{recall}=\frac{\text{true positives}}{\text{true positives}+\text{false negatives}}
$$

In question-answering systems, the F1 score serves a crucial role in evaluating exact matches between predicted and reference answers. This is especially important for span-based QA tasks, where systems must identify precise text segments while maintaining comprehensive coverage of the answer.

BLEU-1 [^26] provides a method for evaluating the precision of unigram matches between system outputs and reference texts:

$$
\text{BLEU-1}=BP\cdot\exp(\tsum\slimits@_{n=1}^{1}w_{n}\log p_{n})
$$

where

$$
BP=\begin{cases}1&\text{if }c>r\\
e^{1-r/c}&\text{if }c\leq r\end{cases}
$$
 
$$
p_{n}=\frac{\tsum\slimits@_{i}\tsum\slimits@_{k}\min(h_{ik},m_{ik})}{\tsum\slimits@_{i}\tsum\slimits@_{k}h_{ik}}
$$

Here, $c$ is candidate length, $r$ is reference length, $h_{ik}$ is the count of n-gram i in candidate k, and $m_{ik}$ is the maximum count in any reference. In QA, BLEU-1 evaluates the lexical precision of generated answers, particularly useful for generative QA systems where exact matching might be too strict.

ROUGE-L [^19] measures the longest common subsequence between the generated and reference texts.

$$
\text{ROUGE-L}=\frac{(1+\beta^{2})R_{l}P_{l}}{R_{l}+\beta^{2}P_{l}}
$$
 
$$
R_{l}=\frac{\text{LCS}(X,Y)}{|X|}
$$
 
$$
P_{l}=\frac{\text{LCS}(X,Y)}{|Y|}
$$

where $X$ is reference text, $Y$ is candidate text, and LCS is the Longest Common Subsequence.

ROUGE-2 [^19] calculates the overlap of bigrams between the generated and reference texts.

$$
\text{ROUGE-2}=\frac{\tsum\slimits@_{\text{bigram}\in\text{ref}}\min(\text{Count}_{\text{ref}}(\text{bigram}),\text{Count}_{\text{cand}}(\text{bigram}))}{\tsum\slimits@_{\text{bigram}\in\text{ref}}\text{Count}_{\text{ref}}(\text{bigram})}
$$

Both ROUGE-L and ROUGE-2 are particularly useful for evaluating the fluency and coherence of generated answers, with ROUGE-L focusing on sequence matching and ROUGE-2 on local word order.

METEOR [^5] computes a score based on aligned unigrams between the candidate and reference texts, considering synonyms and paraphrases.

$$
\text{METEOR}=F_{\text{mean}}\cdot(1-\text{Penalty})
$$
 
$$
F_{\text{mean}}=\frac{10P\cdot R}{R+9P}
$$
 
$$
\text{Penalty}=0.5\cdot(\frac{\text{ch}}{m})^{3}
$$

where $P$ is precision, $R$ is recall, ch is number of chunks, and $m$ is number of matched unigrams. METEOR is valuable for QA evaluation as it considers semantic similarity beyond exact matching, making it suitable for evaluating paraphrased answers.

SBERT Similarity [^27] measures the semantic similarity between two texts using sentence embeddings.

$$
\text{SBERT\_Similarity}=\cos(\text{SBERT}(x),\text{SBERT}(y))
$$
 
$$
\cos(a,b)=\frac{a\cdot b}{\|a\|\|b\|}
$$

SBERT($x$ ) represents the sentence embedding of text. SBERT Similarity is particularly useful for evaluating semantic understanding in QA systems, as it can capture meaning similarities even when the lexical overlap is low.

Table 5: Experimental results on LoCoMo dataset of QA tasks across five categories (Multi Hop, Temporal, Open Domain, Single Hop, and Adversial) using different methods. Results are reported in ROUGE-2 and ROUGE-L scores, abbreviated to RGE-2 and RGE-L. The best performance is marked in bold, and our proposed method A-Mem (highlighted in gray) demonstrates competitive performance across six foundation language models.

<table><tbody><tr><td colspan="2" rowspan="3">Model</td><td rowspan="3">Method</td><td colspan="10">Category</td></tr><tr><td colspan="2">Multi Hop</td><td colspan="2">Temporal</td><td colspan="2">Open Domain</td><td colspan="2">Single Hop</td><td colspan="2">Adversial</td></tr><tr><td>RGE-2</td><td>RGE-L</td><td>RGE-2</td><td>RGE-L</td><td>RGE-2</td><td>RGE-L</td><td>RGE-2</td><td>RGE-L</td><td>RGE-2</td><td>RGE-L</td></tr><tr><td rowspan="10"><p></p><p>GPT</p><p></p></td><td rowspan="5"><p></p><p>4o-mini</p><p></p></td><td>LoCoMo</td><td>9.64</td><td>23.92</td><td>2.01</td><td>18.09</td><td>3.40</td><td>11.58</td><td>26.48</td><td>40.20</td><td>60.46</td><td>69.59</td></tr><tr><td>ReadAgent</td><td>2.47</td><td>9.45</td><td>0.95</td><td>13.12</td><td>0.55</td><td>5.76</td><td>2.99</td><td>9.92</td><td>6.66</td><td>9.79</td></tr><tr><td>MemoryBank</td><td>1.18</td><td>5.43</td><td>0.52</td><td>9.64</td><td>0.97</td><td>5.77</td><td>1.64</td><td>6.63</td><td>4.55</td><td>7.35</td></tr><tr><td>MemGPT</td><td>10.58</td><td>25.60</td><td>4.76</td><td>25.22</td><td>0.76</td><td>9.14</td><td>28.44</td><td>42.24</td><td>36.62</td><td>43.75</td></tr><tr><td>A-Mem</td><td>10.61</td><td>25.86</td><td>21.39</td><td>44.27</td><td>3.42</td><td>12.09</td><td>29.50</td><td>45.18</td><td>42.62</td><td>50.04</td></tr><tr><td rowspan="5"><p></p><p>4o</p><p></p></td><td>LoCoMo</td><td>11.53</td><td>30.65</td><td>1.68</td><td>8.17</td><td>3.21</td><td>16.33</td><td>45.42</td><td>63.86</td><td>45.13</td><td>52.67</td></tr><tr><td>ReadAgent</td><td>3.91</td><td>14.36</td><td>0.43</td><td>3.96</td><td>0.52</td><td>8.58</td><td>4.75</td><td>13.41</td><td>4.24</td><td>6.81</td></tr><tr><td>MemoryBank</td><td>1.84</td><td>7.36</td><td>0.36</td><td>2.29</td><td>2.13</td><td>6.85</td><td>3.02</td><td>9.35</td><td>1.22</td><td>4.41</td></tr><tr><td>MemGPT</td><td>11.55</td><td>30.18</td><td>4.66</td><td>15.83</td><td>3.27</td><td>14.02</td><td>43.27</td><td>62.75</td><td>28.72</td><td>35.08</td></tr><tr><td>A-Mem</td><td>12.76</td><td>31.71</td><td>9.82</td><td>25.04</td><td>6.09</td><td>16.63</td><td>33.67</td><td>50.31</td><td>30.31</td><td>36.34</td></tr><tr><td rowspan="10"><p></p><p>Qwen2.5</p><p></p></td><td rowspan="5"><p></p><p>1.5b</p><p></p></td><td>LoCoMo</td><td>1.39</td><td>9.24</td><td>0.00</td><td>4.68</td><td>3.42</td><td>10.59</td><td>3.25</td><td>11.15</td><td>35.10</td><td>43.61</td></tr><tr><td>ReadAgent</td><td>0.74</td><td>7.14</td><td>0.10</td><td>2.81</td><td>3.05</td><td>12.63</td><td>1.47</td><td>7.88</td><td>20.73</td><td>27.82</td></tr><tr><td>MemoryBank</td><td>1.51</td><td>11.18</td><td>0.14</td><td>5.39</td><td>1.80</td><td>8.44</td><td>5.07</td><td>13.72</td><td>29.24</td><td>36.95</td></tr><tr><td>MemGPT</td><td>1.16</td><td>11.35</td><td>0.00</td><td>7.88</td><td>2.87</td><td>14.62</td><td>2.18</td><td>9.82</td><td>23.96</td><td>31.69</td></tr><tr><td>A-Mem</td><td>4.88</td><td>17.94</td><td>5.88</td><td>27.23</td><td>3.44</td><td>16.87</td><td>12.32</td><td>24.38</td><td>36.32</td><td>46.60</td></tr><tr><td rowspan="5"><p></p><p>3b</p><p></p></td><td>LoCoMo</td><td>0.49</td><td>4.83</td><td>0.14</td><td>3.20</td><td>1.31</td><td>5.38</td><td>1.97</td><td>6.98</td><td>12.66</td><td>17.10</td></tr><tr><td>ReadAgent</td><td>0.08</td><td>4.08</td><td>0.00</td><td>1.96</td><td>1.26</td><td>6.19</td><td>0.73</td><td>4.34</td><td>7.35</td><td>10.64</td></tr><tr><td>MemoryBank</td><td>0.43</td><td>3.76</td><td>0.05</td><td>1.61</td><td>0.24</td><td>6.32</td><td>1.03</td><td>4.22</td><td>9.55</td><td>13.41</td></tr><tr><td>MemGPT</td><td>0.69</td><td>5.55</td><td>0.05</td><td>3.17</td><td>1.90</td><td>7.90</td><td>2.05</td><td>7.32</td><td>10.46</td><td>14.39</td></tr><tr><td>A-Mem</td><td>2.91</td><td>12.42</td><td>8.11</td><td>27.74</td><td>1.51</td><td>7.51</td><td>8.80</td><td>17.57</td><td>21.39</td><td>27.98</td></tr><tr><td rowspan="10"><p></p><p>Llama 3.2</p><p></p></td><td rowspan="5"><p></p><p>1b</p><p></p></td><td>LoCoMo</td><td>2.51</td><td>11.48</td><td>0.44</td><td>8.25</td><td>1.69</td><td>13.06</td><td>2.94</td><td>13.00</td><td>39.85</td><td>52.74</td></tr><tr><td>ReadAgent</td><td>0.53</td><td>6.49</td><td>0.00</td><td>4.62</td><td>5.47</td><td>14.29</td><td>1.19</td><td>8.03</td><td>34.52</td><td>45.55</td></tr><tr><td>MemoryBank</td><td>2.96</td><td>13.57</td><td>0.23</td><td>10.53</td><td>4.01</td><td>18.38</td><td>6.41</td><td>17.66</td><td>41.15</td><td>53.31</td></tr><tr><td>MemGPT</td><td>1.82</td><td>9.91</td><td>0.06</td><td>6.56</td><td>2.13</td><td>11.36</td><td>2.00</td><td>10.37</td><td>38.59</td><td>50.31</td></tr><tr><td>A-Mem</td><td>4.82</td><td>19.31</td><td>1.84</td><td>20.47</td><td>5.99</td><td>18.49</td><td>14.82</td><td>29.78</td><td>46.76</td><td>60.23</td></tr><tr><td rowspan="5"><p></p><p>3b</p><p></p></td><td>LoCoMo</td><td>0.98</td><td>7.22</td><td>0.03</td><td>4.45</td><td>2.36</td><td>11.39</td><td>2.85</td><td>8.45</td><td>25.47</td><td>30.26</td></tr><tr><td>ReadAgent</td><td>2.47</td><td>1.78</td><td>3.01</td><td>3.01</td><td>5.07</td><td>5.22</td><td>3.25</td><td>2.51</td><td>15.78</td><td>14.01</td></tr><tr><td>MemoryBank</td><td>1.83</td><td>6.96</td><td>0.25</td><td>3.41</td><td>0.43</td><td>4.43</td><td>2.73</td><td>7.83</td><td>14.64</td><td>18.59</td></tr><tr><td>MemGPT</td><td>0.72</td><td>5.39</td><td>0.11</td><td>2.85</td><td>0.61</td><td>5.74</td><td>1.45</td><td>4.42</td><td>16.62</td><td>21.47</td></tr><tr><td>A-Mem</td><td>6.02</td><td>17.62</td><td>7.93</td><td>27.97</td><td>5.38</td><td>13.00</td><td>16.89</td><td>28.55</td><td>35.48</td><td>42.25</td></tr></tbody></table>

Table 6: Experimental results on LoCoMo dataset of QA tasks across five categories (Multi Hop, Temporal, Open Domain, Single Hop, and Adversial) using different methods. Results are reported in METEOR and SBERT Similarity scores, abbreviated to ME and SBERT. The best performance is marked in bold, and our proposed method A-Mem (highlighted in gray) demonstrates competitive performance across six foundation language models.

<table><tbody><tr><td colspan="2" rowspan="3">Model</td><td rowspan="3">Method</td><td colspan="10">Category</td></tr><tr><td colspan="2">Multi Hop</td><td colspan="2">Temporal</td><td colspan="2">Open Domain</td><td colspan="2">Single Hop</td><td colspan="2">Adversial</td></tr><tr><td>ME</td><td>SBERT</td><td>ME</td><td>SBERT</td><td>ME</td><td>SBERT</td><td>ME</td><td>SBERT</td><td>ME</td><td>SBERT</td></tr><tr><td rowspan="10"><p></p><p>GPT</p><p></p></td><td rowspan="5"><p></p><p>4o-mini</p><p></p></td><td>LoCoMo</td><td>15.81</td><td>47.97</td><td>7.61</td><td>52.30</td><td>8.16</td><td>35.00</td><td>40.42</td><td>57.78</td><td>63.28</td><td>71.93</td></tr><tr><td>ReadAgent</td><td>5.46</td><td>28.67</td><td>4.76</td><td>45.07</td><td>3.69</td><td>26.72</td><td>8.01</td><td>26.78</td><td>8.38</td><td>15.20</td></tr><tr><td>MemoryBank</td><td>3.42</td><td>21.71</td><td>4.07</td><td>37.58</td><td>4.21</td><td>23.71</td><td>5.81</td><td>20.76</td><td>6.24</td><td>13.00</td></tr><tr><td>MemGPT</td><td>15.79</td><td>49.33</td><td>13.25</td><td>61.53</td><td>4.59</td><td>32.77</td><td>41.40</td><td>58.19</td><td>39.16</td><td>47.24</td></tr><tr><td>A-Mem</td><td>16.36</td><td>49.46</td><td>23.43</td><td>70.49</td><td>8.36</td><td>38.48</td><td>42.32</td><td>59.38</td><td>45.64</td><td>53.26</td></tr><tr><td rowspan="5"><p></p><p>4o</p><p></p></td><td>LoCoMo</td><td>16.34</td><td>53.82</td><td>7.21</td><td>32.15</td><td>8.98</td><td>43.72</td><td>53.39</td><td>73.40</td><td>47.72</td><td>56.09</td></tr><tr><td>ReadAgent</td><td>7.86</td><td>37.41</td><td>3.76</td><td>26.22</td><td>4.42</td><td>30.75</td><td>9.36</td><td>31.37</td><td>5.47</td><td>12.34</td></tr><tr><td>MemoryBank</td><td>3.22</td><td>26.23</td><td>2.29</td><td>23.49</td><td>4.18</td><td>24.89</td><td>6.64</td><td>23.90</td><td>2.93</td><td>10.01</td></tr><tr><td>MemGPT</td><td>16.64</td><td>55.12</td><td>12.68</td><td>35.93</td><td>7.78</td><td>37.91</td><td>52.14</td><td>72.83</td><td>31.15</td><td>39.08</td></tr><tr><td>A-Mem</td><td>17.53</td><td>55.96</td><td>13.10</td><td>45.40</td><td>10.62</td><td>38.87</td><td>41.93</td><td>62.47</td><td>32.34</td><td>40.11</td></tr><tr><td rowspan="10"><p></p><p>Qwen2.5</p><p></p></td><td rowspan="5"><p></p><p>1.5b</p><p></p></td><td>LoCoMo</td><td>4.99</td><td>32.23</td><td>2.86</td><td>34.03</td><td>5.89</td><td>35.61</td><td>8.57</td><td>29.47</td><td>40.53</td><td>50.49</td></tr><tr><td>ReadAgent</td><td>3.67</td><td>28.20</td><td>1.88</td><td>27.27</td><td>8.97</td><td>35.13</td><td>5.52</td><td>26.33</td><td>24.04</td><td>34.12</td></tr><tr><td>MemoryBank</td><td>5.57</td><td>35.40</td><td>2.80</td><td>32.47</td><td>4.27</td><td>33.85</td><td>10.59</td><td>32.16</td><td>32.93</td><td>42.83</td></tr><tr><td>MemGPT</td><td>5.40</td><td>35.64</td><td>2.35</td><td>39.04</td><td>7.68</td><td>40.36</td><td>7.07</td><td>30.16</td><td>27.24</td><td>40.63</td></tr><tr><td>A-Mem</td><td>9.49</td><td>43.49</td><td>11.92</td><td>61.65</td><td>9.11</td><td>42.58</td><td>19.69</td><td>41.93</td><td>40.64</td><td>52.44</td></tr><tr><td rowspan="5"><p></p><p>3b</p><p></p></td><td>LoCoMo</td><td>2.00</td><td>24.37</td><td>1.92</td><td>25.24</td><td>3.45</td><td>25.38</td><td>6.00</td><td>21.28</td><td>16.67</td><td>23.14</td></tr><tr><td>ReadAgent</td><td>1.78</td><td>21.10</td><td>1.69</td><td>20.78</td><td>4.43</td><td>25.15</td><td>3.37</td><td>18.20</td><td>10.46</td><td>17.39</td></tr><tr><td>MemoryBank</td><td>2.37</td><td>17.81</td><td>2.22</td><td>21.93</td><td>3.86</td><td>20.65</td><td>3.99</td><td>16.26</td><td>15.49</td><td>20.77</td></tr><tr><td>MemGPT</td><td>3.74</td><td>24.31</td><td>2.25</td><td>27.67</td><td>6.44</td><td>29.59</td><td>6.24</td><td>22.40</td><td>13.19</td><td>20.83</td></tr><tr><td>A-Mem</td><td>6.25</td><td>33.72</td><td>14.04</td><td>62.54</td><td>6.56</td><td>30.60</td><td>15.98</td><td>33.98</td><td>27.36</td><td>33.72</td></tr><tr><td rowspan="10"><p></p><p>Llama 3.2</p><p></p></td><td rowspan="5"><p></p><p>1b</p><p></p></td><td>LoCoMo</td><td>5.77</td><td>38.02</td><td>3.38</td><td>45.44</td><td>6.20</td><td>42.69</td><td>9.33</td><td>34.19</td><td>46.79</td><td>60.74</td></tr><tr><td>ReadAgent</td><td>2.97</td><td>29.26</td><td>1.31</td><td>26.45</td><td>7.13</td><td>39.19</td><td>5.36</td><td>26.44</td><td>42.39</td><td>54.35</td></tr><tr><td>MemoryBank</td><td>6.77</td><td>39.33</td><td>4.43</td><td>45.63</td><td>7.76</td><td>42.81</td><td>13.01</td><td>37.32</td><td>50.43</td><td>60.81</td></tr><tr><td>MemGPT</td><td>5.10</td><td>32.99</td><td>2.54</td><td>41.81</td><td>3.26</td><td>35.99</td><td>6.62</td><td>30.68</td><td>45.00</td><td>61.33</td></tr><tr><td>A-Mem</td><td>9.01</td><td>45.16</td><td>7.50</td><td>54.79</td><td>8.30</td><td>43.42</td><td>22.46</td><td>47.07</td><td>53.72</td><td>68.00</td></tr><tr><td rowspan="5"><p></p><p>3b</p><p></p></td><td>LoCoMo</td><td>3.69</td><td>27.94</td><td>2.96</td><td>20.40</td><td>6.46</td><td>32.17</td><td>6.58</td><td>22.92</td><td>29.02</td><td>35.74</td></tr><tr><td>ReadAgent</td><td>1.21</td><td>17.40</td><td>2.33</td><td>12.02</td><td>3.39</td><td>19.63</td><td>2.46</td><td>14.63</td><td>14.37</td><td>21.25</td></tr><tr><td>MemoryBank</td><td>3.84</td><td>25.06</td><td>2.73</td><td>13.65</td><td>3.05</td><td>21.08</td><td>6.35</td><td>22.02</td><td>17.14</td><td>24.39</td></tr><tr><td>MemGPT</td><td>2.78</td><td>22.06</td><td>2.21</td><td>14.97</td><td>3.63</td><td>23.18</td><td>3.47</td><td>17.81</td><td>20.50</td><td>26.87</td></tr><tr><td>A-Mem</td><td>9.74</td><td>39.32</td><td>13.19</td><td>59.70</td><td>8.09</td><td>32.27</td><td>24.30</td><td>42.86</td><td>39.74</td><td>46.76</td></tr></tbody></table>

Table 7: Experimental results on LoCoMo dataset of QA tasks across five categories (Multi Hop, Temporal, Open Domain, Single Hop, and Adversial) using different methods. Results are reported in F1 and BLEU-1 (%) scores with different foundation models.

<table><tbody><tr><td rowspan="3">Method</td><td colspan="10">Category</td></tr><tr><td colspan="2">Multi Hop</td><td colspan="2">Temporal</td><td colspan="2">Open Domain</td><td colspan="2">Single Hop</td><td colspan="2">Adversial</td></tr><tr><td>F1</td><td>BLEU-1</td><td>F1</td><td>BLEU-1</td><td>F1</td><td>BLEU-1</td><td>F1</td><td>BLEU-1</td><td>F1</td><td>BLEU-1</td></tr><tr><td colspan="11">DeepSeek-R1-32B</td></tr><tr><td>LoCoMo</td><td>8.58</td><td>6.48</td><td>4.79</td><td>4.35</td><td>12.96</td><td>12.52</td><td>10.72</td><td>8.20</td><td>21.40</td><td>20.23</td></tr><tr><td>MemGPT</td><td>8.28</td><td>6.25</td><td>5.45</td><td>4.97</td><td>10.97</td><td>9.09</td><td>11.34</td><td>9.03</td><td>30.77</td><td>29.23</td></tr><tr><td>A-Mem</td><td>15.02</td><td>10.64</td><td>14.64</td><td>11.01</td><td>14.81</td><td>12.82</td><td>15.37</td><td>12.30</td><td>27.92</td><td>27.19</td></tr><tr><td colspan="11">Claude 3.0 Haiku</td></tr><tr><td>LoCoMo</td><td>4.56</td><td>3.33</td><td>0.82</td><td>0.59</td><td>2.86</td><td>3.22</td><td>3.56</td><td>3.24</td><td>3.46</td><td>3.42</td></tr><tr><td>MemGPT</td><td>7.65</td><td>6.36</td><td>1.65</td><td>1.26</td><td>7.41</td><td>6.64</td><td>8.60</td><td>7.29</td><td>7.66</td><td>7.37</td></tr><tr><td>A-Mem</td><td>19.28</td><td>14.69</td><td>16.65</td><td>12.23</td><td>11.85</td><td>9.61</td><td>34.72</td><td>30.05</td><td>35.99</td><td>34.87</td></tr><tr><td colspan="11">Claude 3.5 Haiku</td></tr><tr><td>LoCoMo</td><td>11.34</td><td>8.21</td><td>3.29</td><td>2.69</td><td>3.79</td><td>3.58</td><td>14.01</td><td>12.57</td><td>7.37</td><td>7.12</td></tr><tr><td>MemGPT</td><td>8.27</td><td>6.55</td><td>3.99</td><td>2.76</td><td>4.71</td><td>4.48</td><td>16.52</td><td>14.89</td><td>5.64</td><td>5.45</td></tr><tr><td>A-Mem</td><td>29.70</td><td>23.19</td><td>31.54</td><td>27.53</td><td>11.42</td><td>9.47</td><td>42.60</td><td>37.41</td><td>13.65</td><td>12.71</td></tr></tbody></table>

### A.3 Comparison Results

Our comprehensive evaluation using ROUGE-2, ROUGE-L, METEOR, and SBERT metrics demonstrates that A-Mem achieves superior performance while maintaining remarkable computational efficiency. Through extensive empirical testing across various model sizes and task categories, we have established A-Mem as a more effective approach compared to existing baselines, supported by several compelling findings. In our analysis of non-GPT models, specifically Qwen2.5 and Llama 3.2, A-Mem consistently outperforms all baseline approaches across all metrics. The Multi-Hop category showcases particularly striking results, where Qwen2.5-15b with A-Mem achieves a ROUGE-L score of 27.23, dramatically surpassing LoComo’s 4.68 and ReadAgent’s 2.81 - representing a nearly six-fold improvement. This pattern of superiority extends consistently across METEOR and SBERT scores. When examining GPT-based models, our results reveal an interesting pattern. While LoComo and MemGPT demonstrate strong capabilities in Open Domain and Adversarial tasks, A-Mem shows remarkable superiority in Multi-Hop reasoning tasks. Using GPT-4o-mini, A-Mem achieves a ROUGE-L score of 44.27 in Multi-Hop tasks, more than doubling LoComo’s 18.09. This significant advantage maintains consistency across other metrics, with METEOR scores of 23.43 versus 7.61 and SBERT scores of 70.49 versus 52.30. The significance of these results is amplified by A-Mem’s exceptional computational efficiency. Our approach requires only 1,200-2,500 tokens, compared to the substantial 16,900 tokens needed by LoComo and MemGPT. This efficiency stems from two key architectural innovations: First, our novel agentic memory architecture creates interconnected memory networks through atomic notes with rich contextual descriptions, enabling more effective capture and utilization of information relationships. Second, our selective top-k retrieval mechanism facilitates dynamic memory evolution and structured organization. The effectiveness of these innovations is particularly evident in complex reasoning tasks, as demonstrated by the consistently strong Multi-Hop performance across all evaluation metrics. Besides, we also show the experimental results with different foundational models including DeepSeek-R1-32B [^11], Claude 3.0 Haiku [^2] and Claude 3.5 Haiku [^3].

### A.4 Memory Analysis

In addition to the memory visualizations of the first two dialogues shown in the main text, we present additional visualizations in Fig.5 that demonstrate the structural advantages of our agentic memory system. Through analysis of two dialogues sampled from long-term conversations in LoCoMo [^22], we observe that A-Mem (shown in blue) consistently produces more coherent clustering patterns compared to the baseline system (shown in red). This structural organization is particularly evident in Dialogue 2, where distinct clusters emerge in the central region, providing empirical support for the effectiveness of our memory evolution mechanism and contextual description generation. In contrast, the baseline memory embeddings exhibit a more scattered distribution, indicating that memories lack structural organization without our link generation and memory evolution components. These visualizations validate that A-Mem can autonomously maintain meaningful memory structures through its dynamic evolution and linking mechanisms.

![Refer to caption](https://arxiv.org/html/2502.12110v11/x13.png)

Figure 5: T-SNE Visualization of Memory Embeddings Showing More Organized Distribution with A-Mem (blue) Compared to Base Memory (red) Across Different Dialogues. Base Memory represents without link generation and memory evolution.

### A.5 Hyperparameters setting

All hyperparameter k values are presented in Table 8. For models that have already achieved state-of-the-art (SOTA) performance with k=10, we maintain this value without further tuning.

Table 8: Selection of k values in retriever across specific categories and model choices.

| Model | Multi Hop | Temporal | Open Domain | Single Hop | Adversial |
| --- | --- | --- | --- | --- | --- |
| GPT-4o-mini | 40 | 40 | 50 | 50 | 40 |
| GPT-4o | 40 | 40 | 50 | 50 | 40 |
| Qwen2.5-1.5b | 10 | 10 | 10 | 10 | 10 |
| Qwen2.5-3b | 10 | 10 | 50 | 10 | 10 |
| Llama3.2-1b | 10 | 10 | 10 | 10 | 10 |
| Llama3.2-3b | 10 | 20 | 10 | 10 | 10 |

## Appendix B Prompt Templates and Examples

### B.1 Prompt Template of Note Construction

<svg height="372.33" id="A2.SS1.p1.pic1" overflow="visible" version="1.1" viewBox="0 0 477.38 372.33" width="477.38"><g fill="#000000" stroke="#000000" stroke-width="0.4pt" style="--ltx-stroke-color:#000000;--ltx-fill-color:#000000;" transform="translate(0,372.33) matrix(1 0 0 -1 0 0)"><g fill="#000000" fill-opacity="1.0" style="--ltx-fill-color:#000000;"><path d="M 0 17.72 L 0 354.61 C 0 364.4 7.93 372.33 17.72 372.33 L 459.66 372.33 C 469.44 372.33 477.38 364.4 477.38 354.61 L 477.38 17.72 C 477.38 7.93 469.44 0 459.66 0 L 17.72 0 C 7.93 0 0 7.93 0 17.72 Z" style="stroke:none"></path></g><g fill="#F9F9F9" fill-opacity="1.0" style="--ltx-fill-color:#F9F9F9;"><path d="M 1.97 17.72 L 1.97 354.61 C 1.97 363.31 9.02 370.36 17.72 370.36 L 459.66 370.36 C 468.36 370.36 475.41 363.31 475.41 354.61 L 475.41 17.72 C 475.41 9.02 468.36 1.97 459.66 1.97 L 17.72 1.97 C 9.02 1.97 1.97 9.02 1.97 17.72 Z" style="stroke:none"></path></g><g fill-opacity="1.0" transform="matrix(1.0 0.0 0.0 1.0 21.65 16.85)"><foreignObject color="#000000" height="344.77" overflow="visible" style="--ltx-fg-color:#000000;--fo_width :31.37em;--fo_height:24.69em;--fo_depth :0.22em;" transform="matrix(1 0 0 -1 0 341.7)" width="434.07"><span style="width:31.37em;"><span id="A2.SS1.p1.pic1.p1">The prompt template in Note Construction: <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline" data-latex="P_{s1}"><semantics><msub><mi>P</mi> <mrow><mi>s</mi> <mo lspace="0em" rspace="0em"></mo><mn>1</mn></mrow></msub> <annotation encoding="application/x-tex">P_{s1}</annotation></semantics></math><br>Generate a structured analysis of the following content by:<br>1. Identifying the most salient keywords (focus on nouns, verbs, and key concepts)<br>2. Extracting core themes and contextual elements<br>3. Creating relevant categorical tags<br>Format the response as a JSON object:<br>{<br>"keywords": [ // several specific, distinct keywords that capture key concepts and terminology // Order from most to least important // Don’t include keywords that are the name of the speaker or time // At least three keywords, but don’t be too redundant. ],<br>"context": // one sentence summarizing: // - Main topic/domain // - Key arguments/points // - Intended audience/purpose,<br>"tags": [ // several broad categories/themes for classification // Include domain, format, and type tags // At least three tags, but don’t be too redundant. ]<br>}<br>Content for analysis:</span></span></foreignObject></g></g></svg>

### B.2 Prompt Template of Link Generation

<svg height="236.42" id="A2.SS2.p1.pic1" overflow="visible" version="1.1" viewBox="0 0 477.38 236.42" width="477.38"><g fill="#000000" stroke="#000000" stroke-width="0.4pt" style="--ltx-stroke-color:#000000;--ltx-fill-color:#000000;" transform="translate(0,236.42) matrix(1 0 0 -1 0 0)"><g fill="#000000" fill-opacity="1.0" style="--ltx-fill-color:#000000;"><path d="M 0 17.72 L 0 218.7 C 0 228.49 7.93 236.42 17.72 236.42 L 459.66 236.42 C 469.44 236.42 477.38 228.49 477.38 218.7 L 477.38 17.72 C 477.38 7.93 469.44 0 459.66 0 L 17.72 0 C 7.93 0 0 7.93 0 17.72 Z" style="stroke:none"></path></g><g fill="#F9F9F9" fill-opacity="1.0" style="--ltx-fill-color:#F9F9F9;"><path d="M 1.97 17.72 L 1.97 218.7 C 1.97 227.4 9.02 234.45 17.72 234.45 L 459.66 234.45 C 468.36 234.45 475.41 227.4 475.41 218.7 L 475.41 17.72 C 475.41 9.02 468.36 1.97 459.66 1.97 L 17.72 1.97 C 9.02 1.97 1.97 9.02 1.97 17.72 Z" style="stroke:none"></path></g><g fill-opacity="1.0" transform="matrix(1.0 0.0 0.0 1.0 21.65 13.78)"><foreignObject color="#000000" height="208.86" overflow="visible" style="--ltx-fg-color:#000000;--fo_width :31.37em;--fo_height:15.09em;--fo_depth :0em;" transform="matrix(1 0 0 -1 0 208.86)" width="434.07"><span style="width:31.37em;"><span id="A2.SS2.p1.pic1.p1">The prompt template in Link Generation: <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline" data-latex="P_{s2}"><semantics><msub><mi>P</mi> <mrow><mi>s</mi> <mo lspace="0em" rspace="0em"></mo><mn>2</mn></mrow></msub> <annotation encoding="application/x-tex">P_{s2}</annotation></semantics></math><br>You are an AI memory evolution agent responsible for managing and evolving a knowledge base.<br>Analyze the the new memory note according to keywords and context, also with their several nearest neighbors memory.<br>The new memory context:<br>{context} content: {content}<br>keywords: {keywords}<br>The nearest neighbors memories: {nearest_neighbors_memories}<br>Based on this information, determine:<br>Should this memory be evolved? Consider its relationships with other memories.</span></span></foreignObject></g></g></svg>

### B.3 Prompt Template of Memory Evolution

<svg height="654.99" id="A2.SS3.p1.pic1" overflow="visible" version="1.1" viewBox="0 0 477.38 654.99" width="477.38"><g fill="#000000" stroke="#000000" stroke-width="0.4pt" style="--ltx-stroke-color:#000000;--ltx-fill-color:#000000;" transform="translate(0,654.99) matrix(1 0 0 -1 0 0)"><g fill="#000000" fill-opacity="1.0" style="--ltx-fill-color:#000000;"><path d="M 0 17.72 L 0 637.27 C 0 647.06 7.93 654.99 17.72 654.99 L 459.66 654.99 C 469.44 654.99 477.38 647.06 477.38 637.27 L 477.38 17.72 C 477.38 7.93 469.44 0 459.66 0 L 17.72 0 C 7.93 0 0 7.93 0 17.72 Z" style="stroke:none"></path></g><g fill="#F9F9F9" fill-opacity="1.0" style="--ltx-fill-color:#F9F9F9;"><path d="M 1.97 17.72 L 1.97 637.27 C 1.97 645.97 9.02 653.02 17.72 653.02 L 459.66 653.02 C 468.36 653.02 475.41 645.97 475.41 637.27 L 475.41 17.72 C 475.41 9.02 468.36 1.97 459.66 1.97 L 17.72 1.97 C 9.02 1.97 1.97 9.02 1.97 17.72 Z" style="stroke:none"></path></g><g fill-opacity="1.0" transform="matrix(1.0 0.0 0.0 1.0 21.65 17.24)"><foreignObject color="#000000" height="627.43" overflow="visible" style="--ltx-fg-color:#000000;--fo_width :31.37em;--fo_height:45.09em;--fo_depth :0.25em;" transform="matrix(1 0 0 -1 0 623.97)" width="434.07"><span style="width:31.37em;"><span id="A2.SS3.p1.pic1.p1">The prompt template in Memory Evolution: <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline" data-latex="P_{s3}"><semantics><msub><mi>P</mi> <mrow><mi>s</mi> <mo lspace="0em" rspace="0em"></mo><mn>3</mn></mrow></msub> <annotation encoding="application/x-tex">P_{s3}</annotation></semantics></math><br>You are an AI memory evolution agent responsible for managing and evolving a knowledge base.<br>Analyze the the new memory note according to keywords and context, also with their several nearest neighbors memory.<br>Make decisions about its evolution.<br>The new memory context:{context}<br>content: {content}<br>keywords: {keywords}<br>The nearest neighbors memories:{nearest_neighbors_memories}<br>Based on this information, determine:<br>1. What specific actions should be taken (strengthen, update_neighbor)?<br>1.1 If choose to strengthen the connection, which memory should it be connected to? Can you give the updated tags of this memory?<br>1.2 If choose to update neighbor, you can update the context and tags of these memories based on the understanding of these memories.<br>Tags should be determined by the content of these characteristic of these memories, which can be used to retrieve them later and categorize them.<br>All the above information should be returned in a list format according to the sequence: [[new_memory],[neighbor_memory_1],<br>...[neighbor_memory_n]]<br>These actions can be combined.<br>Return your decision in JSON format with the following structure: {{<br>"should_evolve": true/false,<br>"actions": ["strengthen", "merge", "prune"],<br>"suggested_connections": ["neighbor_memory_ids"],<br>"tags_to_update": ["tag_1",..."tag_n"],<br>"new_context_neighborhood": ["new context",...,"new context"],<br>"new_tags_neighborhood": [["tag_1",...,"tag_n"],...["tag_1",...,"tag_n"]],<br>}}</span></span></foreignObject></g></g></svg>

### B.4 Examples of Q/A with A-Mem

<svg height="568.51" id="A2.SS4.p1.pic1" overflow="visible" version="1.1" viewBox="0 0 477.38 568.51" width="477.38"><g fill="#000000" stroke="#000000" stroke-width="0.4pt" style="--ltx-stroke-color:#000000;--ltx-fill-color:#000000;" transform="translate(0,568.51) matrix(1 0 0 -1 0 0)"><g fill="#000000" fill-opacity="1.0" style="--ltx-fill-color:#000000;"><path d="M 0 17.72 L 0 550.79 C 0 560.58 7.93 568.51 17.72 568.51 L 459.66 568.51 C 469.44 568.51 477.38 560.58 477.38 550.79 L 477.38 17.72 C 477.38 7.93 469.44 0 459.66 0 L 17.72 0 C 7.93 0 0 7.93 0 17.72 Z" style="stroke:none"></path></g><g fill="#F9F9F9" fill-opacity="1.0" style="--ltx-fill-color:#F9F9F9;"><path d="M 1.97 17.72 L 1.97 550.79 C 1.97 559.49 9.02 566.54 17.72 566.54 L 459.66 566.54 C 468.36 566.54 475.41 559.49 475.41 550.79 L 475.41 17.72 C 475.41 9.02 468.36 1.97 459.66 1.97 L 17.72 1.97 C 9.02 1.97 1.97 9.02 1.97 17.72 Z" style="stroke:none"></path></g><g fill-opacity="1.0" transform="matrix(1.0 0.0 0.0 1.0 21.65 13.78)"><foreignObject color="#000000" height="540.95" overflow="visible" style="--ltx-fg-color:#000000;--fo_width :31.37em;--fo_height:39.09em;--fo_depth :0em;" transform="matrix(1 0 0 -1 0 540.95)" width="434.07"><span style="width:31.37em;"><span id="A2.SS4.p1.pic1.p1">Example:<br>Question 686: Which hobby did Dave pick up in October 2023?<br>Prediction: photography<br>Reference: photography<br>talk start time:10:54 am on 17 November, 2023<br>memory content: Speaker Davesays: Hey Calvin, long time no talk! A lot has happened. I’ve taken up photography and it’s been great - been taking pics of the scenery around here which is really cool.<br>memory context: The main topic is the speaker’s new hobby of photography, highlighting their enjoyment of capturing local scenery, aimed at engaging a friend in conversation about personal experiences.<br>memory keywords: [<span style="--ltx-fg-color:#FF0000;">’photography’</span>, ’scenery’, ’conversation’, ’experience’, ’hobby’]<br>memory tags: [’hobby’, <span style="--ltx-fg-color:#FF0000;">’photography’</span>, ’personal development’, ’conversation’, ’leisure’]<br>talk start time:6:38 pm on 21 July, 2023<br>memory content: Speaker Calvinsays: Thanks, Dave! It feels great having my own space to work in. I’ve been experimenting with different genres lately, pushing myself out of my comfort zone. Adding electronic elements to my songs gives them a fresh vibe. It’s been an exciting process of self-discovery and growth!<br>memory context: The speaker discusses their creative process in music, highlighting experimentation with genres and the incorporation of electronic elements for personal growth and artistic evolution.<br>memory keywords: [’space’, ’experimentation’, ’genres’, ’electronic’, ’self-discovery’, ’growth’]<br>memory tags: [’music’, ’creativity’, ’self-improvement’, ’artistic expression’]<br></span></span></foreignObject></g></g></svg>

## NeurIPS Paper Checklist

The checklist is designed to encourage best practices for responsible machine learning research, addressing issues of reproducibility, transparency, research ethics, and societal impact. Do not remove the checklist: The papers not including the checklist will be desk rejected. The checklist should follow the references and follow the (optional) supplemental material. The checklist does NOT count towards the page limit.

Please read the checklist guidelines carefully for information on how to answer these questions. For each question in the checklist:

- You should answer \[Yes\], \[No\], or \[N/A\].
- \[N/A\] means either that the question is Not Applicable for that particular paper or the relevant information is Not Available.
- Please provide a short (1–2 sentence) justification right after your answer (even for NA).

The checklist answers are an integral part of your paper submission. They are visible to the reviewers, area chairs, senior area chairs, and ethics reviewers. You will be asked to also include it (after eventual revisions) with the final version of your paper, and its final version will be published with the paper.

The reviewers of your paper will be asked to use the checklist as one of the factors in their evaluation. While "\[Yes\] " is generally preferable to "\[No\] ", it is perfectly acceptable to answer "\[No\] " provided a proper justification is given (e.g., "error bars are not reported because it would be too computationally expensive" or "we were unable to find the license for the dataset we used"). In general, answering "\[No\] " or "\[N/A\] " is not grounds for rejection. While the questions are phrased in a binary way, we acknowledge that the true answer is often more nuanced, so please just use your best judgment and write a justification to elaborate. All supporting evidence can appear either in the main paper or the supplemental material, provided in appendix. If you answer \[Yes\] to a question, in the justification please point to the section(s) where related material for the question can be found.

IMPORTANT, please:

- Delete this instruction block, but keep the section heading “NeurIPS Paper Checklist",
- Keep the checklist subsection headings, questions/answers and guidelines below.
- Do not modify the questions and only use the provided macros for your answers.

1. Claims
2. Question: Do the main claims made in the abstract and introduction accurately reflect the paper’s contributions and scope?
3. Answer: \[Yes\]
4. Justification: The abstract and the introduction summarizes our main contributions.
5. Guidelines:
	- The answer NA means that the abstract and introduction do not include the claims made in the paper.
	- The abstract and/or introduction should clearly state the claims made, including the contributions made in the paper and important assumptions and limitations. A No or NA answer to this question will not be perceived well by the reviewers.
	- The claims made should match theoretical and experimental results, and reflect how much the results can be expected to generalize to other settings.
	- It is fine to include aspirational goals as motivation as long as it is clear that these goals are not attained by the paper.
6. Limitations
7. Question: Does the paper discuss the limitations of the work performed by the authors?
8. Answer: \[Yes\]
9. Justification: This paper cover a section of the limiations.
10. Guidelines:
	- The answer NA means that the paper has no limitation while the answer No means that the paper has limitations, but those are not discussed in the paper.
	- The authors are encouraged to create a separate "Limitations" section in their paper.
	- The paper should point out any strong assumptions and how robust the results are to violations of these assumptions (e.g., independence assumptions, noiseless settings, model well-specification, asymptotic approximations only holding locally). The authors should reflect on how these assumptions might be violated in practice and what the implications would be.
	- The authors should reflect on the scope of the claims made, e.g., if the approach was only tested on a few datasets or with a few runs. In general, empirical results often depend on implicit assumptions, which should be articulated.
	- The authors should reflect on the factors that influence the performance of the approach. For example, a facial recognition algorithm may perform poorly when image resolution is low or images are taken in low lighting. Or a speech-to-text system might not be used reliably to provide closed captions for online lectures because it fails to handle technical jargon.
	- The authors should discuss the computational efficiency of the proposed algorithms and how they scale with dataset size.
	- If applicable, the authors should discuss possible limitations of their approach to address problems of privacy and fairness.
	- While the authors might fear that complete honesty about limitations might be used by reviewers as grounds for rejection, a worse outcome might be that reviewers discover limitations that aren’t acknowledged in the paper. The authors should use their best judgment and recognize that individual actions in favor of transparency play an important role in developing norms that preserve the integrity of the community. Reviewers will be specifically instructed to not penalize honesty concerning limitations.
11. Theory assumptions and proofs
12. Question: For each theoretical result, does the paper provide the full set of assumptions and a complete (and correct) proof?
13. Answer: \[N/A\]
14. Justification: N/A
15. Guidelines:
	- The answer NA means that the paper does not include theoretical results.
	- All the theorems, formulas, and proofs in the paper should be numbered and cross-referenced.
	- All assumptions should be clearly stated or referenced in the statement of any theorems.
	- The proofs can either appear in the main paper or the supplemental material, but if they appear in the supplemental material, the authors are encouraged to provide a short proof sketch to provide intuition.
	- Inversely, any informal proof provided in the core of the paper should be complemented by formal proofs provided in appendix or supplemental material.
	- Theorems and Lemmas that the proof relies upon should be properly referenced.
16. Experimental result reproducibility
17. Question: Does the paper fully disclose all the information needed to reproduce the main experimental results of the paper to the extent that it affects the main claims and/or conclusions of the paper (regardless of whether the code and data are provided or not)?
18. Answer: \[Yes\]
19. Justification: Both code and datasets are available.
20. Guidelines:
	- The answer NA means that the paper does not include experiments.
	- If the paper includes experiments, a No answer to this question will not be perceived well by the reviewers: Making the paper reproducible is important, regardless of whether the code and data are provided or not.
	- If the contribution is a dataset and/or model, the authors should describe the steps taken to make their results reproducible or verifiable.
	- Depending on the contribution, reproducibility can be accomplished in various ways. For example, if the contribution is a novel architecture, describing the architecture fully might suffice, or if the contribution is a specific model and empirical evaluation, it may be necessary to either make it possible for others to replicate the model with the same dataset, or provide access to the model. In general. releasing code and data is often one good way to accomplish this, but reproducibility can also be provided via detailed instructions for how to replicate the results, access to a hosted model (e.g., in the case of a large language model), releasing of a model checkpoint, or other means that are appropriate to the research performed.
	- While NeurIPS does not require releasing code, the conference does require all submissions to provide some reasonable avenue for reproducibility, which may depend on the nature of the contribution. For example
		1. If the contribution is primarily a new algorithm, the paper should make it clear how to reproduce that algorithm.
		2. If the contribution is primarily a new model architecture, the paper should describe the architecture clearly and fully.
		3. If the contribution is a new model (e.g., a large language model), then there should either be a way to access this model for reproducing the results or a way to reproduce the model (e.g., with an open-source dataset or instructions for how to construct the dataset).
		4. We recognize that reproducibility may be tricky in some cases, in which case authors are welcome to describe the particular way they provide for reproducibility. In the case of closed-source models, it may be that access to the model is limited in some way (e.g., to registered users), but it should be possible for other researchers to have some path to reproducing or verifying the results.
21. Open access to data and code
22. Question: Does the paper provide open access to the data and code, with sufficient instructions to faithfully reproduce the main experimental results, as described in supplemental material?
23. Answer: \[Yes\]
24. Justification: We provide the code link in the abstract.
25. Guidelines:
	- The answer NA means that paper does not include experiments requiring code.
	- Please see the NeurIPS code and data submission guidelines ([https://nips.cc/public/guides/CodeSubmissionPolicy](https://nips.cc/public/guides/CodeSubmissionPolicy)) for more details.
	- While we encourage the release of code and data, we understand that this might not be possible, so “No” is an acceptable answer. Papers cannot be rejected simply for not including code, unless this is central to the contribution (e.g., for a new open-source benchmark).
	- The instructions should contain the exact command and environment needed to run to reproduce the results. See the NeurIPS code and data submission guidelines ([https://nips.cc/public/guides/CodeSubmissionPolicy](https://nips.cc/public/guides/CodeSubmissionPolicy)) for more details.
	- The authors should provide instructions on data access and preparation, including how to access the raw data, preprocessed data, intermediate data, and generated data, etc.
	- The authors should provide scripts to reproduce all experimental results for the new proposed method and baselines. If only a subset of experiments are reproducible, they should state which ones are omitted from the script and why.
	- At submission time, to preserve anonymity, the authors should release anonymized versions (if applicable).
	- Providing as much information as possible in supplemental material (appended to the paper) is recommended, but including URLs to data and code is permitted.
26. Experimental setting/details
27. Question: Does the paper specify all the training and test details (e.g., data splits, hyperparameters, how they were chosen, type of optimizer, etc.) necessary to understand the results?
28. Answer: \[Yes\]
29. Justification: We cover all the details in the paper.
30. Guidelines:
	- The answer NA means that the paper does not include experiments.
	- The experimental setting should be presented in the core of the paper to a level of detail that is necessary to appreciate the results and make sense of them.
	- The full details can be provided either with the code, in appendix, or as supplemental material.
31. Experiment statistical significance
32. Question: Does the paper report error bars suitably and correctly defined or other appropriate information about the statistical significance of the experiments?
33. Answer: \[No\]
34. Justification: The experiments utilize the API of Large Language Models. Multiple calls will significantly increase costs.
35. Guidelines:
	- The answer NA means that the paper does not include experiments.
	- The authors should answer "Yes" if the results are accompanied by error bars, confidence intervals, or statistical significance tests, at least for the experiments that support the main claims of the paper.
	- The factors of variability that the error bars are capturing should be clearly stated (for example, train/test split, initialization, random drawing of some parameter, or overall run with given experimental conditions).
	- The method for calculating the error bars should be explained (closed form formula, call to a library function, bootstrap, etc.)
	- The assumptions made should be given (e.g., Normally distributed errors).
	- It should be clear whether the error bar is the standard deviation or the standard error of the mean.
	- It is OK to report 1-sigma error bars, but one should state it. The authors should preferably report a 2-sigma error bar than state that they have a 96% CI, if the hypothesis of Normality of errors is not verified.
	- For asymmetric distributions, the authors should be careful not to show in tables or figures symmetric error bars that would yield results that are out of range (e.g. negative error rates).
	- If error bars are reported in tables or plots, The authors should explain in the text how they were calculated and reference the corresponding figures or tables in the text.
36. Experiments compute resources
37. Question: For each experiment, does the paper provide sufficient information on the computer resources (type of compute workers, memory, time of execution) needed to reproduce the experiments?
38. Answer: \[Yes\]
39. Justification: It could be found in the experimental part.
40. Guidelines:
	- The answer NA means that the paper does not include experiments.
	- The paper should indicate the type of compute workers CPU or GPU, internal cluster, or cloud provider, including relevant memory and storage.
	- The paper should provide the amount of compute required for each of the individual experimental runs as well as estimate the total compute.
	- The paper should disclose whether the full research project required more compute than the experiments reported in the paper (e.g., preliminary or failed experiments that didn’t make it into the paper).
41. Code of ethics
42. Question: Does the research conducted in the paper conform, in every respect, with the NeurIPS Code of Ethics [https://neurips.cc/public/EthicsGuidelines](https://neurips.cc/public/EthicsGuidelines)?
43. Answer: \[N/A\]
44. Justification: N/A
45. Guidelines:
	- The answer NA means that the authors have not reviewed the NeurIPS Code of Ethics.
	- If the authors answer No, they should explain the special circumstances that require a deviation from the Code of Ethics.
	- The authors should make sure to preserve anonymity (e.g., if there is a special consideration due to laws or regulations in their jurisdiction).
46. Broader impacts
47. Question: Does the paper discuss both potential positive societal impacts and negative societal impacts of the work performed?
48. Answer: \[No\]
49. Justification: We don’t discuss this aspect because we provide only the memory system for LLM agents. Different LLM agents may create varying societal impacts, which are beyond the scope of our work.
50. Guidelines:
	- The answer NA means that there is no societal impact of the work performed.
	- If the authors answer NA or No, they should explain why their work has no societal impact or why the paper does not address societal impact.
	- Examples of negative societal impacts include potential malicious or unintended uses (e.g., disinformation, generating fake profiles, surveillance), fairness considerations (e.g., deployment of technologies that could make decisions that unfairly impact specific groups), privacy considerations, and security considerations.
	- The conference expects that many papers will be foundational research and not tied to particular applications, let alone deployments. However, if there is a direct path to any negative applications, the authors should point it out. For example, it is legitimate to point out that an improvement in the quality of generative models could be used to generate deepfakes for disinformation. On the other hand, it is not needed to point out that a generic algorithm for optimizing neural networks could enable people to train models that generate Deepfakes faster.
	- The authors should consider possible harms that could arise when the technology is being used as intended and functioning correctly, harms that could arise when the technology is being used as intended but gives incorrect results, and harms following from (intentional or unintentional) misuse of the technology.
	- If there are negative societal impacts, the authors could also discuss possible mitigation strategies (e.g., gated release of models, providing defenses in addition to attacks, mechanisms for monitoring misuse, mechanisms to monitor how a system learns from feedback over time, improving the efficiency and accessibility of ML).
51. Safeguards
52. Question: Does the paper describe safeguards that have been put in place for responsible release of data or models that have a high risk for misuse (e.g., pretrained language models, image generators, or scraped datasets)?
53. Answer: \[N/A\]
54. Justification: N/A
55. Guidelines:
	- The answer NA means that the paper poses no such risks.
	- Released models that have a high risk for misuse or dual-use should be released with necessary safeguards to allow for controlled use of the model, for example by requiring that users adhere to usage guidelines or restrictions to access the model or implementing safety filters.
	- Datasets that have been scraped from the Internet could pose safety risks. The authors should describe how they avoided releasing unsafe images.
	- We recognize that providing effective safeguards is challenging, and many papers do not require this, but we encourage authors to take this into account and make a best faith effort.
56. Licenses for existing assets
57. Question: Are the creators or original owners of assets (e.g., code, data, models), used in the paper, properly credited and are the license and terms of use explicitly mentioned and properly respected?
58. Answer: \[Yes\]
59. Justification: Their contribution has already been properly acknowledged and credited.
60. Guidelines:
	- The answer NA means that the paper does not use existing assets.
	- The authors should cite the original paper that produced the code package or dataset.
	- The authors should state which version of the asset is used and, if possible, include a URL.
	- The name of the license (e.g., CC-BY 4.0) should be included for each asset.
	- For scraped data from a particular source (e.g., website), the copyright and terms of service of that source should be provided.
	- If assets are released, the license, copyright information, and terms of use in the package should be provided. For popular datasets, [paperswithcode.com/datasets](https://arxiv.org/html/2502.12110v11/paperswithcode.com/datasets) has curated licenses for some datasets. Their licensing guide can help determine the license of a dataset.
	- For existing datasets that are re-packaged, both the original license and the license of the derived asset (if it has changed) should be provided.
	- If this information is not available online, the authors are encouraged to reach out to the asset’s creators.
61. New assets
62. Question: Are new assets introduced in the paper well documented and is the documentation provided alongside the assets?
63. Answer: \[N/A\]
64. Justification: N/A
65. Guidelines:
	- The answer NA means that the paper does not release new assets.
	- Researchers should communicate the details of the dataset/code/model as part of their submissions via structured templates. This includes details about training, license, limitations, etc.
	- The paper should discuss whether and how consent was obtained from people whose asset is used.
	- At submission time, remember to anonymize your assets (if applicable). You can either create an anonymized URL or include an anonymized zip file.
66. Crowdsourcing and research with human subjects
67. Question: For crowdsourcing experiments and research with human subjects, does the paper include the full text of instructions given to participants and screenshots, if applicable, as well as details about compensation (if any)?
68. Answer: \[N/A\]
69. Justification: N/A
70. Guidelines:
	- The answer NA means that the paper does not involve crowdsourcing nor research with human subjects.
	- Including this information in the supplemental material is fine, but if the main contribution of the paper involves human subjects, then as much detail as possible should be included in the main paper.
	- According to the NeurIPS Code of Ethics, workers involved in data collection, curation, or other labor should be paid at least the minimum wage in the country of the data collector.
71. Institutional review board (IRB) approvals or equivalent for research with human subjects
72. Question: Does the paper describe potential risks incurred by study participants, whether such risks were disclosed to the subjects, and whether Institutional Review Board (IRB) approvals (or an equivalent approval/review based on the requirements of your country or institution) were obtained?
73. Answer: \[N/A\]
74. Justification: N/A
75. Guidelines:
	- The answer NA means that the paper does not involve crowdsourcing nor research with human subjects.
	- Depending on the country in which research is conducted, IRB approval (or equivalent) may be required for any human subjects research. If you obtained IRB approval, you should clearly state this in the paper.
	- We recognize that the procedures for this may vary significantly between institutions and locations, and we expect authors to adhere to the NeurIPS Code of Ethics and the guidelines for their institution.
	- For initial submissions, do not include any information that would break anonymity (if applicable), such as the institution conducting the review.
76. Declaration of LLM usage
77. Question: Does the paper describe the usage of LLMs if it is an important, original, or non-standard component of the core methods in this research? Note that if the LLM is used only for writing, editing, or formatting purposes and does not impact the core methodology, scientific rigorousness, or originality of the research, declaration is not required.
78. Answer: \[N/A\]
79. Justification: N/A
80. Guidelines:
	- The answer NA means that the core method development in this research does not involve LLMs as any important, original, or non-standard components.
	- Please refer to our LLM policy ([https://neurips.cc/Conferences/2025/LLM](https://neurips.cc/Conferences/2025/LLM)) for what should or should not be described.

[^1]: Sönke Ahrens. How to Take Smart Notes: One Simple Technique to Boost Writing, Learning and Thinking. Amazon, 2017. Second Edition.

[^2]: Anthropic. The claude 3 model family: Opus, sonnet, haiku. Anthropic, Mar 2024. Accessed May 2025.

[^3]: Anthropic. Claude 3.5 sonnet model card addendum. Technical report, Anthropic, 2025. Accessed May 2025.

[^4]: Akari Asai, Zeqiu Wu, Yizhong Wang, Avirup Sil, and Hannaneh Hajishirzi. Self-rag: Learning to retrieve, generate, and critique through self-reflection. arXiv preprint arXiv:2310.11511, 2023.

[^5]: Satanjeev Banerjee and Alon Lavie. Meteor: An automatic metric for mt evaluation with improved correlation with human judgments. In Proceedings of the acl workshop on intrinsic and extrinsic evaluation measures for machine translation and/or summarization, pages 65–72, 2005.

[^6]: Sebastian Borgeaud, Arthur Mensch, Jordan Hoffmann, Trevor Cai, Eliza Rutherford, Katie Millican, George Bm Van Den Driessche, Jean-Baptiste Lespiau, Bogdan Damoc, Aidan Clark, et al. Improving language models by retrieving from trillions of tokens. In International conference on machine learning, pages 2206–2240. PMLR, 2022.

[^7]: Xiang Deng, Yu Gu, Boyuan Zheng, Shijie Chen, Sam Stevens, Boshi Wang, Huan Sun, and Yu Su. Mind2web: Towards a generalist agent for the web. Advances in Neural Information Processing Systems, 36:28091–28114, 2023.

[^8]: Khant Dev and Singh Taranjeet. mem0: The memory layer for ai agents. [https://github.com/mem0ai/mem0](https://github.com/mem0ai/mem0), 2024.

[^9]: Darren Edge, Ha Trinh, Newman Cheng, Joshua Bradley, Alex Chao, Apurva Mody, Steven Truitt, and Jonathan Larson. From local to global: A graph rag approach to query-focused summarization. arXiv preprint arXiv:2404.16130, 2024.

[^10]: Yunfan Gao, Yun Xiong, Xinyu Gao, Kangxiang Jia, Jinliu Pan, Yuxi Bi, Yi Dai, Jiawei Sun, and Haofen Wang. Retrieval-augmented generation for large language models: A survey. arXiv preprint arXiv:2312.10997, 2023.

[^11]: Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi Wang, Xiao Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. arXiv preprint arXiv:2501.12948, 2025.

[^12]: I. Ilin. Advanced rag techniques: An illustrated overview, 2023.

[^13]: Jihyoung Jang, Minseong Boo, and Hyounghun Kim. Conversation chronicles: Towards diverse temporal and relational dynamics in multi-session conversations. arXiv preprint arXiv:2310.13420, 2023.

[^14]: Zhengbao Jiang, Frank F Xu, Luyu Gao, Zhiqing Sun, Qian Liu, Jane Dwivedi-Yu, Yiming Yang, Jamie Callan, and Graham Neubig. Active retrieval augmented generation. arXiv preprint arXiv:2305.06983, 2023.

[^15]: David Kadavy. Digital Zettelkasten: Principles, Methods, & Examples. Google Books, May 2021.

[^16]: Jiho Kim, Woosog Chay, Hyeonji Hwang, Daeun Kyung, Hyunseung Chung, Eunbyeol Cho, Yohan Jo, and Edward Choi. Dialsim: A real-time simulator for evaluating long-term multi-party dialogue understanding of conversational agents. arXiv preprint arXiv:2406.13144, 2024.

[^17]: Kuang-Huei Lee, Xinyun Chen, Hiroki Furuta, John Canny, and Ian Fischer. A human-inspired reading agent with gist memory of very long contexts. arXiv preprint arXiv:2402.09727, 2024.

[^18]: Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, et al. Retrieval-augmented generation for knowledge-intensive nlp tasks. Advances in Neural Information Processing Systems, 33:9459–9474, 2020.

[^19]: Chin-Yew Lin. Rouge: A package for automatic evaluation of summaries. In Text summarization branches out, pages 74–81, 2004.

[^20]: Xi Victoria Lin, Xilun Chen, Mingda Chen, Weijia Shi, Maria Lomeli, Rich James, Pedro Rodriguez, Jacob Kahn, Gergely Szilvasy, Mike Lewis, et al. Ra-dit: Retrieval-augmented dual instruction tuning. arXiv preprint arXiv:2310.01352, 2023.

[^21]: Zhiwei Liu, Weiran Yao, Jianguo Zhang, Liangwei Yang, Zuxin Liu, Juntao Tan, Prafulla K Choubey, Tian Lan, Jason Wu, Huan Wang, et al. Agentlite: A lightweight library for building and advancing task-oriented llm agent system. arXiv preprint arXiv:2402.15538, 2024.

[^22]: Adyasha Maharana, Dong-Ho Lee, Sergey Tulyakov, Mohit Bansal, Francesco Barbieri, and Yuwei Fang. Evaluating very long-term conversational memory of llm agents. arXiv preprint arXiv:2402.17753, 2024.

[^23]: Kai Mei, Zelong Li, Shuyuan Xu, Ruosong Ye, Yingqiang Ge, and Yongfeng Zhang. Aios: Llm agent operating system. arXiv e-prints, pp. arXiv–2403, 2024.

[^24]: Ali Modarressi, Ayyoob Imani, Mohsen Fayyaz, and Hinrich Schütze. Ret-llm: Towards a general read-write memory for large language models. arXiv preprint arXiv:2305.14322, 2023.

[^25]: Charles Packer, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G Patil, Ion Stoica, and Joseph E Gonzalez. Memgpt: Towards llms as operating systems. arXiv preprint arXiv:2310.08560, 2023.

[^26]: Kishore Papineni, Salim Roukos, Todd Ward, and Wei-Jing Zhu. Bleu: a method for automatic evaluation of machine translation. In Proceedings of the 40th annual meeting of the Association for Computational Linguistics, pages 311–318, 2002.

[^27]: Nils Reimers and Iryna Gurevych. Sentence-bert: Sentence embeddings using siamese bert-networks. In Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing. Association for Computational Linguistics, 11 2019.

[^28]: Aymeric Roucher, Albert Villanova del Moral, Thomas Wolf, Leandro von Werra, and Erik Kaunismäki. ‘smolagents‘: a smol library to build great agentic systems. [https://github.com/huggingface/smolagents](https://github.com/huggingface/smolagents), 2025.

[^29]: Zhihong Shao, Yeyun Gong, Yelong Shen, Minlie Huang, Nan Duan, and Weizhu Chen. Enhancing retrieval-augmented large language models with iterative retrieval-generation synergy. arXiv preprint arXiv:2305.15294, 2023.

[^30]: Zeru Shi, Kai Mei, Mingyu Jin, Yongye Su, Chaoji Zuo, Wenyue Hua, Wujiang Xu, Yujie Ren, Zirui Liu, Mengnan Du, et al. From commands to prompts: Llm-based semantic file system for aios. arXiv preprint arXiv:2410.11843, 2024.

[^31]: Harsh Trivedi, Niranjan Balasubramanian, Tushar Khot, and Ashish Sabharwal. Interleaving retrieval with chain-of-thought reasoning for knowledge-intensive multi-step questions. arXiv preprint arXiv:2212.10509, 2022.

[^32]: Bing Wang, Xinnian Liang, Jian Yang, Hui Huang, Shuangzhi Wu, Peihao Wu, Lu Lu, Zejun Ma, and Zhoujun Li. Enhancing large language model with self-controlled memory framework. arXiv preprint arXiv:2304.13343, 2023.

[^33]: Xingyao Wang, Boxuan Li, Yufan Song, Frank F Xu, Xiangru Tang, Mingchen Zhuge, Jiayi Pan, Yueqi Song, Bowen Li, Jaskirat Singh, et al. Openhands: An open platform for ai software developers as generalist agents. arXiv preprint arXiv:2407.16741, 2024.

[^34]: Zhiruo Wang, Jun Araki, Zhengbao Jiang, Md Rizwan Parvez, and Graham Neubig. Learning to filter context for retrieval-augmented generation. arXiv preprint arXiv:2311.08377, 2023.

[^35]: Lilian Weng. Llm-powered autonomous agents. lilianweng.github.io, Jun 2023.

[^36]: J Xu. Beyond goldfish memory: Long-term open-domain conversation. arXiv preprint arXiv:2107.07567, 2021.

[^37]: Wenhao Yu, Hongming Zhang, Xiaoman Pan, Kaixin Ma, Hongwei Wang, and Dong Yu. Chain-of-note: Enhancing robustness in retrieval-augmented language models. arXiv preprint arXiv:2311.09210, 2023.

[^38]: Zichun Yu, Chenyan Xiong, Shi Yu, and Zhiyuan Liu. Augmentation-adapted retriever improves generalization of language models as generic plug-in. arXiv preprint arXiv:2305.17331, 2023.

[^39]: Wanjun Zhong, Lianghong Guo, Qiqi Gao, He Ye, and Yanlin Wang. Memorybank: Enhancing large language models with long-term memory. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 38, pages 19724–19731, 2024.