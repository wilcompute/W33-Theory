# Passes 5016–5023 — executed outcomes

**Date:** 2026-08-13  
**Status:** EXECUTED in exact finite computations; Pass5016 and Pass5017 have executable producers, and all eight passes have frozen certificates/regressions.

## Pass5016 — symmetry/topology factorization of the radius closure

The 1,890 low-shell observables still have character rank 324, so their full relation space has dimension 1,566. The 1,080 sigma-even triangle checks alone have rank 324 and therefore 756 internal relations.

Every one of the 1,080 K4 subgraphs of H36 has all four triangular faces in the sigma-even shell. Their tetrahedral four-face relations form one PGSp orbit and have rank 755. The remaining one-dimensional mod-2 relation class is genuinely global. An explicit 18-triangle representative uses 10 vertices and 27 edges, every edge occurs twice, every vertex link is a cycle, and V-E+F=1. Thus it is a closed triangulated real projective plane and is not in the K4-boundary span.

The 270 octahedral relations are independent because their residual-equator triples are disjoint. Consequently the complete relation count factors as

`1566 = 755 tetrahedral + 1 RP2 + 270 octahedral + 540 residual attachments`.

Equivalently the previous 1,296 post-local deficit is now resolved as `756 + 540`. This sharply symmetry-reduces the distance-173 closure problem but does not complete the final feasibility decision. The rigorous interval remains `134 <= rho(K) <= 173`.

## Pass5017 — the two 60s are opposite nonsplit extensions

Let `L60` be the primitive integral lattice in the real octahedron sector

`ker(X-2I) intersect ker(B_end^T)`.

Its rational dimension is 60. The defining equation kernel becomes singular in small characteristic: its nullities are 174 over F2, 130 over F3, and 60 over F5. A primitive rational nullspace basis has denominator 3 on all 60 generators; the resulting integral lattice reduces with ranks 60, 14, and 60 over F2, F3, and F5 respectively.

The full-PGSp comparison with binary K60 is decisive. The equivariant Hom spaces in both directions are one-dimensional, but their unique nonzero maps have different ranks:

- `L60 -> K60`: rank 14;
- `K60 -> L60`: rank 46.

Both compositions vanish, and both endomorphism rings have dimension one. The rank-14 image agrees exactly with the Pass5010 S14 obtained from the unique V20-to-K60 map. Therefore the modules are not isomorphic. Instead they form opposite nonsplit extensions of the same factors:

`0 -> S14 -> K60 -> Q46 -> 0`,

`0 -> Q46 -> L60 -> S14 -> 0`.

This is the correct cross-characteristic relationship between the real and binary 60-dimensional octahedron sectors.

## Pass5018 — the 200 covers form a rank-19 two-fiber coherent configuration

The 200 nine-tritangent exact covers split under PGSp as 40 W33 point-covers plus 160 incident point-line flag-covers. The ordered orbital algebra has 19 relations:

- 3 point-to-point;
- 4 point-to-flag;
- 4 flag-to-point;
- 8 flag-to-flag.

For a point source the subdegrees are `PP: 1,12,27` and `PF: 4,12,36,108`. For a flag source they are `FP: 1,3,9,27` and `FF: 1,3,3,9,9,27,27,81`.

The 200×45 cover/tritangent incidence matrix U has row weight 9, column weight 40 and rank 25. With A_trit the srg(45,12,3,3) tritangent-intersection adjacency,

`U^T U = 30 I - 10 A_trit + 10 J`,

with nonzero squared singular spectrum `360^1 + 60^24`. Thus its row image is exactly `1 + V24`; the tritangent V20 sector is killed.

## Pass5019 — the 120 Steiner/K3,3 circuits are a saturated V24 code

Orient each of the 120 support-six K3,3 circuits by +1 on one independent tritangent triple and -1 on the other. The resulting 120×45 integer matrix S has rank 24 over Q, F2 and F3. Its Smith form has exactly twenty-four nonzero invariant factors, all equal to one, so the integer row lattice is saturated.

Exactly,

`S^T S = 15 I - 5 A_trit + J = 30 P24`.

Its real kernel is 21-dimensional and equals the raw tritangent-selector image `1+20`. Hence the circuit row space is precisely the canonical tritangent V24.

The binary row code is `[45,24,6]_2` with exactly 120 minimum words, the K3,3 supports. The ternary row code is `[45,24,6]_3` with exactly 240 minimum words, the two signs of the 120 circuit rows.

## Pass5020 — forty local eight-cover cubes glue into the directed-edge carrier

For each W33 line, its three Steiner/K3,3 circuits give eight side choices. The induced local cover graph is exactly

`Q3 = K4,4 minus a perfect matching`.

The forty cubes are edge-disjoint. Globally they form a connected bipartite graph on 40 point-covers and 160 flag-covers with 480 edges. Point-covers have degree 12 and flag-covers degree 3. Every edge has the canonical interpretation

`point-cover r -- flag-cover (p,q)  iff  r in q and r != p`,

so it is literally the directed W33 edge `p -> r` on the unique line q.

The graph spectrum is `±6^1, ±4^24, ±2^15, 0^120`. The 40×200 line/cube-support matrix has 320 ones, row weight 8, point-cover column weight 4, flag-cover column weight 1, full rank 40 over Q/F2/F3, and

`R R^T = 8 I + A_Q43`.

## Pass5021 — the cube complex has exact homology (1,81,40)

Fill the six square faces of each of the forty cubes. The resulting cell counts are

`C0=200, C1=480, C2=240`.

The boundary ranks are `rank d1=199` and `rank d2=200`, giving

`(H0,H1,H2) = (1,81,40)`.

The result is torsion-free. Topologically, the complex is forty cube-boundary 2-spheres glued only at their W33 point-cover vertices. Its attachment graph has 40 point nodes, 40 line-sphere nodes and 160 incidences, hence free cycle rank `160-80+1=81`; each sphere contributes one H2 generator. Equivalently the homotopy type is a wedge of 81 circles and 40 two-spheres.

The 480 one-cells are the directed W33 edges. The 240 square faces are canonically indexed by unordered collinear point pairs, hence by the 240 undirected W33 edges.

## Pass5022 — exact-cover and minimum-circuit frames are the same V24

Center each cover row by subtracting one fifth of the all-ones tritangent vector. If Uc is the centered 200-cover matrix, then

`Uc^T Uc = 60 P24`,

while Pass5019 gives

`S^T S = 30 P24`.

Therefore

`Uc^T Uc = 2 S^T S`.

The 200 exact covers and the 120 signed minimum circuits are two distinct canonical tight frames for the same tritangent V24. Their cross matrix `S U^T` has rank 24 and nonzero squared singular value 1,800 with multiplicity 24.

## Pass5023 — the new 81 is explicitly the old W33 Hodge 81

There is a canonical chain map from the glued-cube complex to the W33 line-triangle complex:

- point-cover `r` maps to W33 point `r`;
- flag-cover `(p,q)` maps to W33 point `p`;
- cube edge `(p,q)-r` maps to the W33 edge `{p,r}`.

Every cube square maps to a four-cycle inside a single W33 K4 line, hence lies in the W33 triangle-boundary span. The induced homology map has rank 81 over both F2 and F3. Since source and target H1 both have dimension 81, it is an isomorphism.

Thus the 81-dimensional cover-cube homology is not a count coincidence: it is an explicit refinement of the canonical W33 line-triangle H1. In particular, over F3 it is the same 81-dimensional homological carrier audited earlier in `analysis/2026-05-18_w33_tqc_hodge_audit.md`.

## Synthesis

1. The radius closure is now factored into one PGSp tetrahedral orbit, one global RP2 class, the 270 octahedral equations, and 540 residual attachments.
2. The two 60-dimensional octahedron sectors are related by opposite nonsplit extensions, not equality.
3. The 120 Steiner minimum circuits and 200 exact covers both realize the same tritangent V24 as tight frames.
4. The 40 local cover cubes thicken the W33 incidence geometry into a 200/480/240 cell complex whose H1 is canonically the existing W33 Hodge 81.
5. This packet is complementary to the parallel Pass5024–5027 cover/line support graph, whose 2-core is the W33 Levi graph.

Pass4959 remains untouched. No covering-radius improvement is claimed without the missing exact feasibility certificate, and no physical identification is inferred merely from a shared finite-module dimension.
