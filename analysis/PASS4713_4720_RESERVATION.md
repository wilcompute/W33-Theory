# Passes 4713–4720 executed outcomes

Canonical collision-free continuation reserved after the occupied frontier through Pass4712. All five requested fronts and all three outside-box probes are executed on `master`, with executable witnesses, frozen certificates, a focused regression/regeneration workflow, a shared theorem insert in the three maintained manuscripts, and registered public card/page surfaces.

## 4713 — a genuinely PSp-invariant apartment cohomology class
The earlier five-generator Schreier base was not preserved by full PSp. Replace it by the smallest connected self-paired PSp orbital graph on the 810 selected point-line flags. Its exact parameters are:

- vertices `810`;
- valency `16`;
- edges `6480`;
- diameter `5`;
- `b1 = 6480-810+1 = 5671`.

Its equivariant lift to the 1620 apartments is connected, 16-regular and has exactly two lift edges above each base edge. The base triangle

`0 -> 482 -> 367 -> 0`

lifts between the two apartment sheets over flag zero, so the C2 deck class is nonzero. The PGSp outer similitude preserves both base and lift. Consequently the deck class is fixed by PGSp and spans an honest one-dimensional trivial PGSp submodule of

`H^1(base;F2)`.

This repairs the scope defect isolated in Pass4683; no optical phase is inferred.

## 4714 — the two dual shells intrinsically reconstruct GQ(4,2)
Start from the selected binary code and only its dual shells. The 45 complements of dual weight-132 words partition the 135 selected coordinates into `45 x 3`. Project the 270 dual weight-three words to those packet labels. The resulting 270 triples have pair graph

`SRG(45,12,3,3)`.

The only maximal cliques are exactly 27 copies of K5. Every projected triple lies in one unique K5, and each K5 contributes all `C(5,3)=10` triples. Thus the dual shells alone reconstruct the point-line geometry

`GQ(4,2): 45 points, 27 lines, 3 lines/point, 5 points/line`.

The dual line graph is `SRG(27,10,1,5)` and has full automorphism order `51840`, computed directly from the reconstructed graph.

For the 45x270 point-triangle incidence H,

`H H^T = 18 I + 3 A45`,

with Gram spectrum `54^1,27^20,9^24`, rational rank 45, modular ranks `(F2,F3,F5,F7)=(45,44,45,45)`, and

`SNF(H)_nonzero = 1^44 3`.

For the 45x27 GQ point-line incidence B,

`B B^T = 3 I + A45`,

with rational and tested modular rank 21 and

`SNF(B)_nonzero = 1^21`.

No protected-45 label is imported in this reconstruction.

## 4715 — exact ordinary-character decompositions of the 378 and 1485 edge kernels
The witness reconstructs the 25920-element PSp(4,3) permutation group, its 20 conjugacy classes and the complete 20-dimensional class algebra directly, recovering the ordinary irreducible degree multiset

`1,5,5,6,10,10,15,15,20,24,30,30,30,40,40,45,45,60,64,81`.

The 405 shortcut-edge permutation carrier has orbital rank 24 and decomposes as

`1 + 6 + 2(15_L) + 2(20) + 24 + 2(30_C-) + 2(30_C+) + 2(60) + 64`.

Its 27-object quotient is `1+6+20`, giving the exact 378-dimensional fiber kernel

`378 = 2(15_L) + 20 + 24 + 2(30_C-) + 2(30_C+) + 2(60) + 64`.

This agrees independently with the local Petersen-edge module `1+4+5+5` under A5: the kernel is `Ind_H960^PSp(4+5+5)`.

The 1620 robust-base edge carrier has orbital rank 146 and decomposes as

`1 + 6 + 4(15_L) + 4(20) + 3(24) + 30_R + 4(30_C-) + 4(30_C+) + 40_C+ + 40_C- + 45_C+ + 45_C- + 5(60) + 4(64) + 5(81)`.

Its 135-edge quotient is

`1 + 6 + 2(20) + 24 + 64`.

Therefore the exact 1485-dimensional fiber kernel is

`4(15_L)+2(20)+2(24)+30_R+4(30_C-)+4(30_C+)+40_C++40_C-+45_C++45_C-+5(60)+3(64)+5(81)`.

A second calculation fixes one quotient edge. Its 12-edge fiber has image order 96 and multiplicity-free complex permutation dimensions `1,1,1,3,6`, so the kernel is independently

`Ind_H192^PSp(omega + omega_bar + 3 + 6)`

with induced dimensions `135+135+405+810=1485`.

Equal-degree labels use action/complex-conjugation fingerprints only; no physics names are inferred.

## 4716 — selected135 is an S3 three-cover, and its fixed-sheet triangles reconstruct selected270
The 135 selected singular coordinates split into the 45 packet fibers reconstructed above. Between adjacent packet pairs the selected135 graph has exactly three edges, forming a perfect matching. Hence selected135 is a connected three-sheet graph cover of the GQ(4,2) point graph with an S3-valued connection.

After spanning-tree gauge, the 226 cotree voltages are:

- identity: `64`;
- each of the three transpositions: `54`.

The generated monodromy is all of S3, so this is a nonregular three-cover.

Every one of the 270 base triangles has order-two holonomy. The three transpositions occur exactly `90+90+90` times. Each transposition has one fixed sheet; following that fixed sheet around the triangle reconstructs exactly one original selected singular 3-point line. Recovering all 270 fixed-sheet triangles reproduces the original `135_6-270_3` incidence and therefore the selected270 intersection graph exactly.

The 27 GQ lines are the 27 ten-vertex Petersen fibers. For every one of the 135 adjacent fiber pairs, the 12 robust-base cross edges split as

`3 K2,2`,

one K2,2 for each of the three singular coordinates in their shared packet. This is an explicit coordinate-preserving inter-fiber connection law for the full 270-router.

## 4717 — exact finite-capacity envelope, plus explicit queue/erasure models
The exact all-pairs path frontier gives uniform per-edge `(base,shortcut)` loads

`P0=(35,239/3)`,
`P1=(137/3,37)`,
`P2=(155/3,21)`,
`P3=(373/6,0)`.

Normalize base-edge capacity to `C_b=1` and set `rho=C_s/C_b`. PSp averaging reduces the uniform all-pairs max-concurrent-flow problem to the convex hull of those four load vectors. The exact capacity envelope is

- `0 < rho < 63/155`: mix P2-P3, `lambda_max=3(rho+2)/373`;
- `63/155 < rho < 111/137`: mix P1-P2, `lambda_max=3(3rho+8)/1429`;
- `111/137 < rho < 239/105`: mix P0-P1, `lambda_max=3(rho+4)/659`;
- `rho >= 239/105`: P0, `lambda_max=1/35`.

For equal capacities the exact optimum is

`13/80 P0 + 67/80 P1`,

which equalizes both edge-orbit loads at `659/15` and gives

`lambda_max = 15/659`.

Under an explicitly assumed symmetric M/M/1 edge-server model, operation at half this capacity has mean system-time expression `1318/269` in normalized service-time units per source-destination pair. Under an explicitly assumed independent retransmission model, replace capacities by `C_i q_i`; for the example `q_b=199/200`, `q_s=49/50`, `rho_eff=196/199` and the effective normalized demand is `372/16475`.

The capacity theorem is exact for the stated symmetric routing model; queue and erasure extensions are modelling assumptions, not hardware measurements.

## 4718 — outside box: the dual-shell design already contains the 27 Petersen shortcut fibers
Within each of the 27 reconstructed five-point GQ lines there are ten projected three-subsets. Two such triples have intersection size one or two. The two relations are:

- intersection size one: Petersen graph, degree 3, 15 edges per fiber, total `405`;
- intersection size two: `J(5,3)`, the six-regular Petersen complement, total `810` edges.

The 405 intersection-one edges are literally the selected270 shortcut/hot edge set. Thus the dual-shell triangle design already contains the full `27 x Petersen` shortcut fabric before the S3 singular-sheet connection is used; that connection is needed to reconstruct the 1620 cross-fiber base edges.

## 4719 — outside box: the S3 regular closure is a different 270-vertex graph
The full S3 monodromy has a canonical connected regular six-sheet cover over the 45-point base:

- vertices `270`;
- edges `1620`;
- degree `12`;
- deck group `S3`.

The parity of the S3 connection is gauge-equivalent to an all-odd signing; one explicit gauge has 41 packet values zero and 4 packet values one. The map

`(packet,g) -> (packet,g(0), parity(g)+gauge(packet))`

is an explicit isomorphism from the regular closure to the Kronecker/bipartite double cover of selected135.

Its spectrum is

`12^1,6^30,3^44,0^120,(-3)^44,(-6)^30,(-12)^1`.

This graph is bipartite. The 1620-edge selected270 base graph is non-bipartite and has spectrum

`12^1,8^15,(1+sqrt(13))^20,2^84,(-1)^64,(1-sqrt(13))^20,(-4)^60,(-6)^6`.

Therefore the tempting `270 vertices + 1620 edges` identification fails closed: the two graphs are not isomorphic.

## 4720 — outside box: canonical S5-invariant Petersen cycle/cut codes
One 15-edge Petersen fiber has binary vertex-edge incidence rank 9. Its cycle and cut spaces are

`[15,6,5]_2` and `[15,9,3]_2`.

The cycle-code weight enumerator is

`1 + 12 z^5 + 10 z^6 + 15 z^8 + 20 z^9 + 6 z^10`.

The 12 minimum weight-five words are exactly the twelve Petersen 5-cycles. The full Petersen automorphism group has order 120 and preserves both codes, so they are compatible with the already certified local A5 PSp action and S5 PGSp action.

The cycle code corrects every erasure pattern of at most four edge symbols. Exact failure counts begin `12/3003` at five erasures and rise to certainty by ten erasures. Across all 27 Petersen fibers the direct sums are

`[405,162,5]_2` cycle code and `[405,243,3]_2` cut code,

both PSp/PGSp invariant.

This is redundancy, not free capacity: the cycle-code rate is `2/5` and cut-code rate is `3/5`. No fault-free throughput increase or physical threshold is claimed.

## Integration and evidence
- Executable witnesses: `analysis/w33_pass4713_invariant_flag_cohomology.py` through `analysis/w33_pass4720_petersen_network_code.py`.
- Frozen certificates: `data/PART_W33_PASS4713_*` through `data/PART_W33_PASS4720_*`.
- Regression: `tests/test_w33_pass4713_4720_invariant_gq_bundle_flow.py`.
- Exact-regeneration workflow: `.github/workflows/w33_pass4713_4720_invariant_gq_bundle_flow.yml`.
- Shared theorem insert: `analysis/PASS4713_4720_invariant_gq_bundle_flow_insert.tex`, integrated into `w33_paper.tex`, `photonic_holonet.tex`, and `holonet_machine_blueprint.tex` in numerical frontier order.
- Public card/page: `analysis/PASS4713_4720_invariant_gq_bundle_flow_index_insert.html` and `docs/invariant-gq-s3-bundle-capacity-code.html`, registered in the public frontier manifest.
- `docs/index.html` was not rewritten directly; publication uses the registered-card route because connector reads of the giant file truncate.

Evidence discipline: all promoted statements are exact finite group, graph/design, graph-cover/cohomology, ordinary-character/permutation-module, binary-code, or explicitly parameterized network-model statements. No particle, generation, gauge-field, optical-phase, measured-hardware, or fault-tolerance-threshold identification follows from them alone.
