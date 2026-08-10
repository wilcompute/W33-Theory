# Passes 4769–4776 executed outcomes

Collision-free continuation after the occupied frontier through Pass4768. All five requested fronts and all three outside-box probes were executed. The theorem-critical values below were independently reconstructed from the finite W33 geometry in-session and frozen as repository certificates; the self-materializing Actions workflow remains a reproducibility layer rather than the sole source of evidence.

## 4769 — modular H1 head/socle and a nonsplit deck line
For the invariant 810-flag valency-16 graph,

`dim_F2 H^1 = 6480 - 810 + 1 = 5671`.

Exact spanning-tree action matrices for the PSp generators and PGSp outer involution give

- `dim (H^1)^PSp = 4`;
- `dim (H^1)^PGSp = 4`;
- `dim H^1_PSp = 1` and `dim H^1_PGSp = 1` for coinvariants/trivial head;
- augmentation dimension `dim sum_g (g-1)H^1 = 5670`.

All four invariant vectors lie in the augmentation subspace. The apartment deck vector is one of them, is PSp- and PGSp-fixed, and has deterministic tree-gauge weight `2296`. Therefore the fixed trivial socle is four-dimensional but every one of those trivial lines is buried in the augmentation/radical side of the module; in particular the deck line does **not** split as a trivial direct summand. This is a genuine characteristic-two nonsplit extension. No complete 5671-dimensional Loewy series is claimed.

## 4770 — exact S3 moduli modulo vertex gauge
Put the Pass4716 connection on the 45-vertex, 270-edge GQ(4,2) point graph into spanning-tree gauge, leaving 226 cotree voltages. Since the odd elements of S3 are exactly its three transpositions, the condition “all 270 base triangles have transposition holonomy” is exactly a binary sign condition.

The exact affine GF(2) triangle-sign system has

- rank `162`;
- affine dimension `64`;
- exactly `2^64 = 18446744073709551616` sign sectors.

For one fixed sign sector each cotree edge has three allowed lifts of its prescribed parity. Burnside reduction by the residual global S3 conjugation gives exactly

`(3^225 - 1)/2`

connected vertex-gauge classes per sign sector. Numerically this is

`112525853641624202021632199459978446954265333660156200574003740207440302794263728193626266765193829380550721`.

Thus before the further 51,840-element base-automorphism quotient, the total connected vertex-gauge classes are

`2^64 (3^225 - 1)/2`.

All `452` one-cotree-edge same-sign perturbations of the selected tree-gauge connection remain connected. The triangle rule is therefore massively non-rigid. The quotient by the full base automorphism group is intentionally left as a further finite orbit problem rather than falsely called solved.

## 4774 — the nonabelian deformation sector is twisted F3 cohomology
Write an S3 voltage as `r^a s^p`, with `r^3=s^2=1` and `srs=r^-1`. The A3 exponent is then a rank-one F3 local system whose sign flips across odd S3 edges.

For the selected sign cocycle the exact twisted coboundary

`C^0 = F3^45 -> C^1 = F3^270`

has rank `45`, so

- `H^0 = 0`;
- `dim_F3 H^1 = 225`.

Every one of the `2^64` binary sign sectors therefore carries the projective point set of nonzero F3^225 vectors modulo +/-1, i.e. a `PG(224,3)` point set, before the base-automorphism quotient.

This deformation sector cannot be linearly identified with the characteristic-two apartment deck line: there is no nonzero additive homomorphism from an F2 line to an F3 vector space. The shared “gauge” vocabulary is therefore explicitly separated by characteristic.

## 4771 — the degree-16 normalizer cover and its second homogeneous lift
Let `H` be a residue stabilizer, `|H|=96`, and `K=C_PSp(h)`, `|K|=48`, the Pass4738/4752 sheet-character kernel. The homogeneous carrier is

`PSp(4,3)/K -> PSp(4,3)/H`, `540 -> 270`.

There are two subdegree-16 residue orbitals. The desired Pass4752 base is identified intrinsically: for adjacent residues the product of their unique four-fixed involutions has order 3 and fixes **7** W33 lines; the other degree-16 orbital fixes only **1** line.

The selected 270-vertex base has

- 2160 edges, degree 16;
- diameter 4 and edge-connectivity 16;
- 2880 triangles;
- binary adjacency rank 78;
- cycle-code dimension 1891;
- spectrum

`16^1 + (-8)^6 + 6^24 + (-3)^64 + 0^135 + (2+2 sqrt(13))^20 + (2-2 sqrt(13))^20`.

Above this same base there are **two** connected 540-vertex homogeneous degree-16 graph lifts, both with 4320 edges and diameter 4. Easy graph fingerprints therefore do not select the apartment cover. Their triangle counts are `1440` and `4320`, and their signed spectra are exact negatives:

- rejected 1440-triangle lift: `(-8)^20 + (-4)^81 + 1^64 + 4^105`;
- Pass4752 lift: `8^20 + 4^81 + (-1)^64 + (-4)^105`.

An independent reconstruction of the Pass4752 810->270 cochain descent gave beta weight `1172`; tree-gauging beta and both homogeneous lifts selects the 4320-triangle lift by literal equality of cohomology classes.

The selected cover has binary adjacency rank `226` and cycle-code dimension `3781`. Its signed induced character is

`10a + 10b + 15a + 45a + 45b + 64 + 81`.

## 4775 — the base is in the M2 block; the sheet module is not
Starting from the full 12-orbital residue multiplication tensor, the rank-40 central projector onto the multiplicity-two degree-20 sector is recovered intrinsically by Chinese-remainder projection of the cold adjacency onto

`x^2 - 2x - 12`.

A primitive rank-20 idempotent gives a two-dimensional rational left ideal. In one exact basis,

`A_cold -> [[0,12],[1,2]]`,

`A_hot -> [[3,6],[0,-2]]`,

`A_16 -> [[4,-24],[-2,0]]`.

The degree-16 matrix has exact characteristic polynomial

`x^2 - 4x - 48`

and eigenvalues `2 +/- 2 sqrt(13)`.

All twelve 2x2 matrices reproduce the complete orbital multiplication tensor exactly. However, the signed normalizer-cover sheet representation listed in Pass4771 has degree-20 multiplicity **zero**. Thus the degree-16 **base** relation acts nontrivially in the unique `M2(Q)` Wedderburn block, while the C2 sheet sector itself is representation-theoretically transverse to that block.

## 4776 — dependency cubes are literally the Pass4748 coding cells
The 135 dependency Q3 cubes of Pass4758 and the 135 fifteen-edge cross-fiber coding cells of Pass4748 are the same PSp(4,3) G-set under an explicit equivariant map:

`cube union u -> selected135 vertex phiU(u) -> packet-coordinate coding cell`.

Representative stabilizers are equal as actual subgroups of order `192`.

For every cube:

- its six residue vertices have cold graph `K6 - 3K2`;
- under the residue->selected270 intertwiner, its six vertices are exactly the six selected270 lines through the corresponding selected135 point;
- the three missing pairs are exactly the three Petersen-hot edges;
- adding those three pairs completes the physical cell to `K6`;
- the other twelve edges are exactly the three cold `K2,2` blocks.

The 135 completed K6 cells partition all `2025` physical router edges exactly once.

## 4772 — canonical global code coupling: [2025,378,14]
Use the cube/cell K6 coordinates. The local `[15,3,7]_2` code has three logical generators indexed by the three quotient GQ lines through the cell. One generator consists of all three hot matching edges plus the cold K2,2 block between the other two line fibers.

Therefore the 405 local logical coordinates split canonically into

`27 groups x 15 coordinates`,

one group for each quotient GQ line.

Imposing one even-parity constraint on each group gives the exact PGSp-invariant code

`[2025,378,14]_2`.

The distance proof is exact. Total logical weight is even. Logical weight 2 forces two distinct cells in one quotient-line group, giving disjoint physical supports of weight `7+7=14`. Logical weight at least 4 has physical weight at least 16 because the local physical weight law is

`h=1 -> 7`, `h=2 -> 8`, `h=3 -> 15`,

which satisfies `w(h)>=4h` for `h=1,2,3`. An explicit weight-14 witness exists.

The explicit `K*d` metric improves from Pass4748's

`405*7 = 2835`

to

`378*14 = 5292`.

The extreme line-repetition outer code gives a second exact family

`[2025,27,105]_2`.

No universal coding optimality or physical fault-tolerance threshold is claimed.

## 4773 — exact symmetry-reduced all-pairs multicommodity flow
Use unit demand for every ordered distinct selected270 pair, cold-edge capacity 1 and hot-edge capacity `rho`. PSp has eleven nontrivial ordered-pair orbitals. Exact nondominated path signatures and group averaging reduce the entire 72,630-commodity fractional concurrent-flow problem to the lower convex frontier

`(113400,64530), (147960,29970), (167400,17010), (201420,0)`,

where coordinates are aggregate cold/hot traversals per unit concurrent demand.

The exact throughput law is

- `lambda(rho)=3(rho+2)/746` for `0<rho<=63/155`;
- `lambda(rho)=3(3rho+8)/2858` for `63/155<=rho<=111/137`;
- `lambda(rho)=3(rho+4)/1318` for `111/137<=rho<=239/105`;
- `lambda(rho)=1/70` for `rho>=239/105`.

At equal capacities,

`lambda(1)=15/1318 ~= 0.011380880121396054`.

The 27-fiber quotient `SRG(27,10,1,5)` has exact ordered-all-pairs throughput `10/7` when each quotient edge receives its twelve cold physical-edge capacities.

For symmetry-breaking failures, the intact orbit reduction no longer applies. The packet therefore freezes only explicit all-shortest-path feasible lower bounds plus rigorous single-vertex-cut upper bounds for one/two hot-fiber outages and one/two full vertex-fiber removals. Those failure-case values are **not** claimed optimal.

## Integration and evidence
- Executable witnesses: `analysis/w33_pass4769_modular_h1_head_socle.py`, `analysis/w33_pass4770_4774_s3_moduli_twisted_tangent.py`, corrected `analysis/w33_pass4771_4775_degree16_cover_hecke_certified.py`, `analysis/w33_pass4772_4776_global_cube_cell_code.py`, and `analysis/w33_pass4773_symmetry_reduced_multicommodity_flow.py`.
- Eight frozen certificates: `data/PART_W33_PASS4769_*` through `data/PART_W33_PASS4776_*`.
- Cross-certificate regression: `tests/test_w33_pass4769_4776_modular_moduli_cover_code_flow.py`.
- Reproducibility workflow: `.github/workflows/w33_pass4769_4776_modular_moduli_cover_code_flow.yml`, configured to preserve diagnostics before enforcing success.
- Shared theorem insert: `analysis/PASS4769_4776_modular_moduli_cover_code_flow_insert.tex`, integrated into `w33_paper.tex`, `photonic_holonet.tex`, and `holonet_machine_blueprint.tex` after Pass4753–4760 and before the later canonical Pass4785–4792 packet.
- Public card/page: `analysis/PASS4769_4776_modular_moduli_cover_code_flow_index_insert.html` and `docs/modular-h1-s3-moduli-normalizer-code-flow.html`, registered in the public frontier registry.
- `docs/index.html` was not directly rewritten.

Evidence discipline: all promoted statements are exact finite graph/group/cohomology/module/code/semisimple-algebra results or exact fractional-flow theorems under the stated demand convention. Negative/nonidentification results are preserved. No physical gauge field, particle/generation assignment, measured hardware performance or fault-tolerance threshold is inferred.
