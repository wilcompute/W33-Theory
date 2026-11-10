# W33 nonlinear flux, exact temperature law, and a sufficient global-vacuum theorem

**Research date:** November 9, 2026 (America/New_York). **Model boundary:** finite 80-vertex W33 point–line Levi graph, 40×40 half-filled spinless fermion hopping matrix, and the explicit **all-1620-octagon** compact U(1) Wilson action. This is not a continuum limit, empirical calibration, physical gauge coupling or theory-of-everything result.

**Public executable:** analysis/w33_20261110_nonlinear_flux_public_replay.py

**Prior exact ingredients:** analysis/w33_20261109_one_edge_flux_poly_curvature.py; analysis/w33_20261109_exact_octagon_hessian_theorem.py; analysis/w33_20261109_full_u1_variational_vacuum.py. The previous exact finite Hessian identity is retained and not claimed anew.

## I. Direct 81-octagon coordinate theorem

Fix the deterministic BFS spanning-tree gauge used in the existing 81-chord solver; let W be its signed 1620×81 octagon/chord incidence matrix. Its first 81 rows form a **signed permutation matrix U**, not merely an integer-unimodular matrix:

- Each row and each column contains exactly one ±1.
- U-transpose × U = identity exactly (integer check).
- Therefore for **every** compact chord phase vector x,

\[
S_{\rm all}(x)=\sum_{c=1}^{1620}[1-\cos((Wx)_c)]
\ge \sum_{i=1}^{81}[1-\cos((Ux)_i)]
=\sum_{j=1}^{81}(1-\cos x_j).
\]

This exact nonlinear inequality supplies a control on all independent gauge coordinates by shortest Wilson loops. The only zero-action configuration is the flat gauge orbit.

## II. Fully nonlinear one-edge potential

For B_theta obtained by setting one occupied incidence-matrix entry to exp(i theta), let y=1−cos(theta) between 0 and 2, and P_theta(t)=det(I+t B_theta B_theta^dagger).

The earlier exact certificate gave

\[
P_0(t)=(1+16t)(1+6t)^{24},\qquad
P_\pi(t)-P_0(t)=324t^4(1+6t)^{22}.
\]

Each altered entry and its conjugate enters the Hermitian block determinant once, so P_theta is affine in exp(i theta)+exp(−i theta), and consequently

\[
\boxed{P_\theta(t)=P_0(t)+162t^4(1+6t)^{22}y.}
\]

For beta>0, put t_n=beta²/[pi²(2n+1)²] and a_n=162t_n⁴/[(1+16t_n)(1+6t_n)²]. With F_beta=−(2/beta) Σ log[2cosh(beta*sigma(B)/2)], the standard infinite product for cosh yields exactly

\[
\boxed{\Delta J(y)=81\kappa y-\frac2\beta\sum_{n\ge0}\log(1+a_ny).}
\]

This converges absolutely and is strictly convex in y. Define

\[
\kappa_\pi(\beta)=\frac2{81\beta}\sum_{n\ge0}\frac{a_n}{1+2a_n},
\quad
\kappa_c(\beta)=\frac2{81\beta}\sum_{n\ge0}a_n.
\]

The constrained one-edge minimizer is y=2 when κ≤κ_pi, the unique interior derivative root for κ_pi<κ<κ_c, and y=0 for κ≥κ_c.

**At beta=1:** κ_pi=0.00006194380356262749; κ_c=0.00006225567742678594. This is not a claim about global minimization of all 81 variables.

## III. All-temperature closed form and low-T dark cusp

The partial-fraction identity

\[
\frac1{w(w+16)(w+6)^2}
=\frac1{576w}-\frac1{1600(w+16)}-\frac1{900(w+6)}
-\frac1{60(w+6)^2}
\]

evaluates the Matsubara sum to

\[
\boxed{\kappa_c(\beta)=
\frac{\beta}{1152}-\frac{\tanh(2\beta)}{6400}
-\frac{\tanh(\sqrt6\,\beta/2)}{400\sqrt6}
+\frac{\beta}{1440}\operatorname{sech}^2(\sqrt6\,\beta/2).}
\]

Its small- and large-beta limits are respectively

\[
\kappa_c(\beta)=17\beta^7/40320-31\beta^9/25920+O(\beta^{11}),
\]
\[
\kappa_c(\beta)=\beta/1152-1/6400-1/(400\sqrt6)
+O(\beta e^{-\sqrt6\beta}).
\]

The positive Matsubara summands increase strictly with beta (a direct differentiation of beta⁷/[(1+c beta²)(1+d beta²)²]); thus κ_c grows strictly from zero to infinity. For each fixed finite positive κ there is **exactly one crossing** of the flat Hessian's local sign, not a proven thermodynamic phase transition.

At flat phase B has 15 zero singular values. Changing one edge to an infinitesimal nonzero phase generically lifts exactly one, with leading slope 3/8 in |theta|. The left and right zero projectors have endpoint diagonal 3/8, so the singular perturbation has size (3/8)|theta| and the zero-temperature free energy has a negative cusp of leading size −(3/8)|theta|. Magnetic action is only quadratic. This is why a fixed finite κ cannot stabilize the flat configuration at the beta→infinity limit.

## IV. Rigorous, nonperturbative global high-coupling bound

Define the 80×80 bipartite Hermitian matrix H(B)=[ [0,B],[B†,0] ], and the spectral function f_beta(lambda)=−log[2cosh(beta lambda/2)]/beta. Because f_beta''(lambda)≥−beta/4, the trace spectral divided-difference formula gives

\[
F(H_0+\Delta)-F(H_0)\ge
\operatorname{Tr}(f_\beta'(H_0)\Delta)
-\frac{\beta}{8}\|\Delta\|_F^2.
\]

At the flat incidence matrix, every occupied link has the same positive spectral-gradient coefficient

\[
s_\beta=\tanh(2\beta)/40+
\frac9{10\sqrt6}\tanh(\sqrt6\,\beta/2).
\]

In spanning-tree gauge, Δ changes only the 81 chord edges. Hence

\[
F_\beta(B(x))-F_\beta(B_0)\ge
(s_\beta-\beta/2)\sum_j(1-\cos x_j).
\]

Use the **exact signed-permutation octagon inequality** from I to conclude

\[
\boxed{J_{\beta,\kappa}(x)-J_{\beta,\kappa}(0)
\ge[\kappa-\beta/2+s_\beta]\;S_{\rm all}(x).}
\]

Thus **for κ>β/2−s_beta, flat is the unique global minimizer modulo gauge**. This is an analytic sufficient condition, not a global numerical search or an actual critical-coupling determination.

At beta=1, s_beta≈0.3331215514433542 and the **global sufficient threshold is κ>0.1668784485566458**. It is much larger than the local κ_c≈0.000062255677: the intermediate interval remains an explicitly open variational problem.

## V. Replay and limits

The executable asserts the exact 81-basis signed-permutation identity; checks nine finite complex log determinants; compares all-temperature closed form to positive Matsubara sums; tests constrained minimizer convexity; independently compares exact one-edge free energies against 40×40 SVDs; and tests the global inequality on random 81-coordinate phase vectors. The fuller local Windows experiment additionally passed six independent unit tests, but its larger tracked proof/report and JSON worktree commits remain separate from this short public replay.

**Critical boundaries:** The Wilson action used here includes all 1620 eight-cycles. The earlier TOE38 action had 1382 contractible cycles on its three-deck geometry, and the theorem above does not apply to it without change. There is no derived 3+1D continuum, Standard Model chirality, physical κ, or gravity. Ordinary Wilson-loop/maximal-tree gauge methods have substantial prior literature; for general graph background see Burbano–Bauer, JHEP (2025), https://doi.org/10.1007/jhep12(2025)060.

**Five orthogonal next tests:** sharpen the global threshold using graph-specific logdet inequalities; compute all 81-dimensional quartic anisotropies at κ_c; replace the all-octagon action by the 1382-deck-contractible one; design a phase-resolved photonic one-link spectroscopic falsifier; compare the beta⁷ law across other finite generalized quadrangles.
