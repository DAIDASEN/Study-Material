## Kimi 1.5

#### Achievement:

- Long Context Scaling $\Rightarrow$ partial rollouts  to improve training efficiency
- Improved policy optimization
- Simplistic Framework
- Multimodalities

Procedure: pretraining $\rightarrow$ vanilla supervised fine-tuning (SFT) $\rightarrow$ long-CoT supervised fine-turning $\rightarrow$ and reinforcement learning (RL)
1
### 1. Prompt Set Curation

- Diverse Coverage (Text only & Text + Images)
- Balanced Difficulty (leverages the model’s own capacity to adaptively assess the difficulty of each prompt)
- Accurate Evaluability

To avoid FP $\Rightarrow$ exclude questions that are prone to such errors

### 2. Long - CoT Supervised Fine - Tuning

​	Use prompt engineering to construct a small yet high-quality long-CoT warmup dataset

### 3. Reinforcement Learning

Initial objective function: <font color=blue>$\max_{\theta} \mathbb{E}_{(x,y^*) \sim D, (y,z) \sim \pi_{\theta}} \left[ r(x, y, y^*) \right] $</font>

#### Policy Optimization

Use a online policy mirror decent as our training algorithm, we have:
$\max_{\theta} \mathbb{E}_{(x,y^*) \sim D}[ \mathbb{E}_{(y,z) \sim \pi_{\theta}} \left[ r(x, y, y^*) \right] - τKL(π_θ(x)||π_{θ_i}(x))]$

Therefore, we have closed-form solution: <font color=blue>$
\pi^*(y, z | x) = {\pi_{\theta_i}(y, z | x) \exp\left ({r(x, y, y^*)}/{\tau}\right)}/{Z}
$</font>

Surrogate loss:
$$
L(\theta) = \mathbb{E}_{(x,y^*) \sim \mathcal{D}} \left[ \mathbb{E}_{(y,z) \sim \pi_{\theta_i}} \left[ \left( r(x,y,y^*) - r \log Z - r \log \frac{\pi_\theta(y,z|x)}{\pi_{\theta_i}(y,z|x)} \right)^2 \right] \right]
$$
However, $r \log Z$ hard to calculate $\Rightarrow$ approximate as $
\tau \log Z \approx \tau \log \frac{1}{k} \sum_{j=1}^{k} \exp\left(\frac{r(x, y_j; y^*)}{\tau}\right)$

Similarly, we have $\bar{r} = mean(r(x, y_1, y^∗ ), . . . , r(x, y_k, y^∗ ))$
$$
\frac{1}{k} \sum_{j=1}^{k} \left( \nabla_\theta \log \pi_\theta(y_j, z_j | x) \left( r(x, y_j,y^*) - \bar{r} \right) \right) - \frac{\tau}{2} \nabla_\theta \left( \log \frac{\pi_\theta(y_j, z_j | x)}{\pi_{\theta_i}(y_j, z_j | x)} \right)^2
$$

#### Length Penalty

$$
\text{len\_reward}(i) =
\begin{cases}
\lambda & \text{if } (x, y, y^*) = 1 \\
\min(0, \lambda) & \text{if } (x, y, y^*) = 0
\end{cases}
$$

$\text{where } \lambda = 0.5 - \frac{\text{len}(i) - \text{min\_len}}{\text{max\_len} - \text{min\_len}}.$

#### Sampling Strategies

- Curriculum Sampling 
- Prioritized Sampling

 
