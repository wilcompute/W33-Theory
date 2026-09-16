# 2026-09-16 — Five-front intertwiner / holonomy / mass / fusion / magic closure

Status: **PASS with two deliberate no-go boundaries**.

This packet executes the five next steps following `PASS20260916_suzuki_e6_instanton_qc_frontier`.

## 1. The local 165 really splits 45+120 — but only the 45 is the old cubic carrier

Using the ATLAS degree-165 permutation representation of `U5(2)` and its maximal subgroup `3 x U4(2)`, the restricted action has two orbits of sizes 45 and 120.  The central order-three factor fixes the 45 orbit pointwise and partitions the 120 orbit into forty 3-cycles.

The 45 orbit's small pair orbital is

\[
\operatorname{srg}(45,12,3,3),
\]

with 270 edges.  This is explicitly graph-isomorphic to the cubic-surface graph in which two tritangents are adjacent when they share one of the 27 cubic lines.  Thus the 45 half has a concrete intertwiner to the old tritangent carrier.

The 120 orbit is subtler.  Its unordered-pair orbit sizes are

\[
120,\quad 1620,\quad 2160,\quad 3240,
\]

exactly the same coarse data as the classical Steiner trihedral-pair action, and the 120 relation is forty disjoint triangles.  However the 2160 relation is a complete `K3,3` lift whose 40-fiber quotient is `SRG(40,12,2,4)` with

\[
\operatorname{rank}_{F_3}(A+I)=11.
\]

That is the **standard W33 point action**.  Pass4870 independently proves the classical Steiner cover quotients to `Q(4,3)` and has rank 15.  Therefore the local `U5(2)` decomposition is

\[
165=45_{\rm tritangent}+120_{\rm Steiner\text{-}twin},
\]

not the old tritangent-plus-Steiner permutation set.

Artifacts:
- `analysis/w33_u52_165_e6_45_120_split.py`
- `data/w33_u52_165_e6_45_120_split.json`

External source: ATLAS `U52G1-p165B0` and maximal subgroup program `U52G1-max2W1`.

## 2. The ten global cubic holonomies are exactly the finite symplectic adjoint

Let `R` be the 27x45 line/tritangent matrix and `N` the 45x36 tritangent/double-six matrix.  Pass7364 gives `RN=0 mod 3`, `rank R=21`, `rank N=14`, hence

\[
H_1=\ker R/\operatorname{im}N,\qquad \dim H_1=10.
\]

Using the same exact `PSp(4,3)` generators on the cubic carrier and on the `O5(3)` model, the simultaneous intertwiner equations between this `H1` and `Lambda^2(F3^5)` have

\[
\dim\operatorname{Hom}_{PSp}=1
\]

and the unique nonzero map has rank ten.  Therefore

\[
\boxed{H_1\cong\Lambda^2(F_3^5)\cong\mathfrak{so}_5(F_3)\cong\mathfrak{sp}_4(F_3).}
\]

This stitches the old Pass7364 cubic homology directly to the independent Pass4858/4864 adjoint controller.  It also sharpens the magic boundary: linear mod-3 cubic holonomy is symplectic-adjoint / Clifford-side data.  A nonzero `H1` class can be a global contextual transport invariant without automatically being a non-Clifford gate.

Artifacts:
- `analysis/w33_e6_cubic_h1_is_sp4_adjoint.py`
- `data/w33_e6_cubic_h1_is_sp4_adjoint.json`

## 3. Exotic mass support has a concrete rank-nine instanton-weighted benchmark

Holotrade already certifies complete sextic+nonic `K_{9,12}` support and positive classical instanton factors.  The repository does **not** yet supply a D/F-flat singlet vacuum, canonically normalized field metrics or all physical-state/OPE phases, so there is no honest unique physical mass matrix to calculate.

The remaining algebraic question can nevertheless be closed.  On the allowed support choose

\[
C_{rc}=(r+1)^c.
\]

The first nine columns form a Vandermonde matrix with

\[
\det C_{0:9}=\prod_{i<j}(j-i)=5056584744960000\ne0.
\]

Multiplication of the eight sextic and four nonic columns by their strictly positive `T_i=1` instanton factors preserves rank.  Hence an explicit allowed instanton-weighted benchmark has rank nine.  The rank-deficient locus is a proper algebraic subset of the allowed coupling/VEV parameter space.

Holotrade artifacts:
- `analysis/w33_exotic_benchmark_mass_matrix.py`
- `data/w33_exotic_benchmark_mass_matrix.json`

Boundary: this is an existence/genericity witness, not a predicted spectrum or proof that a consistent string vacuum chooses that specialization.

## 4. The quaternionic 165 carrier has a canonical complex six-qutrit Pauli shadow

For each local W33 four-space `U`, take the Hilbert-Schmidt subspace spanned by the 80 nonidentity six-qutrit Pauli monomials with degree in `U\{0}`.  All 165 W33s through the fixed Leech point share the two operators labelled by `+/-p`.  Removing that common core leaves rank 78 projections.

For adjacent local W33s, the 4-spaces intersect in vector dimension two, hence share eight nonzero Pauli degrees and six after core removal.  Nonadjacent W33s share only `+/-p`, hence zero after removal.  The normalized projection Gram matrix is therefore

\[
G=I+\frac1{13}A_{165}.
\]

Using the exact `SRG(165,36,3,9)` spectrum gives

\[
\operatorname{spec}G=(49/13)^1+(16/13)^{120}+(4/13)^{44}.
\]

The second projection-frame potential is

\[
\frac{33825}{169},
\]

so this two-distance complex frame is highly symmetric but not tight.  It is a genuine complex/six-qutrit operator-space shadow of the same `U5(2)/GQ(4,8)` incidence carrier, without inferring quaternionic quantum mechanics.

Artifacts:
- `analysis/w33_suzuki_165_complex_pauli_fusion_shadow.py`
- `data/w33_suzuki_165_complex_pauli_fusion_shadow.json`

## 5. Current internal non-Clifford candidates close negatively

Three natural candidates were tested.

1. Three-W33 refactorization moves generate `2.Suz <= Sp(12,3)`: Clifford.
2. The ten cubic channels are the `sp4(F3)` adjoint: Clifford-side controller data.
3. The `A8^3` `Z9` center acts on `Lambda^k(9)` by a scalar ninth root.  A scalar phase conjugates all Pauli operators trivially; the weight-two simple-current fields such as `9 tensor 9 tensor 126` are inter-sector fields, not certified endomorphisms of the fixed `9^3` ground register.

A control shows why the distinction matters.  For `xi^9=1`, the qutrit third-level target

\[
T=\operatorname{diag}(1,\xi,\xi^{-1})
\]

has `T^3=Z`, but `T X T^{-1}` is not proportional to any Pauli `XZ^k`; it is genuinely non-Clifford.  By contrast `xi^k I` is computationally trivial.

Thus the currently certified internal geometry does **not** yet supply the missing universal resource.  The missing datum is precise: an explicit sector-return endomorphism whose Pauli conjugation leaves the Clifford normalizer, or a certified magic-state injection.  This is consistent with the machine blueprint's existing firewall that keeps `M36` magic as an external handshake.

Artifacts:
- `analysis/w33_nonclifford_extension_search.py`
- `data/w33_nonclifford_extension_search.json`

## Claim boundary

The permutation-action separator, mod-3 adjoint intertwiner, rank-nine benchmark existence proof, complex Pauli fusion shadow and current-layer non-Clifford null are exact within their stated models.  They do not supply: a physical D/F-flat exotic vacuum, a measured mass spectrum, a complex realization of the quaternionic projective metric itself, or an internal universal non-Clifford gate.  Those remain open with substantially sharper targets.
