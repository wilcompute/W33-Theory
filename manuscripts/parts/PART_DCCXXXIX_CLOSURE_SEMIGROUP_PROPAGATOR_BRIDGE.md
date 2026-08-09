# Part DCCXXXIX — Closure Semigroup / Propagator Bridge

## Why this part exists

DCCXXXVIII gave the local Bellman recursion that generates the closure geodesic law. The next natural step is to package that law as a true propagator / semigroup statement.

## Exact propagator definitions

For causal classes `T_a <= T_b`, define

```text
J(a,b) = tau_b - tau_a,
K(a,b) = 2^{-J(a,b)}.
```

So:

- `J` is the closure value propagator,
- `K` is the closure weight propagator.

## Exact semigroup laws

The verifier proves two parallel composition rules.

### 1. Min-plus value composition

```text
J(a,c) = min_b ( J(a,b) + J(b,c) ).
```

On this chain, every intermediate causal class `b` already saturates the minimum, because proper-time span is exactly additive.

### 2. Multiplicative weight composition

```text
K(a,c) = K(a,b) K(b,c).
```

Again, every intermediate `b` saturates the identity exactly.

## Endpoint example

For the maximal propagation `T_0 -> T_5`:

```text
J(0,5) = 5,
K(0,5) = 1/32.
```

And for any intermediate `b` in `{0,1,2,3,4,5}`,

```text
J(0,5) = J(0,b) + J(b,5),
K(0,5) = K(0,b) K(b,5).
```

So the closure chain has exact semigroup propagation, not just a recursive minimization rule.

## Meaning

The emergent-time thread now has:

- proper time,
- interval,
- action,
- geodesic refinement,
- Bellman recursion,
- and a propagator semigroup.

This is the first exact evolution law in genuinely semigroup form.

## Exact vs conditional

- **Exact:** the finite closure chain obeys min-plus and multiplicative propagator composition laws.
- **Conditional:** identifying this with a continuum semigroup kernel still requires a limit construction.

## Executable artifact

- Verifier: `verify_dccxxxix_closure_semigroup_propagator_bridge.py`
- Tests: `tests/test_dccxxxix_closure_semigroup_propagator_bridge.py`
- Data: `data/dccxxxix_closure_semigroup_propagator_bridge.json`
