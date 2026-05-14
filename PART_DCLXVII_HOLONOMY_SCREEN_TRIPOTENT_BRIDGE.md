# Part DCLXVII — Holonomy Screen Tripotent Bridge

## Why this part exists

`Part DCLXVI` showed that the universal holonomy-screen family is already the operator

$$
S = A + I
$$

inside the `W(3,3)` adjacency algebra.

The next honest question is whether the whole family can be collapsed even further to one canonical normalized operator with a direct spectral meaning.

This part proves that the answer is **yes**.

## The canonical normalized screen operator

Let `A` be the `W(3,3)` adjacency matrix, `J` the all-ones matrix, and `S=A+I` the screen operator from `DCLXVI`.

Define

$$
M = \frac{S - 13J/40}{3} = \frac{A + I - 13J/40}{3}.
$$

This is exactly the three-channel interpolation operator with spectral values

$$
f(12)=0, \qquad f(2)=1, \qquad f(-4)=-1.
$$

So the whole universal screen bundle collapses to one rational operator with coefficients

$$
M = \frac{1}{3}I + \frac{1}{3}A - \frac{13}{120}J.
$$

## Tripotent closure

The verifier checks the exact identities

$$
M^2 = I - \frac{J}{40},
\qquad
M^3 = M.
$$

So `M` is a **symmetric tripotent**.

Its spectrum is exactly

$$
\operatorname{Spec}(M)=\{0^1,\ 1^{24},\ (-1)^{15}\}.
$$

That means:

- the trivial all-ones mode is annihilated,
- the `24`-dimensional nontrivial positive sector gets eigenvalue `+1`,
- the `15`-dimensional nontrivial negative sector gets eigenvalue `-1`.

So the universal screen family is now a single canonical polarization of the nontrivial `W(3,3)` carrier.

## Recovery of the old projector calculus

From the tripotent, the verifier builds the three idempotents

$$
P_0 = I - M^2,
\qquad
P_+ = \frac{M^2 + M}{2},
\qquad
P_- = \frac{M^2 - M}{2}.
$$

These are orthogonal, complete, and have ranks

$$
\mathrm{rank}(P_0)=1,
\qquad
\mathrm{rank}(P_+)=24,
\qquad
\mathrm{rank}(P_-)=15.
$$

Most importantly, the verifier proves that these are **exactly** the older W(3,3) projector formulas from the existing projector calculus:

$$
P_0 = \frac{J}{40},
$$

$$
P_+ = -\frac{(A-12I)(A+4I)}{60},
$$

$$
P_- = \frac{(A-12I)(A-2I)}{96}.
$$

So the tripotent bridge does not create a new spectral package. It compresses the old projector package into one canonical normalized screen operator.

## Why this is a breakthrough

This is the cleanest finite collapse so far.

After `DCLXIV`, the wall became one explicit qutrit transvection.

After `DCLXV`, it became a universal `40`-anchor family.

After `DCLXVI`, that family became the operator `A+I`.

After `DCLXVII`, the whole package becomes one canonical rational tripotent:

> the universal holonomy-screen family, the adjacency-algebra closure, and the older W(3,3) projector calculus are all the same object seen at different normalizations.

So the honest remaining task is no longer to discover a new finite operator or projector package.

It is:

> realize this one canonical tripotent polarization on the fixed mixed-plane host.

## Executable artifact

Verifier:

```text
verify_dclxvii_holonomy_screen_tripotent_bridge.py
```

Tests:

```text
tests/test_dclxvii_holonomy_screen_tripotent_bridge.py
```

Generated summary:

```text
data/dclxvii_holonomy_screen_tripotent_bridge.json
```

---
*W33-Theory | Part DCLXVII | the universal holonomy-screen bundle collapses to a canonical rational tripotent whose idempotents are exactly the older W(3,3) eigenspace projectors.*
