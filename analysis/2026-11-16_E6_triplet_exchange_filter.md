# Tree-level color-triplet exchange in the \(E_6\) Yukawa candidate

The [charged-Yukawa construction](2026-11-16_E6_adjoint_Yukawa_and_messengers.md) has independent up, down and charged-lepton matrices once the required adjoint insertions are added. The associated heavy spectator \(K+\bar K\) also mediates baryon-violating dimension-five superpotential terms in the original choice of couplings. Both signed triplet weights contribute. A quadratic adjoint polynomial on the up-type Higgs leg removes the two dangerous blocks without changing the light Yukawa maps. The result is for the specified tree-level superpotential with the neutral spectator masses turned on. [Proton decay in supersymmetric \(E_6\) model building](https://arxiv.org/abs/1504.00904) · [Adjoint-based suppression in a different GUT](https://arxiv.org/abs/hep-ph/9306242)

## Resolve the exchange before modifying it

Use the integer-weight convention \(Y_{\rm SM}=-Y/6\). The heavy spectator mass on coordinate \(h\) is \(Y_h+3\) in the reference units. Define the light matter coordinates by the kernel of the rank-ten mass from \(H_1=e_7\), removing its two neutral components by the optional neutral mass terms. The up-type source \(J_h\) is the cubic of two light fields with \(K_h\). The down source \(\bar J_h\) is the cubic of two light fields with the image of \(\bar K_h\) under \(d^*(\bar K,\bar H_1)\). At nonzero \(Y_h+3\), tree elimination gives
\[
 W_{XX\,XX}=-\sum_h\frac{J_h\bar J_h}{Y_h+3}.
\]
Coordinates of weight \(-3\) comprise the light weak doublet and are excluded from this elimination.

The certificate enumerates the original cubic monomials and dual signs before assigning either source. On the remaining shared heavy supports, the two weights \(Y_h=\pm2\) give both \(QQQL\) and \(U^cU^cD^cE^c\) terms. The signed blocks arise from distinct pairings of the light source bilinears. For example, retaining the two family blocks separately gives nonzero coefficients \(-1/5\) and \(+1/5\) for the respective operator types in the \(+2\) sector, and \(-1\) for a \(QQQL\) term in the \(-2\) sector, in the certificate's component normalization. Terms from the two signed weights therefore cannot be assumed to cancel generically. The shared heavy weak-doublet weight \(+3\) carries only baryon-conserving exchanges. The earlier adjoint flavor operators on matter legs multiply these same nonzero tensor entries by weight factors and leave the support classification intact.

## A Higgs-leg polynomial

In every up-type cubic contraction replace \(K\) by
\[
 F(\Phi)K,\qquad F(t)=(t^2-4)/5
\]
in the normalization where the adjoint VEV is \(Y\). This is \(E_6\)-covariant because the adjoint acts on the \(\mathbf{27}\). It has \(F(-3)=1\) on the light up doublet and \(F(\pm2)=0\) on both exchanged triplets. It leaves the spectator mass term and the down-type insertions intact. Thus the independent charged-Yukawa maps survive with the same light coefficients while every baryon-violating term in the displayed spectator exchange vanishes. A single affine polynomial cannot implement these three evaluations. This minimality is only for one polynomial on the up-type spectator Higgs leg, rather than a classification of all possible suppression mechanisms.

Two additional vectorlike \(\mathbf{27}\) pairs \(P,\bar P,Q',\bar Q'\) can generate the filter using renormalizable mass and adjoint couplings. In common mass units choose multiplier terms \(\bar P(P-\Phi K)+\bar Q'(Q'-\Phi P)\), and replace \(K\) in the up-type cubic vertices by \((Q'-4K)/5\). Eliminating the pairs gives \(F(\Phi)K\). They have zero VEV and do not change the earlier Higgs vacuum equations. This is another chosen superpotential relation; an underlying symmetry or ultraviolet origin for its coefficients remains open.

## Other tree sources in the chosen light-field model

At zero light Higgs and matter VEVs, the cubic exotic mass coupling \(d(X,X,H_1)\) can source charged \(H_1\) fluctuations with two light fields. In the gauge slice \([\delta\Phi,Y]=0\), the charged heavy \(H_a,\bar H_a\) Hessian comes from \(\bar H_a\Phi^2H_a\). It is an off-diagonal vectorlike mass \(Y_h^2\) in each nonzero weight. The Gram and adjoint blocks do not mix into it. The chosen operators give no charged \(\bar H_a\) source bilinear in the light matter. The optional neutral-mass operators have zero first variation on two charged light fields, and the down operator's source at two light matter fields is on \(\bar K\), since \(\bar K=0\) at the vacuum. Consequently the charged \(H+\bar H\) exchange needs a source on each side, and contributes no four-matter superpotential term here. A neutral Higgs source cannot contain a pair of light charged matter fields, because none of their integer weights occur in opposite pairs. The explicit Yukawa and filter messengers can be eliminated first by their holomorphic equations, returning precisely the effective superpotential used in this check.

This establishes a tree-level zero for the specified four-light-matter superpotential channel with the filter. The auxiliary construction assumes the chosen operators and tree kinetic regime. It does not constrain every higher-dimensional contact term allowed by the symmetry.

## An independent gauge-mediated channel remains

With canonical Higgs and adjoint kinetic terms in the reduced model, the full complex adjoint block of integer charge \(+5\) has dimension six. Exact cubic-derivation elimination shows that all its generators annihilate both stabilizing Higgs vectors and their duals. Their masses therefore come entirely from the adjoint, with \(m_X^2/(g^2v_Y^2)=25\) in a kinetic convention with adjoint mass operator \(g^2v_Y^2\operatorname{ad}_{Y}^{\dagger}\operatorname{ad}_{Y}\). Here \(\langle\Phi\rangle=v_Y Y\) before the mass units are factored out. The conjugate generators carry charge \(-5\).

The inverse trace Gram matrix of the exact charge-five generators gives a nonzero contraction between the light currents \(Q^\dagger E^c\) and \((U^c)^\dagger Q\). Pairing the first current with the conjugate of the second generates a baryon-violating dimension-six interaction after the gauge boson is eliminated. The verifier computes the contraction in the entire charge-five gauge block, so it includes interference between its generators. The adjoint filter affects the holomorphic Higgs vertices and leaves this gauge-current channel present. The quoted mass and contraction use the reduced model's canonical metric. The explicit heavy-field completion can add kinetic and mass contributions, and a proton lifetime would also require flavor rotation, running and low-energy matrix elements. [Gauge- and Higgs-mediated proton decay in supersymmetric \(E_6\)](https://arxiv.org/abs/1504.00904)

Reproduce the [exact exchange certificate](../data/toe_20261116_E6_triplet_exchange_filter.json) with `py -3 -B analysis/toe_20261116_E6_triplet_exchange_filter.py`.
