### Stochastic Process

Definition: A collection of random variables $\{X_t\}_{t\in T}$
<font color=green>*Geometric series:*</font>$\sum_{i=0}^\infin ar^i=\frac{a}{1-r},\ |r|<1$
<font color=green>*Generalized Binomial Theorem:*</font> $(x+y)^{-n}= \sum_{k=0}^\infin C_{n+k-1}^k(-x)^{-k}y^{-n-k}$
<font color=green>*Transformation of random variables*</font> If $f_Y(y) = f_X(h(y))$ and $f_Y(y) = f_X(h(y)) \left| \det(J_h(y)) \right|$ 其中我们有$\begin{pmatrix} \frac{\partial h_1}{\partial y_1} & \cdots & \frac{\partial h_1}{\partial y_n} \\ \vdots & \ddots & \vdots \\ \frac{\partial h_n}{\partial y_1} & \cdots & \frac{\partial h_n}{\partial y_n} \end{pmatrix}.$

### Bernoulli Process

<font color=blue>**Bernoulli distribution**</font>: $X\sim Bern(p)$, pmf: $P(X = 1) = p,\ P(X = 0) = 1-p$, mgf: $M_X(t) = pe^t+1-p$
**Bernoulli Process** A sequence $\{X_1,X_2,...\}$ of independent Bernoulli variables with $X_i\sim Bern(p)$ 
<font color=Green>**Number of success by time $n$**: </font>==$S_n=X_1+....+X_n$==
<font color=blue>**Binomial distribution: **</font>$S_n\sim B(n,p)$ pmf: $P(S_n=k)= C^k_np^k(1-p)^{n-k},\ for\ k= 0,...,n$, mgf: $M_{S_n}(t)=(pe^t+1-p)^n$
<font color=Green>**$k-th$ time of success:** </font>==$T_k = min\{n:S_n=k\}$==
<font color=blue>**Geometric Distribution: **</font> represents the **first success time** in a Bernoulli process, that is $T_1\sim Geo(p)$. pmf: $P(T_1=n) = (1-p)^{n-1}p$ $E[T_1] = \frac1p, Var[T_1] = \frac{1-p}{p^2}$ and $M_{T_1}(t) = \frac{pe^t}{1-(1-p)e^t}$
<font color=blue>**Negative binomial distribution: **</font>represents the **$r$-th success time**, that is $T_r\sim NB(r,p)$. pmf: $P(T_r=n) = C^{r-1}_{n-1}(1-p)^{n-r}p^r$. $E[T_r] = \frac rp, Var[T_r] = r\frac{1-p}{p^2},\ M_{T_r}(t) = \left( \frac{pe^t}{1-(1-p)e^t} \right)^r$
<font color=green>**i.i.d. waiting times between successes: **</font>Denoting $W_i = T_i-T_{i-1}$, Then $\mathbb{P}(W_1=n_1,\ W_2=n_w,...,W_k=n_k)=\Pi_{i=0}^\infin \mathbb{P}(W_i=n_i) $ (memoryless propert)
**<font color=Green>Law of large number:</font>** Frequency and probability. $\lim_{n \to \infty} \frac{S_n}{n} = p$ 
For discrete case: $\mathbb{E}\left[\lim_{n \to \infty} \frac{S_n}{n}\right] = \lim_{n \to \infty} \mathbb{E}\left[\frac{S_n}{n}\right] = p$ and 
$\text{Var}\left[\lim_{n \to \infty} \frac{S_n}{n}\right] = \lim_{n \to \infty} \text{Var}\left[\frac{S_n}{n}\right] = 0$

### Poisson Process

<font color=green>**From Bernoulli (Counting Process) to Poisson**</font>: 
考虑到时间$k$成功的次数$S_k$，对于Bernoulli只会在整数的时间点更新 $\Rightarrow$更加频繁的做实验，$k/m$时间里做$k$个实验，$S_{k/m}^{(m)}\sim B(k, p/m)$ $\Rightarrow$ $m\rightarrow \infin$,  limiting process ${S^{lim}_t }$, 取$t=1$符合Poisson分布。$$\begin{aligned}
\mathbb{P}(S_{1}^{\text{lim}}=k) &= \lim_{m \to \infty} \mathbb{P}(S_{1}^{(m)}=k) = \lim_{m \to \infty} C_{m}^{k}\left(\frac{p}{m}\right)^{k}\left(1-\frac{p}{m}\right)^{m-k} \\
&= \lim_{m \to \infty} \frac{m!}{(m-k)!k!} \cdot \frac{p^{k}}{m^{k}}\left(1-\frac{p}{m}\right)^{m} \cdot \left(1-\frac{p}{m}\right)^{-k} \\
&= \frac{p^{k}}{k!} \lim_{m \to \infty} \left(1-\frac{p}{m}\right)^{m} \cdot \frac{m(m-1)\cdots(m-k+1)}{(m-p)^{k}} \\
&= \frac{p^{k}}{k!}e^{-p}.
\end{aligned}$$

<font color=blue>**Poisson Distribution: **</font>$X\sim Pois(\lambda)$, $P(X=k) = \frac{\lambda^k}{k!}e^{-\lambda},\ for\ k\geq0$
$E[X] = \lambda$, $Var(X)=\lambda$ and $M_X(t)= e^{\lambda(e^t-1)}$
**Properties 1 (Independent Increment)**: $S_t^{(m)} - S_s^{(m)} \perp \{S_r^{(m)}\}_{r \le s}$
**Properties 2 (Stationary Increment):** $S_t^{(m)} - S_s^{(m)} \stackrel{d}{=} S_{t-s}^{(m)}$
<font color=Green>**Definition:**</font>
A counting process $\{N_t\}_{t \geq 0}$ is called a Poisson process with rate $\lambda > 0$ if it satisfies the following properties: for all $s \leq t$, 1. $N_0 = 0$. 2. independent increment: $N_t - N_s \perp N_r \, \text{for} \, r < s$. 3. stationary increments: $N_t - N_s \sim \text{Pois}(\lambda (t - s))$.
<font color=green>**First arrival time: **</font>==$T_1 \sim \text{Exp}(\lambda)$==
**<font color=blue>Exponential Distribution: </font>**
cdf: 通过“直到时间 $t$ 都没有事件发生”这一逻辑推导：$F_{T_1}(t) = \mathbb{P}(T_1 \le t) = \mathbb{P}(N_t > 0) = 1 - e^{-\lambda t}$，对于 $t \ge 0$。
pdf: 对 cdf 求导得到 $f_{T_1}(t) = \lambda e^{-\lambda t}$，对于 $t \ge 0$。
Properties: $E[T_1] = \frac{1}{\lambda}$，$Var(T_1) = \frac{1}{\lambda^2}$ 且 $M_{T_1}(t) = \frac{\lambda}{\lambda - t}$。
Memoryless property: $\mathbb{P}(T_1 > t + s | T_1 > s) = \mathbb{P}(T_1 > t)$。这意味着已经过去的时间不会影响未来事件发生的概率，这一性质与离散情形下的 $Geo(p)$ 一致。
<font color=green>**$r$-th arrival time:** </font>==$T_r \sim \text{Gamma}(r, \lambda)$==
我们在研究泊松过程中第 $r$ 个事件发生的时间 $T_r$。这可以看作是 $r$ 个独立的、参数为 $\lambda$ 的等待时间（即间期间隔 $W_i$）的总和。
<font color=blue>**Gamma Distribution (Erlang Distribution)**: </font>  
cdf: $F_{T_r}(t) = \mathbb{P}(N_t \ge r) = 1 - \sum_{i=0}^{r-1} \frac{(\lambda t)^i}{i!}e^{-\lambda t}$，对于 $t \ge 0$。
pdf: 对 cdf 求导得到 $f_{T_r}(t) = \frac{\lambda^r t^{r-1} e^{-\lambda t}}{(r-1)!}$，对于 $t \ge 0$。
Properties: $E[T_r] = \frac{r}{\lambda}$，$Var(T_r) = \frac{r}{\lambda^2}$ 且 $M_{T_r}(t) = \left( \frac{\lambda}{\lambda - t} \right)^r$。这与伯努利过程中的负二项分布 $NB(r, p)$ 形成直接对应。
<font color=red>Allow $r$ to take non-integer values</font>: 定义$\Gamma(r) := \int_{0}^{\infty} t^{r-1} e^{-t} dt$
其中$\Gamma(r) = (r-1)!$, $\Gamma(r+1) = r\Gamma(r)$, $\Gamma(1) = 1\ \Gamma(\frac{1}{2}) = \sqrt{\pi}$
$f_X(x) = \frac{\lambda^r x^{r-1} e^{-\lambda x}}{\Gamma(r)}$并且$E[T_r] = \frac{r}{\lambda}$ $\text{Var}(T_r) = \frac{r}{\lambda^2}$和$M_{T_r}(t) = \left( \frac{\lambda}{\lambda - t} \right)^r$

<font color=green>**i.i.d. waiting times between arrivals:** </font>
<font color=blue>1. Joint distribution</font>
$\mathbb P(T_1<t_1,\ T_2<t_2)=\mathbb P(N(t_1)>0,\ N(t_2)>1)$ if $t_1\ge t_2$ 那么 $\mathbb P(N(t_1)>0,\ N(t_2)>1)=\mathbb P(N(t_2)>1)=1-\mathbb P(N(t_2)=0)-\mathbb P(N(t_2)=1)
=1-e^{-\lambda t_2}-\lambda t_2 e^{-\lambda t_2} $
if $t_1<t_2$ 那么$=\mathbb P(N(t_1)=1,\ N(t_2)>1)+\mathbb P(N(t_1)>1) = \mathbb P(N(t_1)=1,\ N(t_2)-N(t_1)>0)+\mathbb P(N(t_1)>1)\\=\mathbb P(N(t_1)=1)\cdot \mathbb P(N(t_2)-N(t_1)>0)+1-\mathbb P(N(t_1)=0)-\mathbb P(N(t_1)=1)=\lambda t_1 e^{-\lambda t_1}\bigl(1-e^{-\lambda (t_2-t_1)}\bigr)+1-e^{-\lambda t_1}-\lambda t_1 e^{-\lambda t_1}\\=1-e^{-\lambda t_2}-\lambda t_2 e^{-\lambda t_2}$
pdf: $f_{T_1,T_2}(t_1,t_2)=\lambda^2 e^{-\lambda t_2},\quad 0<t_1<t_2$

<font color=blue>2. Waiting time i.i.d.:</font>
$  f_{T_1, T_2 - T_1}(t_1, t_2) = f_{T_1, T_2}(t_1, t_1 + t_2) = \lambda^2 e^{-\lambda(t_1 + t_2)}, \quad \text{对于 } t_1, t_2 > 0.
$
$  f_{T_1}(t_1) = \lambda e^{-\lambda t_1} \quad \text{和} \quad f_{T_2-T_1}(t_2) = \lambda e^{-\lambda t_2}, \quad \text{对于 } t_1, t_2 > 0$
**<font color=green>Principle of superposition: </font>** If $\{N^{(1)}\}_t, \cdots, \{N^{(k)}\}_t$ are independent Poisson processes with rates $\mu_1, \cdots, \mu_k$, then $\{N^{(1)} + \cdots + N^{(k)}\}_t$ is a Poisson process with rate $\mu_1 + \cdots + \mu_k$.

**<font color=green>Principle of thinning: </font>**If $N_t$ is a Poisson process with rate $\mu$, and if each arrival is independently assigned one of $k$ labels with probabilities $p_1, \cdots, p_k$, then the counting processes $\{N_t^{(1)}\}, \cdots, \{N_t^{(k)}\}$ that count the arrivals of each type are independent Poisson processes with rates $p_1\mu, \cdots, p_k\mu$.

### Simple Random Walk and Brownian Motion

#### 1. Simple Random Walk (SRW)

一维随机游走描述了一个质点在直线上依概率随机移动的过程。

**Definition**: 随机游走 $\{S_n\}_{n \ge 0}$ 定义为 $S_n = S_0 + X_1 + \dots + X_n$ ，其中 $X_i$ 是独立同分布（i.i.d.）的随机变量 。

**Symmetric SRW**: 当 $S_0$ 为整数且步长 $X_i \in \{1, -1\}$，且 $P(X_i = 1) = P(X_i = -1) = \frac{1}{2}$ 时，称为对称简单随机游走 。

**Properties**: 若 $S_0 = 0$，则对于对称 SRW 有：
$\mathbb{E}[S_n] = 0$  $Var(S_n) = n$ 

#### 2. Continuous Time Limit (From SRW to BM)

为了得到连续时间下的过程，我们对步长和时间间隔进行缩放。==Mean和Variance要和原来的一致==

**Scaling**: 考虑在单位时间内进行 $N$ 次实验，为了保持方差不发散，步长需缩放为 $\frac{1}{\sqrt{N}}$ 。定义缩放后的过程为：
$$S_t^{(N)} = \frac{1}{\sqrt{N}} \sum_{i=1}^{\lfloor Nt \rfloor} X_i^{(N)}$$

**Limiting Distribution**: 当 $N \to \infty$ 时，根据矩母函数（mgf）推导 ：
$$M_{S_1^{(N)}}(t) = \left( \frac{e^{t/\sqrt{N}} + e^{-t/\sqrt{N}}}{2} \right)^N \to e^{t^2/2}$$
这表明 $S_1^{(N)}$ 在极限下服从标准正态分布 $N(0, 1)$ 。

#### 3. Brownian Motion (BM)

**Definition**: 一个连续过程 $\{B_t\}_{t \ge 0}$ 称为标准布朗运动，若其满足：
$B_0 = 0$ 。

**Independent Increments**: 对于任意 $s \le t$，增量 $B_t - B_s$ 独立于历史过程 $\{B_r\}_{r \le s}$ 。

**Stationary Increments**: 增量 $B_t - B_s \sim N(0, t-s)$ 。

**Joint Distribution**: 布朗运动在不同时间点 $(B_{t_1}, B_{t_2}, \dots, B_{t_n})$ 的联合分布是联合正态分布（Jointly Normal） ，其均值为 $0$，协方差矩阵 $\Sigma$ 满足 $\Sigma_{ij} = Cov(B_{t_i}, B_{t_j}) = \min(t_i, t_j)$ 。
PDF 中的协方差矩阵表示为 $Cov(B_{t_i}, B_{t_j}) = t_i$ (若 $t_i < t_j$) 。

#### 4. Normal Distribution & Central Limit Theorem (CLT)

布朗运动的理论基础是正态分布的普适性。

**Normal Distribution**: $X \sim N(\mu, \sigma^2)$ 的 pdf 为 $f_X(x) = \frac{1}{\sqrt{2\pi\sigma^2}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}$ 。
其 mgf 为 $M_X(t) = e^{\mu t + \frac{1}{2}\sigma^2 t^2}$ 。

**Joint Normal Distribution**: $X = (X_1, X_2, \dots, X_n)$ 是联合正态分布如果 $\sum_{i=1}^n a_i X_i$ 对于所有 $a_1,\dots,a_n \in \mathbb{R}$ 都是正态分布。记作 $\mathbf{X} \sim \mathbf{N}(\mu, \mathbf{\Sigma})$，其中 $\mathbb{E}[\mathbf{X}] = \mu$，协方差矩阵为 $\mathbf{\Sigma}$。
$f_{B_{t_1}, B_{t_2} - B_{t_1}, \cdots, B_{t_n} - B_{t_{n-1}}}(x_1, \Delta x_2, \cdots, \Delta x_n)=\frac{1}{\sqrt{2\pi t_1}} e^{-\frac{x_1^2}{2t_1}} \frac{1}{\sqrt{2\pi(t_2 - t_1)}} e^{-\frac{\Delta x_2^2}{2(t_2 - t_1)}} \cdots \frac{1}{\sqrt{2\pi(t_n - t_{n-1})}} e^{-\frac{\Delta x_n^2}{2(t_n - t_{n-1})}}$

**Characterization of Brownian Motion**: 对于 $t_1 \leq t_2 \leq \dots \leq t_n$，有：
$$f_{B_{t_1},B_{t_2},\dots,B_{t_n}}(x_1,x_2,\dots,x_n) = \frac{1}{\sqrt{(2\pi)^n t_1(t_2-t_1)\cdots(t_n-t_{n-1})}} \exp\left(-\frac{x_1^2}{2t_1} - \frac{(x_2-x_1)^2}{2(t_2-t_1)} - \cdots - \frac{(x_n-x_{n-1})^2}{2(t_n-t_{n-1})}\right)$$

**Central Limit Theorem**: 设 $\{X_k\}$ 为 i.i.d. 随机变量，且具有有限均值 $\mu$ 和方差 $\sigma^2$ 。当 $n \to \infty$ 时，其样本均值 $\bar{X}$ 的标准化形式收敛于标准正态分布：
$$W = \frac{\bar{X} - \mu}{\sigma/\sqrt{n}} \xrightarrow{d} N(0, 1)$$
这意味着无论原始分布如何，大量独立随机变量之和（经过适当缩放）总趋向于正态分布 。