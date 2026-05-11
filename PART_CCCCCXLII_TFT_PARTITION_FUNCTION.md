# PART_CCCCCXLII — 2D TFT Partition Function and Genus-Dependence

## Setup

For a 2D Yang-Mills / topological field theory with gauge group \(G\), the partition function on a genus-\(g\) surface is:
\[
Z(g) = \sum_{R} (\dim R)^{2-2g},
\]
where the sum is over irreducible representations \(R\) of \(G\).

## W(3,3) Selection: \(G = \mathrm{PSp}(4,3)\)

The two natural surfaces have genera \(g_1 = 21\) and \(g_2 = 6\). The exponential factors are:
\[
2 - 2g_1 = -40,\qquad 2-2g_2 = -10.
\]

Critically: \(2-2g_1 = -\chi_1 = 2E - 2v\ldots\) wait: \(-\chi_1 = 40 = v\). So:
\[
2-2g_1 = \chi_1 = -v,\qquad 2-2g_2 = \chi_2 = -v/4.
\]

## The Special Representation

For the fundamental representation of \(\mathrm{SU}(3)\) (dim 3) restricted to the W(3,3) geometry:
\[
(\dim 3)^{2-2g_1} = 3^{-40} = 3^{-v},
\]
\[
(\dim 3)^{2-2g_2} = 3^{-10} = 3^{-v/4}.
\]
Both exponents are pure powers of \(q=3\). The **TFT partition function on the genus-21 surface probes the \(v\)th power of the fundamental representation dimension**, directly connecting the vertex count \(v\) to the field theory's UV-IR mixing.

## Ratio

\[
\frac{Z(g_1)}{Z(g_2)} \approx \frac{1 + 2 \cdot 3^{-40} + \ldots}{1 + 2 \cdot 3^{-10} + \ldots} \approx 1 - 2\cdot 3^{-10},
\]
to leading order. The correction \(2 \cdot 3^{-10}\) is suppressed by the Kirchhoff multiplicity \(f = 24 \to\) not directly, but by \(q^{-10} = q^{-(k-s+f\text{ correction})}\).
