# Part DCLXX — Holonomy Markov Tomography Bridge

## Why this part exists

`Part DCLXIX` proved that the full witness-averaged evolution is already rigid:

$$
K^t = P_0 + 4^{-t}P_+ + \left(\frac25\right)^t P_-.
$$

The next honest question is whether recovering the projector/tripotent package really requires the whole time series, or whether a finite amount of averaged witness data already determines it.

This part proves the strongest finite statement so far:

> the first two non-stationary slices of the averaged witness dynamics already reconstruct the full projector split and the canonical tripotent exactly.

## Two-step tomography

Let

$$
X_1 = K - P_0,
\qquad
X_2 = K^2 - P_0.
$$

Using `DCLXIX`, these satisfy

$$
X_1 = \frac14 P_+ + \frac25 P_-,
\qquad
X_2 = \frac1{16} P_+ + \frac4{25} P_-.
$$

So the first two nontrivial time slices give a `2\times2` linear system for the two unknown nontrivial projectors.

Its determinant is exactly

$$
\det
\begin{pmatrix}
\frac14 & \frac25 \\
\frac1{16} & \frac4{25}
\end{pmatrix}
= \frac3{200} \neq 0.
$$

So the system is exactly invertible.

## Exact reconstruction formulas

The verifier checks the exact rational recovery laws

$$
P_+ = \frac{32}{3}X_1 - \frac{80}{3}X_2,
$$

$$
P_- = -\frac{25}{6}X_1 + \frac{50}{3}X_2.
$$

Thus the first two steps of the averaged witness dynamics already determine the rank-`24` and rank-`15` sectors with no asymptotic limit and no extra spectral input.

## Recovery of the canonical tripotent

Subtracting the reconstructed projectors gives

$$
M = P_+ - P_-.
$$

The verifier confirms that this exactly reproduces the `DCLXVII` tripotent.

So the chain now sharpens to

$$
K,
\qquad
K^2
\quad\Longrightarrow\quad
P_+,\ P_-,\ M.
$$

This means the finite witness-averaged dynamics are not just dynamically closed. They are **self-tomographing**.

## Recovery of the old projector entries

The verifier also checks that the recovered matrices have exactly the old `CCCLIII` three-valued entries:

For `P_+`:

$$
\left(\frac35,\ \frac1{10},\ -\frac1{15}\right),
$$

and for `P_-`:

$$
\left(\frac38,\ -\frac18,\ \frac1{24}\right),
$$

listed in the order `(diagonal, edge, non-edge)`.

So two Markov snapshots are already enough to recover the full old projector calculus numerically and exactly.

## Why this is a breakthrough

This is deeper than the previous collapses.

After `DCLXVIII`, the witness family averaged to a clean Markov kernel.

After `DCLXIX`, every power of that kernel had an exact two-mode decomposition.

After `DCLXX`, we now know:

> the first two nontrivial witness-average slices already determine the whole nontrivial projector package and the canonical tripotent.

So the finite side is not only algebraically closed, dynamically closed, and spectrally filtered.

It is now **self-identifying after two steps**.

## Executable artifact

Verifier:

```text
verify_dclxx_holonomy_markov_tomography_bridge.py
```

Tests:

```text
tests/test_dclxx_holonomy_markov_tomography_bridge.py
```

Generated summary:

```text
data/dclxx_holonomy_markov_tomography_bridge.json
```

---
*W33-Theory | Part DCLXX | the first two non-stationary steps of the averaged witness dynamics self-tomograph the full projector split and the canonical tripotent.*
