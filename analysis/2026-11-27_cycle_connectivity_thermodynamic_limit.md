# The degree-two exchange ensemble loses connectivity in the large-size limit

The November 27 graph experiment gave a connected probability of 0.8723445 at eight vertices with the shifted Wilson factor and two exchange excitations. In that same labeled simple degree-two ensemble, **the connected probability tends to zero at every fixed positive cycle weight and fixed finite matter inverse temperature**. Thus this particular finite-size preference does not select a connected geometry. The executable witness reads the published graph certificate and independently recreates its eight-vertex result from the two-token Laplacians.

## Exact graph count

A labeled cycle on a given set of $l\ge3$ vertices has $(l-1)!/2$ undirected labelings. With weight $q>0$ per cycle and $\theta=q/2$, the exponential generating function is

```
A(z) = exp(theta * sum_{l>=3} z^l/l)
     = (1-z)^(-theta) exp(-theta*z-theta*z^2/2).
P_connected(n) = theta/(n*[z^n] A(z)).
```

Differentiating gives $n a_n=\theta\sum_{j=0}^{n-3}a_j$ with $a_0=1$ and $a_1=a_2=0$. This is a linear-time recurrence. At fixed $\theta>0$, singularity analysis gives $a_n\sim e^{-3\theta/2}n^{\theta-1}/\Gamma(\theta)$ and $P_{\rm connected}\sim e^{3q/4}\Gamma(1+q/2)n^{-q/2}$. [Degree-two random graphs](https://doi.org/10.1103/PhysRevE.107.024308) and [Flajolet–Odlyzko transfer theorem](https://doi.org/10.1137/0403019)

## Two exchange excitations cannot reverse the limit

The two-token Laplacian is positive semidefinite, has dimension $D=\binom n2$, and the degree of each token configuration is at most four. Thus its mean eigenvalue is at most four. For $b\ge0$, Jensen bounds its heat trace by $D e^{-4b}\le Z_2(G,b)\le D$. Reweighting changes any event probability by a factor between $e^{-4b}$ and $e^{4b}$. The connected probability therefore has order $n^{-q/2}$ for fixed $b,q$. With $k$ fixed hard-core exchange tokens the same bound uses $2k$ in place of four. Finite-density matter and size-dependent $b$ require separate analysis.

The shifted ternary Wilson factor is $q=(1+2e^{-3\beta/2})/3\ge1/3$. Connected probability decreases with $q$, since it is $1/(1+\sum_{j\ge2}N_j q^{j-1}/N_1)$, where $N_j$ counts graphs with $j$ cycles. Even size-dependent nonnegative gauge $\beta$ therefore gives probability $O(n^{-1/6})$ or smaller at fixed matter $b$.

## How strong a connectivity penalty would be needed?

The same heat-trace bound also gives a necessary resource scale for a growing number of tokens. For the shifted Wilson weight, the connected probability is at most a constant times `exp(2*b*k) n^(-1/6)`. Thus `b*k=o(log n)` still forces disconnection in probability. An order-one connected probability requires `b*k >= (log n)/12 - O(1)`, even before deriving whether the matter actually favors connectivity. At fixed fugacity `q`, the corresponding necessary lower bound is `(q/4)*log n - O(1)`.

Taking zero matter temperature first is another solvable limit. The two-token configuration graph splits by the token counts on each cycle. Within each count sector, moving a token along an edge to an empty site connects all configurations on a cycle, so there is exactly one zero mode per count sector. With `m` cycles, two tokens can occupy the same cycle in `m` ways or separate cycles in `m(m-1)/2` ways. Every cycle has room for both. The zero-temperature trace is therefore `m(m+1)/2`. This reweighting can only decrease connectivity, because connected graphs get weight one and every disconnected graph gets more. The joint limit with large but finite temperature parameter still requires separate control.

Without matter, $q_n=2c/\log n$ for fixed $c>0$ gives $P_{\rm connected}\to e^{-c}$. Weighted permutations with cycle weight $\theta=q/2$, conditioned to exclude cycles of lengths one and two, have the same cycle-size law as the undirected graph model. The factor of two per cycle accounts for orientation. Before conditioning, the one-cycle probability is $\prod_{j=1}^{n-1}(1+\theta/j)^{-1}$. The expected number of length $l$ cycles for $l=1,2$ is $(\theta/l)\prod_{i=0}^{l-1}(n-i)/(n-i-1+\theta)$, which tends to zero. Conditioning thus changes the one-cycle probability by a factor $1+o(1)$. The log of the product is $-\theta H_{n-1}+O(\theta^2)\to-c$. The requisite weight scale is below the floor of the Wilson rule. [Arratia–Tavare conditioning framework](https://arxiv.org/abs/1308.3279)

Run `python analysis/toe_20261127_cycle_connectivity.py`. The certificate uses exact rational arithmetic for the eight-vertex count and floating-point arithmetic for the heat traces and large-size scan. This calculation concerns equilibrium measure on labeled simple degree-two graphs. It leaves the switch-chain gap, interacting finite-density matter, higher-valence ensembles and any spacetime continuum as separate questions.
