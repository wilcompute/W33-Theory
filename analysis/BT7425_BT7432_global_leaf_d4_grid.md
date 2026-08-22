# Passes 7425–7432 — global Eisenstein leaf design, the D4 4×4 A2 grid, and the q=9 radius-nine frontier

## Boundary first

This packet starts from already-certified ingredients rather than reclaiming them.

- Pass7401–7424 owns the global `1120 A2 / 11200 4A2 / 2240 Eisenstein W33 leaves` geometry and its rank-five Weyl association scheme.
- Pass7182 owns the exact census of `3150 D4` subsystems and the selected 90-D4 leaf geometry.
- Pass4964 owns the unique equivariant `36 W33 spreads <-> 36 cubic-surface double-sixes` bridge.
- Pass5300 owns the exact Hoffman-576 result: the order-576 Hoffman stabilizer is **not** the full Klein-Latin autoparatopy group, but its central quotient is the order-288 even-parastrophe subgroup.
- Pass7180 owns q=9 target-48 exclusion through invertible-core deletion radius eight.

The new work below composes and globalizes those objects. It does **not** claim `alpha(W(3,9))=51`, and it does not assign continuum/particle/hardware meaning to finite carriers.

---

## Pass7425 — all 2240 W33 leaves form one exact V300 tight frame

Let `B` be the `2240 x 1120` incidence matrix whose rows are the forty A2 subsystems in each Eisenstein W33 leaf.

The global A2 association scheme has nontrivial valencies

`120, 648, 270, 81`.

Inside one W33 leaf, the stabilizer is transitive on its `240` collinear/orthogonal pairs and on its `540` noncollinear pairs. Therefore all noncollinear pairs occurring in one leaf must belong to one global Weyl orbital.

A fixed A2 lies in 80 leaves. Counting its 39 companions over those leaves gives

`80*39 = 3120`.

The 120 orthogonal A2s each lie with it in eight leaves, contributing `960`. Hence nonorthogonal pair incidences contribute `2160`. Of the three global nonorthogonal valencies,

`2160/648`, `2160/270`, `2160/81`

only the middle one is integral:

`2160/270 = 8`.

Thus two A2s share an Eisenstein W33 leaf iff they are in the global valency-120 or valency-270 relation, and in either case exactly eight leaves contain the pair.

Therefore

`B^T B = 80 I + 8(A_120 + A_270)`.

Evaluating this in the exact Pass7417 first eigenmatrix gives

`3200^1 + 288^300 + 0^819`.

So

`rank_R B = 301`

and the column module is exactly

`1 + V300`.

After centering each leaf indicator by subtracting `1/28` of the all-ones vector,

`C^T C = 288 P_300`.

Hence the 2240 centered leaf indicators are an exact tight frame for the irreducible 300-dimensional Weyl constituent.

---

## Pass7426 — the 4×4 grid is literally inside every D4

Build the D4 root system as the 24 vectors

`+-e_i +-e_j`, `i<j`.

Enumerating root-closed A2 hexagons gives exactly 16 A2 subsystems.

Two such A2s either

- share one antipodal root pair, or
- have disjoint six-root sets.

Joining the disjoint pairs gives

`SRG(16,6,2,2)`.

The graph has eight maximal K4s and therefore is the `4 x 4` rook graph `L2(4)`. Each of those eight K4s consists of four pairwise root-disjoint A2s whose union is **all 24 D4 roots**. Thus the eight rows/columns of the rook model are exactly the eight root-set decompositions

`D4 roots = A2 sqcup A2 sqcup A2 sqcup A2`.

The graph also has exactly 24 maximum cocliques, the 24 transversals of the 4×4 grid. There are exactly 24 partitions of the 16 cells into four transversals. Labeling those four classes gives

`24 * 24 = 576`

Latin squares of order four.

The full graph automorphism group is

`S4 wr C2`, order `1152`,

the full D4 root-system automorphism group. Its row/column-preserving subgroup is

`S4 x S4`, order `576`.

The two occurrences of 576 here are therefore internal consequences of the **same** 4×4 D4 object.

---

## Pass7427 — the certified 64 leaves through D4 resolve as an 8×8 chart

The Weyl group `W(D4)` has order 192. On the eight A2-root partitions above, its induced permutation image has order 96; the central `-I` fixes every A2 subsystem and lies in the kernel. The action is transitive, with partition stabilizer order 24.

Globally every E8 D4 lies in exactly 64 Eisenstein leaves. Its orthogonal complement is another D4 and every containing leaf selects

- one of eight A2-root partitions of `D4`, and
- one of eight A2-root partitions of `D4^perp`.

The stabilizer acts transitively on the `8 x 8` product: the quotient moves the first partition and the complementary D4 Weyl kernel moves the second. Since both the leaf set and partition-pair set have size 64, the equivariant map is a bijection.

Therefore

`64 leaves through D4 <-> 8 x 8 root-partition pairs`.

The natural relation “same D4 partition on either side” is the rook graph

`L2(8) = SRG(64,14,6,2)`.

Important firewall: these eight D4 root partitions are **not** the same W(D4)-set as the eight orientation leaves through an orthogonal A2^4. The root-partition action factors through order 96, while Pass7409 certified a faithful order-192 affine action on the orientation fibre.

---

## Pass7428 — the Hoffman/Latin bridge now has an E8 carrier

For the Klein V4 Latin square, represent a cell by

`(row, column, symbol=row xor column)`.

Join two cells when row, column **and symbol** are all distinct. The resulting graph is again

`SRG(16,6,2,2) = L2(4)`

and has eight K4s, exactly the eight Latin transversals.

An explicit graph isomorphism transports this 16-cell object to the 16 A2 subsystems inside D4. All 576 Klein autoparatopies preserve this graph, giving an index-two subgroup of the full 1152-element D4 A2-grid automorphism group.

Composing with Pass5300 gives the exact chain

`H/Z(H) ~= L+ < AutPar(V4 Latin) < Aut(A2(D4))`

with orders

`288 < 576 < 1152`.

This is the first direct E8/D4 carrier for the user's Hoffman/Latin intuition.

It does **not** undo Pass5300's negative theorem: `H` itself is not the full order-576 Latin autoparatopy group. The exact bridge remains through `H/Z(H)` and the even-parastrophe subgroup.

---

## Pass7429 — 80,640 global double-six charts

Pass4964 already solved the local 36-to-36 question: in every W33 leaf there is a unique `PGSp(4,3)`-equivariant bijection between its 36 spreads and the 36 cubic-surface double-sixes.

Globalizing over 2240 leaves gives

`2240 * 36 = 80,640`

leaf-spread/double-six charts.

Since

`|W(E8)| = 696,729,600`,

the chart stabilizer has order

`696729600 / 80640 = 8640`.

Every global A2^4 line is in eight leaves and in nine spreads within each leaf, hence in

`8*9 = 72`

global charts.

Every global A2 point lies in `80*36=2880` charts.

Pass4965 gives three Steiner triples per W33 line. Hence the global number of Steiner chart objects is

`2240*120 = 268,800`,

and every global A2^4 line supports

`8*3 = 24`

such objects.

No global cubic surface embedded in E8 is asserted; these are canonical **local chart labels** transported over the Weyl leaf orbit.

---

## Pass7430 — a seductive 24=24 identification fails

There are 24 global Steiner chart slots over a fixed A2^4 line:

`8 leaves x 3 Steiner triples`.

The local abstract symmetry has order 192, making it tempting to identify those 24 slots with the 24 D4 roots.

That is false.

The characteristic normal elementary abelian `2^3` subgroup has orbit structure

`8 + 8 + 8`

on the 24 Steiner slots, because it acts regularly on the eight leaves while fixing the Steiner-triple label.

On the actual D4 roots, the normal even-sign `2^3` subgroup preserves coordinate-pair support and has

`4 + 4 + 4 + 4 + 4 + 4`.

Equivalently the point stabilizer meets the normal 2^3 trivially on the chart carrier but in order two on the root carrier.

Therefore the two degree-24 W(D4)-sets are inequivalent.

---

## Pass7431 — q=9 target 48 excluded through radius nine

Pass7180 excluded target 48 through eight deletions from the known 42-state invertible residual core in canonical anchor type `(1,3,5)`.

The exact same blocker-mask/color brancher at deletion radius nine has

- remaining core: 33;
- required compatible additions: 15;
- candidate pool: 469;
- search nodes: `2,535,139`;
- result: **UNSAT**.

Thus any hypothetical residual 48-clique must delete at least ten of the known 42 invertible-core states.

Radius ten was attempted with the straightforward brancher but did not close inside the local execution budget. It is therefore left open rather than inferred.

This is still only a canonical-anchor basin theorem. `alpha(W(3,9))=51` is not claimed.

---

## Pass7432 — the leaves form a spherical 2-design in R^300

Normalize the centered leaf vectors from Pass7425. Since their sum is zero and

`C^T C = 288 P_300`,

the 2240 unit vectors form a spherical 2-design / finite unit-norm tight frame in dimension 300.

The unit-norm frame bound is

`2240/300 = 112/15`.

A useful integral realization is

`y_L = 28 1_L - 1`.

Every vector has

- 40 entries equal to 27;
- 1080 entries equal to -1;
- norm squared `30240`;
- total vector sum zero over all 2240 leaves.

If two leaves intersect in `t` global A2 subsystems,

`<y_L,y_M> = 112(7t-10)`

and the normalized angle is

`(7t-10)/270`.

Thus global leaf intersections become quantized angles in one irreducible 300-dimensional Weyl module.

---

## Literature/prior-art audit

A standard reflection-subgroup census for `W(E8)` already records the raw subsystem counts

- `1120 A2`,
- `3150 D4`,
- `11200 4A2`.

Those counts are not claimed as new. The novel repo-level content in this packet is the **incidence composition**: the V300 leaf frame, the internal D4 16-A2 rook/Latin carrier, the 8×8 leaf coordinatization, and the composed Hoffman/cubic-surface globalizations.

The same census contains an `A1+A2+A5` reflection subgroup of order 8640. This equals the new global chart stabilizer order, but its subsystem orbit size is 40320 while the chart orbit has 80640 elements. That is recorded only as a future two-sheet/orientation test, not as an identification.
