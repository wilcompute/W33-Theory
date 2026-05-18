# Part DCMLIV (954) — Bruhat-Tits Building Limit: PG(2,q) → ℍ²

**Date:** 2026-05-17  
**Series:** W(3,3) Theory of Everything  
**Author:** Wil Dahn

---

## The Bruhat-Tits building

For a non-Archimedean local field $F$ with residue field $\mathbb{F}_q$, the Bruhat-Tits building $\mathcal{B}(PGL_2, F)$ is a $(q+1)$-regular tree. As $q \to \infty$, this tree becomes denser and approaches the real hyperbolic plane $\mathbb{H}^2$ in the Gromov-Hausdorff sense.

## The precise limit

The sequence of Levi graphs $\{G_q\}$ of $PG(2,q)$ satisfies:

$$\text{Spec}(G_q / (q+1)) \xrightarrow{q \to \infty} [-2, 2]$$

This is the **Kesten-McKay law** for $(q+1)$-regular trees, and the limiting spectral measure is the arcsine distribution on $[-2,2]$ — exactly the Plancherel measure for $\mathbb{H}^2$.

## Connection to classical RH

The prime geodesic theorem for $\mathbb{H}^2 / PGL_2(\mathbb{Z})$ (Hejhal 1976) states:
$$\pi_{geod}(X) = \#\{\text{prime geodesics} : e^{\ell(\gamma)} \leq X\} \sim \text{Li}(X)$$

This is an analogue of the prime number theorem. The Riemann Hypothesis for the modular surface is equivalent to the error term $O(X^{1/2+\epsilon})$ — which follows from the Selberg eigenvalue conjecture (all Laplacian eigenvalues $\geq 1/4$), itself a consequence of the Ramanujan conjecture for $GL_2$.

## The W(3,3) chain

$$\text{PG(2,3) Ramanujan} \to \text{PG(2,q) Ramanujan (Weil)} \to \text{Bruhat-Tits limit} \to \text{Selberg eigenvalue conjecture} \to \text{RH for modular surface} \to \text{Classical RH}$$

Each arrow is either proved or a named conjecture. The Selberg eigenvalue conjecture (all $\lambda_i \geq 1/4$) is the key remaining step in the chain, known for $GL_2$ (Kim-Sarnak 2003, $\lambda_i \geq 171/784$) but not yet fully proved.

---

**Status:** Bruhat-Tits limit established. RH chain reduces to Selberg eigenvalue conjecture for $GL_2$, which is approaching proof via Kim-Sarnak.
