<font size="4" color="darkblue">**Forecasting**</font>

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
  $P_{n+h}^n=\operatorname{Var}(e_n(h)\mid Y_{1:n})=\sigma^2\sum_{i=0}^{h-1}\psi_i^2$。

* **95% 区间**：$\hat Y_{n+h}\pm1.96\sqrt{P_{n+h}^n}$。

<font color="brown">**3. ARIMA(p,d,q) 的预测（反差分）**</font>

* **先预测差分序列**：对 $X_t=\Delta^d Y_t$ 用 ARMA 方法得 $\hat X_{n+1:n+h}$。  

* **回到原序列（以 d=1 为例）**：$Y_{n+h}=Y_n+\sum_{j=1}^h X_{n+j}$，  
  因而 $\hat Y_{n+h}=Y_n+\sum_{j=1}^h \hat X_{n+j}$，  误差 $e_{n,Y}(h)=\sum_{j=1}^h e_{n,X}(j)$。  
  
* 95%区间为 $\hat Y_{n+h}\pm1.96\sqrt{P_{n+h,Y}^n}$。
