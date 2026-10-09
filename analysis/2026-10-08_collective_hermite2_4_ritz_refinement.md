# 2026-10-08 — Five-state collective Hermite Ritz refinement (independent recalculation)

**Scope:** This is a stronger variational *upper* bound for the proposed Pass11769 W33 current-square Hamiltonian, not a computed spectrum, an attained vacuum or a physical energy prediction. Pass11775 owns the prior three-state result.

## Construction

Let \(\psi\) be the optimized Gaussian of Pass11769. For each W33 point \(i\), form its 15-kernel direction \(w_i\in\mathbb Z^{40}\) with components \(9\) at \(i\), \(-3\) at its 12 neighbors and \(1\) at its 27 nonneighbors; analogously form the 40 line-side directions. Let \(Y_i=w_i\cdot q/\sqrt{108t}\), where \(t\) is the Pass11769 Gaussian scale. The five mutually orthogonal normalized states are:

1. \(\psi\);
2. the sum of all point-side probabilists' \(\mathrm{He}_2(Y_i)\psi\);
3. the corresponding line-side sum;
4. the sum of all point-side \(\mathrm{He}_4(Y_i)\psi\);
5. the corresponding line-side sum.

For degree \(n\), divide the sum by \(\sqrt{n!\,N_n}\), where
\[
N_n=40\big(1+12(-1/3)^n+27(1/9)^n\big).
\]
Thus \(N_2=320/3\), \(N_4=11200/243\). Hermite chaos orthogonality and the independence of the point and line 15-mode kernel factors make the five-state Gram matrix exactly \(I_5\). No point-line *geometric* isomorphism is assumed.

## Exact orbit reduction; numerical matrix elements

The underlying 40-by-40 incidence matrix is obtained afresh from the symplectic \(\mathbb F_3^4\) construction: 40 points, 40 isotropic four-point lines, 160 incidences. The point collinearity and line-intersection graphs each have degree 12; each \(w_i\) lies in its proper 15-dimensional incidence kernel. The 4800 ordered pairs of point–point, line–line and point–line labels reduce to eight types: three point–point, three line–line, and incident/nonincident point–line.

For any representative pair \(w_i,w_j\), the currents act on a Hermite state through
\[
J_e[\mathrm{He}_n(Y)\psi]
=(x+a)\big[(fx+a+iz)\mathrm{He}_n(Y)
 - i r\,n\mathrm{He}_{n-1}(Y)/\sqrt{108t}\big]\psi,
\]
with the sign-adjusted coefficient \(r=\pm w_i(\mathrm{endpoint}(e))\), \(x=V_eq\), and \(z\) the independent Gaussian momentum coordinate. Four-variate Gaussian covariance matrices and weighted edge-incidence counts determine every pair matrix element. These integrands have degree at most 12, hence both 7- and 8-node tensor Gauss–Hermite rules are degree-exact in ideal arithmetic.

The resulting Ritz values are:

| Trial subspace | Upper bound |
|---|---:|
| Gaussian only, Pass11769 | 128.887391415527 |
| Gaussian + collective point/line fourth Hermites, Pass11775 | 127.619509072726 |
| **Add collective point/line second Hermites** | **127.619377843339** |

The extended basis gains **0.000131229387** relative to the Pass11775 three-state trial. Independently evaluated 7- and 8-node quadrature blocks differ by at most \(2.85\times10^{-14}\), and the resulting minimum agrees to approximately \(3\times10^{-14}\). This is a floating-point comparison of degree-exact formulae, **not** a rigorous outward-rounded interval at all shown digits.

## Physics boundary

The collective second-Hermite modes have vanishing matrix element with the centered optimized Gaussian by stationarity, but couple to the fourth-Hermite modes and lower the Ritz eigenvalue. This demonstrates a higher-chaos correlation beyond the three-state trial. It does **not** determine a positive gap above the actual spectral infimum or show any mass/coupling/continuum prediction. A numerical lower-bound method and a compactness/ground-state argument remain essential.

Other independent frontiers from this pass are recorded separately; this is the quantitatively verified vacuum refinement.
