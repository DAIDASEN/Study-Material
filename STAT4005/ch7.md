<font size="4" color="darkblue">**1. Nonstationarity in Mean: TS vs. DS**</font>

- **Trend Stationary (TS):** $Y_t = \beta_0 + \beta_1 t + \nu_t$. Has deterministic trend. **Fix:** Detrending (Regression).
- **Difference Stationary (DS):** $Y_t = \beta_1 + Y_{t-1} + \nu_t$ (Random Walk with drift). Has stochastic trend. **Fix:** Differencing ($\nabla Y_t = Y_t - Y_{t-1}$).
- **Encompassing Model:** $Y_t = \gamma_0 + \gamma_1 t + \alpha Y_{t-1} + Z_t$.
- If <font color="red">**$\alpha = 1$**</font> $\rightarrow$ **DS** (Unit Root, Non-stationary). If <font color="red">**$|\alpha| < 1$**</font> $\rightarrow$ **TS** (Mean Reverting, Stationary).

<font color="brown">**Unit Root Test (Dickey-Fuller Test)**</font> 查是不是Stationary

- **Hypothesis:** <font color="red">**$H_0: \alpha = 1$**</font> (Non-stationary) vs. $H_1: \alpha < 1$ (Stationary).
- **Test Statistic:** $\hat{\alpha} = \frac{\sum Y_t Y_{t-1}}{\sum Y_{t-1}^2}$. Statistic $T = n(\hat{\alpha} - 1)$.
- Distribution: NOT Normal/t-distribution! Follows Dickey-Fuller Distribution (via FCLT):
  $$n(\hat{\alpha}-1) \xrightarrow{d} \frac{\int_0^1 W(t) dW(t)}{\int_0^1 W^2(t) dt}$$
- **Decision:** Reject $H_0$ if statistic < Critical Value or $\text{p-value}<=0.05 \Rightarrow \text{Stationary}$  

Based on the R-output, as p-value is less than 0.05, there is significant evidence to claim that $\alpha <1$. i. e., the model is weakly-stationary.

------

<font size="4" color="darkblue">**2. Nonstationarity in Variance**</font>

<font color="brown">**Case A: Deterministic Change (Variance Stabilization)**</font>

- **Situation:** Variance depends on mean, $Var(Y_t) \propto h^2(\mu_t)$.

- **Goal:** Find transformation $g(Y_t)$ such that $Var(g(Y_t)) \approx \text{Constant}$.

- **Formula: **
  $g(Y) \approx g(\mu) + g'(\mu)(Y-\mu)
  \Rightarrow Var(g(Y)) \approx [g'(\mu)]^2 h^2(\mu)\sigma^2$.

  To make variance constant, set $g'(\mu) = \frac{k}{h(\mu)}$. $$g(x) = k \int \frac{1}{h(\mu)} d\mu$$

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
  $$\sigma_t^2 = \alpha_0 + \alpha_1 X_{t-1}^2 + \dots + \alpha_q X_{t-q}^2$$
- **Constraints:** $\alpha_i \ge 0$ (Positivity), <font color="red">**$\sum_{i=1}^q \alpha_i < 1$**</font> (Stationarity).

<font color="purple">**ARCH(q) $\Leftrightarrow$ AR(q) for $X_t^2$**</font>
The white-noise sequence is given by $v_t = X_t^2 - \sigma_t^2 = \sigma_t^2 (\epsilon_t^2 - 1)$. Then $\{X_t^2\} \sim \text{ARMA}(q, 0)$ which is an $\text{AR}(q)$ process, as
$$X_t^2 = \sigma_t^2 + (X_t^2 - \sigma_t^2)$$ Noticed that $\sigma_t^2 = \alpha_0 + \sum_{i=1}^{q} \alpha_i X_{t-i}^2$.
$$X_t^2 = \alpha_0 + \sum_{i=1}^{q} \alpha_i X_{t-i}^2 + v_t$$ where $\text{E}(v_t) = 0$ and $\text{Cov}(v_t, v_{t-h}) = 0$ for $h \ne 0$.

**Properties (ARCH(1)):**
<font color=black>1. Unconditional Mean: $E[X_t] = 0$.
<font color=black>2. Unconditional Variance: $\text{Var}(X_t) = E[X_t^2] = \frac{\alpha_0}{1 - \alpha_1}$ (Condition: $\alpha_1 < 1$).
<font color=black>3. Kurtosis (4th Moment): $E(X_t^4) = \frac{3\alpha_0^2(1+\alpha_1)}{(1-\alpha_1)(1-3\alpha_1^2)}$. Exists only if $3\alpha_1^2 < 1$.
<font color=black>4. ACF of $X_t^2$: $\text{Corr}(X_t^2, X_{t+h}^2) = \alpha_1^{|h|}$ (Decays like AR process).

------

<font size="4" color="darkblue">**4. GARCH(p, q) Model**</font>

- Definition: Adds lagged variance terms.
  $$\sigma_t^2 = \alpha_0 + \sum_{i=1}^q \alpha_i X_{t-i}^2 + \sum_{j=1}^p \beta_j \sigma_{t-j}^2$$
- **Stationarity 成立条件:** <font color="red">**$\sum \alpha_i + \sum \beta_j < 1$**</font>.

<font color="purple">**Comparison: Unconditional vs. Conditional Moments (Stationary GARCH)**</font>

| Quantity       | **Unconditional (Long-run)**                                 | **Conditional on $\mathcal{F}_{t-1}$ (Short-run)** |
| -------------- | ------------------------------------------------------------ | -------------------------------------------------- |
| **Mean**       | $E(X_t)=0$                                                   | $E(X_t|\mathcal{F}_{t-1})=0$                       |
| **Variance**   | $Var(X_t)$ $\frac{\alpha_0}{1-\sum_q\alpha_i+\sum_p\beta_j)}$ | $Var(X_t|\mathcal{F}_{t-1}) \sigma_t^2$            |
| **Covariance** | $Cov(X_t,X_{t+h})=0$                                         | $Cov(X_t,X_{t+h}|\mathcal{F}_{t-1})=0$             |

**I-GARCH (Integrated Non-Stationary):** 
If $\alpha_1 + \beta_1 = 1$. Non-stationary.
Forecasting variance: $E[\sigma_{t+j}^2|\mathcal{F}_{t-1}] = j\alpha_0 + \sigma_t^2$ (Linear growth).

<font color="purple">**KEY DERIVATION: GARCH(p,q) $\Leftrightarrow$ ARMA(m, p) for $X_t^2$**</font>
Conditions: 1. 是Stationary的 2. $E(\sigma_t^4)$ exists and is constant over-time
The white-noise sequence is given by $v_t = X_t^2 - \sigma_t^2 = \sigma_t^2 (\epsilon_t^2 - 1)$. Then $\{X_t^2\} \sim \text{ARMA}(m, p)$ as
$X_t^2 = \sigma_t^2 + (X_t^2 - \sigma_t^2) = \alpha_0 + \sum_{j=1}^{q} \alpha_j X_{t-j}^2 + \sum_{i=1}^{p} \beta_i \sigma_{t-i}^2 + (X_t^2 - \sigma_t^2)$$= \alpha_0 + \sum_{j=1}^{m} (\alpha_j + \beta_j) X_{t-j}^2 - \sum_{i=1}^{p} \beta_i (X_{t-i}^2 - \sigma_{t-i}^2) + v_t$$$= \alpha_0 + \sum_{j=1}^{m} (\alpha_j + \beta_j) X_{t-j}^2 + v_t - \sum_{i=1}^{p} \beta_i v_{t-i}$$
where $\alpha_i := 0$ and $\beta_j := 0$ for $i \ge q, j \ge p$.

------

<font size="4" color="darkblue">**5. Estimation & Testing Flow**</font>
**异方差 (Heteroscedasticity)** **同方差 (Homoscedasticity)**

**<font color="brown">A. Detecting Heteroskedasticity (LM Test)</font>**
$H_ 0$: No ARCH effect  $H_1$: ARCH effect exists
Run auxiliary regression of squared residuals: $X_t^2 = \alpha_0 + \alpha_1 X_{t-1}^2 + \dots + \alpha_q X_{t-q}^2$
**Statistic:** $T = n \times R^2 \rightarrow \chi^2(q)$.
**Rule:** If $T> \chi^2_{0.95, p}$ (or p-value < 0.05), **Reject $H_0$**

**<font color="brown">B. Estimation (MLE)</font>**
**Method:** Use Maximum Likelihood (MLE), **NOT OLS** (because variance changes).
Log-Likelihood Function (to maximize):
$l(\theta) = -\frac{n}{2}\ln(2\pi) - \frac{1}{2}\sum_{t=1}^n \left( \ln(\sigma_t^2) + \frac{X_t^2}{\sigma_t^2} \right)$
(Must compute $\sigma_t^2$ recursively from $t=1$ to $n$).

<font color="brown">**C. Model Selection**</font>: 
Use **AIC / BIC**.
Note: PACF of $X_t^2$ works for ARCH order identification, but fails for GARCH.

**<font color="brown">D. Diagnostics (Goodness of Fit)</font>** 
**Object:** Standardized Squared Residuals: $\hat{\epsilon}_t^2 = \frac{X_t^2}{\hat{\sigma}_t^2}$.
**Test:** **Ljung-Box Test** on $\hat{\epsilon}_t^2$.
**Statistic:** $Q(h) = n(n+2) \sum_{j=1}^{h} \frac{r^2(j)}{n-j}\rightarrow\chi^2(h - p - q - 1)$.
**Goal:** Fail to reject $H_0$ (High p-value > 0.05) $\rightarrow$ No correlation left $\rightarrow$ Good Model.