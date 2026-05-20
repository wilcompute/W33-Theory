# Part MCXIII: Completed Spectral Dual Stiffness and Reciprocal Susceptibility

**Date:** 2026-05-19  
**Series:** W(3,3) Theory of Everything  
**Status:** VERIFIED DUAL CURVATURE / CERTIFIED INFINITE-CUTOFF STIFFNESS ENCLOSURES

---

## Why this part exists

Part MCXII showed that the completed spectral packet has a genuine infinite-cutoff equation of state
and a limiting Legendre-dual branch. The next natural question is whether the **curvature of that dual
branch** is also under control.

---

## The theorem

For fixed real $s>0$ and finite cutoff $X$, let
\[
\mathcal F_X(s;\lambda)=-\log\Lambda_X^{\mathrm{def}}(s;\lambda),
\qquad
\mathcal M_X(s;\lambda)=\frac{\partial \mathcal F_X}{\partial\lambda},
\]
and let $\lambda_X(s;M)$ be the inverse branch from MCXI. Then the Legendre-dual potential
\[
\Gamma_X(s;M)=\lambda_X(s;M)\,M-\mathcal F_X\bigl(s;\lambda_X(s;M)\bigr)
\]
satisfies the exact derivative identities
\[
\boxed{\frac{\partial \Gamma_X}{\partial M}=\lambda_X(s;M)},
\qquad
\boxed{\frac{\partial^2 \Gamma_X}{\partial M^2}=\frac{d\lambda_X}{dM}=\frac{1}{\chi_X\bigl(s;\lambda_X(s;M)\bigr)}},
\]
where
\[
\chi_X(s;\lambda)=\frac{\partial^2 \mathcal F_X}{\partial\lambda^2}
\]
is the primal Hessian / susceptibility.

So the dual branch is automatically **strictly convex**, and its curvature is the exact reciprocal of the
primal susceptibility.

Now fix a compact physical branch interval $0\le \lambda\le \rho<6$ and a target value $M$ in the common
image. If MCXII gives the inverse enclosure
\[
\lambda_-(X;M)\le \lambda_\infty(s;M)\le \lambda_+(X;M),
\]
and if $H_X(\rho)$ is the compact-disk Hessian tail bound, then monotonicity of the Hessian yields
\[
\chi_X\bigl(s;\lambda_-(X;M)\bigr)
\le
\chi_\infty\bigl(s;\lambda_\infty(s;M)\bigr)
\le
\chi_X\bigl(s;\lambda_+(X;M)\bigr)+H_X(\rho).
\]
Hence the infinite-cutoff dual stiffness
\[
\Upsilon_\infty(s;M)=\frac{d\lambda_\infty}{dM}=\Gamma_\infty''(s;M)
\]
admits the certified enclosure
\[
\boxed{
\frac{1}{\chi_X\bigl(s;\lambda_+(X;M)\bigr)+H_X(\rho)}
\le
\Upsilon_\infty(s;M)
\le
\frac{1}{\chi_X\bigl(s;\lambda_-(X;M)\bigr)}.
}
\]

---

## Reading

This means the dual thermodynamic branch is not merely present. Its **curvature** is explicitly known.
The deformation branch and the response branch now control one another quantitatively:

1. large primal susceptibility means a soft dual branch;
2. small primal susceptibility means a stiff dual branch;
3. the infinite-cutoff stiffness can be fenced in by explicit finite-cutoff bounds.

So the completed spectral packet now has a controlled thermodynamic geometry on **both** sides of the
Legendre transform.

---

## Numerical profile

For the target order parameter taken from the reference cutoff $X=10^3$ at $(s,\lambda)=(1,1)$, the
recovered finite-cutoff dual stiffness at $X=10^5$ is positive and lies inside the certified infinite-cutoff
stiffness interval. The interval contracts as the split-prime cutoff grows, and the same behavior persists
for the deeper branch target taken from $\lambda=2$.

---

## What is now exact

1. the dual curvature is exactly the reciprocal of the primal susceptibility;
2. the dual branch is strictly convex on the physical response range;
3. the infinite-cutoff dual stiffness exists on the common branch and admits certified finite-cutoff enclosures;
4. both the primal and dual thermodynamic geometries are now quantitatively controlled.

---

## Executable artifact

- Module: `w33/cyclotomic.py`
- Analysis: `analysis/w33_completed_spectral_dual_stiffness.py`
- Tests: `tests/test_w33_cyclotomic.py`
- Data: `data/w33_completed_spectral_dual_stiffness.json`
- Result: `PART_MCXIII_completed_spectral_dual_stiffness_results.json`