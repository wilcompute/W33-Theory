# BT925 — Canonical mod-2 form on the homology

**Status: PARTIAL — canonical mod-2 bilinear form pinned; positive-definite integral lift still open.**

BT924 pinned the E8 rank and 2-adic location over Z. BT925 adds the canonical mod-2 bilinear form on

```text
H = ker(A2) / im(A2).
```

## Corrected canonical statement

For cycles `x,y in ker(A2)`, the integer `x^T A y` is even, so

```text
B(x,y) = (x^T A y)/2 mod 2
```

is well-defined. The verifier checks:

- `B` descends through boundaries: `B(boundary,z)=0`.
- `B` has rank 8 on `H`.
- `B` is alternating: `B(x,x)=0` for all 256 classes of `H`.

Thus:

```text
(H,B) is E8/2E8 as a rank-8 symplectic F2 bilinear space.
```

## Important correction

The edge-parity functional

```text
q(x) = (x^T A x)/2 mod 2
```

is **not** the quadratic refinement of `B`. It is linear on cycles and vanishes on `H`. Equivalently, the Wu class vanishes, which is consistent with an even lattice lift, but it does not distinguish `E8` from the indefinite even unimodular rank-8 form `II_{4,4}`.

## Sharp residual

No mod-2 or mod-4 invariant can close the integral E8 lift. The remaining question is archimedean/integral:

```text
find the positive-definite even unimodular lift of the canonical rank-8 shadow.
```

## Witness

```text
analysis/bt925_canonical_mod2_e8_form.py
data/bt925_canonical_mod2_e8_form.json
```
