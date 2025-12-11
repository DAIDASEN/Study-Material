<font color=blue>**Covariance:**</font> $Cov(X, Y) = E[XY]-E[X][Y]$ $Cov(aX,bY) = abCov(X,Y)\ Cov(X_1+X_2,Y) = Cov(X_1,Y)+Cov(X_2,Y)$
<font color=blue>**Correlation: **</font>$Corr(X, Y) = \frac{Cov(X, Y)}{\sqrt{Var(X)Var(Y)}}\ Corr(aX+b, cY+d) = Corr(X, Y)$
$\frac{1}{1-x} = \sum_{n=0}^{\infin}x^n$
$\frac{1}{1+x} = \sum_{n=0}^{\infin}(-1)^nx^n$
$\Pi_{i=1}^{p}\frac1{a_{i}}=\sum_{i=1}^p\frac{c_i}{a_i}$
<font color=blue>**Taylor's Formula: **</font>$f(x) = f(a) + \frac{f'(a)}{1!}(x-a) + \frac{f''(a)}{2!}(x-a)^2 + \cdots + \frac{f^{(n)}(a)}{n!}(x-a)^n + R_n(x)$
**<font color=blue>Stationary: </font>** $MA$天然Stationary, $AR\ 1-\phi B$没有根在单位圆上 1. $\mu=E(Y_t)=c$ 2. $\gamma(k) = Cov(Y_t,Y_{t+k})$ only depends on k
**<font color=blue>Causality</font>**: AR 特征方程的根在单位圆外 
<font color=blue>**Invertibility**</font> MA 特征方程的根在单位圆外
<font color=blue>**Inverse Matrix**</font>  若 $A=\begin{pmatrix} a & b \\ c & d \end{pmatrix}$，则$
A^{-1} = \frac{1}{|A|}
\begin{pmatrix}
d & -b \\
-c & a
\end{pmatrix},
\quad |A|=ad-bc.
$
<font color="blue"><b>$\gamma(k)$</b></font>  : $MA(q):\ Y_t = \theta_0 Z_t + \theta_1 Z_{t-1} + \dots + \theta_q Z_{t-q}$  $\gamma(k) = \sigma^2 \sum_{i=0}^{q-k} \theta_i \theta_{i+k}, \quad k=0,1,\dots,q;
\qquad \gamma(k)=0,\ k>q.$
$Z\sim N(0,\sigma^2)$, $E(Z^2) = \sigma^2 \text{ and } E(Z^4) = 3\sigma^4$
**<font color=blue>ARMA 课程定义</font>：** $Y_t - \phi_1Y_{t-1} - \cdots - \phi_pY_{t-p} = Z_t - \theta_1Z_{t-1} - \cdots - \theta_qZ_{t-q}$ 
**<font color=blue>ARMA R 定义</font>：** $Y_t - \phi_1Y_{t-1} - \cdots - \phi_pY_{t-p} = Z_t + \theta_1Z_{t-1} + \cdots + \theta_qZ_{t-q}$
$$F(x) = \frac{1}{(x-a)(x-b)} = \frac{A}{x-a} + \frac{B}{x-b}$$
目标：求 $A$。
在等式左边，用手指盖住分母里的 $(x-a)$。 把剩下的部分中所有的 $x$ 都替换成让被盖住的那项为 0 的值。算出来的结果(不包含(x-a))就是 $A$
然后我们分别对每一个式子都进行$1/(1-cB)$的分解

![image-20251208223136588](C:\Users\31670\Desktop\Study-Material\STAT4005\image-20251208223136588.png)
<font color=blue>**Stationary vs. Integrated Processes**</font>
**1. Impact of shocks / Impulse response**
**Stationary (e.g., ARMA):** Shocks are transitory, the impulse response gradually decays to $0$, and the series "forgets" the shock.
**Integrated (e.g., Random Walk):** Shocks are permanent, the impact does not disappear, and the series continuously "accumulates" all shocks (infinite memory).
**2. Forecast & long-run behavior**
**Stationary:** The long-term expected forecast $\hat{X}_{t+h}$ converges to the mean $\mu$.
**Integrated:** The long-term expected forecast mainly "follows" the most recent observation $X_t$, rather than returning to a fixed mean.
**3. Forecast error variance**
**Stationary:** The $h$-step forecast error variance $\text{Var}(e(h)) = \sigma^2 \sum_{j=0}^{h-1}\psi_j^2$ tends towards a finite constant (bounded) as $h$ increases.
**Integrated:** $\psi_j$ does not decay to $0$ (in many cases approximately $\psi_j \approx 1$), and $\text{Var}(e(h)) \approx h\sigma^2$ grows linearly (unbounded) as $h$ increases.

---

<font color=blue>**Decomposition of time series:**</font> 
$X_t = \underbrace{T_t}_{\text{(Trend)}} + \underbrace{S_t}_{\text{(Seasonality)}} + \underbrace{N_t}_{\text{(Noise)}}$
$$T_t + S_t \Rightarrow \text{ Macroscopic Component}$$   $$N_t \Rightarrow \text{ Microscopic Component}$$

<font color=green>**Estimation of trends without seasonality:**</font> 3种方法1. Least Squares Method 2.  Filtering 3. Differencing
<font color=DarkViolet>**1.  Least Squares Method:**</font>  记矩阵$X$的转置是$X'$
由于$t = 1,\ 2,\ 3,\ ....,\ n$ 我们记$X = \begin{pmatrix} 
1 & 1 & \cdots & 1^k \\ 
1 & 2 & \cdots & 2^k \\ 
\vdots & \vdots & & \vdots \\ 
1 & n & \cdots & n^k 
\end{pmatrix}$ $Y = (X_1,X_2,...,X_n)'$ $X_t$是t时刻的观测值
Goal is to minimize $RSS =  \sum_{t=1}^{n}(X_t - T_t)^2 = (Y - X\beta)'(Y - X\beta)$ $\Rightarrow \hat \beta = (X'X)^{-1}X'Y$
<font color=DarkViolet>**2. Filtering**</font>
<font color=blue>**Filter 种类:** </font>
**1. Low-pass filter**: Filter out high-frequencies (volatile) signals Retains low-frequencies (smooth) signals 
**<font color=black>2.</font> High-pass filter**: Filter out low-frequencies (smooth) signals Retains high-frequencies (volatile) signals 
<font color=blue>**Filter Example:**</font>
<font color=black>**1. Moving Average Filter**</font>
$S_t = \frac{1}{2q+1} \sum_{r=-q}^{q} X_{t+r}$, where $S_t$ is the filtered value at time t, and $2q+1$ is the window width.
<font color=black>**2. Spencer 15-point Filter**</font>
 $S_t = \sum_{r=-7}^{7} w_r X_{t+r}$, where the weights $w_r$ are specifically defined as $w = \frac{1}{320} \times [-3, -6, -5, 3, 21, 46, 67, 74, 67, 46, 21, 3, -5, -6, -3]$. 
<font color=red>**Theorem:** </font>
k阶多项式 $T_t = c_0 + c_1t + \cdots + c_kt^k$ 可以无失真地(Passes through unchanged)通过滤波器 $\hat{T}_t = \sum_{r=-s}^{s} a_r T_{t+r}$ 的充要条件是滤波器权重 $a_r$ 满足以下两个条件：1. $\sum_{r=-s}^{s} a_r = 1$ 2. $\sum_{r=-s}^{s} r^j a_r = 0$，对所有 $j = 1,2,...,k$
<font color=DarkViolet>**3. Differencing**</font>
<font color=blue>**概念:**</font>
**一阶差分** First order: $\Delta X_t = X_t - X_{t-1}$  **二阶差分** Second Order: $\Delta^2 X_t = \Delta(\Delta X_t)$
Backshift operator $B$： $B X_t = X_{t-1}$,  $B^k X_t = X_{t-k}$
Differencing operator $\Delta$: $\Delta X_t = (1-B)X_t$    $\Delta^k X_t = (1-B)^k X_t$
<font color = blue>**用法: Differencing removes trend**</font>:
If $X_t = \alpha + \beta t$ 一阶差分后: $\Delta X_t = X_t - X_{t-1} = \alpha + \beta t - [\alpha + \beta(t-1)] = \beta$ 线性趋势被完全去除
If $X_t = \gamma t^p$ 一阶差分后：$\Delta X_t = X_t - X_{t-1} = \gamma t^p - \gamma(t-1)^p = p\gamma t^{p-1} - C_2^p \gamma t^{p-2} + ...$ 次数降低的多项式
In general $X_t = T_t + N_t$ 其中trend 部分$T_t = \sum_{j=0}^{p} a_j t^j$  p阶差分后：$\Delta^p X_t = p! a_p + \Delta^p N_t$

<font color=Green>**Estimating/Removing seasonal effect**</font> 1. Moving average method 2. Seasonal differencing
**Seasonal cycles: ** General Decomposition $\Rightarrow X_t = T_t+S_t+N_t$ Multiplicative Seasonal Component $\Rightarrow X_t = T_tS_tN_t$
Seasonal component $S_t : \text{period}=d$ 1. $S_{t+d} = S_t$ 2. $\sum_{j=1}^{d} S_j = 0$
**Difficulties when both $T_t$ and $S_t$ exist, need to separate the effect of trend $T_t$ and seasonal effect $S_t$** 
<font color=DarkViolet>**1. Moving average method**</font> 基于$X_t = T_t + S_t + N_t$ 
**Step 1:** estimate the trend 移动平均滤波器必须具有长度 $d\ \Rightarrow \sum_{j=1}^{d} S_j = 0$ 
<font color=black>1.</font> 当 $d = 2q+1$: $\hat{T}_t = \frac{1}{d}\sum_{r=-q}^{q} X_{t+r}$ 2. 当 $d = 2q$: $\hat{T}_t = \frac{1}{d}\left(\frac{1}{2}X_{t-q} + X_{t-q+1} + ... + X_{t+q-1} + \frac{1}{2}X_{t+q}\right)$
**Step 2:** estimate the seasonal components $\Rightarrow$ 给定从 $t = 1,...,nd$ 的样本
<font color=black>1. 计算去趋势序列: </font>$D_t = X_t - \hat{T}_t$  2.  计算去趋势序列的平均值: $\bar{D} = \frac{1}{nd}\sum_{t=1}^{nd} D_t$  3. 估计季节性成分$\hat{S}_j = \frac{1}{n}\sum_{k=0}^{n-1}(D_{kd+j} - \bar{D})$
**Step 3: ** Use any filter for the series $X_t − \hat S_t$ to get an improved $\tilde{T}_t$ (can set  $\tilde{T}_t$ = $T_t$ if you are satisfied with the filter in Step 1.)
$X_t = \tilde{T}_t + \hat{S}_t + \hat{N}_t$
<font color=DarkViolet>**2. Seasonal differencing**</font>
**Seasonal differencing**: $\Delta^{(d)} X_t = (1-B^d)X_t = X_t - X_{t-d}$
Noticed that we have $\Delta^{(d)} X_t = S_t - S_{t-d} + N_t - N_{t-d} = N_t - N_{t-d}$ 只是消除影响不是分离估计
<font color=green>**After decomposition or differencing:**</font>
Check the residual: 分解法得到的残差：$\widehat{N}_t = X_t - \widetilde{T}_t - \widehat{S}_t$
差分法得到的残差：$\widehat{N}_t = X_t - X_{t-d}$

---

<font color=blue>**Stochastic process**</font>
${X_t:t=1,2,...,n}$${X_1,X_2,...,X_n}$
随机性来源: $\Omega = (\omega_1,\omega_2,...)$, 每个$\omega$会产生一个特定的效果$\omega_i\rightarrow{X_t(\omega_i)}$
对于一个特定的$\omega$我们会产生一系列的$X_t(\omega)$我们称为==a sample function/ realization/ sample path== 对于某个固定的t $X_t( . )$是一个随机变量
实际上我们只能观察到一条样本路径, 即使用某一个$\omega$得到的
<font color=blue>**Finite dimensional distribution function**</font>
$F_\textbf{t}(\textbf{x}) = P(X_{t_1} ≤ x_1, ..., X_{t_n} ≤ x_n)$, $\textbf{x}=(x_1,x_2,\ ...,x_n),\ \textbf{t} = (t_1,\ ...,t_n)$
<font color=blue>**Strictly stationary**</font>: distribution of a process does not change over time
A process {$X_t$} is said to be strictly stationary if: for all $n$, $(t_1, t_2, ..., t_n)$ and $h$ we have   $(X_{t_1}, ..., X_{t_n}) \stackrel{d}{=} (X_{t_1+h}, ..., X_{t_n+h})$
"$\stackrel{d}{=}$" means "equal in distribution", i.e., $F_{\mathbf{t}}(\mathbf{x}) = P(X_{t_1} \leq x_1,..., X_{t_n} \leq x_n) = P(X_{t_1+h} \leq x_1,..., X_{t_n+h} \leq x_n) = F_{\mathbf{t}+h}(\mathbf{x})$
<font color=blue>**Weakly stationary**</font> (second order stationary/wide-sense stationary)
If $E(X_t) = \mu$ and $\text{Cov}(X_t, X_{t+h}) = \gamma(h) $仅与$h$有关$\Rightarrow$  {$X_t$} 是弱平稳的
<font color=blue>**Autocovariance function & Autocorrelation function**</font> 
==ACVF==: $\gamma(h) = \text{Cov}(X_t, X_{t+h})$, 描述了随机过程在相隔 $h$ 个时间单位的两个观测值之间的协方差
==ACF==: $\rho(h) = \frac{\text{Cov}(X_t, X_{t+h})}{\sqrt{\text{Var}(X_t)\text{Var}(X_{t+h})}} = \frac{\gamma(h)}{\gamma(0)}$ 在[-1,1], 衡量相隔 $h$ 个时间单位的观	测值之间的线性相关程度
<font color=red>Under  stationarity, we have</font>
<font color=black>1. $\gamma(0) = \text{Var}(X_t) = \text{Var}(X_{t+h})$</font>在任何时间点的方差都相同
<font color=black>2. $\gamma(-h) = \gamma(h)$ </font>向前看 $h$ 步和向后看 $h$ 步的协方差相同
<font color=black>3. $\rho(-h) = \rho(h)$</font>向前看 $h$ 步和向后看 $h$ 步的相关性相同
我们注意到他们都是population quantities, 它涉及到随机过程的具体分布, 实际中我们要使用样本估计
==Sample ACVF==：  $C_h = \frac{1}{n}\sum_{i=1}^{n-h}(X_i - \bar{X})(X_{i+h} - \bar{X})$
==Sample ACF==:  $r_h = \frac{C_h}{C_0}$ $C_0$是样本方差(是$n$不是$n-1$)
**为什么ACVF除以n？**
<font color=DarkViolet>Let $\tilde{X}_i = X_i - \bar{X}$ be the centered observations.
With $C_h = \frac{1}{n}\sum_{i=1}^{n-h}\tilde{X}_i\tilde{X}_{i+h}$, the sample covariance matrix can be expressed as:
$\widehat{\text{Var}}(\mathbf{X}) = (C_{|i-j|})_{i,j=1}^n = \frac{1}{n}\mathbf{M}\mathbf{M}'$
where $\mathbf{M}$ is a matrix constructed from the centered observations.
For any vector $\mathbf{a}$:
$\mathbf{a}'\widehat{\text{Var}}(\mathbf{X})\mathbf{a} = \frac{1}{n}(\mathbf{a}'\mathbf{M})(\mathbf{M}'\mathbf{a}) = \frac{1}{n}||\mathbf{M}'\mathbf{a}||^2 \geq 0$
proving non-negative definiteness.
Using $\frac{1}{n-h}$ would introduce different scaling factors for different lags, breaking the quadratic form structure and potentially violating non-negative definiteness.</font>
<font color=green>**Correlogram - ACF plot**</font>
只有当滞后h不超过样本量n的三分之一时($h \leq n/3$)，样本自相关$r_h$才是可靠的。
$r_0=\frac{C_0}{C_0}=1$
我们常常关心$Corr(X_t,\ X_{t+h}) = 0 \Leftrightarrow r_h \text{ significantly difference from 0}$?
If ${X_t}$ is white noise, $r_h \sim N(0,\frac 1n)$, 在ACF图上绘制水平线在$\pm \frac{2}{\sqrt{n}}$， 超出就认为显著不为0
<font color=Green>**Short memory vs long memory:**</font> Short Memory = Short term correlation  Long Memory = long term correlation
<font color=green>**Notice**</font>: 
<font color=black>1. </font>我们可以用ACF图来识别时间序列模式，但是如果数据中存在趋势那么$X_t$变为非平稳序列，直接看ACF不可靠，需要先去除趋势
<font color=black>2. </font>对于$Y_t = Y_{t-1} + Z_t$和$Y_t = at + Z_t$, ACF 衰减的很慢, 这表明他们是非平稳的, 应当对这些数据做detrending和filtering

---

==**Notations**==
<font color =red>$ARMA(p, q)$ </font>model is the most common model for **stationary** time series
$\underbrace{Y_t - \phi_1 Y_{t-1} - \cdots - \phi_p Y_{t-p}}_{\text{Autoregressive (AR)}} = \underbrace{Z_t - \theta_1 Z_{t-1} - \cdots - \theta_q Z_{t-q}}_{\text{Moving Average (MA)}}$
$Y_t$ is observation, $Z_t \sim \text{WN}(0, \sigma^2)$ is white noise.
Also it could be write as $\phi(B)Y_t = \theta(B)Z_t$
$\phi(B) = I - \phi_1 B - \phi_2 B^2 - \cdots - \phi_p B^p,$
$\theta(B) = I - \theta_1 B - \theta_2 B^2 - \cdots - \theta_q B^q,$
$\phi(B) \text { and } \theta(B)$are **characteristic polynomials** without common roots, i.e., no $x$ s.t. $\phi(x) = \theta(x) = 0$

<font color=red>$ARIMA(p, d, q)$</font> model is the most common model for **non-stationary** time series is
$\phi(B) \underbrace{(1-B)^d}_{Integrated} Y_t = \theta(B)Z_t.$
If $Y_t$ follows an $ARIMA(p, d, q)$ model, then $\triangle^d Y_t = (1-B)^d Y_t$ follows an $ARMA(p, q)$ model, where $(1-B)^d Y_t$ is the d-times differenced series from $Y_t$.
$$(1-B)^d Y_t = \sum_{k=0}^{d} \binom{d}{k}(-B)^k Y_t = \sum_{k=0}^{d} \binom{d}{k}(-1)^k Y_{t-k}.$$

==**Moving Average Model**==
A stochastic process $\{Y_t\}_{t=1,2,...}$ follows an MA($q$) model if
$Y_t = Z_t - \theta_1 Z_{t-1} - \cdots - \theta_q Z_{t-q}$  where $Z_t \sim WN(0, \sigma^2)$.
$MA(q)$ is a **stationary process**
<font color=black>**Proof:**</font>
$\mathbb{E}(Y_t) = 0$
$\text{Var}(Y_t) = \left(1 + \theta_1^2 + \cdots + \theta_q^2\right) \sigma^2$
$\gamma_k = \text{Cov}(Y_t, Y_{t+k}) = \begin{cases} 0 & , \quad |k| > q \\ \sigma^2 \sum_{i=0}^{q-|k|} \theta_i \theta_{i+|k|} & , \quad |k| \leq q, (\theta_0 = -1) \end{cases}$

<font color=red>**Invertibility**</font>
Definition: 如果白噪声 $Z_t$ 可以表示为过去观测值 $Y_t, Y_{t-1}, \ldots$ 的线性组合，则该模型是**可逆的** (invertible)。i.e. $Z_t = \sum_{k=0}^{\infty} \psi_k Y_{t-k}$ 其中 $\sum_{k=0}^{\infty} |\psi_k| < \infty$ 
<font color=darkviolet>An $MA(q)$ process ${Y_t}$ is invertible if the roots of the equation $\theta(B)=0$ all lie outside the unit circle</font> 
**Proof: **
$\begin{aligned}
Y_t &= Z_t - \theta_1 Z_{t-1} - \cdots - \theta_q Z_{t-q}\\
&= \theta(B)Z_t\\
&= (1-\bar{\theta}_1 B)(1-\bar{\theta}_2 B)\cdots(1-\bar{\theta}_q B)Z_t
\end{aligned}$
$\frac{1}{\bar{\theta}_k}$s are the roots of the equation $\theta(B) = 0$ 
$(1-\bar{\theta}_k B)$ can be "inverted" to the other side if $|\bar{\theta}_k| < 1$ 
<font color=blue>Therefore the model is **invertible** if all $|\bar{\theta}_k| < 1  \Leftrightarrow$ all $\frac{1}{|\bar{\theta}_k|} > 1 \Leftrightarrow$ all roots lie outside the unit circle</font>

==**Autoregressive Model**==
A stochastic process $\{Y_t\}$ follows an $AR(p)$ model if it satisfies
$Y_t = \phi_1 Y_{t-1} + \cdots + \phi_p Y_{t-p} + Z_t, \text{ or}$ $\phi(B)Y_t = Z_t,$ where $Z_t \sim WN(0, \sigma^2)$ and 
$\phi(B) = 1 - \phi_1 B - \phi_2 B^2 - \cdots - \phi_p B^p$ is the characteristic polynomial.

<font color=red>**Stationarity**</font>
**Lemma**: If $Y_t = \sum_{i=0}^{\infty} \psi_i Z_{t-i}$, $Z_t \sim WN(0, \sigma^2)$ and $\sum_{i=0}^{\infty} |\psi_i| < \infty$, then $\{Y_t\}$ is a stationary process.
Using the properties of white noise, i.e. $\mathrm{E}(Z_t) = 0$, $\mathrm{Cov}(Z_t, Z_k) = \sigma^2 \mathbb{1}_{\{t=k\}}$, we have
<font color=black>1. </font>$\mathrm{E}(Y_t) = 0$
<font color=black>2. </font>$\mathrm{Var}(Y_t) = \sigma^2 \sum_{i=0}^{\infty} \psi_i^2 \leq \sigma^2 \left(\sum_{i=0}^{\infty} |\psi_i|\right)^2 < \infty$
<font color=black>3. </font>$\mathrm{Cov}(Y_t, Y_{t+k}) = \sigma^2 \sum_{i=0}^{\infty} \psi_i \psi_{i+k}$ is independent of $t$
$\Rightarrow$ $\{Y_t\}$ is stationary.
**Theorem: **The process $\phi(B)Y_t = Z_t$, $\quad Z_t \sim WN(0, \sigma^2)$  is stationary iff no root of $\phi(x)$ is on the unit circle (i.e., all roots are outside the unit circle)

<font color=red>**Asymptotic stationary**</font>
考虑AR(1)的展开形式，我们有$Y_t = Z_t + \phi Z_{t-1} + \phi^2 Z_{t-2} + \cdots + \phi^{t-1} Z_1 + \phi^t Y_0$
我们观察到$Y_0$是一个固定值所以我们会发现
$\mathrm{E}(Y_t) = \phi^t \mathrm{E}(Y_0)$
$\mathrm{Var}(Y_t) = \sigma^2(1 + \phi^2 + \cdots + \phi^{2(t-1)}) + \phi^{2t}\mathrm{Var}(Y_0)$，他们是time dependent
However, as $t\rightarrow \infin$, $E(Y_t)\rightarrow 0\ \ \mathrm{Var}(Y_t) = \frac{\sigma^2}{1-\phi^2}$

<font color=red>**Causality**</font>
**Definition**: ${Y_t}$ is causal if it can be expressed as a linear combination of the past white noise $Z_t,Z_{t-1},...$ i.e.  $Y_t = \sum_{k=0}^{\infin}\psi_kZ_{t-k}$, where $\sum _{k=0}^\infin |\psi_k|<\infin$
**Theorem: **An $AR(p)$ process $\phi(B)Y_t = Z_t$, $Z_t \sim WN(0, \sigma^2)$ is causal if the roots of the characteristic polynomial $\phi(B) = 1 - \phi_1 B - \cdots - \phi_p B^p$ are outside the unit circle.
Proof:
Factorization: $\phi(B) = (1 - \xi_1 B)(1 - \xi_2 B) \cdots (1 - \xi_p B)$
The roots of $\phi(x)$ are $x = \frac{1}{\xi_1}, \ldots, \frac{1}{\xi_p}$.
<font color=blue>The roots are outside unit circle $\Leftrightarrow$ $\left|\frac{1}{\xi_k}\right| > 1$, for all $k = 1, \ldots, p$ $\Leftrightarrow$ $|\xi_k| < 1$, for all $k = 1, \ldots, p$ $\Leftrightarrow$ $(1 - \xi_k B)$, for all $k = 1, \ldots, p$, can be "inverted" to another side and represented by past noises. $\Leftrightarrow$ $\{Y_t\}$ is causal.</font>

**Yule-Walker:** 对于一个stationary的Timeseries, 我们有$\gamma_k = E[Y_tY_{t-k}]$

==**ARMA**==
**Definition:** $\{Y_t\}$ is said to be an ARMA$(p, q)$ process if
$$\phi(B)Y_t = \theta(B)Z_t, \quad Z_t \sim WN(0, \sigma^2),$$
where $$\phi(B) = 1 - \phi_1B - \cdots - \phi_pB^p$$     $$\theta(B) = 1 - \theta_1B - \cdots - \theta_qB^q$$ are the characteristic polynomials with NO common roots.
**Property:**
**Stationary solution** exists if $\Rightarrow$ All roots of $\phi(B)$ are **not on** the unit circle 
**Causal** if $\Rightarrow$  All roots of $\phi(B)$ are **outside** the unit circle ⇒ $Y_t = \phi^{-1}(B)\theta(B)Z_t = \sum_{k\geq 0} \psi_k Z_{t-k}$, with $\sum_{k\geq 0}|\psi_k| < \infty$. **Invertible** if $\Rightarrow$ All roots of $\theta(B)$ are **outside** the unit circle ⇒ $Z_t = \theta^{-1}(B)\phi(B)Y_t = \sum_{k\geq 0} \pi_k Y_{t-k}$, with $\sum_{k\geq 0}|\pi_k| < \infty$.

**==ARIMA==**
Noticed that for $ARIMA(p,d,q)$ model, if $d\geq1$, the root of $(1-B)^d$ is 1, therefore it is **non-stationary and non-causal**
But it is **invertible** if the roots of θ(B) are outside the unit circle.

==**Seasonal ARIMA**==
$\{Y_t\}$ follows an $SARIMA(p, d, q) \times (P, D, Q)_s$ model if
$$\phi(B)\Phi_P(B^s)(1-B)^d(1-B^s)^D Y_t = \theta(B)\Theta_Q(B^s)Z_t$$
where
$$\phi(B) = 1-\phi_1 B - \cdots - \phi_p B^p$$
$$\theta(B) = 1-\theta_1 B - \cdots - \theta_q B^q$$
$$\Phi_P(B^s) = 1-\Phi_1 B^s - \cdots - \Phi_P B^{sP}$$
$$\Theta_Q(B^s) = 1-\Theta_1 B^s - \cdots - \Theta_Q B^{sQ}$$

---

#### ==**Estimation**==

<font color="navy">**1. Model Notations & Basics**</font>

  * **ARMA(p, q):** $\phi(B)(Y_{t}-\mu)=\theta(B)Z_{t}$ where $Z_{t}\sim WN(0,\sigma^{2})$.
  * **Sample Moments:**
    * Mean: $\overline{Y}=\frac{1}{n}\sum_{t=1}^{n}Y_{t}$.
    * Variance: $C_{0}=\frac{1}{n}\sum_{t=1}^{n}(Y_{t}-\overline{Y})^{2}$.
    * ACVF: $C_{k}=\frac{1}{n}\sum_{t=1}^{n-k}(Y_{t}-\overline{Y})(Y_{t+k}-\overline{Y})$.
    * ACF: $r_{k}=C_{k}/C_{0}$.

-----

<font color="navy">**2. Method of Moment Estimators (MM)**</font>

Assume $\{Y_t\} \sim \text{ARMA}(p,q)$ is stationary with ACVF $\gamma(\cdot)$ and ACF $\rho(\cdot)$.  $\gamma_0 = \sigma^2$

| Population Quantity | Estimator                                                    |
| ------------------- | ------------------------------------------------------------ |
| $\mu$               | $\displaystyle \bar Y_n = \frac{1}{n}\sum_{t=1}^n Y_t$       |
| $\gamma(k)$         | $\displaystyle C_k = \frac{1}{n}\sum_{t=1}^{n-k} (Y_t - \bar Y)(Y_{t+k} - \bar Y)$ |
| $\rho(k)$           | $\displaystyle r_k = \frac{C_k}{C_0}$                        |

-----

<font color="navy">**3. Yule-Walker Estimators (YW) - AR Models Only**</font>
**<font color="darkred">Matrix Form (The YW Equation):</font>**
$$\hat{\boldsymbol{\phi}} =\begin{pmatrix}\hat{\phi}_{1}\\ \vdots\\ \hat{\phi}_{p}\end{pmatrix} = \begin{pmatrix}1&r_{1}&...&r_{p-1}\\ r_{1}&1&...&r_{p-2}\\ \vdots&\vdots&\ddots&\vdots\\ r_{p-1}&r_{p-2}&\cdot\cdot\cdot&1\end{pmatrix}^{-1}\begin{pmatrix}r_{1}\\ \vdots\\ r_{p}\end{pmatrix}$$
然后把里面的对应的r替换成C
**<font color="darkred">Variance Estimation:</font>**$$\hat{\sigma}^{2}=C_{0}-\sum_{k=1}^{p}\hat{\phi}_{k}C_{k}$$

-----

<font color="navy">**4. Least Squares Estimators (LSE)**</font>

<font color="green">**A. Unconditional Least Squares (ULS) - For AR(p)**</font>
对于 ${Y_t}\sim AR(p), Y_t = \phi_1Y_{t-1}+...+\phi_pY_{t-p}+Z_t$ $\Rightarrow Y=Xϕ+Z$
$$
\mathbf{X} =
\begin{pmatrix}
Y_p     & Y_{p-1} & \cdots & Y_1 \\
Y_{p+1} & Y_p     & \cdots & Y_2 \\
\vdots  & \vdots  & \ddots & \vdots \\
Y_{n-1} & Y_{n-2} & \cdots & Y_{n-p}
\end{pmatrix}
\quad \text{and} \quad
\mathbf{Y} =
\begin{pmatrix}
Y_{p+1} \\
Y_{p+2} \\
\vdots  \\
Y_n
\end{pmatrix},
\quad
\Gamma_p =
\begin{pmatrix}
\gamma(0)     & \gamma(1)     & \cdots & \gamma(p-1) \\
\gamma(1)     & \gamma(0)     & \cdots & \gamma(p-2) \\
\vdots        & \vdots        & \ddots & \vdots      \\
\gamma(p-1)   & \gamma(p-2)   & \cdots & \gamma(0)
\end{pmatrix}
$$
**Estimators:** $\hat{\phi}=(X^{T}X)^{-1}X^{T}Y$. $\hat{\sigma}^{2} = {(Y-X\hat{\phi})^{T}(Y-X\hat{\phi})}/{(n-2p)}$

**Alternative Calculation:** Minimize $S(\phi) = \sum_{t=p+1}^{n} (Y_t - \sum \phi_k Y_{t-k})^2$

**<font color="darkred">Inference (Asymptotic Normality):</font>**
when $n\rightarrow +∞$  $\sqrt{n}(\hat{\phi}-\phi)\rightarrow N_{p}(0,\sigma^{2}\Gamma_{p}^{-1})$ where $\Gamma_p$ is the covariance matrix of the process.
**General C.I.:** $\hat{\phi}_{k}\pm2\sqrt{\hat{Var}(\hat{\phi}_{k})}$ where $\hat{Var}$ comes from diagonal of $\hat{\sigma}^2\hat{\Gamma}_p^{-1}/n$.
Also we have, for $\boldsymbol{w} = (w_{1}, \ldots, w_{p})^{T} \in \mathbb{R}^{p}$, as $n \to \infty$,$$  \sqrt{n}\left(\boldsymbol{w}^{T}\boldsymbol{\phi} - \boldsymbol{w}^{T}\hat{\boldsymbol{\phi}}\right) \xrightarrow{d} \text{N}\left(0, \sigma^{2}\boldsymbol{w}^{T}\boldsymbol{\Gamma}_{p}^{-1}\boldsymbol{w}\right).$$It could be useful in testing a composite hypothesis, for example, $H_{0} : \phi_{1} = \phi_{2}$.
We can estimate $\Gamma_{p}$ by $\hat{\Gamma}_{p}$ by replacing all $\gamma(k)$ by $C_{k}$.

<font color="green">**B. Conditional Least Squares (CLS) - For MA(q) / ARMA(p,q)**</font>

Let $\{Y_{t}\} \sim \text{ARMA}(p,q)$ be **invertible**. Then

1. (**Initialization**) Assume $\tilde{Z}_{s} = Y_{s} = 0$ for all $s \le 0$.
2. (**Sequential Estimation of Noise**) Let $\tilde{Z}_{t} = Y_{t} - \phi_{1}Y_{t-1} - \cdots - \phi_{p}Y_{t-p} + \theta_{1}\tilde{Z}_{t-1} + \cdots + \theta_{p}\tilde{Z}_{t-p}$.
3. (**Quantification of Error**) Define the sum of squared error as $S_{*}(\boldsymbol{\phi}, \boldsymbol{\theta}) = \sum_{t=1}^{n} \tilde{Z}_{t}^{2}$.

Then the **Conditional-Least Squares Estimators** are given by the minimizer of $S_{*}(\boldsymbol{\phi}, \boldsymbol{\theta})$, i.e. $$(\hat{\boldsymbol{\phi}}, \hat{\boldsymbol{\theta}}) = \arg \min_{\boldsymbol{\phi}, \boldsymbol{\theta}} S_{*}(\boldsymbol{\phi}, \boldsymbol{\theta})$$

-----

<font color="navy">**5. Maximum Likelihood Estimators (MLE)**</font>

<font color="navy">**1. 构建 Joint PDF**</font>

MLE 的核心是写出观测数据 $Y_1, Y_2, ..., Y_n$ 的 **Joint PDF** $f(y_1, ..., y_n; \theta)$，这在统计学中被称为 **似然函数** $L(\theta)$。

由于时间序列数据不是独立的（$Y_t$ 依赖于过去的 $Y_{t-1}$），我们不能简单地将概率相乘。我们主要通过两种方法来构建这个联合密度函数：

<font color="green">**方法一：Iterative Conditioning**</font>
**公式分解：**$f(Y_1, ..., Y_n) = f(Y_1)\, f(Y_2|Y_1)\, f(Y_3|Y_2, Y_1)\, \dots\, f(Y_n|Y_{n-1}, \dots, Y_1)$
以 AR(1) 为例 $(Y_t = \phi Y_{t-1} + Z_t)$：

1. **条件部分 ($t \ge 2$)**：给定 $Y_{t-1}$，当前的 $Y_t$ 服从正态分布，均值为 $\phi Y_{t-1}$，方差为 $\sigma^2$，即  
   $Y_t \mid Y_{t-1} \sim N(\phi Y_{t-1}, \sigma^2)$。
2. **初始部分 ($t=1$)**：为了保证精确性，需要 $Y_1$ 的边缘分布。对于平稳 AR(1)，  
   $Y_1 \sim N\big(0, \frac{\sigma^2}{1-\phi^2}\big)$。
3. **最终似然函数**：将上述两部分相乘得到 $L(\phi, \sigma^2)$。

<font color="green">**方法二：Multivariate Normal / Matrix Approach**</font>
这种方法不进行拆解，而是将整个时间序列向量 $\mathbf{Y} = (Y_1, \dots, Y_n)^T$ 视为一个整体，服从 **多元正态分布**。

* **公式：**$L(\theta, \sigma^2) = (2\pi)^{-n/2} |\Sigma|^{-1/2}
  \exp\left\{-\frac{1}{2} \mathbf{y}^{T}\Sigma^{-1}\mathbf{y}\right\}$

* **关键点**：这里的 $\Sigma$ 是协方差矩阵，其中元素 $\Sigma_{ij} = \gamma(|i-j|)$（$n\times n$ 矩阵），是参数 $\phi, \theta, \sigma^2$ 的函数。MLE 就是要调整这些参数，使得这个矩阵最能描述数据的相关结构。

<font color=navy>**2. 最大化似然函数**</font>
有了似然函数 $L(\theta)$ 后，我们的任务是找到 $\hat{\theta}$ 让 $L$ 最大。
1.**对数化 (Log-Likelihood)**：$l(\theta) = \ln L(\theta)$。 AR(1)：$l(\phi, \sigma^2) = \frac{1}{2}\ln(1-\phi^2) - \frac{n}{2}\ln(\sigma^2) - \frac{S(\phi)}{2\sigma^2}$, 其中$S(\phi)= \sum_{t=2}^n (Y_t - \phi Y_{t-1})^2 + (1-\phi^2)Y_1^2.$
2.**数值优化 (Numerical Optimization)**：对于 **MA(q)** 或 **ARMA** 模型，通常 **没有闭式解**，需要用 Newton–Raphson、Scoring Method 等数值方法来最大化对数似然。

<font color="red"><b>Comparison</b></font>
**Category 1: AR Models**
**1. ULS** 
**Pros:** **Fast & Simple:** It transforms into a standard linear regression problem. **Closed-Form Solution:** Has an exact analytical formula; no iteration required.
**Cons:** **Information Loss:** Treats the first $p$ observations as fixed constants, ignoring their probability distribution. **Small Sample Bias:** Less accurate than MLE when sample size $n$ is small.
**2. MLE**
**Pros:** **Precision:** Uses full information, including the distribution of initial values $Y_1$. **Stationarity:** Naturally imposes stationarity constraints on parameters.
**Cons:** **Computation:** No closed-form solution; requires numerical optimization.
**Category 2: MA & ARMA Models**
**1. CLS**
**Pros: ** **Feasibility:** Makes calculation possible by recursively estimating unobservable noise $Z_t$. **Efficiency:** Computationally faster than exact MLE; estimates are very close to MLE for large $n$.
**Cons:** **Initialization Bias:** Relies on the arbitrary assumption that initial errors $Z_0=0$, which causes bias in small samples. **Constraint:** Requires the model to be invertible.
**2. MLE**
**Pros:** **Optimal:** The most theoretically efficient estimator; utilizes the full covariance matrix $\Sigma$. **No Approximation:** Does not need to assume $Z_0=0$.
**Cons:** **Computationally Expensive:** Calculation of the inverse covariance matrix $\Sigma^{-1}$ or iterative conditioning is complex and slow.

**MM Estimation in Time Series**
**Advantages:**1. Simple and intuitive; based on matching sample and theoretical moments. 2. Computationally easy—no need for complex optimization like MLE. 3. Can give consistent estimates under mild assumptions.
**Disadvantages:** 1. Less efficient than MLE (larger variance). 2. Sensitive to choice of moments or lag order. 3. Not optimal for small samples or non-Gaussian data.

==**Model Selection** and **Diagnostics**==
<font color="navy">**1. ACF & PACF**</font>
![image-20251208230604776](C:\Users\31670\AppData\Roaming\Typora\typora-user-images\image-20251208230604776.png)

<font color="navy">**2. Order Selection**</font>
$\hat{\beta} = (\hat{\phi}_1, \dots, \hat{\phi}_p, \hat{\theta}_1, \dots, \hat{\theta}_q)$ and $\hat{\sigma}^2$ as the MLE of the model given $Y_1, \dots, Y_n$.
$S_Y(\hat{\beta}) = \sum_{t=1}^n \hat{Z}_t^2$, where $\hat{Z}_t = Y_t - \hat{\phi}_1 Y_{t-1} - \dots - \hat{\phi}_p Y_{t-p} - \hat{\theta}_1 Z_{t-1} - \dots - \hat{\theta}_q Z_{t-q}$. 
$L(\hat{\beta}, \hat{\sigma}^2) = (2\pi\hat{\sigma}^2)^{-n/2} \exp\{-S_Y(\hat{\beta})/(2\hat{\sigma}^2)\}$, as the likelihood function of ARMA($p, q$) model.
$\frac{S_Y(\hat{\beta})}{n} = \hat \sigma^2$.

<font color="red">**A. AIC (Akaike Information Criterion)**</font>  $\mathrm{AIC}
= -2\log L(\hat\beta,\hat\sigma^2)+2(p+q+1)$ 
**Principle:** AIC aims to estimate the **Expected Predictive Log-likelihood**. It strikes a balance between **model goodness-of-fit** (the likelihood function) and **model complexity** (the number of parameters $p+q+1$).
**Applicable Scenarios:** Use when your primary goal is to achieve **accurate prediction**.
**Drawback:** AIC is **Not Consistent**; even with a large sample size $n$, it may select a model more complex than the true model. It tends to **overfit** with small sample sizes.

<font color="red">**B. AICC (Corrected AIC)**</font>   $\mathrm{AICC}= -2\log L(\hat\beta,\hat\sigma^2)+ \frac{2(p+q+1)n}{\,n-p-q-2\,}$
**Principle:** AICC is a **small-sample correction** of AIC. When the sample size $n$ is small, AIC tends to select models with too many parameters (overfitting). AICC introduces the correction factor $\frac{n}{n-p-q-2}$, which imposes a harsher penalty on the number of parameters when $n$ is small.
**Applicable Scenarios:** You **must use AICC** to prevent overfitting when the sample size $n$ is small. Since AICC converges to AIC when $n$ is large, it is a generally more robust choice.

<font color="red">**C. BIC (Bayesian Information Criterion)**</font>   $BIC= (n-p-q)\log\left[\frac{n\hat{\sigma}^2}{\,n-p-1\,}\right] - n\bigl(1 + \log\sqrt{2\pi}\bigr)-(p+q)\log\left[\frac{\sum_{i=1}^n X_i^2 - n\hat{\sigma}^2}{p+q}\right].$
**Principle:** Based on **Bayesian inference**, BIC aims to estimate the **Marginal Log-likelihood**. BIC assumes the existence of a "true model" and penalizes model complexity **more heavily** than AIC (the penalty term involves $\log n$).
**Applicable Scenarios:** BIC is a **Consistent** estimator. Use BIC when your goal is not purely prediction, but to find the **"true" underlying model structure** of the data (i.e., identifying the correct $p$ and $q$) and the sample size $n$ is sufficiently large.

<font color="red">**D. FPE (Final Prediction Error, AR Model Only)**</font>  $\mathrm{FPE}=\left(\frac{n+p}{n-p}\right)\hat{\sigma}^2$
**Principle:** FPE is designed to estimate the **Mean Squared Error (MSE)** of the parameter estimators, specifically $E[(\hat{\phi}-\phi)'(\hat{\phi}-\phi)]$. It reflects the average predictive error variance when performing a one-step-ahead forecast using this model.
**Applicable Scenarios:** **Only applicable to AR models**. If you are fitting a pure AR model and wish to minimize the prediction error, you can use FPE. For large samples, the results selected by FPE are generally very similar to those selected by AIC (both lack consistency).

<font color="navy">**3. Model Diagnostics**</font> 检测Residuals，看是否足够小，并且可以看是否是WN
**Step 1: **Residual $\hat{Z}_t = Y_t - \hat{Y}_t$,  计算$\hat{r}_Z(j) = \frac{\sum_{t=1}^{n-j} (\hat{Z}_t - \bar{Z})(\hat{Z}_{t+j} - \bar{Z})}{\sum_{t=1}^{n} (\hat{Z}_t - \bar{Z})^2}$ 
**Step 2: **Plot $\hat{r}_Z(j)$ 的图看是不是在$(-2/\sqrt n, +2/\sqrt n)$
**Step 3: **Apply the Ljung-Box test.

<font color=red>**Ljung-Box: **</font>
Let $r_Z(j)$ be the sample ACF of $\{\hat Z_t\}$ and $\rho_Z$ be the ACF of the true noise sequence.
$H_0 : \rho_Z(k) = 0 \text{ whenever } |k| \leq h \quad \text{against} \quad H_1 : \rho_Z(k) \neq 0 \text{ for some } |k| \leq h$
The Ljung-Box Test is defined by $Q(h) = n(n+2)\sum_{j=1}^h \frac{r_{\hat Z}^2(j)}{n-j}$ and $Q(h) \xrightarrow{d} \chi^2(h-p-q) \text{ under } H_0 \text{ as } n \to \infty.$
**Remark: ** 1. A common choice of $h$ lies between **10 and 30**. 2. If $Q(h) \geq \chi^2_{h-p-q, 0.95}$, $H_0$ is **rejected** $\Rightarrow$ the **model is not a bad fit to the data**.

<font color=navy>**4. Four Stages of Model Building:**</font>
<font color=black>1. Pre-processing:</font> (1) Remove trend and seasonal effect. (2)Check ACF of the residual to see if it is stationary. Otherwise, take differences to make it stationary
<font color=black>2. Model Estimation:</font> (1) Draw ACF/PACF of the filtered data and get an initial ARMA model (2) Do estimation 
<font color=black>3. Model Identification:</font> Repeat step 2 for various ARMA models, choose an ARMA model by FPE/AIC/BIC
<font color=black>4. Model Checking: (1) Residual analysis (ts.plot/acf of $\hat Z_t $) (2) Ljung-Box test</font>

<font size="4" color="black">**==Forecasting==**</font>

<font color="brown">**1. Model Setup & Assumptions**</font>

* **ARIMA → ARMA（差分）**  
  若 $\{Y_t\}\sim ARIMA(p,d,q)$，令 $X_t=\Delta^d Y_t$，则 $\{X_t\}\sim ARMA(p,q)$。

* **${X_t}$ Assumption**  
  **Causal**：$X_t=\sum_{i=0}^\infty \psi_i Z_{t-i}$ 且 $\sum|\psi_i|<\infty$。  
  **Invertible**：$Z_t=\sum_{i=0}^\infty \pi_i X_{t-i}$ 且 $\sum|\pi_i|<\infty$。  
  设 $Z_t=0$（$t\le p$），对 $t=p+1,\dots,n$ 用 $Z_t=\sum_{k=1}^q\theta_k Z_{t-k}+ \big(X_t-\sum_{k=1}^p\phi_k X_{t-k}\big)$ 递推。

<font color="brown">**2. ARMA(p,q) 的 Box–Jenkins 预测**</font>

* **因果表示**：$Y_t=\sum_{i=0}^\infty \psi_i Z_{t-i}$，$Z_t\sim WN(0,\sigma^2)$。  

* **h 步预测**：$\hat Y_{n+h}=E(Y_{n+h}\mid Y_1,...,Y_n)=\sum_{i=h}^\infty \psi_i Z_{n+h-i}$（仅用已知 $Z$）。  

* **预测误差与方差**：  
  $e_n(h)=Y_{n+h}-\hat Y_{n+h}=\sum_{i=0}^{h-1}\psi_i Z_{n+h-i}$，  
  $P_{n+h}^n=\operatorname{Var}(e_n(h)\mid Y_1,...,Y_n)=\sigma^2\sum_{i=0}^{h-1}\psi_i^2$。

* **95% 区间**：$\hat Y_{n+h}\pm1.96\sqrt{P_{n+h}^n}$。

<font color="brown">**3. ARIMA(p,d,q) 的预测（反差分）**</font>

* **先预测差分序列**：对 $X_t=\Delta^d Y_t$ 用 ARMA 方法得 $\hat X_{n+1:n+h}$。  

* **回到原序列（以 d=1 为例）**：$Y_{n+h}=Y_n+\sum_{j=1}^h X_{n+j}$，因而 $\hat Y_{n+h}=Y_n+\sum_{j=1}^h \hat X_{n+j}$，  误差 $e_{n,Y}(h)=\sum_{j=1}^h e_{n,X}(j)$。  

* 95%区间为 $\hat Y_{n+h}\pm1.96\sqrt{P_{n+h,Y}^n}$

<font size="4" color="black">==**Non-Stationary**==</font>

<font size="4" color="darkblue">**1. Nonstationarity in Mean: TS vs. DS**</font>

- **Trend Stationary (TS):** $Y_t = \beta_0 + \beta_1 t + \nu_t$. Has deterministic trend. **Fix:** Detrending (Regression).
- **Difference Stationary (DS):** $Y_t = \beta_1 + Y_{t-1} + \nu_t$ (Random Walk with drift). Has stochastic trend. **Fix:** Differencing ($\Delta Y_t = Y_t - Y_{t-1}$).
- **Encompassing Model:** $Y_t = \beta_0+\beta_1t+v_t;\ v_t = \alpha v_{t-1}+Z_t$ 1代入2花间可得  $Y_t = \gamma_0 + \gamma_1 t + \alpha Y_{t-1} + Z_t$.
- If <font color="red">**$\alpha = 1$**</font> $\rightarrow$ **DS** (Unit Root, Non-stationary). If <font color="red">**$|\alpha| < 1$**</font> $\rightarrow$ **TS** (Mean Reverting, Stationary).

<font color="brown">**Unit Root Test (Dickey-Fuller Test)**</font> 查是不是trend  stationary (但是只考$Y_t=\alpha Y_{t-1}+Z_t$, 所以直接是Stationary)

- **Hypothesis:** <font color="red">**$H_0: \alpha = 1 \Leftrightarrow \rho = 0$**</font>  vs. $H_1: \alpha < 1$ (trend  stationary).
- **Test Statistic:** AR coefficient $\hat{\alpha} = \frac{\sum Y_t Y_{t-1}}{\sum Y_{t-1}^2}$. Statistic $T = n(\hat{\alpha} - 1)$.
- **Distribution:** Follows Dickey-Fuller Distribution (FCLT):
  $$n(\hat{\alpha}-1) \xrightarrow{d} \frac{\int_0^1 W(t) dW(t)}{\int_0^1 W^2(t) dt}$$ $W(t)$是Brownian motion
- **Decision:** Reject $H_0$ if statistic < Critical Value or $\text{p-value}<=0.05 \Rightarrow \text{Stationary}$  

FCLT: $Y_k = \sum_{i=1}^k Z_i,\quad \dfrac{Y_{\lfloor nt \rfloor}}{\sqrt{n}} \xrightarrow{d} W(t).$
Unit root statistic: $\hat{\alpha} = \dfrac{\sum_{t=2}^n Y_t Y_{t-1}}{\sum_{t=2}^n Y_{t-1}^2}$
Denominator:$\sum_{t=2}^n Y_{t-1}^2= n^2 \sum_{t=2}^n \left(\frac{Y_{t-1}}{\sqrt{n}}\right)^2 \frac{1}{n}\approx n^2 \int_0^1 W^2(t)\,dt$
Numerator:$\sum_{t=2}^n Y_t Y_{t-1}= \sum_{t=2}^n Y_{t-1}^2+ n \sum_{t=2}^n \frac{Y_{t-1}}{\sqrt{n}} \frac{Y_t - Y_{t-1}}{\sqrt{n}}\approx n^2 \int_0^1 W^2(t)\,dt + n \int_0^1 W(t)\,dW(t)$

------

<font size="4" color="darkblue">**2. Nonstationarity in Variance**</font>

<font color="brown">**Case A: Deterministic Change (Variance Stabilization)**</font>$Y_t=\mu_t+Z_t$

- **Situation:** Variance depends on mean, $Var(Y_t) =\sigma^2 h^2(\mu_t)$.

- **Goal:** Find transformation $g(Y_t)$ such that $Var(g(Y_t)) \approx \text{Constant}$.

- **Formula: **
  $g(Y) \approx g(\mu) + g'(\mu)(Y-\mu)
  \Rightarrow Var(g(Y)) \approx [g'(\mu)]^2 h^2(\mu)\sigma^2$.

  To make variance constant, set $g'(\mu) = \frac{k}{h(\mu)}$ and  $$g(x) = k \int \frac{1}{h(\mu)} d\mu$$

- **Box-Cox Transformation Family ($g_\lambda(y)$):**
  $$g_\lambda(y) = \begin{cases} \frac{y^\lambda - 1}{\lambda} & \lambda \neq 0 \\ \ln(y) & \lambda = 0 \end{cases}$$

<font color="brown">**Case B: Stochastic Change (Heteroskedasticity)**</font>

- **Stylized Facts of Financial Returns ($X_t = \Delta \ln P_t$):**
  1. **Heavy-tailed:** Kurtosis > 3 (Not Normal).
  2. **Uncorrelated $X_t$:** ACF of returns $\approx 0$ (White Noise).
  3. **Correlated $X_t^2$:** ACF of squared returns $\neq 0$ (**Volatility Clustering**).

------

<font size="4" color="darkblue">**3. ARCH(q) Model**</font>

- Definition: $X_t = \sigma_t \epsilon_t$, where $\epsilon_t \sim i.i.d N(0,1)$.
  $$\sigma_t^2 = \alpha_0 + \alpha_1 X_{t-1}^2 + \dots + \alpha_q X_{t-q}^2 = var(X_t|\mathcal{F}_{t-1})$$
- **Constraints:** $\alpha_i \ge 0$ (Positivity), <font color="red">**$\sum_{i=1}^q \alpha_i < 1$**</font> (Stationarity).

<font color="purple">**ARCH(q) $\Leftrightarrow$ AR(q) for $X_t^2$**</font>
The white-noise sequence is given by $v_t = X_t^2 - \sigma_t^2 = \sigma_t^2 (\epsilon_t^2 - 1)$. Then $\{X_t^2\} \sim \text{ARMA}(q, 0)$ which is an $\text{AR}(q)$ process, as
$$X_t^2 = \sigma_t^2 + (X_t^2 - \sigma_t^2)$$ Noticed that $\sigma_t^2 = \alpha_0 + \sum_{i=1}^{q} \alpha_i X_{t-i}^2$.
$$X_t^2 = \alpha_0 + \sum_{i=1}^{q} \alpha_i X_{t-i}^2 + v_t$$ where $\text{E}(v_t) = 0$ and $\text{Cov}(v_t, v_{t-h}) = 0$ for $h \ne 0$.

**Properties (ARCH(1)):**
<font color=black>1. Unconditional Mean: $E[X_t] = 0$.</font>
<font color=black>2. Unconditional Variance: $\text{Var}(X_t) = E[X_t^2] = \frac{\alpha_0}{1 - \alpha_1}$ (Condition: $\alpha_1 < 1$).</font>
<font color=black>3. Kurtosis (4th Moment): $E(X_t^4) = \frac{3\alpha_0^2(1+\alpha_1)}{(1-\alpha_1)(1-3\alpha_1^2)}$. Exists only if $3\alpha_1^2 < 1$.</font>
<font color=black>4. ACF of $X_t^2$: $\text{Corr}(X_t^2, X_{t+h}^2) = \alpha_1^{|h|}$ (Decays like AR process).</font>

------

<font size="4" color="darkblue">**4. GARCH(p, q) Model**</font>

- Definition: Adds lagged variance terms.
  $$\sigma_t^2 = \alpha_0 + \sum_{i=1}^q \alpha_i X_{t-i}^2 + \sum_{j=1}^p \beta_j \sigma_{t-j}^2$$
- **Stationarity 成立条件:** <font color="red">**$\sum \alpha_i + \sum \beta_j < 1$**</font>.

<font color="purple">**Comparison: Unconditional vs. Conditional Moments (Stationary GARCH)**</font>

| Quantity       | **Unconditional (Long-run)**                                 | **Conditional on $\mathcal{F}_{t-1}$ (Short-run)** |
| -------------- | ------------------------------------------------------------ | -------------------------------------------------- |
| **Mean**       | $E(X_t)=0$                                                   | $E(X_t|\mathcal{F}_{t-1})=0$                       |
| **Variance**   | $Var(X_t)$ $\frac{\alpha_0}{1-(\sum_q\alpha_i+\sum_p\beta_j)}$ | $Var(X_t|\mathcal{F}_{t-1}) =\sigma_t^2$           |
| **Covariance** | $Cov(X_t,X_{t+h})=0$                                         | $Cov(X_t,X_{t+h}|\mathcal{F}_{t-1})=0$             |

**I-GARCH (Integrated Non-Stationary):** 
If $\alpha_1 + \beta_1 = 1$. Non-stationary.
Forecasting variance: $E[\sigma_{t+j}^2|\mathcal{F}_{t-1}] = j\alpha_0 + \sigma_t^2$ (Linear growth).

<font color="purple">**KEY DERIVATION: GARCH(p,q) $\Leftrightarrow$ ARMA(m, p) for $X_t^2$**</font>
Conditions: 1. 是Stationary的 2. $E(\sigma_t^4)$ exists and is constant over-time
The white-noise sequence is given by $v_t = X_t^2 - \sigma_t^2 = \sigma_t^2 (\epsilon_t^2 - 1)$. Then $\{X_t^2\} \sim \text{ARMA}(m, p)$ as
$X_t^2 = \sigma_t^2 + (X_t^2 - \sigma_t^2) = \alpha_0 + \sum_{j=1}^{q} \alpha_j X_{t-j}^2 + \sum_{i=1}^{p} \beta_i \sigma_{t-i}^2 + (X_t^2 - \sigma_t^2)$$= \alpha_0 + \sum_{j=1}^{m} (\alpha_j + \beta_j) X_{t-j}^2 - \sum_{i=1}^{p} \beta_i (X_{t-i}^2 - \sigma_{t-i}^2) + v_t$$$= \alpha_0 + \sum_{j=1}^{m} (\alpha_j + \beta_j) X_{t-j}^2 + v_t - \sum_{i=1}^{p} \beta_i v_{t-i}$$
where $\alpha_i := 0$ and $\beta_j := 0$ for $i \ge q, j \ge p$.

<font color=red>**Compare: **</font>In an ARCH(q) model the conditional variance $\sigma_t^2$ depends **only** on past shocks $X_{t-i}^2$, so to capture long‐lasting volatility clustering we often need a **large q**.
 GARCH adds lagged variances $\sigma_{t-j}^2$ on top of past shocks, so the variance “remembers” the distant past through its own lags.

------

<font size="4" color="darkblue">**5. Estimation & Testing Flow**</font>
**异方差 (Heteroscedasticity)** **同方差 (Homoscedasticity)**

**<font color="brown">A. Detecting Heteroskedasticity (LM Test)</font>**
$H_ 0$: No ARCH effect $\alpha_1 = ...= \alpha_p = 0$  $H_1$: ARCH effect exists
Run auxiliary regression of squared residuals: $X_t^2 = \alpha_0 + \alpha_1 X_{t-1}^2 + \dots + \alpha_q X_{t-q}^2$
**Statistic:** $T = n \times R^2 \rightarrow \chi^2(q)$.
**Rule:** If $T> \chi^2_{0.95, p}$ (or p-value < 0.05), **Reject $H_0$**

**<font color="brown">B. Estimation (MLE)</font>**
$
f(x_t \mid \mathcal{F}_{t-1})
= \frac{1}{\sqrt{2\pi\sigma_t^{2}}}
  \exp\left(-\frac{1}{2\sigma_t^{2}}x_t^{2}\right)
$
**Method:** Use Maximum Likelihood (MLE), **NOT OLS** (because variance changes).
Log-Likelihood Function (to maximize):
$l(\theta) = -\frac{n}{2}\ln(2\pi) - \frac{1}{2}\sum_{t=1}^n \left( \ln(\sigma_t^2) + \frac{X_t^2}{\sigma_t^2} \right)$
(Must compute $\sigma_t^2$ recursively from $t=1$ to $n$).

<font color="brown">**C. Model Selection**</font>: 
Use **AIC / BIC**.
$AIC = -2logL+2(p+q+1)$  $BIC=-2logL+(p+q+1)logn$
Note: PACF of $X_t^2$ works for ARCH order identification, but fails for GARCH.

**<font color="brown">D. Diagnostics (Goodness of Fit)</font>** 
**Object:** Standardized Squared Residuals: $\hat{\epsilon}_t^2 = \frac{X_t^2}{\hat{\sigma}_t^2}$.
**Test:** **Ljung-Box Test** on $\hat{\epsilon}_t^2$. $H_0$: no autocorrelation in $ϵ_t^2$ up to lag h.
**Statistic:** $Q(h) = n(n+2) \sum_{j=1}^{h} \frac{r^2(j)}{n-j}\rightarrow\chi^2(h - p - q - 1)$.
**Goal:** Fail to reject $H_0$ (High p-value > 0.05) $\rightarrow$ No correlation left $\rightarrow$ Good Model.
