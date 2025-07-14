# From $r$ to $Q^*$: Your language model is Secretly a Q-function.

Define: A token level MDP as a tuple: $M=(S,A,f,r,\rho)$
State space $S$: All token up-to-now
Action space $A$: vocabulary of tokens $A$.
Dynamics $f$ is a deterministic transition model between tokens $f(s,a) = s|a$，$|$ is concatenation.
The initial state distribution $\rho _0$ prompt $x$'s distribution.

Under token-level MDP, we have Bradley-Terry:
$$
P(r^{l}\leq r^{w})=\frac{\exp(\sum_{i=1}^{N} r(s_i^{w}, a_i^{w}))}{\exp(\sum_{i=1}^{N} r(s_i^w, a_i^w)) + \exp(\sum_{i=1}^{M} r(s_i^l, a_i^l))}
$$

Entropy-Bonus: 

$$
H(x) = - \int_x P(x) \log P(x)
$$

<font color=blue>RLHF  PPO with $KL$ penalty and Entropy Bonus:</font>
$$
\max_{\pi_\theta} \mathbb{E}_{a \sim \pi_{\theta}(.|s_t) } \left[ \sum r(s_t,a_t) + \beta \log \pi_{ref}(a_t|s_t) + \beta H(\pi) \right]
$$
reward-model: (token-level)
$$
r(s_t, a_t) = 
\begin{cases} 
\beta \log \pi_{ref}(a_t|s_t), & \text{if } s_{t+1} \text{ not terminate} \\
r(x,y)+ \beta \log  \pi_{ref}(a_t|s_t), & \text{if } s_{t+1} \text{ terminal}
\end{cases}
$$
<font color=blue>DPO: </font>

 Closed-form Solution:
$$
\pi^*(y|x) = \frac{1}{Z(x)} \pi_{ref}(y|x) e^{r(x,y)}
$$
reward $ r(x,y) = \beta \log \pi^*(y|x) - \beta \log \pi_{ref}(y|x) - Z(x) $
$$
\Rightarrow L_{DPO} (\pi_\theta; \pi_{ref}) = -\mathbb{E}_{(x,y^w,y^l)\sim D} [\log \sigma(
\beta\log \frac{\pi_\theta(y^w|x)}{\pi_{ref}(y^w|x)} - \beta \log \frac{\pi_\theta(y^l|x)}{\pi_{ref}(y^l|x)})]
$$
For RLHF's equation we have fixed point solution
$$
\Rightarrow \pi^*(a_t|s_t) = e^{(Q^*(s_t,a_t) - V^*(s_t)) / \beta} \quad
$$
Also we have: 
$$
V^*(s_t) = \beta \log \sum_{a \in A} e^{Q^*(s_t,a) / \beta}
$$
Proof: $\pi^*(a_t|s_t) = \frac{e^{Q^*(s_t,a_t) / \beta}}{e^{V^*(s_t) / \beta}}$

$$
\sum_{a \in A} \pi^*(a_t|s_t) = 1 \quad \text{Therefore} \quad e^{V^*(s_t) / \beta} = \sum_{a \in A} e^{Q^*(s_t,a) / \beta}
$$
However no information for single State  action pair $ r$  

#### From $r$ to $Q^*$:

Original DPO make $Q^* = r$ cause no future reward

In token-level we define the following $Q^*$:
$$
Q^*(s_t, a_t) = 
\begin{cases} 
r(s_t, a_t) + \beta \log \pi_{ref}(a_t|s_t) + V^*(s_{t+1}) & \text{if not terminal} \\
r(s_t, a_t) + \beta \log \pi_{ref}(a_t|s_t) & \text{if } s_{t+1} \text{ terminal}
\end{cases}
$$
**Lemma 1** $r(s_t, a_a)$ and  $Q^*(s_t, a_t)$ have bijection

#### DPO learns our best estimate of $Q^*$:

$$
\sum_{t=0}^{T-1} r(s_t, a_t) = \sum_{t=0}^{T-1} (Q^*(s_t, a_t) - \beta \log \pi_{ref}(a_t|s_t) - V^*(s_{t+1}))
$$
$$
= Q^*(s_0, a_0) - \beta \log \pi_{ref}(a_0|s_0) + \sum_{t=1}^{T-1} (Q^*(s_t, a_t) - \beta \log \pi_{ref}(a_t|s_t) - V^*(s_{t}))
$$
$$
V^*(s_T) = 0
$$

From Fixed point solution:
$$
\beta \log (\pi^*(a_t|s_t)) = Q^*(s_t, a_t) - V^*(s_t)
$$
Therefore,
$$
\sum_{t=0}^{T-1} r(s_t, a_t) = Q^*(s_0, a_0) - \beta \log \pi_{ref}(a_0|s_0) + \sum_{t=1}^{T-1} \beta \log \frac{\pi^*(a_t|s_t)}{\pi_{ref}(a_t|s_t)}
$$
$$
= V^*(s_0) + \sum_{t=1}^{T-1} \beta \log \frac{\pi^*(a_t|s_t)}{\pi_{ref}(a_t|s_t)}
$$

$$

$$

#### Token-Level DPO Can Parameterize Any Dense Reward Function

Advantage function define as:
$$
A^∗(s,a)=Q 
^∗
 (s,a)−V 
^∗
 (s)
$$
Also we have: 
$$
\beta \log \frac{\pi^*(a_t | s_t)}{\pi_{\text{ref}}(a_t | s_t)} = r(s_t, a_t) + V^*(s_{t+1}) - V^*(s_t).
$$
Denote $ \beta \log \frac{\pi^*(a_t | s_t)}{\pi_{\text{ref}}(a_t | s_t)} $ as another reward function, 2 reward functions are equivalent.

**Theorem 1.** Given a reference policy \( $\pi_{\text{ref}}$ \) and a parameter \($ \beta > 0 $\), all reward classes consistent with the Plackett-Luce (and Bradley-Terry) models in equation (1) can be represented with the re-parameterization of the form
$$
r(s, a) = \beta \log \pi(a | s) - \beta \log \pi_{\text{ref}}(a | s)
$$

within the token MDP where \($ V^*(s_t) = 0 $\) for all terminal states.
