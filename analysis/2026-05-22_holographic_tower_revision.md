# 2026-05-22 - W33 holographic tower revision

This revision upgrades `paper/w33_holographic_tower_final.tex` from a tower-only draft into a two-substrate, minimal-logical-surface paper.

## Main structural corrections

1. The internal graph is `W(3,3)`, the generalized-quadrangle collinearity graph with 40 vertices and 240 edges.
2. The horizon graph is `K_12`; its orientable complete-graph genus is `(12-3)(12-4)/12 = 6`.
3. Riemann-Roch explains the AG-code dimension law `n-k=g`, but it is not used as a standalone proof of distance `3`.

## New theorem stack added to the paper

- Minimal logical census: `d_X=3`, `d_Z=4`, projective counts `|X_min|=160`, `|Z_min|=1620`, vector counts `320` and `3240`.
- Support biregularity: `160*81=1620*8=12960`.
- Minimal logical E6 pairing: nonzero vector phase count `25920+25920=51840=|W(E6)|`.
- Signed phase frame: `Spec(AA^T)=160^81 + 0^79`, so `AA^T/160` is an exact rank-81 projector.
- X-side visibility scheme: overlaps `1,3,9,27` with row multiplicities `81,54,18,6`.
- Z-side dual visibility: row distribution `0^1187,1^288,2^96,3^32,4^16`, giving `432=16*27` nonzero Z-neighbors.
- Toroidal generating function: `P(t)=(1+t)Q(t)` where `Q(t)=68+79t+48t^2+38t^3+16t^4+3t^5`.

## Verification companion

Added:

- `analysis/w33_holographic_tower_paper_checks.py`
- `data/w33_holographic_tower_paper_checks.json`

The script checks the arithmetic invariants in the revised paper and emits the JSON data file.

## Current synthesis

The clean synthesis is:

```text
forget phase -> |W(E6)| = 51840
retain phase -> rank(A) = 81
```

So the minimal logical W33 surface carries E6 as its unsigned noncommutation shadow and the protected 81-dimensional sector as its signed phase geometry.
