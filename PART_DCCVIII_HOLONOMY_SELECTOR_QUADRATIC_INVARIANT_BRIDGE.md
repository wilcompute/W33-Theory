# Part DCCVIII — Holonomy Selector-Quadratic-Invariant Bridge

## Why this part exists

`Part DCCVII` identified the live selector as a signed polarization-charge choice:

$$
(+81,-81) \longleftrightarrow (-81,+81)
$$

under the selector flip `1 \leftrightarrow 2`.

The next step is to separate invariant shell data from oriented choice.

This part proves that separation exactly.

## Quadratic shell invariants

For each selector value, the verifier computes on ordered coordinates `(negative, positive)`:

- norm squared: `q_-^2 + q_+^2`,
- signed product: `q_- q_+`,
- orientation scalar: `q_+ - q_-`.

It proves:

1. norm squared is constant:

$$
81^2 + 81^2 = 13122,
$$

1. signed product is constant:

$$
(-81)(+81) = -6561,
$$

1. orientation scalar is exactly `\pm 162` and flips sign under selector flip.

So selector flip preserves the quadratic shell and only reverses orientation.

## Why this is a breakthrough

This isolates the remaining live freedom to a strict `\mathbb{Z}_2` orientation bit over fixed invariant data.

The frontier is now:

> fixed quadratic shell (`13122`, `-6561`) + one sign choice (`\pm 162`).

That is a sharper and more stable form than raw channel bookkeeping.

## Executable artifact

Verifier:

```text
verify_dccviii_holonomy_selector_quadratic_invariant_bridge.py
```

Tests:

```text
tests/test_dccviii_holonomy_selector_quadratic_invariant_bridge.py
```

Generated summary:

```text
data/dccviii_holonomy_selector_quadratic_invariant_bridge.json
```

---
*W33-Theory | Part DCCVIII | the live selector is a `\mathbb{Z}_2` orientation over a fixed quadratic invariant shell: norm `13122`, signed product `-6561`, orientation scalar `\pm 162`.*
