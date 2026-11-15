# Quartic magnetic terms restore a static D9 shape response

The earlier [D9 radion calculation](2026-11-14_d9_radion_response.md) found that a homogeneous mass source for the spin-two mode with equal angular degrees on both spheres shifts their log-radii equally. Here the higher-dimensional Einstein term is retained, the magnetic charges are held fixed, and the Maxwell potential is corrected by the two quartic magnetic invariants. This tests the robustness of that static result within the product ansatz. Four-field-strength operators arise in gauge-field effective actions. Their coefficients in this D9 model are free inputs. [Example four-photon effective action](https://arxiv.org/abs/1707.08106) · [Einstein–Maxwell compactifications on products](https://arxiv.org/abs/1310.6360)

Use units with the sum of the unperturbed inverse squared radii equal to one and put \(\delta=A-B\) in those units. Let \(u\) be the common log-radius displacement and \(v\) the half difference. The two squared magnetic flux densities are \(X=(7/5+\delta)e^{-4(u+v)}\) and \(Y=(7/5-\delta)e^{-4(u-v)}\). Add \(e^{-8u/3}[\alpha(X+Y)^2+\beta(X^2+Y^2)]\) to the homogeneous potential. The invariants descend from \((F_{MN}F^{MN})^2\) and \(\operatorname{tr}F^4\) with their overall factors absorbed into \(\alpha,\beta\). The positive unperturbed Hessian gives a unique nearby stationary point for sufficiently small coefficients. Its shift from the uncorrected shape, to first order, is

\[
v_1=\frac{4\delta}{15(21-5\delta^2)}\left[49\alpha+(147-50\delta^2)\beta\right].
\]

## Exact reduction of the sourced problem

For common angular eigenvalue \(n=\ell(\ell+1)\), adding the specified mass source \(Jm_{\rm KK}^2\) multiplies the internal curvature term by \(k=1-Jn/2\). For \(k>0\), shift \(u=U-\tfrac12\log k\). The curvature and quadratic magnetic terms now both carry the common factor \(k^{10/3}\), while the quartic term carries \(k^{16/3}\). Consequently the sourced stationary shape is exactly the unsourced stationary shape at **rescaled coefficients** \((k^2\alpha,k^2\beta)\) on the same nearby branch. The static source derivative of the corrected shape at \(J=0\) is therefore \(-nv_1+O((|\alpha|+|\beta|)^2)\).

At equal flux the exchange symmetry gives \(v=0\) along the local branch. For unequal flux, either quartic term alone gives a nonzero first-order static response. Cancellation at an individual asymmetric point requires \(49\alpha+(147-50\delta^2)\beta=0\). The coefficient ratio varies with the flux asymmetry, so no fixed nonzero quartic combination preserves the cancellation to first order across the whole unequal-flux branch. For example, at \(\delta=3/5,\ \ell=1,\ \beta=0\), the shape derivative is \(-49\alpha/60+O(\alpha^2)\).

This calculation includes the displacement of the magnetic vacuum before differentiating in the source. It concerns a homogeneous source for the internal derivative mass term. A physical scattering calculation also requires the derivative, curvature, and flux vertices. Higher-curvature corrections modify the graviton operator and need a separate calculation.

Replay with `py -3 analysis/toe_20261114_d9_quartic_flux.py`.
