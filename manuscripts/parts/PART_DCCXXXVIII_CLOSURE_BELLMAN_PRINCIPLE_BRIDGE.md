# Part DCCXXXVIII — Closure Bellman-Principle Bridge

## Why this part exists

DCCXXXVII proved a global extremal law: among all causal refinements with fixed endpoints, the unit-step monotone history uniquely minimizes the quadratic refinement action.

This part derives the corresponding **local recursion** that generates that minimizer.

## Exact value function

For endpoint span `n >= 0`, define

```text
V(n) = min { d_1^2 + ... + d_m^2 : d_i >= 1, d_1 + ... + d_m = n }.
```

Then the closure chain satisfies the exact Bellman recursion

```text
V(0) = 0,
V(n) = min_{1 <= d <= n} (d^2 + V(n-d)).
```

## Exact solution on the closure chain

The verifier proves that for `n = 1,2,3,4,5`:

```text
V(n) = n,
```

and the unique minimizer in the Bellman step is always

```text
d = 1.
```

So the geodesic refinement principle is generated locally by the stationary unit-jump policy

```text
1,1,1,1,1.
```

Equivalently,

```text
V(n) = 1 + V(n-1).
```

This is the discrete Hamilton-Jacobi form of the closure geodesic law.

## Meaning

The closure chain now has a true recursive evolution principle:

- the global minimizer is no longer only recognized after the fact,
- it is produced step-by-step by a local optimality rule,
- and the rule is stationary: always take one unit of proper-time advance.

So the emergent-time thread now has:

- proper time,
- interval,
- action,
- geodesic minimization,
- and Bellman/Hamilton-Jacobi recursion.

## Exact vs conditional

- **Exact:** the closure geodesic law obeys the Bellman principle `V(n)=min_d(d^2+V(n-d))` with unique optimizer `d=1`.
- **Conditional:** promoting this discrete recursion to a continuum Hamilton-Jacobi equation requires a separate limit theorem.

## Executable artifact

- Verifier: `verify_dccxxxviii_closure_bellman_principle_bridge.py`
- Tests: `tests/test_dccxxxviii_closure_bellman_principle_bridge.py`
- Data: `data/dccxxxviii_closure_bellman_principle_bridge.json`
