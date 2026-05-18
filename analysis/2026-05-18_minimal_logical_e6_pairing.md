# Minimal Logical E6 Pairing Theorem

## Executive result

For the canonical W(3,3) edge CSS code

\[
[[240,81,3]]_3,
\qquad d_X=3,
\qquad d_Z=4,
\]

the minimal logical witnesses have the following corrected counts:

| Object | Count |
|---|---:|
| minimal X supports | 160 |
| minimal X unique \(\mathbb F_3\) vectors | 320 |
| minimal Z supports | 1620 |
| minimal Z unique \(\mathbb F_3\) vectors | 3240 |
| minimal Z oriented-walk presentations | 6480 |

The convention correction is important:

\[
\boxed{6480\text{ counts oriented-walk presentations, not unique }\mathbb F_3\text{ vectors}.}
}
\]

The unique vector count is

\[
\boxed{3240=2\cdot1620=40\cdot81.}
\]

## Support-level incidence

At the support level, the minimal X/Z incidence graph is biregular:

\[
160\cdot81=1620\cdot8=12960.
\]

So every minimal X support meets exactly \(81\) minimal Z supports, and every minimal Z support meets exactly \(8\) minimal X supports.

This is already structural:

- \(81\) is the protected \(H_1\) logical sector.
- \(8\) is the tomotope cell count.

## Vector-level commutation census

At the actual \(\mathbb F_3\)-vector level, there are

\[
320\cdot3240=1{,}036{,}800
\]

total X/Z minimal-vector pairs.

The symplectic pairing phase counts are:

| Phase | Count |
|---:|---:|
| 0 | 984960 |
| 1 | 25920 |
| 2 | 25920 |

Therefore the number of nonzero pairings is

\[
25920+25920=51840.
\]

And

\[
\boxed{51840=|W(E_6)|.}
\]

Equivalently, the noncommutation graph is biregular:

\[
320\cdot162=3240\cdot16=51840.
\]

So every minimal X vector fails to commute with exactly \(162\) minimal Z vectors, and every minimal Z vector fails to commute with exactly \(16\) minimal X vectors.

## Closed forms

The full census collapses into substrate primitives:

\[
X_{\min}^{\mathrm{supp}}=160=40\cdot4,
\]

\[
X_{\min}^{\mathbb F_3}=320=2\cdot160=40\cdot2^3,
\]

\[
Z_{\min}^{\mathrm{supp}}=1620=20\cdot81=60\cdot27,
\]

\[
Z_{\min}^{\mathbb F_3}=3240=40\cdot81,
\]

\[
Z_{\min}^{\mathrm{oriented}}=6480=240\cdot27=80\cdot81=\frac{|W(E_6)|}{8},
\]

\[
\#\{(x,z):\langle x,z\rangle\neq0\}=51840=|W(E_6)|.
\]

## The theorem

**Minimal Logical E6 Pairing Theorem.** In the canonical W(3,3) edge CSS code over \(\mathbb F_3\), there are 320 minimal X logical vectors and 3240 unique minimal Z logical vectors. The number of nonzero symplectic pairings between them is exactly

\[
\boxed{51840=|W(E_6)|.}
\]

The nonzero phases split evenly:

\[
\boxed{25920+25920.}
\]

Equivalently, the noncommutation graph is biregular with X-degree \(162\) and Z-degree \(16\):

\[
\boxed{320\cdot162=3240\cdot16=51840.}
\]

## Interpretation

This is the cleanest E6 bridge so far.  The exceptional group does not enter as a fitted phenomenological number.  It appears as the exact number of elementary noncommuting interactions between the minimal logical X and Z error surfaces of the W(3,3) edge code.

In physical language, if the edge code is the protected qutrit substrate, then \(W(E_6)\) is the finite commutation shadow of its minimal logical error surface.

## Honesty boundary

This theorem is an exact finite CSS commutation census.  It does not by itself prove a physical anyon braid representation or a Standard Model prediction.  It gives the TQC/SM bridge a precise finite invariant that later physical interpretations must preserve.
