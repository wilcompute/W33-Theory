# Passes 5824–5831 — the common `W_9` has three distinct integral forms

## Executive result

Passes 5776–5823 identified a single absolutely irreducible rational module `W_9` inside the q=5 point, heavy and Reye-line carriers.  This packet asks the stricter question: are the three copies also the same over `Z` or `F_2`?

They are not.

The exact saturated lattices are

\[
\boxed{L_P=L_H\cong A_3^3},
\qquad
\boxed{L_L\cong A_3\otimes A_3}.
\]

Their discriminants are

\[
\boxed{\det L_P=\det L_H=2^6},
\qquad
\boxed{\det L_L=2^{12}}.
\]

So rational representation equivalence does not lift to integral equivalence.  The mismatch is entirely 2-primary and is measured exactly by the Smith forms of the three Radon maps.

## Pass 5824 — point/heavy are `A_3^3`, line is `A_3\otimes A_3`

The point carrier has three four-element fibres.  Inside each fibre the integral mean-zero lattice is

\[
A_3=\{(z_0,z_1,z_2,z_3)\in\mathbb Z^4:\sum z_i=0\}.
\]

The common rational nine-space on points is the direct sum of the three fibre mean-zero spaces, hence its saturation is

\[
\boxed{L_P\cong A_3^3}.
\]

The heavy carrier has the same three-by-four fibre structure, so

\[
\boxed{L_H\cong A_3^3}.
\]

Using the standard basis `e_i-e_3`, the `A_3` Gram matrix is

\[
G_{A_3}=\begin{pmatrix}2&1&1\\1&2&1\\1&1&2\end{pmatrix},
\qquad\det G_{A_3}=4.
\]

Therefore

\[
\det(A_3^3)=4^3=64=2^6.
\]

The line lattice is subtler.  An explicit `GL_4(2)` dual-label map

\[
L=\begin{pmatrix}
0&1&1&0\\
1&0&1&1\\
0&1&1&1\\
1&0&0&1
\end{pmatrix}
\]

sends the nine rank-one Fourier labels to the nine labels `(\alpha,\beta)` with both two-bit coordinates nonzero.  The corresponding primal coordinate map `C=L^{-T}` is

\[
C=\begin{pmatrix}
1&1&0&1\\
0&1&1&0\\
1&0&0&1\\
1&1&1&0
\end{pmatrix}.
\]

After this integral coordinate permutation, the line `W_9` is exactly the lattice of `4 x 4` integer arrays with every row sum and every column sum zero.  Its basis is

\[
(e_i-e_3)\otimes(e_j-e_3),\qquad0\le i,j<3,
\]

so

\[
\boxed{L_L\cong A_3\otimes A_3}.
\]

Its Gram matrix is `G_A3 tensor G_A3`, hence

\[
\det L_L=4^3\,4^3=4^6=4096=2^{12}.
\]

The discriminant-group Smith forms are

\[
\boxed{L_P^*/L_P\cong L_H^*/L_H\cong(\mathbb Z/4)^3},
\]

and

\[
\boxed{L_L^*/L_L\cong(\mathbb Z/4)^4\oplus\mathbb Z/16}.
\]

## Pass 5825 — the line identification is constructive, not discriminant matching

The `GL_4(2)` map above is not inferred from equal determinants.  It is checked directly on all nine rank-one dual matrices: the determinant-zero nonzero locus is sent to the product-nonzero `3 x 3` Fourier block.

The associated permutation of the sixteen line coordinates is integral and orthogonal.  Every transformed rank-one Walsh vector has all row sums and column sums zero, and the nine transformed vectors span the full nine-dimensional row/column-zero rational subspace.  The displayed tensor basis is a saturated basis of its integer points.

Thus `L_L=A_3\otimes A_3` is an explicit lattice isometry statement.

## Pass 5826 — Walsh bases are not saturated

The nine point and heavy Walsh vectors each span an index-64 sublattice of their `A_3^3` saturation.  Their column Smith form is

\[
\boxed{1^3\,2^6},
\]

so

\[
\boxed{[L_P:W_P]=[L_H:W_H]=2^6}.
\]

The nine rank-one line Walsh vectors have Smith form

\[
\boxed{1\,2^4\,4^4},
\]

hence

\[
\boxed{[L_L:W_L]=2^{12}}.
\]

This is why the orthogonal Walsh basis, while ideal over `Q`, hides substantial binary saturation data.

## Pass 5827 — saturated Radon maps have exact 2-primary cokernels

Write the point–line, point–heavy and heavy–line transforms on the saturated bases.  The exact Smith forms are

\[
\boxed{
\operatorname{SNF}(R^T|_{W_9})
=\operatorname{SNF}(D|_{W_9})
=1^5\,2^2\,4^2,
}
\]

and

\[
\boxed{
\operatorname{SNF}(H^T|_{W_9})
=1^2\,2^5\,4^2.
}
\]

Therefore

\[
\boxed{
\operatorname{coker}(R^T|_{W_9})
\cong\operatorname{coker}(D|_{W_9})
\cong(\mathbb Z/2)^2\oplus(\mathbb Z/4)^2,
}
\]

of order `2^6`, while

\[
\boxed{
\operatorname{coker}(H^T|_{W_9})
\cong(\mathbb Z/2)^5\oplus(\mathbb Z/4)^2,
}
\]

of order `2^9`.

Thus the rational Radon equivalence is glued integrally by explicit powers of two.

## Pass 5828 — ambient Smith forms

The full incidence maps have

\[
\boxed{\operatorname{SNF}(R)=\operatorname{SNF}(D)=1^8\,2^2},
\]

\[
\boxed{\operatorname{SNF}(H)=1^4\,2^6}.
\]

For the rank-nine projector numerator and centered cross maps,

\[
\boxed{\operatorname{SNF}(K_9)=1^3\,4^6},
\]

\[
\boxed{\operatorname{SNF}(B)=\operatorname{SNF}(C_R)=1\,4^6\,8^2},
\]

and

\[
\boxed{\operatorname{SNF}(C_H)=1\,2^4\,4^4}.
\]

These exact forms are useful certificates for any later binary/code interpretation.

## Pass 5829 — characteristic-two firewall

The corresponding `F_2` ranks are

\[
\boxed{\operatorname{rank}_2R=\operatorname{rank}_2D=8},
\qquad
\boxed{\operatorname{rank}_2H=4},
\]

\[
\boxed{\operatorname{rank}_2K_9=3},
\]

and

\[
\boxed{\operatorname{rank}_2B
=\operatorname{rank}_2C_R
=\operatorname{rank}_2C_H=1}.
\]

This sharply contrasts with the common rational dimension nine.  In the intrinsic `3K_4` block coordinates, the reason for `rank_2 K_9=3` is visible immediately:

\[
K_9=I_3\otimes(4I_4-J_4)
\equiv I_3\otimes J_4\pmod2,
\]

one rank-one block per fibre.

## Pass 5830 — corrected coefficient-ring hierarchy

The safe hierarchy is now:

\[
\boxed{
\text{over }\mathbb Q:
P,H,L\text{ share one absolutely irreducible }W_9;
}
\]

\[
\boxed{
\text{over }\mathbb Z:
L_P=L_H\cong A_3^3,
\quad L_L\cong A_3\otimes A_3;
}
\]

\[
\boxed{
\text{over }\mathbb F_2:
\text{the incidence ranks split }8,4,8
\text{ and the centered maps collapse further.}
}
\]

Any future code/CSS statement that uses the common-nine theorem must specify its coefficient ring.

## Boundary

This is exact integral lattice arithmetic and finite incidence theory.  It is a correction-strengthening result: rational carrier equivalence must not be promoted to integral or binary equivalence.  No physical significance is assigned to the powers of two without an independent operational map.
