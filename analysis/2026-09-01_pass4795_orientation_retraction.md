# 2026-09-01 — Pass 4795 degree-45 orientation correction

## Exact correction

The Pass 4795 claim that the degree-45 `PSp(4,3)` carrier has local image `C3` on the three incident maximal `K5` lines, and therefore supports a global two-sheet cyclic-orientation torsor, is withdrawn.

Two independent exact checks now settle the action:

1. `analysis/w33_20260901_degree45_action_crosswalk.py` reconstructs the Pass 4795 dependency-cube quotient and the later polar-pair packet carrier under the **same four PSp transvection generators**.  It finds an explicit 45-point equivariant bijection preserving the degree-45 graph and all 27 maximal `K5`s.  For a point stabilizer of order 576, the induced permutation group on its three incident `K5`s has order 6 with order profile
   `1^1, 2^3, 3^2`, hence is `S3`, not `C3`.

2. `analysis/w33_20260901_degree45_tom_uniqueness.g` independently verifies from the `U4(2) ~= PSp(4,3)` Table of Marks that the transitive index-45 action is unique.  There is therefore no second transitive degree-45 PSp action on which the old `C3` local image could live.

The corrected local exact sequence is consequently

`1 -> H_96 -> H_576 -> S3 -> 1`,

not a quotient by `C3`.

## What survives

The correction is deliberately narrow.

- The 45 packet/support objects survive.
- The 27 maximal `K5` completion charts survive.
- The graph/GQ/cubic incidence results not using cyclic orientation survive.
- The shortest three-gate port compiler survives.  The corrected executable certificate has chart-graph diameter 11 and order-960 holonomy, now with full local `S3` port gauge.
- Independent central `C3` extensions elsewhere in the project are **not** affected.  This retraction concerns only the Pass 4795 degree-45 local-action/orientation theorem.

## Superseded wording

Historical files may still contain the old `C3` sentence as the claim being tested or as a pre-correction comparison.  They are retained for provenance, but they are not frontier evidence for a cyclic orientation.  The authoritative evidence is now:

- `analysis/w33_20260901_degree45_action_crosswalk.py`
- `analysis/w33_20260901_degree45_compiler_correction.py`
- `analysis/w33_20260901_degree45_tom_uniqueness.g`
- this correction note
- `data/w33_retractions.json`

## Boundary

`S3` is an exact finite-group local action.  No physical parity, chirality, particle family, or gauge-field interpretation follows merely from replacing the false `C3` quotient by the correct `S3` quotient.
