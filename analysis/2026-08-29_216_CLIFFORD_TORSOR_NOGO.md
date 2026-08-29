# The 216 sentinel circuits are not an internal qutrit-Clifford torsor

Date: 2026-08-29

**Status: PASS.** Executable:
`analysis/w33_20260829_216_clifford_torsor_nogo.py`.
Certificate:
`data/PART_W33_20260829_216_CLIFFORD_TORSOR_NOGO.json`.

The sentinel-shell theorem produces a transitive 216-element set

`C5 = {five-element binary circuits among the 45 sentinel minima}`

with stabilizer `S5`, hence

`C5 = PSp(4,3)/S5`.

The project independently contains the projective single-qutrit Clifford group
of order 216. The cardinalities are therefore identical, but cardinality is not
a group-action theorem. This packet tests the strongest natural version of the
proposed identification and rules it out.

## 1. There are only two internal order-216 subgroup classes

Connor and Leemans' complete subgroup lattice of `PSp(4,3)` lists exactly two
conjugacy classes of subgroups of order 216:

1. class 10, `3^(1+2):Q8`, with 40 conjugates;
2. class 11, the second order-216 class, with 120 conjugates.

The executable constructs representatives of both classes directly in the
repository's native W33 permutation coordinates.

### Point-side class

Fix a W33 point. Its stabilizer has order 648. The derived subgroup has order
216. Exact normalizer computation gives

`|N_G(H_point)| = 648`,

so the class length is `25920/648 = 40`, matching Connor-Leemans class 10.

On the 216 five-circuits its orbit partition is

`108 + 36 + 36 + 36`.

It is not transitive.

### Line-pair class

Fix a W33 line and one of the three perfect matchings of its four points. The
setwise stabilizer of that matching has order 216. Exact normalizer computation
gives

`|N_G(H_pair)| = 216`,

so its conjugacy class has length `25920/216 = 120`, matching the second
published order-216 class.

Its orbit partition on the 216 circuits is

`108 + 36 + 27 + 27 + 18`.

It is also not transitive.

Since the subgroup lattice has no third order-216 class,

**no subgroup of order 216 inside `PSp(4,3)` acts regularly—or even
transitively—on the 216 sentinel circuits.**

## 2. The actual qutrit Clifford 216 is a quotient, and the quotient does not descend

The point stabilizer has structure of order 648 with a central `C3`. The
project's already-certified projective single-qutrit Clifford group is the
quotient

`point stabilizer / C3`,

of order 216, i.e. the Hessian/affine-special-linear group
`ASL(2,3) = C3^2 : SL(2,3)`.

For this quotient to inherit the point-stabilizer action on `C5`, the central
`C3` would have to lie in the kernel of the circuit action.

It does not.

The executable reconstructs the center exactly. Each of its two nonidentity
elements acts on the 216 circuits as

`72 disjoint 3-cycles`,

with zero fixed circuits. Therefore the central `C3` is maximally visible on
this orbit rather than invisible, and the quotient action cannot descend.

This is the sharp obstruction:

`648-point-stabilizer action on C5`

cannot be projected to

`216-qutrit-Clifford action on C5`.

## 3. The correct conclusion

The recurring 216s now have a precise relationship and a precise boundary:

- the sentinel dependency shell is a 216-point homogeneous space
  `PSp(4,3)/S5`;
- the projective qutrit Clifford is a 216-element quotient of an order-648
  point stabilizer;
- no internal order-216 subgroup is transitive on the circuit homogeneous
  space;
- the central `C3` obstruction prevents the natural quotient action from
  descending.

So the equality `216 = 216` is **not** the missing Clifford identification.
Any real bridge must introduce additional structure: a different action, a
cover/quotient correspondence, a cocycle or central-extension construction,
or an explicitly non-`PSp(4,3)`-equivariant map.

## 4. External cross-check

The subgroup-class exhaustion is cross-checked against:

- Thomas Connor and Dimitri Leemans, *The Subgroup Lattice of PSp4(3)*,
  whose table lists exactly the two order-216 subgroup classes with lengths 40
  and 120;
- the standard Hessian-group identification
  `ASL(2,3)=C3^2:SL(2,3)` of order 216.

The orbit decompositions, normalizer orders, central action and quotient
obstruction are carried by the executable certificate in the native repo
coordinates.
