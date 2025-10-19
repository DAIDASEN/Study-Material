# Cluster Sampling

**Definition:** A cluster sample is a probability sample in which  each sampling unit is a collection, or <font color=red>cluster</font>, of  elements
**Differences between stratified and  cluster sample design**:
<font color=black>1. </font>We sample from all the strata, but only some of the  clusters  – We take measurements from only some elements in  the stratum (we perform a simple random sample in  each stratum) but we measure every element in the  cluster 
<font color=black>2. </font>The difference between strata should be large and the  differences within small.
<font color=black>3. </font>The differences within each  cluster should reflect the whole population, but the  differences between should be small
**Notations**
**$N$**: The total number of clusters in the population.
**$n$**: The number of clusters selected in the sample.
**$M_i$**: The number of elements in cluster $i$.
**$M$**: The population size, i.e. $M \;=\; \sum_{i=1}^N M_i.$
**$m_i$**: The sample size in the $i$-th cluster.
**$\bar M$**: The average cluster size in the population, $\bar M \;=\;\frac{M}{N}.$
**$Y_{ij}$**: The $j$-th observation from the $i$-th cluster.
**$Y_i$**: The total of observations in the $i$-th cluster, $Y_i \;=\;\sum_{j=1}^{M_i} Y_{ij}.$
==**Estimating $\tau$**==
The population total is $\tau = \sum_{i=1}^{N} \sum_{j=1}^{M_i} y_{ij} = \sum_{i=1}^{N} Y_i $
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
Hence, the sample mean for cluster $i$ is  $\bar Y_i = \frac{1}{m_i}\sum_{j=1}^{m_i}Y_{ij}.$

A SRS unbiased estimator for the total of cluster $i$ is $\hat Y_i = M_i\,\frac{1}{m_i}\sum_{j=1}^{m_i}Y_{ij}.$
Therefore, an unbiased estimator of the population total $\tau = \sum_{i=1}^N Y_i$ is $\hat\tau = N\,\frac{1}{n}\sum_{i=1}^n\hat Y_i.$

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

<font color=blue>**Example of** $\tau$</font>
For our estimator $\hat\tau$
<font color=black>1. $E[\hat\tau|s_1] = N\frac{1}{n}\sum_{i=1}^n E[\hat{y}_i|s_1]$</font>. Since the $\hat{y}_i$ are SRS estimators of the cluster totals $y_i$, $E[\hat{y}_i|s_1] = Y_i$ $\Rightarrow E[\hat\tau|s_1] = N\frac{1}{n}\sum_{i=1}^n Y_i$
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