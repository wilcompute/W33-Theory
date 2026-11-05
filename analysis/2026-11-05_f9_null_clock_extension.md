# November 5, 2026 — An independent \(\mathbb F_9\) clock check

**Exact algebra; numerical check of integer eigenvalue census; physical scope closed.**

The primary theorem/certificate in
`analysis/w33_20261105_general_q_null_clock_continuum_guard.py`
is proved for every odd prime power using quadratic Gauss sums,
but its executable tests used prime fields \(q=3,5,7,11,13\).
This addendum independently tests the **non-prime** field \(q=9\).

Represent \(\mathbb F_9=\mathbb F_3[\alpha]/(\alpha^2+1)\) with
\(\alpha^2=2\). For symmetric matrices \(\begin{psmallmatrix}t&x\\x&y\end{psmallmatrix}\),
take \(Q=t^2-x^2-y^2\) in \(\mathbb F_9\). Their additive
group has \(9^3=729\) elements or six ternary coordinates.
Its nonzero null differences number \(9^2-1=80\).

A six-dimensional additive Fourier transform, treating the two field
coordinates exactly when forming the connection set, gives:

| adjacency eigenvalue | multiplicity |
|---|---:|
| 80 | 1 |
| 8 | 360 |
| -1 | 80 |
| -10 | 288 |

These match the odd-prime-power formula without substituting the
incorrect ring \(\mathbb Z/9\mathbb Z\) for \(\mathbb F_9\).
The Laplacian levels are \(0,72,81,90\);
\(U_9=\exp(-2\pi i L/81)\) has exact order 9 and 81 fixed modes.
The stochastic nontrivial spectral radius is \(1/8\).

This extension field is **not** evidence for a continuous space-time.
The mathematical family is a standard affine polar graph family;
the distinction is a verified cross-field continuation of the
`Forty Points` null-history clock with an explicit continuum guard.

Execute:
`python analysis/w33_20261105_f9_null_clock_extension.py`
and
`python -m pytest -q tests/test_w33_20261105_f9_null_clock_extension.py`.
