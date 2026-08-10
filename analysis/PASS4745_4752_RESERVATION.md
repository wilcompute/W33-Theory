# Passes 4745–4752 executed outcomes

Collision-free continuation after occupied frontier through Pass4744. All five requested fronts and three outside-box probes are executed and frozen on `master`. The packet uses the Pass4737–4744 involution-residue realization as an independent cross-check of the selected270 router.

## 4745 — full invariant H1 character and a characteristic-two boundary
For the Pass4713 invariant 810-flag graph, the deterministic first connected self-paired valency-16 orbital is the suborbit seeded by flag `173`. Its parameters remain `v=810`, `k=16`, `E=6480`, diameter `5`, and

`dim H^1(Q)=6480-810+1=5671`.

Reconstructing the complete 25920-element `PSp(4,3)` group, its 20 conjugacy classes and ordinary character table gives

`H1 = 5a + 5b + 3(10a+10b) + 4(15a) + 20 + 4(24) + 7(30a) + 4(30b+30c) + 10(40a+40b) + 12(45a+45b) + 11(60) + 14(64) + 19(81)`.

The dimension closes exactly at 5671. The trivial multiplicity is zero. The self-paired edge stabilizer has order 4 and contains two endpoint reversers, so the oriented characteristic-zero edge module has no invariant line.

Pass4713 nevertheless supplies a nonzero `PGSp(4,3)`-fixed deck class in `H^1(F2)`. Therefore that mod-2 deck line has no PGSp-invariant integral/rational lift: it is an intrinsically characteristic-two invariant, not the reduction of an ordinary trivial constituent.

## 4746 — full base symmetry, but the triangle rule is nonunique
The explicit `PGSp(4,3)` action on the 45 reconstructed GQ packets has image order 51840, equal to the independently frozen full automorphism order of the GQ(4,2) point graph. The inner generators and outer generator satisfy the fiber-lift equation, so every base automorphism lifts to the selected three-cover.

In spanning-tree gauge, two triangular fundamental cycles already generate the monodromy:

- cotree edges `(1,12)` and `(1,20)`;
- two distinct transposition voltages;
- cycle lengths `3,3`;
- generator orders `2,2` and product order `3`.

Hence the monodromy presentation is

`<a,b | a^2=b^2=(ab)^3=1> = S3`.

However, the condition “all 270 base triangles have transposition holonomy” does **not** characterize the selected connection. Exhaustive one-cotree-edge deformation already finds a distinct connected S3 connection: change the cotree voltage on edge `(1,12)` to the third transposition `(0,2,1)`. All 270 triangle holonomies still have order 2 and the monodromy remains S3. Thus uniqueness fails already at Hamming radius one in cotree-voltage space.

## 4747 — the radical spectrum is a multiplicity-two PSp(20) sector
The cold 270-vertex permutation module decomposes as

`1 + 6 + 15b + 2(20) + 24 + 30b + 30c + 60 + 64`.

The cold adjacency eigenspaces are

- `12^1 -> 1`;
- `8^15 -> 15b`;
- `(1+sqrt(13))^20 -> 20`;
- `2^84 -> 24+30b+30c`;
- `(-1)^64 -> 64`;
- `(1-sqrt(13))^20 -> 20`;
- `(-4)^60 -> 60`;
- `(-6)^6 -> 6`.

The two irrational 20-dimensional eigenspaces are therefore the same degree-20 irreducible appearing with multiplicity two. After removing the rational sectors, `tr(A)=0` and `tr(A^2)=270*12` force trace `2` and determinant `-12` on its two-dimensional multiplicity space, so the exact polynomial is

`x^2 - 2x - 12`,

with roots `1 ± sqrt(13)`. The full characteristic factorization is

`(x-12)(x-8)^15(x-2)^84(x+1)^64(x+4)^60(x+6)^6(x^2-2x-12)^20`.

## 4748 — genuine cross-fiber coding on all 2025 router edges
The `3 K2,2` connection law canonically partitions all 2025 physical router edges into 135 disjoint 15-edge cells indexed by a GQ packet and one of its three internal coordinates. Each cell contains:

- 3 hot Petersen edges;
- 3 cold `K2,2` blocks, 4 physical edges per block.

Compressing each repeated cold block to one symbolic coordinate gives a triangle with three physical-weight-1 vertex symbols and three physical-weight-4 edge symbols. Exhausting all 2825 binary subspaces of `F2^6` leaves exactly 25 invariant under the local `S3` action. Their weighted rate-distance Pareto frontier is

`(k,d_w) = (1,15),(2,10),(3,7),(4,3),(5,2),(6,1)`.

Thus the exact PGSp-invariant global families include

`[2025,135,15]_2`, `[2025,270,10]_2`, `[2025,405,7]_2`, `[2025,540,3]_2`, `[2025,675,2]_2`, `[2025,810,1]_2`.

The uncoupled Petersen-cycle plus cold-repetition baseline is `[2025,567,4]_2` with `K*d=2268`. The cross-fiber `[2025,405,7]_2` member has `K*d=2835`, improving this explicit metric while deliberately trading rate for distance. No universal coding optimum is claimed.

## 4749 — exact adversarial min-cut and targeted fiber failures
Normalize every cold-edge capacity to `1` and every hot-edge capacity to `rho>0`. Exact structural data are:

- cold graph edge-connectivity `12`;
- every Petersen fiber edge-connectivity `3`;
- 27-vertex quotient edge-connectivity `10`;
- exactly `12` cold physical edges over every quotient edge.

Therefore a cut that splits a Petersen fiber costs at least `12+3 rho`, attained by a single router vertex. A cut that splits no Petersen fiber is a union of complete fibers and has cold cost at least `12*10=120`, attained by one complete fiber. Hence

`lambda_min(rho) = min(12+3 rho, 120)`

with the sole technology breakpoint `rho=36`.

At equal capacities all `C(270,2)=36315` unordered vertex pairs have min-cut 15. Removing all 15 hot edges from one Petersen fiber lowers the global min-cut to exactly 12 for every positive rho; at rho=1, 2645 unordered pairs have min-cut12 and 33670 retain min-cut15.

Full ten-vertex fiber removals remain connected: one removed fiber leaves 260 vertices, min-cut13 and diameter3; two representative fibers leave 250 vertices, min-cut11 and diameter3 for both quotient-adjacent and quotient-nonadjacent pairs.

## 4750 — dependency circuits form a chain complex, but not a code map
The 540 minimum weight-three words of the residue `[270,240,3]_2` dependency code are exactly the 540 cold triangles whose edge sets partition all 1620 cold edges. Sending a free circuit generator to its three-edge triangle boundary gives an exact binary chain complex

`F2^540 --d2--> F2^1620 --d1--> F2^270`

with

- `rank d2 = 540`;
- `rank d1 = 269`;
- `d1 d2 = 0`;
- `dim H1 = 1620-540-269 = 811`.

The stronger tempting map from the actual dependency code fails. The 540 minimum dependency words span dimension240 and obey 300 independent linear relations, while their 540 edge-disjoint triangle boundaries are linearly independent. Therefore no linear map from the dependency-code span can send every minimum word to its corresponding triangle boundary.

## 4751 — exact finite S3 Fourier block; initial orientation bug caught and corrected
The three-sheet permutation representation splits as `1 + Std_2`. In the integral sum-zero basis, the standard lattice Gram matrix is

`[[2,-1],[-1,2]]`.

The corrected 90x90 matrix-valued voltage operator is self-adjoint for this Gram form and satisfies exactly

`S(S^2-36 I)=0`.

Its spectrum is `6^15,0^60,(-6)^15`; the trivial 45-block has `12^1,3^20,(-3)^24`. Together they reproduce selected135 exactly, while `trivial + sign + 2 Std_2` reproduces the Pass4719 regular six-sheet S3 closure spectrum.

No S3 Fourier block contains `x^2-2x-12`. Thus the selected270 `1±sqrt(13)` radical is not this direct cover-Fourier mechanism; Pass4747 locates it in the multiplicity-two degree-20 PSp sector.

An initial implementation placed the column-action permutation matrix in the source-target adjacency block without transposing it, producing spurious radicals. Independent execution caught the mismatch. The source/target orientation was corrected before freezing the theorem, and the corrected lift matches the original selected135 spectrum and exact polynomial identity.

## 4752 — major outside-box closure: the apartment deck cover is the Pass4738 normalizer cover after descent
The canonical projection from 810 selected flags to their 270 selected lines admits an exact F2 cochain descent

`alpha(u,v) + s_u + s_v = beta(pi(u),pi(v))`.

The projected base relation has 2160 edges and degree16. It is disjoint from both the 405 hot and 1620 cold router relations. One exact gauge solution has flag-gauge weight350; the descended beta has 1172 one-edges and 988 zero-edges.

Beta defines a connected double cover with

- vertices `540`;
- edges `4320`;
- degree `16`;
- diameter `4`.

The descended `PSp(4,3)` action has order25920 and is transitive on all540 vertices, hence a point stabilizer has order48.

For the corresponding selected-line/residue stabilizer `H` of order96, the three-flag sheet gauge `(0,1,1)` gives a nontrivial character `epsilon:H->C2` whose kernel has order48. Reconstructing the Pass4738 outer order-four root `h` gives

`K = C_PSp(h)`, `|K|=48`,

and the subgroup equality is literal:

`ker(epsilon) = K`.

Therefore the descended apartment deck double cover is exactly the homogeneous normalizer cover

`PSp(4,3)/K -> PSp(4,3)/H`,

with `H/K=C2`. This identifies the apartment deck twist and Pass4738 residue normalizer twist globally after an explicit equivariant descent; it is not a matching-order analogy.

## Integration and evidence
- Eight executable witnesses: `analysis/w33_pass4745_invariant_h1_character.py` through `analysis/w33_pass4752_deck_normalizer_twist_comparison.py`.
- Eight frozen certificates: `data/PART_W33_PASS4745_*` through `data/PART_W33_PASS4752_*`.
- Frozen cross-certificate regression: `tests/test_w33_pass4745_4752_invariant_bundle_code_capacity.py`.
- Regeneration workflow: `.github/workflows/w33_pass4745_4752_invariant_bundle_code_capacity.yml`; it executes all eight witnesses, runs the frozen regression, and preserves diagnostics/evidence even if a theorem assertion fails.
- Shared manuscript insert: `analysis/PASS4745_4752_invariant_bundle_code_capacity_insert.tex`, integrated after Pass4737–4744 in `w33_paper.tex`, `photonic_holonet.tex`, and `holonet_machine_blueprint.tex`.
- Public card/page: `analysis/PASS4745_4752_invariant_bundle_code_capacity_index_insert.html` and `docs/invariant-cohomology-router-spectrum-coding-capacity.html`, registered in the public frontier registry.
- `docs/index.html` was not directly rewritten.

Evidence discipline: every promoted statement is an exact finite graph/group/cohomology/ordinary-character/code/chain-complex result or an exact undirected finite-network capacity theorem. The word Fourier denotes finite-group representation decomposition. No optical phase, continuum gauge field, particle/generation assignment, measured hardware performance, or fault-tolerance threshold is inferred.
