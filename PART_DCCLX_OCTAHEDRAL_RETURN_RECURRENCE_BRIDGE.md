# Part DCCLX — Octahedral Return/Recurrence Bridge

## Why this part exists

DCCLIX gave exact finite-time mixing clocks. This part adds exact return/recurrence structure for the same walk.

## Exact return profile

Using projector power law and diagonal projector constants, the verifier proves for any vertex `i`:

```text
p_t(i,i) = 1/6 + (1/3)(-1/2)^t,   t >= 1,
p_0(i,i) = 1.
```

So return probability oscillates around `1/6` with exponentially decaying amplitude.

## Exact mean return time (Kac)

The verifier proves by both linear hitting solve and stationary formula:

```text
E_i[T_i^+] = 1/pi_i = 6.
```

So recurrence time is exactly six steps in expectation.

## Exact generating function

For return generating function

```text
G(z) = sum_{t>=0} p_t(i,i) z^t,
```

the verifier proves closed form

```text
G(z) = 1 + z/(6(1-z)) + (1/3) * ((-z/2)/(1+z/2)).
```

and matches it numerically against long partial sums.

## Meaning

The octahedral closure random-walk chain now has:

- exact contraction and mixing-time laws,
- exact recurrence-time law,
- exact return generating function.

This is the cleanest exact recurrence/return bridge so far in the closure transport program.

## Exact vs conditional

- **Exact:** return profile, mean return time, and return generating function are all explicit and verified.
- **Conditional:** continuum recurrence interpretation still requires a scaling limit.

## Executable artifact

- Verifier: `verify_dcclx_octahedral_return_recurrence_bridge.py`
- Tests: `tests/test_dcclx_octahedral_return_recurrence_bridge.py`
- Data: `data/dcclx_octahedral_return_recurrence_bridge.json`
