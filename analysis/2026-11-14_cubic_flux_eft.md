# The first local curvature correction that can lift the cubic-surface moduli

The [fixed-flux cubic-surface vacua](2026-11-14_cubic_flux_moduli.md) give a complex four-dimensional family in source-free D9 Einstein–Maxwell theory. Consider local, parity-even, diffeomorphism- and gauge-invariant corrections even under \(F\mapsto-F\). Count a field strength as one derivative and a curvature as two. At first order in a Wilson coefficient the change of the reduced potential along this family is obtained by inserting the operator on the leading backgrounds, at fixed magnetic flux and with constant external scalar fields. Variations of the leading action caused by first-order backreaction vanish on these solutions. The overall conversion to five-dimensional Einstein frame uses the internal volume, which is independent of complex structure on this family.

## Four-derivative insertions are constant

The product background is \(\mathrm{AdS}_5\times M^4\), with \(M\) Kähler–Einstein, \(\mathrm{Ric}_M=\kappa g_M\), \(s=4\kappa\), and parallel \(F=f\omega\). The numbers \(f,\kappa,L\) and the internal volume \(6\pi^2/\kappa^2\) are fixed at fixed flux. Terms quadratic in Ricci or scalar curvature and algebraic terms quartic in \(F\) are therefore constant pointwise. The mixed curvature and two-field-strength contractions reduce to Ricci contractions or to the action of the curvature operator on \(\omega\), which is \(\kappa\omega\). Terms containing \(\nabla F\) vanish on the background, and a contracted double derivative of curvature integrates to zero or reduces to algebraic terms. The remaining curvature-square integral is fixed by Gauss–Bonnet and the constant Ricci data. This argument includes the external curvature contributions of the product. Hence the four-derivative operators in this class give a **constant first-order potential** on the eight real moduli. This statement uses first order in their Wilson coefficients and the given field content.

## A six-derivative contraction detects the smoothing

Use the trace of the cube of the full curvature operator on two-forms as a local six-derivative insertion. The mixed two-forms have zero curvature operator, and the external contribution is constant. For the internal Einstein block \(\mathcal R=W^+\oplus W^-+sI/12\), use norms as endomorphisms of the three-dimensional self-dual and anti-self-dual bundles. In the Kähler orientation the eigenvalues of \(W^+\) are \(s/6,-s/12,-s/12\). For the smooth cubic, \(\chi=9\) and \(\tau=-5\); volume and the signature formula give \(\int|W^+|^2=4\pi^2\) and \(\int|W^-|^2=64\pi^2\). The integrated Derdziński identity on the anti-self-dual block reads

\[
6\int \mathrm{tr}(W^-)^3 = \int |\nabla W^-|^2 + \frac{s}{2}\int |W^-|^2.
\]

Expanding the operator cube yields the exact cubic-surface identity

\[
\int_M \mathrm{tr}(\mathcal R^3)=23\pi^2s + \frac16\int_M |\nabla W^-|^2.
\]

Here \(\mathrm{tr}(\mathcal R^3)\) means the trace of the cubed endomorphism. This identity fixes the coefficient independently of the normalization used for a Riemann-index contraction in a higher-dimensional Lagrangian. [Four-dimensional Einstein curvature identities](https://pi.math.cornell.edu/~cao/3nonnegative.pdf)

The functional is nonconstant. Choose a generic smoothing of the Cayley cubic with its orbifold Kähler–Einstein metric. In the nodal gluing construction, at length scale \(\epsilon\to0\) the rescaled metric about a smoothed node converges smoothly on compact subsets to a nonflat Eguchi–Hanson metric. This follows from the preglued Eguchi–Hanson region and the small rescaled metric correction, with interior elliptic regularity. In the Kähler orientation the Ricci-flat bubble has \(W^+=0\), and its \(W^-\) is nonparallel because its curvature decays at infinity and is nonzero near the core. Pick a compact bubble region where the integral of \(|\nabla W^-|^2\) is positive. Under length scaling by \(\epsilon\), its squared curvature derivative scales as \(\epsilon^{-6}\) and its volume as \(\epsilon^4\). Thus its contribution is bounded below by a positive constant times \(\epsilon^{-2}\) for sufficiently small \(\epsilon\). Contributions outside that region are nonnegative, and the topological term stays constant. This proves variation of the smooth-family insertion and rules out an exact classical flat potential from this operator with a nonzero standalone coefficient. [Nodal Kähler–Einstein gluing](https://arxiv.org/abs/1211.5344)

The divergence is a statement about the coefficient of the perturbative insertion on the leading family. Taking the bubble curvature past the EFT cutoff invalidates quantitative use of the truncated action there. The calculation gives an admissible operator that can break the flatness, with the actual coefficient, stationary points, and their Hessians requiring further dynamics.

## The Fermat point is stationary by symmetry

At the Fermat cubic the four complex tangent coordinates correspond to the square-free monomials omitting one projective coordinate each. Independent cube-root phases act by four distinct nontrivial characters, with no character inverse to any of the four. Coordinate permutations act transitively on them. Consequently every smooth invariant potential on the moduli family has vanishing first derivative there and quadratic part proportional to \(\sum_{i=1}^{4}|z_i|^2\) in these tangent coordinates. The invariant kinetic form has the same structure. If the six-derivative Hessian is nonzero at Fermat, it gives one common squared mass to all eight real modes. Symmetry alone gives neither the magnitude nor the sign of that Hessian. [Fermat tangent slice](2026-11-14_cubic_flux_moduli.md) · [Fermat surface in the cubic moduli space](https://arxiv.org/abs/math/0007048)

Replay the coefficient and scaling checks with `py -3 analysis/toe_20261114_cubic_flux_eft.py`.
