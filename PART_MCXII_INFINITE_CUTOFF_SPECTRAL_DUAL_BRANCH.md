# Part MCXII: Infinite-Cutoff Spectral Equation of State and Dual Branch Limit

**Date:** 2026-05-19  
**Series:** W(3,3) Theory of Everything  
**Status:** VERIFIED LIMITING INVERSE BRANCH / CERTIFIED EQUATION-OF-STATE ENCLOSURES

---

## Why this part exists

Part MCXI showed that each finite-cutoff completed spectral packet has an invertible equation of state and a Legendre-dual description. The remaining natural question is whether this inverse branch is only a finite-cutoff convenience or whether it survives the infinite-cutoff limit in a controlled way.

---

## The theorem

Fix real $s>0$ and a compact deformation interval $0\le\lambda\le\rho<6$. For each cutoff $X$, the order parameter
\[
\mathcal M_X(s;\lambda)=\frac{\partial \mathcal F_X}{\partial\lambda}
\]
is strictly increasing in $\lambda$ and converges monotonically from below to the infinite-cutoff order parameter $\mathcal M_\infty(s;\lambda)$. If
\[
0<\mathcal M_\infty(s;\lambda)-\mathcal M_X(s;\lambda)\le T_X(\rho),
\]
then every target value $M$ in the infinite-cutoff branch range satisfies the inverse enclosure
\[
\boxed{
\lambda_X\bigl(s;\max\{M-T_X(\rho),\mathcal M_X(s;0)\}\bigr)
\le
\lambda_\infty(s;M)
\le
\lambda_X(s;M).
}
\]
Hence the finite-cutoff inverse branches decrease to a unique limiting inverse branch
\[
\lambda_\infty=\lambda_\infty(s;M).
\]
In particular, the completed spectral packet carries a genuine infinite-cutoff equation of state, and the finite-cutoff inverses converge to it monotonically from above with certified interval width.

Because the finite-cutoff Legendre potentials are evaluated on these inverse branches,
\[
\Gamma_X(s;M)=\lambda_X(s;M)\,M-\mathcal F_X\bigl(s;\lambda_X(s;M)\bigr),
\]
they converge to the corresponding infinite-cutoff dual branch as well.

---

## Reading

This completes the thermodynamic picture. The packet is no longer merely a convex free energy with an invertible finite-cutoff response curve. It now has a bona fide **infinite-cutoff equation of state** and a **limiting dual branch**, with explicit finite-cutoff enclosures that shrink as $X$ grows.

So the full global spectral object may be read in either of two equivalent languages:

1. the deformation language $\lambda \mapsto \mathcal F_\infty(s;\lambda)$;
2. the response language $M \mapsto \Gamma_\infty(s;M)$.

---

## Numerical profile

Using the target order parameter taken from the reference cutoff $X=10^3$ at $(s,\lambda)=(1,1)$, the recovered inverse branches at larger cutoffs decrease monotonically and the certified interval width contracts sharply. The same pattern persists for the deeper branch point $\lambda=2$.

---

## What is now exact

1. the infinite-cutoff order parameter admits a unique inverse branch;
2. finite-cutoff inverse branches converge monotonically from above to that limit;
3. the convergence comes with explicit certified interval enclosures;
4. the Legendre-dual description survives the infinite-cutoff limit.

---

## Executable artifact

- Module: `w33/cyclotomic.py`
- Analysis: `analysis/w33_completed_spectral_infinite_dual_branch.py`
- Tests: `tests/test_w33_cyclotomic.py`
- Data: `data/w33_completed_spectral_infinite_dual_branch.json`
- Result: `PART_MCXII_completed_spectral_infinite_dual_branch_results.json`
