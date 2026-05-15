# Part DCCXXXVI — Closure-Action / Weight Bridge

## Why this part exists

DCCXXXV gave the exact interval invariant

```text
sigma = (Delta_tau)^2.
```

This part upgrades interval into an exact discrete action law.

## Exact action law

On each elementary causal step, define the line element

```text
ds = 1.
```

For a monotone causal path from `T_a` to `T_b`, define

```text
S(a,b) = sum_path ds = Delta_tau(a,b).
```

So the action is exactly the proper-time separation.

Because DCCXXXII already proved

```text
C = 12 * 2^tau,
```

we get the exact weight law

```text
W(a,b) = 2^{-S(a,b)} = C_a / C_b.
```

Thus the closure path weight is the inverse codec scale ratio.

## What is proved exactly

The verifier checks:

- elementary causal edges have unit action,
- path action equals `Delta_tau`,
- path action equals the logarithm base 2 of scale ratio,
- path weight is exactly the inverse scale ratio,
- action is additive under composition,
- weight is multiplicative under composition,
- maximal path `T_0 -> T_5` has
  - `S = 5`
  - `W = 1/32`.

## Meaning

The chain now has a genuine dynamics-like structure:

- **proper time** gives the action,
- **scale ratio** gives the weight,
- **composition** behaves exactly like a discrete path law.

So the emergent-time thread is no longer only kinematic. It now carries an exact action/weight calculus on closure histories.

## Exact vs conditional

- **Exact:** the closure chain has a discrete action `S=Delta_tau` and weight `W=2^{-S}`.
- **Conditional:** interpreting `W` as a full continuum path-integral amplitude still needs an additional measure and continuum limit theorem.

## Executable artifact

- Verifier: `verify_dccxxxvi_closure_action_weight_bridge.py`
- Tests: `tests/test_dccxxxvi_closure_action_weight_bridge.py`
- Data: `data/dccxxxvi_closure_action_weight_bridge.json`
