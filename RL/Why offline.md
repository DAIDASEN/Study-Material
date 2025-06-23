### RLHF

##### Step 1: Reward model

$$
\max_{r_{\phi}}\left\{\mathbb{E}_{(x,y_\text{win},y_\text{lose})\sim\mathcal{D}}[\log\sigma(r_\phi(x,y_\text{win})-r_\phi(x,y_\text{lose}))]\right\}
$$

##### Step 2: Update policy

$$
\max_{\pi_\theta}\left\{\mathbb{E}_{x\sim \mathcal{D},y\sim\pi_\theta(y|x)}[r_\phi(x,y)]-\beta\mathbb{D}_{\text{KL}}[\pi_\theta(y|x)||\pi_\text{ref}(y|x)]\right\}
$$

### DPO

From step 2, we have a closed form policy solution, which is:
$$
\pi^*(y|x) = \pi_\text{ref}(y|x)e^{r_\phi(x,y)/\beta}/Z(x)
$$
Also we can have reward function:
$$
r_{\phi}(x,y)=\beta\log\frac{\pi^*(y|x)}{\pi_\text{ref}(y|x)}+\beta \log Z(x)
$$
Therefore, we can combine it with step 1. The loss now is:
$$
\max_{\pi_\theta}\left\{\mathbb{E}_{(x,y_\text{win},y_\text{lose})\sim\mathcal{D}}[\log\sigma(\beta\log\frac{\pi_\theta(y_\text{win}|x)}{\pi_\text{ref}(y_\text{win}|x)} - \beta\log\frac{\pi_\theta(y_\text{lose}|x)}{\pi_\text{ref}(y_\text{lose}|x)})]\right\}
$$

### Kimi 1.5

$$
\max_{\theta} \mathbb{E}_{(x,y^*) \sim D}[ \mathbb{E}_{(y,z) \sim \pi_{\theta}} \left[ r(x, y, y^*) \right] - τKL(π_θ(x)||π_{θ_i}(x))]
$$

Closed form solution:
$$
\pi^*(y, z | x) = {\pi_{\theta_i}(y, z | x) \exp\left ({r(x, y, y^*)}/{\tau}\right)}/{Z}
$$
Surrogate loss:
$$
L(\theta) = \mathbb{E}_{(x,y^*) \sim \mathcal{D}} \left[ \mathbb{E}_{(y,z) \sim \pi_{\theta_i}} \left[ \left( r(x,y,y^*) - r \log Z - r \log \frac{\pi_\theta(y,z|x)}{\pi_{\theta_i}(y,z|x)} \right)^2 \right] \right]
$$
