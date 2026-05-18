# W(3,3) Exact CSS-Code Audit

## Executive result

The canonical CSS code determined directly by the W(3,3) line-triangle chain complex is not a vertex code on 40 qutrits.  It is an **edge-carrier CSS code** on the 240 W(3,3) edges:

\[
H_X=d_1:C_1\to C_0,\qquad H_Z=d_2^T:C_1\to C_2.
\]

Over \(\mathbb F_3\), using the 160 triangles contained in the 40 isotropic projective lines:

```text
n       = 240 edge qutrits
rank HX = 39
rank HZ = 120
k       = 240 - 39 - 120 = 81
d_Z     = 4
d_X     = 3
```

So the exact canonical chain-complex code is

\[
\boxed{[[240,81,3]]_3}\quad \text{with asymmetric distances}\quad d_X=3,\ d_Z=4.
\]

This is a very strong result for the theory: the protected \(81\)-sector is exactly the logical qutrit count of the natural W(3,3) edge-carrier code.

## Distance witnesses

The code audit supplies explicit minimal logical witnesses.

### Z-distance witness, weight 4

A non-boundary 4-cycle using edge supports:

```text
(0,1), (0,13), (1,4), (4,13)
```

with coefficients:

```text
edge_index 0:  (0,1)   coeff 1
edge_index 3:  (0,13)  coeff 2
edge_index 14: (1,4)   coeff 1
edge_index 44: (4,13)  coeff 1
```

This proves \(d_Z\le 4\), while exhaustive support search through weight 3 shows no lower non-boundary Z logical.

### X-distance witness, weight 3

A non-exact triangle-star cocycle using edge supports:

```text
(0,1), (0,2), (0,3)
```

with all coefficients equal to 1.  This proves \(d_X\le 3\), while exhaustive support search through weight 2 shows no lower non-exact X logical.

## Important correction to the recent claim

The recent statement

\[
W(3,3) \text{ is a } [[40,12,13]]_3 \text{ CSS code}
\]

is not implied by the canonical W(3,3) incidence data.  It may still exist as a separate derived construction, but it needs explicit stabilizer matrices \(H_X,H_Z\), a proof that \(H_XH_Z^T=0\), and a distance-13 computation.

The raw 40-vertex point-line incidence matrix has rank 25 over \(\mathbb F_3\), and its Gram matrix is not zero.  Therefore it is not by itself a symmetric commuting CSS stabilizer on the 40 vertex qutrits.

## Interpretation for the TOE architecture

The clean replacement is stronger and more natural:

\[
\boxed{240 = 39 + 120 + 81.}
\]

- \(39\): exact-gradient / gauge modes from \(\operatorname{im}(d_1^T)\)
- \(120\): triangle-boundary / curvature modes from \(\operatorname{im}(d_2)\)
- \(81\): harmonic protected logical sector \(H_1\)

This turns the 240-edge / 81-homology story into a precise stabilizer-code theorem.  The TQC substrate should therefore be formulated first as an edge-qutrit code, with vertex-particle dictionaries emerging as readout/anchor projections rather than as the primary code block.
