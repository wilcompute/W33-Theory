# Part DCCLVII — Octahedral Chi-Square Contraction Bridge

## Why this part exists

DCCLVI gave entropy growth and KL decay. This part adds an exact quadratic-information law (L2 / chi-square) for the same octahedral walk.

## Exact quadratic information

For walk law `mu_t = delta_i P^t` and uniform equilibrium `pi` on 6 states, define

```text
L2sq(mu||pi) = sum_i (mu_i - pi_i)^2,
chi2(mu||pi) = sum_i (mu_i - pi_i)^2 / pi_i.
```

For uniform `pi`, the verifier confirms exact identity

```text
chi2 = 6 * L2sq.
```

## Exact contraction law

Using DCCLV projector power formula, the verifier proves for `t >= 1`:

```text
L2sq_{t+1} = (1/4) L2sq_t,
chi2_{t+1} = (1/4) chi2_t.
```

So both quadratic distances decay by exact ratio `1/4` per step.

## Exact initial values

The verifier proves:

```text
chi2_0 = 5,
chi2_1 = 1/2.
```

Hence the full post-step-1 profile is exactly geometric.

## Meaning

The closure phase-space information stack now has:

- TV exact half-contraction,
- entropy/KL directionality,
- and exact chi-square quarter-contraction.

This is the cleanest exact quadratic-coercivity bridge so far in the octahedral dynamics program.

## Exact vs conditional

- **Exact:** chi-square and L2-squared distances to equilibrium contract by exact factor `1/4` per step (from step 1 onward).
- **Conditional:** continuum hypocoercive interpretation still requires a scaling limit.

## Executable artifact

- Verifier: `verify_dcclvii_octahedral_chi_square_contraction_bridge.py`
- Tests: `tests/test_dcclvii_octahedral_chi_square_contraction_bridge.py`
- Data: `data/dcclvii_octahedral_chi_square_contraction_bridge.json`
