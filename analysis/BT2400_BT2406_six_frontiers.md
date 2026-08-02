# Passes 2400–2406 — syndrome-first U6, shell algebra, duad solver, arithmetic quotients, E8 obstruction, and the tomotope 192 atlas

## Executive result

All six requested fronts were executed. Five close as exact structural theorems. The colouring problem and the global U6 coefficient remain explicitly open.

The most important correction occurred during implementation: the exploratory external-merge worker originally allocated five bits to a shard ID. That is sufficient for the frozen 28-shard `B=8` run, but not for the `66` and `120` shards at `B=12,16`. The published worker uses seven bits and all extension counts below are corrected reruns.

## Pass 2400 — syndrome-first external merging replaces the rigid shard graph

The new C++ worker writes fixed-coordinate weight-six records into 256 radix buckets keyed by the top eight syndrome bits. Each bucket is sorted by the exact composite key `(45-bit syndrome << 7) | shard_id`. Syndrome groups are then aggregated globally inside the merged supershard.

| cutoff | shards | records | syndrome groups | singletons | cross-shard collisions |
|---:|---:|---:|---:|---:|---:|
| `B=8` | 28 | 58,282,126 | 46,732,216 | 38,099,164 | 5,389,182 |
| `B=12` | 66 | 132,728,827 | 103,253,623 | 82,546,353 | 21,732,677 |
| `B=16` | 120 | 233,088,428 | 179,498,008 | 142,386,379 | 43,428,489 |

The `B=8` run reproduces the frozen Passes 1939/1950 counts exactly, including 3,163,606 shared-syndrome shard-pair incidences. The corrected `B=16` census covers 3.741 percent of the fixed-coordinate chart. It is an executable replacement architecture, not yet the global U6 coefficient.

## Pass 2401 — the five shell orbits generate a rank-527 coherent configuration

Exceptional `S6` has five frame fibers of sizes `180,120,45,180,15`. Its orbitals on all ordered frame pairs form a coherent configuration of rank `527`.

In fiber order `(pair-phase, mixed, parallel, rectangle, residual)`, the numbers of basis relations between fiber pairs are

```text
58 32 17 58  6
32 26 10 32  5
17 10  8 17  4
58 32 17 58  6
 6  5  4  6  3
```

There are 65 self-transpose relations and 231 transpose pairs. The exact algebra has 216,244 nonzero intersection numbers, with maximum value 48. Its compact structure-constant stream has SHA-256 `29c780f81fdea4ee6b8e07c825f7c7ab9b254df1a49f8633309a1e05eb8a7a69`.

The `S6` permutation module decomposes with multiplicities `5,8,13,7,6,11,3,6,4,1,1` across the eleven partitions of six. Their squares sum to 527, so `End_S6(C^540)` has dimension 527 and center dimension 11. The shell algebra is not a five-class commutative association scheme; it is the full noncommutative five-fiber orbital coherent configuration.

## Pass 2402 — the duad ABI gives a compact exact-cover formulation

A deterministic `F2` pivot scan selects the 15 frame anchors `0,1,2,3,6,27,28,29,30,54,57,60,81,82,87`. Their `15 x 15` frame-to-duad submatrix is invertible. Its pointwise and setwise stabilizers in exceptional `S6` are both trivial. More sharply, frames `0` and `1`, with matchings `(3,12,57,66)` and `(6,12,60,69)`, already form a pointwise base.

Each W33 edge belongs to nine frames. Consequently a nine-colouring is exactly a nine-colour exact cover of the 240 edge cliques: each frame receives one colour and each nine-frame edge clique receives every colour once.

The compact model has 4,860 binary variables, 2,700 equality constraints and 24,300 nonzeros. This reduces the earlier model by 52.64 percent in variables, 86.11 percent in constraints and 70 percent in nonzeros. All 720 exceptional-`S6` images of the frozen proper 14-colouring have distinct signatures on the 15 anchors, so anchor lexicographic symmetry breaking is demonstrably nonvacuous.

A bounded 20-second HiGHS run on the compact nine-colour model returned `TIME_LIMIT / UNKNOWN` with no primal solution. Thus `chi(H)=9` remains undecided.

## Pass 2403 — the arithmetic-shell bridge is an `S4` parabolic quotient

- Modulo two the generators produce `SL3(2)` of order 168. Its projective-point stabilizer has order 24 and is `S4`.
- Modulo three they produce `SL3(3)` of order 5,616. Its point stabilizer has order 432, with radical `3^2`, Levi `GL2(3)` of order 48 and projective Levi quotient `PGL2(3)=S4`.
- The stabilizer of a residual duad in exceptional `S6` is `S2 x S4` of order 48; quotienting by the commuting `S2` gives the same `S4`.

Thus the first exact common finite packet between the arithmetic multiplicity lattice and residual tetrahedral shell is `S4` of order 24—the tetrahedral facet packet beneath the tomotope scale. There is no nontrivial common quotient of the full groups `S6` and `SL3(2)` or `SL3(3)`, and no canonical Fano-point-to-duad map is supplied.

## Pass 2404 — the full-PSp linear E8-to-coexact question closes negatively

The repository's invariant quadratic-form computation gives the canonical eight-dimensional mod-two `PSp(4,3)=U4(2)` module a unique plus-type quadratic refinement, placing it in the `E8/2E8` orthogonal space. Any characteristic-zero root-span lift has dimension eight.

The coexact signed-edge `90` is irreducible under full `PSp(4,3)`. Therefore `Hom_PSp(8,90)=0` and `Hom_PSp(90,8)=0`: a nonzero map from dimension eight into irreducible dimension 90 would have to be surjective, while a nonzero map out of irreducible dimension 90 would have to inject into dimension eight.

This resolves the Pass-1954 boundary. An abstract noncanonical `C6`-linear injection of primitive characters may exist, but full `PSp` equivariance kills every linear map. Proper-subgroup, nonlinear and symmetry-breaking constructions remain open.

## Pass 2405 — the 192 is genuinely tomotopal, but three 96-layers compete

The repository had already separated an intermediate semiregular group of order `192=8x24` from the actual tomotope with automorphism order 96 and `192=2x96` flags in two flag orbits. It had also proved that the 2,880 curved events form a unit tight frame in rank-15 `E15` with frame bound 192.

The new objectwise census intersects each curved event with the 15 residual-duad octets. Three exact exceptional-`S6` relations appear:

| relation | events | labels/event | incidences | degree at each duad |
|---|---:|---:|---:|---:|
| unique maximum intersection 3 | 1,440 | 1 | 1,440 | 96 |
| two-way maximum-2 tie | 720 | 2 | 1,440 | 96 |
| two-way maximum-3 tie | 720 | 2 | 1,440 | 96 |

Thus every residual duad carries three exact `96`-element layers. Each layer has the size of one tomotope flag orbit; any two layers give 192 incidences per duad.

This is stronger than `2880=15x192`, but it reveals the remaining obstruction: the incidence geometry gives three natural 96-layers, whereas the tomotope needs two flag orbits. No canonical rule selects two of the three. Neither a labelled equivariant flag bijection nor a disjoint `15x192` event partition is claimed.

## Pass 2406 — evidence boundary

The packet separates exact finite counts and actions from the unresolved global U6 merge and nine-colour decision; an exact full-PSp linear obstruction from smaller-subgroup possibilities; and a genuine 96/192 tomotope scale from the still-missing canonical two-layer selector. No shell relation, arithmetic quotient, E8 coordinate, tomotope flag or syndrome count is promoted to a measured physical particle, coupling, charge, generation, colour or spacetime degree of freedom.
