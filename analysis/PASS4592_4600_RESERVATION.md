# Passes 4592--4615 paired-axis / Golay execution ledger

This packet executed the user's five queued fronts, three independent outside-the-box probes, and the additional user-directed investigation of the two Pass4575 self-orthogonal cubic incidence axes against the repository's Golay work.

A parallel lane independently reserved 4592--4599 after this lane had already reserved 4592--4600. Passes4592 and4593 here were already committed, so the remaining queued tasks were moved collision-safely to Passes4601--4606. The Golay/MOG result briefly used 4607 before the parallel lane's earlier 4607--4614 reservation surfaced; it was canonically moved to Pass4615 and the collided 4607 alias was deleted. The canonical results are therefore 4592,4593,4601--4606,4615.

## User-directed paired-axis / Golay result — Pass4592

The two Pass4575 self-orthogonal codes are complementary evaluations of one six-dimensional space:

- `C36=[36,6,16]` on the 36 anisotropic vectors;
- `C27=[27,6,12]` on the 27 nonzero singular vectors.

Using the same `x in F2^6` on both axes and concatenating gives exactly the binary simplex code `[63,6,32]`, with enumerator `1+63 z^32`; its dual is the Hamming code `[63,57,3]`. The 63 coordinates are all nonzero vectors of `F2^6=PG(5,2)` and the 27+36 split is precisely the minus-quadratic coloring. Forgetting that coloring enlarges the coordinate symmetry from the `O^-(6,2)=PGSp(4,3)` color-preserving action to the full simplex `GL(6,2)` action.

Choosing a compatible `F4^3` structure turns the same six binary message dimensions into the standard hexacode `[6,3,4]_4`. Concatenating each F4 symbol with binary `[3,2,2]` gives `[18,6,8]` with enumerator `1+45 z^8+18 z^12`. The repository's explicit cyclic extended binary Golay `G24` contains an exact six-generator subcode that vanishes on six coordinates and, on its eighteen active coordinates, is mapped word-for-word to this binary hexacode concatenation by a frozen coordinate permutation. This is a genuine code embedding, not a count match.

## Five queued fronts

- **Pass4593 — apartment enumerator:** complete exact support-10 census. All `C(40,10)=847,660,528` ten-row subsets were evaluated. There are 147 weights, minimum 582 with multiplicity 2160 and maximum 1080 with multiplicity 36. Complete labelled support spectra are now exact through support ten. The full `[1620,39,162]` numerical enumerator remains OPEN for supports 11--20.
- **Pass4601 — S186 extensions:** one explicit eleven-factor composition series is closed:
  `0<14<54<60<74<80<120<126<134<140<146<186`, with ordered simple factors `14,40,6,14,6,40,6,8,6,6,40`. This refines the already closed multiset `40^3+14^2+8+6^5`. The full unlabeled submodule/Ext/radical-socle lattice remains OPEN.
- **Pass4602 — C8 phase boundary:** the Pass4573 `GQ(2,2)` collision is exceptional at the first exact anchors. Exhausting every four-line support of `Q^-(5,2)=GQ(2,4)` shows exactly 1080 supports with primitive-C8 degree-four coefficient 60, exactly the 1080 apartments. Thus exact anchors are GQ(2,2) FAIL, GQ(2,4) SUCCEED, GQ(3,3) SUCCEED. A symbolic all-(s,t) criterion remains OPEN; universal C6->line adjacency->induced C4 remains exact.
- **Pass4603 — apartment-fiber scheme:** the five cross-fiber values `n2 in {0,2,6,12,48}` plus the diagonal form a symmetric five-class association scheme on 135 points, with valencies `[1,24,12,32,64,2]`. The `n2=48` relation is `45 K3`; quotienting those triples and joining the `6*n2=12+3*n2=6` cross-pattern gives `SRG(45,32,22,24)`.
- **Pass4604 — unary protected/cubic bridge:** the degree-three search is superseded by an all-degree G-set obstruction. Protected V8 nonzero orbits have sizes 135,120; cubic U6 nonzero orbits 27,36. The only arithmetically possible nonzero orbit map, 135->27, would require a block of size five, but the actual singular-point stabilizer has suborbits `1,1,1,12,12,12,32,32,32`, so no such block exists. Every unary PSp(4,3)-equivariant set map V8<->U6 is zero. The known exterior-square bridge survives because it is two-input.

## Three outside-the-box probes

- **Pass4605 — symplectic enlargement:** forgetting the quadratic color on the fused 63-point carrier and retaining the polar form gives `SRG(63,32,16,16)`, the Sp(6,2) symplectic graph. `|Sp(6,2)|=1,451,520`; the color-preserving `O^-(6,2)` subgroup has order 51,840 and index 28. The 64 quadratic refinements split 28 minus / 36 plus.
- **Pass4606 — periodic complex / CSS:** `RR^T=R^TR=0` makes `R,R^T` a genuine two-periodic differential. Its homology dimensions are 24 and 15. The two axes yield CSS `[[36,24,3]]` and `[[27,15,3]]`; the fused simplex/Hamming pair yields `[[63,51,3]]`, the binary quantum Hamming code for m=6. The 24/15 equality with W33 spectral multiplicities is recorded only as an equivariant-comparison target.
- **Pass4615 — Golay/MOG completion:** the 45 weight-8 words of the embedded `[18,6,8]` section are Golay octads. Pair frequencies on its 18 active coordinates reconstruct six disjoint K3 inner-code triples. Exhausting all `6!=720` assignments of the six zero Golay coordinates to those triples gives exactly one assignment whose six tetrads form a Golay sextet (all 15 pairwise tetrad unions are Golay octads). Thus the ambient G24 uniquely completes this six-dimensional section to a MOG/sextet in the repository coordinate model.

## Release state

- The theorem insert is `analysis/PASS4592_4615_paired_axes_golay_enumerator_scheme_insert.tex` and is chained into `w33_paper.tex`, `photonic_holonet.tex`, and `holonet_machine_blueprint.tex`.
- Public card/page are `analysis/PASS4592_4615_paired_axes_golay_index_insert.html` and `docs/apartment-paired-axes-golay.html`, registered through the safe public extension manifest; `docs/index.html` is not directly overwritten.
- Frozen regression tests and a read-only evidence workflow are installed at `tests/test_w33_pass4592_4615_paired_axes_golay.py` and `.github/workflows/w33_pass4592_4615_paired_axes_golay.yml`.
- The Golay bridge is a code embedding after a chosen F4 structure. It is not an embedding of `O^-(6,2)` into `M24`; group orders already forbid that interpretation.

Evidence discipline remains strict: exact executable theorem/certificate or explicit bounded OPEN frontier; no count-only sporadic, lattice, physics, or hardware identification.