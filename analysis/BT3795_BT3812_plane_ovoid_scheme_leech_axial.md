# Passes 3795–3812 — plane-ovoid dictionary, complete ovoid scheme, rootless Leech polarization, finite descent, and intrinsic axial classification

## Status

The exact source returns

```text
PASS_3795_3812 be5ee56a84141a7bbc896b4cef0e8eda32167a00749dbb17f10d24d0505bdd41
```

All fifteen promoted checks pass.  The packet executes the five queued fronts and three independent constructions.  Concrete Monster/mmgroup words, Monster class fusion, Griess/VOA identification, remote CI/PDF success, and physical claims remain fail-closed.

## 1. Canonical W33–plane-ovoid dictionary

The previous packet established that the graph on the forty plane ovoids of `GQ(4,2)`, with adjacency defined by three shared quadrangle lines, is isomorphic to `W(3,3)`.  The present packet replaces that existential isomorphism by a frozen objectwise dictionary.

There are exactly `51,840` graph isomorphisms, forming the full `O_6^-(2)=U_4(2):2` torsor.  Lexicographic minimization over that torsor gives the canonical map

```text
[0,1,8,9,3,4,7,36,21,31,34,18,27,2,28,26,5,38,35,6,
 23,19,16,37,15,11,25,20,30,12,32,17,10,39,13,22,24,29,33,14]
```

with digest

```text
2bae92fbba3d66f58f9931a42972987359303cb796993e537267f0516abd3800
```

The verifier regenerates all forty projective lines of `W(3,3)`, each containing four points, and proves that their images are exactly the forty maximal `K4` line cliques of the plane-ovoid graph.  Exact-cover enumeration then regenerates all thirty-six spreads, each containing ten lines.  The dictionary therefore transports the complete point-line-spread geometry, not only adjacency.

## 2. Complete coherent configuration on all 200 ovoids

The full `O_6^-(2)` action on the `40+160` plane-ovoid/tripod split has exactly nineteen ordered-pair orbitals.  Their sizes are

```text
160, 480, 480, 4320, 4320, 12960, 4320, 160, 1440, 1440,
480, 1440, 480, 40, 480, 4320, 1080, 160, 1440.
```

They sum to `200^2=40,000`.  Every orbital records its source fiber, target fiber, transpose relation, valency, and ovoid-intersection size.  The complete intersection tensor has shape `19×19×19`, 405 nonzero entries, maximum entry 108, and digest

```text
58ea7adb73798c435d665b25fc7637c52544e4e87412af078e222fe4e57f039f
```

The orbital matrices are linearly independent, so the adjacency algebra has dimension nineteen.  Its center has dimension five modulo `1,000,003`.  Characteristic-zero Wedderburn identification is left for a later packet; the present result is the complete executable coherent configuration and multiplication tensor.

## 3. Rootless Leech polarization with exact surviving symmetry

The construction begins from the standard degree-24 ATLAS generators of `M24`:

- an involution of cycle shape `2^12`;
- an element of order three with six 3-cycles;
- product order twenty-three;
- base octad `{1,2,3,4,5,11,17,24}`.

The base-octad orbit contains exactly 759 octads.  Their binary span is a `[24,12,8]` code with weight distribution

```text
0^1, 8^759, 12^2576, 16^759, 24^1.
```

The integral coordinate construction produces a numerator basis of determinant

```text
2^36 = 68,719,476,736.
```

After division by eight, its Gram matrix is integral, positive definite, even, and has determinant one.  An exact rational LDL/Fincke–Pohst recursion visits 59,869 nodes and finds only the zero vector at norm at most two.  A basis vector has norm four.  Hence the minimum norm is exactly four.  By the standard uniqueness theorem for even unimodular rootless rank-24 lattices, this is the Leech lattice.

An explicit word in the ATLAS generators produces an order-eight element whose fourth power has cycle shape `1^8 2^8`.  A frozen determinant-one integral transport intertwines that involution with the trace-eight involution in the rank-24 axial carrier.  The transported axial Gram has digest

```text
e33fb427b918fbb792e886298e4cd2250dbd4b66c0abd732153d7f0266f5648a
```

Every one of the `25,920` elements of the axial `U_4(2)` action is tested against this Gram matrix.  Exactly two preserve it: the identity and the distinguished involution.  Therefore

```text
Stab_U4(2)(Lambda_axial) = C2.
```

This is an exact maximality statement inside the complete axial `U_4(2)` action.  It is not a claim about the full Conway stabilizer or a Monster embedding.

## 4. Explicit abstract finite-group descent

Seven exact degree-45 permutations generate

```text
O_6^-(2)=U_4(2):2,  order 51,840,
```

with index-two subgroup

```text
U_4(2),  order 25,920.
```

The full element-order census is

```text
1^1, 2^891, 3^800, 4^5940, 5^5184,
6^12960, 8^6480, 9^5760, 10^5184, 12^8640.
```

The seven-generator digest is

```text
d2c6f225821b2a197e00f01e9b1b7a951a9be77695cba4b5f476395702f0f6f4
```

The action simultaneously carries the fingerprint

```text
45 GQ points, 27 GQ lines, 120 Norton lines, 135 D4 frames,
40 plane ovoids, 160 tripods, and 19 coherent orbitals.
```

This completes the abstract finite descent.  No serialized `mmgroup` elements or executed Monster class fusion are present, so the Monster front remains fail-closed.

## 5. Intrinsic classification of the 45-axis algebra

The algebra has dimension twenty-four and forty-five idempotent axes.  The twenty-seven `GQ(4,2)` line relations

```text
sum_{i in L} a_i = 0
```

have rank twenty-one.  The forty-five axes have rank twenty-four, so their full linear-relation kernel also has dimension twenty-one.  Consequently the line sums generate every linear dependency among the axes.

The pair laws from the previous packet give the complete two-axis classification:

```text
collinear pair      -> generated dimension 2,
noncollinear pair   -> generated dimension 4.
```

The `U_4(2):2` action has six orbits on unordered triples:

| Orbit size | Induced edges | Generated dimension |
|---:|---:|---:|
| 240 | 0 | 4 |
| 2160 | 0 | 10 |
| 2880 | 0 | 24 |
| 6480 | 1 | 10 |
| 2160 | 2 | 5 |
| 270 | 3 | 3 |

A modular linear-system test shows that no identity element exists.  Together with the previously certified full multiplication-operator algebra and zero derivations, the intrinsic verdict is:

- simple;
- positive Frobenius;
- nonunital;
- derivation algebra zero;
- generated by the forty-five axes with precisely the twenty-seven line relations and the two orbitwise pair laws.

## Bonkers construction A — two tripod fibrations reconstruct all W33 flags

Two self-paired valency-three relations on the 160 tripods each decompose into forty disjoint `K4` components.  Let the two block systems be `P` and `Q`.  Their `40×40` intersection matrix `B` is binary, has exactly 160 ones, and every row and column has weight four.

Moreover,

```text
B B^T = 4 I + A_W33.
```

The matrix has rank twenty-five over both the rationals and `F_1000003`.  Each tripod is the unique nonempty intersection of one block from `P` and one block from `Q`.  Thus the tripods are exactly the 160 flags between two dual forty-object block systems, and either Gram graph reconstructs `W(3,3)` with parameters `(40,12,2,4)`.

## Bonkers construction B — a rootless axial Leech bridge

The determinant-one transport does more than prove existence of a rootless polarization.  It places a concrete Leech Gram directly on the same rank-24 carrier supporting the new axial multiplication.  The exact intersection of the axial `U_4(2)` symmetry with the Leech isometry group is `C2`.

This supplies a rigorous bridge

```text
GQ(4,2) axial carrier  --integral determinant-one transport-->  Leech lattice,
```

while sharply measuring the symmetry cost: the full `U_4(2)` action breaks to one involution.

## Bonkers construction C — three-axis universality

Pairs generate only dimensions two or four, yet one orbit of 2,880 independent triples generates all twenty-four dimensions.  A representative is the axis triple `(0,6,33)`.  Therefore the algebra exhibits a genuine threshold:

```text
2 axes: local subalgebra only;
3 suitable axes: the complete algebra.
```

This is an exact finite generation theorem, not a heuristic claim.

## Evidence boundary

### Executed here

- canonical W33/plane-ovoid point-line-spread dictionary;
- complete nineteen-orbital coherent configuration;
- double-`K4` reconstruction of the 160 flags;
- explicit even unimodular rootless rank-24 lattice and exact `C2` stabilizer in `U_4(2)`;
- explicit abstract `O_6^-(2)` descent and element-order census;
- complete linear presentation and pair/triple axial generation census.

### Not executed here

- Monster/mmgroup words or Monster class fusion;
- Majorana, Griess, Monster, or VOA identification;
- full coherent-configuration automorphism equality beyond the exhibited action;
- remote CI or manuscript PDFs until observed;
- hardware, laboratory, or physical implementation.
