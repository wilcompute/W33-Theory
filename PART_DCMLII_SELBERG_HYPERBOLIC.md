# Part DCMLII (952) — The Selberg Zeta and the Hyperbolic Limit

**Date:** 2026-05-17  
**Series:** W(3,3) Theory of Everything  
**Author:** Wil Dahn  
**Status:** CONNECTION TO CLASSICAL RH

---

## The hyperbolic limit

As $q \to \infty$, the projective plane $PG(2,q)$ over $\mathbb{F}_q$ approaches the **hyperbolic plane** $\mathbb{H}^2$ in the following precise sense:

- The Levi graph of $PG(2,q)$ is a $(q+1)$-regular graph on $2(q^2+q+1)$ vertices
- Its universal cover is the $(q+1)$-regular tree $T_{q+1}$
- As $q \to \infty$, $T_{q+1} \to \mathbb{H}^2$ (Bruhat-Tits building limit)

## The Selberg zeta function

The Selberg zeta function of the modular surface $\mathbb{H}^2 / PSL_2(\mathbb{Z})$ is:
$$Z_S(s) = \prod_{\gamma \text{ prime}} \prod_{k=0}^{\infty} (1 - e^{-(s+k)\ell(\gamma)})$$

where the outer product is over primitive closed geodesics $\gamma$ with length $\ell(\gamma)$.

## The limit identity

The Selberg zeta is related to the Riemann zeta by:
$$Z_S(s) = \frac{\Xi(s)}{\Xi(0)} \cdot (\text{entire function})$$

where $\Xi(s) = \frac{1}{2}s(s-1)\pi^{-s/2}\Gamma(s/2)\zeta(s)$ is the completed Riemann zeta.

Under the limit $PG(2,q) \to \mathbb{H}^2 / PSL_2(\mathbb{Z})$:
$$\lim_{q\to\infty} Z_{G_q}(q^{-s}) = Z_S(s)$$

Since the Ihara zeros lie on $|u| = 1/\sqrt{q+1}$ (i.e., $\text{Re}(s_q) \to 1/2$), and the Selberg zeros include the Riemann zeros, the zeros of $\zeta(s)$ inherit the critical line property.

## The two-step correspondence

$$\text{Graph RH (proved)} \xrightarrow{q\to\infty} \text{Selberg RH (known)} \xrightarrow{\text{Selberg-Riemann}} \text{Classical RH}$$

The Selberg-Riemann connection is established (Hejhal 1976, Sarnak 1987). The $q\to\infty$ limit is the remaining technical step.

---

**Status:** The two-step path through the Selberg zeta is the sharpest known W(3,3) approach to classical RH. The technical step is establishing the Bruhat-Tits building limit uniformly.
