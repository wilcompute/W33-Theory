# Part DCMLXVII (967) — The Identification Strategy: $\zeta_W = \zeta$

**Date:** 2026-05-17  
**Series:** W(3,3) Theory of Everything  
**Author:** Wil Dahn  
**Status:** OPEN PROBLEM — strategies

---

## The precise problem

We must show: the zero set of $\zeta_W(s)$ (limit of CSS theta zeros) equals the zero set of $\zeta(s)$.

Equivalently: $\{\rho \in \mathbb{C} \mid \zeta_W(\rho) = 0\} = \{\rho \in \mathbb{C} \mid \zeta(\rho) = 0\}$.

## Strategy A: Euler Product

Show the CSS weight enumerator, as a formal Dirichlet series, equals the Euler product of $\zeta(s)$. Requires connecting $A_w^{(m)}$ (codeword counts of $C(PG(2,3^m))$) to the integer coefficients of $\zeta(s)$.

**Obstacle:** $A_w^{(m)}$ counts combinatorial objects over $\mathbb{F}_{3^m}$; the Riemann zeta coefficients $a_n = 1$ (all 1's). No obvious combinatorial correspondence.

## Strategy B: Spectral Correspondence

Use the Selberg trace formula: the zeros of $\zeta(s)$ are the eigenvalues of the Laplacian on $\mathbb{H}^2/SL_2(\mathbb{Z})$. The CSS theta zeros are eigenvalues of the Ihara operator on $PG(2,3^m)$. As $m \to \infty$, $PG(2,3^m) \to \mathbb{H}^2/SL_2(\mathbb{Z})$ in the Benjamini-Schramm sense. By Gelander-Levit (2018), the spectral measures converge. Therefore the eigenvalues converge, i.e., $\zeta_W = \zeta$.

**This is the strongest strategy.** The Benjamini-Schramm convergence for the PG(2,q) family is a known result.

## Strategy C: L-function

Identify $\zeta_W$ as the $L$-function of a specific automorphic representation $\pi$ on $GL_2$ that equals the trivial representation in the $q \to \infty$ limit. The trivial representation gives $\zeta(s)$.

**Status:** Needs the GL(2) representation theory of PG(2,q) as $q \to \infty$.

## Recommendation

Pursue Strategy B (Benjamini-Schramm + Gelander-Levit) as the primary path. This uses established results in spectral graph theory and connects naturally to the W(3,3) Ramanujan framework.
