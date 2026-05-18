# Minimal Logical Witness Census for the W(3,3) Edge CSS Code

## Executive result

For the canonical edge-chain CSS code

\[
H_X=d_1:C_1\to C_0,\qquad H_Z=d_2^T:C_1\to C_2,
\]

with parameters

\[
[[240,81,3]]_3,
\qquad d_X=3,
\qquad d_Z=4,
\]

the full minimal witness census is:

| Logical type | Minimal weight | Supports | Vectors |
|---|---:|---:|---:|
| X logical | 3 | 160 | 320 |
| Z logical | 4 | 1620 | 6480 |

This gives real combinatorial mass to the \((3,4)\) CSS-genus hinge.

## X-side: weight-3 witnesses

The minimal X witnesses are exactly the line-star supports inside the 40 isotropic \(K_4\) lines.

Each isotropic line has 4 vertices.  Choosing a center vertex gives the 3 incident edges from that center to the other vertices.  Thus each line has 4 line-stars, and W(3,3) has 40 lines:

\[
40\cdot4=160.
\]

This equals the number of line-triangles in the W(3,3) triangle complex.

Over \(\mathbb F_3\), each support has two scalar multiples, so

\[
2\cdot160=320.
\]

Equivalently,

\[
320=40\cdot2^3.
\]

## Z-side: weight-4 witnesses

The minimal Z witnesses are exactly the quadrangles determined by nonadjacent point pairs.

W(3,3) has

\[
\binom{40}{2}-240=540
\]

nonedges.  Each nonedge has \(\mu=4\) common neighbors.  Choosing two common neighbors gives a quadrangle.  Each quadrangle is counted twice by its two opposite nonedges, so

\[
\frac{540\binom{4}{2}}{2}
=\frac{540\cdot6}{2}
=1620.
\]

Every such support is non-boundary in the triangle complex.  Each support has two orientations and two nonzero scalar multiples, so

\[
4\cdot1620=6480.
\]

The closed forms are extremely suggestive:

\[
1620=20\cdot81=60\cdot27,
\]

and

\[
6480=240\cdot27=80\cdot81=\frac{|W(E_6)|}{8}.
\]

## Why this matters

The minimal logical population now touches every major substrate layer:

| Count | Meaning |
|---:|---|
| 160 | line-triangles / minimal X supports |
| 320 | minimal X vectors |
| 1620 | minimal Z quadrangle supports |
| 6480 | minimal Z vectors |
| 27 | \(q^q\), E6 fundamental/cubic-surface line count |
| 81 | protected \(H_1\) logical sector |
| 240 | W(3,3) edge carrier / E8-root count |
| 51840 | \(|W(E_6)|\) |

So the edge CSS code is not only parameter-compatible with the theory.  Its minimal logical error surface produces the same integer ecology as the E6/W33 bridge.

## Theorem statement

**Minimal Logical Census Theorem.** In the canonical W(3,3) edge CSS code, the weight-3 X logical witnesses are exactly the 160 line-star supports inside the 40 isotropic \(K_4\) lines, with two scalar vectors per support for 320 vectors total.  The weight-4 Z logical witnesses are exactly the 1620 quadrangle supports determined by noncollinear point pairs and pairs of their four common neighbors; all are non-boundary, and each support has four oriented/scalar vectors, giving 6480 vectors total.

## Connection to the previous hinge

The previous hinge showed

\[
d_X=3,\quad d_Z=4,
\quad d_X+d_Z=7,
\quad d_Xd_Z=12.
\]

This census adds the population layer:

\[
X_{\min}:160,320;
\qquad
Z_{\min}:1620,6480.
\]

The distance pair gives the toroidal polynomial.  The witness populations give the E6/W33 counting bridge.

## Honesty boundary

This is an exact finite CSS witness census.  It does not by itself prove a physical anyon braid representation or empirical Standard Model prediction.  It does, however, give the TQC architecture a precise finite error-surface population that any physical bridge should preserve.
