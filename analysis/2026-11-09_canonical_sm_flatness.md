# A flatness obstruction for the canonical Standard Model and its family twists

The signed W33 cubic supplies the alternating form `Omega` on `V = 27 ⊗ 3`. Three copies of `V` are needed to use it as a nonzero holomorphic cubic. This calculation takes the canonical Standard Model embedding in Pass 11271 and tests its compatibility with the D and F equations of the signed three-copy model. The answer is an exact obstruction for the original field content and an explicit three-family extension.

## Every compact family twist of the fixed internal embedding

A twist is the graph of a homomorphism from the fixed canonical Standard Model Lie algebra to the external family `su(3)`. A nonzero color image exhausts the external algebra and forces the external weak and hypercharge images to vanish. Internal hypercharge then restricts the fields to coordinates 0 and 1. Both are internal color singlets, so tensoring with the external fundamental leaves no singlets under diagonal color.

When the external color image vanishes, the internal color singlet space consists of three weak singlets of hypercharges 0, 0, and 1 and three weak doublets of hypercharges −1/2, −1/2, and +1/2. If the external weak image vanishes, the fixed space is contained in the three internal weak singlets tensored with the family fundamental. The internal Cartan element `H = -H[0] - 3 H[3]` from the exact signed-cubic basis acts as twice the identity on those three coordinates. Its D-term is strictly positive at every nonzero point in that space, independently of the external hypercharge.

The external weak action is otherwise either irreducible of dimension three or a doublet plus a singlet. The irreducible action leaves no fixed tensor with the internal color singlets. In the regular case the external hypercharge has eigenvalues `(t,t,-2t)`. The only fixed-space cases are `t = 0, −1/2, +1/2`. At the first two values every fixed field lies in one family block, so the family Cartan with eigenvalues `(1,1,-2)` obstructs D-flatness.

At `t = +1/2`, the fixed space has dimension three. An orthonormal basis consists of two diagonal weak singlets built from the negatively charged internal doublets and the tensor of internal coordinate 2 with the family singlet. Write their species columns as `u,v,w ∈ C³`. The compressed gauge matrices give precisely the D equations `||u||² = ||v||² = ||w||² = a` and `u†v = 0`. The restricted three-form is minus the unit volume form. The three F terms therefore vanish exactly when the species matrix has rank at most one. The D equations force rank at least two at every nonzero point. The calculation checks the full bracket, including components outside the fixed space.

There is a quantitative obstruction on this exceptional D-flat branch. With the bracket normalization of the producer, the squared F norm is `||u∧v||² + ||u∧w||² + ||v∧w||² ≥ 2a²`, since the first wedge contributes `a²` and the last two contribute at least `a²` by orthogonal projection. Equality holds when `w` lies in the span of `u,v`. Thus the minimum of the squared F norm divided by the fourth power of the field norm is exactly `2/9` on the nonzero D-flat fixed space.

## An exact two-dual repair

Add two `(27̄,3̄)` fields and one internal adjoint `A`. For family basis `f0,f1,f2` and internal basis `e0,e1`, choose the fundamental and dual coordinates

- `X1 = e0 f0, X2 = e1 f1, X3 = (e0+e1) f2`.
- `Z1 = X1+X2, Z2 = X3` in the conjugate coordinate basis.
- `A = 6Y` in the integral chart.

Use the supplied superpotential `Omega(X1,X2,X3) + Z1 (A ⊗ I) X3`. The two marginal Gram matrices agree between the fundamental and dual fields. The opposite dual generator action cancels all 86 D-terms, and the Hermitian adjoint contributes zero. The signed bracket vanishes on the fundamental VEVs, hypercharge kills their internal coordinates, and the family support of `Z1` is disjoint from `X3`, so all F derivatives vanish. The compact stabilizer dimensions without and with the adjoint are 24 and 12. The adjoint leaves the canonical Standard Model algebra, and all eight external family generators are broken.

Two is minimal for this untwisted stabilizer within the fundamental, conjugate, and internal adjoint field content. The positive Cartan `H` commutes with the full internal centralizer of the canonical Standard Model, as checked by the rank-six commutator certificate. Therefore Standard Model invariant internal adjoints contribute zero to its D-term. With zero conjugates its D-term forces the fundamental VEVs to vanish. With one conjugate, `H` forces equality of the total norms, and the family D equation then gives equality of the two family marginals. A single `27̄ ⊗ 3̄` singlet has internal support on the two-dimensional `e0,e1` plane, so its family marginal has rank at most two. Every fundamental and conjugate VEV is supported on the resulting common family subspace of dimension `r ≤ 2` under conjugate identification. The generator `H` combined with a traceless family Cartan acting by −2 there and by `2r/(3-r)` on the complement fixes all VEVs. For zero support the entire external algebra survives. In either case an extra continuous gauge generator survives.

## Anomaly and mass ledger

With all fields taken as chiral superfields, three fundamentals and two duals have net internal Standard Model chirality equal to three `27`s, hence three Standard Model families. The broken gauge directions and holomorphic mass pairs are vectorlike under the surviving algebra. The remaining perturbative external family anomaly is +27 in fundamental units. A zero-VEV spectator in `(1, Sym³(3̄))` contributes −27. This is the decuplet already used in the repository's anomaly work. The cubic trace check uses family eigenvalues `(1,1,-2)` and the four multiplicities `4-r` at symmetric-cube charge `3-3r`.

The exact 483-field holomorphic Hessian has rank 198. Quotienting its kernel by the 74 broken complex gauge directions leaves 211 uneaten zero-mass chiral components before the spectator, which adds ten singlets when kept uncoupled. The certificate resolves the counts by hypercharge and checks that every gauge orbit direction is in the Hessian kernel. This extension gives the desired net chirality and continuous stabilizer. Its chosen couplings leave extensive vectorlike matter and flat directions, and their removal and the selection of the vacuum remain open. The no-go concerns graphs over the fixed canonical internal embedding and the stated original F and D equations.

The three adjoint couplings that preserve this VEV are `Z1 A X3`, `Z2 A X1`, and `Z2 A X2`. The six candidate mixed terms give a rank-three adjoint derivative, with these three coordinate directions spanning its kernel. A bilinear `Z M X` would require `M = 0`, since `A` annihilates the VEVs and the three `X` vectors are linearly independent. An adjoint mass must also vanish, by contracting its F equation with `Y`. Every mixed contribution vanishes in that contraction, while `Tr(Y²)` is positive. The adjoint invariant degrees exclude a pure adjoint cubic. It follows that the 12 adjoint chiral components along the unbroken gauge algebra are massless and uneaten for this fixed VEV throughout these renormalizable couplings. With all three allowed mixed coefficients set to one, the exact Hessian rank rises from 198 to 308 and the uneaten massless count falls from 211 to 101 before the spectator. This is a second explicit point, and the calculation leaves the maximal possible rank open. [Adjoint invariant degrees](https://jolt.centre-mersenne.org/item/10.5802/jolt.1068.pdf)

## Sources and replay

- [Canonical Standard Model embedding, Pass 11271](w33_pass11271_canonical_sm_higgs_bridge.py)
- [Exact signed cubic and original flat vacuum](2026-11-08_exact_signed_cubic_and_three_copy_vacuum.md)
- [Repository decuplet anomaly construction, Pass 11613](PASS11608_11613_CHIRAL_UNIFICATION.md)
- [Bajc and Susič's supersymmetric E6 analysis](https://arxiv.org/abs/1311.0775) and [their adjoint extension](https://arxiv.org/abs/1504.00904) give the prior GUT context. The family twist and the two-dual argument here use the explicit W33 representation.
- Run `python analysis/toe_20261109_canonical_sm_flatness.py` from the repository root to regenerate [the exact certificate](../data/toe_20261109_canonical_sm_flatness.json).
