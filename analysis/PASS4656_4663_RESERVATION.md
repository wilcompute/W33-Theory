# Passes 4656–4663 executed outcomes

Canonical continuation after Passes 4648–4655. All five requested fronts and all three outside-box probes are materialized on `master` with executable witnesses, frozen certificates, focused regression/workflow, a shared theorem insert in the three maintained manuscripts, and registered public card/page surfaces.

## 4656 — the global apartment C2 cover has a nonzero cohomology class
Use the labelled Schreier graph on the 810 selected point-line flags for the five deterministic W33 transvections. It has 4050 labelled edges, is connected, and has first Betti number

`4050 - 810 + 1 = 3241`.

The induced 1620-apartment lift is connected. With the lexicographically sorted two-lift section, the voltage cochain has 3414 zero edges and 636 one edges. After spanning-tree gauge fixing, one explicit representative has 918 nonzero cotree coordinates.

Most importantly, the length-six generator word

`g3 g0^-1 g1 g2^-1 g4 g3^-1`

is closed on the 810-flag base but lifts from one apartment sheet to the other. Its voltage evaluation is one. Therefore the apartment deck coordinate represents a nonzero element of

`H^1(Schreier_810; F2)`.

This is a graph-cover cohomology theorem for the stated canonical Schreier graph, not an optical phase claim.

## 4657 — the order-216 triality intersection is 3^{1+2}:Q8
The W33 point stabilizer has order 648 and exact derived-series orders

`648 -> 216 -> 54 -> 27 -> 3 -> 1`.

The order-27 third derived subgroup is nonabelian extraspecial of exponent three: center and derived subgroup both have order 3, and all 26 nonidentity elements have order 3.

For the order-216 derived subgroup, quotienting by this `3_+^{1+2}` radical gives order 8 with element-order census

`1^1 2^1 4^6`,

hence `Q8`. The full order-648 point stabilizer quotient has order 24 and census

`1^1 2^1 3^8 4^6 6^8`,

hence `SL(2,3)=2A4`.

Combining the Pass4649 pair-intersection invariants with the Pass4654 anisotropic-plane/W33-point intertwiner identifies the actual subgroup tower as

`3^{1+2}:Q8 (216) < 3^{1+2}:2A4 (648) < PSp(4,3) (25920)`.

## 4658 — the selected code reconstructs its dual geometry and has full Aut(C)=PGSp(4,3)
For

`C = ker_F2(N^T) = [135,16,30]_2`,

MacWilliams gives the complete dual

`C^perp = [135,119,3]_2`.

There are exactly 270 weight-three dual words. Because `C^perp=row(N^T)`, these are exactly the 270 selected singular lines, so the code reconstructs its own `135_6-270_3` geometry from the dual minimum shell.

For the full coordinate automorphism group, use only code data first. The 36 minimum words and all 432 weight-45 words define a joint-Jacobi pair invariant. The 630 unordered minimum-word pairs split intrinsically into classes of size 270 and 360. The 270 relation is 15-regular. Under the already proved minimum-word-to-W33-spread transport it is literally the spread overlap-4 graph `SRG(36,15,6,6)`, whose full graph automorphism order 51840 was independently certified. The 135 coordinate signatures across the 36 minimum words are all distinct, hence any code automorphism acts faithfully on this 36-graph and

`|Aut(C)| <= 51840`.

Conversely, the explicit outer similitude `diag(1,2,1,2)` together with PSp acts on the selected 135 coordinates, preserves the 270 selected triples and therefore the code, and generates order 51840. Thus

`Aut(C) = PGSp(4,3)`, order `51840`.

The full nonzero dual weight enumerator is frozen in `data/PART_W33_PASS4658_SELECTED_CODE_DUAL_AUTOMORPHISM.json`.

## 4659 — the selected geometry closes the complete 27–36–45 E6 incidence triangle internally
The 27 maximal singular generators and the 36 code minimum supports reproduce the Pass4655 zero-intersection matrix `R` with row degree 16, column degree 12 and rational rank 21. The recovered meeting graph on the 27 is `SRG(27,10,1,5)`.

That graph has exactly 45 triangles, with five through each of the 27 lines. Let `T` be the 27x45 line-triangle incidence. Every triangle meets every double-six in zero or two lines, with exact census

`0^540, 2^1080`.

Let `D` be the 45x36 triangle/double-six disjointness matrix. Then

`T^T R = 2 (J-D)`.

The internal triangle orbit has size 45 and stabilizer order 576. That stabilizer fixes exactly one protected 16-line support, producing a PSp-equivariant bijection from the internally reconstructed triangle 45 to the protected 45. Composing with Pass4616 identifies it with the center-quad/E6-tritangent carrier.

Thus the selected geometry contains a literal internally reconstructed `27 <-> 36 <-> 45` cubic-surface incidence triangle.

## 4660 — topology-aware routing exposes a 27xPetersen shortcut fabric
Exact fractional all-shortest-path routing gives:

- W33: all 240 edges load `5.5`;
- selected135: all 810 edges load `26.833333...`;
- Levi160: all 480 edges load `88`;
- selected270: two exact edge-load classes, 1620 edges at `38.377777...` and 405 edges at `66.155555...`.

The 405 high-load selected270 edges are not arbitrary bottlenecks. They form exactly 27 connected components, each a Petersen graph on 10 vertices. Those 27 ten-vertex components are literally the ten selected lines contained in each of the 27 internal maximal-singular/Schlaefli objects.

Removing all 405 Petersen shortcut edges leaves a connected 12-regular graph with shell

`1,12,67,160,30`,

diameter 4 and edge connectivity 12. Thus selected270 is naturally a robust 12-regular base plus a 27xPetersen shortcut layer.

The hardware sensitivity model uses explicit design assumptions (1 cm edge, binary switch depth `ceil(log2 degree)`) and component-mixed published anchors: 1.77 dB/m waveguide loss, 0.38 dB / 14 us MZI switching, about 1.05 dB / 1.27 ns EO switching, and 98% SNSPD system efficiency. These are sensitivity anchors from separate demonstrations, not a measured integrated Holonet stack. The topology remains Pareto rather than yielding a universal scalar winner.

## 4661 — outside box: the nonsingular 120 has the selector Bose–Mesner algebra on the dual action type
There are 1120 anisotropic binary two-planes in the W33-derived plus-type V8. Under PSp they split into orbits

`40 + 1080`.

The 40-orbit partitions all 120 nonsingular vectors into `40 x 3`. Define relations by same plane, totally orthogonal plane pair, nonadjacent-plane orthogonal pair and nonadjacent-plane nonorthogonal pair. The exact valencies are

`1, 2, 36, 27, 54`.

The complete intersection-number tensor is exactly the historical Pass1355 120-selector matching association algebra.

However, this is deliberately not promoted as the same PSp G-set. The new 40-fiber quotient is the W33 point carrier by Pass4654, while the historical selector fibers are indexed by the 40 isotropic W33 lines. Since the three-fiber relation is intrinsic, an equivariant scheme isomorphism would force the inequivalent W33 point and line actions to be isomorphic. They are not. So the result is an exact Bose-Mesner duality plus an action-level non-identification.

## 4662 — outside box: the binary code alone reconstructs the protected/E6 45
Start from only the code-intrinsic 36-minimum-word Jacobi graph of Pass4658. It has exactly 135 maximal `K4` cliques.

Put an edge between two K4s when they are completely anticomplete in the 36-graph. The resulting graph on the 135 K4s has exactly 135 edges, is 2-regular, and decomposes as

`45 C3`.

For each triangle component, unite its three K4s. The union has size 12 and induces exactly `3 K4` inside the 36-graph; each of the 24 outside vertices has six neighbors into the union. This yields 45 code-intrinsic 12-subsets.

The PSp action is transitive on these 45 unions with stabilizer 576. The stabilizer fixes exactly one protected 16-line support, producing a unique equivariant bijection to the protected 45 and hence, via Pass4616, to the center-quad/E6-tritangent carrier.

The resulting code-only reconstruction chain is

`[135,16,30] code -> 36 minima -> intrinsic SRG(36,15,6,6) -> 135 K4 -> 45 C3 -> protected/E6 45`.

## 4663 — outside box: the apartment duo bit fails to descend to a spread sign, but produces a new incidence
A representative apartment stabilizer `K` has order 16. Its intersections with the 36 spread stabilizers have exact order profile

`1^16, 4^16, 8^4`.

`K` fixes no spread, so there is no PSp-equivariant set map from the 1620 apartments to the 36-spread carrier that could carry the deck sheet into a spread label/sign.

The four order-8 spread cases nevertheless define a natural transported relation. Across all apartments it has shape `1620 x 36`, row degree 4 and column degree 180. But it has only 135 distinct rows, each repeated exactly 12 times: the relation depends only on the selected singular apartment fiber. It therefore factors to a new incidence

`135_4-36_15`.

Under the Pass4658 code-minimum/spread transport, the four spreads in this new row are disjoint from the eight minimum words/spreads containing the same selected singular coordinate. Hence the new `135_4-36_15` incidence is rowwise disjoint from the existing code incidence `135_8-36_30`.

The natural duo-to-spread signing therefore fails closed: the strongest stabilizer coupling is deck-blind rather than a binary phase/sign.

## Integration and evidence
- Executable witnesses: `analysis/w33_pass4656_apartment_c2_voltage_cohomology.py` through `analysis/w33_pass4663_duo_spread_coupling_obstruction.py`.
- Frozen certificates: `data/PART_W33_PASS4656_*` through `data/PART_W33_PASS4663_*`.
- Regression: `tests/test_w33_pass4656_4663_cohomology_code_e6_routing.py`.
- Focused workflow: `.github/workflows/w33_pass4656_4663_cohomology_code_e6_routing.yml`.
- Shared theorem insert: `analysis/PASS4656_4663_cohomology_code_e6_routing_insert.tex`, integrated into `w33_paper.tex`, `photonic_holonet.tex`, and `holonet_machine_blueprint.tex`.
- Public card/page: `analysis/PASS4656_4663_cohomology_code_e6_routing_index_insert.html` and `docs/cohomology-code-e6-petersen-routing.html`, registered in the public frontier manifest.
- `docs/index.html` was not rewritten directly; publication uses the established registered-card route because connector reads of the giant file truncate.

Evidence discipline: all promoted statements are exact finite group, graph, graph-cover/cohomology, binary-code, incidence, or parameterized routing statements. No particle, generation, gauge-field, optical-phase, or measured-hardware identification follows from them alone.
