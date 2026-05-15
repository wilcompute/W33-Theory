# Part DCCXXXIV — Proper-Time / Causal-Order Bridge

## Why this part exists

DCCXXXIII established the exact `3+1` split:

- `B23, B31, B12` are the three spatial channels,
- `tau = log2(C/12)` is the fourth scalar channel.

This part strengthens that statement. It shows the fourth channel is not just a count label but a **discrete proper-time scalar**:

- invariant under spatial symmetries,
- monotone across closure updates,
- organizing the process into totally ordered causal classes.

## Exact statement

Let

```text
T_a <= T_b   iff   tau_a <= tau_b.
```

Then the distinct proper-time levels are exactly

```text
0, 1, 2, 3, 4, 5,
```

with representative scales

```text
12, 24, 48, 96, 192, 384.
```

Successive proper-time jumps satisfy

```text
delta_tau = 1,
scale_ratio = 2.
```

So one unit of proper time is one doubling step in the closure-driven codec flow.

## Spatial symmetry separation

The spatial triad `B23, B31, B12` has:

- `3! = 6` permutations,
- `2^3 = 8` sign choices,
- total `48` signed spatial symmetries.

The verifier checks that proper-time history is unchanged under this whole signed-permutation orbit. Therefore:

- **space** transforms,
- **proper time** does not.

This is the exact discrete analogue of a scalar proper-time channel separated from spatial frame choice.

## Meaning

The closure process now has a rigorous causal skeleton:

- the three bivectors form the spatial frame,
- the closure clock gives the proper-time scalar,
- causal classes are the distinct `tau` levels,
- the future direction is the monotone increase of `tau`.

So the fourth dimension is not merely “the extra thing after 3.”
It is the **symmetry-invariant ordered accumulation of closure events**.

## Exact vs conditional

- **Exact:** proper time is the scalar `tau` labeling the totally ordered closure classes.
- **Conditional:** identifying this discrete proper time with continuum relativistic proper time still needs a separate dynamical/continuum theorem.

## Executable artifact

- Verifier: `verify_dccxxxiv_proper_time_causal_order_bridge.py`
- Tests: `tests/test_dccxxxiv_proper_time_causal_order_bridge.py`
- Data: `data/dccxxxiv_proper_time_causal_order_bridge.json`
