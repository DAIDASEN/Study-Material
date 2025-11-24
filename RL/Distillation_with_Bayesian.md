## 1. 目标分布的定义

我们以教师策略为先验、以任务奖励为“类似然”构造**目标序列分布**
$$
\pi^*(y|x) \propto \pi_T(y|x)^{\lambda} \exp(\beta r(x,y))
$$
其中 $λ$ 控制先验强度，$β$ 控制奖励强度。写成对数形式为
$$
\log \pi^*(y|x) = \lambda \log \pi_T(y|x) + \beta r(x,y) - \log Z(x),
$$
$(Z(x))$ 为归一化常数。

**与贝叶斯的关系：** 若将 $π_T(\cdot|x)^{λ}$ 视为先验 $p(y|x)$，并以
$p(o=1|x,y) \propto \exp(\beta r(x,y))$ 
建模“好结果被观察到”，则 Bayes 定理给出
$$
p(y|x,o=1) \propto p(y|x) p(o=1|x,y) \propto \pi_T(y|x)^{\lambda} \exp(\beta r(x,y)),
$$
------

## 2. 学习目标：投影到 $\pi^*$

给定训练输入分布 $\mathcal{D}(x)$，我们希望学生策略在每个 $x$ 上逼近 $\pi^*(\cdot|x)$。
$$
\mathcal{J}(\theta) = \mathbb{E}_{x\sim\mathcal{D}} \left[ \mathrm{KL}\left( \pi^*(\cdot|x) || \pi_\theta(\cdot|x) \right) \right] = -\mathbb{E}_{x\sim D, y\sim \pi^*(x)} \left[ \log \pi_\theta(y|x) \right] + \text{const}.
$$
该选择使得学生“覆盖” $\pi^*$ 的模式（mode-covering），有利于保持多样性。

------

## 3. **前向 KL 的 on-policy 估计（序列级）**

$$
\nabla_\theta \mathcal{J}(\theta) = -\mathbb{E}_{x} \mathbb{E}_{y \sim \pi^*(\cdot|x)} \left[\nabla_\theta \log \pi_\theta(y|x)\right].
$$

由于无法直接从 $\pi^*$ 采样，采用学生策略 $\pi_\theta$ 的 on-policy 自归一化重要性采样：
对固定的 $x$，令
$$
\log \tilde{w}(x,y) = \lambda \log \pi_T(y|x) + \beta r(x,y) - \log \pi_\theta(y|x).
$$
给定样本 $y^{(k)} \sim \pi_\theta(\cdot|x)$，令

$$
\hat{w}^{(k)} = \frac{\exp\left(\log \tilde{w}^{(k)} - c\right)}{\sum_j \exp\left(\log \tilde{w}^{(j)} - c\right)} \quad (\text{如 } c = \max_j \log \tilde{w}^{(j)}),
$$
则单个 $x$ 的梯度估计为

$$
\widehat{\nabla_\theta \mathcal{J}}(x) = -\sum_{k=1}^K \hat{w}^{(k)} \nabla_\theta \log \pi_\theta\left(y^{(k)}|x\right),
$$
再跨 $x$ 取平均。实现时对 $\hat{w}^{(k)}$ **停止梯度**。

将整序列对数概率写成 token 和：

$$
\log \pi_\theta(y^{(k)} \mid x) = \sum_{t=1}^{T_k} \log \pi_\theta\left(y^{(k)}_t \mid x, y^{(k)}_{<t}\right),
$$
所以梯度可拆成 token 和：

$$
\widehat{\nabla_\theta \mathcal{J}}(x) = -\sum_{k=1}^K \hat{w}^{(k)} \sum_{t=1}^{T_k} \nabla_\theta \log \pi_\theta\left(y^{(k)}_t \mid x, y^{(k)}_{<t}\right).
$$

1. **先按序列算出权重**：
   $$
   \log \tilde{w}^{(k)} = \lambda \sum_{t} \log \pi_T(\cdot) - \sum_t \log \pi_\theta(\cdot) + \beta r^{(k}),
   $$
   做 softmax 得到 $\hat{w}^{(k)}$（停用梯度）。

2. **损失写成 token 交叉熵带序列权重**：
   $$
   L = -\sum_{k=1}^K \hat{w}^{(k)} \sum_{t=1}^{T_k} \log \pi_\theta\left(y^{(k)}_t \mid x, y^{(k)}_{<t}\right).
   $$
