**Mean** performs best when we have a symmetric distribution with thin tails.  If skewed, use the **median**. The **mean** may be more affected by the tails.

==**The *p*th percentile**==
**Case 1:** If $\frac{np}{100}$ is **not an integer**: Let $k$ = smallest integer > $\frac{np}{100}$   the *p*th percentile is the $k$th smallest sample point
**Case 2:** If $\frac{np}{100}$ is **an integer**: The *p*th percentile is the average of the $(\frac{np}{100})$th and $(\frac{np}{100}+1)$th smallest sample points
**Positively Skewed / Right Skewed**: Upper hinge is farther from the Median than the lower hinge. The distribution has a longer tail on the right side
**Negatively Skewed / Left Skewed**: Lower hinge is farther from the Median than the upper hinge. The distribution has a longer tail on the left side
==**Population Parameters**==

$$\text{Var}(aX + bY + c) = a^2\text{Var}(X) + b^2\text{Var}(Y) + 2ab\text{Cov}(X,Y)$$
**Sample Correlation Coefficient**: $$r = \frac{1}{n-1}\sum_{i=1}^{n}\left(\frac{x_i - \bar{x}}{s_x}\right)\left(\frac{y_i - \bar{y}}{s_y}\right)$$
$Cov(X, Y) = \frac1N\sum_{i=1}^{N}[(y_i-\mu_Y)(x_i-\mu_X)] = E(XY)-E(X)E(Y)$        $$\rho_{X,Y} = \frac{\text{Cov}(X,Y)}{\sigma_X \sigma_Y}$$
**Binomial**: $X \sim B(n, p)$.If $X \sim B(n, p)$ and $np \geq 10$, $n(1-p) \geq 10$,  $\mu_X = np$, $\sigma_X = \sqrt{np(1-p)}$, $$Z = \frac{X - np}{\sqrt{np(1-p)}}$$
**Normal**: $$f(x) = \frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{1}{2}\left(\frac{x-\mu}{\sigma}\right)^2}$$
**corrected population variance**: $$S^2 = \frac{1}{N-1} \sum_{i=1}^{N} (u_i - \mu)^2$$
The factor $\frac{1}{N-1}$ simplifies many formulas in statistical analysis. This adjustment is useful in various statistical contexts. $\sigma^2$ better reflects the idea of variance as an expectation: $$\text{Var}(Y) = E[(Y-\mu)^2]$$
The quantity $E[\hat{\theta} - \theta]$ is called the **bias** of the estimator $\hat{\theta}$. We want our estimators to be unbiased, i.e., to have zero bias. An unbiased estimator satisfies $E[\hat{\theta}] = \theta$, $MSE(\hat{\theta}) = Var(\hat{\theta})$

$$MSE(\hat{\theta}) = Var(\hat{\theta}) + [Bias(\hat{\theta})]^2$$
**Unbiased**: $E[\hat{\theta}] = \theta$, **Precise**: $Var(\hat{\theta})$ is small (The estimates from different samples are close to each other), **Accurate**: unbiased&precise

==**Survey Terminology:**==
<font color=black>1. </font>Population: A collection of elements about which we want to make inferences
<font color=black>2. </font>Element: An element is an object on which a measurement is taken
<font color=black>3. </font>Sampling Units: Partition the population
<font color=black>4. </font>Frame: A frame is a list of sampling units
<font color=black>5. </font>Sample: A collection of sampling units drawn from a single or from multiple frames

<font color=Red>Probability Sampling:</font> Each population unit has a known and non-zero probability of being selected, and the sampling process relies entirely on a random mechanism. **Can make probability statements (e.g. *Confidence Intervals*)** <font color = blue>Randomisation balances out all factors inherent in a  population</font>
<font color=red>Quota Sampling:</font> Quotas are first established based on certain characteristics (such as gender, age, region), then interviewers **subjectively** or conveniently select samples within each quota.  **Can not make probability statements**

---

**==Simple Random Sampling(SRS)==** : Random sampling without replacement such that every possible sample of 𝑛 units is equally likely 
$\pi_i = P(\text{Element } i \text{ is in the sample})$
We can write $\pi_i = E[Z_i]$ 
$\pi_i = \frac{\text{Number of samples containing element }i}{\text{Total number of possible samples}}$
$$\pi_i = Pr(Z_j=1) = \frac{\binom{N-1}{n-1}}{\binom{N}{n}} = \frac{\frac{(N-1)!}{(n-1)!(N-n)!}}{\frac{N!}{n!(N-n)!}} = \frac{n}{N} = E[Z_i]$$
**Methods** 1. Draw Lots 2. Random Number Table 3.Random Numbers in Excel/R

<font color=purple>**Notation（抽样率 & f.p.c.）**</font>  
**population size** $N$，**sample size** $n$，**sampling fraction **$f=\frac{n}{N}$，**finite population correction** f.p.c.$=1-f=1-\frac{n}{N}$。  
**population mean** $\mu=\frac{1}{N}\sum_{j=1}^N u_j$。样本观测记为$Y_1,\dots,Y_n$，样本均值$\bar Y=\frac{1}{n}\sum_{i=1}^n Y_i=\frac{1}{n}\sum_{j=1}^N u_j Z_j$。

==**Estimating sample mean $\mu$**==
$$\hat \mu = \bar{Y} = \frac{1}{n} \sum_{j=1}^{N} u_j Z_j$$
*<font color=blue>Proof of unbiased:</font>* $$E[\bar{Y}] = \frac{1}{n} \sum_{j=1}^{N} u_j E[Z_j] = \frac{1}{n} \sum_{j=1}^{N} u_j \frac{n}{N} = \frac{1}{N} \sum_{j=1}^{N} u_j = \mu$$
$$Var(\bar{Y}) = \frac{N-n}{N-1}\frac{1}{n}\sigma^2$$
$$\widehat{Var}(\bar{Y}) = \frac{N-n}{N-1}\frac{\hat{\sigma}^2}{n} = \left(1-\frac{n}{N}\right)\frac{\hat{\sigma}^2}{n}$$ , where $\hat{\sigma}^2 = \frac{1}{n-1}\sum_{i=1}^{n}(Y_i-\bar{Y})^2$ is the unbiased estimator of the population variance. $\left(1 - \frac{1}{N}\right) \hat{\sigma}^2$ is an unbiased estimator for $\sigma^2$
<font color=blue>*Proof:*</font>
$$Var(\bar{Y}) = \sum_{j=1}^{N} \left(\frac{u_j}{n}\right)^2 Var(Z_j) + \sum_{j=1}^{N}\sum_{k\neq j} \frac{u_j}{n}\frac{u_k}{n}Cov(Z_j, Z_k)$$
$$Var(Z_j) = \frac{n}{N}\left(1-\frac{n}{N}\right)$$, $$E(Z_j)= {\frac{n}{N}}$$
$$Cov(Z_j, Z_k) = E[Z_j Z_k] - E[Z_j]E[Z_k] = E[Z_j Z_k] - \left(\frac{n}{N}\right)^2$$
Note that $Z_j Z_k = 1$ only when both elements $j$ and $k$ are in the sample, otherwise it equals 0.
$$E[Z_j Z_k] = \frac{\binom{N-2}{n-2}}{\binom{N}{n}} = \frac{n(n-1)}{N(N-1)}$$
$$Cov(Z_j, Z_k) = \frac{n(n-1)}{N(N-1)} - \frac{n^2}{N^2} = -\frac{n(N-n)}{N^2(N-1)} = -\frac{n(1-\frac{n}{N})}{N(N-1)}$$
$\left(1 - \frac{1}{N}\right) \hat{\sigma}^2$ is an unbiased estimator for $\sigma^2$
**100(1-$\alpha$)% C. I. :** if N, n, N-n都足够大那么我们就有$\bar{Y} \pm z_{1-\frac{\alpha}{2}}\sqrt{\frac{N-n}{N-1}}\frac{\sigma}{\sqrt{n}}$, 但是我们一般没有$\sigma^2$, 所以我们要$\frac{N-1}{N}\hat{\sigma}^2$代替$$\Rightarrow \bar{Y} \pm z_{1-\alpha/2}\sqrt{\frac{N-n}{N}}\frac{\hat{\sigma}}{\sqrt{n}}$$ , 考虑我们的其实是样本所以有 $$\bar{y} \pm z_{1-\alpha/2}\sqrt{\frac{N-n}{N}}\frac{s}{\sqrt{n}}$$
但是我们其实应该使用t-distribution  $$\bar{y} \pm t_{n-1,1-\alpha/2}\sqrt{\frac{N-n}{N}}\frac{s}{\sqrt{n}}$$  $${\ = \bar y\ \pm\ t_{n-1,\alpha/2}\ \sqrt{\ \frac{1-\frac{n}{N}}{n}\cdot \frac{1}{n-1}\sum_{i=1}^n\bigl(y_i-\bar y\bigr)^2\ }\ }$$
<font color=purple>**Sample size for $\mu$（目标半宽$d$）**</font>: $$n = 1 \Bigg/ \left(\frac{1}{N} + \frac{d^2}{v^2 t_{n-1,1-\alpha/2}^2}\right)$$其中$v$表示我们对$\sigma$的一些估计/猜测
**Initial approximation**: Start with the z-distribution$:$$$n_0 = 1 \Bigg/ \left(1/N + d^2/(v^2 \cdot z_{1-\alpha/2}^2)\right)$$
**Iteration**: Use the formula recursively: $$n_{i+1} = 1 \Bigg/ \left(1/N + d^2/(v^2 \cdot t_{n_i-1,1-\alpha/2}^2)\right)$$
We choose the first 𝑛 which is larger than the right hand side of the equation

==<font color=purple>**Estimating a total $\tau$**</font>==
Estimator: $\hat{\tau} =N\bar{Y}$
$E(\hat{\tau}) = \tau$
$Var(\hat{\tau}) = \frac{N-n}{N-1}\frac{N^2}{n}\sigma^2$ => $\widehat{Var}(\hat{\tau})= N^2\left(1-\frac{n}{N}\right)\frac{\hat{\sigma}^2}{n}$
C.I.:$\hat{\tau} \pm \sqrt{N^2\frac{\sigma^2}{n}\left(\frac{N-n}{N-1}\right)}z_{1-\frac{\alpha}{2}}$
    =>$\hat{\tau} \pm \sqrt{N^2\left(1-\frac{n}{N}\right)\frac{s^2}{n}}t_{n-1,1-\frac{\alpha}{2}}$
Sample size: $$n = 1 \Bigg/ \left(1/N + \frac{d^2}{N^2\sigma^2z^2_{1-\alpha/2}}\left(1-\frac{1}{N}\right)\right) \Rightarrow n = 1 \Bigg/ \left(1/N + \frac{d^2}{N^2v^2t^2_{n-1,1-\alpha/2}}\right)$$

==<font color=purple>**Estimating a proportion $p$**</font>==
$p = \frac{1}{N} \sum_{j=1}^{N} y_j$. That is, $p$ is a special case where $\hat{p} = \frac{1}{n} \sum_{i=1}^{n} Y_i$, where $Y_i = 1$ if element $i$ has the characteristic and $Y_i = 0$ otherwise
$\Rightarrow Var(\hat{p}) = \frac{N-n}{N-1} \frac{1}{n} p(1-p)$
$\displaystyle \widehat{\mathrm{Var}}(\hat p)=\frac{1-\frac{n}{N}}{n-1}\ \hat p(1-\hat p)$ 
When the $Y_i$ are Bernoulli random variables,  $\hat{\sigma}^2 = \frac{1}{n-1} \sum_{i=1}^{n} (Y_i - \bar{Y})^2 = \frac{n}{n-1} \hat{p}(1-\hat{p})$
$\hat{p} \pm \sqrt{(1-\frac{n}{N}) \frac{1}{n-1} \hat{p}(1-\hat{p})} \cdot t_{n-1,1-\frac{\alpha}{2}}$, Because $\sigma^2 = p(1-p)$ will be unknown. If it is known we would know $p$.
What is large enough, in this case?   We require $n\hat{p} \geq 5$ and $n(1-\hat{p}) \geq 5$
$n = \left(1 \Bigg/ \left(\frac{1}{N}+ \frac{d^2}{p(1-p)z^2_{1-\frac{\alpha}{2}}}\left(1-\frac{1}{N}\right)\right)\right) $
If we don't know p:  For a conservative sample size, use $p = 0.5$. ($p(1-p)$ is maximized at $p = 0.5$)

---

**==Stratified Random Sampling==**
Reduction of estimator variance,Reduction of cost, Comparison among sub-groups, Prevent really bad (unrepresentative) samples

**Notations:**
$L$ = Number of strata
$N_i$ = Population size of stratum $i$
$N$ = Total population size $N = N_1 + N_2 + ... + N_L$
$\bar{Y}_{st}$ = Estimator of population mean from stratified sampling
$n=$ Total sample size
$n_i$ = Sample size for stratum $i$
$a_i$ = percentage for stratum $i$ in the sample size 
A subscript of $i$ will mean that the parameter/estimator concerned is from stratum $i$.  E.g. $\bar{Y}_i$, $\mu_i$, $s_i^2$, $\tau_i$ etc.

==<font color=black>**Estimating total $\hat \tau = \sum_{i=1}^{L} N_i\bar{Y}_i$**</font>==
$Var(\hat{\tau}_{st}) = Var\left(\sum_{i=1}^{L} N_i\bar{Y}_i\right) = \sum_{i=1}^{L} Var(N_i\bar{Y}_i)= \sum_{i=1}^{L} N_i^2 \frac{\sigma_i^2}{n_i}\frac{N_i-n_i}{N_i-1}$
$$\widehat{Var}(\hat{\tau}_{st}) = \sum_{i=1}^{L} N_i^2 \frac{1}{n_i} \frac{N_i-n_i}{N_i-1} \left(1 - \frac{1}{N_i}\right) \hat\sigma_i^2$$$$= \sum_{i=1}^{L} N_i^2 \left(1 - \frac{n_i}{N_i}\right) \frac{\hat\sigma_i^2}{n_i}$$
**C. I.** $$\hat{\tau}_{st} \pm t_{df,1-\frac{\alpha}{2}}\sqrt{\widehat {Var}(\hat{\tau}_{st})}$$
Intuitively, we might guess $df = df_1 + df_2 + ... + df_L$ where $df_k = n_k - 1$, the degrees of freedom from the SRS in stratum $k$. However, this is correct **only if** the variances of all the strata are the same
**$\Rightarrow$Satterthwaite's Approximation provides a solution:**
$df_{\chi'} \approx \left(\sum_{i=1}^{n} k_i\hat{\sigma}_i^2\right)^2 \Bigg/ \sum_{i=1}^{n} \frac{(k_i\hat{\sigma}_i^2)^2}{n_i-1}$, where $\hat{\sigma}_i^2$ has sample size $n_i$.
$df \approx \left(\sum_{h=1}^{L} k_h s_h^2\right)^2 \Bigg/ \sum_{h=1}^{L} \frac{(k_h s_h^2)^2}{n_h-1}$, where $k_h = \frac{N_h(N_h-n_h)}{n_h}$, $${s_h}^2 =\frac{n_h}{n_h-1} \hat{p}_h(1-\hat{p}_h)$$
If the strata sample sizes are **at least 30**, we can avoid calculating $df$ by using the normal distribution instead: $$\hat{\tau}_{st} \pm z_{1-\frac{\alpha}{2}}\sqrt{Var(\hat{\tau}_{st})}$$
<font color=purple>**Sample size for $\tau$（目标半宽$d$）**</font>: $$n = \left(\sum_{i=1}^{L} N_i^3 \cdot \frac{1}{a_i} \cdot \frac{\sigma_i^2}{N_i-1}\right) \Bigg/ \left(d^2/z_{1-\frac{\alpha}{2}}^2 + \sum_{i=1}^{L} N_i^2 \cdot \frac{\sigma_i^2}{N_i-1}\right)$$

**==Estimating the population mean $\mu$==**
$\hat \mu = \bar{Y}_{st} = \frac{\hat \tau_{st}}{N} = \frac{1}{N}\sum_{i=1}^LN_i\bar Y_i$
$Var(\bar{Y}_{st}) = \frac{1}{N^2}\sum^L_{i=1}N^2_i\frac{\sigma^2_i}{n_i}\left(\frac{N_i-n_i}{N_i-1}\right)$
$ \widehat{Var}(\bar{Y}) = \frac{1}{N^2}\sum^L_{i=1}N^2_i\left(1-\frac{n_i}{N_i}\right)\frac{\hat{\sigma}^2_i}{n_i}$
If each strata bigger than 30 $$\bar{y}_{st} \pm z_{1-\frac{\alpha}{2}}\sqrt{\widehat{Var}(\bar{y}_{st})}$$
Otherwise  $$\bar{y}_{st} \pm t_{df,1-\frac{\alpha}{2}}\sqrt{\widehat{Var}(\bar{y}_{st})}$$
where $df \approx \left(\sum_{h=1}^{L} k_h s_h^2\right)^2 \Bigg/ \sum_{h=1}^{L} \frac{(k_h s_h^2)^2}{n_h-1}$,  $k_h = \frac{N_h(N_h-n_h)}{N^2n_h}$, $${s_h}^2 =\frac{n_h}{n_h-1} \hat{p}_h(1-\hat{p}_h)$$
<font color=purple>**Sample size for $\mu$（目标半宽$d$）**</font>: 
$$n = \left(\sum_{i=1}^{L} (N_i^3/a_i) \cdot \sigma_i^2/(N_i-1)\right) \Bigg/ \left(N^2d^2/z_{1-\alpha/2}^2 + \sum_{i=1}^{L} N_i^2 \cdot \sigma_i^2/(N_i-1)\right)$$

==**Estimating the population proportion $p$**==
$$\hat{p}_{st} = \frac{1}{N} \sum_{i=1}^{L} N_i\hat{p}_i$$
$$Var(\hat{p}_{st}) = \frac{1}{N^2} \sum_{i=1}^{L} N_i^2 Var(\hat{p}_i)$$ $$= \frac{1}{N^2} \sum_{i=1}^{L} N_i^2 \cdot \frac{N_i-n_i}{N_i-1} \cdot \frac{p_i(1-p_i)}{n_i}$$
$$\widehat{Var}(\hat{p}_{st}) = \frac{1}{N^2} \sum_{i=1}^{L} N_i^2 \cdot {(1-\frac{n_i}{N_i}) }\cdot \frac{\hat{p}_i(1-\hat{p}_i)}{n_i-1}$$
If each strata bigger than 30 $$\hat{p}_{st} \pm z_{1-\alpha/2} \sqrt{\hat{Var}(\hat{p}_{st})}$$
Otherwise $$\hat{p}_{st} \pm t_{df,1-\alpha/2} \sqrt{\hat{Var}(\hat{p}_{st})}$$,  $$df \approx (\sum_{h=1}^{L} k_h s_h^2)^2 \Bigg/ \sum_{h=1}^{L} \frac{(k_h s_h^2)^2}{n_h-1}$$, Where: $k_h = \frac{N_h(N_h-n_h)}{{N}^2n_h}$ 
<font color=purple>**Sample size for $p$（目标半宽$d$）:**</font>
Originally: $n = \left(\sum_{i=1}^{L} N_i^3 \cdot \frac{1}{a_i} \cdot \frac{p_i(1-p_i)}{N_i-1}\right) \Bigg/ \left(\frac{N^2d^2}{z^2_{1-\frac{\alpha}{2}}} + \sum_{i=1}^{L} N_i^2 \cdot \frac{p_i(1-p_i)}{N_i-1}\right)$ 如果不知道$p_i$假设等于0.5, 以下一些化简形式: 
Assume $\frac{N_i}{N_i-1} \approx 1$ , the formula becomes:$$n = \left(\sum_{i=1}^{L} N_i^2 \cdot \frac{1}{a_i} \cdot p_i(1-p_i)\right) \Bigg/ \left(N^2d^2/z_{1-\alpha/2}^2 + \sum_{i=1}^{L} N_i \cdot p_i(1-p_i)\right)$$
$p_i = 0.5$ for all strata, we get: $$n = \left(\sum_{i=1}^{L} N_i^2 \cdot \frac{1}{a_i}\right) \Bigg/ \left(4N^2d^2/z_{1-\alpha/2}^2 + N\right)$$
With proportional allocation ($a_i = \frac{N_i}{N}$): $$n = \frac{N^2}{4N^2d^2/z_{1-\alpha/2}^2 + N}$$
For a 95% C. I. , $z_{1-\alpha/2}^2 = z_{0.975}^2 \approx 1.96^2 \approx 3.84$, giving: $$n = \frac{N}{1.04d^2N + 1}$$
When $N$ is very large, the formula further simplifies to: $$n = \frac{1}{1.04d^2}$$

==**Sample Allocation**==
最佳的分配方案$n_1,n_2,...,n_L$应该受以下几个方面的影响
<font color=black>1. </font>The relative size of each stratum in the population affects how much information we gain from sampling(同样的20个里面取10个和2000个取10个不一样)
<font color=black>2. </font>The variability of observations within each stratum (measured by $\sigma_i$) significantly impacts required sample sizes (层内方差越大取的越多)
<font color=black>3. </font>The cost of obtaining observations may differ substantially between strata(不同层的花销不一样)
<font color=red>**Naive: **</font>$n_i = nN_i/N$ $\Rightarrow $ it does not consider the  variability within each stratum
<font color=red>**Neyman Allocation**:</font> $n_h = n \cdot {N_h \sigma_h}/{\sum_{i=1}^L N_i \sigma_i}$
The proportional allocation formula is: $n_i = \frac{n \cdot N_i}{N}$
$a_1 = \frac{N_1}{N}, a_2 = \frac{N_2}{N}, \ldots, a_L = \frac{N_L}{N}$
We choose the $a_i$ that minimize the variance of our estimator, $Var(\bar{Y}_{st})$
<font color=black>1. </font>Minimize: $\frac{1}{N^2} \sum_{i=1}^{L} N_i^2 \frac{\sigma_i^2}{n_i} \frac{N_i-n_i}{N_i-1}$
<font color=black>2. </font>over all $n_1$,$n_2$,…,$n_L$
<font color=black>3. </font>Subject to: $\sum_{i=1}^{L} n_i = n$
use Lagrange Multipliers: 
$L(n_1,...,n_L,\lambda) = \frac{1}{N^2} \sum_{i=1}^{L} N_i^2 \frac{\sigma_i^2}{n_i} \frac{N_i-n_i}{N_i-1} - \lambda\left(n - \sum_{i=1}^{L} n_i\right)$
Taking the partial derivative with respect to $n_i$:
$\frac{\partial L}{\partial n_i} = \frac{1}{N^2} \frac{\partial}{\partial n_i}\left[N_i^2 \frac{\sigma_i^2}{n_i} \frac{N_i-n_i}{N_i-1}\right] + \lambda$
$\frac{\partial L}{\partial \lambda} = \sum_{i=1}^{L} n_i - n = 0$
$\Rightarrow$ $$n_i = n \cdot \left(\sqrt{N_i/(N_i-1)} \cdot N_i \cdot \sigma_i\right) \Bigg/ \left(\sum_{j=1}^{L} \sqrt{N_j/(N_j-1)} \cdot N_j \cdot \sigma_j\right)$$

如果我们考虑每个stratum的cost不一样以及考虑总的cost
Choose the $n_i$ that minimize $Var(\bar{Y}_{st})$
subject to the constraint that ${c_0 + c_1n_1 + c_2n_2 +...+c_Ln_L = c}$
$\Rightarrow n_i = \left((c-c_0) \cdot \sqrt{N_i/(N_i-1)} \cdot N_i \cdot \sigma_i/\sqrt{c_i}\right) \Bigg/ \left(\sum_{j=1}^{L} \sqrt{N_j/(N_j-1)} \cdot N_j \cdot \sigma_j \cdot \sqrt{c_j}\right)$

当各层均值差异小而方差差异大的时候，按层抽样不起作用。
Stratifying will not necessarily result in a smaller  variance
If your reason for stratifying is to have a smaller  error of estimation, choose strata whose  observations within are likely to be homogeneous

---

**==Cluster Sampling==**: A cluster sample is a probability sample in which each sampling unit is a collection, or cluster, of elements (to keep the cost of survey down)

We sample from all the strata, but only some of the  clusters  – We take measurements from only some elements in  the stratum (we perform a simple random sample in  each stratum) but we measure every element in the  cluster 

The difference between strata should be large and the differences within small. The differences within each cluster should reflect the whole population, but the differences between should be small.

**$N$**: The total number of clusters in the population.
**$n$**: The number of clusters selected in the sample.
**$M_i$**: The number of elements in cluster $i$.
**$M$**: The population size, i.e. $M \;=\; \sum_{i=1}^N M_i.$
**$m_i$**: The sample size in the $i$-th cluster.
**$\bar M$**: The average cluster size in the population, $\bar M \;=\;\frac{M}{N}.$
**$Y_{ij}$**: The $j$-th observation from the $i$-th cluster.
**$Y_i$**: The total of observations in the $i$-th cluster, $Y_i \;=\;\sum_{j=1}^{M_i} Y_{ij}.$
==**Estimating $\tau$**==
The population total is $\tau = \sum_{i=1}^{N} \sum_{j=1}^{M_i} y_{ij} = \sum_{i=1}^{N} y_i $
<font color=red>**Estimator**</font> $ \hat\tau = N \,\frac{1}{n}\sum_{i=1}^{n}Y_i = N\bar Y $
Let $\mu_c$ be the average total for a cluster, that is: $ \mu_c = \frac{1}{N}\sum_{i=1}^{N}Y_i $
<font colore=blue>$\hat\tau$ is unbiased.</font>
$ \mathrm{Var}(\hat\tau) = N^2\,\mathrm{Var}(\bar Y) = N^2\,\frac{N - n}{N - 1}\,\frac{1}{n}\,\sigma_c^2 $ , where $\sigma_c^2$ is the variance of the cluster totals.
$ \widehat{\mathrm{Var}}(\hat\tau) = N^2\Bigl(1 - \frac{n}{N}\Bigr)\,\frac{\hat\sigma_c^2}{n} $, where $\hat\sigma_c^2$ is the sample variance of the cluster totals.
$100(1−\alpha)%$ 的C. I.  $\Rightarrow \ \hat\tau \pm t_{n-1,\,1-\alpha/2}\sqrt{\widehat{\mathrm{Var}}(\hat\tau)}$
==**簇数的样本量估算**== We may find an appropriate number of clusters to sample to achieve a 100(1−α)% C.I. of width $2d$ by solving  $d = z_{1-\alpha/2}\,\sqrt{\mathrm{Var}(\hat\tau)}$ for $n$.  
Note: this will depend on $\sigma_c^2$, which is almost certainly unknown.  Plug in a reasonable guess for $\sigma_c^2$ to obtain a number.
==**Two stage cluster sampling**==
<font color="red">**Advantages**</font> 1. More practical when a complete sampling frame is unavailable 2. Reduces costs when sampled elements are geographically dispersed

Implementation Process
**Large clusters:** Tend to be heterogeneous $\Rightarrow$ Require larger samples within each cluster $\Rightarrow$ Can use fewer clusters overall
**Small clusters:** Tend to be homogeneous $\Rightarrow$ Require smaller samples within each cluster $\Rightarrow$ Need more clusters to achieve precision

**Notion:** 与之前一样除了
$m_i$ = number of elements selected from the $i$-th cluster by SRS  
$Y_{ij}$ = the $j$-th observation in the sample from cluster $i$
Hence, the sample mean for cluster $i$ is  $\bar Y_i = \frac{1}{m_i}\sum_{j=1}^{m_i}Y_{ij}.$ (在整群分类中是$$n_i$$)

A SRS unbiased estimator for the total of cluster $i$ is $\hat Y_i = M_i\,\frac{1}{m_i}\sum_{j=1}^{m_i}Y_{ij}.$
Therefore, an unbiased estimator of the population total $\tau = \sum_{i=1}^N Y_i$  is  $\hat\tau = N\,\frac{1}{n}\sum_{i=1}^n\hat Y_i.$

**Estimating**
对于一个two-stage我们要通过两个指标来看一个Estimator到底是好还是不好
Conditional expectations  和 Conditional variances
Let $ \hat\theta $ be an estimator based on a two‐stage sample, $ s_1 $ be the (random) set of primary sampling units selected in the first stage.
Then by the <font color=red>**Conditional expectations**</font>, $E\bigl[E(\hat\theta \mid s_1)\bigr] \;=\; E(\hat\theta)\,.$
And by the <font color=red>**Conditional variances**</font>, $\mathrm{Var}(\hat\theta)
\;=\;
\mathrm{Var}\bigl(E[\hat\theta \mid s_1]\bigr)
\;+\;
E\bigl[\mathrm{Var}(\hat\theta \mid s_1)\bigr].
$

[$$\mathrm{Var}(X|Y=y) = E[(X - E[X|Y=y])^2|Y=y]$$]

<font color=blue>**Example of** $\tau$</font>
For our estimator $\hat\tau$
<font color=black>1. $E[\hat\tau|s_1] = N\frac{1}{n}\sum_{i=1}^n E[\hat{y}_i|s_1]$</font>. Since the $\hat{y}_i$ are SRS estimators of the cluster totals $y_i$, $E[\hat{y}_i|s_1] = Y_i$ $\Rightarrow E[\hat\tau|s_1] = N\frac{1}{n}\sum_{i=1}^n Y_i$
<font color=black>2. </font>Hence $E[\hat\tau] = E[E[\hat\tau|s_1]] = E\left[N\frac{1}{n}\sum_{i=1}^n Y_i\right] = NE[\bar{Y}]$ $\Rightarrow E[\hat\tau] = \tau$, so our estimator is unbiased.

<font color=red>$Var(\hat\tau) = N^2\frac{N-n}{N-1}\frac{\sigma_c^2}{n} + \frac{N}{n}\sum_{i=1}^N M_i^2\frac{M_i-m_i}{M_i-1}\frac{\sigma_i^2}{m_i}$</font>, where $\sigma_c^2$ is the population variance of the cluster totals, i.e. the $y_i$s and $\sigma_i^2$ is the population variance within the $i$-th cluster
<font color=red>$\widehat{Var}(\hat\tau) = N(N-n)\frac{1}{n}\hat{\sigma}_c^2 + \frac{N}{n}\sum_{i=1}^n M_i(M_i-m_i)\frac{1}{m_i}\hat{\sigma}_i^2$</font>, where $\hat{\sigma}_c^2$ is the sample variance of the estimated cluster totals (the $\hat{Y}_i$) and $\hat{\sigma}_i^2$ is the sample variance inside cluster $i$
Thus the $100(1-\alpha)%$ C.I. for $\tau$ will be $\hat \tau \pm Z_{1-\alpha/2} \sqrt{\widehat{Var}(\hat\tau)}$

<font color=blue>**Estimating Population Proportion $p$**</font>
$\hat{p} = \frac{N}{M}\frac{1}{n}\sum_{i=1}^n \hat{Y}_i$, where $\hat{Y}_i$ is the estimator for the number of people in cluster with the characteristic
We may write $\hat{Y}_i = M_i\hat{p}_i$ to relate $p$ to the sample proportions inside the clusters
**Unbiased estimator for the variance** is <font color="red">$\widehat{Var}(\hat{p}) = \frac{1}{M^2}N(N-n)\frac{1}{n}\hat{\sigma}_c^2 + \frac{1}{M^2}\frac{N}{n}\sum_{i=1}^n M_i(M_i-m_i)\frac{1}{m_i}\hat{\sigma}_i^2$</font>
Recall: $\hat{\sigma}_i^2$ is the estimator for population variance of cluster $i$, hence $\hat{\sigma}_i^2 = \frac{m_i}{m_i-1}\hat{p}_i(1-\hat{p}_i)$
$\hat{\sigma}_c^2$ is the sample variance of the estimated cluster totals, hence <font color="red">$\hat{\sigma}_c^2 = \frac{1}{n-1}\sum_{i=1}^n \left(M_i\hat{p}_i - \frac{M}{N}\hat{p}\right)^2$</font>

**Assumption**: officially we need: n, N, N-n shall be large, but if $$Y_i$$ can be assumed as i.i.d normal, we can use CI formula.
officially we need: n, N, N-n shall be large (which is satisfied), $$Y_i$$ shall be roughly i.i.d normal (which is not satisfied since $$Y_i$$ is either 2 or -1). But since n/N/N-n are large, sample variance is a good estimate of population variance, so using z quantile under the large n/N/N-n condition is approximately ok.
