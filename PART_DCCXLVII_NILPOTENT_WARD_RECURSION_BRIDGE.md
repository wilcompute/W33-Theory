# Part DCCXLVII - Nilpotent Ward-Recursion Bridge

## Why this part exists

DCCXLVI proved the full finite jet tower for the nilpotent closure action.
That is a complete response table, but a response table is weaker than an
equation of motion.

This part proves that the same nilpotent generator enforces an exact finite
Ward / Schwinger-Dyson recursion for every jet.

## Exact finite recursion

Let

```text
A(z) = -log(I - zG)
```

with the six-state nilpotent generator `G` from the closure-clock chain.
At `z=1`, the verifier proves:

```text
(I - G) A'(1) = G
(I - G) A^(r)(1) = (r - 1) G A^(r-1)(1),  r = 2..6.
```

Because every jet is a polynomial in `G`, the right-sided equations hold too:

```text
A^(r)(1) (I - G) = (r - 1) A^(r-1)(1) G,  r = 2..6.
```

## Terminal order

The sixth jet is zero, but the recursion still closes honestly:

```text
A^(6)(1) = 0
G A^(5)(1) = 0
A^(5)(1) G = 0
```

So the terminal equation is not an arbitrary cutoff.  The nilpotent generator
itself kills the fifth response.

## Meaning

The closure-action stack now has:

```text
propagator -> action -> finite jets -> Ward recursion.
```

This is the first finite equation-of-motion layer for the nilpotent proper-time
architecture.  The action is not only differentiable inside the finite package;
its derivatives are recursively sourced by the same operator that generated the
closure propagator.

## Exact vs conditional

- **Exact:** the finite nilpotent action obeys the left and right Ward
  recursions through the terminal sixth order.
- **Conditional:** interpreting this finite recursion as a continuum
  Schwinger-Dyson equation still requires a scaling limit.

## Executable artifact

- Verifier: `verify_dccxlvii_nilpotent_ward_recursion_bridge.py`
- Tests: `tests/test_dccxlvii_nilpotent_ward_recursion_bridge.py`
- Data: `data/dccxlvii_nilpotent_ward_recursion_bridge.json`
