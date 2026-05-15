# Part DCCXXXVII — Closure Geodesic Refinement Bridge

## Why this part exists

DCCXXXVI gave an exact discrete action/weight law:

```text
S = Delta_tau,
W = 2^{-S}.
```

But for fixed endpoints these are endpoint invariants; they do not yet distinguish coarse from finely resolved causal histories.

This part adds the missing extremal principle.

## Exact refinement action

Write a causal history from `T_a` to `T_b` as a positive-integer refinement of the total proper-time span:

```text
Delta_tau = d_1 + ... + d_m,   d_i >= 1.
```

Define the quadratic refinement action

```text
A_ref = d_1^2 + ... + d_m^2.
```

Then:

- the linear action is always

  ```text
  S = d_1 + ... + d_m = Delta_tau,
  ```

- the path weight is always

  ```text
  W = 2^{-Delta_tau},
  ```

- but the refinement action is uniquely minimized by the unit-step path

  ```text
  (1,1,...,1).
  ```

## The `0 -> 5` endpoint example

For the maximal closure span `T_0 -> T_5`, every refinement satisfies

```text
Delta_tau = 5,
S = 5,
W = 1/32.
```

Two extreme examples are:

- canonical monotone refinement:

  ```text
  [1,1,1,1,1],   A_ref = 5
  ```

- single coarse jump:

  ```text
  [5],           A_ref = 25
  ```

So the canonical unit-step closure path is selected by the exact extremal gap

```text
25 - 5 = 20.
```

## Meaning

The closure-time chain now has its first true equation-of-motion style statement:

- all causal refinements between fixed endpoints carry the same linear action,
- all carry the same endpoint weight,
- but the finest monotone closure history uniquely minimizes the quadratic refinement action.

This is the discrete geodesic principle of the closure chain.

## Exact vs conditional

- **Exact:** the unit-step monotone closure path uniquely minimizes `A_ref` among all positive-integer causal refinements with fixed endpoints.
- **Conditional:** promoting this to a continuum geodesic principle requires a separate limit theorem.

## Executable artifact

- Verifier: `verify_dccxxxvii_closure_geodesic_refinement_bridge.py`
- Tests: `tests/test_dccxxxvii_closure_geodesic_refinement_bridge.py`
- Data: `data/dccxxxvii_closure_geodesic_refinement_bridge.json`
