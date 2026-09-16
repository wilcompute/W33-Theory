# 2026-09-16 — Suzuki/E6/instanton/QC frontier

Status: **exact finite results plus explicitly delimited physics probes**.

This packet integrates the post-`PASS20260915_execute_all5_pauli_stack` work and cross-links the heterotic results in `wilcompute/Holotrade`.  It also records three deliberately outside-the-box quantum/physics probes, including the ones that fail.

## 1. Local Suzuki 165 = GQ(4,8), with a 45+120 spectral split

From the exact 2.Suz 12-dimensional GF(3) module, fix one point of the 32760-point tight orbit.  Exactly 165 certified full W33 four-spaces contain it.  Adjacency by vector-intersection dimension two gives

\[
\operatorname{srg}(165,36,3,9),
\]

the classical U5(2) polar graph / point graph of `GQ(4,8)`.  Its spectrum is

\[
36^1+3^{120}+(-9)^{44},
\]

so its permutation module splits as

\[
165=(1+44)+120=45+120.
\]

The equality with the repo's 45 tritangents and 120 Steiner triangles is exact at the dimension level.  No equivariant intertwiner is claimed yet.  Locally, the 36 neighbors of a base W33 split as nine non-isotropic projective lines through the chosen point, four neighbors per line; the four isotropic W33 lines through that point are the complementary directions.

Artifacts:
- `analysis/w33_suzuki_local_165_gq48_spectral_bridge.py`
- `data/w33_suzuki_local_165_gq48_spectral_bridge.json`

## 2. Heterotic exotics: instanton-supported structural rank nine

Holotrade previously left 864 sextic and 12960 nonic channels after gauge, point/space-group, R-charge and Rules 4/5.  The factorized A2^3/Z3 classical instanton kernels are

\[
K_S(T)=\sum_{m,n\in\mathbb Z}e^{-2\pi T(m^2-mn+n^2)},
\]
\[
K_D(T)=\sum_{m,n\in\mathbb Z}e^{-2\pi TQ(m+1/3,n+2/3)}.
\]

Both are strictly positive for `T>0`.  The Rule-4-safe aggregate kernels are

\[
K_6=2K_S(T_0)K_D(T_b)[K_S(T_c)+2K_D(T_c)],
\]

and

\[
K_9=K_S(T_0)[K_S(T_1)+2K_D(T_1)][K_S(T_2)+2K_D(T_2)].
\]

At `T_i=1`, `K_S=1.0112046955376903`, `K_D=0.3701266069929033`, `K_6=1.3110494848380547`, `K_9=3.1019763867453394`.  Hence classical worldsheet-instanton cancellation cannot erase the allowed support.  The mass matrix is now **instanton-supported structural/generic rank nine**, not yet an explicit low-energy numerical rank: Kahler metrics, singlet VEVs, quantum/OPE normalization and physical-state phases remain.

Holotrade artifacts:
- `analysis/w33_exotic_worldsheet_instanton_kernel.py`
- `data/w33_exotic_worldsheet_instanton_kernel.json`
- parents `analysis/w33_exotic_sextic_nonic_completion.py`, `data/w33_exotic_sextic_nonic_completion.json`

Literature boundary: Choi–Kobayashi, arXiv:0711.4894; Kobayashi–Parameswaran–Ramos-Sanchez–Zavala, arXiv:1107.2137.

## 3. 1,216,215 tensor-frame graph: exact sporadic Clifford compiler

The three-W33 decompositions form a graph by sharing one W33 block.  Since each W33 lies in 27 decompositions, every frame has

\[
3(27-1)=78
\]

neighbors, giving 47,432,385 edges.  The complete local move library fixing one block is its W33 stabilizer `2_-^(1+6):U4(2)`.  Two distinct block stabilizers are distinct conjugate maximal subgroups of Suz, so they generate Suz projectively; in the exact symplectic lift the generated group is `2.Suz`.

This does **not** generate the full six-qutrit Clifford group:

\[
[Sp(12,3):2.Suz]=16054507443872541110987520.
\]

Thus refactorization is a real, very large Clifford compiler primitive, but not Clifford-universal and not a magic resource by itself.

Artifacts:
- `analysis/w33_suzuki_refactorization_compiler.py`
- `data/w33_suzuki_refactorization_compiler.json`

## 4. The 45 tritangent phases reduce to ten homological targets

An individual Pauli/Chevalley triangle phase is cocycle-gauge dependent: the solved E8->Pauli lift permits homogeneous generator rephasing.  Let `R` be the 27x45 line/tritangent incidence matrix.  Vertex rephasing changes a 45-vector of phases by `R^T a`; gauge-invariant linear phase observables therefore lie in `ker R`.

Pass7364 already proved the integral cubic identity

\[
RN=3Q,
\]

with `rank_F3(R)=21` and `rank_F3(N)=14`.  Consequently

\[
\dim\ker R=24,
\qquad
\dim H_1=24-14=10.
\]

So a single tritangent central phase cannot supply non-Clifford magic.  The first mathematically honest target is a **ten-dimensional mod-3 global cubic holonomy sector** after quotienting the canonical double-six boundaries.  Evaluating it still requires a certified transport from the E6 minuscule 27 to an enriched Pauli/VOA carrier; no such transport is invented here.

Artifacts:
- `analysis/w33_e6_tritangent_pauli_holonomy_frontier.py`
- `data/w33_e6_tritangent_pauli_holonomy_frontier.json`

## 5. Outside-box probe A — the isotropic 36 is an MRD/rank-metric computer

The earlier Suzuki isotropic section is `PG(3,3)` minus a line; its 81 internal graph lines are `M_2(F3)`.  Invertible difference gives

\[
\operatorname{srg}(81,48,27,30),
\]

with spectrum `48^1+3^48+(-6)^32`.  Exactly 18 two-dimensional subspaces of `M_2(F3)` are MRD planes (all eight nonzero matrices invertible).  Their nine affine cosets give 162 distinct nine-line parallel frames; adding the deleted line closes a ten-line projective spread.

These are **not** the 36 symplectic W33 spreads: this four-space is totally isotropic.  The computational reading is rank-metric addressing/collision-free routing in a four-trit affine matrix chart.

Artifacts:
- `analysis/w33_isotropic36_rank_metric_m2.py`
- `data/w33_isotropic36_rank_metric_m2.json`

## 6. Outside-box probe B — quaternionic tight-design shadow

The local 165 graph reconstructs exactly 297 five-point lines, nine through each point, with every adjacent pair on one line:

\[
165\cdot9=297\cdot5.
\]

This is the same U5(2) degree-165/297 incidence G-set that has the classical quaternionic realization as a 165-ray tight projective 3-design in `HP^4`, with the 297 GQ(4,8) lines as Jordan frames.  The exact finite G-set equivalence is useful; a physical claim is not made until a natural complex/fusion-frame intertwiner is built.

Artifacts:
- `analysis/w33_suzuki_165_quaternionic_design_shadow.py`
- `data/w33_suzuki_165_quaternionic_design_shadow.json`

External anchors: ATLAS U5(2) degree-165 and degree-297 actions; Hoggar/Nasmith quaternionic tight-design realization.

## 7. Outside-box probe C — A8^3 -> Moonshine naive orbifold surgery fails

The exact all-level identity

\[
Z_{(123)}^{A_8^3}=T_{3C},
\qquad
Z_{(12)}^{A_8^3}=T_{2A}+80
\]

remains intact.  But the plain factor 3-cycle cannot orbifold `V_{A8^3}` to Moonshine: weight one is `sl9^3`, and the cycle fixes diagonal `sl9`, dimension 80.  Those fixed currents survive in the fixed-point VOA, while `V^natural_1=0`.  The cyclic-permutation twisted ground shift is

\[
h_{tw}=\frac{8}{24}(3-1/3)=8/9.
\]

The obvious center/simple-current dressing also fails to remove the obstruction because the SU(9) center acts trivially on adjoint currents.  Thus the Monster equality is an exact **twining shadow**, while a literal surgery would require a genuinely different operation (commutant/coset/BRST-like reduction, non-central automorphism, or the known fixed-point-free Leech route).

Artifacts:
- `analysis/w33_a8cubed_monster_orbifold_surgery_obstruction.py`
- `data/w33_a8cubed_monster_orbifold_surgery_obstruction.json`
- parent `analysis/w33_a8cubed_monster_s3_twining.py`

External anchors: Chen–Lam–Shimakura arXiv:1606.05961; Abe–Lam–Yamada arXiv:1705.09022.

## Claim boundary

The finite incidence, coding, group, VOA-character and classical-instanton statements above are exact within their stated models.  The following remain open and are not promoted to physical facts: an actual rank-nine low-energy exotic mass matrix, physical implementation of Suzuki refactorization moves, a complex quantum realization of the quaternionic design, a nonzero ten-class tritangent magic witness, and any literal identification of A8^3 with the Moonshine VOA.
