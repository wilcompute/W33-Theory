# Passes 558–562 — triality, radial/quadratic transfer, local cyclotomy, noise, and tensor derivation

This release executes the five directions opened after Pass 557.

## Pass 558 — a single PG(3,2) triality object

The three fixed-magnitude 80-word fibres of five-parallel-four-cube type share one four-dimensional translation group. Their quotient is the 15-point projective geometry `PG(3,2)`, partitioned into three elliptic quadrics `Q^-(3,2)`.

The partition stabilizer has order 60 and is

`C15 semidirect C4`, with `s r s^-1 = r^2`.

It induces the full `S3` on the three quadrics and has `D10` kernel. The three quartic values form the permutation representation `1 + 2`; this is a triality orbit of a quartic covariant, not a `Z3` grading by invariant degree.

## Pass 559 — structured Hjelmslev transfer through 59,049 sections

The affine `F3^8` family is enlarged by a common deep-anchor trit and the quadratic packet `q ell_b(u)^2`, producing a ten-dimensional function space.

Exact image sizes are

`13 -> 26 -> 96 -> 336 -> 921 -> 3056 -> 9266`.

Minimal future-complete state counts are

`41 -> 122 -> 365 -> 1094 -> 3281 -> 9841 -> 9266`.

The Pass-554 family is exactly the `d=q=0` face. Once radial and quadratic futures are allowed, its 921 terminal polynomials refine to all 3,281 projective affine histories, so it is embedded but not closed.

## Pass 560 — actual fifth-cyclotomic algebra in Lean

Lean proves

`Phi5(1-lambda)=lambda^4-5 lambda^3+10 lambda^2-10 lambda+5`

and

`lambda^4=5(lambda^3-2lambda^2+2lambda-1)`.

It proves the residual factor is `-1 mod lambda` and derives `v(lambda)=1` and `v(lambda^n)=n` from standard additive valuation laws, `v(5)=4`, and valuation zero of the residual factor.

The polynomial and ramification identities are no longer certificate hypotheses. Construction and completeness of `Q_5(zeta_5)`, and the local theorem making the residual factor a unit, remain explicit model fields.

## Pass 561 — a contrast-adaptive orientation compiler

The 70 quartic levels have minimum squared four-embedding distance 3750. Conditional five-sigma shot bounds are compiled for several single-shot noise scales.

For the orientation latch, direct twelvefold parity is optimal at high contrast, while repeated single-channel measurements plus classical parity are superior after sufficient loss. In the declared profiles:

- conservative: repeated channels, 564 shots versus 1,295 direct;
- nominal: direct parity, 161 shots versus 468 repeated;
- aspirational: direct parity, 42 shots versus 420 repeated.

The compiler therefore selects the pointwise minimum architecture instead of freezing one readout design.

## Pass 562 — the five fibre types from invariant tensors

For each level set of `(e3,e4,e5)`, Walsh and Boolean Möbius transforms derive the translation dimension, affine-hull dimension, coset count, and principal-generator degree. This reproduces exactly

- `(16,4,4,1,8)^1`;
- `(40,11,1,20,9)^44`;
- `(40,11,2,10,9)^48`;
- `(80,8,4,5,8)^3`;
- `(80,12,1,40,8)^2`.

The classification is therefore derived from the invariant-tensor level indicators rather than assigned after a separate geometry census.

## Validation boundary

All five executable owners, their immutable JSON certificates, the focused regressions, and the aggregate release lock are exact for their declared finite families. The release does not claim a full q=5 all-magnitudes theorem, the full `9^40` image, a completed Lean construction of the cyclotomic local field, or measured photonic-device performance.
