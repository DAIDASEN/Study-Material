我注意到原文中的公式在渲染上确实存在一些问题，下面我将所有公式用标准 LaTeX 格式重新整理输出，保持原文逻辑不变。

---

过去半年，On-Policy Distillation（OPD）相关工作里有一条很清晰的技术路线：大家开始意识到，OPD 的核心不只是“student 自己 rollout，然后 teacher 给 token-level supervision”，而是 **这个 token-level supervision 到底应该被解释成什么目标函数**。早期 OPD 的直觉很简单：student 在自己的轨迹上生成 token，teacher 在这些 prefix 上给 logits，student 去对齐 teacher。这样比 SFT 更 on-policy，也比 RL 的 sparse outcome reward 更 dense。但最近的工作开始追问更底层的问题：OPD 的 KL 到底是在做 imitation，还是在做 dense reward optimization？teacher logits 应该被直接匹配，还是应该被重写成某种 calibrated target？reverse KL、forward KL、advantage weighting、reward extrapolation，到底各自适合什么 token？这篇文章就围绕最近的 G-OPD / reward / divergence 变式 做一个梳理。

## 1. OPD 的关键转折：teacher logits 可以被看成 dense reward

标准 OPD 通常可以理解成：student 生成自己的轨迹，然后在这些 student-generated trajectories 上最小化 student 和 teacher 的 token-level divergence。这个做法的好处是，它把 teacher supervision 放到了 student 实际会访问的状态上，缓解 off-policy KD 的 train-test mismatch。

但真正让 OPD 最近变得有趣的，是 G-OPD / ExOPD 这篇文章。它指出，标准 OPD 不只是“对齐 teacher logits”，而可以被重新解释为一种 dense KL-constrained RL。更具体地说，teacher 相对 reference model 的 log-prob ratio 可以看成 token-level implicit reward：

$$
r_t = \log\frac{\pi_T(y_t|h_t)}{\pi_{ref}(y_t|h_t)}
$$

这意味着 OPD 的每个 token 都有一个 dense reward，而不是像普通 RL 那样只在最终答案处拿 outcome reward。G-OPD 进一步引入 reward scaling factor $\lambda$，用来控制 reward term 相对 KL regularization 的强度【0†L1-L4】。

这个视角非常重要，因为它把 OPD 从一个“蒸馏算法”变成了一个“可设计的策略优化目标”。标准 OPD 相当于：

$$
\lambda = 1
$$

G-OPD 允许：

$$
0 < \lambda < 1
$$

这时叫 reward interpolation，student 行为介于 reference 和 teacher 之间；也允许：

$$
\lambda > 1
$$

这时叫 reward extrapolation，student 不只是模仿 teacher，而是沿着 teacher 相对 reference 的改进方向继续往前推。G-OPD 论文报告，在数学推理和代码生成上，合适的 $\lambda > 1$ 可以超过标准 OPD，甚至在某些 same-size / multi-teacher 设置里让 student 超过 domain teachers【0†L1-L4】。

这篇文章的意义不只是“$\lambda = 1.25$ 效果好”，而是打开了一个设计空间：OPD 里面有很多默认被固定的东西：reward 权重、reference、KL 方向、target distribution、confidence calibration。它们都可以被重新设计。

## 2. G-OPD / ExOPD：奖励外推为什么能“超过 teacher”？

G-OPD 的核心公式可以写成：

$$
J_{\text{G-OPD}} = \mathbb{E}_{y \sim \pi_\theta} \left[ \lambda \log\frac{\pi_T(y|x)}{\pi_{ref}(y|x)} - D_{KL}(\pi_\theta \| \pi_{ref}) \right]
$$

当 $\lambda = 1$ 时，它退化为标准 OPD。当 $\lambda > 1$ 时，它不再只是匹配 teacher，而是在 log-policy 空间里把 teacher 相对 reference 的变化继续放大。

直观上，如果 teacher 是从 base model 经过 RL 得到的，那么：

$$
\log \pi_T - \log \pi_{base}
$$

就表示 teacher 经过 RL 后学到的方向。ExOPD 做的是：

$$
\log \pi_S^{new} \approx \log \pi_{ref} + \lambda(\log \pi_T - \log \pi_{ref})
$$

如果 $\lambda > 1$，student 就会被推到 teacher 之外的位置。这解释了为什么 ExOPD 有可能超过 teacher：它并不是在做普通 imitation，而是在做 teacher improvement direction 的外推。

但这也解释了它为什么有风险。G-OPD 论文也观察到，$\lambda$ 过大可能导致 student 过度拟合 log-ratio peak，带来不稳定、长度膨胀或 reward hacking【0†L1-L4】。

所以 ExOPD 的真正启发是：teacher/reference log-ratio 可以作为 reward，但 reward 不是越大越好；外推应该有边界。这也自然引出后面几类工作：有的研究外推边界，有的研究 divergence 方向，有的研究 teacher entropy，还有的研究 calibration。

## 3. Veto：不要直接跨越 teacher-student gap，而是在 logit space 搭桥

论文：Stable On-Policy Distillation through Adaptive Target Reformulation

Veto 是一篇很适合和 G-OPD 放在一起读的文章。它关注的问题不是 reward extrapolation，而是 on-policy KD 里 teacher 和 novice student 分布差太大时，直接用 KL 目标会不稳定。这篇文章指出，forward KL 可能出现 pathological gradients，reverse KL 又容易造成 diversity collapse。为了解决这个问题，Veto 不去混合数据，而是在 logit space 里构造一个 teacher 和 student 之间的中间 target distribution。这个中间 target 起到一个 geometric bridge 的作用：它强调 teacher 和 student 已经有共识的区域，同时抑制低置信 token 上的 harmful gradients【0†L4-L6】。

它的核心思想可以概括成：当 teacher 和 student 差太远时，不要强迫 student 一步跳到 teacher；先构造一个可达的 intermediate target。这和 G-OPD 的思路有相似之处：两者都不是简单接受原始 OPD 目标，而是在改目标函数本身。区别是：G-OPD 改 reward/KL 相对强度，用 $\lambda$ 做 interpolation / extrapolation；Veto 改 teacher target，用一个 logit-space bridge 稳定 teacher-student alignment。

我觉得 Veto 的价值在于，它把“OPD 不稳定”解释成 divergence objective 的问题，而不是简单归因于数据或模型大小。它说明，OPD 的 target distribution 本身也可以被重写。

## 4. Entropy-Aware OPD：teacher 高熵时，不该只用 reverse KL

论文：Entropy-Aware On-Policy Distillation of Language Models

标准 OPD 常用 reverse KL。reverse KL 有一个典型特点：mode-seeking。它倾向于让 student 去追 teacher 高概率的模式，而不是覆盖 teacher 分布里的所有可能选择。这在 teacher 非常确定时是好事。比如数学推理某一步只有一个明显正确 token，reverse KL 可以很精准地让 student 学到 teacher 的偏好。但当 teacher entropy 很高时，reverse KL 就可能出问题。因为 teacher 自己认为多个 token 都合理，student 如果只追一个模式，就会丢失 diversity，并且训练信号变得不稳定。

Entropy-Aware OPD 的核心观点正是：teacher uncertainty 应该影响 divergence choice。该文提出，在 teacher entropy 高的位置加入 forward KL，从而在高不确定 token 上更好地覆盖 teacher 的 plausible outputs，同时在低熵 token 上保留 reverse KL 的精准 imitation【0†L7-L10】。

它的目标不是完全抛弃 reverse KL，而是做一种局部切换：

$$
\text{low teacher entropy} \Rightarrow \text{reverse KL}
$$

$$
\text{high teacher entropy} \Rightarrow \text{add forward KL}
$$

这篇文章的实验也比较清楚：在六个数学推理 benchmark 上，相比 baseline OPD，它报告 Qwen3-0.6B-Base、Qwen3-1.7B-Base、Qwen3-4B-Base 的 Pass@8 分别提升 +1.37、+2.39、+5.05【0†L7-L10】。

这篇文章给 OPD 设计带来一个重要原则：KL 方向不应该全局固定；teacher 分布越不确定，就越需要 mode-covering。这和前面 flawed prefix / token selection 那条线也有交集。teacher entropy 高不一定代表 teacher 错了，但代表 teacher signal 的性质变了：它不再是“选这个 token”，而更像是“这些 token 都可以”。

## 5. AOPD：positive advantage 用 RL，non-positive advantage 用 imitation

论文：Asymmetric On-Policy Distillation: Bridging Exploitation and Imitation at the Token Level

AOPD 从另一个角度重新设计 OPD 的 token-level update。它认为标准 advantage-weighted OPD 有三个结构性问题：高方差更新、zero-advantage 区域梯度消失，以及在 corrective signals 不足时的探索瓶颈。于是 AOPD 提出一种 asymmetric objective：当 token 的 advantage 为正时，保留 policy-gradient 式的 positive reinforcement；当 advantage 非正时，不再做低效的 negative reinforcement，而是改成 localized divergence matching，让 student 在局部对齐 teacher【0†L10-L13】。

这个思路很有意思，因为它把 token 分成两种训练语义：

- **positive advantage region**：这个 token 值得强化，所以用 exploitation / RL-style update；
- **non-positive advantage region**：这个 token 本身不值得强化，但也不能什么都不学，所以用 imitation / local distribution matching 修正。

AOPD 的实验显示，在数学推理 benchmark 上，它相比标准 OPD 在 strong initialization 和 weak initialization 下分别有 4.09 和 8.34 的平均提升，同时保持更高 policy entropy，并在 sequential tool-use adaptation 中有更好的 capability retention【0†L10-L13】。

这篇文章的重点不是“换一个 KL”，而是提出：同一个 token-level OPD loss 里，positive 和 non-positive 区域应该承担不同功能。这和 G-OPD 的关系也很清楚。G-OPD 用 $\lambda$ 控制 reward strength；AOPD 则问：当 reward/advantage 信号本身不够 informative 时，是否还应该继续用 reward-style update？

## 6. Extrapolation Cliff：$\lambda > 1$ 有用，但 structured output 里有悬崖

论文：The Extrapolation Cliff in On-Policy Distillation of Near-Deterministic Structured Outputs

如果 G-OPD 说“reward extrapolation 可以超过 teacher”，Extrapolation Cliff 这篇文章就像是在提醒：可以外推，但不是所有任务都能无限外推。这篇文章研究的是 near-deterministic structured output，例如 JSON listwise ranking。它发现，当 reward-extrapolation coefficient $\lambda > 1$ 时，student 的确可能在 domain 内超过 teacher；但超过某个阈值 $\lambda^\star$ 后，模型会突然破坏输出 contract，比如 JSON 格式、字段绑定、ID 完整性等【0†L13-L16】。

文章做了一个很有价值的理论化处理：在 single-position Bernoulli reduction 下，推导出一个 closed-form clip-safety threshold。这个阈值由三个可测量量决定：teacher modal probability、warm-start mass 和 importance-sampling clip strength【0†L13-L16】。

更关键的是，它发现 collapse 主要体现在 parse validity 上，而不是 parsed outputs 上的 semantic ranking quality。也就是说，模型不是突然不会排序了，而是格式 contract 崩了。文章报告，在 Amazon Fashion listwise 任务中，NDCG@1 在 parsed outputs 上基本保持平，但 parse validity 在预测边界附近急剧变化【0†L13-L16】。

这篇文章对 OPD 目标函数设计非常重要，因为它说明：reward extrapolation 的风险不是平均发生在所有 token 上，而是集中发生在 contract-critical tokens 上。这也解释了为什么 structured output 比数学自由文本更敏感。数学推理里输出格式可以有弹性；JSON / function calling 里，一个括号、引号、字段名错了，就直接 invalid。

因此，Extrapolation Cliff 不是在否定 G-OPD，而是在补上一个边界理论：

$$
\lambda > 1 \text{ 有收益，但必须知道安全区间。}
$$

## 7. CaOPD：能力蒸馏不等于置信度蒸馏

论文：The Illusion of Certainty: Decoupling Capability and Calibration in On-Policy Distillation

CaOPD 关注的是另一个非常现实的问题：OPD 可以提升 accuracy，但也可能让模型变得过度自信。这篇文章提出一个现象，叫 Scaling Law of Miscalibration：OPD 虽然提高任务能力，但会系统性地把模型推向 severe overconfidence。作者认为根源是 training 和 deployment 的信息不匹配：训练时 teacher supervision 可能基于 privileged context，而部署时模型只能用 deployment-time information 来报告自己的 confidence【0†L16-L19】。

换句话说，teacher-conditioned success 不一定是 deployment-time confidence 的合理目标。一个模型在 teacher 帮助下学会做对，不代表它应该在没有 teacher privileged context 的情况下给出同样高的置信度。

CaOPD 的解决思路是 calibration-aware OPD：从 model rollouts 中估计 empirical confidence，用 student-grounded target 替换原始 self-reported confidence，再通过 self-distillation pipeline 蒸馏 revised response。论文报告，CaOPD 能在保持 competitive capability 的同时实现更好的 calibration，并且能在 OOD 和 continual learning 设置下更稳健【0†L16-L19】。

这篇文章非常值得放进 reward/divergence 变式类，因为它提出：OPD 里的 target 不只有“答案能力”，还包括“置信度语义”。能力可以蒸馏，但 confidence 不能照抄 teacher-conditioned target。这和 Entropy-Aware OPD 是互补的。Entropy-Aware 关心 teacher distribution 的不确定性如何影响 KL；CaOPD 关心 student 最终报告的 confidence 是否被 OPD 扭曲。

## 8. Uni-OPD：teacher supervision 要和 outcome reward 保持顺序一致

论文：Uni-OPD: Unifying On-Policy Distillation with a Dual-Perspective Recipe

Uni-OPD 不完全是 divergence 变式，但它对 reward / supervision calibration 很重要。它把 OPD 的瓶颈总结成两个：student 需要探索 informative states，teacher supervision 需要可靠。更具体地，Uni-OPD 认为 aggregated token-level guidance 是否可靠，取决于它和 outcome reward 是否保持 order consistency【0†L19-L22】。

这个观点很关键。因为 OPD 给的是 dense token-level guidance，但最终我们真正关心的是 sequence-level outcome，比如数学题是否答对、代码是否通过测试、tool-use 是否成功。如果 token-level KL 的累计信号和最终 outcome reward 排序不一致，那么 dense supervision 反而可能误导 student。

Uni-OPD 提出 outcome-guided margin calibration，用全局 outcome reward 去校准 token-level guidance 的 margin，让正确轨迹和错误轨迹之间的信号更符合最终任务目标。它在 5 个领域、16 个 benchmark 上覆盖 LLM、MLLM、single-teacher、multi-teacher、strong-to-weak、cross-modal 等设置【0†L19-L22】。

Uni-OPD 对目标函数设计的启发是：dense teacher signal 不能只看局部 token-level KL；它还要和全局 outcome reward 对齐。这其实是 OPD 的一个基本张力：token-level supervision 很 dense，但任务目标往往是 sequence-level。好的 OPD 目标需要在这两者之间建立校准关系。

## 9. Rethinking OPD：目标函数再漂亮，也要看 teacher-student 是否可对齐

论文：Rethinking On-Policy Distillation of Large Language Models: Phenomenology, Mechanism, and Recipe

这篇文章不是直接提出新 divergence，但它非常适合作为 reward/divergence 变式的背景分析。它系统研究 OPD 什么时候成功、什么时候失败，并提出两个条件：student 和 teacher 需要有 compatible thinking patterns；即使 thinking pattern 一致，teacher 也必须提供 student 训练中没有见过的新能力【0†L22-L25】。

更细粒度地，它发现成功 OPD 体现为 student-visited states 上 high-probability tokens 的 progressive alignment，而且一个很小的 shared token set 可以集中 97%–99% 的概率质量【0†L22-L25】。

这对 reward/divergence 变式有一个现实提醒：不是所有 teacher signal 都能靠换 loss 解决。OPD 首先需要 teacher 和 student 在 student-visited states 上有可对齐的局部 token support。换句话说，G-OPD、Entropy-Aware、AOPD、Veto 都在改目标函数，但目标函数能发挥作用的前提，是 student 的 rollout 仍然落在 teacher 可以提供有效 dense guidance 的区域。如果 teacher 和 student 的 thinking pattern 完全不兼容，再复杂的 $\lambda$、KL 混合或 target reformulation 也可能只是缓解，而不是根治。

## 10. AlignDistil：稍早一点，但非常值得放进这条线

论文：AlignDistil: Token-Level Language Model Alignment as Adaptive Policy Distillation

AlignDistil 不是最近半年内的 OPD 新作，但它和 reward/divergence 变式高度相关。它把 RLHF / DPO 学到的 reward 引入 token-level distillation，并证明相关目标可以等价为一种 token-level distillation process，其中 teacher distribution 由 DPO model 和 reference model 的 logits 线性组合而成。它还提出 token-adaptive logit extrapolation，用来避免不同 token 上的 under-optimization 和 over-optimization【0†L25-L27】。

为什么它值得放进这条线？因为它很早就提出了一个和 G-OPD 类似的思路：alignment reward 可以被转写成 token-level distillation target。G-OPD 从 OPD 推导到 dense KL-constrained RL；AlignDistil 则从 RLHF / DPO reward 推回 token-level distillation。两者方向不同，但都在说明同一件事：distillation 和 reward optimization 之间的边界正在变模糊。

## 11. On-policy preference learning：理论上为什么 on-policy signal 会越来越好？

论文：Coverage Improvement and Fast Convergence of On-policy Preference Learning

这篇不是传统 OPD，但值得作为理论背景。它分析 online on-policy preference learning 为什么能显著优于 offline 对应方法。核心观点是 coverage improvement principle：如果 batch size 足够，每次 on-policy update 会把 policy 移动到目标附近 coverage 更好的区域，从而让后续数据越来越 informative，并带来快速收敛【0†L27-L29】。

它还证明，在 contextual bandit + Bradley-Terry preferences + linear softmax policy class 下，on-policy DPO 在满足 generalized coverage threshold 时可以指数收敛；相比之下，只能用 initial policy 离线样本的 learner 会有更慢的 minimax rate【0†L27-L29】。

这和 OPD 的关系是：OPD 之所以有吸引力，不只是因为 teacher 给 dense reward，还因为 policy 更新后访问的状态会变，后续 supervision 的信息量也会变。但这也提醒我们：on-policy 是动态系统。reward / divergence 设计不只是影响当前 batch 的 loss，也会改变下一轮 student 会访问什么状态。这就是为什么 $\lambda$、KL 方向、entropy handling、calibration 都会产生连锁效应。

## 12. 这条线的统一图景：OPD 目标函数正在被“模块化”

把这些工作放在一起，可以看到一个非常清晰的趋势：OPD 不再是一个固定 loss，而是一组可设计的模块。可以把它们放到下面这个表里：

| 模块                   | 原始 OPD 默认选择                   | 最近工作怎么改                                        | 代表论文            |
| ---------------------- | ----------------------------------- | ----------------------------------------------------- | ------------------- |
| reward scale           | 固定 $\lambda = 1$                  | $\lambda < 1$ 插值，$\lambda > 1$ 外推                | G-OPD / ExOPD       |
| reference              | 固定或默认 student base             | 用 teacher pre-RL base 做 reward correction           | G-OPD / ExOPD       |
| target distribution    | 直接 teacher logits                 | logit-space intermediate bridge                       | Veto                |
| KL 方向                | 主要 reverse KL                     | teacher 高熵时加入 forward KL                         | Entropy-Aware OPD   |
| advantage region       | 同一套 advantage update             | 正 advantage 用 RL，非正 advantage 用 local imitation | AOPD                |
| extrapolation boundary | 手动扫 $\lambda$                    | 推导 structured-output 安全阈值                       | Extrapolation Cliff |
| confidence target      | 跟随 teacher-conditioned confidence | 用 empirical confidence 替换                          | CaOPD               |
| token-level vs outcome | token KL 独立优化                   | 用 outcome reward 校准 token guidance                 | Uni-OPD             |

所以这条线最核心的变化是：大家不再问“要不要 OPD”，而是在问 **“OPD 的 dense signal 应该被解释成哪种 reward、哪种 target、哪种 divergence”**。