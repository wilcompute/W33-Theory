# Part DCCXLVIII - Retarded Green Uniqueness Bridge

## Why this part exists

DCCXLVII proved the finite Ward recursion for the nilpotent action jets.  The
next question is whether those source equations merely admit the known jets, or
whether the jets are forced.

This part proves they are forced inside the six-level closure-clock sector.

## Exact retarded inverse

With `D = I - G`, the closure propagator from DCCXL is:

```text
K = D^(-1) = I + G + G^2 + G^3 + G^4 + G^5.
```

The verifier checks both sides:

```text
D K = I
K D = I.
```

So the Ward equations have a unique finite retarded solution.

## Source-to-jet solution

For every Ward source `S_r` from DCCXLVII:

```text
A^(r)(1) = K S_r = S_r K,  r = 1..6.
```

The first source resolves to the strict propagator part:

```text
K G = K - I.
```

The terminal source resolves to zero:

```text
K S_6 = S_6 K = 0.
```

## No hidden homogeneous branch

If a homogeneous response `H` satisfied

```text
D H = 0,
```

then multiplying by `K` gives:

```text
H = K 0 = 0.
```

So this finite sector has no extra homogeneous mode hiding behind the Ward
recursion.  That matters architecturally: the closure-clock response is
deterministic once the Ward source is fixed.

## Exact vs conditional

- **Exact:** `K` is the two-sided finite inverse of `I-G`; all Ward sources
  have unique retarded solutions; the terminal source maps to the zero sixth
  jet.
- **Conditional:** interpreting this as a continuum retarded Green function
  still requires a separate external scaling theorem.

## Executable artifact

- Verifier: `verify_dccxlviii_retarded_green_uniqueness_bridge.py`
- Tests: `tests/test_dccxlviii_retarded_green_uniqueness_bridge.py`
- Data: `data/dccxlviii_retarded_green_uniqueness_bridge.json`
