# Einstein-frame flux radius classifier — exact extension and topology guard

**Date:** 2026-11-14. **Status:** exact conditional dimensional-reduction calculation; not an ExFT vacuum, a new physical principle, or a TOE solution.

## Why this was checked

The live repository's E6 section analysis, \`analysis/toe_20261114_E6_flux_shape_volume_runaway_nogo.py\`, has a nonzero quantized three-form flux on a fixed-shape flat four-torus. It optimizes a *shape* parameter but yields no stabilized *overall radius*. This note generalizes the radius scaling to arbitrary external dimension \(d>2\), internal dimension \(n\ge2\), and internal form degrees \(1\le p\le n\). It must not be conflated with an E6 ExFT solution of the section constraint or with a fully consistent compactification.

## Exact derivation

Use \(D=d+n\), and an unwarped metric \(ds_D^2=g_{\mu\nu}dx^\mu dx^\nu+R^2 h_{mn}dy^m dy^n\) with unit-volume fixed \(h\). A quantized internal \(p\)-form contributes \(A_p R^{n-2p}\) to the \(d\)-dimensional pre-Einstein-frame action. The rescaling \(g^E_{\mu\nu}=R^{2n/(d-2)}g_{\mu\nu}\) adds \(R^{-dn/(d-2)}\). Therefore

\[
V_p(R)=A_pR^{-a_p},\qquad a_p=2p+\frac{2n}{d-2},\quad A_p>0.
\]

For **any finite collection of positive internal flux kinetic energies**, \(dV/d\log R=-\sum_p a_p A_p R^{-a_p}<0\). No positive finite-radius critical point exists in this truncation, even after optimizing independent shape moduli while maintaining positive flux energy.

The previous \(d=5,n=4,p=3\) computation is recovered without fitting: \(n-2p=-2\), Einstein rescaling exponent \(-20/3\), and \(V(R)=AR^{-26/3}\).

## What would actually compete?

A *hypothetical* internal positive-scalar-curvature term, when meaningful for a specified internal manifold, has the opposite sign:

\[
V_{\rm curv}(R)=-BR^{-c},\qquad c=2+\frac{2n}{d-2},\quad B>0.
\]

For one flux of degree \(p>1\), \(a_p>c\). The radial potential \(V=AR^{-a_p}-BR^{-c}\) has exactly one critical radius:

\[
R_*^{a_p-c}=\frac{a_p A}{cB},\qquad
\frac{d^2V}{d(\log R)^2}\bigg|_*=
a_p(a_p-c)A R_*^{-a_p}>0,
\]
\[
V_*=\left(1-\frac{a_p}{c}\right)A R_*^{-a_p}<0.
\]

This is a **stable radial AdS extremum in the toy potential**, not a claim about other moduli or the ten-/eleven-dimensional field equations. For the \(d=5,n=4,p=3\) exponent pair, \(a=26/3\), \(c=14/3\), and \(R_*^4=13A/(7B)\). If \(p=1\), the powers coincide and there is no isolated radial minimum.

For multiple higher-form fluxes \(p>1\), positivity and monotonicity of \(\sum_p a_p A_p R^{-(a_p-c)}\) give precisely one stable radial AdS extremum whenever a genuine positive curvature coefficient dominates any degree-one terms. The numerical or algebraic value of that radius depends on assumed amplitudes, not on W33 alone.

## The topology firewall

The established \(T^4\) construction is **flat** and has zero curvature contribution. One cannot add \(-BR^{-c}\) while silently keeping that flat metric. More strongly, a smooth torus has no metric with scalar curvature strictly positive everywhere (Gromov–Lawson, enlargeability; Schoen–Yau). This is **not** a theorem that its integrated scalar curvature can never be positive for an arbitrary sign-changing metric. To use curvature balancing one must specify a different internal geometry, its nontrivial flux cohomology, shape response, backreaction, equations of motion, and quantization/tadpole conditions.

Even a radial AdS minimum does **not** establish a self-contained vacuum, dimensional reduction, or TOE. It identifies the missing competition in this particular toy model.

## Reproducibility and sources

- Producer: \`analysis/toe_20261114_general_flux_curvature_radius_classifier.py\`
- Regressions: \`tests/test_toe_20261114_general_flux_curvature_radius_classifier.py\`
- Certificate: \`data/toe_20261114_general_flux_curvature_radius_classifier.json\`
- Project antecedent: \`analysis/toe_20261114_E6_flux_shape_volume_runaway_nogo.py\`
- Baguet, Hohm, Samtleben, *E6 Exceptional Field Theory: Review and Embedding of Type IIB*: https://arxiv.org/abs/1506.01065
- Maldacena and Núñez, *Supergravity description... and a no-go theorem*: https://arxiv.org/abs/hep-th/0007018
- Gromov and Lawson, *Spin and Scalar Curvature in the Presence of a Fundamental Group I*: https://www.ihes.fr/~gromov/wp-content/uploads/2018/08/826.pdf

**Next physics gate:** replace the conditional curvature term by a genuine E6-compatible source/coset compactification with a signed full moduli Hessian and enforced gauge constraints.