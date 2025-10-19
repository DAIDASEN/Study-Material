==<font color=black>**Definitions of Population Parameters:**</font>==
1.Population Mean: $\mu = \frac{\sum_{i=1}^N x_i}{N}$ (Equals to average value)
2.Finite Population Variance: $\sigma^2 = \frac 1N \sum_{i=1}^N(x_i-\mu)$
   Population standard deviation (SD): $\sqrt{\frac1N\sum_{i=1}^N(x_i-\mu)}$
3.Covariance: $Cov(X, Y) = \frac1N\sum_{i=1}^{N}[(y_i-\mu_Y)(x_i-\mu_X)] = E(XY)-E(X)E(Y)$
4.Correlation:$\rho=\frac{Cov(X, Y)}{\sigma_X\sigma_Y}$
5.$U = \sum a_i X_i \rightarrow Var(U) = \sum_{i=1}^{n}a_i^2Var(X_i) + \sum_{i=1}^n\sum _{j\neq i}a_ia_jCov(X_i,X_j)$ 

==<font color=black>**Estimation:**</font>==
we would like our estimation to be close to $\theta \Rightarrow |\hat\theta - \theta|$ to smaller than some number d. $|\hat\theta - \theta|$ is <font color=red>error of estimation</font>
<font color=red>$Pr(|\hat\theta - \theta|<d) = 1-\alpha$</font>, where $\alpha$ is a small number and $d$ is called <font color=red>margin of error.</font>
样本量$n$ 决定估计量$\hat\theta$ 的抽样分布特性
-$n$ 很小 → 分布复杂且未知
-$n$ 足够大（相对于无限总体）→ CLT生效，可用正态等熟悉分布近似 
-$n$ 很大且接近总体规模$N$ → 抽样方差急剧降低，但需FPC，分布不再是简单的正态
If we are confident enough to say $\frac{\hat\theta-E[\hat\theta]}{\sigma_\hat\theta} \sim N(0,1)$
Then we have $P(\hat \theta - \sigma_\hat\theta z_{1-\frac\alpha2}<E[\hat\theta]<\hat \theta +\sigma_\hat\theta z_{1-\frac\alpha2}) = 1-\alpha$
If $\hat \theta$ is unbiased $\Rightarrow E[\hat\theta] = \theta$ then we have $P(- \sigma_\hat\theta z_{1-\frac\alpha2}<\hat\theta-\theta<\sigma_\hat\theta z_{1-\frac\alpha2}) = 1-\alpha \Rightarrow P(|\hat \theta - \theta|<\sigma_\hat\theta z_{1-\frac\alpha2}) = 1-\alpha$meaning we have found  our sensible number, $d$
The interval above is the <font color=red>$100 \times (1-\alpha)%$ confidence interval</font> for parameter 
For a observation of $\hat \theta$ we want <font color=red>$E[\hat \theta] -\theta=0 $</font><font color=blue>**(bias)**</font> and <font color=red>$E[(\hat \theta - \theta)^2]$</font><font color=blue>**(MSE)** </font><font color = red>is small
 </font>
$MSE(\hat\theta) = Var(\hat \theta)+Bias(\hat \theta)^2$, if estimate unbiased MSE equals its variance.
**<font color=Red>Three words describe an estimator:</font> ** 1. **Unbiased** 2. **Precise** (Var is small) 3. **Accurate** (Unbiased + Precise)

==**<font color=black>Survey Terminology:</font>**==

1. Population: A collection of elements about which we want to  make inferences
2. Element: An element is an object on which a measurement  is taken
3. Sampling Units: Partition the population
4. Frame: A frame is a list of sampling units
5. Sample: A collection of sampling units drawn from a single  or from multiple frames

<font color=Red>Probability Sampling:</font> Each population unit has a known and non-zero probability of being selected, and the sampling process relies entirely on a random mechanism. **Can make probability statements (e.g. *Confidence Intervals*)** <font color = blue>Randomisation balances out all factors inherent in a  population</font>
<font color=red>Quota Sampling:</font> Quotas are first established based on certain characteristics (such as gender, age, region), then interviewers **subjectively** or conveniently select samples within each quota.  **Can not make probability statements**

**<font color=black>==Simple Random Sampling(SRS)==</font>**

---

<font color=purple>**Notation（抽样率 & f.p.c.）**</font>  

- **population size** $N$，**sample size** $n$，**sampling fraction **$f=\frac{n}{N}$，**finite population correction** f.p.c.$=1-f=1-\frac{n}{N}$。  
- **population mean** $\mu=\frac{1}{N}\sum_{j=1}^N u_j$。样本观测记为$Y_1,\dots,Y_n$，样本均值$\bar Y=\frac{1}{n}\sum_{i=1}^n Y_i$。  
- 记$Z_j=\mathbf 1\{\text{单位 }j\text{被抽中}\}$，则$\bar Y=\frac{1}{n}\sum_{j=1}^N u_j Z_j$。

---

所有大小为$n$ 的样本等概率；任意单位的**包含概率**：$\displaystyle \Pr(Z_j=1)=\frac{n}{N}$。
**<font color=green>Proof</font>（含$\Pr(Z_j=1)$）**  $\displaystyle \Pr(Z_j=1)=\frac{\binom{N-1}{n-1}}{\binom{N}{n}}=\frac{n}{N}$。

---

<font color=purple>**Estimating a mean $\mu$**</font>

**(A) Unbiasedness**  $\displaystyle \mathbb E[\bar Y]=\mu$.
**<font color=green>Proof</font>**   $\displaystyle \mathbb E[\bar Y]=\frac{1}{n}\sum_{j=1}^N u_j\,\mathbb E[Z_j]=\frac{1}{n}\sum_{j=1}^N u_j\,\frac{n}{N}=\mu$.

**(B) Variance of $\bar Y$**  
$$\boxed{\mathrm{Var}(\bar Y)=\frac{1-\frac{n}{N}}{n}\cdot \frac{1}{N-1}\sum_{j=1}^N\bigl(u_j-\mu\bigr)^2\ = \frac{N-n}{\,N-1\,}\;\frac{\sigma^2}{\,n\,}}.$$
**<font color=green>Proof</font>**  
记$a_j=\frac{u_j}{n}$。有  
$\displaystyle \mathrm{Var}(\bar Y)=\sum_j a_j^2\mathrm{Var}(Z_j)+\sum_{j\ne k}a_ja_k\mathrm{Cov}(Z_j,Z_k)$。  
SRS 下$\mathrm{Var}(Z_j)=\frac{n}{N}\Bigl(1-\frac{n}{N}\Bigr)$,   $E(Z_j) = \frac nN$
$\mathrm{Cov}(Z_j,Z_k)= E(Z_j Z_k) - E(Z_j)E(Z_k)=\frac{n(n-1)}{N(N-1)}-\frac{n^2}{N^2}\\=-\,\frac{n}{N}\Bigl(1-\frac{n}{N}\Bigr)\frac{1}{N-1}$。  

**(C) Unbiased estimator of $\mathrm{Var}(\bar Y)$ **  
$$\boxed{\ \widehat{\mathrm{Var}}(\bar Y)=\frac{1-\frac{n}{N}}{n}\cdot \frac{1}{n-1}\sum_{i=1}^n\bigl(Y_i-\bar Y\bigr)^2\ }.$$
<font color=green>**Proof**</font>
From B we have $Var(\bar Y)$ with $\sigma^2$, however it is hard to know.
Noticed that if we use $s^2 = \frac{1}{n-1}\sum_{i=1}^n(y_i-\bar y)^2$ to represent $\hat \sigma^2$. It is biased $E[\hat \sigma^2] = \frac{N}{N-1}\sigma^2$
Therefore, $(1-\frac1N)\hat \sigma ^2$ is an unbiased estimator of $\sigma^2$, then we have our $\widehat {Var}(\bar Y)$

**(D) t‑CI for $\mu$**  
$$\boxed{\ \mu \in \bar y\ \pm\ t_{n-1,\alpha/2}\ \sqrt{\ \frac{1-\frac{n}{N}}{n}\cdot \frac{1}{n-1}\sum_{i=1}^n\bigl(y_i-\bar y\bigr)^2\ }\ }.$$

---

<font color=purple>**Sample size for $\mu$（目标半宽$d$）**</font>

$$\boxed{\ n=\frac{N\,z_{\alpha/2}^2\,v^2}{d^2\,(N-1)+z_{\alpha/2}^2\,v^2}\ }.$$ 其中$v$是方差，如果不知道可以用s

若用$t$ 值，解$\displaystyle n=\frac{N\,t_{n-1,\alpha/2}^2\,v^2}{d^2\,(N-1)+t_{n-1,\alpha/2}^2\,v^2}$；因$t$ 随$n$ 变化，需迭代试算。

---

<font color=purple>**Estimating a total $\tau=N\mu$**</font>

**结论（点估计 / 方差估计 / t‑CI）**  

$\displaystyle \hat\tau=N\,\bar y$.  

$Var(\hat \tau) = \frac{N-n}{N-1} \frac{N^2}{n}\sigma^2$

$\displaystyle \widehat{\mathrm{Var}}(\hat\tau)=N^2\cdot \frac{1-\frac{n}{N}}{n}\cdot \frac{1}{n-1}\sum_{i=1}^n\bigl(y_i-\bar y\bigr)^2$.  

$\displaystyle \boxed{\ \tau \in N\bar y\ \pm\ t_{n-1,\alpha/2}\ N\sqrt{\ \frac{1-\frac{n}{N}}{n}\cdot \frac{1}{n-1}\sum_{i=1}^n\bigl(y_i-\bar y\bigr)^2\ }\ }$.

**样本量（目标半宽$d$）**   
$$\boxed{\ n=\frac{N\,z_{\alpha/2}^2\,v^2}{\left(\frac{d}{N}\right)^2\,(N-1)+z_{\alpha/2}^2\,v^2}\ }.$$

---

<font color=purple>**Estimating a proportion $p$**</font>

把 0/1 变量视作均值问题：令$x_i\in\{0,1\}$，样本比例$\hat p=\bar x=\frac{1}{n}\sum_{i=1}^n x_i$。
$Var(\hat p)=\frac{N-n}{N-1}\frac1np(1-p)$

$\displaystyle \widehat{\mathrm{Var}}(\hat p)=\frac{1-\frac{n}{N}}{n}\ \hat p(1-\hat p)$

$\displaystyle \boxed{\ p \in \hat p\ \pm\ t_{n-1,\alpha/2}\ \sqrt{\ \frac{1-\frac{n}{N}}{n}\ \hat p(1-\hat p)\ }\ }$（常用条件：$n\hat p\geq 5,\ n(1-\hat p)\geq 5$ ）

