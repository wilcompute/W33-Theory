# Part DCCX — Holonomy Selector-Carrier-Weld Bridge

## Why this part exists

`Part DCCIX` showed a precise statistical closure:

- selector orientation cancels in first moment,
- orientation persists in one deterministic rank-1 covariance kernel.

The next question is structural:

> Is that covariance kernel merely a statistic, or is it already the single geometric carrier that welds the two selector orientations?

This part proves it is already the welded carrier.

## Weld law

From DCCIX, the two selector chart vectors are exactly antipodal:

$$
(81,-81),\;(-81,81).
$$

Averaging their outer products gives

$$
\Sigma =
\begin{bmatrix}
6561 & -6561\\
-6561 & 6561
\end{bmatrix},
$$

exactly the DCCIX covariance kernel.

So both selector charts are boundary orientations of one axis, not two unrelated laws.

## Projector/seam closure

Normalize by trace:

$$
P = \frac{1}{\operatorname{tr}(\Sigma)}\Sigma
= \frac{1}{2}
\begin{bmatrix}
1 & -1\\
-1 & 1
\end{bmatrix}.
$$

The verifier proves:

1. `P^2 = P` (idempotent rank-1 projector),
2. seam direction `(1,1)` is exactly kernel (`\Sigma(1,1)^T=0`),
3. weld axis `(81,-81)` is the unique nontrivial image direction.

So DCCIX's covariance is not just a moment statistic — it is the welded carrier geometry itself.

## Why this is a breakthrough

The live wall is now compressed from a two-chart selector ambiguity into one deterministic welded object:

> two selector orientations are boundary charts of one carrier weld with one seam kernel.

This reframes the frontier as a coherence/gluing problem rather than a remaining sign-choice problem.

## Executable artifact

Verifier:

```text
verify_dccx_holonomy_selector_carrier_weld_bridge.py
```

Tests:

```text
tests/test_dccx_holonomy_selector_carrier_weld_bridge.py
```

Generated summary:

```text
data/dccx_holonomy_selector_carrier_weld_bridge.json
```

---
*W33-Theory | Part DCCX | the two selector orientations are antipodal boundary charts of one welded carrier axis; DCCIX covariance is that welded rank-1 projector kernel.*
