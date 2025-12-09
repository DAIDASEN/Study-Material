**我先用中文帮你把这份 “Using Auxiliary Data（使用辅助信息）” 的核心知识串起来，所有符号尽量跟你 Lecture / Tutorial 一致。公式我会直接写，用来理解就好；等你需要“考试答案版 Markdown cheat sheet”的时候，我们再单独做英文版。**

**一、大图：为什么要用 Auxiliary Variable（辅助变量）**

课程里默认的基本情形是：
 • 要估计某个变量 $Y$ 的总体总量/均值（$\tau_y, \mu_y$），只用到抽样观测的 $Y_1,\dots,Y_n$。
 • 但是有时存在另一个变量 $X$：
 – 和 $Y$ 强相关（线性、正相关）
 – 而且 **更便宜/更容易** 测量，甚至**全体都已知**（$\tau_x$ 或 $\mu_x$ 已知）。

这种 $X$ 就叫辅助变量（auxiliary variable）。思路是：

> 利用 $X$ 帮助预测 $Y$，从而减小估计量的方差（更精准），有时还能避免需要知道 $N$。

在这份讲义里，主要有三块：

1. SRS 下的 Ratio Estimation（比率估计）
2. Cluster Sampling（整群抽样）里的 Ratio Estimation（一段、两段整群）
3. SRS 下的 Regression Estimation（回归估计）

**二、SRS 下的 Ratio Estimation（比率估计）**

**2.1 设置与记号**

每个总体单位有两条观测：$y_i$ 和 $x_i$。
 • $y_i$：目标变量（我们想估计 $\tau_y, \mu_y$）。
 • $x_i$：辅助变量，和 $y_i$ 强相关，且总体信息（$\tau_x$ 或 $\mu_x$）已知。

总体层面有：
 • $\tau_y = \sum_{i=1}^N y_i,\quad \tau_x = \sum_{i=1}^N x_i$
 • $\mu_y = \tau_y / N,\quad \mu_x = \tau_x / N$

定义总体比率：
 • $R = \dfrac{\tau_y}{\tau_x} = \dfrac{\mu_y}{\mu_x}$

样本里（SRS）有：
 • 样本均值：$\bar{y} = \dfrac{1}{n}\sum_{i=1}^n y_i,\quad \bar{x} = \dfrac{1}{n}\sum_{i=1}^n x_i$

**2.2 比率估计量的定义**

1）比率本身的估计量
 • $\hat{R} = \dfrac{\bar{y}}{\bar{x}}$

2）用比率估计总体总量 $\tau_y$、总体均值 $\mu_y$

• 总量的 ratio estimator
 $\hat{\tau}_r = \hat{R}\tau_x = \dfrac{\bar{y}}{\bar{x}}\tau_x$

• 均值的 ratio estimator
 $\hat{\mu}_r = \hat{R}\mu_x = \dfrac{\bar{y}}{\bar{x}}\mu_x$

注意：比率估计 **不需要知道 $N$**，只要知道 $\tau_x$ 或 $\mu_x$。这在讲义里用“糖分 / 橙子重量”例子强调过。

**2.3 方差估计的核心结构**

关键量：
 • 定义新的变量 $Z_i = y_i - R x_i$，可以证明 $\mathbb{E}(Z_i)=0$。
 • 它的总体方差：$\sigma_r^2 = \dfrac{1}{N}\sum_{i=1}^N (y_i - R x_i)^2$

在 SRS 下，$Z_i$ 也等价于从总体 $Z$ 做 SRS，所以套用普通 SRS 的方差公式：

1）均值的理论方差近似
 • $\operatorname{Var}_d(\hat{\mu}_r) \approx \dfrac{N-n}{N-1}\dfrac{1}{n}\sigma_r^2$

• 用样本估计：
 $\hat{\sigma}_r^2 = \dfrac{1}{n-1}\sum_{i=1}^n (Y_i - \hat{R}X_i)^2$（注意分母是 $n-1$）
 $\widehat{\operatorname{Var}}_d(\hat{\mu}_r) = \left(1-\dfrac{n}{N}\right)\dfrac{1}{n}\hat{\sigma}_r^2$

2）总量的理论方差近似
 • $\operatorname{Var}_d(\hat{\tau}_r) \approx \dfrac{N-n}{N-1}\dfrac{N^2}{n}\sigma_r^2$

• 样本估计：
 $\widehat{\operatorname{Var}}_d(\hat{\tau}_r) = \dfrac{N-n}{N}\dfrac{N^2}{n}\hat{\sigma}_r^2$

3）比率 $R$ 的方差

• $\operatorname{Var}_d(\hat{R}) \approx \dfrac{1}{\mu_x^{2}}\dfrac{N-n}{N-1}\dfrac{1}{n}\sigma_r^2$

• 样本估计：
 $\widehat{\operatorname{Var}}_d(\hat{R}) = \dfrac{1}{\mu_x^{2}}\left(1-\dfrac{n}{N}\right)\dfrac{1}{n}\hat{\sigma}_r^2$

（你在 Tutorial Notes 里看到的是等价写法，把 $\sigma_r^2$ 展开成 $\sigma_y^2, \sigma_x^2, \rho$ 的形式。）

**2.4 Ratio vs 普通 SRS 估计：什么时候“更好”**

对比两种均值估计的方差：
 • 普通 SRS：$\widehat{\operatorname{Var}}_d(\bar{Y}) = \left(1-\dfrac{n}{N}\right)\dfrac{\hat{\sigma}_y^2}{n}$
 • Ratio：$\widehat{\operatorname{Var}}_d(\hat{\mu}_r) = \left(1-\dfrac{n}{N}\right)\dfrac{\hat{\sigma}_r^2}{n}$

所以 ratio 更好 ⇔ $\hat{\sigma}_r^2 \ll \hat{\sigma}_y^2$。讲义和 Tutorial 给出了展开公式：
 • $\hat{\sigma}_r^2 = \hat{\sigma}_y^2 + \hat{R}^2\hat{\sigma}_x^2 - 2\hat{R}\hat{\rho}\hat{\sigma}_x\hat{\sigma}_y$
 • 再配合系数变异（CV）：$\hat{cv,x} = \dfrac{\hat{\sigma}_x}{\bar{x}}$，$\hat{cv,y} = \dfrac{\hat{\sigma}_y}{\bar{y}}$

Tutorial 给出的一个条件是：
 如果样本相关系数 $\hat{\rho}$ 满足
 $$\hat{\rho} \gg \frac{1}{2}\frac{\hat{cv,x}}{\hat{cv,y}},$$
 那么 $\hat{\sigma}_r^2 \ll \hat{\sigma}_y^2$，比率估计是一个好选择。

特别地，如果 $\hat{cv,x}$ 和 $\hat{cv,y}$ 差不多，那么只要 $\hat{\rho} > 0.5$ 左右，ratio 就通常优于普通 SRS。

**直观记忆：**

1. $X$ 和 $Y$ 要有 **强烈正线性关系**；
2. 散点图看起来接近一条穿过原点的直线；
3. CV 相近、相关系数大 → ratio 好。

**三、Cluster Sampling 里的 Ratio Estimation（$M_i$ 做辅助）**

Tutorial 的第 2 部分就是把 ratio 用到整群抽样上。

**3.1 一段整群（One-Stage Cluster）**

设总体有 $N$ 个群（cluster），第 $i$ 群大小为 $M_i$，群总量 $Y_i$：
 • $M_i =$ 群大小（元素个数）
 • $Y_i =$ 群中 $Y$ 的总和

我们通常 **知道所有的 $M_i$**，或者至少知道 $M = \sum_{j=1}^N M_j$。这里把 $M_i$ 当作辅助变量。

从 $N$ 个群中 SRS 选出 $n$ 个群，观测它们的 $Y_i, M_i$。
 • 样本均值：$\bar{Y} = \dfrac{1}{n}\sum_{i=1}^n Y_i,\ \bar{M} = \dfrac{1}{n}\sum_{i=1}^n M_i$
 • 定义比率 $R = \dfrac{\tau_y}{M}$，估计量 $\hat{R} = \dfrac{\bar{Y}}{\bar{M}}$

**总体总量的比率估计量：**
 • $\hat{\tau}_r = \hat{R} M = \dfrac{\bar{Y}}{\bar{M}} M$

**方差估计：**
 • $\widehat{\operatorname{Var}}_d(\hat{\tau}_r) = N(N-n)\dfrac{1}{n}\hat{\sigma}_r^2$
 • 其中 $\hat{\sigma}_r^2 = \dfrac{1}{n-1}\sum_{i=1}^n (Y_i - \hat{R}M_i)^2$（分母 $n-1$）

**群比例的比率估计量：**（Tutorial 里的 $p_r$）
 • $A_i$ = 群内“有某种特征”的个数
 • $p_r$ 的估计：$\hat{p}_r = \dfrac{\sum_{i=1}^n A_i}{\sum_{i=1}^n M_i}$
 • 方差估计：$\widehat{\operatorname{Var}}_d(\hat{p}_r) = \dfrac{N-n}{N}\dfrac{N^2}{M^2}\dfrac{\hat{\sigma}_r^2}{n}$，其中同样 $\hat{\sigma}_r^2 = \dfrac{1}{n-1}\sum_{i=1}^n (A_i - \hat{p}_r M_i)^2$（具体形式见 Tutorial）。

**直观记忆：**
 • 一段整群里，$M_i$ 是“群大小”，类似 $X_i$；$Y_i$ 是“群总量”。
 • 用 ratio：就是假设 $Y_i \approx R M_i$，线性通过原点。

**3.2 两段整群（Two-Stage Cluster）**

两段整群时，每个群内部还再抽一层样本。记号按 Tutorial：
 • 群 $i$ 的大小：$M_i$
 • 在群 $i$ 中抽 $m_i$ 个二级单位，得到样本均值 $\bar{Y}_i$，于是群总量估计为 $\hat{Y}_i = M_i \bar{Y}_i$

总体所有单位总数：$M = \sum_{i=1}^N M_i$（已知或可估）。样本选 $n$ 个群。

**总体均值的比率估计量：**
 • $\hat{\mu}_r = \dfrac{\sum_{i=1}^n M_i \bar{Y}_i}{\sum_{i=1}^n M_i} = \dfrac{\sum_{i=1}^n \hat{Y}_i}{\sum_{i=1}^n M_i}$

**方差估计（结构要记）：**

Tutorial 给出的形式是“群间 + 群内”两部分：
 $$\widehat{\operatorname{Var}}_d(\hat{\mu}_r) = \frac{1}{M^2}\left{N(N-n)\frac{1}{n}\hat{\sigma}*r^2 + \frac{N}{n}\sum*{i=1}^n M_i(M_i - m_i)\frac{1}{m_i}\hat{\sigma}_i^2\right}$$

其中：
 • $\hat{\sigma}_r^2 = \dfrac{1}{n-1}\sum_{i=1}^n (\hat{Y}_i - \hat{\mu}_r M_i)^2$：群间变异
 • $\hat{\sigma}_i^2$：群 $i$ 内的样本方差（带分母 $m_i-1$ 的那种）

**记忆技巧：**
 • 第一项 $N(N-n)\dfrac{1}{n}\hat{\sigma}_r^2$ = 群间抽样带来的方差（类似一段整群）。
 • 第二项是群内二次抽样带来的额外方差：和 $M_i(M_i - m_i)$、$\hat{\sigma}_i^2$ 有关。

**四、SRS 下的 Regression Estimation（回归估计）**

Regression Estimation 可以看作是“有截距的比率估计”（更一般的线性关系）。Tutorial 有一句话直接说了这一点。

**4.1 模型和估计 a, b**

假设总体中 $X,Y$ 有线性关系：
 • $Y_i = a + b X_i + \varepsilon_i,\quad \varepsilon_i \sim N(0,\sigma^2)$

在样本 $(x_i,y_i)$ 上做最小二乘回归（LS），估计 $a,b$：
 • $\hat{b} = \dfrac{S_{XY}}{S_{XX}} = \dfrac{\sum_{i=1}^n (x_i - \bar{x})(y_i - \bar{y})}{\sum_{i=1}^n (x_i - \bar{x})^2}$
 • $\hat{a} = \bar{y} - \hat{b}\bar{x}$

**4.2 回归估计量（总体均值）**

已知 $\mu_x$ 时，用回归估计总体均值 $\mu_y$：
 • $\hat{\mu}_L = \hat{a} + \hat{b}\mu_x = \bar{y} + \hat{b}(\mu_x - \bar{x})$

可以和 ratio 做对比：
 • ratio：$\hat{\mu}_r = \dfrac{\bar{y}}{\bar{x}}\mu_x$（强迫直线过原点）
 • regression：$\hat{\mu}_L = \bar{y} + \hat{b}(\mu_x - \bar{x})$（允许有截距）

**4.3 方差估计与置信区间**

Tutorial 给出：
 • $\widehat{\operatorname{Var}}_d(\hat{\mu}_L) = \frac{N-n}{Nn}\cdot\frac{1}{n-2}\sum_{i=1}^n (Y_i - \hat{a} - \hat{b}X_i)^2$

也可以近似写为：
 • $\approx \dfrac{N-n}{Nn}\sigma_y^2(1-\hat{\rho}^2)$（你 Tutorial 里有说明 “derive it when you use it”）

构造 $(1-\alpha)100%$ 置信区间：
 • $\hat{\mu}_L \pm t_{n-2,1-\alpha/2}\sqrt{\widehat{\operatorname{Var}}_d(\hat{\mu}_L)}$

注意自由度是 $n-2$。

**4.4 Ratio vs Regression：何时用哪个？**

结合 Lecture 的观点：

1. 看散点图 $Y$ vs $X$：

 • 如果点云大致是一条 **穿过原点** 的直线 → ratio 更合适。
 • 如果明显有 **截距**（不过原点）、但整体线性很强 → regression 更好。

2. 两者都是 **有偏估计**（在 SRS 下），但大样本时偏差较小，因此我们主要用 MSE ≈ Var 来比较哪个更优。
3. 经验上：

 • 强线性关系 $\Rightarrow$ regression 通常比简单 SRS 好很多；
 • 如果还同时满足“过原点”，ratio 有时会更简单；
 • 很多考试题会让你算 **三种估计**：普通 SRS、ratio、regression，然后比较哪个方差更小。

**五、和考试题的对应关系（你在 Tutorial 里会遇到的）**

你 Tutorial 里这些题目基本都围绕：

1. 给 SRS 总体、给出样本统计量（$\bar{x},\bar{y},\hat{\sigma}_x^2,\hat{\sigma}_y^2,\hat{\sigma}_{xy}$），问：

 • 普通 SRS 下 $\hat{\mu}_y, \widehat{\operatorname{Var}}_d(\hat{\mu}_y)$
 • Ratio estimator $\hat{\mu}_r, \widehat{\operatorname{Var}}_d(\hat{\mu}_r)$
 • Regression estimator $\hat{\mu}_L, \widehat{\operatorname{Var}}_d(\hat{\mu}_L)$
 • 比较谁的方差最小，说明原因（用 $\hat{\rho}, \hat{cv,x}, \hat{cv,y}$ 的条件）。

2. 给死树数、收入等例子，通常已知 $\tau_x$ 或 $\mu_x$，又给了一组 $(x_i,y_i)$：

 • 要你用 ratio estimator 估计 $\tau_y$ 或 $\mu_y$，并给 95% CI。

3. 整群 + ratio：

 • 已知各群 $M_i$ 或总 $M$，抽取一些群并测 $Y_i$；
 • 按照一段整群 ratio 公式算 $\hat{\tau}_r$、估计 Var 和 CI；
 • 或两段整群里，用群间 + 群内两部分方差。

4. 理论推导题：

 • 证明 $\hat{\tau}_L = aN + b\tau_x$ 这种形式；
 • 证明给出的方差公式（把 regression 的残差平方和整理出来）。
