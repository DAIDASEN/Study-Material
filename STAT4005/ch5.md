==**Estimation**==

-----

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

  * **Definition:** $\hat{\theta}_{MLE}=arg~max_{\theta}L(\theta|Y_{1},...,Y_{n})$. Assumes $Z_t \sim N(0, \sigma^2)$.
  * **Method I: Iterative Conditioning (General)**
      * $f(Y_{1},...,Y_{n})=\{\prod_{t=2}^{n}f(Y_{t}|Y_{t-1},...,Y_{1})\}f(Y_{1})$.
      * **Exact AR(1) Likelihood:**
        $$L = \underbrace{\sqrt{1-\phi^2}(\frac{1}{2\pi\sigma^2})^{\frac{1}{2}}e^{-\frac{1}{2\sigma^2}(1-\phi^2)Y_1^2}}_{\text{Initial } Y_1} \times \underbrace{(\frac{1}{2\pi\sigma^2})^{\frac{n-1}{2}}e^{-\frac{1}{2\sigma^2}\sum_{t=2}^n(Y_t-\phi Y_{t-1})^2}}_{\text{Conditional Part}}$$
  * **Method II: Multivariate Normal (Explicit Form)**
      * $L \propto |\Sigma|^{-1/2}exp\{-\frac{1}{2}y^{T}\Sigma^{-1}y\}$ where $\Sigma_{ij}=\gamma(|i-j|)$.
      * Simpler form but computationally harder to optimize matrix inverse.

-----

<font color="navy">**6. Partial ACF (PACF) Calculation**</font>

  * **Definition:** $\phi_{kk}$ is the coefficient of $Y_{t-k}$ in an AR(k) regression $Y_t = \sum_{j=1}^k \phi_{kj} Y_{t-j} + Z_t$.
  * **Calculation via Correlation:**
      * $\phi_{11} = \rho(1)$.
      * $\phi_{22} = \frac{\rho(2)-\rho(1)^{2}}{1-\rho(1)^{2}}$.
      * General $k$: Solve $\boldsymbol{\rho}_k = \boldsymbol{R}_k \boldsymbol{\phi}_k$ (same structure as YW).
  * **MA(1) PACF Formula:** $\phi_{kk} = -\frac{(-\theta)^{k}(1-\theta^{2})}{1-\theta^{2(k+1)}}$ (Decays exponentially).
  * **Pattern Identification:**
      * **AR(p):** PACF cuts off at lag $p$ ($\phi_{kk}=0$ for $k>p$).
      * **MA(q):** PACF decays/trails off.
      * **Significance:** Sample PACF $\hat{\phi}_{kk}$ is significant if $|\hat{\phi}_{kk}| > 2/\sqrt{n}$.