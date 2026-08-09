# PART_CCCCCXXXVIII — Local Graph = Lines of GQ(3,3) Through a Point

## Theorem

The 4 components of the local graph \(4\times K_3\) at any vertex \(v_0\) are precisely the **4 isotropic lines of GQ(3,3) passing through \(v_0\)**.

## Proof

In the generalised quadrangle \(\mathrm{GQ}(q,q)\):
- Every point lies on exactly \(q+1 = 4\) lines.
- Every line contains exactly \(q+1 = 4\) points (including the base point).
- In the collinearity graph (= W(3,3)), two distinct points are adjacent iff they lie on a common line.

The neighbors of \(v_0\) are exactly the points on the 4 lines through \(v_0\), excluding \(v_0\) itself: \((q+1)\times q = 4\times 3 = 12 = k\). ✓

Within each line \(\ell_i\), the 3 points \(\{p_1^{(i)}, p_2^{(i)}, p_3^{(i)}\}\) are mutually collinear (they lie on the same line), hence mutually adjacent, forming \(K_3\).

Points on *different* lines through \(v_0\) are **not** collinear (in a GQ, two lines meet in at most one point, so points on distinct lines through \(v_0\) share only \(v_0\), which is excluded from the local graph), hence they are non-adjacent.

Therefore \(\Gamma[N(v_0)] = 4\times K_3\). ✓

## Physical Interpretation: SM Lines as Gauge Channels

| Line \(\ell_i\) | Physical identification | Gauge symmetry |
|---|---|---|
| \(\ell_1\) | Colour triplet (u-quark) | \(\mathrm{SU}(3)_c\) fundamental |
| \(\ell_2\) | Colour triplet (d-quark) | \(\mathrm{SU}(3)_c\) conjugate |
| \(\ell_3\) | Weak isospin doublet + singlet | \(\mathrm{SU}(2)_L\times\mathrm{U}(1)_Y\) |
| \(\ell_4\) | Lepton sector | \(\mathrm{U}(1)_{em}\) |

All 12 interaction channels are exhausted by the 4 lines: \(4 \times 3 = 12 = k\). The SM gauge group structure is encoded in the local geometry of W(3,3) with no free parameters.

## Algebraic Confirmation

\(\mathrm{PSp}(4,3)\) has exactly 4 maximal parabolic subgroups (stabilisers of isotropic lines). Their order is:
\[
|P_i| = \frac{|\mathrm{PSp}(4,3)|}{|\mathrm{orbit}|} = \frac{25920}{12} = 2160.
\]
Note \(2160 = |\mathrm{Aut}(A_6)|\), linking the local symmetry of each line to the automorphism group of the alternating group \(A_6\).
