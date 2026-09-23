# 2026-09-23 — Cubic Jacobian rank stratification

The signed E6 cubic tensor now answers the single-background rank question exactly.

In the canonical 81-coordinate matter gauge
\[
n=3i+a,\qquad i\in\{0,\ldots,26\},\quad a\in\mathbb F_3,
\]
the source-locked root bracket is
\[
[e_{i,a},e_{j,b}]=d_{ijk}\epsilon_{abc}\,\bar e_{k,c}.
\]
For a matter background \(v\), define
\[
D_v(x)=[v,x]:g_1\to g_2.
\]

After pairing the \(g_2\) labels with the same \((i,a)\) labels, every tested \(D_v\)
is exactly skew-symmetric and satisfies \(D_vv=0\).  Fraction-free integer
Gaussian elimination gives exact rational ranks:

| background | formula | rank | kernel |
|---|---:|---:|---:|
| root | \(e_0\) | 20 | 61 |
| uniform | \(v_n=1\) | 54 | 27 |
| linear | \(v_n=n+1\) | 54 | 27 |
| quadratic | \(v_n=(n+1)^2\) | 78 | 3 |

The immediate compiler consequence is important.  The independently proved
minimal symmetry-changing compiler must retype 54 coordinates.  A single
quadratic matter background already has cubic tangent rank 78, leaving a rank
margin of 24 above that requirement.  Therefore the nonlinear cubic interaction
is not blocked by raw tangent rank.

The equality
\[
\operatorname{rank}D_{\rm uniform}
=\operatorname{rank}D_{\rm linear}
=54
\]
with the independent 54-dimensional equivariance deficit is only a dimension
collision at this stage.  The image subspace has not yet been shown to equal
the specific Fourier-retyped target subspace.

The quadratic kernel dimension three is also suggestive in light of the
classical Vinberg order-three \(E_8\) representation \(SL_3\times E_6\) on
\(3\otimes27\), but no generic-orbit or Cartan-subspace classification is
imported into the certificate.

Evidence:
- analysis/w33_e6_cubic_jacobian_rank_stratification.py
- data/w33_e6_cubic_jacobian_rank_stratification.json
