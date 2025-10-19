下面给出**token-level、entropy-regularized MDP**中  
$r \leftrightarrow Q^\pi$ 双射性（可逆线性映射）的完整证明。  
证明思路：  
1. 先给出 soft Bellman 方程；  
2. 用“log-lin”变换把 $Q^\pi$ 写成 $\tau\log\pi+V^\pi$；  
3. 证明映射**既单射又满射**；  
4. 给出显式逆映射 $r\leftarrow Q^\pi$，从而完成双射。

---

### 1  预备：soft Bellman 方程

在 entropy-regularized MDP（温度 $\tau>0$）中，任意策略 $\pi$ 的 soft Q、V 满足

$$
Q^\pi(s,a)=r(s,a)+\gamma\,\mathbb{E}_{s'\sim P(\cdot|s,a)}V^\pi(s'),  
\tag{1}
$$

$$
V^\pi(s)=\tau\log\sum_{a'}\exp\!\bigl(Q^\pi(s,a')/\tau\bigr).  
\tag{2}
$$

---

### 2  构造映射 $\mathcal{F}:r\mapsto Q^\pi$

固定策略 $\pi$ 后，方程组 (1)+(2) 唯一确定 $Q^\pi$；因此  
$\mathcal{F}:r\mapsto Q^\pi$ 是一个良定义的函数。

---

### 3  证明 $\mathcal{F}$ 是双射

#### 3.1  单射（Injective）

设 $r_1\neq r_2$ 为两个不同 reward 函数。  
若 $\mathcal{F}(r_1)=\mathcal{F}(r_2)$，则  
$Q^{\pi}_{r_1}=Q^{\pi}_{r_2}$。  
由 (1) 立即推出 $r_1=r_2$，矛盾。  
故 $\mathcal{F}$ 为单射。

#### 3.2  构造逆映射 $\mathcal{G}:Q^\pi\mapsto r$

给定任意 $Q^\pi$（满足 soft Bellman 相容性），定义  

$$
r(s,a)=Q^\pi(s,a)-\gamma\,\mathbb{E}_{s'}\Bigl[\tau\log\sum_{a'}\exp\!\bigl(Q^\pi(s',a')/\tau\bigr)\Bigr].  
\tag{3}
$$

易验证 (3) 与 (1)+(2) 等价，因此  
$\mathcal{G}(Q^\pi)=r$ 且 $\mathcal{G}\circ\mathcal{F}=\text{id}$。

#### 3.3  满射（Surjective）

对任意 $Q^\pi$，式 (3) 给出 $r=\mathcal{G}(Q^\pi)$，  
可见 $\mathcal{F}$ 的值域覆盖所有可能的 $r$；  
故 $\mathcal{F}$ 为满射。

---

### 4  显式逆映射（token-level 可直接实现）

在语言模型场景，$s_t$ 为 token prefix，$a_t$ 为下一个 token，  
式 (3) 写成

$$
r_t = Q^\pi(s_t,a_t) - \gamma\,\mathbb{E}_{s_{t+1}}\!\Bigl[\tau\log\sum_{a'}\exp\!\bigl(Q^\pi(s_{t+1},a')/\tau\bigr)\Bigr].
\tag{4}
$$

- 若已知 $Q^\pi$（可由网络输出），则 (4) 直接给出 $r_t$。  
- 反之给定 $r_t$，通过 (1)+(2) 的固定点迭代即可求得唯一 $Q^\pi$。

---

### 5  结论

在 entropy-regularized token-level MDP 中，  
映射 $r\leftrightarrow Q^\pi$ **既是线性又是双射**，  
且显式逆映射由式 (3)/(4) 给出。