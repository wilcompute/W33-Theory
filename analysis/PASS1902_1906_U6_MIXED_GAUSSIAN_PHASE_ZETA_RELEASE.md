# Passes 1902–1906 release

## Status

`PASS_WITH_U6_MIXED_AND_FULL_SUBGROUP_BOUNDARIES`

Frozen verification: **33/33** assertions.

Canonical packet SHA-256:

`abe7b169b5e39bb8ac5beecd33f8e80e73712604b1ce05ed20e1e1cd728dfb7c`

## Delivered

- **1902 — U6 exact reduction.** All collision edges are resolved by difference weight. The weight-12 shell contributes `412008338280` disjoint edges and `20600416914` fixed-coordinate external incidences with multiplicity. A compiled external-memory component pipeline is supplied; no U6 value is promoted before it completes.
- **1903 — mixed separator tensor.** The full enumerator is reduced to an exact six-block/15-residual tensor with `20+180+40` factors and a `155841`-bin chunk format. Tutte–Coxeter incidence is exactly the set of 45 absent pair factors.
- **1904 — Gaussian V9 lattice.** Minimum norm `24`, 60 minimal vectors, 15 minimal lines with graph `KG(6,2)`, and full unitary group `C4×S6` of order `2880`.
- **1905 — phase skeleton.** `PSp(4,3)` gives the canonical 90-sector phase `±J`; the outer Weyl involution removes it. The named chain and all cyclic classes are exact. A GAP worker completes the remaining noncyclic S6 classes.
- **1906 — twisted Ihara zeta.** Character dimensions `26,20,24,20`, four exact reciprocal Artin–Ihara factors, and primitive reduced-cycle counts through length 24.

## Parallel correction integrated

The false spread bound `|class∩K10|≤5` is neither used nor repeated. The parallel theorem `End_PSp(90)=C` sharpens phase existence to uniqueness up to orientation.

## Boundaries

- U6 awaits the complete external-memory singleton-component run.
- The mixed enumerator awaits all 156 residual-orbit contractions and a verified merge.
- The phase table awaits the GAP output before claiming every noncyclic subgroup class.
