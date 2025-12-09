**1. Using Auxiliary Data & Ratio Estimation (SRS)**

**Notation (SRS & ratio)**
 $N$ pop. size; $n$ SRS size; $Y_i,X_i$ values for unit $i$;
 $\tau_y=\sum_{i=1}^N Y_i$; $\tau_x=\sum_{i=1}^N X_i$; $\mu_y=\tau_y/N$; $\mu_x=\tau_x/N$; $\bar{Y}=\frac1n\sum Y_i$; 
$\bar{X}=\frac1n\sum X_i$; $R=\tau_y/\tau_x=\mu_y/\mu_x$; $\hat{R}=\bar{Y}/\bar{X}$; 
$\sigma_y^2,\sigma_x^2,\sigma_{xy}$ population var/cov; $\hat{\sigma}_y^2=\frac{1}{n-1}\sum(Y_i-\bar{Y})^2$; $\hat{\sigma}_x^2=\frac{1}{n-1}\sum(X_i-\bar{X})^2$;
$Z_i=Y_i-RX_i$; $\sigma_r^2=\frac1N\sum(Y_i-RX_i)^2$;  $\hat{cv}_x=\hat{\sigma}_x/\bar{X}$; $\hat{cv}_y=\hat{\sigma}_y/\bar{Y}$;
Auxiliary $X$ is easy/cheap and strongly related to $Y$; assume $Y_i\approx RX_i$ (through origin).

**1.1 Ratio estimators**
 Population ratio: $R=\tau_y/\tau_x=\mu_y/\mu_x$. Sample ratio: $\hat{R}=\bar{Y}/\bar{X}$.
 ==Total==: $\hat{\tau}_r=\hat{R}\tau_x=(\bar{Y}/\bar{X})\tau_x$.    ==Mean==: $\hat{\mu}_r=\hat{R}\mu_x=(\bar{Y}/\bar{X})\mu_x$.
 Bias exists but small for large $n$, so MSE $\approx$ variance.

**1.2 Variance approximations**
 Define $Z_i=Y_i-RX_i$, $\sigma_r^2=\frac1N\sum(Y_i-RX_i)^2$, $\hat{\sigma}_r^2=\frac{1}{n-1}\sum(Y_i-\hat{R}X_i)^2$.
 Approx design var of $\hat{\mu}_r$: $\operatorname{Var}(\hat{\mu}_r)\approx\frac{N-n}{N-1}\frac{1}{n}\sigma_r^2$.
 Estimator: $\widehat{\operatorname{Var}}(\hat{\mu}_r)=\Big(1-\frac{n}{N}\Big)\frac{1}{n}\hat{\sigma}_r^2$.
Total: $\operatorname{Var}(\hat{\tau}_r)\approx\frac{N-n}{N-1}\frac{N^2}{n}\sigma_r^2$,  $\widehat{\operatorname{Var}}(\hat{\tau}_r)=\frac{N-n}{N}\frac{N^2}{n}\hat{\sigma}_r^2$.
Ratio $R$: $\operatorname{Var}(\hat{R})\approx\frac{1}{\mu_x^2}\frac{N-n}{N-1}\frac{1}{n}\sigma_r^2$,  $\widehat{\operatorname{Var}}(\hat{R})=\frac{1}{\mu_x^2}\Big(1-\frac{n}{N}\Big)\frac{1}{n}\hat{\sigma}_r^2$.

**1.3 When is ratio better than SRS?**
 <font color=red>SRS mean</font>: $\bar{Y}$, $\widehat{\operatorname{Var}}(\bar{Y})=\Big(1-\frac{n}{N}\Big)\frac{\hat{\sigma}_y^2}{n}$.  <font color=red>Ratio mean</font>: $\hat{\mu}_r$, $\widehat{\operatorname{Var}}(\hat{\mu}_r)=\Big(1-\frac{n}{N}\Big)\frac{\hat{\sigma}_r^2}{n}$.
Key identity: $\hat{\sigma}_r^2=\hat{\sigma}_y^2+\hat{R}^2\hat{\sigma}_x^2-2\hat{R}\hat{\rho}\hat{\sigma}_x\hat{\sigma}_y$.   $\hat{\rho}=\hat{\sigma}_{xy}/(\hat{\sigma}_x\hat{\sigma}_y)$
Ratio better if ==$\hat{\sigma}_r^2\ll\hat{\sigma}_y^2$==. Sufficient condition: $\hat{\rho}\gg\frac12{\hat{cv}_x}/{(\hat{cv}_y)}$. or When $\hat{c}_{v, x}\approx\hat{c}_{v,y}$, “$\hat{\rho}>0.5$ usually enough”.

**1.4 CI & sample size **
CI: $\text{Point Estimator}\pm t_{n-1,1-\alpha/2}\sqrt{\widehat{\operatorname{Var}}(E)}$.
Planning (approx): $d=z_{1-\alpha/2}\sqrt{\operatorname{Var}(E)}$ with assumed $\sigma_r^2$, or iteratively solve $d=t_{n-1,1-\alpha/2}\sqrt{\widehat{\operatorname{Var}}(E)}$ for $n$.

------

**2. Ratio Estimation in Cluster Sampling**

**Notation (clusters)**
 $N$ #clusters; $M_i$ cluster size; $M=\sum_{j=1}^N M_j$ total elements; $Y_i$ total $Y$ in cluster $i$; $\bar{Y}_i$ sample mean in cluster $i$ (if 2-stage); $\hat{Y}_i=M_i\bar{Y}_i$ 
est. cluster total; $A_i$ count with a characteristic in cluster $i$; $p$ pop proportion; $\hat{p}_i$ cluster sample proportion.

Auxiliary variable: $M_i$. Ratio good when $Y_i$ and $M_i$ are highly correlated (cluster total ≈ proportional to size).

**2.1 One-stage clusters, total $\tau_y$**
 Pop: $N$ clusters, $M$ known. Sample: SRS of $n$ clusters, observe $(M_i,Y_i)$.
 Sample means: $\bar{Y}=\frac1n\sum Y_i$, $\bar{M}=\frac1n\sum M_i$.
 Ratio est of total: $\hat{\tau}_r=\frac{\bar{Y}}{\bar{M}}M=\hat{R}M$, where $\hat{R}=\bar{Y}/\bar{M}$. 
 Variance est: $\widehat{\operatorname{Var}}(\hat{\tau}_r)=N(N-n)\frac1n\hat{\sigma}_r^2$, $\hat{\sigma}_r^2=\frac{1}{n-1}\sum(Y_i-\hat{R}M_i)^2$.

**2.2 One-stage clusters, proportion $p$**
 Let $A_i$ the number of people in the cluster $i$ who have a certain characteristic.
 Ratio est of $p$: $\hat{p}_r={\sum_{i=1}^N A_i}/{\sum_{i=1}^N M_i}$.
 Var est: $\widehat{\operatorname{Var}}(\hat{p}_r)=\dfrac{N-n}{N}\dfrac{N^2}{M^2}\dfrac{\hat{\sigma}_r^2}{n}$,  $\hat{\sigma}_r^2=\dfrac{1}{n-1}\sum(A_i-\hat{p}_rM_i)^2$.

------

**3. Ratio Estimation in Two-stage Cluster Sampling**

**Notation (two-stage)**
 $N$ clusters; cluster $i$ has $M_i$ elements, $M=\sum_{i=1}^N M_i$; stage 1: SRS of $n$ clusters; stage 2 in cluster $i$: SRS of $m_i$ elements; $Y_{ij}$ value for element $j$ in cluster $i$; $\bar{Y}_i$ sample mean in cluster $i$; $\hat{Y}_i=M_i\bar{Y}_i$; for proportions: $\hat{p}_i$ within-cluster prop. Within-cluster var: $\hat{\sigma}_i^2=\frac{1}{m_i-1}\sum(Y_{ij}-\bar{Y}_i)^2$ (or $\hat{\sigma}_i^2=\frac{m_i}{m_i-1}\hat{p}_i(1-\hat{p}_i)$ for binary).

**3.1 Two-stage: mean $\mu_y$**
 Ratio est: $\hat{\mu}_r=\dfrac{\sum_{i=1}^n M_i\bar{Y}_i}{\sum_{i=1}^n M_i}=\dfrac{\sum_{i=1}^n \hat{Y}_i}{\sum_{i=1}^n M_i}$.
 Between-cluster var est: $\hat{\sigma}_r^2=\dfrac{1}{n-1}\sum(\hat{Y}_i-\hat{\mu}_rM_i)^2$.
 Design var est: $\widehat{\operatorname{Var}}(\hat{\mu}_r)=\dfrac{1}{M^2}{N(N-n)\dfrac{1}{n}\hat{\sigma}_r^2+\frac1{M^2}\dfrac{N}{n}\sum_{i=1}^n M_i(M_i-m_i)\dfrac{1}{m_i}\hat{\sigma}_i^2}$.

**3.2 Two-stage: total $\tau_y$ and proportion $p$**
 Total: $\hat{\tau}_r=M\dfrac{\sum\hat{Y}_i}{\sum M_i}$,
 $\widehat{\operatorname{Var}}(\hat{\tau}_r)=N(N-n)\dfrac{1}{n}\hat{\sigma}_r^2+\dfrac{N}{n}\sum_{i=1}^n M_i(M_i-m_i)\dfrac{1}{m_i}\hat{\sigma}_i^2$ $\hat{\sigma}_r^2=\dfrac{1}{n-1}\sum(\hat{Y}_i-\hat{\mu}_rM_i)^2$.

Proportion: $\hat{p}_r=\dfrac{\sum M_i\hat{p}_i}{\sum M_i}$.
 Var est: $\widehat{\operatorname{Var}}(\hat{p}_r)=\dfrac{N(N-n)}{nM^2}\hat{\sigma}_r^2+\dfrac{N}{nM^2}\sum_{i=1}^n M_i(M_i-m_i)\dfrac{1}{m_i}\hat{\sigma}_i^2$,
 $\hat{\sigma}_r^2=\dfrac{1}{n-1}\sum(M_i\hat{p}_i-\hat{p}_rM_i)^2$, $\hat{\sigma}_i^2=\dfrac{m_i}{m_i-1}\hat{p}_i(1-\hat{p}_i)$.

------

**4. Regression Estimation (SRS)**

**Notation (regression)**
known aux: $\mu_x,\tau_x$; $N,n,\hat{\rho}$ as before.
Regression = generalisation of ratio (allows non-zero intercept). Use when $(X,Y)$ approx linear but not through origin.

**4.1 LS estimators**
 $\hat{b}=\dfrac{\sum_{i=1}^n(X_i-\bar{X})(Y_i-\bar{Y})}{\sum_{i=1}^n(X_i-\bar{X})^2}=\dfrac{\sum_{i=1}^n X_iY_i-\frac1n(\sum_{i=1}^n X_i)(\sum_{i=1}^n Y_i)}{\sum_{i=1}^n X_i^2-\frac1n(\sum_{i=1}^n X_i)^2}$,
 $\hat{a}=\bar{Y}-\hat{b}\bar{X}$, $\hat{Y}_i=\hat{a}+\hat{b}X_i$.

**4.2 Regression estimator for mean $\mu_y$**
 Assume $\mu_x$ known.
 Estimator: $\hat{\mu}_L=\hat{a}+\hat{b}\mu_x=\bar{Y}+\hat{b}(\mu_x-\bar{X})$. Var est: $\widehat{\operatorname{Var}}(\hat{\mu}_L)=\dfrac{N-n}{Nn}\dfrac{1}{n-2}\sum_{i=1}^n(Y_i-\hat{a}-\hat{b}X_i)^2$.
 Approx (large $n$): $\operatorname{Var}(\hat{\mu}_L)\approx\dfrac{N-n}{Nn}\sigma_y^2(1-\hat{\rho}^2)$. CI: $\hat{\mu}_L\pm t_{n-2,1-\alpha/2}\sqrt{\widehat{\operatorname{Var}}(\hat{\mu}_L)}$ 

**4.3 Regression estimator for total $\tau_y$**
 Estimator: $\hat{\tau}_L=\hat{a}N+\hat{b}\tau_x$.  Var est: $\widehat{\operatorname{Var}}(\hat{\tau}_L)=N(N-n)\dfrac{1}{n}\dfrac{1}{n-2}\sum(Y_i-\hat{a}-\hat{b}X_i)^2$.

**4.4 SRS vs ratio vs regression (quick comparison)**

- SRS: $\bar{Y}$ (or $N\bar{Y}$) unbiased, no aux info.
- Ratio: assumes line through origin; best when scatter is tight around $Y\approx RX$ and $X$ known at pop level. Often largest gain when that assumption holds.
- Regression: line with intercept; gain roughly factor ==$(1-\hat{\rho}^2)$== vs SRS; more flexible than ratio when origin assumption fails.