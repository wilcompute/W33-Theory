# Part MCXI: Completed Spectral Equation of State and Legendre Duality

**Date:** 2026-05-19  
**Series:** W(3,3) Theory of Everything  
**Status:** VERIFIED INVERTIBLE EQUATION OF STATE / LEGENDRE-DUAL BRANCH

---

## Why this part exists

Part MCX showed that the completed spectral action is strictly increasing and strictly convex on the whole physical deformation branch. Once that is true, the next thermodynamic object is forced: the branch should admit a genuine equation of state and a corresponding Legendre dual description.

---

## The theorem

For fixed real $s>0$ and finite split-prime cutoff $X$, define the real order parameter of the completed spectral action by
\[
\mathcal M_X(s;\lambda)=\frac{\partial \mathcal F_X}{\partial\lambda}.
\]
Part MCX gives
\[
\chi_X(s;\lambda)=\frac{\partial^2 \mathcal F_X}{\partial\lambda^2}>0
\qquad (0<\lambda<6),
\]
so the map
\[
\lambda\longmapsto \mathcal M_X(s;\lambda)
\]
is strictly increasing on the physical branch. Hence it is injective and admits a unique inverse on its image:
\[
\lambda_X=\lambda_X(s;M).
\]
Therefore the completed spectral action has a well-defined finite-cutoff Legendre dual
\[
\Gamma_X(s;M)=\lambda_X(s;M)\,M-\mathcal F_X\bigl(s;\lambda_X(s;M)\bigr).
\]
Because $\chi_X>0$, this dual branch is unique. In particular the physical packet at any chosen $\lambda$ may be reconstructed from its order parameter alone by solving the equation of state.

At the level of executable finite-cutoff physics, the inverse is obtained by monotone bisection, and the recovered deformation agrees numerically with the original physical slice to machine precision. The same structure passes to the infinite-cutoff branch by the monotone convergence and derivative tail bounds from MCX.

---

## Reading

This is the thermodynamic completion of the completed spectral family. The packet is no longer only an odd analytic object with a convex free energy. It now has:

1. a genuine **equation of state** $M=M(s;\lambda)$;
2. a unique inverse branch $\lambda=\lambda(s;M)$;
3. a **Legendre-dual potential** describing the same physics in the conjugate variable.

So the completed spectral package now behaves like a true one-parameter thermodynamic system rather than only a decorated Euler product.

---

## Numerical profile

At the verified slice $(s,\lambda)=(1,1)$ and cutoff $X=10^6$, the order parameter determines the deformation branch uniquely; inverting the equation of state recovers $\lambda=1$ to numerical precision, and the corresponding Legendre dual value is stable. The same remains true at $\lambda=2$ and deeper on the branch.

---

## What is now exact

1. the completed spectral action has an invertible real equation of state on the physical branch;
2. the deformation parameter can be reconstructed uniquely from the order parameter;
3. the branch admits a unique Legendre-dual description;
4. finite-cutoff reconstructions converge monotonically to the infinite-cutoff branch.

---

## Executable artifact

- Module: `w33/cyclotomic.py`
- Analysis: `analysis/w33_completed_spectral_equation_of_state.py`
- Tests: `tests/test_w33_cyclotomic.py`
- Data: `data/w33_completed_spectral_equation_of_state.json`
- Result: `PART_MCXI_completed_spectral_equation_of_state_results.json`
