# Part DCCLIX — Octahedral Exact Mixing-Time Bridge

## Why this part exists

DCCLVIII gave the sharp global one-step TV contraction coefficient `alpha = 1/2`. This part integrates that into an exact closed formula for `epsilon`-mixing time.

## Exact TV profile

For delta-start walk law on octahedron, the verifier proves

```text
TV_0 = 5/6,
TV_t = (2/3) 2^{-t}   for t >= 1.
```

So convergence is exactly geometric after the first step.

## Exact mixing-time formula

Define

```text
tau(epsilon) = min { t : TV_t <= epsilon }.
```

Then the verifier proves

```text
tau(epsilon) = ceil(max(1, log2(2/(3 epsilon)))).
```

It also checks this matches brute-force worst-case TV search for sample `epsilon` values.

## Sample exact values

The verifier recovers:

- `tau(0.1) = 3`,
- `tau(0.01) = 7`.

So the closure walk has an exact finite-time convergence clock, not only asymptotic rates.

## Meaning

The octahedral transport/mixing chain now has:

- sharp one-step contraction,
- exact multistep decay profile,
- exact epsilon-mixing time formula.

This is the cleanest exact finite-time equilibration theorem so far in the closure random-walk program.

## Exact vs conditional

- **Exact:** octahedral TV profile and epsilon-mixing time are given by explicit closed formulas.
- **Conditional:** continuum equilibration-time interpretation still requires a scaling limit.

## Executable artifact

- Verifier: `verify_dcclix_octahedral_exact_mixing_time_bridge.py`
- Tests: `tests/test_dcclix_octahedral_exact_mixing_time_bridge.py`
- Data: `data/dcclix_octahedral_exact_mixing_time_bridge.json`
