# PART_CCCCCLX — The Tetrahedral Harmonic Oscillator Tower

## Overview

The Császár polyhedron, Szilassi polyhedron, the tomotope, and W(3,3) are not independent structures. They form the **levels of a tetrahedral harmonic oscillator** — a tower of maximal-adjacency objects whose invariants (vertex counts, edge counts, genera) are all W(3,3) parameters.

## The Tower

| Level | Object | V | E | genus | W(3,3) parameter |
|---|---|---|---|---|---|
| 0 | K₄ (tetrahedron) | 4 | 6 | 0 | GQ line; \(|\mathrm{Aut}(K_4)| = 24 = f\) |
| 1 | K₆ | 6 | 15 | 1 | \(E = g = 15\) (neg eigenvalue mult) |
| 1 | K₇ = Császár | 7 | 21 | 1 | \(E = g_1 = 21\) (W(3,3) surface genus) |
| 1\* | Szilassi (dual) | 14 | 21 | 1 | \(V = 7r = 14\); \(F = 7\) |
| 2 | Tomotope / 24-cell | 24 | 96 | 0 | \(V = f = 24\) (pos eigenvalue mult) |
| \(\infty\) | W(3,3) | 40 | 240 | 21/6 | The organiser of all levels |

## Physical Interpretation

Each level corresponds to an **energy level** of the tetrahedral oscillator.

The Laplacian spectrum of \(K_n\) is \(\{0^{(1)}, n^{(n-1)}\}\), giving partition function:
\[
Z_{K_n}(\beta) = 1 + (n-1)e^{-n\beta}.
\]

Comparing with W(3,3):
\[
Z_{W(3,3)}(\beta) = 1 + 24e^{-10\beta} + 15e^{-16\beta}.
\]

The ratios are exact:
- Multiplicity ratio: \(f / (K_7\text{ degen}) = 24/6 = 4 = q+1\)
- Gap difference: \(10 - 7 = 3 = q\)
- Second multiplicity: \(g = 15 = 3 \times 5 = q \times (K_6\text{ degen})\)
