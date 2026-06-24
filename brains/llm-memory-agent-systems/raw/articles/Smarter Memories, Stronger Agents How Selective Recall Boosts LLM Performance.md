---
title: "Smarter Memories, Stronger Agents: How Selective Recall Boosts LLM Performance"
source: "https://aiinstitute.hbs.edu/smarter-memories-stronger-agents-how-selective-recall-boosts-llm-performance/"
author:
  - "[[HBS AI Content & Learning]]"
  - "[[HBS]]"
  - "[[HBS AI Affiliate Research]]"
published: 2025-08-21
created: 2026-06-24
description: "One of AI agents’ most powerful tools is memory: the ability to learn from the past, adapt to new situations, and improve over time. But as organizations"
tags:
  - "clippings"
---
One of AI agents’ most powerful tools is memory: the ability to learn from the past, adapt to new situations, and improve over time. But as organizations and professionals increasingly deploy AI agents for complex and long-term tasks, an important question emerges: how can we ensure that these systems learn from experience without getting trapped by their past mistakes? In the new paper “ [How Memory Management Impacts LLM Agents: An Empirical Study of Experience-Following Behavior](https://arxiv.org/abs/2505.16067v1),” [Himabindu Lakkaraju](https://www.hbs.edu/faculty/Pages/profile.aspx?facId=1057381), Assistant Professor of Business Administration at Harvard Business School and PI in the [Trustworthy AI Lab](https://aiinstitute.hbs.edu/labs/trustworthy-ai-lab/) at the Harvard Business School AI Institute, and several co-authors delve into the critical role of memory management in LLM agents. Their paper sheds light on how strategic addition and deletion of experiences can impact the long term performance of AI agents and, critically, how the absence or mismanagement of these measures can actually make agents worse.

## Key Insight: Accelerate or Anchor?

> “\[A\] high ‘input similarity’ between the current task query and the one from the retrieved record often yields a high ‘output similarity’ between their corresponding (output) executions.” [\[1\]](#ref1)

The study identifies a foundational behavioral pattern: when an agent’s current task closely resembles a stored memory, the outputs tend to closely match as well. This “experience-following” correlation mirrors how humans often rely on familiar patterns, and it can accelerate learning when the stored example is correct. However, it’s also not without risks. If erroneous or low-quality experiences are stored in memory, they can be applied to future tasks, thereby decreasing the agent’s overall performance. This means that the quality of stored examples is paramount, as bad memories don’t just linger, they can create a propagating error feedback loop.

## Key Insight: Selective Addition

> “\[S\]imply storing every experience leads to significantly worse outcomes.” [\[2\]](#ref2)

If the experience-following property shows why quality matters in LLM agents, then addition shows how to control it, and a clear finding from the study is that indiscriminate memory growth actually hurts performance. In tests with three different agents, covering electronic health records (EHRs), the LLM-based autonomous driving agent AgentDriver, and a network security agent, storing every task and output (“add-all”) performed worse than using no memory addition at all. However, using strict evaluation criteria and filtering before storage led to an average 10% performance boost, so memory improvement is less about hoarding information than curating a high-quality knowledge base.

## Key Insight: Improvement through Deletion

> “History-based deletion consistently removes poor demonstrations with low output similarity, thereby improving long-term performance.” [\[3\]](#ref3)

Even with careful addition, not all stored experiences are equally useful over time. Some look similar to new tasks (“high input similarity”), but consistently produce poor output (“low output similarity”). The authors term this “misaligned experience replay,” and show that pruning these entries improves long-term outcomes. Removing experiences with repeatedly low utility (“history-based deletion”) offered the best boost to performance while effectively and efficiently maintaining memory size. From a strategic perspective, this practice mirrors audits of playbooks, datasets, and best practices to ensure that institutional knowledge remains in top shape.

## Why This Matters

The results from this research should give business leaders important context for thinking about how to choose and deploy AI agents: more data isn’t automatically better, and AI’s “experience” can actually be a liability, entrenching errors and bloating infrastructure. Disciplined curation, by selectively adding high-value experiences and strategically deleting low-value or misaligned ones, yields not only better accuracy but also more efficient, adaptable systems. In a world where executives may be involved in decision-making around LLM agents for their organizations, it’s important to have a blueprint for keeping AI agents sharp, reliable, and resilient, just like they plan for the training and advancement of their human employees. By understanding and investing in the processes that keep your AI’s memory in top-shape, your business will be equipped for tomorrow’s challenges.

## References

[\[1\]](#q1) Zidi Xiong et al., “How Memory Management Impacts LLM Agents: An Empirical Study of Experience-Following Behavior,” *arXiv* *preprint* arXiv:2505.16067v1 (May 21, 2025): 2.

[\[2\]](#q2) Xiong et al., “How Memory Management Impacts LLM Agents,” 5.

[\[3\]](#q3) Xiong et al., “How Memory Management Impacts LLM Agents,” 9.

## Meet the Authors

![](https://aiinstitute.hbs.edu/wp-content/uploads/2025/08/Xiong.png)

Zidi Xiong is a PhD student in computer science at Harvard University, advised by Himabindu Lakkaraju.

[Zidi Xiong](https://polaris-73.github.io/) is a PhD student in computer science at Harvard University, advised by Himabindu Lakkaraju.

![](https://aiinstitute.hbs.edu/wp-content/uploads/2025/08/Lin.jpg)

Yuping Lin is a PhD student in computer science at Michigan State University.

[Yuping Lin](https://yuplin2333.github.io/) is a PhD student in computer science at Michigan State University.

[Wenya Xie](https://openreview.net/profile?id=~Wenya_Xie1) is a PhD student in computer science engineering at University of Minnesota – Twin Cities.

![](https://aiinstitute.hbs.edu/wp-content/uploads/2025/08/He.png)

Pengfei He is a PhD student in computer science and engineering at Michigan State University.

[Pengfei He](https://pengfeihepower.github.io/) is a PhD student in computer science and engineering at Michigan State University.

![](https://aiinstitute.hbs.edu/wp-content/uploads/2025/08/Tang.jpg)

Jiliang Tang is a University Foundation Professor in the computer science and engineering department at Michigan State University.

[Jiliang Tang](https://www.cse.msu.edu/~tangjili/) is a University Foundation Professor in the computer science and engineering department at Michigan State University.

![](https://aiinstitute.hbs.edu/wp-content/uploads/2025/06/HimaLakkarajuPhoto.jpg)

Himabindu Lakkaraju is an Assistant Professor of Business Administration at Harvard Business School and PI at the HBS AI Institute Trustworthy AI Lab. She is also a faculty affiliate in the Department of Computer Science at Harvard University, the Harvard Data Science Initiative, Center for Research on Computation and Society, and the Laboratory of Innovation Science at Harvard. Professor Lakkaraju’s research focuses on the algorithmic, practical, and ethical implications of deploying AI models in domains involving high-stakes decisions such as healthcare, business, and policy.

[Himabindu Lakkaraju](https://www.hbs.edu/faculty/Pages/profile.aspx?facId=1057381) is an Assistant Professor of Business Administration at Harvard Business School and PI at the HBS AI Institute [Trustworthy AI Lab](https://aiinstitute.hbs.edu/labs/trustworthy-ai-lab/). She is also a faculty affiliate in the Department of Computer Science at Harvard University, the Harvard Data Science Initiative, Center for Research on Computation and Society, and the Laboratory of Innovation Science at Harvard. Professor Lakkaraju’s research focuses on the algorithmic, practical, and ethical implications of deploying AI models in domains involving high-stakes decisions such as healthcare, business, and policy.

![](https://aiinstitute.hbs.edu/wp-content/uploads/2025/08/zhen_xiang.jpg)

Zhen Xiang is Assistant Professor of Computer Science at University of Georgia.

[Zhen Xiang](https://computing.uga.edu/directory/people/zhen-xiang) is Assistant Professor of Computer Science at University of Georgia.