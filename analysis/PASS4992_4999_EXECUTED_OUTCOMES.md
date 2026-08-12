# Passes 4992–4999 — executed outcomes

**Date:** 2026-08-11  
**Status:** EXECUTED exactly in committed producers/certificates; dedicated remote replay is reported separately.

## Pass 4992 — octahedral shell algebra reaches beyond radial moments

The 270 tritangent-pair octahedra now carry three simultaneous partitions of the same twelve H36 edges:

- four edge-disjoint sigma-even weight-three dual checks;
- four edge-disjoint sigma-odd Steiner triangles;
- three edge-disjoint residual weight-four equators.

The four even faces partition all 1080 weight-three checks exactly once. The 120 odd Steiner triangles each occur in nine octahedra. The three equators partition all 810 residual A4 checks exactly once.

For character signs `t_i` on the four even faces and `q_j` on the three equators,

`prod_i t_i = prod_j q_j = chi(all 12 octahedral edges)`.

The octahedral Boolean algebra also gives exact distinct restricted subshells:

- 1620 weight-six words from even-face pairs;
- 1080 weight-nine words from even-face triples;
- 810 weight-eight words from equator pairs;
- 270 weight-twelve full-octahedron words.

For a hypothetical distance-173 coset, the Pass4951 third-moment inequality forces `T3 <= -704`, hence at most 188 positive A3 signs. Consequently at most 188 octahedra can have negative top product, forcing the restricted weight-twelve sum to satisfy `U12 >= -106`; the residual-equator A4 sum satisfies `U4 >= -646`.

These are genuine non-radial shell constraints, but they do not yet control the complementary portions of the A4/A6/A8/A9/A12 shells strongly enough to lower the rigorous interval `134 <= rho(K) <= 173`.

## Pass 4993 — exact erasure distance of the 85-reader is eight

Let `R=[C^T;M]` be the 85x36 line-plus-tritangent reader from Pass4987.

For the 45-vertex tritangent intersection graph, let `N` be the 27x45 cubic-line/tritangent incidence matrix. Then

`N^T N = 3I + A_T`.

If two cubic-surface lines intersect, each lies on five tritangents and their stars share one tritangent. The difference of the two star vectors therefore has support eight and is an eigenvalue-three vector of `A_T`. There are exactly 135 distinct such support-eight failures.

The lower bound is exact as well:

- in the mean-zero tritangent V20 sector, a support at most seven would require a connected induced component with eigenvalue 3; exhaustive graph-atlas classification through seven vertices shows any such component has 3 as its Perron root, making the required outside cancellation impossible;
- in the line V15 sector, no connected graph on at most seven vertices has eigenvalue -4;
- for nonzero mean, both reader blocks must be nonzero dominating supports in degree-12 graphs, and each needs at least four coordinates.

Therefore

`d_erasure(R) = 8`.

Every seven-sensor erasure is correctable; an eight-sensor erasure can destroy rank.

## Pass 4994 — the residual affine ambiguity is a C3 torsor

Pass4991 organized the twelve local AG(2,3) completions as four canonical triples indexed by the four points of the base W33 line. After choosing one of those points/triples:

- the PSp line-and-point stabilizer has order 162;
- its image on the residual triple is exactly `C3=A3`, with kernel 54;
- the full PGSp line-and-point stabilizer has order 324;
- its image is the full `S3`, again with kernel 54.

Thus the remaining three-state ambiguity is a canonical C3 torsor. The outer quotient `PGSp/PSp = C2` is exactly the permutation-parity quotient `S3/C3` on that residual triple, matching the finite Witting phase sign at the group-action level.

This still does **not** pick one completion and does not identify the finite outer sign with physical CP.

## Pass 4995 — the residual-equator chain complex exposes a 30-layer

Over F2, H36 has 36 vertices, 360 edges, edge-boundary rank 35, and graph cycle-space dimension 325.

The 810 residual squares have boundary rank 294. Every square uses four edges and every H36 edge lies in exactly nine residual squares. The square-only 2-complex therefore has

`H0=1, H1=31, H2=516`.

The 1080 sigma-even triangle checks have boundary rank 324, giving

`H0=1, H1=1, H2=756`.

Adding both families does not increase boundary rank beyond 324. Hence the exact invariant filtration is

`294 < 324 < 325`,

with quotient dimensions

`30, 1`.

The square complex leaves 31 one-cycle classes; the triangle checks kill exactly 30, leaving the single switching-parity class. The new 30-dimensional binary quotient is real, but it is not identified with the real `15_p (+) 15_l` Levi nullspace merely because the dimensions agree.

## Pass 4996 — fail-closed stale-claim firewall

`tools/w33_stale_claim_firewall.py` now scans live markdown, TeX, HTML, Python, JSON, GAP and text surfaces for a narrow set of already-retracted claims:

- the fabricated 33-vertex SRG identification;
- the superseded Ihara discriminants;
- the old point/line-correlation statement;
- a Witting CP2 ambient claim;
- Witting = Q43/Steiner identification;
- an outer automorphism exchanging the 24- and 15-dimensional adjacency eigenspaces.

Only explicit historical/erratum paths are allowlisted. The firewall also positively asserts that the corrected Ihara factors, exact critical group, and Pass4986 no-correlation certificate remain present. The frozen scan has zero non-allowlisted violations; the dedicated workflow reruns this against the whole clean checkout.

This is intentionally a targeted regression firewall, not a claim that every sentence in the repository has been globally re-proved.

## Pass 4997 — bonkers: H36 checks project canonically onto Q43 geometry

There is a literal binary projection from the 360 H36 edge coordinates to the 40 W33-line/Q43 coordinates:

`H36 edge {S1,S2} -> the unique W33 line in S1 intersection S2`.

Under this map:

- the 1080 sigma-even H36 triangle checks map bijectively to the 1080 zero-center independent triads of Q(4,3);
- the 810 residual A4 squares map three-to-one onto 270 distinct independent four-sets;
- those 270 four-sets are exactly the size-four intersections of W33 spread pairs with overlap four.

The triangle-image span has binary rank 40. The square-image span has rank 30. The Q43 adjacency code has dimension 10, and the square image is exactly its orthogonal complement.

Therefore the 30-dimensional quotient from Pass4995 has a canonical surjection onto a ten-dimensional target,

`30 -> 10`,

with kernel dimension 20. Equivalently the target is the dual functional space of the `[40,10,12]` Q43 binary adjacency code.

This is the first explicit map resolving the new 30-layer; no unrelated real representation is inferred from the dimensions.

## Pass 4998 — bonkers: the 135 pure-tritangent minimum cocircuits are exactly 2K4

The tritangent SRG contains exactly 135 K4 subgraphs. For each intersecting pair of cubic lines, remove their one common tritangent from the two five-tritangent stars. The remaining eight tritangents induce two disjoint K4 components with no cross edges.

There are exactly 135 such supports. Conversely, there are exactly 135 pairs of disjoint nonadjacent K4s, and their unions are exactly the star-difference supports.

Thus the pure mean-zero V20 support-eight cocircuits are completely classified:

`minimum tritangent cocircuit = 2 K4`,

canonically indexed by the 135 intersecting pairs of cubic-surface lines.

Mixed line-plus-tritangent support-eight cocircuits are not classified by this pass.

## Pass 4999 — bonkers: the 270 octahedra form a rank-120/rank-90 edge frame

Let `O` be the 270x360 incidence matrix of tritangent-pair octahedra versus H36 edges. Then

- every row has weight 12;
- every column has weight 9;
- real rank is 120;
- binary rank is 90;
- two distinct octahedra share either zero or three edges.

The exact squared singular spectrum is

`108^1, 54^20, 36^15, 18^84, 0^150`.

The graph joining octahedra that share three edges is 32-regular on 270 vertices with 4320 edges. It is not strongly regular: adjacent pairs have 10 common neighbors, while nonadjacent pairs split among 0, 4, and 8 common neighbors.

The ranks 120 and 90 echo other project carrier dimensions, but this packet does not promote a cross-carrier identification without an explicit intertwiner.

## Packet synthesis

The packet closes three previously open structures and opens one sharper frontier:

1. **Fault tolerance:** the 85-reader has exact erasure distance 8, with the pure tritangent minimum family classified as `2K4`.
2. **Local qutrit gauge:** `12 -> 4 x 3` refines to a point-selected C3 torsor, with the outer finite sign acting as the S3 reflection parity.
3. **Code topology:** residual squares, full dual triangles, and the full H36 cycle space form `294 < 324 < 325`; the new 30-layer has an explicit Q43 projection with `20 -> 30 -> 10`.
4. **Covering radius:** the octahedral character algebra is substantially stronger than radial moments, but the rigorous radius remains `134 <= rho(K) <= 173` until complementary shell correlations are controlled.

Pass4959 was not touched. Finite-group signs are not promoted to spacetime CP/CPT, and equal dimensions are not promoted to representation isomorphisms without explicit maps.
