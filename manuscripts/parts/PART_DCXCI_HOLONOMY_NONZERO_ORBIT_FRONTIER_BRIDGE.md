# Part DCXCI — Holonomy Nonzero-Orbit Frontier Bridge

## Why this part exists

`Part DCXC` reduced the live frontier to one upper-right slot with current value `0` and exact live values `{1,2}` over `F3`.

The next question is whether those two live values are genuinely different frontier states.

This part proves that they are not.

## Exact orbit split

The verifier imports the known mixed-plane gauge equivalence and proves that the two live increments

$$
\begin{pmatrix}0&1\\0&0\end{pmatrix},
\qquad
\begin{pmatrix}0&2\\0&0\end{pmatrix}
$$

are conjugate under the adapted change of basis.

So they form one single nonzero orbit.

Meanwhile,

$$
\begin{pmatrix}0&0\\0&0\end{pmatrix}
$$

is a separate orbit.

## Why this is a breakthrough

This sharpens the frontier again.

It is no longer a three-valued slot problem.

It is a binary orbit problem:

- zero orbit,
- nonzero orbit.

So the remaining question is simply whether the host has crossed from the zero orbit to the unique nonzero orbit.

## Executable artifact

Verifier:

```text
verify_dcxci_holonomy_nonzero_orbit_frontier_bridge.py
```

Tests:

```text
tests/test_dcxci_holonomy_nonzero_orbit_frontier_bridge.py
```

Generated summary:

```text
data/dcxci_holonomy_nonzero_orbit_frontier_bridge.json
```

---
*W33-Theory | Part DCXCI | the two exact live slot values form one gauge-equivalent nonzero orbit, so the remaining frontier is binary: zero orbit versus nonzero orbit.*
