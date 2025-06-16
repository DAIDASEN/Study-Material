## DeepSeek - R1

### DeepSeek - R1 - zero

$$
J_{ppo}(\Theta) = \mathbb{E}_{q \sim p(Q),o \sim \pi_{\theta_{old}}} \left[ \frac{1}{|o|} \sum_{t=1}^{|O|} \min \left[ \frac{\pi_{\theta}(o_{t}| q,o_{<t})}{\pi_{\theta_{old}}(o_{t}| q,o_{<t})} A_t, \text{clip} \left( \frac{\pi_{\theta}(o_{t}| q,o_{<t})}{\pi_{\theta_{old}}(o_{t}| q,o_{<t})} , 1-\epsilon, 1+\epsilon \right)A_t \right] \right]
$$

![image-20250616095841515](C:\Users\31670\AppData\Roaming\Typora\typora-user-images\image-20250616095841515.png)
$$
J_{GRPO}(\theta)=&\mathbb{E}_{\left[q\sim P(Q),\left\{o_i\right\}_{i=1}^G\sim\pi_{\theta_{old}}\left(O\mid q\right)\right]}\\
&\frac{1}{G}\sum_{i=1}^G\frac{1}{\left|o_i\right|}\sum_{t=1}^{\left|o_i\right|}\Bigg\{\min\left[\frac{\pi_\theta\left(o_{i,t}\mid q,o_{i,<t}\right)}{\pi_{\theta_{old}}\left(o_{i,t}\mid q,o_{i,<t}\right)}\hat{A}_{i,t},\mathrm{clip}\left(\frac{\pi_\theta\left(o_{i,t}\mid q,o_{i,<t}\right)}{\pi_{\theta_{old}}\left(o_{i,t}\mid q,o_{i,<t}\right)},1-\varepsilon,1+\varepsilon\right)\hat{A}_{i,t}\right]\Bigg\}
&-\beta \mathbb{D}_{KL}\left[\pi_\theta\|\pi_{ref}\right]\bigg\}
$$
Where we have
$$
\mathbb{D}_{KL}\left[\pi_\theta \| \pi_{ref}\right] = \frac{\pi_{ref}(o_{i,t} \mid q, o_{i,<t})}{\pi_\theta(o_{i,t} \mid q, o_{i,<t})} - \log \frac{\pi_{ref}(o_{i,t} \mid q, o_{i,<t})}{\pi_\theta(o_{i,t} \mid q, o_{i,<t})} - 1
$$

$$
A_i= \frac{r_i-\text{mean}(\{ r_1, r_2, \ldots, r_G \})}{\text{std}(\{ r_1, r_2, \ldots, r_G \})}
$$

Reward = Accuracy rewards + Format rewards

<font color=red>Problems:</font>

- poor readability
- language mixing

### DeepSeek - R1

#### Cold Start

Collect a small amount of long CoT data to fine-tuning the model (SFT)

#### Reasoning-oriented Reinforcement Learning

Apply the same large-scale reinforcement learning training process as employed in DeepSeek-R1-Zero

#### Rejection Sampling and Supervised Fine-Tuning

**Reasoning data:** After the convergence of reasoning - oriented RL, reasoning trajectories are generated from checkpoints via rejection sampling. The dataset is expanded using a generative reward model, and messy outputs are filtered out, resulting in about 600k reasoning - related training samples.

**Non - Reasoning data:** The DeepSeek - V3 pipeline is adopted, reusing part of its SFT dataset. For some non - reasoning tasks, a potential chain - of - thought is generated before answering, but not for simple queries like “hello”, and approximately 200k non - reasoning training samples are collected.

#### Reinforcement Learning for all Scenarios

Aligns the model with human preferences by using rule - based rewards for specific domains and general reward models for complex scenarios, while enhancing helpfulness and harmlessness.

