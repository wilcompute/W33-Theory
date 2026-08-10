# Passes 4640–4647 executed outcomes

Canonical collision-free D4/Schläfli/spread/holonomy continuation. The mathematics was first developed in transient Pass4592–4599 filenames while a parallel paired-axis/Golay lane was expanding into that range; `analysis/PASS4592_4599_D4_PACKET_NAMESPACE_COLLISION.md` marks those helpers noncanonical. The theorem/data/test/public/manuscript surfaces below use only Passes 4640–4647.

## 4640 — degree-27 half-spinor orbit = Schläfli/cubic-line carrier
The unique degree-27 orbit has point stabilizer order `960`, subdegrees `[1,10,16]`, and its degree-16 orbital is exactly `SRG(27,16,10,8)` with spectrum `16^1,4^6,(-2)^20`. The identification is therefore by the actual PSp(4,3) action, not by 27=27 cardinality.

## 4641 — explicit split-octonion D4 triality and type-preserving normalizer
In the split-octonion Zorn model over F2, the norm `N(a,b,u,v)=ab+u·v` is exhaustively multiplicative on all 65,536 ordered pairs. The 135 nonzero singular vectors have 135 distinct left and 135 distinct right annihilators, each of size 16; together they exhaust all 270 maximal totally singular four-spaces. An explicit hyperbolic coordinate transport identifies these with the W33-derived plus-type V8, and `P(x) -> LAnn(x) -> RAnn(x) -> P(x)` preserves all three outer-type incidence relations with zero failures.

Separately, the PSp type-preserving building centralizer is `C3`. The W33 outer similitude is an involution inverting this C3. The generated normalizer has structure `(3 x PSp(4,3)):2`, order `155520`, and quotient `S3` over PSp. The type-cycling triality and type-preserving normalizer are logically distinct.

## 4642 — selected `135_6–270_3` integral/coherent algebra
For the `135 x 270` selected point-line incidence matrix N:
- `rank_Q(N)=120`;
- `rank_F2(N)=119`, while F3/F5/F7/F11 rank is 120;
- Smith nonzero profile is `1^119,2^1`, with 15 zeros;
- `coker(N)=Z^15 + Z/2`.

Thus exactly one Smith invariant 2 explains the entire one-dimensional binary rank drop. The PSp point action yields a noncommutative rank-9 Schurian coherent configuration with subdegrees `1,1,1,12,12,12,32,32,32`.

This pass also corrected Pass4589: the selected-line graph spectrum is `15^1,9^15,6^20,3^60,0^24,(-3)^150`. The previous `(-3)^165` expression double-counted the 15-dimensional point-gram nullity. The original Pass4589 verifier and regression were both repaired.

## 4643 — simultaneous three spread sheets
The three degree-36 half-spinor PSp-orbits are three genuine copies of the 36 W33 spreads: a representative stabilizer has order 720 and fixes exactly one spread, giving a unique equivariant bijection for each sheet. The PSp building-centralizer C3 cycles the three sheets and the PGSp involution supplies a transposition; together the type-preserving normalizer realizes S3 on the copy fiber.

## 4644 — Holonet routing falsifier
The selected point graph is 12-regular on 135 vertices, diameter 3, shell profile `[1,12,56,66]`, and vertex/edge connectivity 12. The selected-line graph is 15-regular on 270 vertices, diameter 3, shell profile `[1,15,118,136]`, and vertex/edge connectivity 15. These beat the 160-flag Levi line graph on unweighted hop diameter/connectivity at larger address count, while W33 remains the stronger compact 40-address mixer. Optical loss, switching latency, detector noise, weighted coupler cost and fault-tolerance thresholds remain outside the finite graph comparison.

## 4645 — flat rank-50 triality Fourier holonomy
For centered triality incidence maps `D_ij=9M_ij-J`, `D D^T=54^2 E_50` and `D_PA D_AB=54 D_PB` cyclically. After normalization by 54, a complete three-leg cycle is exactly the identity projector on each active rank-50 constituent. There is no hidden finite phase in this incidence algebra.

## 4646 — triple Schläfli/double-six weld
For the degree-27 orbit X and any of the three degree-36 sheets Y, the natural relation `|X∩Y|=1` yields a `27 x 36` incidence matrix R with row degree 16, column degree 12, rational rank 21, and exact Gram identities
`RR^T=10I+2A27+6J` and `R^TR=6I-2A36+6J`. These are exactly the frozen classical Schläfli-line/double-six identities from Passes4545–4549.

After indexing all three sheets by their unique PSp-equivariant maps to the same W33 spread carrier, `R1=R2=R3` literally. The combined matrix `[R R R]` has rank 21; its 72-dimensional sheet-difference sector is dark, and the full kernel has dimension 87.

## 4647 — apartment six-sheet cover has D12 monodromy
The `1620 -> 270` apartment map is the homogeneous cover `G/K -> G/H` with `|G|=25920`, `|K|=16`, `|H|=96`, and fiber size 6. The local six-sheet monodromy image is the dihedral group D12 of order 12, with element-order census `1^1 2^7 3^2 6^2`. The six sheets have a natural `3 x 2` block system: three selected-line points, two apartment lifts over each point-line flag. The block quotient is S3, while the kernel is the central C2 half-turn, acting fixed-point-freely by swapping the two lifts in every block.

## Integration/evidence
- Canonical certificates: `data/PART_W33_PASS4640_*` through `data/PART_W33_PASS4647_*`.
- Executable split-octonion verifier: `analysis/w33_pass4641_split_octonion_triality.py`.
- Corrected legacy verifier: `analysis/w33_pass4589_apartment_selected_singular_graph.py`.
- Regression: `tests/test_w33_pass4640_4647_d4_schlaefli_spread_holonomy.py`.
- Focused evidence workflow: `.github/workflows/w33_pass4640_4647_d4_schlaefli_spread_holonomy.yml`.
- Theorem insert: `analysis/PASS4640_4647_d4_schlaefli_spread_holonomy_insert.tex`, integrated into `w33_paper.tex`, `photonic_holonet.tex`, and `holonet_machine_blueprint.tex`.
- Public card/page: `analysis/PASS4640_4647_d4_schlaefli_spread_holonomy_index_insert.html` and `docs/d4-schlaefli-spread-holonomy.html`, registered in the public frontier manifest.
- Direct `docs/index.html` rewriting was deliberately avoided because the connector truncates that giant file; publication uses the established registered-card/standalone-page route.

Evidence boundary: all promoted statements are finite incidence, group-action, representation, integral linear-algebra, routing-graph, or cover-monodromy results. No physical particle/generation/spinor, optical phase, or hardware-performance claim follows without separate dynamics or measurements.
