# Removing the quadric's geometric vectors changes its gauge sector

The earlier candidate d84e57a8e has an explicit local A4/su5 source and a
flat SM-breaking connection, but four unwanted continuous geometric modes.
This follow-up tests a finite repair rather than ignoring those modes.
The repair removes the continuous algebra. It also introduces extra
singularities and an outer gauge monodromy, so the previous SU5-to-SM
calculation cannot be carried over.

## A concrete finite extension

Keep the cone f=z0^2+z1^2+z2^2+uv=0, the order-five generator
g:(u,v)->(zeta5*u,zeta5^-1*v), and the real involution K from
`analysis/2026-11-18_quadric_local_SU5_and_SM_Wilson.md`.
Add the holomorphic map

    h:(z,u,v)->(-z,v,u).

In the original orthogonal coordinates this is
diag(-1,-1,-1,1,-1), with determinant+1. It preserves f and the
holomorphic volume form; hgh=g^-1. Thus it kills the normal SO2
centralizer. The first three coordinates still have SO3.

Now add the tetrahedral rotation group on z: even sign changes and
cyclic coordinate permutations. Its order is12, its nonidentity element
orders are2 (three elements) and3 (eight elements), and its real
representation on R3 is irreducible. It commutes with h and g. The
holomorphic group is consequently

    tetrahedral A4 x D10, order120,

where D10 has order10. K commutes with these real orthogonal maps,
giving a full group of order240. Here tetrahedral A4 means a finite
rotation group, whereas an A4 singularity means the ADE root type;
they are different objects.

Exact skew-matrix commutator constraints give dimensions4,3,0 for
the so5 centralizers of <g>, <g,h>, and <g,h,tetrahedral>, respectively.
The Reeb direction is already odd under K. Thus the continuous geometric
algebra of the earlier construction is removed in this finite extension.
This is a statement about the inherited isometries, not a complete
interacting mass spectrum.

## The repair introduces additional gauge strata

The exact characteristic-zero fixed-space census in C5 is

| Ambient fixed dimension | Number of holomorphic elements |
|---|---:|
| 5 | 1 |
| 3 | 30 |
| 1 | 89 |

Among the30 elements fixing a3-plane,18 have order2,8 have order3 and4
have order5. Their orthogonal fixed spaces are nondegenerate, so their
quadric sections are complex surfaces with3-dimensional links. For
generic points of the respective fixed surfaces the transverse cyclic
actions give A1, A2 and A4 singularities. These are additional localized
gauge sources, not a removal of all unwanted fields. The table counts
elements, not connected strata or gauge-group factors of the final space.
Intersections require their own higher-codimension analysis.

The anti-holomorphic extension becomes less benign too. Although K alone
was free on the link, hK fixes a real slice of signature(1,4). Its section
at fixed Euclidean norm is S0 x S3 before further identifications. Thus
new real fixed loci must be included in any global completion.

The old gauge-locus C4 cannot simply be reused. The point stabilizers
already generate the entire120-element holomorphic group, checked by
exact finite closure. Since hK also has fixed points, their normal
closure in the full group contains K and hence all240 elements. The
underlying full orbit space has trivial fundamental group by the
stabilizer-quotient theorem (the original V5,2 is simply connected).
This is the underlying space's group, not its orbifold fundamental group
or a computation of every singular gauge locus's group.

## The decisive difference is the sign of the cycle monodromy

For the transverse resolution chain E1,...,E4, the holomorphic swap in h
acts as

    h: E_i -> E_(5-i).

It preserves complex curve orientations and reverses the Dynkin diagram.
This is an outer A4 action. By contrast, anti-holomorphic K reverses each
curve orientation as well:

    K: E_i -> -E_(5-i).

That minus sign made the previous K action an inner longest-Weyl action.
It is absent for h. Therefore adding h changes the gauge-algebra bundle;
one cannot declare the old global SU5 connection unchanged.

The producer verifies both maps on all four simple roots. With J the
5x5 reversal matrix, the canonical outer Lie automorphism is

    theta(X)=-J X^T J,   X in sl5.

Its fixed algebra has dimension10 and is so5, with rank2. This is a
control for the canonical projection, not the complete gauge algebra of
the singular quotient: other strata, twists and gluing have not been
solved. In particular, a rank-four SM sector cannot be inferred from
this rank-two fixed algebra. Inner versus outer gauge actions are also
central in [Khlaif and Najjar's ADE construction](https://arxiv.org/abs/2508.00564),
which uses a different geometry. The general anti-Calabi-Yau/Spin7 route
is established by [Forcella and Zaffaroni](https://arxiv.org/abs/0911.2595).
Neither source is being cited as a proof of the present global completion.

## What this test changes

There is a broader tradeoff within a precisely limited class. Let H be
a finite subgroup of SO5(R) normalizing the original C5. Its elements
preserve the intrinsic splitting into the C5-fixed R3 and its orthogonal
rotation plane R2. Thus H lies in S(O3 x O2). If every element preserves
the orientation of R2, its normal action lies in SO2, and that entire
SO2 still centralizes H: at least one unwanted continuous mode remains.
To remove it, H must contain an orientation-reversing normal action.
Such an action conjugates g to g^-1 and swaps u,v up to phases. Those
phases act trivially on exceptional-curve classes, leaving the same
outer Dynkin reversal. Therefore within this real orthogonal normalizer
class, removing the normal U1 necessarily introduces outer A4 cycle
monodromy. This is not a theorem about finite groups that do not normalize
the chosen C5, nonorthogonal cone changes, flux backgrounds or other ADE
sources. It explains why changing only the tetrahedral factor cannot
repair the particular SU5 construction.

This is an explicit failed shortcut: a tetrahedral/dihedral quotient
does remove the unwanted continuous algebra, but changes the local
gauge system and creates new fixed loci. A viable repair must track
normalizer actions, curve orientations and localized states together.
Counting invariant bulk fields alone misses this cost.

The separate Brieskorn test in d84e57a8e concerns replacing the uv
quadratic term by u^p+v^p in a different weighted-homogeneous cone.
It should not be read as showing that simply adding higher-order terms
to an unchanged nondegenerate quadratic singularity changes its local
analytic type. Neither that test nor this quotient rules out all
nonhomogeneous or flux-deformed alternatives.

Repo checks searched the V5,2/quadric material and the actual compound
tetrahedral/dihedral result, including the earlier packet. No priority
claim is made. Run
`python analysis/toe_20261118_tetrahedral_quadric_quotient.py` to regenerate
`data/toe_20261118_tetrahedral_quadric_quotient.json`. The exact producer
checks group closure, fixed dimensions, centralizers and the canonical
outer projection. Full localized supersymmetry, chirality, quantum
gluing, vacuum selection and observed physics remain open.
