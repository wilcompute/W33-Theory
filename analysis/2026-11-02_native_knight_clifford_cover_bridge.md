# Native chiral torus, toroidal knights and a signed Clifford bridge

The user's recollection is correct. The established knight–Q4–Cl4–Pascal
connection is already explicit in
`2026-05-29_cl4_q4_hypercube_network_unification.md` and its verifier
`w33_cl4_q4_hypercube_network_unification.py`. This packet extends that work
by constructing maps to the **actual native chiral branched covering** from
`w33_20261102_chiral_surface_development.py`, and to the **actual spinor
matrices** from `w33_20261031_unitary_stabilizer_lift.py`.

The advance is these explicit maps and their compatibility, not a new claim
about binomial coefficients, knight graphs or the order of the Clifford group.
The source and certificate are
`w33_20261102_toroidal_knight_clifford_bridge.py` and
`data/w33_20261102_toroidal_knight_clifford_bridge.json`.

## Prior ownership and a useful negative control

The May report identifies all subsets of four generators with Clifford blades,
the augmented face lattice of a tetrahedron, and hypercube vertices. Its grade
row is exactly **1,4,6,4,1**. The augmentation includes the empty face and the
whole tetrahedron. The tetrahedral **boundary** used as the native covering
target instead has four vertices, six edges and four faces. Those two uses of
the tetrahedron are related constructions with different carriers.

`w33_pass5311_order4_latin_toroidal_q4_census.py` and
`w33_pass5316_latin_knight_q4_affine_derivative_census.py` already study
colorings on the fixed knight cube. The present parity coloring is not a Latin
square: rows repeat two symbols. Their Latin-square census cannot be imported
as a theorem about this covering.

The complete corrected `2026-05-29_flag_codec_toroidal_hypercube_boundary.md`
also matters. Its appended Pass5638 erratum rejects the proposed sixteen-codec
adjacency: a 6-regular graph with triangles cannot be Q4. The present maps use
the literal board edge sets, rather than identifying objects by their size.
`2026-10-08_early_torus_archaeology_five_fronts.md` likewise distinguishes the
older apartment CW torus, external four-tori and polyhedral tori. None is
identified with this 16-vertex triangulation here.

## An explicit graph switch that preserves the native cover labels

Use board coordinates `(x,y)` in Z4², with vertex index `4*x+y`. Encode each
coordinate by Gray code `g(t)=t xor (t>>1)`, with the x bits in the lower two
positions. Write the resulting four-bit mask as `v`.

* Ordinary torus grid edges have Hamming distance **one**.
* Toroidal knight edges have Hamming distance **three** in these coordinates.
* Both graphs have 16 vertices and 32 edges and are Q4; the coordinates used
  here differ from the May verifier's fixed knight-to-cube dictionary.

The explicit involution is

```
F(v) = v xor 1111 if v has odd weight; otherwise F(v)=v.
f(x,y) = (-x+2y, 2x-y) mod 4.
```

All eight even masks are fixed; the four vectors and four trivectors are
exchanged by support complementation. The verifier checks every vertex and
every graph edge. Grid and knight edges are disjoint; their union is K8,8.

The existing triangulated torus has grid edges G and diagonal edges D of step
±(1,1). The new fact connecting the native computation is

```
f(G)=K, f(D)=D,
f : (G union D, original oriented faces) ->
    (K union D, transported oriented faces).
```

This transports all 32 oriented triangular faces. Both surfaces have
`(V,E,F)=(16,48,32)`, with six faces at each vertex. Development against the
frozen **120-tick native completion table**, rather than an abstract coloring
rule, gives the same four labels:

| (x mod 2,y mod 2) | Native label |
|---|---:|
| (0,0) | 0 |
| (0,1) | 16 |
| (1,0) | 12 |
| (1,1) | 20 |

Both coordinate parities are preserved by f. Thus `pi(f(v))=pi(v)`, and every
transported face still has native positive maximal chirality. This is a
commuting diagram of explicit simplicial maps to the same native tetrahedral
boundary. It connects this knight realization to the previous **degree-eight
branched covering with sixteen simple ramification points**. Four source
vertices over each target vertex does not make the covering degree four:
each has local degree two, and every target face has eight preimages.

There are two important limits. f is an isomorphism **between two specified
triangulations**, not a deck automorphism of the fixed original triangulation.
Also, combining both face sets gives four triangles on each diagonal edge;
their union is not another closed surface triangulation.

In the chosen Gray coordinates the grade counts in the four native fibers are:

| Label | Scalar | Vectors | Bivectors | Trivectors | Pseudoscalar |
|---|---:|---:|---:|---:|---:|
| 0 | 1 | 0 | 2 | 0 | 1 |
| 12 | 0 | 2 | 0 | 2 | 0 |
| 16 | 0 | 2 | 0 | 2 | 0 |
| 20 | 0 | 0 | 4 | 0 | 0 |

These are coordinate-dependent identifications, not an intrinsic assignment of
Clifford grades to physical native projectors.

## The signed algebra lift is more informative than the Pascal row

Take the first four Hermitian anticommuting gamma axes in the existing
spinor certificate, with `e_i²=1`. All sixteen products `e_S` form an
orthogonal basis of Mat4(C), with Hilbert–Schmidt Gram matrix `4 I16`.
Let `P=e1 e2 e3 e4`. Then `P²=1`, and

```
U = (I+iP)/sqrt(2),
U e_i U† = i P e_i.
```

On even blades conjugation is the identity. On odd blades it is multiplication
by `iP`, so its unsigned mask action is exactly F. All **256 blade products**
are checked independently for multiplicative compatibility, including phases.

The phase is essential: `(P e_i)²=-1`, whereas `e_i²=+1`. A bare real
Euclidean vector-to-trivector support swap does not preserve generator squares.
The complex phase repairs that. The binomial row itself does not choose any
real Clifford signature, let alone derive a Lorentzian metric.

The three orders are different:

```
unsigned mask F: order 2
signed adjoint action: order 4, square = grade involution
unitary U: order 8, U²=iP, U⁴=-I
```

## The same gate enlarges the actual restricted spinor symmetry

The old **linear** spinor group has order1920 and **projective** order960.
Using those exact six old generators, the verifier computes their action on
the sixteen blades with integer phase exponents, then closes the group after
adding U. It finds

```
old projective action: 960
old unsigned Pauli action: 60
new projective action: 11520
new unsigned Pauli action: 720
projective Pauli kernel: 16
```

Independent Schreier–Sims tests use permutations of the 32 signed Hermitian
Pauli axes and reproduce both projective group orders. Since the blades span
Mat4(C), an adjoint action is faithful modulo scalar matrices. This proves
the result projectively; the full enlarged linear matrix group is not
enumerated here.

There are exactly six five-element pairwise anticommuting subsets of the
fifteen nonidentity Pauli axes: the ovoids of W(3,2). The original five gamma
axes form one ovoid. The old group fixes it, and U acts as one transposition
on the six ovoids. The enlarged unsigned group acts faithfully as S6.
The full projective stabilizer of an ovoid has order1920; the old projective
group is an index-two subgroup of it. This projective1920 must not be confused
with the old **linear1920**, which projects to960.

The well-known ambient groups and their classification are external prior
mathematics: [Kubischta and Teixeira, Classification of the Subgroups of the
Two-Qubit Clifford Group](https://arxiv.org/html/2409.14624v1). The paper
distinguishes projective orders from scalar-center factors and lists multiple
inequivalent subgroups of the same order. We identify our result by its
explicit generators and action, not order alone. The relation of the two-qubit
Pauli geometry to S6 is also prior work: [Planat, Clifford quantum computer
and the Mathieu groups](https://arxiv.org/abs/0711.1733).

Finally `Uᵀ Omega U != Omega` for the actual symplectic form preserved by the
old group. Thus this gate adds a specific operation outside that restricted
USp4 realization. It cannot simply be assumed to act on the old27-dimensional
signed module or preserve its common-cover interaction tensors. Extending
that module requires another compatible map, not just this group enlargement.

## Scope and reproducibility

Run the producer above, then
`py -3 -m pytest -q tests/test_w33_20261102_toroidal_knight_clifford_bridge.py`.
The seven tests check the literal knight rule and spectrum, every native
face/link, the failure of the deck/union-surface interpretations, all256
Clifford products, exact matrix identities, independent group orders and the
complete ovoid/grade-fiber census. The validation artifact records the actual
producer/test commands and outcomes, including the connected14 prior tests.

This establishes a finite graph, surface-cover and operator-algebra bridge.
It does not supply a spacetime metric, topology-selection dynamics, physical
fermion identification, a non-Clifford computational resource or a complete TOE.

Five independent investigations: extension of the signed27 module; chiral
Hamiltonians under surface transport; physical cost of U; real-signature
representations; maps from the corrected Q4-plaquette flag construction.
