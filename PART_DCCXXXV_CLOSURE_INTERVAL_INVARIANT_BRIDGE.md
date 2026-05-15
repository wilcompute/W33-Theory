# Part DCCXXXV — Closure-Interval Invariant Bridge

## Why this part exists

DCCXXXIV showed that the closure process carries a symmetry-invariant discrete proper time `tau` with causal classes

```text
T_0, T_1, T_2, T_3, T_4, T_5.
```

This part turns that ordered clock into an exact interval law.

## Exact interval definition

For causal classes `T_a <= T_b`, define

```text
Delta_tau(a,b) = tau_b - tau_a,
sigma(a,b) = Delta_tau(a,b)^2.
```

This is the discrete proper-time interval on the closure chain.

Because DCCXXXII already proved the scale law

```text
C = 12 * 2^tau,
```

we get immediately

```text
Delta_tau(a,b) = log2(C_b / C_a),
sigma(a,b) = (log2(C_b / C_a))^2.
```

So interval is not an extra postulate. It is already encoded in the codec flow.

## What is proved exactly

The verifier checks:

- there are exactly 6 causal classes,
- interval vanishes on the diagonal,
- `Delta_tau` is additive along causal chains,
- scale ratio is exactly `2^{Delta_tau}`,
- `sigma` is exactly the square of the logarithmic scale ratio,
- the maximal interval is the `0 -> 5` jump:
  - `Delta_tau = 5`
  - `sigma = 25`
  - `C_5 / C_0 = 32`

## Meaning

The chain now has a genuine discrete interval structure:

- **space** is the Clifford bivector frame,
- **proper time** is the monotone scalar `tau`,
- **interval** is the invariant square `sigma = (Delta_tau)^2`.

This is the cleanest exact discrete analogue so far of a proper-time interval built from closure dynamics rather than assumed a priori.

## Exact vs conditional

- **Exact:** the closure chain carries an exact interval invariant `sigma=(Delta_tau)^2`.
- **Conditional:** identifying this with a continuum Lorentzian interval still requires a separate limit theorem.

## Executable artifact

- Verifier: `verify_dccxxxv_closure_interval_invariant_bridge.py`
- Tests: `tests/test_dccxxxv_closure_interval_invariant_bridge.py`
- Data: `data/dccxxxv_closure_interval_invariant_bridge.json`
