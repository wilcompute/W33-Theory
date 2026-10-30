# V45 — Exact Inflation Observable Closure from W(3,3)

## Main point

The repaired inflation sector now closes **algebraically**: once the exact e-fold count is fixed, the primordial observables are no longer independent. They satisfy a rigid closure packet with **no hidden inflation parameter left**.

The key bridge is that the two existing e-fold derivations are exactly the same number:

- `N = E / mu = 240 / 4 = 60`
- `N = 2 (v - Phi_4) = 2 (40 - 10) = 60`

So the edge-count derivation and the inflaton-mode derivation coincide:

\[
N \,=\, \frac{E}{\mu} \,=\, 2(v-\Phi_4) \,=\, 60.
\]

Equivalently,

\[
E = 2\mu (v-\Phi_4).
\]

For W(3,3), with `mu = 4`, this specializes to

\[
E = 8(v-\Phi_4) = 8 \cdot 30 = 240.
\]

## Exact closure packet

Using the Starobinsky relations already adopted in the repo,

\[
n_s = 1 - \frac{2}{N}, \qquad r = \frac{12}{N^2}, \qquad \alpha_{\rm run} = \frac{dn_s}{d\ln k} = -\frac{2}{N^2}, \qquad n_T = -\frac{r}{8}, \qquad f_{NL} = \frac{5}{12}(n_s-1).
\]

At `N = 60` this gives

- \(n_s = 29/30\)
- \(r = 1/300\)
- \(\alpha_{\rm run} = -1/1800\)
- \(n_T = -1/2400\)
- \(f_{NL} = -1/72\)

Now eliminate `N`. The observables obey the exact relations

\[
r = 3(1-n_s)^2,
\]

\[
\alpha_{\rm run} = -\frac{1}{2}(1-n_s)^2 = -\frac{r}{6},
\]

\[
n_T = -\frac{r}{8} = \frac{3}{4}\,\alpha_{\rm run},
\]

\[
f_{NL} = -\frac{5}{12}(1-n_s).
\]

## Why this matters

This is stronger than just listing several successful inflation numbers. It says the repaired W(3,3) inflation sector defines a **one-parameter rigidity class**, and once `N=60` is fixed by the graph, the remaining primordial observables are chained together exactly.

So the inflation sector is now not merely a set of separate matches:

- one graph-fixed e-fold count,
- one exact observable packet,
- multiple exact closure identities among observables.

That is the right next level of structure after the recent `r = 1/300` repair.
