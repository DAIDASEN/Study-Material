## 8) The Problem of Running Average & Its Expectation  

* Define running average $ m_t = \delta m_{t-1} + (1 - \delta) g_t, \ m_0 = 0 $.
* Finite geometric series indicates: if data is stationary,
$$
E[m_t] \approx E[g_t](1 - \delta^t) + \zeta',
$$
indicating early **bias towards 0** (due to initialization at 0). The same reasoning applies to the second-moment running average. 

The bias arises from initialization $ (m_0 = 0) $, causing early “averages” to be influenced by **zero padding**; the goal of correction is to eliminate this “start-up bias.”

---

## 9) Running-Average **Bias Correction**

$$
\hat{E}[(\partial_w L)^2]_{t-1} = \frac{E[(\partial_w L)^2]_{t-1}}{1 - \gamma^{t-1}},
\qquad
\hat{E}[\partial_w L]_{t-1} = \frac{E[\partial_w L]_{t-1}}{1 - \delta^{t-1}}.
$$
The correction effect is **largest** at small $ t $. 

These denominators serve as the **normalization constants** for the geometric weights (offsetting the bias from “starting at 0”), similar to the standard unbiased correction for exponential weighted moving averages (EWMA).

---

## 10) Adam: Adaptive Moment Estimation 

$$
\boxed{w_t = w_{t-1} - \alpha \frac{\hat{E}[\partial_w L]_{t-1}}{\hat{E}[(\partial_w L)^2]_{t-1} + \varepsilon},}
\qquad
\begin{aligned}
\hat{E}[(\partial_w L)^2]_{t-1} &= \frac{E[(\partial_w L)^2]_{t-1}}{1 - \gamma^{t-1}}, \\
\hat{E}[\partial_w L]_{t-1} &= \frac{E[\partial_w L]_{t-1}}{1 - \delta^{t-1}}.
\end{aligned}
$$
Typical: $(\alpha = 10^{-3}, \gamma = 0.999, \delta = 0.9, \varepsilon = 10^{-7})$. 

---

## 11)Learning Rate Scheduling

* Many popular methods can be viewed as GD with a shaped step:
  $$
  w^{t} = w^{t-1} - \frac{\alpha}{\sqrt{\hat{E}\left[(\partial_{w}L)^2\right]_{t-1} + \varepsilon}} \hat{E}\left[\partial_{w}L\right]_{t-1}.
  $$
* Why schedule the learning rate ourselves?

  * **Beginning:** use a **large** LR to increase speed.
  * **End:** use a **small** LR to improve accuracy.

**Learning rate decay schedulers (as on the slides):**

* **“Old days” manual:** reduce LR by a factor of 10 every **XX** epochs.
* **Factor:**$ \alpha_{t+1} = \max(\alpha_{\min}, \alpha_t \cdot \tau)$
* **Multi-factor (milestones):**$ \alpha_{t+1} = \alpha \cdot \tau$ every several epochs / at milestones.
* **Cosine:** 
  $$
  \alpha_t = \alpha_T + \frac{\alpha_0 - \alpha_T}{2} \left(1 + \cos\left(\frac{\pi t}{T}\right)\right)
  $$
* **Warmup:** for unstable optimization, start with a **small LR** then ramp to target LR.

![image-20251004164016466](C:\Users\31670\AppData\Roaming\Typora\typora-user-images\image-20251004164016466.png)
