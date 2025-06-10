### State Value

$$
v_{\pi}(s) = \mathbb{E}[R_{t+1}|S_t= s]+\gamma\mathbb{E}[G_{t+1}|S_t=s]
\\=\sum_a\pi(a|s)[\sum_r p(r|s,a)r+\gamma \sum_{s'}p(s'|s,a)v_{\pi}(s')]
$$

Also we have matrix form, which is <font color=blue>$v_\pi (s) = r_\pi(s)+\gamma P_\pi v_\pi$</font>
<font color = Green>How to solve:</font>

1.  $v_\pi = (I-\gamma P_\pi)^{-1}r_\pi$ Hard to calculate when model is complex

2. <font color = red>Iteration Solution:</font>

   $v_{k+1}=r_\pi +\gamma P_\pi v_k$ We can proof that when $k\rightarrow \infty \ v_k = v_\pi$

### Action Value

For **definition** we have: <font color = blue>$q_\pi(s,a) = \mathbb E [G_t|S_t=s,A_t=a]\\$. </font>

Moreover consider State value function we have $v_\pi(s) = \mathbb{E}[G_t|S_t=s] = \sum_{a} \pi(a|s) \mathbb{E}[G_t|S_t=s,A_t=a]$. Therefore we have <font color=blue> $V_\pi(s) = \sum_a \pi(a | s) q_\pi(s, a)$.</font>

Compare the equation above we can find that $q_\pi(s,a) =\sum_r p(r|s,a)r+\gamma \sum_{s'}p(s'|s,a)v_{\pi}(s')$

<font color = Green>How to solve:</font>

1. Use State-value to calculate
2. Calculate without models $\Rightarrow$ based on data

### Optimal Policy

Core Concepts: optimal state-value and optimal policy $\Rightarrow$ Bellman optimality equation

For deterministic, for $q_\pi(s,a)$ we have $a' \in A$ that in the state s $q_\pi(s,a')$ is the maximum value.
Therefore 
$$
\pi_{new}(a|s)=
\begin{cases}
1& \text{a=a'}\\0& \text{a ≠ a'}
\end{cases}
$$
**<font color=red>BOE</font>**: 
$$
v_{\pi}(s) =max_\pi\sum_a\pi(a|s)[\sum_r p(r|s,a)r+\gamma \sum_{s'}p(s'|s,a)v_{\pi}(s')]
		 \\= max_\pi[\sum_a\pi(a|s)q(s,a)] , \ \ \ \ \ \  \ \forall s \in S
$$
Matrix form: $ v = max_\pi(r_\pi+\gamma P_\pi v)$
Consider the right-hand-side of BOE, <font color = blue>$max_\pi[\sum_a\pi(a|s)q(s,a)] = max_{a\in \Alpha}q(s,a)$ </font>

The optimality is achieved when:
$$
\pi(a|s)=
\begin{cases}
1& \text{a=a'}\\0& \text{a ≠ a'}
\end{cases}
$$
<font color=green>How to solve</font>: Denote $f(v) = max_\pi(r_\pi+\gamma P_\pi v)$, therefore the equation is $v = f(v)$. Since $f$ is a contraction mapping, we have a sequence $v_{k+1} = f(v_k)$, when $k \rightarrow \infty \  v_k\rightarrow v^*$, $v^*$ is optimal state value function. and we can get corresponding policy.

### Value iteration algorithm

$\Rightarrow$ Based on the algorithm above, we have the Value iteration

- For every action $ \alpha \in A(s) $, do:
  	**q-value**: $q_k(s, a) = \sum_{r} p(r | s, a) r + \gamma \sum_{s'} P(s' | s, a) v_k(s')$
- **Maximum action value**: $a^*_k(s) = \arg \max_a q_k(s, a)$
- **Policy update**: $
  \pi_{k+1}(a | s) = 1 \ \text{if } a = a^*_k \\\pi_{k+1}(a|s)=0 & \text{otherwise} 
  $

- **Value update**: $v_{k+1}(s) = \max_a q_k(s, a)$

### Policy iteration algorithm

While the policy has not converged, for the $k$th iteration, do

- **Policy evaluation:**
  **Initialization:** an arbitrary initial guess $v_{\pi_k}^{(0)}$
  	While $v_{\pi_k}^{(j)}$ has not converged, for the $j$ th iteration, do
  	For every state $s \in \mathcal{S}$, do<font color=blue> $v_{\pi_k}^{(j+1)}(s) = \sum_a \pi_k(a|s) \left[\sum_r p(r|s,a)r + \gamma \sum_{s'} p(s'|s,a)v_{\pi_k}^{(j)}(s')\right]$ </font>

- **Policy improvement:**
  For every state $s \in \mathcal{S}$, do
  	For every action $a \in \mathcal{A}(s)$, do
  		$$q_{\pi_k}(s,a) = \sum_r p(r|s,a)r + \gamma \sum_{s'} p(s'|s,a)v_{\pi_k}(s')$$
  	$$a_k^*(s) = \arg\max_a q_{\pi_k}(s,a)$$
  	$$\pi_{k+1}(a|s) = 1 \text{ if } a = a_k^*, \text{ and } \pi_{k+1}(a|s) = 0 \text{ otherwise}$$

### MC

For basic part, same idea from Policy iteration. However, we do not use state value  to calculate action value. We use sampling method to get action value 

#### **MC Exploring start**

Based on the second image content, here's the markdown formatted with Typora-style formulas:

**Initialization:** Initial guess $\pi_0$.
**Aim:** Search for an optimal policy.

For each episode, do
**Episode generation:** Randomly select a starting state-action pair $(s_0, a_0)$ and ensure that all pairs can be possibly selected. Following the current policy, generate an episode of length $T$: $s_0, a_0, r_1, \ldots, s_{T-1}, a_{T-1}, r_T$.

**Policy evaluation and policy improvement:**
Initialization: $g \leftarrow 0$
For each step of the episode, $t = T-1, T-2, \ldots, 0$, do
	$$g \leftarrow \gamma g + r_{t+1}$$
	**Use the first-visit strategy:**
	If $(s_t, a_t)$ does not appear in $(s_0, a_0, s_1, a_1, \ldots, s_{t-1}, a_{t-1})$, then
		     $Returns(s_t, a_t) \leftarrow Returns(s_t, a_t) + g$
		     $q(s_t, a_t) = \text{average}(Returns(s_t, a_t))$
                    $\pi(a|s_t) = 1 \text{ if } a = \arg\max_a q(s_t, a)$

<font color=green>However,</font> we need to get episode from every action state pair, we can't ensure evert action state pair appear in the episode. $\Rightarrow$ soft policy

#### **$\epsilon$ - greedy policies** (a kind of soft policy)

Initialization: Initial guess $\pi_0$ and $\epsilon \in [0,1]$

**Aim:** Search for an optimal policy.

For each episode, do
**Episode generation:** Randomly select a starting state-action pair $(s_0, a_0)$. Following the current policy, generate an episode of length $T$: $s_0, a_0, r_1, \ldots, s_{T-1}, a_{T-1}, r_T$.
**Policy evaluation and policy improvement:**
Initialization: $g \leftarrow 0$
For each step of the episode, $t = T-1, T-2, \ldots, 0$, do
	$g \leftarrow \gamma g + r_{t+1}$
	**Use the every-visit method:**
	If $(s_t, a_t)$ does not appear in $(s_0, a_0, s_1, a_1, \ldots, s_{t-1}, a_{t-1})$, then
		$Returns(s_t, a_t) \leftarrow Returns(s_t, a_t) + g$
		$q(s_t, a_t) = \text{average}(Returns(s_t, a_t))$
		Let $a^* = \arg \max_a q(s_t, a)$ and
			$$\pi(a|s_t) = \begin{cases} 
1 - \frac{|\mathcal{A}(s_t)|-1}{|\mathcal{A}(s_t)|} \varepsilon, & a = a^* \\
\frac{1}{|\mathcal{A}(s_t)|} \varepsilon, & a \neq a^*
\end{cases}$$

### QAC

**Aim:** Search for an optimal policy by maximizing $J(θ)$.

At time step t in each episode, do

Generate $a_t$ following $π(a|s_t, θ_t)$, observe $r_{t+1}, s_{t+1}$, and then generate $a_{t+1}$ following $π(a|s_{t+1}, θ_t)$.

**Critic (value update):** <font color=blue>$w_{t+1} = w_t + α_w [r_{t+1} + γq(s_{t+1}, a_{t+1}, w_t) - q(s_t, a_t, w_t)] ∇_w q(s_t, a_t, w_t)$</font>

**Actor (policy update):** <font color=blue>$θ_{t+1} = θ_t + α_θ ∇_θ ln π(a_t|s_t, θ_t) q(s_t, a_t, w_{t+1})$</font>

### Advantage Actor Critic (A2C)

<font color = red>Core idea: introduce a baseline to reduce variance </font>

For  $$\nabla_\theta J(\theta) = \mathbb{E}_{S \sim \eta, A \sim \pi} \left[ \nabla_\theta \ln \pi(A|S, \theta_t) q_\pi(S, A) \right] = \mathbb{E}_{S \sim \eta, A \sim \pi} \left[ \nabla_\theta \ln \pi(A|S, \theta_t) (q_\pi(S, A) - b(S)) \right]$$
Normally we use $v_\pi(s)$ as baseline $b(S)$.

**Aim:** Search for an optimal policy by maximizing $J(\theta)$.

At time step $t$ in each episode, do
Generate $a_t$ following $\pi(a|s_t, \theta_t)$ and then observe $r_{t+1}, s_{t+1}$.

**TD error (advantage function): **<font color=blue>$\delta_t = r_{t+1} + \gamma v(s_{t+1}, w_t) - v(s_t, w_t)$</font>

**Critic (value update):** <font color=blue>$w_{t+1} = w_t + \alpha_w \delta_t \nabla_w v(s_t, w_t)$</font>

**Actor (policy update):** <font color=blue>$\theta_{t+1} = \theta_t + \alpha_\theta \delta_t \nabla_\theta \ln \pi(a_t|s_t, \theta_t)$ </font>

**<font color=red>Policy Gradient is on-policy algortihm, $A$ follow $\pi$</font>** $\Rightarrow$  Importance Sampling change it to off-policy

<font color=green>Impotance Sampling</font>
$$\mathbb{E}_{X \sim p_0}[X] = \sum_x p_0(x)x = \sum_x p_1(x) \frac{p_0(x)}{p_1(x)} x = \mathbb{E}_{X \sim p_1}[f(X)]$$, where $f(x) = \frac{p_0(x)}{p_1(x)}$
Moreover we have: $$\mathbb{E}_{X \sim p_0}[X] \approx \bar{f} = \frac{1}{n} \sum_{i=1}^n f(x_i) = \frac{1}{n} \sum_{i=1}^n \frac{p_0(x_i)}{p_1(x_i)} x_i$$
$\frac{p_0(x_i)}{p_1(x_i)}$ is called importance weight
