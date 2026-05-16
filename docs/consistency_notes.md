# Consistency notes

This note records formula-level drift identified during the May 16, 2026 W33-Theory audit. It is intentionally conservative: it does not decide which expression is correct, but it does make the inconsistency explicit so that future theorem claims can be regression-tested.

## Items to canonicalize

### Fine-structure constant

Two close but distinct public expressions appear in the project lineage:

- docs/script lineage: `137 + 40/1111 = 137.03600360036003`
- paper/report lineage: `137 + 880/24445 = 137.0359991818368`

These differ by approximately `4.4185e-6`. That is small numerically, but large conceptually for a zero-free-parameter claim.

### Weinberg angle

Two electroweak normalizations appear in public-facing theory artifacts:

- low-energy/electroweak package: `sin^2(theta_W) = 3/13`
- GUT-scale/mathematical-pillar package: `sin^2(theta_W) = 3/8`

Both may be meaningful in different regimes, but the regime labels must be explicit anywhere the values are presented.

## Immediate policy

Until these are resolved, docs and papers should avoid presenting all variants simultaneously as final exact theorem outputs. New scripts should either:

1. import canonical expressions from a single source of truth, or
2. deliberately label alternatives by regime and assert that cross-file references agree.

## Reproduction hook

See `scripts/reproduce_w33_core.py` and `tests/test_reproduce_w33_core.py` for the first CI-level checks added to keep this drift visible.
