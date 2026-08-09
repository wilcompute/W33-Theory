# Part DCLXXVIII — Holonomy Minimal Host Realization Bridge

## Why this part exists

`Part DCLXXV` fixed the exact transfer function.

`Part DCLXXVI` fixed the exact boundary scattering law.

`Part DCLXXVII` fixed the exact two-atom relaxation measure.

The next deeper question is what this forces on any actual host realization.

This part proves the stronger statement:

> the non-stationary holonomy future has an explicit self-adjoint minimal realization of dimension `39`, split exactly into `24` fast states and `15` slow states.

So any exact mixed-plane host realization must implement at least this `24+15` internal dynamic architecture, while the rank-`1` stationary mode remains purely transmitted at the boundary.

## Exact host realization

Let `U_+` and `U_-` be orthonormal bases for the ranges of `P_+` and `P_-`.

Then the verifier constructs the exact realization

$$
A = \operatorname{diag}\bigl(-\log(4) I_{24},\,-\log(5/2) I_{15}\bigr),
$$

$$
B = \begin{bmatrix} U_+^T \\ U_-^T \end{bmatrix},
\qquad
C = \begin{bmatrix} U_+ & U_- \end{bmatrix}.
$$

This realizes the full non-stationary transfer law:

$$
R(s)=C(sI-A)^{-1}B
=\frac{P_+}{s+\log(4)}+\frac{P_-}{s+\log(5/2)}.
$$

## Minimality

The verifier proves that:

- the fast residue rank is exactly `24`,
- the slow residue rank is exactly `15`,
- the dynamic mass is exactly the rank-`39` stationary complement,
- the controllability and observability Gramians are positive definite.

So the McMillan degree is exactly

$$
24 + 15 = 39.
$$

Therefore no exact host realization can use fewer than `39` internal dynamic states.

## Why this is a breakthrough

This is the first layer in the chain that gives an exact architectural lower bound.

The previous parts told us what the holonomy future is.

This part tells us what any exact host must contain:

- `1` transmitted stationary channel,
- `24` fast internal states,
- `15` slow internal states.

So the theory now constrains not just the finite witness object, but the minimum internal architecture of any realization that could carry it.

## Executable artifact

Verifier:

```text
verify_dclxxviii_holonomy_minimal_host_realization_bridge.py
```

Tests:

```text
tests/test_dclxxviii_holonomy_minimal_host_realization_bridge.py
```

Generated summary:

```text
data/dclxxviii_holonomy_minimal_host_realization_bridge.json
```

---
*W33-Theory | Part DCLXXVIII | any exact host realization of the non-stationary holonomy future must carry a minimal 39-state internal architecture split into 24 fast and 15 slow modes.*
