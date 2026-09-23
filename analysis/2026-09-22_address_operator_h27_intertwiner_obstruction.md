# Address/operator H27 linear-intertwiner obstruction

## Result

The current frontier leaves an explicit frozen-root-gauge change of basis between the regular **address** H27 and the center-correct trinification **operator** H27 open.  The two actions can now be separated more sharply: an **H27-equivariant invertible change of basis does not exist**.

For the extraspecial Heisenberg group of order 27 and exponent 3, the complex irreducibles are nine one-dimensional characters plus two three-dimensional Schroedinger representations with the two nontrivial central characters.  Hence the 27-dimensional regular/address module decomposes as

\[
\mathbb C[H_{27}]
\cong
\bigoplus_{\chi\in\widehat{H_{27}/Z}}\chi
\oplus 3V_\omega\oplus3V_{\omega^2}.
\]

The landed trinification action on the E6 minuscule 27 is

\[
27\downarrow H_{27}^{\rm op}=9V_\omega.
\]

Therefore

\[
\dim\operatorname{Hom}_{H_{27}}
(\mathbb C[H_{27}],9V_\omega)
=3\cdot9=27,
\]

but the largest possible image contains only the three source copies of the shared irrep:

\[
\boxed{\operatorname{rank}T\le 3\cdot3=9}
\qquad
(T\text{ H27-equivariant}).
\]

The bound is sharp, but it is far below 27.  Thus no invertible H27 intertwiner exists.

## One-line central proof

The center generator acts on the regular address basis as nine 3-cycles.  Its eigenvalue multiplicities are therefore

\[
1^9,\quad\omega^9,\quad(\omega^2)^9.
\]

On the operator 27 the same abstract central generator is scalar:

\[
\omega I_{27}.
\]

If \(TR_z=\omega T\), then \(T\) kills the 18-dimensional source sum of the \(1\)- and \(\omega^2\)-eigenspaces, immediately forcing \(\operatorname{rank}T\le9\).

Twisting either action by an automorphism of H27 cannot fix the obstruction: the center is characteristic and its nonidentity generator can only be exchanged with its inverse.  The regular central spectrum remains \(9+9+9\), whereas the operator center remains scalar.

## Consequence for the TOE frontier

This upgrades the previous fixed-point/permutation non-identification.  The missing root-gauge map cannot be sought as a basis conjugacy that identifies the two landed H27 actions.  A viable address-to-operator compiler must instead do one of three explicit things:

1. use a non-equivariant coordinate dictionary and record the broken symmetry;
2. retarget the address H27 to a different representation/subgroup before comparison; or
3. enlarge the carrier so the missing operator multiplicity can be supplied.

That sharply narrows the next search.  In particular, the 1920 anchored GQ(2,4) incidence gauges cannot hide an equivariant solution: this obstruction is representation-theoretic and survives every coordinate relabeling.

## Scope

This is an exact finite representation theorem.  It does **not** obstruct the existence of an ordinary bijection between the two 27-label sets, and it does not decide whether the non-FI powers of the Qpsi clock normalize the two-qutrit execution algebra.  That normalizer question must now be attacked in the explicit trinification/operator basis rather than via an impossible regular-H27 conjugacy.

External context: this is the finite-Heisenberg/Stone--von Neumann distinction between the regular representation and the irreducible Schroedinger central-character sector; no novelty claim is made for that general representation theory.  The increment is its application to the two independently certified H27 roles in this repository.
