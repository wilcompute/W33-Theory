# Passes 4785–4792 canonical execution ledger

This support-12 grid/cycle/Golay packet was first reserved as 4761–4768 at 2026-08-10 19:28:55Z. A later Track A lane reserved and began using the same numbers at 19:51:02Z. To keep one theorem per canonical pass number, the already-executed mathematics is released canonically as 4785–4792. The original `w33_pass4761_...` through `w33_pass4768_...` source/certificate files are retained only as implementation/provenance aliases. No theorem statement changed in the renumbering.

## Pass 4785 — support-12 thickening even-cycle code

For each of the 1,620 support-12 apartment thickenings, record the 28 edges induced in the 40-vertex/240-edge W33 line-intersection graph `X`.

Exact incidence data:
- 1,620 rows;
- 240 columns;
- row weight 28;
- column weight 189;
- binary rank 200;
- every row is Eulerian and has even edge weight.

Since `dim Z1(X;F2)=240-40+1=201`, the row span is exactly the even cycle hyperplane:

`C_thick = Z1(X;F2) ∩ Even = [240,200,4]_2`.

Its dual is

`C_thick^perp = Cut(X)+<1_E> = [240,40,12]_2`.

The ordinary cut distance is the edge-connectivity 12. The all-edge coset has weight at least 80 from the SRG least-eigenvalue max-cut bound, so the dual minimum remains 12.

## Pass 4786 — unique partner involution and literal protected 45

Pairwise intersections of the 28-edge thickening vectors occur at sizes

`0,1,2,6,7,8,12,16,21`.

Exactly 810 unordered pairs occur at overlap 8, and every thickening belongs to exactly one such pair. This defines a fixed-point-free partner involution.

For every partner pair:
- the two 12-line thickenings meet in 8 W33 lines;
- their source apartments are disjoint;
- their union has 16 W33 lines.

The 810 unions collapse 18-to-1 onto exactly 45 distinct 16-line supports. Each induces `SRG(16,6,2,2)` with eight maximal K4s, hence the 4x4 rook graph `L_2(4)`.

Rebuilding the old protected 45 from the 135 singular apartment fibers gives literal set equality: the support-12 rook grids are the same 45 subsets of the same 40 W33 line coordinates as the protected E6/center-quad/tritangent carrier.

## Pass 4787 — support-12 reconstruction of SRG(45,32,22,24)

The 45 rook-grid supports meet pairwise in exactly:
- 7 lines for 720 pairs;
- 4 lines for 270 pairs.

Declaring intersection 7 adjacent gives `SRG(45,32,22,24)`.

For the 45x40 grid-line incidence matrix `T`:

`TT^T = 12 I45 + 3 A45 + 4 J45`,

`T^T T = 12 I40 + 3 A_dual + 6 J40`.

Ranks:
- `rank_Q(T)=25`;
- `rank_F2(T)=24`;
- `rank_F2(A45)=14`;
- `rank_F2(A_dual)=10`.

Thus the exceptional 45-object transport graph is reconstructed directly from the support-12 minimum shell without importing protected coordinates.

## Pass 4788 — local 36-state rectangle model

Every 16-line rook grid contains exactly 36 support-12 minima. The eight maximal K4s split into two families of four, giving the canonical state space

`C(4,2) x C(4,2)`.

The overlap-8 partner is

`(R,C) -> (R^c,C^c)`.

The four-line complement of a thickening inside the grid is exactly its partner apartment.

Group data:
- PGSp grid stabilizer 1,152;
- PSp grid stabilizer 576;
- each has pointwise kernel 2 on the 16 grid lines;
- induced rectangle actions have orders 576 and 288;
- both induced actions are transitive;
- the partner involution is not in the PGSp image;
- it centralizes the PGSp image;
- adjoining it gives a 1,152-element permutation group on the 36 rectangle states.

The last 1,152 is an extension of the rectangle action and is not asserted to be a new subgroup of PGSp.

## Pass 4789 — dual-line edge carrier is not the point-edge CSS carrier

Both the W33 point graph and the W33 line-intersection graph have 240 edges, but their canonical PSp G-sets are inequivalent.

For a dual-line edge stabilizer of order 108, suborbits are:

on line edges:
`1,1,2,2,18,18,18,18,27,27,54,54`;

on point edges:
`6,6,6,6,54,54,54,54`.

The stabilizer fixes no point edge. Twisting the point action by the PGSp outer involution leaves the obstruction unchanged. Therefore Pass 4785's coordinates are not the existing point-edge CSS/Hodge carrier in disguise.

## Pass 4790 — the 45-grid code recovers point edges as its minimum shell

The row code of the 45x40 rook-grid incidence matrix is

`[40,24,6]_2`.

Its 240 minimum words are exactly

`Star(p) XOR Star(q)`

for the 240 collinear W33 point pairs `p~q`. Hence the point-edge carrier is recovered code-theoretically from line coordinates even though Pass 4789 excludes a coordinate-level PSp bijection.

Algebraically, if `B` is the point-line incidence matrix,

`C45 = B^T(Even point coefficients)`.

The dual is

`[40,16,10]_2 = { y : B y in <1_points> }`.

Its 252 minimum words split exactly into:
- 36 spreads, with point-degree profile `1^40`;
- 216 kernel words, with point-degree profile `0^20 2^20`.

The complete primal and dual weight enumerators are frozen in the canonical certificate.

## Pass 4791 — Golay is the relation code of the 24 Leech-neighbor characters

For the explicit Pass 4699 Leech two-neighbors, define parity characters

`chi_i(x)=(x,v_i) mod 2`,

where `v_i=(1,...,1,3_i,1,...,1)/sqrt(2)`.

Evaluating the 24 characters on an exact generating set of the Golay Construction-A Niemeier lattice gives:
- character span dimension 12;
- relation-space dimension 12;
- relation space exactly equal to the extended binary Golay code `G24`.

Therefore:
- every subset of at most seven neighbor characters is independent;
- the first dependencies have weight 8;
- there are exactly 759 minimum dependencies, the Golay octads.

The corrected sextet supplies 15 explicit octad relations as unions of two tetrads. Its order-138,240 stabilizer is transitive on the 24 neighbors; a neighbor stabilizer has order 5,760 and suborbits `1+3+20`.

## Pass 4792 — characteristic-two deck/parity analogy is not a canonical identification

The quotient `Z1(X)/C_thick` is dual to the all-edge mod-2 cohomology class on the W33 line-intersection graph. A triangle evaluates nontrivially, so the class is nonzero. It is group-fixed in characteristic two. The edge stabilizer contains 54 endpoint reversers, so there is no corresponding invariant characteristic-zero oriented lift.

This parallels the Pass 4745/4752 apartment deck line, which is also fixed in characteristic two and has no invariant rational lift.

However:
- the line-graph base has PSp vertex stabilizer 648;
- the deck base has PSp vertex stabilizer 96.

Neither stabilizer order divides the other. A transitive equivariant base map would require stabilizer inclusion, so there is no PSp-equivariant map in either direction. The two one-dimensional F2 invariants are therefore not promoted to the same cohomology object.

## Release state

- canonical certificates `PART_W33_PASS4785...` through `PART_W33_PASS4792...` are on `master`;
- original 4761–4768 source/certificate names remain as provenance aliases only;
- `analysis/w33_pass4785_4792_canonical_relay.py` re-executes the implementation witnesses and materializes canonical certificates;
- `analysis/PASS4785_4792_support12_grid_cycle_golay_insert.tex` is integrated into `w33_paper.tex`, `photonic_holonet.tex`, and `holonet_machine_blueprint.tex`;
- the public card/page are registered via the extension manifest, and `docs/index.html` was not directly overwritten;
- focused regression tests and a read-only exact regeneration/compile workflow are installed;
- a registry typo introduced during append was caught and repaired before final audit.

Evidence boundary: the full apartment numerical enumerator remains open beyond exact support 12; point-edge and line-edge coordinate carriers remain inequivalent under the canonical action; the rectangle partner extension is not promoted to PGSp; the Golay relation-code theorem is a finite lattice-character statement; and the two characteristic-two parity classes remain distinct cohomology objects absent an explicit functor.