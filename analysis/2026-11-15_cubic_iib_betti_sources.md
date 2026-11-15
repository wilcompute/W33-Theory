# Massive spin-two sources from the cubic link's RR vectors

The [six Betti vectors](2026-11-14_cubic_iib_spin.md) on the primitive Type IIB cubic link arise from the self-dual five-form, with three-form wavefunctions \(\xi_i\) proportional to \(\eta\wedge\pi^*\gamma_i\). Here \(\eta\) is the fiber one-form and \(\gamma_i\) are primitive harmonic \((1,1)\)-forms on the cubic. Their integrated kinetic term is determined by the intersection form. The pointwise inner products vary over the base and consequently source neutral massive spin-two modes at quadratic order in the gauge fields. This tests the reduction that sets the independent massive wave amplitudes to zero in the harmonic expansion. [Betti vector reduction and five-form conventions](https://arxiv.org/abs/hep-th/0601054)

## Local source and a summed overlap bound

In the convention \(\delta F_5=(1+*_{10})\sum_i f_i\wedge\xi_i\), with \(f_i\) external two-form field strengths, write \(G_{ij}(y)=\langle\xi_i,\xi_j\rangle_y\). The external Einstein equation uses \(R_{\mu\nu}=F_{\mu PQRS}F_\nu{}^{PQRS}/96\) in the pure five-form sector. Its two contributions from the displayed fluctuation have separate index types. The external Hodge identity in signature \((-++++)\) is

\[
\tfrac12(*f)_{\mu\alpha\beta}(*f)_\nu{}^{\alpha\beta}
=f_{\mu\alpha}f_\nu{}^\alpha-\tfrac12 g_{\mu\nu} f_{\alpha\beta}f^{\alpha\beta} .
\]

Thus the quadratic contribution is \(\tfrac12\sum_{ij}G_{ij} T_{\mu\nu}(f_i,f_j)\), where \(T\) is the polarization of the Maxwell stress tensor. The cross term of the background five-form with a second-order five-form fluctuation has only a pure external trace in this projection because the background carries five external or five internal indices. Hence the internal profile of this transverse-traceless source is the scalar function \(G_{ij}(y)\), independent of fiber angle. Its nonconstant component expands into the neutral massive spin-two wavefunctions. Maxwell stresses have nonzero external transverse-traceless projections for suitable field configurations, so a nonzero overlap is a source for the corresponding mode in the field equations.

Choose a real orthonormal gauge basis using the averaged internal kinetic pairing, so \(\int_Y G\,d\mu=I_6\) for probability volume measure \(d\mu\). Pointwise, \(G\) is positive semidefinite with rank at most three because primitive \((1,1)\)-forms on a Kähler surface are anti-self-dual. For a complete real neutral scalar eigenbasis \(Y_j\) with \(Y_0=1\), set \(C_j=\int G Y_j\,d\mu\). Parseval and the rank bound give

\[
\sum_{j>0}\|C_j\|_{\mathrm F}^2
=\int_Y\|G-I_6\|_{\mathrm F}^2\,d\mu
\ge \frac{(\int_Y\mathrm{tr}G\,d\mu)^2}{3}-6=6.
\]

The sphere average of \((u^T(G-I)u)^2\) over unit vectors in \(\mathbb R^6\) is \(((\mathrm{tr}(G-I))^2+2\|G-I\|_{\mathrm F}^2)/48\). Thus at least one unit gauge direction has a diagonal profile whose massive part has RMS at least \(1/2\) in this normalization. These are overlap bounds. They leave the location of the spectral weight open.

## Every individual gauge direction has a massive overlap

Suppose a nonzero primitive harmonic form \(\gamma\) had constant pointwise norm. After rescaling to norm \(\sqrt2\), the closed anti-self-dual form would be an almost Kähler form for the same Riemannian metric with opposite orientation. The cubic's metric is positive Einstein, so Sekigawa's theorem makes this second almost Kähler structure Kähler and the form parallel. The original Kähler form is also parallel. The two orthogonal complex structures commute, and their product is a parallel involution with two rank-two eigenspaces. The smooth cubic is simply connected and complete, so the de Rham splitting gives a product of two positive Einstein surfaces, each a round two-sphere. Its second Betti number would be two, whereas the cubic's is seven. Thus every nonzero \(\gamma\) has nonconstant norm, and every individual Betti direction has a nonzero massive neutral spin-two source. [Sekigawa's nonnegative Einstein rigidity theorem](https://doi.org/10.2969/JMSJ/03940677)

The obstruction applies to setting the massive harmonics to zero while keeping arbitrary retained Maxwell fields. A nonlinear uplift with prescribed massive profiles or a five-dimensional effective action obtained by integrating out the massive tower requires additional analysis. Consistent truncations built from other Sasaki–Einstein fields have their own nonlinear ansätze. [Consistent Sasaki–Einstein truncations](https://arxiv.org/abs/1003.4283)

Replay the full five-dimensional Hodge contraction and the algebraic rank-bound control with `py -3 analysis/toe_20261115_cubic_iib_betti_sources.py`.
