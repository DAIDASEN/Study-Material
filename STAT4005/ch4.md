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