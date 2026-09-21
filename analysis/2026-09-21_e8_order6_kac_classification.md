# E8 order-six Kac classification of the two physicalized Z6 actions

## Result

The repository contains two independently certified inner order-six actions on the E8 adjoint:

- the FI x matter-parity structural quotient, with eigendimensions
  `(54,48,33,32,33,48)`;
- the flagship physical/holonomy action, with eigendimensions
  `(44,40,38,48,38,40)`.

Kac/Cartan torsion theory classifies inner finite-order automorphisms by
nonnegative relatively-prime affine Kac coordinates `(s0,...,s8)` satisfying

[
sum_{i=0}^8 a_i s_i=m,
]

where `(a0,...,a8)` are the affine highest-root marks.  In the W33 repository's
frozen simple-root ordering,

[
(a_0,ldots,a_8)=(1,4,6,5,4,3,2,2,3).
]

For exact order six there are only **20** normalized Kac diagrams.  Exhausting
all 20 against the full 240-root E8 shell gives one and only one diagram for
each repository action:

[
oxed{s_{m FI	imes P_M}=(2,0,0,0,1,0,0,0,0)}
]

and

[
oxed{s_{m hol}=(0,0,0,0,1,0,0,1,0)}.
]

Thus the previous statement “same order, same D8 cube, different Z6” is now a
standard conjugacy-class theorem.

## Power ladders

For the FI x matter-parity class,

[
g: D_5+A_2+mathfrak u_1,qquad
g^2: E_6+A_2,qquad
g^3: D_8.
]

The corresponding fixed Lie dimensions are

[
54,qquad86,qquad120.
]

For the flagship holonomy class,

[
h: D_4+A_3+mathfrak u_1,qquad
h^2: D_7+mathfrak u_1,qquad
h^3: D_8,
]

with fixed dimensions

[
44,qquad92,qquad120.
]

So the two classes share their involution cube but separate already at the
square.  In Kac coordinates the distinction is particularly small and exact:
both use the same mark-4 finite node; the remaining Kac weight two sits on the
**affine node** for the FI x parity class and on a **finite mark-2 node** for
the holonomy class.

## External classification anchor

The classification used here is standard.  Mark Reeder,
*Torsion automorphisms of simple Lie algebras*, L'Enseignement Mathématique
56 (2010), 3--47, reviews the Cartan/Kac description: torsion classes are
represented by affine Kac coordinates satisfying the weighted-order equation,
the coordinates determine the root-space eigenvalues, and the zero-labelled
subgraph is the Dynkin diagram of the fixed reductive subalgebra.

## Evidence

- `analysis/w33_e8_order6_kac_classification.py`
- `data/w33_e8_order6_kac_classification.json`
- `tests/test_w33_e8_order6_kac_classification.py`

## Scope firewall

This classifies the two **complex E8 inner automorphism conjugacy classes**.
It does not prove that the heterotic vacuum preserves matter parity; Holotrade
correctly keeps that class-wide D/F-flatness theorem blocked until the raw
88-model rational charge ledgers are committed.  Nor does the classification
by itself identify either order-six action with a spacetime orbifold twist
beyond the separately certified physical inputs.
