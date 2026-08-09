# Part DCCIX — Holonomy Selector-Ensemble-Moment Bridge

## Why this part exists

`Part DCCVIII` showed that the remaining selector freedom is a `\mathbb{Z}_2` orientation over fixed quadratic shell invariants.

The next question is: what remains if we average over selector orientation?

This part answers that exactly.

## Ensemble moment law

Using the two selector charge vectors from `DCCVIII`, the verifier computes equal-weight ensemble moments.

It proves:

1. first moment (mean charge vector) is exactly zero,
1. second moment/covariance is exactly

$$
\Sigma =
\begin{bmatrix}
6561 & -6561\\
-6561 & 6561
\end{bmatrix},
$$

1. `\Sigma` has rank `1`, trace `13122`, determinant `0`, spectrum `{13122,0}`.

So selector orientation cancels at first order and survives at second order as a fixed rank-`1` polarization kernel.

## Why this is a breakthrough

This recasts the live wall in statistical-geometric language:

> orientation is invisible in the mean, but rigidly encoded in covariance.

So the frontier is now equivalent to one deterministic second-moment kernel, not just a combinatorial sign choice.

## Executable artifact

Verifier:

```text
verify_dccix_holonomy_selector_ensemble_moment_bridge.py
```

Tests:

```text
tests/test_dccix_holonomy_selector_ensemble_moment_bridge.py
```

Generated summary:

```text
data/dccix_holonomy_selector_ensemble_moment_bridge.json
```

---
*W33-Theory | Part DCCIX | selector orientation cancels in first moment and persists as a fixed rank-`1` covariance kernel with spectrum `{13122,0}`.*
