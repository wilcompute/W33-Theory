# Part DCCLVIII — Octahedral Dobrushin-Contraction Bridge

## Why this part exists

DCCLV-DCCLVII proved exact contraction laws for specific observables (TV from a start state, entropy/KL, chi-square). This part upgrades to a global sharp contraction theorem over all distributions.

## Exact coefficient

For transition matrix `P`, define Dobrushin coefficient

```text
alpha(P) = (1/2) max_{i,j} ||P(i,.) - P(j,.)||_1.
```

The verifier proves for octahedral walk:

```text
alpha(P) = 1/2.
```

## Sharp global contraction law

For any two distributions `mu, nu`:

```text
TV(muP, nuP) <= alpha(P) TV(mu,nu) = (1/2) TV(mu,nu).
```

And for `t` steps:

```text
TV(muP^t, nuP^t) <= (1/2)^t TV(mu,nu).
```

The verifier checks these globally on the full delta-law family and confirms sharpness.

## Sharpness

The bound is attained by a worst-case row pair (adjacent-type orbit), giving exact one-step ratio `1/2`.
So this is not merely an inequality with slack; it is the exact contraction constant.

## Meaning

The octahedral closure random walk now has:

- exact spectral contraction,
- exact entropy/KL/chi-square contraction,
- and exact global TV contraction coefficient.

This is the cleanest finite mixing-optimality statement so far in the closure transport program.

## Exact vs conditional

- **Exact:** global sharp Dobrushin coefficient is `alpha=1/2`, yielding exact worst-case TV decay `(1/2)^t`.
- **Conditional:** continuum contractivity interpretation still requires a scaling limit.

## Executable artifact

- Verifier: `verify_dcclviii_octahedral_dobrushin_contraction_bridge.py`
- Tests: `tests/test_dcclviii_octahedral_dobrushin_contraction_bridge.py`
- Data: `data/dcclviii_octahedral_dobrushin_contraction_bridge.json`
