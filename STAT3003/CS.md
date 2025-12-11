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
<font color=black>1. </font>The relative size of each stratum in the population affects how much information we gain from sampling(同样的20个里面取10个和2000个取10个不一样)
<font color=black>2. </font>The variability of observations within each stratum (measured by $\sigma_i$) significantly impacts required sample sizes (层内方差越大取的越多)
<font color=black>3. </font>The cost of obtaining observations may differ substantially between strata(不同层的花销不一样)
<font color=red>**Naive: **</font>$n_i = nN_i/N$ $\Rightarrow $ it does not consider the  variability within each stratum
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

**Assumption**: 
officially we need: n, N, N-n shall be large, but if $$Y_i$$ can be assumed as i.i.d normal, we can use CI formula.
officially we need: n, N, N-n shall be large (which is satisfied), $$Y_i$$ shall be roughly i.i.d normal (which is not satisfied since $$Y_i$$ is either 2 or -1). But since n/N/N-n are large, sample variance is a good estimate of population variance, so using z quantile under the large n/N/N-n condition is approximately ok.
**Quota Sampling**
Disadvantage: 1. Instructions leave room for human subjectivity when objectivity is needed 2. Interviewers may seek "nicer" people (e.g., richer), creating bias 3. Impossible to control all factors influencing preferences 4. Fixing one demographic ratio might disturb others 5.Unlike randomization, cannot balance unknown factors in the population

---

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
Population:  $\hat{\tau}_{sys} = NY_1 = kY_1$    $Var(\hat\tau) = N^2\sigma^2_c$    $\widehat{Var}(\hat \tau) =N^2(1-n/N)\hat \sigma_c^2/n$    $\hat \sigma_c^2$ can't be calculate  $\Rightarrow$ Regard it as SRS.
<font color=red>Assumption: </font>the secondary units are in random order
$Var(\hat{\tau}_{\text{sys}}) \approx \frac{M - M_1}{M_1}  \frac{M^2}{M - 1}  \sigma^2$   $\hat{Var}(\hat{\tau}_{\text{sys}}) \approx M^2 \left(1 - \frac{M_1}{M} \right)  \frac{1}{M_1}  \hat{\sigma}^2= \frac{M^2}{M_1} \left(1 - \frac{M_1}{M} \right)  \frac{1}{M_1 - 1} \sum_{j=1}^{M_1} \left(Y_{1j} - \bar{Y}_1 \right)^2$
半宽d估计:  $$M_1 \ge M\Big/(1 + (M-1) \frac{d^2}{z^2 M^2 \sigma^2})$$
Mean: $\hat{\mu}_{\text{sys}} = \bar{Y}_{\text{sys}} = \bar{Y}_1 = \frac{1}{M_1} \sum_{j=1}^{M_1} Y_{1j}$     $\hat{\tau}_{\text{sys}} = M \, \hat{\mu}_{\text{sys}}$  $\hat Var(\hat\mu_{sys}) = \hat{Var}(\hat{\tau}_{\text{sys}})/M^2$    $\hat{\mu}_{\text{sys}} \pm t_{\alpha/2,\,M_1-1} \,
\sqrt{\hat{V}ar(\hat{\mu}_{\text{sys}})}$
半宽d估计: $$z_{1-\alpha/2} \sqrt{Var(\hat{\mu})} \le d$$ 其中$$Var(\hat{\mu}) = \frac{M - M_1}{M - 1} \cdot \frac{\sigma^2}{M_1}$$  所以我们有$$M_1 \ge {M}\Big / ({1 + (M - 1)\frac{d^2}{\sigma^2 z^2}})$$

<font color="navy">**4. Cluster Variance, ICC, and the Guiding Principle**</font>
**Intraclass Correlation Coefficient** 
Based on equal cluster size $\bar{M}$, the intraclass correlation coefficient is  $ICC = 
\left(
\sum_{i=1}^{N}\sum_{j=1}^{\bar{M}}\sum_{k\ne j}(Y_{ij}-\mu)(Y_{ik}-\mu)
\right)
\Big/
\left(
N\bar{M}(\bar{M}-1)\sigma^2
\right)$
It measures the correlation between pairs of elements within the same cluster.
Assume all clusters have the same size $\bar{M} = \frac{1}{N}\sum_{i=1}^N M_i$.  
Relationship between cluster-level variance and element-level variance:  $\sigma_c^2 = \bar{M}\sigma^2 \bigl(1 + (\bar{M}-1)ICC\bigr)$ 

If we select multiple clusters, the variance depends on $ICC$: 
• If $ICC \approx 0$: design behaves like SRS. goodestimate
• If $ICC > 0$: variance is inflated (homogeneous clusters). underestimate
• If $ICC < 0$: variance is reduced (heterogeneous clusters).  overestimate

<font color="navy">**Guiding principle for variance reduction**</font>  
• To obtain estimators with low variance, clusters should be internally heterogeneous (high within-cluster variance) and similar to each other (low between-cluster variance).  
• Cluster sampling often violates this: grouping neighbors (e.g. geographic blocks) usually creates homogeneous clusters (high $ICC$), leading to higher variance.  
• Systematic sampling often follows this: because sample points are spaced apart by $k$, elements within the systematic sample are usually diverse (heterogeneous), leading to low or negative $ICC$ and lower variance.

<font color="navy">**5. Effect of Population Ordering on Systematic Sampling**</font>
The sign and magnitude of $ICC$ depend on how the frame is ordered.
<font color="navy">7.1 Random ordering</font>  
• Ordering is independent of $y_i$.  • $ICC \approx 0$.  
• Result: SRS variance formulas are accurate:  $\widehat{\operatorname{Var}}(\bar{y}_{sys}) \approx \widehat{\operatorname{Var}}(\bar{y}_{SRS})$
<font color="navy">7.2 Monotone trend (increasing/decreasing)</font>  
• Values $y_i$ show a smooth trend. Systematic sampling spreads sample points across the range.  
• $ICC < 0$.   • Result: true variance is smaller than SRS approximation: $\operatorname{Var}(\bar{y}_{sys}) < \operatorname{Var}(\bar{y}_{SRS})$
• Implication: SRS formulas overestimate variance (conservative / safe).
<font color="navy">7.3 Periodic pattern</font>  
• Values repeat in a cycle with period $P$.  
• If $k \approx P$ (or a multiple), all selected elements may come from the same phase (e.g. all peaks).  
• $ICC > 0$ (strongly positive).  Result: true variance is much larger than SRS approximation:  $\operatorname{Var}(\bar{y}_{sys}) \gg \operatorname{Var}(\bar{y}_{SRS})$
• Implication: SRS formulas underestimate variance (dangerous / misleading).

<font color="navy">**6. Repeated Systematic Sampling**</font>
Repeated systematic sampling is used to estimate variance directly when the **random-order assumption** is unsafe.
<font color="navy">6.1 Design idea</font>  
• Instead of one large 1-in-$k$ sample, take $n_s$ separate systematic samples.  
• New interval: $k' = n_s  k$.  
• Select $n_s$ random starts $r_1, \dots, r_{n_s}$ from $\{1, \dots, k'\}$.  
• This creates $n_s$ clusters (repeated systematic samples), allowing us to compute a variance.
<font color="navy">6.2 Estimator and variance (cluster formulas)</font>  
$\hat{\tau} = N \dfrac{1}{n_s}\sum_{i=1}^{n_s} Y_i$    $Var(\hat{\tau}) = N \dfrac{N-n_s}{N-1}\sigma_c^2$   $\widehat{Var}(\hat{\tau}) = N(N-n_s)\dfrac{1}{n_s}\hat{\sigma}_c^2$
**Assumption:** the distribution of the cluster totals (the systematic sample totals) follows a Normal distribution, or that the Central Limit Theorem applies to the mean of the 10 cluster totals.

---

==<font color="navy">**Auxiliary Data**</font>==

**1. Using Auxiliary Data & Ratio Estimation (SRS)**

**Notation (SRS & ratio)**
 $N$ pop. size; $n$ SRS size; $Y_i,X_i$ values for unit $i$;
 $\tau_y=\sum_{i=1}^N Y_i$; $\tau_x=\sum_{i=1}^N X_i$; $\mu_y=\tau_y/N$; $\mu_x=\tau_x/N$; $\bar{Y}=\frac1n\sum Y_i$; 
$\bar{X}=\frac1n\sum X_i$; $R=\tau_y/\tau_x=\mu_y/\mu_x$; $\hat{R}=\bar{Y}/\bar{X}$; 
$\sigma_y^2,\sigma_x^2,\sigma_{xy}$ population var/cov; $\hat{\sigma}_y^2=\frac{1}{n-1}\sum(Y_i-\bar{Y})^2$; $\hat{\sigma}_x^2=\frac{1}{n-1}\sum(X_i-\bar{X})^2$;
$Z_i=Y_i-RX_i$; $\sigma_r^2=\frac1N\sum(Y_i-RX_i)^2$;  $\hat{c}_{v,x}=\hat{\sigma}_x/\bar{X}$; $\hat{c}_{v,y}=\hat{\sigma}_y/\bar{Y}$;
Auxiliary $X$ is easy/cheap and strongly related to $Y$; assume $Y_i\approx RX_i$ (through origin).

**1.1 Ratio estimators**
 Population ratio: $R=\tau_y/\tau_x=\mu_y/\mu_x$. Sample ratio: $\hat{R}=\bar{Y}/\bar{X}$.
 ==Total==: $\hat{\tau}_r=\hat{R}\tau_x=(\bar{Y}/\bar{X})\tau_x$.    ==Mean==: $\hat{\mu}_r=\hat{R}\mu_x=(\bar{Y}/\bar{X})\mu_x$.
 Biased exists but small for large $n$(大SRS样本), so MSE $\approx$ variance.
Biased of $\hat R = E[\hat R]-R = -Cov(\hat R, \bar X)/\mu_x$ $Cov(X,Y)^2<=Var(X)Var(Y)$ 所以$|Bias|/\sqrt{Var(\hat R)}<=\sqrt{Var(\bar X)}/\mu_x$
根据泰勒展开$\hat{R} \approx \frac{\mu_y}{\mu_x} - \frac{\mu_y}{\mu_x^2}(\bar{X} - \mu_x) + \frac{1}{\mu_x}(\bar{Y} - \mu_y)$  所以$\text{Var}(\hat{R}) \approx MSE(\hat{R}) \approx \frac{1}{\mu_x^2}\text{Var}(\bar{Y} - R\bar{X})$

**1.2 Variance approximations**
Define $Z_i=Y_i-RX_i$, $\sigma_r^2=\frac1N\sum(Y_i-RX_i)^2$, $\hat{\sigma}_r^2=\frac{1}{n-1}\sum(Y_i-\hat{R}X_i)^2 =\hat{\sigma}_y^2+\hat{R}^2\hat{\sigma}_x^2-2\hat{R}\hat{\sigma}_{xy}$.
Estimator: $\operatorname{Var}(\hat{\mu}_r)\approx\frac{N-n}{N-1}\frac{1}{n}\sigma_r^2$;  $\widehat{\operatorname{Var}}(\hat{\mu}_r)=\Big(1-\frac{n}{N}\Big)\frac{1}{n}\hat{\sigma}_r^2$.
Total: $\operatorname{Var}(\hat{\tau}_r)\approx\frac{N-n}{N-1}\frac{N^2}{n}\sigma_r^2$;   $\widehat{\operatorname{Var}}(\hat{\tau}_r)=\frac{N-n}{N}\frac{N^2}{n}\hat{\sigma}_r^2$.
Ratio $R$: $\operatorname{Var}(\hat{R})\approx\frac{1}{\mu_x^2}\frac{N-n}{N-1}\frac{1}{n}\sigma_r^2$;  $\widehat{\operatorname{Var}}(\hat{R})=\frac{1}{\mu_x^2}\Big(1-\frac{n}{N}\Big)\frac{1}{n}\hat{\sigma}_r^2$.

**1.3 When is ratio better than SRS?**
 <font color=red>SRS mean</font>: $\bar{Y}$, $\widehat{\operatorname{Var}}(\bar{Y})=\Big(1-\frac{n}{N}\Big){\hat{\sigma}_y^2}/{n}$.  <font color=red>Ratio mean</font>: $\hat{\mu}_r$, $\widehat{\operatorname{Var}}(\hat{\mu}_r)=\Big(1-\frac{n}{N}\Big){\hat{\sigma}_r^2}/{n}$.
Key identity: $\hat{\sigma}_r^2=\hat{\sigma}_y^2+\hat{R}^2\hat{\sigma}_x^2-2\hat{R}\hat{\rho}\hat{\sigma}_x\hat{\sigma}_y$.   $\hat{\rho}=\hat{\sigma}_{xy}/(\hat{\sigma}_x\hat{\sigma}_y)$ $\hat{c}_{v, x}=\hat{\sigma}_x/\bar{X}$
Ratio better if $\hat{\rho}\gg\frac12{\hat{cv}_x}/{(\hat{cv}_y)}$  then ==$\hat{\sigma}_r^2\ll\hat{\sigma}_y^2$==. 
Also if $\hat{c}_{v, x}\approx\hat{c}_{v,y}$, “$\hat{\rho}>0.5$ usually enough to say Ratio better”.

**1.4 CI & sample size **
CI: $\text{Point Estimator}\pm t_{n-1,1-\alpha/2}\sqrt{\widehat{\operatorname{Var}}(E)}$.
Planning (approx): $d=z_{1-\alpha/2}\sqrt{\operatorname{Var}(E)}$ with assumed $\sigma_r^2$, or iteratively solve $d=t_{n-1,1-\alpha/2}\sqrt{\widehat{\operatorname{Var}}(E)}$ for $n$.

**2. Ratio Estimation in Cluster Sampling**

**Notation (clusters)**
 $N$ #clusters; $M_i$ cluster size; $M=\sum_{j=1}^N M_j$ total elements; $Y_i$ total $Y$ in cluster $i$; $\bar{Y}_i$ sample mean in cluster $i$ (if 2-stage); $\hat{Y}_i=M_i\bar{Y}_i$  est cluster total; $A_i$ count with a characteristic in cluster $i$; $p$ pop proportion; $\hat{p}_i$ cluster sample proportion.
相关性系数$\hat \rho_{XY} = \frac{\text{Cov}(X, Y)}{\sqrt{\text{Var}(X) \text{Var}(Y)}}$

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

**3. Ratio Estimation in Two-stage Cluster Sampling**

**Notation (two-stage)**
 $N$ clusters; cluster $i$ has $M_i$ elements, $M=\sum_{i=1}^N M_i$; stage 1: SRS of $n$ clusters; stage 2 in cluster $i$: SRS of $m_i$ elements; $Y_{ij}$ value for element $j$ in cluster $i$; $\bar{Y}_i$ sample mean in cluster $i$; $\hat{Y}_i=M_i\bar{Y}_i$; for proportions: $\hat{p}_i$ within-cluster prop. Within-cluster var: $\hat{\sigma}_i^2=\frac{1}{m_i-1}\sum(Y_{ij}-\bar{Y}_i)^2$ (or $\hat{\sigma}_i^2=\frac{m_i}{m_i-1}\hat{p}_i(1-\hat{p}_i)$ for binary).

**3.1 Two-stage: mean $\mu_y$**
 Ratio est: $\hat{\mu}_r=\dfrac{\sum_{i=1}^n M_i\bar{Y}_i}{\sum_{i=1}^n M_i}=\dfrac{\sum_{i=1}^n \hat{Y}_i}{\sum_{i=1}^n M_i}$.
 Between-cluster var est: $\hat{\sigma}_r^2=\dfrac{1}{n-1}\sum(\hat{Y}_i-\hat{\mu}_rM_i)^2$.
$\widehat{\operatorname{Var}}(\hat{\mu}_r)=\dfrac{1}{M^2}{N(N-n)\dfrac{1}{n}\hat{\sigma}_r^2+\frac1{M^2}\dfrac{N}{n}\sum_{i=1}^n M_i(M_i-m_i)\dfrac{1}{m_i}\hat{\sigma}_i^2}$.

**3.2 Two-stage: total $\tau_y$ and proportion $p$**
 Total: $\hat{\tau}_r=M\dfrac{\sum\hat{Y}_i}{\sum M_i}$,   $\hat{\sigma}_r^2=\dfrac{1}{n-1}\sum(\hat{Y}_i-\hat{\mu}_rM_i)^2$.	
$$
\widehat{\operatorname{Var}}(\hat{\tau}_r)=N(N-n)\dfrac{1}{n}\hat{\sigma}_r^2+\dfrac{N}{n}\sum_{i=1}^n M_i(M_i-m_i)\dfrac{1}{m_i}\hat{\sigma}_i^2
$$
 Proportion: $\hat{p}_r=\dfrac{\sum M_i\hat{p}_i}{\sum M_i}$.     $\hat{\sigma}_r^2=\dfrac{1}{n-1}\sum(M_i\hat{p}_i-\hat{p}_rM_i)^2$, $\hat{\sigma}_i^2=\dfrac{m_i}{m_i-1}\hat{p}_i(1-\hat{p}_i)$.
$$
\widehat{\operatorname{Var}}(\hat{p}_r)=\dfrac{N(N-n)}{nM^2}\hat{\sigma}_r^2+\dfrac{N}{nM^2}\sum_{i=1}^n M_i(M_i-m_i)\dfrac{1}{m_i}\hat{\sigma}_i^2
$$
**4. Regression Estimation (SRS)**

**Notation (regression)**
known aux: $\mu_x,\tau_x$; $N,n,\hat{\rho}$ as before.
Regression = generalization of ratio (allows non-zero intercept). Use when $(X,Y)$ approx linear but not through origin.

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

==**Lecture 7: Beyond Formulas**==

<font color="navy">**Notation**</font>
• $N$: Population size
• $n$: Sample size
• $\tau$: Population total
• $\mu$: Population mean
• $k$: Sampling interval (in systematic context) or scale length (in Likert context)

<font color="navy">**调查误差主要分为两类：非观测误差 (Errors of Non-observation) 和 观测误差 (Errors of Observation)。**</font>
<font color="navy">**1.1 Errors of Non-observation**</font>
这类误差源于我们未能观测到总体中的某些部分。
• Sampling Error: The difference between our estimate and the true parameter value due to the sampling. (Can be reduced by appropriate sample design and increasing sample size $n$).
• Error of Coverage: Occurs when the sampling frame does not contain every sampling unit in the population (e.g., outdated lists, unlisted numbers).
• Non-response: The most serious non-observation error. It happens in three ways:
<font color="navy">1.</font> Inability to contact: The sample element cannot be reached (e.g., not at home).
<font color="navy">2.</font> Inability to answer: The respondent lacks the knowledge or opinion to answer.
<font color="navy">3.</font> Refusal to answer: The respondent deliberately declines to participate.
<font color="navy">**1.2 Errors of Observation**</font>
这类误差发生在已经联系上受访者并进行观测的过程中，由以下四个因素引起：
• Error due to the interviewer: Interviewers may influence responses through intonation, emphasis, or by creating a sense of confrontation.
• Error due to the respondent:
<font color="navy">a)</font> Recall bias: Respondent recalls information incorrectly.
<font color="navy">b)</font> Prestige bias: Respondent exaggerates answers to look good.
<font color="navy">c)</font> Intentional deception: Respondent deliberately lies.
<font color="navy">d)</font> Incorrect measurement: Respondent misunderstands the question or units.
• Error due to the measurement instrument: Concepts defined ambiguously (e.g., "glass of water", "unemployed").
• Error due to the method of data collection:
<font color="navy">i)</font> Personal interviews: Good response rate but expensive; risk of interviewer bias.
<font color="navy">ii)</font> Telephone interviews: Cheaper but harder to get a complete frame; must be shorter.
<font color="navy">iii)</font> Self-administered questionnaires: Cheapest but high non-response rate and potential bias.
<font color="navy">iv)</font> Direct observation: Less bias but prone to human error.

<font color="navy">**2. Reducing Errors**</font>
为了减少非抽样误差，我们可以采取以下措施：
• Callbacks: Re-attempting to contact sampling elements at different times to reduce non-response.
• Rewards / Incentives: Offering benefits (money, products) to encourage participation. Note: Rewards should be offered after selection to avoid selection bias.
• Interviewer training: Training interviewers to remain neutral and encourage honest responses.
• Data checks: Performing logic checks (e.g., proportions between 0 and 1) after data collection.

<font color="navy">**3. Question Design**</font>
问卷设计是减少非抽样误差的关键。设计时需注意以下原则：
<font color="navy">3.1 Ordering Effects</font>
• It is usually better to ask general questions first, then follow with specific questions.
• Previous questions can change the frame of mind of a respondent (priming effect).
<font color="navy">3.2 Types of Questions</font>
• Closed questions: Have fixed choices or single numerical answers. Easier to analyze but restrictive.
• Open questions: Allow free-form answers. Yield nuanced data but hard to analyze. (Often used in pre-tests to design closed questions).
<font color="navy">3.3 Handling Uncertainty</font>
• "Don't know" options: Excluding these forces an opinion; including them may lead to laziness. Use screening questions to filter knowledgeable respondents.
• Middle-ground options: A neutral midpoint prevents forcing a direction but acts as an "easy out".
<font color="navy">3.4 Wording Pitfalls to Avoid</font>
• Leading questions: Questions phrased to favor a specific answer (e.g., "Do you agree that...").
• Unbalanced questions: Offering only one side of an argument. (Should use "Do you favor or oppose...").
• Argumentative tone: Using strong words like "forbid" vs "not allow".
• Double-barrelled questions: Asking about two concepts in one question (e.g., "Bill Clinton AND the loan to Mexico").
• Ambiguity: Unclear definitions (e.g., "How much water do you drink?").
<font color="navy">3.5 Memory Errors</font>
• Telescoping: Recent events seem more distant, and memorable distant events seem more recent.
• Solution: Relate questions to specific memorable events (anchoring) or use direct observation.

<font color="navy">**4. Likert Scales**</font>
Likert 量表用于测量态度或意见：
• Likert items: Statements where respondents choose a level of agreement (e.g., "Strongly Agree" to "Strongly Disagree").
• Likert scale: The sum or average of scores from multiple Likert items representing an overall attitude.
• Scale points: Usually 5 or 7 points. Odd numbers are preferred to provide a neutral midpoint (e.g., "Undecided").

<font color="navy">**5. Interpreting Results**</font>
在解释调查结果时，必须注意因果关系的推断风险：
• Confounding variables: Factors not considered by researchers that affect both the suspected cause and the effect.
• Simpson's Paradox: A trend that appears in groups of data can disappear or reverse when the groups are aggregated. (Example: Berkeley Sex Bias study, where department choice was the confounding variable).
• Correlation does not imply causation.

<font color="navy">**6. Planning a Survey (11-Point Plan)**</font>
规划调查时应遵循以下步骤：
<font color="navy">1.</font> Statement of objectives: Define clear, simple goals.
<font color="navy">2.</font> Target population: Define precisely.
<font color="navy">3.</font> The frame: Choose frames covering the population (multiple frames if needed).
<font color="navy">4.</font> Sample design: Determine method and sample size $n$.
<font color="navy">5.</font> Method of measurement: Interview vs. Questionnaire vs. Observation.
<font color="navy">6.</font> Measurement instrument: Design the questionnaire.
<font color="navy">7.</font> Selection and training of fieldworkers.
<font color="navy">8.</font> The pretest: Test design and estimate parameters.
<font color="navy">9.</font> Organization of fieldwork: Logistics.
<font color="navy">10.</font> Organization of data management: Handling large data.
<font color="navy">11.</font> Data analysis: Plan analysis methods beforehand.

==**Lecture 8: Applied Problems**==

<font color="navy">**Notation**</font>
• $N$: Population size
• $n$: Sample size
• $L$: Number of strata
• $N_i$: Population size of stratum $i$ (or subpopulation $i$)
• $n_i$: Sample size observed in stratum $i$ (random in post-stratification)
• $\overline{Y}_{pst}$: Post-stratified estimator of the mean
• $\hat{\phi}$: Sample proportion of "Yes" answers in Random Response Model
• $p$: Proportion of population in Group A (sensitive group)
• $p_S$: Probability of answering the sensitive question
• $p_{Yes|T}$: Probability of answering "Yes" to the trivial question
• $\hat{\sigma}_i^2$: Sample variance of stratum/subpopulation $i$ (denominator $n_i-1$)
• $\tau_1$: Subpopulation total
• $U_i$: Auxiliary variable for subpopulation ($Y_i$ if in subpop, 0 otherwise)

<font color="navy">**1. Random Response Model(Respondents are unlikely to give truthful answers.)**</font>
Used to estimate proportion $p$ of a sensitive group (Group A) when respondents may not answer truthfully. Uses a randomization device (e.g., coin).  一般用于问你是Group A还是Group B这样的二分类问题。
• Setup:
<font color="navy">1.</font> Sensitive Question: "Are you in Group A?"
<font color="navy">2.</font> Trivial Question: "Is the last digit of your phone number even?" (Known probability $p_{Yes|T}$).
<font color="navy">3.</font> Randomization device: Answer sensitive question with probability $p_S$, trivial with $1-p_S$.
• Estimator:
By Law of Total Probability: $\phi = p\cdot p_S + p_{Yes|T}(1-p_S)$.
The estimator for $p$ is:$\hat{p} = \left[ \hat{\phi} - p_{Yes|T}(1-p_S) \right] / p_S$
• Variance:$$\widehat{Var}(\hat{p}) = {\widehat{Var}(\hat{\phi})}\big /{p_S^2} = \frac{1}{p_S^2}\left(1-\frac{n}{N}\right)\frac{1}{n-1}\hat{\phi}(1-\hat{\phi})$$
<font color="navy">Note</font>: The factor $\frac{1}{p_S^2}$ represents the variance penalty for using the random response model. Variance is larger than direct questioning.

<font color="navy">**2. Post-Stratification(The sample is unrepresentative.)**</font>
Used when strata cannot be determined *before* sampling (e.g., gender in a phone survey), but stratum weights $N_i/N$ are known. The sample sizes $n_i$ are random variables.
• Estimator:$$\overline{Y}_{pst} = \sum_{i=1}^{L} \frac{N_i}{N}\overline{Y}_i$$ , where $\overline{Y}_i$ is the sample mean of stratum $i$.
• Variance Estimator: when N is large N-n/nN is 1/n and N-n/N-1 = 1
$$
\widehat{Var}(\overline{Y}_{pst}) = \sum_{i=1}^{L}\frac{N-n}{nN}\frac{N_i}{N}\hat{\sigma}_i^2 + \sum_{i=1}^{L}\frac{1}{n^2}\frac{N-n}{N-1}\left(1-\frac{N_i}{N}\right)\hat{\sigma}_i^2
$$
<font color="navy">Interpretation</font>:
• First term: Equivalent to stratified sampling with proportional allocation.
• Second term: The increase in variance due to the randomness of $n_i$. When n is large, the increase is small.
• Condition: Only use post-stratification when $n$ and all $n_i$ are reasonably large.

<font color="navy">**3. Adjusting for Non-response**</font>
Non-response introduces bias if non-respondents differ from respondents.
High non-response rate $\Rightarrow$ sample not properly reflect the groupings in  the population $\Rightarrow$ some stratum is over-represented
<font color="red">3.1 Post-stratification Adjustment</font>
• Use when population stratum proportions $N_i/N$ are known.
• Treat respondents as the sample and adjust weights to match population $N_i/N$.
• Use $\overline{Y}_{pst}$ formulas.
• Effect: 1. Correct the estimate 2. standard deviation has reduced, because of the small variance within groups.
<font color="red">3.2 Weight-class Adjustment</font>
• Use when population stratum proportions $N_i/N$ are unknown.
• Estimate stratum sizes $\hat{N}_i$ from the initial sample (including non-respondents).  $$\hat{N}_i = N \cdot {n_{i, \text{total}}}/{n_{\text{total}}}$$  • Estimator: $\overline{y}_{wc} = \sum \frac{\hat{N}_i}{N}\overline{y}_i$.
• Effect: 1. This estimate is biased because of the estimation of the stratum sizes. 2. Variance is even smaller. 

<font color="navy">**4. Subpopulations (population we study contains elements we are not interested in)**</font>
Estimating parameters for a specific subpopulation (size $N_1$) where membership is not known prior to sampling.
<font color="navy">**4.1 Estimating Subpopulation Mean** $\mu_1 = \frac {1} {N_1} \sum_{j=1} ^ {N_1} Y_{1j}$</font>
• Estimator: $\hat{\mu}_1 = \overline{Y}_1 = \frac{1}{n_1}\sum_{i=1}^{n_1} Y_{1i}$ (This is technically a ratio estimator because $n_1$ is random).
• Variance Estimator:$\widehat{Var}(\overline{Y}_1) = \frac{N^2}{N_1^2}\left(1-\frac{n}{N}\right)\frac{1}{n}\frac{n_1-1}{n-1}\hat{\sigma}_1^2$
If $N_1/N$ is unknown, approximate using $n_1/n$:$\widehat{Var}(\overline{Y}_1) = \left(1-\frac{n}{N}\right)(\frac{n}{n-1})(\frac{n_1-1}{n_1})\frac{\hat{\sigma}_1^2}{n_1}$ $ \approx \left(1-\frac{n}{N}\right)\frac{\hat{\sigma}_1^2}{n_1}$ when $n, n_1$ are large
<font color="navy">**4.2 Estimating Subpopulation Total $\tau_1$**</font>
•<font color=red> Case A</font>: $N_1$ is Known$$\hat{\tau}_1 = N_1 \overline{Y}_1$$
$$\widehat{Var}(\hat{\tau}_1) = N_1^2 \widehat{Var}(\overline{Y}_1) \approx N_1^2 \left(1-\frac{n}{N}\right)\frac{\hat{\sigma}_1^2}{n_1}$$
This has lower variance (preferred).
• <font color=red> Case B</font>: $N_1$ is Unknown
Define variable $U_i = Y_i$ if element $i$ is in subpopulation, $0$ otherwise.
$$\hat{\tau}_1 = \frac{N}{n}\sum_{i=1}^{n} U_i = N\overline{U}$$
$$\widehat{Var}(\hat{\tau}_1) = N^2\left(1-\frac{n}{N}\right)\frac{\hat{\sigma}_u^2}{n}$$
• Calculation of $\hat{\sigma}_u^2$:
Sample variance of $U$ (including the $n-n_1$ zeros). $$\hat{\sigma}_u^2 = \frac{1}{n-1}\left(\sum_{i=1}^{n} U_i^2 - n(\overline{U})^2\right)$$, where $\sum U_i^2 = \sum_{j=1}^{n_1} y_{1j}^2$.
$y_{1j}$ 就是你抽到的那 $n_1$ 个“有效样本”（子总体成员）的具体数值。
<font color="navy">Note</font>: This estimator has higher variance because the zeros in $U$ inflate the variance ($\hat{\sigma}_u^2 > \hat{\sigma}_1^2$). 

<font color=red>1. </font>Main motivation to use Stratified Random Sampling:  Reduce **var** and **control sample composition** by dividing the population into strata and sampling within each stratum.
<font color=red>2. </font>Main reason to use Cluster Sampling: Reduce **cost** by sampling natural groups (clusters) instead of individual units.
<font color=red>3. </font>Main reason to use Systematic Sampling: Achieve **operational simplicity** and **good coverage of an ordered population** using one random start and then every k-th unit.
<font color=red>4. </font>Main motivation of using two-stage Cluster Sampling instead of one-stage Cluster Sampling: **Cut cost and gain flexibility** when clusters are large by sampling only a subset of units within each selected cluster instead of all units.
<font color=red>5. </font>Main motivation of using repeated systematic sampling: To obtain a design-based estimate of the var of a systematic-sample estimator without relying on the random-order assumption, and to protect against hidden trends or periodicity in the ordered population.
<font color=red>6. </font>Main reason to use Ratio estimator: To **use a known auxiliary variable X** that is strongly correlated with Y, so we get a **lower-var estimate** of the population mean/total when Y is roughly proportional to X. = nonzero intercept Regression
<font color=red>7. </font>Main reason to use Regression estimator: To **use one or more known auxiliary variables X1, X2, ...** that are strongly correlated with Y, ... by adjusting for the linear relationship between Y and the X's.
<font color=red>8. </font>C.I. Assumption: The distribution of the cluster totals (the systematic sample totals) is approximately Normal, or equivalently the CLT applies to the mean of the  cluster totals.
