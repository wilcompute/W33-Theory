# 2026-09-17 — execute-all-five: affine control, FI vacuum, determinant depth, decoder distance, dark-15 bridge

Status: **five-front closure with explicit physical boundaries**.

This packet integrates the live W33 and Holotrade results produced around the same frontier.  It distinguishes exact finite/representation-theoretic statements from control assumptions and unresolved heterotic vacuum dynamics.

## 1. A8^3 affine return descendants give conditional sl(729) controllability

The certified twisted ground register is `9 x 9 x 9 = 729`, with local current algebra `sl9^3`.  A glue generator such as `(1,1,4)` has nonzero components in all three A8 factors.  In the free-boson lattice-VOA return OPE `V_lambda V_-lambda`, the quadratic descendant contains `(J_lambda)^2/2`, hence nonzero pairwise cross terms `H_i tensor H_j` on a connected three-block graph.

Under the explicit control assumption that the local `sl9` zero modes and at least one such nonzero return-OPE cross Hamiltonian on each edge of a connected block graph are independently addressable with continuously tunable real coefficients, simplicity of `sl9` gives

`sl9 tensor sl9`

on an edge.  Adding the local summands gives `sl81`, and induction across the third block gives

\[
\boxed{\mathfrak{sl}_{729}},\qquad \dim=729^2-1=531440.
\]

This is a mathematical controllability theorem, not a hardware universality certificate.  The repository certifies the operator algebra, not independent physical drive, switching, leakage control or pulse synthesis.

Artifacts:
- `analysis/w33_a8cubed_affine_return_universality.py`
- `data/w33_a8cubed_affine_return_universality.json`

## 2. FI cancellation and exotic lifting are charge-compatible, but rank is a vacuum-profile question

Holotrade now fixes the anomalous direction for the frozen SU(5) witness:

\[
\operatorname{Tr}Q_A=-72,
\]

with two minimal FI-cancelling untwisted bilinears `U0 U1` and `U2 U3`, each of total `Q_A=+2`.  Those are exactly the untwisted singlet pairs entering the sextic exotic-mass operators, so there is no charge-level incompatibility between FI cancellation and the higher-order exotic channels.

A parallel fixed-point audit corrects the earlier interpretation of the rank-nine benchmark.  The nine exotic rows are fixed-point labels `f in F3^2`, and the matrix factorizes through four twisted-singlet pair profiles,

\[
M(f,c)=\sum_s A_s(f)B_s(c).
\]

Consequently:

- translation-invariant twisted VEVs give rank `1`;
- one fixed point per twisted type gives rank at most `4`;
- the diagonal fixed-point profile used by the degree-12 quartic cube gives rank `1`;
- rank `9` is reachable from support size `2`, and becomes robust in the sampled generic profiles by support size `4`.

Thus full exotic decoupling is a statement about the **D/F-flat vacuum profile**, not generic unconstrained coupling coefficients.  The Vandermonde matrix remains an algebraic existence witness in free coefficient space, but not a physical-vacuum certificate.

The same witness has 16 neutral `U*T0*T1*T2` rays protected through order 11. Their degree-12 cubes pass the currently implemented space-group, R-charge, Rule-4 and Rule-5 tests; hence they are not all-order flat.

Holotrade artifacts:
- `analysis/w33_su5_fi_degree12_flatness.py`
- `data/w33_su5_fi_degree12_flatness.json`
- `analysis/the_exotic_mass_rank_is_set_by_where_the_singlets_condense.py`
- `data/w33_exotic_mass_rank_by_condensate.json`
- `analysis/w33_fi_exotic_condensate_compatibility.py`
- `data/w33_fi_exotic_condensate_compatibility.json`

## 3. Determinant magic has exact minimal operator depth two

The ten global cubic holonomy variables form the adjoint `sp4(F3)`, whose first genuinely new pointwise nonlinear invariant is quartic `det X`.  One synchronized A8^3 weight-two operator carries only three Pauli directions, and the complete equivariant moment-map space forces rank at most three, so `det X=0` identically at depth one.

Depth two is sufficient.  Take two copies of the weight-two glue sector

\[
c=(1,1,4),
\]

which fuse to `2c=(2,2,8)`, again a synchronized weight-two sector with central character `r=2`.  Choose Pauli labels `(e1,e2,e3)` and `(e4,0,0)`.  Their summed diagonal moment map has

\[
S=I_4,\qquad X=SJ=J,\qquad \det X=1\pmod 3.
\]

Hence the finite fusion/equivariant layer permits the nontrivial candidate phase

\[
\omega^{r\det X}=\omega^2.
\]

This proves the determinant obstruction disappears at two insertions.  It does **not** prove that the actual VOA OPE realizes the nonlinear determinant phase or that its coefficient is independently controllable.

Artifacts:
- `analysis/w33_h1_det_weight2_coupling_no_go.py`
- `data/w33_h1_det_weight2_coupling_no_go.json`
- `analysis/w33_h1_det_two_weight2_witness.py`
- `data/w33_h1_det_two_weight2_witness.json`

## 4. The 165+297 GQ(4,8) peeling decoder has exact stopping distance 30

The 165 local Suzuki/W33 encodings are the points of `GQ(4,8)` and the 297 five-point GQ lines provide redundant line-sum measurements.  A peeling stopping set `S` meets every line in either zero or at least two erased points.

Every erased point lies on nine GQ lines, so a stopping set induces minimum point-graph degree at least nine:

\[
2e(S)\ge9|S|.
\]

The point graph is `SRG(165,36,3,9)` with largest nontrivial eigenvalue `3`.  For `m=|S|`, the Rayleigh bound gives

\[
2e(S)\le 3m+\frac{m^2}{5}.
\]

Therefore `m>=30`.  An explicit 30-point set in the classical Hermitian model `H(4,4)` meets the 297 GQ lines as

\[
0^{162}+2^{135},
\]

and is 9-regular internally.  Thus

\[
\boxed{d_{\rm stop}=30}.
\]

Every pattern of at most 29 point-channel erasures is therefore peel-decodable from surviving point values plus the 297 line sums, and the bound is sharp for peeling.  This does not exclude a stronger global linear decoder on a 30-point stopping set.

Artifacts:
- `analysis/w33_suzuki_gq48_stopping_distance.py`
- `data/w33_suzuki_gq48_stopping_distance.json`

## 5. The first dark-15 point/line transceiver is uniquely quartic

Earlier exact work proved the two inequivalent 15-dimensional dark constituents of the W33 point and line permutation modules have no linear PSp-equivariant map, and the actual PGSp outer twist does not restore one.

Full `PSp(4,3)` character enumeration now gives

\[
\dim\operatorname{Hom}(\operatorname{Sym}^2V_{15}^{\rm line},V_{15}^{\rm point})=0,
\]
\[
\dim\operatorname{Hom}(\operatorname{Sym}^3V_{15}^{\rm line},V_{15}^{\rm point})=0,
\]
\[
\boxed{\dim\operatorname{Hom}(\operatorname{Sym}^4V_{15}^{\rm line},V_{15}^{\rm point})=1}.
\]

The first ordinary equivariant nonlinear bridge is therefore quartic and unique up to scale.  This is representation-theoretic existence and uniqueness; a preferred local polynomial, normalization and physical/VOA realization remain open.

Artifacts:
- `analysis/w33_dark15_first_nonlinear_bridge.py`
- `data/w33_dark15_first_nonlinear_bridge.json`

## Frontier after this pass

The computational picture is now unusually specific.  The affine A8^3 operator algebra is conditionally controllable up to `sl729`; the first finite nonlinear determinant witness appears at two synchronized weight-two insertions; the point/line dark sectors first communicate at quartic degree; and the 165/297 readout layer has exact peeling distance 30.  On the heterotic side, the FI and exotic operators use compatible massless singlets, but physical rank-nine decoupling requires a nonuniform D/F-flat fixed-point condensate rather than a symmetric vacuum.

These statements should not be collapsed into a single claim of machine universality or a Standard-Model vacuum.  The remaining physical bottlenecks are addressability of affine-return Hamiltonians, realization of the determinant/quartic nonlinear maps, and explicit solution of the fixed-point-resolved heterotic F-term equations.
