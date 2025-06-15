## Kimi 1.5

#### Achievement:

- Long Context Scaling $\Rightarrow$ partial rollouts  to improve training efficiency
- Improved policy optimization
- Simplistic Framework
- Multimodalities

Procedure: pretraining $\rightarrow$ vanilla supervised fine-tuning (SFT) $\rightarrow$ long-CoT supervised fine-turning $\rightarrow$ and reinforcement learning (RL)

### 1. Prompt Set Curation

- Diverse Coverage (Text only & Text + Images)
- Balanced Difficulty (leverages the model’s own capacity to adaptively assess the difficulty of each prompt)
- Accurate Evaluability

To avoid FP $\Rightarrow$ exclude questions that are prone to such errors

### 2. Long - CoT Supervised Fine - Tuning

​	Use prompt engineering to construct a small yet high-quality long-CoT warmup dataset

### 3. Reinforcement Learning

Goal: $$\max_{\theta} \mathbb{E}_{(x,y^*) \sim D, (y,z) \sim \pi_{\theta}} \left[ r(x, y, y^*) \right] $$