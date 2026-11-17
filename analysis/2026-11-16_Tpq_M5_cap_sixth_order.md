# Sixth-order action at the capped M5 spectator bifurcation

The [spectator-mode calculation](2026-11-16_Tpq_M5_cap_spectator_branch.md) found a quartic sign change at \(\alpha\simeq0.917576899\). At that crossing the reduced sixth-order coefficient is positive, \(d=0.00215694742\) in the same normalization. The positive value survives a large subtraction from the complementary response. It gives a local two-parameter regime on the negative-quartic side in which the uniform and modulated caps both have a stable magnitude direction in the spectator sector and compete in action. This is a fixed-background single-brane result. [Normal graphs and CMC bifurcation](https://projecteuclid.org/journals/journal-of-differential-geometry/volume-64/issue-3/From-Constant-mean-Curvature-Hypersurfaces-to-the-Gradient-Theory-of/10.4310/jdg/1090426999.full) · [Variational reduction at a quartic sign change](https://arxiv.org/abs/1207.1966)

## Keep the third-order complementary response

Use the exact tube action of the preceding calculation and fix the phase of the critical mode \(\phi=\psi(s)\cos\theta\), with \(\langle\psi^2\rangle_s=1\). Let \(H\) be the Jacobi operator in the even-meridian, even-spectator graph sector at \(K=K_c\). The complement excludes the sole critical mode. Fixing the meridian and angular symmetries also excludes the center translations in this calculation.

The second-order correction \(\chi\) has only harmonics 0 and 2 in \(\theta\). It is already determined by the complementary variational equation at order \(a^2\). Set \(f=a\phi+a^2\chi\), expand the exact graph action to degree six, and take the cubic part \(F_3\) of the variational derivative at this graph. Its only harmonics are 1 and 3. In harmonic 1, subtract the projection onto \(\phi\) before applying the inverse. The third-order correction is \(\eta=-H_{\perp}^{-1}F_{3,\perp}\), and the reduced sixth-order coefficient is
\[
 d=[a^6] I(a\phi+a^2\chi)-\frac12
       \langle F_{3,\perp},H_\perp^{-1}F_{3,\perp}\rangle .
\]
The fourth-order graph response could enter the sixth-order action only through the order-two complementary force, which vanishes. The fifth-order response could enter only through \(H\phi=0\). They are therefore unnecessary for this coefficient. The odd action powers vanish by the exact half-period translation acting on amplitude.

The verifier constructs Taylor coefficients of the tube, volume primitive, gradient square root and their variational derivatives at the quadrature points. It recovers the separately computed quartic from the fourth action coefficient, and the critical projection of \(F_3\) equals four times that quartic. At the crossing the uncorrected sixth-order term is \(0.15734145846\), and the additional response contributes \(-0.15518451104\). Two meridian resolutions agree on their sum to better than \(10^{-11}\). Substituting \(\eta\) directly into the graph and evaluating its action coefficient also reproduces the sum. The sign remains positive at the two nearby sampled values \(\alpha=\alpha_*\pm0.002\). These checks provide numerical convergence, rather than an interval-certified bound on the root or coefficient.

## Local action ordering and index

Let \(\sigma=K-K_c\), \(b\) be the quartic coefficient on the critical curve, and \(z=a^2\). The leading action difference relative to the uniform cap is
\[
 \Delta I=\sigma z/4+bz^2+dz^3 .
\]
At \(b=0\) the small nonzero branch exists on \(\sigma<0\) with \(|a|\sim[-\sigma/(12d)]^{1/4}\). It is lower in action and has a positive magnitude direction. This fourth-root law replaces the usual square-root bifurcation at the crossing.

For small \(b<0\) with \(d>0\), two nonuniform solutions coexist with the uniform cap over the leading range \(0<\sigma<4b^2/(3d)\). The smaller one has a negative magnitude direction. The larger one has a positive magnitude direction and competes with the uniform cap, which also has positive spectator Hessian for \(\sigma>0\). They exchange action ordering at
\[
 \begin{array}{lll}
 \text{fold:}&\sigma=4b^2/(3d),&z=-b/(3d),\\
 \text{equal action:}&\sigma=b^2/d,&z=-b/(2d).
 \end{array}
\]
These are leading asymptotics as \(b\to0^-\), with \(z=O(|b|)\) and \(\sigma=O(b^2)\), so the omitted terms include \(z^4\) and \(\sigma z^2\). At the fold the two nonuniform solutions merge. At equal action the preferred saddle changes at finite amplitude for fixed nonzero \(b\). The original negative cap mode survives throughout this local reduction. Whenever the other bosonic sectors retain the gaps of the [capped probe](2026-11-16_Tpq_M5_cap_probe_index.md), the larger and uniform solutions in this coexistence range each have one negative mode, and the smaller has two. The result classifies the local geometric saddle competition. Construction at finite deformation, charge quantization of the parameters, and gravitational backreaction remain separate.

Reproduce the [certificate](../data/toe_20261116_Tpq_M5_cap_sixth_order.json) with `py -3 -B analysis/toe_20261116_Tpq_M5_cap_sixth_order.py`.
