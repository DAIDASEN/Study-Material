# Stochastic Process

Definition: A collection of random variables $\{X_t\}_{t\in T}$

## Bernoulli Process

**Bernoulli distribution** $X\sim Bern(p)$, pmf: $P(X = 1) = p,\ P(X = 0) = 1-p$, mgf: $M_X(t) = pe^t+1-p$
**Bernoulli Process** A sequence $\{X_1,X_2,...\}$ of independent Bernoulli variables with $X_i\sim Bern(p)$ ==(P6最下面在讲什么？)==
**Number of success by time $n$**: $S_n=X_1+....+X_n$
**$k-th$ time of success:** $T_k = min\{n:S_n=k\}$
<font color=blue>**Binomial distribution: **</font>$S_n\sim B(n,p)$ represents the number of success in a Bernoulli process. pmf: $P(S_n=k)= C^k_np^k(1-p)^{n-k},\ for\ k= 0,...,n$, mgf: $M_{S_n}(t)=(pe^t+1-p)^n$
<font color=blue>**Geometric Distribution: **</font> represents the first success time in a Bernoulli process, that is $T_1\sim Geo(p)$. pmf: $P(T_1=n) = (1-p)^{n-1}p$ $E[T_1] = \frac1p, Var[T_1] = \frac{1-p}{p^2}$ and $M_{T_1}(t)=\frac{pt}{1-(1-p)e^t}$
<font color=blue>**Negative binomial distribution: **</font>represents the $r$-th success time, that is $T_r\sim NB(r,p)$. pmf: $P(T_r=n) = C^{r-1}_{n-1}(1-p)^{n-r}p^r$. $E[T_r] = \frac rp, Var[T_r] = r\frac{1-p}{p},\ M_{T_r}(t) = (\frac{1}{1-(1-p)e^t})^r$
<font color=green>*Generalized Binomial Theorem:*</font> $(x+y)^{-n}= \sum C_{n+k-1}^k(-x)^{-k}y^{-n-k}$

## Poisson Process

## Simple random walk, Brownian motion and Branching Process