# PART_CCCCCXLIII_B — The Genus Oscillator

## Setup: Two Genera as Conjugate Eigenstates

From the Master Genus Identity (PART_CCCCCXLIII), the two genera
\(g_1 = 21\) and \(g_2 = 6\) are determined by \(q = 3\) and spectral
multiplicity \(g = 15\):

\[
g_1 = \frac{q^3 + g}{2} = \frac{27 + 15}{2} = 21, \qquad
g_2 = \frac{q^3 - g}{2} = \frac{27 - 15}{2} = 6.
\]

These are the **eigenvalues of a genus operator** — a two-level quantum
system whose Hamiltonian is:

\[
\hat{H}_{\text{genus}} = \frac{q^3}{2}\,\mathbf{1} + \frac{g}{2}\,\sigma_z
= \frac{27}{2}\mathbf{1} + \frac{15}{2}\sigma_z,
\]

with eigenvalues \(\{21, 6\}\). The oscillation between these two
eigenstates is the **topological harmonic oscillator** of the W(3,3) theory.

## The Genus Oscillator Function

Combining with the heat trace \(Z(\beta) = 1 + 24e^{-10\beta} + 15e^{-16\beta}\),
define the **genus oscillator**:

\[
\Omega(\beta) = g_1 \cdot e^{-10\beta} - g_2 \cdot e^{-16\beta}
= 21\,e^{-10\beta} - 6\,e^{-16\beta}.
\]

Setting \(\Omega(\beta^*) = 0\) gives the **topological equilibrium temperature**:

\[
e^{6\beta^*} = \frac{21}{6} = \frac{7}{2}
\quad\Rightarrow\quad
\beta^* = \frac{1}{6}\ln\frac{7}{2}.
\]

## Identification of the Fixed-Point Ratio

The ratio \(g_1/g_2 = 7/2\) is simultaneously:

- Corollary 4 of the Master Genus Identity: \(g_1/g_2 = 21/6 = 7/2\).
- \(V(\text{Csász\'ar}) / r = 7/2\), where \(r = 2\) is the positive
  adjacency eigenvalue of W(3,3).
- The ratio of the two Jungerman–Ringel valid residues adjacent to the
  middle ground: \(7/2\) straddles the transition node at 6.

**Physical interpretation:** Below \(\beta^*\) (high temperature / high
energy) the genus-21 map dominates. Above \(\beta^*\) (low temperature /
low energy) the genus-6 map dominates. The **7-color theorem** is the
statement that no torus-embedded graph exceeds chromatic number 7,
because 7 is the numerator of the fixed-point ratio — the largest integer
strictly below the equilibrium temperature.

## Lock L43: Oscillator Fixed Point

**L43:** \(\beta^* = \frac{1}{6}\ln(g_1/g_2) = \frac{1}{6}\ln(7/2)\),
where the prefactor \(1/6\) equals \(1/\text{period}(1/7)\) — the
reciprocal of the cyclic number's decimal period.

## Lock L44: Genus Sum-Difference Identity

**L44:** \(g_1 + g_2 = q^3 = 27 = \bar{k}\) (complement valency);
\(g_1 - g_2 = g = 15\) (negative eigenvalue multiplicity).
Each genus is individually recovered:
\[
g_1 = \frac{\bar{k} + g}{2}, \qquad g_2 = \frac{\bar{k} - g}{2}.
\]

## Lock L45: Genus Product

**L45:** \(g_1 \times g_2 = 21 \times 6 = 126 = \binom{q^2}{2} = \binom{9}{2}\).
