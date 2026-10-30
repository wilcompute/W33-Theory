# Passes 588–594 — optimal collision degree, complete linear symmetry, oriented Singer cover, Dedekind localization, corrected continuous readout, and pentagon holonomy

This release executes the five directions opened after Pass 587 and adds two cross-tower workstreams suggested by the combined W33, 600-cell, Johnson, Singer, and photonic structures.

## Pass 588 — degree 13 is optimal for projective transpositions

Work in the reduced function ring `F3[x0,...,x6]/(xi^3-xi)` on the seven-dimensional hidden-`C3` fixed locus. For each nonzero projective point `[a]` the odd point indicator

`s_a(x)=h_a(x) product_j (1-l_j(x)^2)`

has support `{a,-a}` and reduced degree 13.

The generalized Reed–Muller minimum-support formula gives minimum support two first at degree 13. An exact enumeration of all 1,093 points of `PG(6,3)` further shows that their degree-13 leading forms are pairwise distinct. Consequently every projective transposition

`F_ab(x)=x+s_a(x)(b-a)+s_b(x)(a-b)`

has unique reduced degree exactly 13. The exceptional three-point fibre and all five nonidentity elements of its `S3` also have degree 13.

Therefore degree 13 is necessary and sufficient for every projective-point transposition and for any transposition-generated realization of the collision groupoid. This does not exclude a generating system built exclusively from larger-support permutations of lower degree.

## Pass 589 — the full linear spectral group is exactly `C3`

The complete characteristic-polynomial coloring of the 797,162 sign-projective words in `PG(12,3)` has 221,451 colors. Eleven nonzero singleton colors span rank five. Extending five independent singleton points by eight points from three-element color classes gives a full projective frame with class sizes

`1,1,1,1,1,3,3,3,3,3,3,3,3`.

An exact color-and-incidence backtracking search checks every possible image of this frame. Only three projective linear automorphisms survive:

`I, U, U^2`,

where `U` is the hidden Hjelmslev shear. Thus `Aut_linear(spectrum)=C3`.

The packet `C3` module has Jordan partition `(3,3,3,1,1,1)`. Its endomorphism algebra has dimension 54, and its invertible centralizer has exact order

`18,935,612,583,143,002,835,272,704`.

Every colored-600-cell intertwiner differs from the canonical one by an element of this centralizer. Because the full linear spectral group is only `C3`, no one of those roughly `1.89e25` intertwiners can transport the full `A4` into a linear spectral symmetry. This is a universal linear no-go; nonlinear actions remain outside the claim.

## Pass 590 — oriented Johnson cover and the 672-object refinement

The 56 triples of an eight-set admit a canonical orientation double cover with 112 objects. The stabilizer of an oriented triple in `A8` has order 180 and is `C3 x A5`.

These 112 objects are exactly the signed exterior basis vectors `±(e_i wedge e_j wedge e_k)` of `Lambda^3(8)`.

Refining an oriented triple by one of the six Sylow-5 pentagons on its complementary five-set gives 672 objects. This system maps two-to-one onto the 336 Singer flags by forgetting orientation and six-to-one onto the 112 oriented triples by forgetting the pentagon.

The refined stabilizer has order 30 and is `C3 x D10`. The unoriented triple stabilizer acts on the six pentagons through `S5` with kernel `C3`; the oriented stabilizer acts through `A5` with the same kernel.

This identifies the oriented cover with the signed basis orbit of the `SL8` module `Lambda^3(8)`. It does not identify it with the `E7` minuscule 56, whose `A7` restriction is `28+28`.

## Pass 591 — maximal order and the generic DVR closure

For `f(x)=x^4-5x^3+10x^2-10x+5`, Eisenstein at five gives degree four. Its discriminant is 125, equal to the fifth-cyclotomic field discriminant `5^3`. The order index therefore has square one, so the shifted `AdjoinRoot` order is the maximal order and hence a Dedekind domain.

At the prime `(lambda)`,

`lambda^4=5(lambda^3-2lambda^2+2lambda-1)`,

and the factor in parentheses reduces to `-1`, hence is a local unit. The local arithmetic is therefore `e=4`, `f=1`, `v(lambda)=1`.

The new Lean module invokes Mathlib's theorem that localization of a Dedekind domain at a nonzero prime is a discrete valuation ring. It contains no `sorry`, `admit`, or declared axiom. The remaining presentation-level formal task is to register the concrete index-one `AdjoinRoot` order as the ring of integers/Dedekind instance and compile the full chain.

## Pass 592 — the aspirational grid tie is superseded

The earlier nearest-composition belief grid reported an aspirational uniform-prior value `4.2574616`. This is impossible in the declared experiment.

The orientation marginal alone is a symmetric binary sequential problem with effective accuracy `14559/20000 = 0.72795`. Exact rational Bellman equations prove that the optimal policy continues for `|k|<5` and stops for `|k|>=5`, with value `12.2560439301`.

The joint terminal error obeys `200(1-mF mO) >= 100(1-mF)+200(1-mO)`. Because separate sensing must pay at least one unit for fibre information,

`V_base(uniform) >= 13.2560439301`.

A concrete joint policy uses `J1` for each orientation-SPRT sample. One `J1` quartic result already has fibre error below `2.3e-6`, giving

`V_joint(uniform) < 12.2565039301`.

Hence the continuous-model gain is at least `0.99954`. A 200-Lipschitz Bayes-value bound certifies strict improvement throughout an `L1` ball of radius `0.00249885` around the uniform prior. The old grid tie resulted from posterior projection creating artificial information and is explicitly superseded.

## Pass 593 — each Singer fibre is an icosahedral `P1(F5)`

The six Sylow-5 subgroups on a five-set carry the exceptional degree-six action `S5 ~= PGL(2,5)` on `P1(F5)`. Its alternating subgroup is `A5 ~= PSL(2,5)`.

Geometrically these six objects are the six fivefold rotation axes of an icosahedron, equivalently the six antipodal vertex pairs. The axis stabilizer is `D10`.

The six-axis permutation module splits as `1+5`; its five-dimensional augmentation is irreducible under `A5`. Across the 56 Johnson blocks this gives the complete Singer fibre complement `56*5=280`.

The identity `280=56*5=40*7` is recorded, but no canonical 56-by-40 W33 incidence follows from the count alone. The five snub-octahedral colorings form the distinct `1+4` module, so the two occurrences of five must not be conflated.

## Pass 594 — full `S5` holonomy over `J(8,3)`

A canonical reversible connection was placed on the six-pentagon bundle over the Johnson graph. For adjacent triples exchanging `a` and `b`, the edge transporter is the even permutation `(a b)` times the transposition of the two smallest points outside their union.

After spanning-tree gauge fixing, the holonomy group on one six-point fibre has order 120 and exact element-order census `1^1, 2^25, 3^20, 4^30, 5^24, 6^20`.

It is the full exceptional degree-six `S5`, equivalently `PGL(2,5)` on `P1(F5)`. Johnson triangle loops alone already generate the full group.

Thus the 336 Singer flags form a nontrivial six-state icosahedral local system over `J(8,3)`, and the classical outer-automorphism seed `S5 < S6` appears as its fibre holonomy. No equality with the repository's 2,160-slot Witting holonomy is asserted.

## Validation

The seven owners report **86/86 checks**, the aggregate lock reports **19/19 checks**, and the focused suite reports **7/7 tests**.

The release is exact for the declared finite function rings, the complete projective linear coloring, finite group actions, cyclotomic arithmetic, and stochastic observation model. It deliberately preserves the boundaries on nonlinear symmetry, the concrete compiled Dedekind instance, exceptional-Lie identifications, and the full continuous equality locus.
