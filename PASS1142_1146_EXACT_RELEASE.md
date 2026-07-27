# Passes 1142-1146: Hecke Algebra, Steinberg Bridge, Corpus Migration, and A2 Color Torsor

Date: 2026-07-27

## Pass 1142 - the S5 Hecke algebra is rank 26 and noncommutative

For each of the three transitive 432-element W(E6)-sets, the point stabilizer is S5 and its suborbits have sizes

`1,1,5x6,10x4,20x9,30x4,60`.

Thus `End_{W(E6)} C[W(E6)/S5]` has dimension 26. The permutation module decomposes as

`1 + 2*6 + 15 + 15a + 3*20 + 2*30 + 60a + 2*64 + 81_minus`.

Consequently the Hecke algebra has Wedderburn type

`C + M2(C) + C + C + M3(C) + M2(C) + C + M2(C) + C`

and is noncommutative. Every inter-orbit Hom space between the three 432 carriers also has dimension 26; the full three-copy commutant has dimension `9*26 = 234`.

## Pass 1143 - first explicit Steinberg bridge

The 27-label permutation module is `1 + 6 + 20`; its augmentation is `6 + 20`. The smallest tested natural Schur functor containing `81_minus` is

`Lambda^2(Aug26)`, dimension 325,

with decomposition

`6 + 2*15 + 20 + 2*30 + 2*64 + 81_minus`.

For the 36-element class 2C, let

`K_2C = sum_{g in 2C} Lambda^2(Aug26)(g)`.

On the six constituents above its eigenvalues are `24,12,18,12,9,4`. Therefore

`P_81 = (K-24I)(K-18I)(K-12I)(K-9I)/11200`

is the exact central projector onto the 81-dimensional Steinberg summand. A rank-81 integer intertwiner from a 432 carrier to `Lambda^2(Aug26)` was constructed and verified against all six simple generators. Hence

`dim Hom_G(81_minus, Lambda^2(Aug26)) = 1`

and the three-copy kernel has a 3-dimensional Steinberg-specific Hom space into this target.

## Pass 1144 - shifted-adjacency descendants migrated

The historical `{-7,-1,5}` cubic family is not merely registered: active pure descendants are replaced by retraction stubs with archived originals, legacy derivations receive executable guards, tests are quarantined explicitly, and manuscript surfaces receive visible erratum notices. A generated erratum PDF and migration report freeze the correction.

## Pass 1145 - zero-ambiguity 540 registry

Every historical 540 occurrence is assigned one of four exact identities:

- `line-nonedge`: 540 disjoint line pairs;
- `point-nonedge`: 540 noncollinear point pairs;
- `both`: shared arithmetic that identifies neither object;
- `unrelated`: a numeric 540 outside this two-object ambiguity.

Structured files are covered by a content-hashed occurrence registry rather than syntax-breaking inline comments. Any changed file whose hash no longer matches the registry must carry an inline tag or regenerate the registry. The full-corpus strict gate therefore has zero unresolved occurrences without falsifying ambiguous factorization-only passages.

## Pass 1146 - the three 432 copies are an A2 color torsor

Each 432 orbit consists of mixed A2 triples whose positive and negative roots lie in the same one of the three 27-shell colors and have distinct E6 labels. The three colors distinguish the three orbits exactly.

The order-three A2 Coxeter element commutes with W(E6), cycles the colors, and cycles the 432 orbits. Therefore the carrier is canonically

`Omega_432 x C3`

as a `W(E6) x C3` object. The missing label is A2 shell color, not an abstract S5 subgroup type.

## Parallel-agent audit

Draft PR #162 supplies valid exact 2240-carrier, cubic-incidence, and character data; those inputs are incorporated under collision-free numbering.

PR #160's proposed defect-ray verifier is not imported. Its construction calls a 40-ray object a qutrit SIC, although a dimension-three SIC has nine rays, and it falls back to arbitrary indices `[0,1,2,3]`. The exact A2 color torsor above replaces that non-invariant defect labeling.
