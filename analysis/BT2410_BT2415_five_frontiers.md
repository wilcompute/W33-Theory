# Passes 2410–2415 — tomotope selector, global collision ledger, exact-cover search, rank-22 fusion, and the E8 double-cover boundary

## Executive result

All five requested fronts were executed. Three close as exact positive structure theorems, one closes as an exact central-extension obstruction, and the literal nine-colour decision remains fail-closed `UNKNOWN` after a complete first-colour census.

## 2410 — the tomotope selector is event-side valency two

The three curved-event/residual-duad profiles have event-side valencies `1,2,2`. Therefore the canonical selector is not an arbitrary choice of two layers: it selects exactly the two tie profiles. At every residual duad they contribute `96+96=192` incidences.

Each tie layer is supported on the 60 edges of the triangular graph `T(6)=L(K6)`, with multiplicity 12 on every adjacent duad pair and zero on disjoint pairs. For a fixed duad, three-point event-overlap splits the selected 192 carrier into eight connected components of 24. Every component contains 12 flags from each 96-layer. The eight neighboring duads split as `4+4` according to which endpoint of the fixed duad they meet, reproducing `192=2*96=8*24` and the unordered four-plus-four facet split.

This is a canonical local carrier theorem. A generator-by-generator isomorphism to the archived labelled maniplex remains open.

## 2411 — the global pair-collision merge is closed algebraically

For a codeword of weight `w in {4,6,8,10,12}`, the number of unordered pairs of weight-six errors with difference that codeword is `(1/2) C(w,w/2) C(240-w,6-w/2)`.

| difference weight | collision edges |
|---:|---:|
| 4 | 204,105,833,100 |
| 6 | 202,385,664,000 |
| 8 | 397,812,076,200 |
| 10 | 507,826,972,800 |
| 12 | 412,008,338,280 |
| **total** | **1,724,138,884,380** |

For one fixed-coordinate chart, the exact internal collision count is `11,362,631,040` and the crossing-partner incidence count is `63,481,682,139`. The weight-12 crossing contribution is `20,600,416,914`, independently reproducing Pass 1907.

The remaining global `U6` task is union/deduplication of overlapping partner and lower-shadow marks. Pair counts alone cannot determine singleton cosets.

## 2412 — complete first-colour domain, literal resolution still open

The fixed-frame exact-cover enumerator completed after `477,262,755` nodes and produced exactly `394,200` covers containing frame 0, matching Pass 1821. By double counting this corresponds to `3,547,800` global covers.

The literal nine-colour model uses 540 frame variables and 240 exact `AllDifferent(9)` edge cliques. A custom perfect-matching support propagator, with only the sound global colour pin on edge clique 0, ran for 20 seconds: 6,059 nodes, 9,303 backtracks, 2,047,166 propagations, status `UNKNOWN`.

The Pass-2309 nine-signature capacity witness is retained as a positive necessary-condition witness only. The next exact level is to choose one of the 394,200 first covers and eight frame-disjoint global covers completing all 540 frames.

## 2413 — canonical rank-22 full-PGSp fusion

The rank-527 exceptional-`S6` shell coherent configuration fuses exactly to the orbitals of full `PGSp(4,3)` on ordered frame pairs. The fusion rank is 22.

Four independent seeds—frame adjacency, shared W33 lines, shared point support, and adjacency plus shared lines—produce the same closure and the same map hash `c23b38938ef6ad38ec0b782cda6ebe7b699d3b8e524f5df9c0e18088e048c671`.

The rank-22 algebra is transpose-closed and noncommutative. Its center has dimension 10 and its Wedderburn blocks have sizes `1,1,1,1,1,1,2,2,2,2`.

## 2414 — the E8 question is controlled by the double cover

The integral eight-dimensional E8 carrier listed by ATLAS is a representation of `2.U4(2)`, with character `chi21+chi22`. The coexact 90 is a representation of `U4(2)=PSp(4,3)` and inflates to the double cover with central involution acting as `+I`.

On the faithful E8 carrier, the central involution acts as `-I`. Consequently `Hom_{2.U4(2)}(8,90)=Hom_{2.U4(2)}(90,8)=0`, and the same is true for every lifted subgroup containing the center. In particular, the common quotient-level `S4` packet does not define a coupling: its full preimage contains the center, so the Hom space remains zero. A nonzero proper-subgroup map requires an explicitly chosen split subgroup avoiding the center and a compatible lift.

This sharpens Pass 2404: the obstruction is central character before it is dimension.

## Evidence boundary

The tomotope carrier, collision ledger, full-group fusion, and double-cover obstruction are exact. The global singleton coefficient and nine-colour decision remain open. No finite packet, code coefficient, flag layer, or representation is promoted to a measured physical particle, charge, coupling, generation, colour, or spacetime degree of freedom.
