# TOE80B — Exact native W33 octagon dictionaries into all eight E8/E6/A2 matter sectors

**14 October 2026.** This follows TOE80's exact rank-six projector, 72 E6 roots and explicit Weyl group of order 51,840 on the 27 shared W33 theta octagons.

## Why this is not a duplicate E8 result

The repository's earlier Part MCCCXC (analysis/w33_e6_minuscule_27_a2_phase_factorization.py) **already proved** that each of four E8-to-E6×A2 coordinate splits has two 81-root matter sectors, and each sector decomposes into 27 E6 minuscule weights with three A2 phase lifts. It verified the E6 rank-six Gram, cubic-line graph and reflection closure independently, before the present octagon program. We do not claim to rediscover that branching theorem.

TOE80 newly identified an *actual chosen native W33 octagon address space* with 27 weights, constructed from the two chord flags, their 216 stabilizer, the invariant cubic-surface graph, the rational projector P6=(3I−3A+J)/18 and its resulting 72 root vectors and W(E6) Weyl permutations.

This pass tests a **direct, exact interface between these independently built source families**, rather than another numerical match.

## Eight independent E8 sector-to-W33 address dictionaries

For each A2 coordinate 0,1,2,3, and for each matter_81_coset_1 and matter_81_coset_2, read the original, *unmodified* E8 root construction via sectorize_by_coordinate. Project its 81 E8 roots into the corresponding E6 six-dimensional subspace and group them by their exact Fraction-valued E6 weights. Each produces precisely 27 different projected weights, with three A2 phase labels per weight.

Build an E6 cubic-line adjacency directly from exact inner product -2/3 among these old weights. Independently build the native W33 octagon cubic-line adjacency from the 27-by-27 integer Q = 18P6.

For each of all **eight** matter sectors:
1. Construct and freeze one **explicit graph isomorphism** native octagon index ↔ E8-derived projected weight index; check bijectivity of all 27 labels.
2. Pull the entire old **27×27 Fraction-valued Gram** through that map and verify, entry by entry, equality with the **native** Q/3. This is 729 exact rational checks per sector, not just spectrum matching.
3. Take differences of each of the native **216 nonadjacent pairs**, in this transported weight gauge. Keep both root signs, and verify equality, as exact coordinate tuples, with the **independently reconstructed set of 72 E6 roots** from the original E8 sectorizer.
4. Assign each native octagon **exactly three** A2 phase lifts, retaining the original E8 matter root labels.
5. Compare the two conjugate 81-root matter-sector weight sets under global negation in each A2 coordinate, recording the result rather than assuming it.

The expected scope is **8 × 81 = 648 sector-memberships**, where the same underlying E8 roots recur in different choices of A2 embedding; 648 is not a count of 648 distinct E8 roots or physical states.

## Canonicality and physical guardrail

The native Weyl graph has 51,840 automorphisms, so an abstract graph isomorphism has 51,840 gauge choices; fixing one native address ↔ one E8 weight leaves 1,920 choices. The code freezes a deterministic representative, but that does **not** mean the correspondence is canonically dictated by physics. A generator-level intertwiner between the native PGSp(4,3) action on all 240 theta-chord pairs and the Weyl group action remains open. Likewise, three A2 phases per address are E8 root-coordinate labels, not experimentally verified photonic time bins or three fermion generations.

The exact interface makes it possible to write and independently audit future native-octagon to E8/E6/A2 amplitude compilers, while avoiding silent basis identifications.

## Reproduction

- analysis/w33_20261014_toe80_octagon_e8_a2_dictionary.py
- tests/test_w33_20261014_toe80_octagon_e8_a2_dictionary.py
- .github/workflows/w33_toe80_octagon_e8_dictionary.yml
- data/w33_20261014_toe80_octagon_e8_a2_dictionaries.json, regenerated as a CI artifact.

The dependency is the previously certified native TOE80 E6 projector and old independent Part MCCCXC E8/A2 root-sector construction. CI status and any failing invariants must be checked before describing the eight dictionaries as verified.

## Five independent next tests

1. Group-generator transport: construct and certify one explicit PGSp↔W(E6) map that extends the native order-216 subgroup action and respects the 240 cosets, or prove an obstruction.
2. Signed E6 cubic: transfer the repository's full coefficient-level 27-matter cubic to octagon phases; test all Weyl and H27 center transformations including antiunitary involutions.
3. E8/A2 phase homotopy: compare exact three phase labels against independently compiled holonet qutrit time-bin and orbital-angular-momentum gates with a negative generic-theta control.
4. Dynamics: build an interacting gauge-invariant W33 octagon matter Hamiltonian with local hopping and a meaningful measured observable, not an arbitrary cubic support label.
5. 4D structure: verify chiral/antichiral and anomaly properties with an admissible overlap-Dirac construction, respecting the 26-zero-mode obstruction for the original 80-site free Levi hopping model.

**All results here concern exact finite root/graph models, not a proven physical Theory of Everything.**
