# Token-level Direct Preference Optimization

$$
Q_{\pi}([x, y^{<t}], y^t) = \mathbb{E}_{\pi}\left[\left.\sum_{k=0}^{\infty} \gamma^k R_{t+k}\right| s_t = [x, y^{<t}], a_t = y^t\right]
\\
V_{\pi}([x, y^{<t}]) = \mathbb{E}_{\pi}\left[ Q_{\pi}([x, y^{<t}], y^t) | s_t = [x, y^{<t}] \right],
\\
A_{\pi}([x, y^{<t}], y^t) = Q_{\pi}([x, y^{<t}], y^t) - V_{\pi}([x, y^{<t}]).
$$

<font color=blue>In this paper $\gamma$ = 1</font>

### <font color=red>Objective function</font>

$$
\max _ {\pi_{\theta}} \mathbb{E} _ {x, y^{<t} \sim \mathcal{D}, z \sim \pi_{\theta}(\cdot | [x, y^{<t}])} \Big[ A_ {\pi_{\text{ref}}} \big( [x, y^{<t}], z \big) - \beta  D_ {\text{KL}} \Big( \pi _ {\theta} ( \cdot  | [x, y^{<t}]) || \pi _ {\text{ref}} ( \cdot  | [x, y^{<t}]) \Big) \Big]
$$

Closed-form solution: $
\pi^*_\theta(z|[x, y^{<t}]) = \pi_{\text{ref}}(z|[x, y^{<t}]) \exp\left(\frac{1}{\beta} Q_{\pi_{\text{ref}}}([x, y^{<t}], z)\right) / Z([x, y^{<t}]; \beta)
$

where $ Z([x, y^{<t}]; \beta) = \mathbb{E}_{z \sim \pi_{\text{ref}}(\cdot|[x, y^{<t}])} \exp\left(\frac{1}{\beta} Q_{\pi_{\text{ref}}}([x, y^{<t}], z)\right) $is the partition function.

However, $Q$ and $Z$ is hard to estimate. $\Rightarrow$ Use it to represent $Q$
$
Q_{\pi_{\text{ref}}}([x, y^{<t}], z) =  \beta \log \frac{\pi^*_\theta(z|[x, y^{<t}])}{\pi_{\text{ref}}(z|[x, y^{<t}])}  +  \beta \log Z([x, y^{<t}]; \beta)
$

##### <Font color=blue>Define: </Font>

$$
D_{\text{SeqKL}}(x, y; \pi_1 \| \pi_2) = \sum_{t=1}^{T} D_{\text{KL}}(\pi_1(\cdot | [x, y^{<t}]) \| \pi_2(\cdot | [x, y^{<t}]))
$$

$$
P_{\text{BT}}(y_1 \succ y_2 | x) = \sigma\left( \sum_{t=1}^{T_1} \gamma^{t-1} A_{\pi}([x, y_1^{<t}], y_1^t) - \sum_{t=1}^{T_2} \gamma^{t-1} A_{\pi}([x, y_2^{<t}], y_2^t) \right),
$$

where $\sigma(x) = 1/(1 + \exp(-x))$ is the logistic sigmoid function.

Hard to control if train an $A$. From closed form solution above we can derive $Q$. And $A=Q-V$.

![image-20250707101455441](C:\Users\31670\AppData\Roaming\Typora\typora-user-images\image-20250707101455441.png)

![image-20250707103025296](C:\Users\31670\AppData\Roaming\Typora\typora-user-images\image-20250707103025296.png)

#### Advantage

- Better control the KL divergence
- Achieve a better between Alignment and Generation Diversity

### Maybe some combination with k1.5 

For token-level, we have:  $
\pi^*_\theta(z|[x, y^{<t}]) = \pi_{\text{ref}}(z|[x, y^{<t}]) \exp\left(\frac{1}{\beta} Q_{\pi_{\text{ref}}}([x, y^{<t}], z)\right) / Z([x, y^{<t}]; \beta)
$. 
It can be write as $
Q_{\pi_{\text{ref}}}([x, y^{<t}], z) -  \beta \log \frac{\pi^*_\theta(z|[x, y^{<t}])}{\pi_{\text{ref}}(z|[x, y^{<t}])}  -  \beta \log Z([x, y^{<t}]; \beta) = 0
$
Define $loss= (Q_{\pi_{\text{ref}}}([x, y^{<t}], z) -  \beta \log \frac{\pi^*_\theta(z|[x, y^{<t}])}{\pi_{\text{ref}}(z|[x, y^{<t}])}  -  \beta \log Z([x, y^{<t}]; \beta) )^2 $

However, hard to calculate $Q$ and $Z$?