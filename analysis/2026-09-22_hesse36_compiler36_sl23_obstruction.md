# The two 36-state Hesse carriers separate exactly on both qutrit order-three classes

The preceding maximal-common-symmetry theorem produced a new 36-object carrier:
the maximal compiler-safe \(C_3^2\) subgroups of
\[
K=H_{27}^{\rm address}\times C_3^{\rm external}.
\]
The repository already has another exact 36-object Hesse carrier: the ordinary
non-fiber Payne/Hesse lines, \(36=12\times3\). A count match is not enough, so
this audit compares the two as permutation representations of the exact common
physical complement.

## The common group is the physical \(SL(2,3)\)

The fixed-center automorphism group of \(H_{27}\) has order 216. In the fixed
physical Clifford gauge, exactly 24 of those automorphisms preserve the five
selected GQ directions through the identity: the center plus the four
noncentral directions
\[
\langle\omega X\rangle,\quad
\langle\omega Z\rangle,\quad
\langle ZX\rangle,\quad
\langle\omega^2ZX^2\rangle.
\]
This order-24 subgroup is the split \(SL(2,3)\) complement used by the physical
Clifford-648 dictionary.

Both 36-object carriers are invariant under this same group.

## Orbit decompositions already disagree

For the ordinary Payne/Hesse 36,
\[
\boxed{36=24+4+4+4.}
\]
For the compiler-safe 36,
\[
\boxed{36=8+8+8+4+4+4.}
\]
Therefore there cannot be an equivariant objectwise bijection.

The stronger permutation-character audit localizes the mismatch much more
precisely.

## Character fingerprint

The common \(SL(2,3)\) elements have order profile
\[
1^1,\quad2^1,\quad3^8,\quad4^6,\quad6^8.
\]
The two permutation characters have the following fixed-point counts:

| element order | element count | ordinary Hesse 36 | compiler-safe 36 |
|---:|---:|---:|---:|
| 1 | 1 | 36 | 36 |
| 2 | 1 | 12 | 12 |
| 3 | 8 | 3 | 9 |
| 4 | 6 | 0 | 0 |
| 6 | 8 | 3 | 3 |

The order profile aggregates conjugacy classes.  Exact conjugation inside the
24-element group gives seven classes, of sizes `1,1,4,4,6,4,4` at orders
`1,2,3,3,4,6,6`.  Thus the eight order-three elements form two classes of
four.  Both order-three classes have the same fixed-point mismatch `3` versus
`9`; the characters agree on all five other classes.

\[
\boxed{\chi_{\rm ordinary}-\chi_{\rm safe}
\text{ is supported only on the two qutrit order-3 shear classes}.}
\]

This is the useful part of the no-go. The two Hesse lifts are not globally
different. Their obstruction is concentrated in the genuinely ternary
unipotent/transvection sector.

## Consequence for the compiler

The naive identification
\[
36_{\rm ordinary\ tritangents}
\stackrel{?}{\longleftrightarrow}
36_{\rm maximal\ safe\ planes}
\]
is false as a physical \(SL(2,3)\)-set, even though both admit a
\(12\times3\) Hesse organization.

That redirects the next construction. A viable relation between the two
36-dimensional permutation modules must change only the order-three sector:
for example a Fourier/induced transform, quotient/extension, or other
non-objectwise intertwining mechanism. Rebuilding the order-2, order-4, or
order-6 sectors would be unnecessary because their permutation characters
already agree.

## Ownership / scope

The ordinary 36 and its phase-decorated Hesse interpretation are prior
repository results in docs/PAYNE_HESSE_PACKET_DICTIONARY.md. The compiler-safe
36 is the new maximal-common-symmetry carrier. This note proves only the
common-\(SL(2,3)\) non-equivalence and pinpoints its two-class order-three defect. It does
not exclude equivalence after restricting to a smaller subgroup, nor a
non-objectwise linear transform between their permutation modules.
