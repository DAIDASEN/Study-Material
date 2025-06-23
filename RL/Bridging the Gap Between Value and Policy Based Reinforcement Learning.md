First we have expected reward 
$$
O_{ER}(s, \pi) = \sum \pi(a | s) \cdot r(s, a) + \gamma O_{ER}(s', \pi)
$$
For a softmax version we have an entropy:
$$
O_{ENT}(s, \pi) = O_{ER}(s, \pi) + \tau H(s, \pi)
$$
Where $\mathbb{H}(s, \pi) = \sum_{a} \pi(a | s) \left[ -\log \pi(a | s) + \gamma \mathbb{H}(s', \pi) \right]$
$$
O_{ENT}(s, \pi) = \sum_{a} \pi(a | s) \left[ r(s, a) - \tau \log \pi(a | s) + \gamma O_{ENT}(s', \pi) \right].
$$
Therefore we have <font color=blue>$V^*(s) = \max_{\pi} O_{ENT}(s, \pi)$</font>

The optimal strategy is no longer a one-hot distribution over actions. Entropy measures the uncertainty of a distribution, and the positive term of entropy encourages the strategy to become more uncertain.
$$
\pi^*(a | s) \propto \exp\left\{ r(s, a) + \frac{\gamma V^*(s)}{\tau} \right\}
$$
Then, we have softmax expression:$V^*(s) = O_{ENT}(s, \pi^*) = \tau \log \sum_{a} \exp\left( \frac{r(s, a) + \gamma V^*(s')}{\tau} \right).$
And we also have Q function:$Q^*(s, a) = r(s, a) + \gamma V^*(s') = r(s, a) + \gamma \tau \log \sum_{a'} \exp\left( \frac{Q^*(s', a')}{\tau} \right)$

Consider the $\pi^*$, the whole expression is: 
$$
\pi^*(a | s) = \frac{\exp\left( \frac{r(s, a) + \gamma V^*(s')}{\tau} \right)}{\exp\left( \frac{V^*(s)}{\tau} \right)}
$$
Take log in both side we have:

**Theorem 1.** For $ \tau $> 0 , the policy $\pi^*$ that maximizes $O_{ENT}$ and state values   $V^*(s) = \max_{\pi} O_{ENT}(s, \pi)*$satisfy the following temporal consistency property for any state $ s $ and action $a$ where $s' = f(s, a) $:
$$
V^*(s) - \gamma V^*(s') = r(s, a) - \tau \log \pi^*(a | s).
$$

Put it into Q function:
$$
\pi^*(a | s) = \exp\left( \frac{Q^*(s, a) - V^*(s)}{\tau} \right)
$$
Also from Theorem 1 we can have
$$
V^*(s_1) - \gamma^{t-1} V^*(s_t) = \sum_{i=1}^{t-1} \gamma^{i-1} \left[ r(s_i, a_i) - \tau \log \pi^*(a_i | s_i) \right]
$$
Through minimize the difference between two side of Theorem 1 and the equation above can get the policy and value estimation.

#### PCL

trajectory: $s_{i:i+d} = (s_i, a_i, \ldots, s_{i+d-1}, a_{i+d-1}, s_{i+d})$

Our goal is to update $V_\phi$ and $\pi_\theta$ to approximate 0.
$$
C(s_{i:i+d}, \theta) = -V_\phi(s) + \gamma^d V_\phi {(s_{i+d})} + \sum_{j=0}^{d-1} \gamma^j [r(s_{i+j}, a_{i+j}) - \tau \log \pi_\theta(a_{i+j} | s_{i+j})]
$$
Therefore loss is <font color=blue>$O_{PCL}(\theta, \phi) = \sum_{s_{i:i+d} \in E} \frac{1}{2} C(s_{i:i+d}, \theta, \phi)^2$</font>

Derive loss we have:
$$
\Delta \theta = \eta_\theta C(s_{i:i+d}, \theta, \phi) \sum_{j=0}^{d-1} \gamma^j \nabla V_0 \log \pi(a_{i+j} | s_{i+j}),
$$

$$
\Delta \phi = \eta_\phi C(s_{i:i+d}, \theta, \phi) \left( \nabla V_\phi(s_i) - \gamma^d V_\phi(s_{i+d}) \right),
$$

