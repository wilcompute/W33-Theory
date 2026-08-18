# Passes 7163–7170 — E8 as a hexagonal lift of W33, the D4/center-quad dictionary, and the q=9 rank boundary

## Scope and prior-art firewall

This packet deliberately separates old ingredients from new bridges.

Prior repo results reused here:

- Pass 85 already proved that the binary adjacency-row code of W(3,3) is `[40,16,8]_2`, with exactly 45 weight-8 words, identified with the 45 tritangent planes.
- Pass 1021 already proved the deterministic six-to-one E8 fibration `240 roots -> 40 W33 points` using the Coxeter `c^5` Eisenstein-unit orbits, and identified the quotient as the W33 point action.
- `exploration/w33_center_quad_gq42_e6_bridge.py` already proved `90 center-quads -> 45 antipodal pairs -> 27 lines`, giving dual GQ(4,2) and the cubic-surface 27/45 layer.
- Passes 7138–7154 reduced the q=9 52-point problem to eight 512-state Gram graphs and identified the `448+64` invertible/rank-one matrix split.

The new content is the objectwise identification among those layers, the E8 root-graph lift law, the induced `[240,16,48]_2` code, the exact D4 dictionary, the Z12 phase cocycle, and exact closure of the 64-state q=9 rank-one boundaries. Nothing below proves `alpha(W(3,9))=51`.

## Pass 7163 — exact q=9 rank-one boundary closure

Write every normalized residual Gram row as

`r=(1,a,b,c) <-> [[1,a],[b,c]]`,  `a,b,c in GF(9)^*`.

The determinant vanishes exactly at `c=ab`, hence the 512 states split as

`512 = 64 rank-one + 448 invertible`.

For the eight anchor types

`(1,1,2),(1,1,3),(1,1,4),(1,1,5),(1,2,3),(1,2,4),(1,3,4),(1,3,5)`,

the 64-node rank-one induced conflict graphs were solved exactly with a deterministic bitset maximum-clique search on their complements. Their exact independence numbers are

`21, 25, 22, 25, 23, 24, 21, 26`.

The known 51-point q=9 witness uses anchor type `(1,3,5)`. After an exact diagonal/permutation gauge transport to the canonical anchor Gram, its 47 residual rows split

`5 rank-one + 42 invertible`.

Thus the witness is very far from saturating the rank-one boundary, but this is a structural constraint only. The full 512-state target-48 decision remains open pending a separate SAT/SDP certificate.

## Pass 7164 — the E8 root graph is a hexagonal lift of the complement of W33

Rebuild the 240 E8 roots in the same integral scaling used by Pass 1021 and let `c` be the deterministic Coxeter element of order 30. The element `d=c^5` partitions the roots into 40 six-cycles, exactly the Pass-1021 Eisenstein fibers.

Use the standard positive-inner-product root graph: two roots are adjacent when their scaled dot product is `+4` (ordinary normalized inner product `+1`). Each root has degree 56.

The six-root fibers have the following exact graph law.

1. Each individual fiber induces one `C6`, hence contributes six root-graph edges.
2. Of the `C(40,2)=780` unordered fiber pairs, exactly 240 have no root-graph edge between them. Those 240 pairs form the quotient SRG `(40,12,2,4)`, i.e. W33 adjacency.
3. The other 540 base pairs are the nonedges of W33. Every such pair carries exactly 12 root-graph edges, every root has degree two into the opposite fiber, and the induced 12-vertex bipartite graph is always a single `C12`.
4. In Coxeter phase coordinates `Z6`, every cross-fiber coupling has difference set exactly `{s,s+1}`.

Therefore the complete E8 root-graph degree decomposes as

`56 = 2 + 27*2`,

and its edges decompose as

`6720 = 40*6 + 540*12 = 240 + 6480`.

This is a much more explicit form of the Pass-1021 fibration: W33 edges suppress the positive-root coupling, while W33 nonedges lift to `C12` cylinders between the two root hexagons.

## Pass 7165 — pull the W33 binary code through the E8 fibration

Replay the Pass-85 code on the 40-point quotient:

`C_2(W33) = [40,16,8]_2`,

with weight enumerator

`1 + 45 z^8 + 1120 z^12 + 15570 z^16 + 32064 z^20 + 15570 z^24 + 1120 z^28 + 45 z^32 + z^40`.

Repeat every base coordinate on the six roots in its Eisenstein fiber. This gives the canonical fiber-constant E8-root code

`C_E8,fib = [240,16,48]_2`,

whose weight enumerator is obtained by multiplying every base weight by six:

`1 + 45 z^48 + 1120 z^72 + 15570 z^96 + 32064 z^120 + 15570 z^144 + 1120 z^168 + 45 z^192 + z^240`.

The dimension does not change because the repetition map is injective.

## Pass 7166 — the two six-fold symmetries fit in one D12 diamond

The old E8 controller theorem distinguishes:

- the internal Eisenstein fiber `C6`, and
- the external minimal controller `S3 = C3:C2`, with the involution acting on `C3` by inversion.

The q=9 witness hexad independently produced `D12`.

These are not three unrelated order-six/order-twelve coincidences. Abstractly

`D12 = <r,s | r^6=s^2=1, srs=r^-1>`

contains the cyclic hexagon `C6=<r>`, has central inversion `<r^3>=C2`, and satisfies

`D12/<r^3> ~= S3`.

Equivalently it also contains an `S3=<r^2,s>` subgroup. Thus D12 is the minimal common symmetry envelope of a cyclic six-state fiber and an inversion-controlled `C3:C2` controller.

This is a group-theoretic bridge only: it does not identify a q=9 witness hexad with an E8 root fiber.

## Pass 7167 — selected-C6 criterion

Let involutions `a,f` act faithfully on a six-object orbit. If `|af|=6` and the stabilizer of one orbit object in `<a,f>` is a reflection `C2`, then

`<a,f> ~= D12`,

and `af` supplies a canonical Hamiltonian `C6` on the orbit.

Consequently, if a larger abstract outer automorphism group forgets this cycle, ambient liftability is equivalent to preserving the selected `C6`. This is exactly what happened in the q=9 `Aut(K3,3)=S3 wr C2` outer code object: six Hamiltonian cycles exist and the geometry selects one.

The theorem is field-independent. The specific q=9 realization with `f` equal to nontrivial field Frobenius is not asserted for prime fields or for every q.

## Pass 7168 — an exact Z12 holonomy from the E8 root fibers

For an oriented W33-nonedge `x->y`, the cross-fiber difference set is `{s,s+1}` in `Z6`. Define its midpoint phase

`phi_xy = 2s+1 mod 12`.

Reversal gives `phi_yx=-phi_xy`. Rephasing a fiber origin by `a_x in Z6` changes

`phi_xy -> phi_xy + 2(a_y-a_x)`,

so cycle sums are gauge-invariant modulo 12.

The complement of W33 contains exactly 3240 triangles. The exact triangle-holonomy histogram is

- `+1 mod 12`: 1440,
- `-1 mod 12`: 1440,
- `+3 mod 12`: 180,
- `-3 mod 12`: 180.

No physical gauge-field interpretation is asserted. The point is purely finite: the E8/W33 fibration canonically produces a nontrivial `mu_12`-valued cycle phase, independently of the repo's separate Clifford `mu_12` theorem.

## Pass 7169 — the 90 center-quads are literally 90 D4 root subsystems

This is the strongest objectwise closure in the packet.

Every one of the 45 minimum weight-8 words induces `K4,4` on its eight W33 support points. Its two bipartition classes are four-point independent sets, giving 90 halves in total.

Compute the center-quads independently from the W33 graph as the four common neighbors of a pairwise noncollinear triple. The two 90-element sets agree exactly:

`{90 minimum-word halves} = {90 center-quads}`.

Now lift one four-point half through the Pass-1021 six-root fibration. It gives 24 E8 roots. For all 90 halves, exact rational row reduction verifies:

- the 24 roots span a four-dimensional rational subspace,
- each root has positive-root-graph degree 8 inside the 24-set,
- the only E8 roots lying in that four-space are those same 24 roots.

Hence every half is an actual `D4` root subsystem, not merely a 24-vertex graph with D4-like parameters.

The existing center-quad involution pairs every center-quad with its four common neighbors. Under the E8 lift, the two corresponding D4 root systems are exactly orthogonal. Thus

`90 center-quads = 90 D4 subsystems`,

and

`45 antipodal center-quad pairs = 45 selected orthogonal D4 + D4 subsystems in E8`.

Objectwise, the union of each pair is exactly one of the 45 weight-8/tritangent supports.

## Pass 7170 — the old 90->45->27 E6 quotient becomes an E8 D4 partition geometry

The prior center-quad bridge proved that the 45 paired eight-point supports form the points of dual GQ(4,2), and that its 27 lines are five-tuples of disjoint eight-point supports partitioning all 40 W33 vertices.

Translate the new D4 dictionary through the six-root fibration:

`90 D4 -> 45 (D4 orthogonal D4) -> 27 five-packs`.

Each of the 27 five-packs partitions all 240 E8 roots into five disjoint 48-root `D4+D4` supports. Every one of the 45 selected `D4+D4` supports lies on exactly three such partitions, reproducing the `5 points/line, 3 lines/point` incidence of GQ(4,2).

The 27-line / cubic-surface interpretation is prior repo work. What is new here is that its 45 quotient points now have a concrete E8 root-system meaning as selected `D4+D4` subsystems.

## Exact boundary

The packet proves finite geometry/root-system/code statements only. It does not prove a physical E8 unification, does not identify the new q=9 witness hexads with E8 fibers, and does not close the q=9 51-vs-52 problem. The exact residual target remains the eight 512-state target-48 decisions or an equivalent coherent-algebra upper certificate.
