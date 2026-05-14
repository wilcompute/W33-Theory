# Part DCLXXIX — Holonomy Balanced Core Bridge

## Why this part exists

`Part DCLXXVIII` identified the exact minimal `39`-state host architecture.

The next deeper question is whether that host already contains a canonical energy-ordered core.

This part proves the stronger statement:

> the explicit minimal host realization is already balanced, and its principal balanced core is exactly the `15`-dimensional slow sector.

## Exact balanced structure

For the minimal host realization from `Part DCLXXVIII`, the verifier proves that the controllability and observability Gramians coincide exactly.

So the realization is already balanced.

Its two Hankel singular values are exactly

$$
\sigma_{\mathrm{fast}} = \frac{1}{2\log(4)},
\qquad
\sigma_{\mathrm{slow}} = \frac{1}{2\log(5/2)}.
$$

Because

$$
\log\!\left(\frac52\right) < \log(4),
$$

we get

$$
\sigma_{\mathrm{slow}} > \sigma_{\mathrm{fast}}.
$$

So the slow sector carries the larger balanced energy weight.

## Principal balanced core

The verifier proves that the rank-`15` retained balanced core is exactly the slow sector, with reduced transfer function

$$
R_{\mathrm{slow}}(s)=\frac{P_-}{s+\log(5/2)}.
$$

The discarded rank-`24` piece is exactly the fast sector,

$$
R_{\mathrm{fast}}(s)=\frac{P_+}{s+\log(4)}.
$$

And the full transfer law splits exactly as

$$
R(s)=R_{\mathrm{fast}}(s)+R_{\mathrm{slow}}(s).
$$

So the balanced reduction does not merely approximate the slow tail qualitatively.

It isolates it exactly.

## Why this is a breakthrough

This sharpens the architectural picture again:

- `DCLXXVIII` said any exact host must carry `24+15` internal states.
- `DCLXXIX` says the canonical retained host core is the `15`-dimensional slow sector.

So the theory now distinguishes between:

- the full exact host architecture, and
- the exact principal core that carries the dominant long-time balanced weight.

That is the cleanest host-level compression in the chain so far.

## Executable artifact

Verifier:

```text
verify_dclxxix_holonomy_balanced_core_bridge.py
```

Tests:

```text
tests/test_dclxxix_holonomy_balanced_core_bridge.py
```

Generated summary:

```text
data/dclxxix_holonomy_balanced_core_bridge.json
```

---
*W33-Theory | Part DCLXXIX | the exact minimal holonomy host is already balanced, and its principal retained core is exactly the 15-dimensional slow sector.*
