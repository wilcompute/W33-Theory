# The two W33 mass phases on Standard Model bundles and monopoles

The heavy adjoint and triplet phases have different responses before electroweak breaking and identical responses after it. For the canonical primitive monopole, each full phase winding shifts the electric character by a weight of electromagnetic charge −1. The two shifts differ by a character that is trivial on the electroweak stabilizer. This extends the relative QCD match to the faithful Standard Model quotient and its dyonic labels. [Canonical global group](2026-11-10_global_gauge_topology.md) · [Colored threshold calculation](2026-11-13_canonical_strong_cp.md)

## Spin bundles and angle periods

Write the faithful gauge group as `H=S(U(3)×U(2))`. An H bundle is a pair of bundles E3 and E2 with a trivialization of their product determinant. Set `c=c1(E3)=−c1(E2)`, `n3=−∫c2(E3)`, `n2=−∫c2(E2)), and `k=∫c²/2`. On closed spin four-manifolds k is integral by the Wu formula.

Use the positive Chern–Weil convention of the parent calculation. For the Abelian factor use integer charges `6Y` and normalize its topological charge as half the square of its flux class. The Abelian flux class is `−c/6` in the rational covering chart. Removing the trace from the U(3) and U(2) curvatures gives

```text
Q3 = n3 + 2k/3
Q2 = n2 + k/2
QY = k/36.
```

Unit liftable instantons on S⁴ realize the individual n3 and n2 directions. On S²×S² take a line bundle L with `c1(L)=x+y`, where x and y generate the two factors, and take `E3=L⊕1⊕1`, `E2=L⁻¹⊕1`. This realizes `(n3,n2,k)=(0,0,1)`. These witnesses make the period conditions necessary as well as sufficient for the three continuous gauge terms. In `(θ3,θ2,θY)`, the shifts in 2π units have generators `(1,0,−24)`, `(0,1,−18)`, and `(0,0,36)`. This is the spin-bundle calculation for the stated normalization. [Standard Model line operators and angle periods](https://arxiv.org/abs/1705.01853) · [Dyonic derivation and axion context](https://arxiv.org/abs/2606.20319)

The canonical color and weak coroots both have squared norm two in the parent basic form. In the five-block the generator 6Y has squared norm 30. Thus the parent E6 term restricts to `Q3+Q2+30QY=n3+n2+2k`. The family factor is trivial on this stabilizer. The parent column below can be varied around a full circle using the simultaneous 2π parent angle shift. [Faithful parent angle lattice](2026-11-12_parent_theta_lattice.md)

## The threshold responses

The phase of the adjoint trace polynomial multiplies one color octet and one weak triplet of chiral fermions. Both have zero hypercharge. The weak weights with nonzero weak Cartan charge in the varying Hessian are exactly the pair of weak roots, with nonzero mass and no accompanying colored weights. The triplet-splitting determinant has winding three in the vectorlike `(3,1)_{−1/3}` representation, which is the E3 fundamental. A Dirac pair in this representation gives unit color angle and `3·(−2)²=12` units of the integer-hypercharge angle. The three phase directions therefore have the following coefficients per radian.

| Phase | Coefficients of `(Q3,Q2,QY)` | Coefficients of `(n3,n2,k)` |
| --- | --- | --- |
| Adjoint `arg z_A` | (3, 2, 0) | (3, 2, 3) |
| Triplet `arg z_T` | (3, 0, 36) | (3, 0, 3) |
| Parent E6 | (1, 1, 30) | (1, 1, 2) |

The two heavy columns have Smith factors (1,6). Their gauge topological image has two continuous angles and the map from the two phase circles has a six-element kernel. Adding the parent direction gives Smith factors (1,1,6), so these three phases can vary all three continuous topological weights in the Higgs phase. This statement concerns their gauge topological terms at fixed other sources. The adjoint and triplet responses differ by exactly `2n2`. The pure determinant-flux witness has index three for either heavy phase.

A neutral down- or up-Higgs VEV reduces E2 to a line plus a trivial line, so n2 vanishes on bundles with this reduction. The responses then coincide. With the physical electric generator `Q=Y+T3`, the Abelian photon coefficient is `2·(1/2)=1` for the adjoint and `36·(1/6)²=1` for the triplet. The common color coefficient is three. If either phase were promoted to an axion, the heavy-sector anomaly ratio in the conventional `E/N` normalization would be `2/3`. This ratio concerns the given heavy fermions. A dynamical axion, its potential and other charged contributions remain to be supplied.

## Witten relabeling of the primitive monopole

Use the canonical five-block cocharacter `m=(1,0,0,−1,0)`. A full winding of a heavy phase changes the canonical electric label by the bilinear trace pairing of its topological term with m, in the convention that increasing theta shifts the canonical label positively at fixed kinetic charge. On the diagonal torus electric characters are integer five-vectors modulo the all-ones vector. The two shifts are

```text
λ_A = (2,−1,−1,−1,1)
λ_T = (3, 0, 0, 0,0).
```

Their second and third entries agree, so these are characters of the full residual centralizer of m, including its U(2) block. Each gives electric charge −1 under `Q=diag(−1/3,−1/3,−1/3,1,0)`. Their difference modulo the trivial character is twice the fifth diagonal character. It is trivial on the electroweak stabilizer, where the neutral Higgs fixes the fifth component. The parent phase gives the one-root step m, as in the rotor calculation.

Both heavy shifts evaluate to `3/2` on the lift generator `m/2`. They are odd under its endpoint `κ=exp(iπm)`. The full electric relabeling therefore changes the kernel-character sector in the framed rotor description. This is an asymptotic charge result. The fermionic spectral flow in the smooth core and the physical realization of the relabeling require a separate calculation. [W33 monopole phase and endpoint](2026-11-11_monopole_electric_phase.md) · [Witten effect](https://doi.org/10.1016/0370-2693%2879%2990838-4)

Run `python analysis/toe_20261113_sm_threshold_theta.py` from the repository root. [Exact output](../data/toe_20261113_sm_threshold_theta.json)
