==<font color="navy">**Systematic Sampling**</font>==

<font color="navy">**1. Definition of 1-in-$k$ Systematic Sampling**</font>
<font color="navy">The Process</font>  
<font color="navy">1.</font> Population elements are ordered in a list (time, space, or any fixed order).  
<font color="navy">2.</font> Choose an integer interval $k$. Ideally, $k = N/n$, $N$ and desired $n$.  
<font color="navy">3.</font> Randomly select a start $r$ from $\{1, 2, \dots, k\}$.  
<font color="navy">4.</font> Select units with indices  $r,\ r+k,\ r+2k,\ \dots,\ r+(n-1)k.$
<font color="red">Unknown Population Size $N$</font> : If $N$ is unknown (e.g. stopping shoppers at a mall), we must guess a value for $k$.  If $k$ is chosen too large, we might not achieve the desired sample size $n$ before the population list is exhausted.

<font color="navy">**2. Systematic Sampling as One-Stage Cluster Sampling**</font>
• Systematic sampling is statistically equivalent to selecting $n=1$ cluster from a population of $k$ possible clusters.
<font color="navy">Cluster notation mapping</font> 
• N is the number of primary units in the population 
• n is the number of primary units in the sample (Normally n = 1)
• $M_i$ is the number of secondary units in the *i*th primary unit 
• $M = \sum_{i=1}^{N} M_i$ is the total number of secondary units in the population
• $Y_{ij}$ is the *j*th observation in the *i*th primary unit 
• $Y_i = \sum_{j=1}^{M_i} Y_{ij}$ is the total of observations in the $i$th primary unit

<font color="navy">**3. Estimating Population Total and Mean**</font>
<font color="navy">4.1 Estimator via cluster view (one selected cluster)</font>  
Population:  $\hat{\tau}_{sys} = NY_1 = kY_1$    $Var(\hat\tau) = N^2\sigma^2_c$    $\widehat{Var}(\hat \tau) =N^2(1-n/N)\hat \sigma_c^2/n$    $\hat \sigma_c^2$ can't be calculate  $\Rightarrow$ Regard it as SRS.
<font color=red>Assumption: </font>the secondary units are in random order
$Var(\hat{t}_{\text{sys}}) \approx \frac{M - M_1}{M_1}  \frac{M^2}{M - 1}  \sigma^2$ $
\hat{V}ar(\hat{t}_{\text{sys}}) \approx M^2 \left(1 - \frac{M_1}{M} \right)  \frac{1}{M_1}  \hat{\sigma}^2= \frac{M^2}{M_1} \left(1 - \frac{M_1}{M} \right)  \frac{1}{M_1 - 1} \sum_{j=1}^{M_1} \left(Y_{1j} - \bar{Y}_1 \right)^2
$

<font color="navy">**5. Approximate Variance under Random Ordering (SRS Assumption)**</font>
Because $n=1$ at the cluster level, we cannot estimate the variance directly without assumptions. We assume the list is in random order, so the systematic sample behaves like a simple random sample.

<font color="navy">5.1 Approximate variance of the mean</font>  
Using the finite population correction (FPC):  $\widehat{\operatorname{Var}}(\bar{y}_{sys}) \approx \left(1 - \frac{n}{N}\right)\frac{s^2}{n}$

<font color="navy">5.2 Approximate variance of the total</font> $\widehat{\operatorname{Var}}(\hat{\tau}_{sys}) \approx N^2 \left(1 - \frac{n}{N}\right)\frac{s^2}{n}$

<font color="navy">5.3 Confidence interval (t-based)</font>  For large $n$, or under normality:  $\bar{y}_{sys} \pm t_{n-1, 1-\alpha/2} \sqrt{\widehat{\operatorname{Var}}(\bar{y}_{sys})}$

<font color="navy">**6. Cluster Variance, ICC, and the Guiding Principle**</font>

<font color="navy">6.1 Definition of ICC (from Lecture)</font>  
Based on equal cluster size $\bar{M}$, the intraclass correlation coefficient is  $ICC = \frac{\sum_{i=1}^{N}\sum_{j=1}^{\bar{M}}\sum_{k\ne j}(Y_{ij}-\mu)(Y_{ik}-\mu)}{N\bar{M}(\bar{M}-1)\sigma^2}$
It measures the correlation between pairs of elements within the same cluster.

<font color="navy">6.2 Relationship between variances</font>  
Assume all clusters have the same size $\bar{M}$.  
• Relationship between cluster-level variance and element-level variance:  $\sigma_c^2 = \bar{M}\sigma^2 \bigl(1 + (\bar{M}-1)ICC\bigr)$ 

<font color="navy">6.3 Variance of total under cluster sampling</font>  
If we select multiple clusters, the variance depends on $ICC$:  $\operatorname{Var}(\hat{\tau}) \propto \sigma_c^2 \propto \bigl(1 + (\bar{M}-1)ICC\bigr)$
• If $ICC \approx 0$: design behaves like SRS.  
• If $ICC > 0$: variance is inflated (homogeneous clusters).  
• If $ICC < 0$: variance is reduced (heterogeneous clusters).  

<font color="navy">6.4 Guiding principle for variance reduction</font>  
• To obtain estimators with low variance, clusters should be internally heterogeneous (high within-cluster variance) and similar to each other (low between-cluster variance).  
• Cluster sampling often violates this: grouping neighbors (e.g. geographic blocks) usually creates homogeneous clusters (high $ICC$), leading to higher variance.  
• Systematic sampling often follows this: because sample points are spaced apart by $k$, elements within the systematic sample are usually diverse (heterogeneous), leading to low or negative $ICC$ and lower variance.

<font color="navy">**7. Effect of Population Ordering on Systematic Sampling**</font>
The sign and magnitude of $ICC$ depend on how the frame is ordered.

<font color="navy">7.1 Random ordering</font>  
• Ordering is independent of $y_i$.  • $ICC \approx 0$.  
• Result: SRS variance formulas are accurate:  $\widehat{\operatorname{Var}}(\bar{y}_{sys}) \approx \widehat{\operatorname{Var}}(\bar{y}_{SRS})$

<font color="navy">7.2 Monotone trend (increasing/decreasing)</font>  
• Values $y_i$ show a smooth trend. Systematic sampling spreads sample points across the range.  
• $ICC < 0$.  
• Result: true variance is smaller than SRS approximation:  $\operatorname{Var}(\bar{y}_{sys}) < \operatorname{Var}(\bar{y}_{SRS})$
• Implication: SRS formulas overestimate variance (conservative / safe).

<font color="navy">7.3 Periodic pattern</font>  
• Values repeat in a cycle with period $P$.  
• If $k \approx P$ (or a multiple), all selected elements may come from the same phase (e.g. all peaks).  
• $ICC > 0$ (strongly positive).  
• Result: true variance is much larger than SRS approximation:  $\operatorname{Var}(\bar{y}_{sys}) \gg \operatorname{Var}(\bar{y}_{SRS})$
• Implication: SRS formulas underestimate variance (dangerous / misleading).

---

<font color="navy">**8. Repeated Systematic Sampling**</font>

Repeated systematic sampling is used to estimate variance directly when the random-order assumption is unsafe.

<font color="navy">8.1 Design idea</font>  
• Instead of one large 1-in-$k$ sample, take $n_s$ separate systematic samples.  
• New interval: $k' = n_s  k$.  
• Select $n_s$ random starts $r_1, \dots, r_{n_s}$ from $\{1, \dots, k'\}$.  
• This creates $n_s$ clusters (repeated systematic samples), allowing us to compute a variance.

<font color="navy">8.2 Estimator and variance (cluster formulas)</font>  
Let $K' = k'$ be the total number of possible clusters. Let $Y_i$ be the total of the $i$-th repeated systematic sample ($i=1, \dots, n_s$).  
• Estimator of population total: $\hat{\tau} = \frac{K'}{n_s} \sum_{i=1}^{n_s} Y_i = K' \bar{Y},\quad \bar{Y} = \frac{1}{n_s}\sum_{i=1}^{n_s} Y_i$
• Sample variance of cluster totals: $s_c^2 = \frac{1}{n_s - 1} \sum_{i=1}^{n_s} (Y_i - \bar{Y})^2$
• Estimated variance of $\hat{\tau}$: $\widehat{\operatorname{Var}}(\hat{\tau}) = (K')^2 \left(1 - \frac{n_s}{K'}\right)\frac{s_c^2}{n_s}$
Note: this treats repeated systematic samples as clusters in a one-stage cluster sampling design with $K'$ clusters and sample size $n_s$.

---

==<font color="navy">**Auxiliary Data**</font>==

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
• SRS: $\bar{Y}$ (or $N\bar{Y}$) unbiased, no aux info.
• Ratio: assumes line through origin; best when scatter is tight around $Y\approx RX$ and $X$ known at pop level. Often largest gain when that assumption holds.
• Regression: line with intercept; gain roughly factor ==$(1-\hat{\rho}^2)$== vs SRS; more flexible than ratio when origin assumption fails.