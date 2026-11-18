# The missing executable Albert selector works, but its matter embedding differs

On the repository's E8-derived real Albert product, an explicit complex
qutrit subalgebra and a complex qubit inside it select the SM gauge
algebra. This fills the specific missing computational step identified
in Pass11569. It also gives commuting order-two/order-three selectors
and an order-six centralizer description. It does not derive a vacuum,
fermions or observed physics.

The matter and coupling checks are essential: this F4 embedding is not
conjugate to the parallel standard E6 SM embedding. Its real26 cannot
itself supply one chiral SM family. With a single F4 kinetic form, its
tree coupling ratios differ from standard SU5 unification.

## Existing objects and published theorem

The producer imports `w33_pass10950_clock_albert_lorentz_spinor.py` and
rebuilds the existing27-dimensional Jordan product from the E8 bracket.
It retains that code's basis, frame, Peirce decomposition and exact
rational arithmetic. It does not substitute an unrelated abstract F4.
The parent report is `PASS10950_CLOCK_ALBERT_LORENTZ_SPINOR.md`.

`PASS11562_11569_CANONICAL_SPIN_GAUGE_FRONTIER.md` explicitly stopped at
Spin6 dimension15 and identified the missing complex-subalgebra selector.
This packet supplies that extra input and computes its stabilizer. It
does not refute the earlier result for the smaller selector set.

The general group characterization is already a theorem of
[Baez and Schwahn, arXiv:2606.15235](https://arxiv.org/abs/2606.15235),
building on Todorov and Dubois-Violette: preserving a nested complex
qubit/qutrit pair in the Albert algebra, with the specified identity
component, gives S(U2 x U3). Our contribution here is its executable
realization and checks on the existing repository product, not discovery
of that group theorem. Older repo references include
`docs/archive/LEECH_DECOMPOSITION_BREAKTHROUGH.md`.

## Named subalgebras and exact stabilizers

In the existing27-dimensional real basis, use the primitive frame
indices(26,0,9). The first chosen closed subalgebra is

    B = span(e0,e1,e2,e9,e10,e11,e24,e25,e26),
    c = e26,
    X = B intersect E0(c) = span(e0,e1,e2,e9).

The code checks closure under the actual Jordan multiplication, not
just subspace dimensions. B contains the full frame and has2-dimensional
Peirce spaces between each pair of frame idempotents. This identifies
the rank-three Euclidean Jordan subalgebra as H3(C); X is H2(C), with
unit1-c. The coordinate-line seed search has48 successful seed pairs
and16 distinct coordinate subalgebras. These are choices in this basis,
not a census of all subalgebras or a count of particle generations.

From all multiplication-operator commutators, the code selects an exact
52-dimensional derivation basis. It imposes linear equations on its
27x27 matrices:

| Constraint | Stabilizer dimension |
|---|---:|
| Albert derivations | 52 |
| Preserve B setwise | 16 |
| Fix c | 36 |
| Preserve B and fix c | 12 |
| Preserve B and X setwise | 12 |

Within the final algebra, the ideal acting trivially on B has dimension8
and zero center. The full derived algebra has dimension11, and its
center has dimension1. Compactness inherited from F4 identifies the
algebra as su3+su2+u1. In particular the weak su2 is an internal
stabilizer here; it is not identified with the earlier event/spacetime
Spin3.

The global group follows from the published stabilizer theorem, including
its Z6 quotient. A Lie-algebra dimension alone would not determine that
quotient. Preserving B without choosing its connected unitary stabilizer
also allows disconnected transformations; these must not silently be
added to the connected SM gauge group.

## Finite selectors and an independent polyhedral check

Let Q be the real skew generator of the final one-dimensional center,
normalized to have eigenvalues i times integer weights, with Q=6Y in
quark-doublet hypercharge units. Its full27x27 matrix is in the JSON.
Its squared-weight projectors E0,E1,E4,E9 are exact polynomials in -Q².
The code constructs

    T2 = E0-E1+E4-E9 = 1-8L_c+8L_c²,
    T3 = E0+E9-(E1+E4)/2 + sqrt(3)(Q E1-Q E4/2)/2.

Here L_c is unscaled Jordan multiplication. T2 is the existing Peirce
symmetry, with fixed real dimension11. T3 has order3 and fixed subspace
exactly B, dimension9. Both are exponentials of derivations, hence
Jordan automorphisms; their orders and commutation are checked exactly.
T2*T3 has order6 and the SM Lie centralizer.

The complete adjoint characteristic polynomial is

    x^12 (x²+1)^6 (x²+4)^9 (x²+9)^2 (x²+16)^3.

Thus exp(2pi Q/k) has centralizer dimensions

| k | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---:|---:|---:|---:|---:|---:|
| Dimension | 52 | 36 | 16 | 18 | 12 | 12 |

For an independent realization, take the24 short F4 roots (a24-cell)
and24 long D4 roots. Their pairing with(1,1,1,3), adding four Cartans,
reproduces the entire adjoint charge census. This checks the normalization
in another basis, beyond a stabilizer dimension count. It does not
identify a24-cell with a physical spacetime or with W33. The finite
W(F4)/real-Clifford distinctions in
`PASS362_ALPHA_CODE_REAL_CLIFFORD_K44_F4_SYNTHESIS.md` remain distinct
from this continuous compact Lie algebra.

These finite transformations are algebraic candidates for holonomies.
No internal cycle carrying an order-five or order-six flat bundle has
been supplied by this calculation; the former quadric gauge locus had
C4, and its tetrahedral repair did not preserve its old gauge bundle.

## The real26 is not one SM family

The charge multiplicities computed from the actual matrix are:

| 6Y | 0 | each of +/-1 | each of +/-2 | each of +/-3 |
|---|---:|---:|---:|---:|
| Albert27 | 5 | 6 | 3 | 2 |
| Traceless26 | 4 | 6 | 3 | 2 |

They are conjugate-paired, and |Y|<=1/2. The real26 has neither a
Y=-2/3 state nor a Y=+1 state, required for a left-handed SM family.
The three Peirce off-diagonal sectors therefore cannot be called three
chiral generations. This is a statement about this representation and
embedding, not a no-go for additional localized states or all F4 models.
No Dirac zero-mode count is being replaced by a weight count.

For direct comparison the producer imports
`hypercharge_integer_weights()` from the parallel
`toe_20261116_E6_full_cubic_SM_stabilizer.py`. Its standard E6 27 has

    6Y : multiplicity
    -4:3, -3:4, -2:3, 0:2, 1:6, 2:6, 3:2, 6:1.

That spectrum differs even after reversing hypercharge sign. Hence the
two hypercharge generators, normalized by the quark charge, are not
E6-conjugate. A full F4 outer projection cannot preserve that standard
hypercharge in the same27. Equal names for the abstract SM Lie algebra
do not establish equal physical embeddings. This is a compatibility
test of the alternative route, not a correction to the parallel E6
stabilizer computation.
More generally, restriction of this27 to any conjugate of compact F4 is
real26 plus a singlet, so every compact Cartan has a conjugate-paired
spectrum. The standard E6 hypercharge census above is not paired.
This reality test excludes preserving that standard hypercharge in any
such full F4 fixed subgroup, not merely the particular coordinate choice.

## Coupling normalization adds another physical constraint

In the independent root realization, color has long roots such as
e1-e2, while the weak simple root can be(1,1,1,-1)/2. Using T3=alpha/alpha²
for each SU2 Cartan and Y=(1,1,1,3)/6 gives

    ||Tweak||²/||Tcolor||² = 2,
    ||Tweak||²/||Y||² = 3.

The producer independently checks these ratios on the actual Albert
matrices: after SU2-Cartan normalization, -Tr27(Tcolor²)=3,
-Tr27(Tweak²)=6 and -Tr27(Y²)=2 for real skew generators. The weak ideal
is obtained by trace orthogonality to color and the center, rather than
assuming its root length from another coordinate model.

If there is one F4-invariant gauge kinetic form, the tree boundary is

    g3²=2g2²,  gY²=3g2²,  sin²(thetaW)=3/4.

This is not the SU5 tree normalization. Thresholds, RG evolution, an
actual compactification scale and kinetic corrections have not been
computed, so these equations are not a fit to observed couplings.
Rescaling Y to improve the ratio would also change the assigned matter
charges and would not remove the spectral mismatch above.

## Keep the E6 real forms and outer projection separate

Pass10950's real str0(A) is E6(-26), not compact E6. The compact
continuation is Der(A)+iL_(trace zero) acting on the complexified27.
The code verifies trace-form blocks of inertia(0,52,0) and(26,0,0)
before the i multiplication, and zero mixed trace, yielding compact
inertia(0,78,0). Complex conjugation fixes Der(A)=F4 and reverses the
26 imaginary multiplication directions. It exchanges the complex
matter representation with its conjugate; a complete gauge/matter
outer action cannot be inferred from the gauge fixed algebra alone.

The F4-fixed E6 outer involution and its 27->26+1,78->52+26 branchings
are established in [Henning et al., section5](https://arxiv.org/abs/2111.04728).
That paper also explains why outer symmetry gauging needs a quantum
anomaly check. No such full anomaly completion is supplied here.

A researched alternative is to retain the complex hermitian triple
instead of reducing all matter to the real Albert algebra.
[Baez, Bokor and Boyle, arXiv:2607.10833](https://arxiv.org/abs/2607.10833)
study the complex16-dimensional bi-Cayley triple and its Spin10 action.
That gives a specific next comparison with the repo's Peirce16 and E6
matter operators. Its embedding, triple closure and chiral dynamics
have not been implemented by this producer; the literature's proposed
correspondence is not a substitute for those checks.

Run `python analysis/toe_20261118_Albert_qubit_qutrit_SM_selector.py`.
The certificate records the selector, full Q matrix, exact dimensions,
finite-order controls, charge comparison and physical limitations.
The remaining goal requires a selected vacuum and a chiral matter
mechanism with observed charges, dynamics, scales and gravity; this
packet supplies one concrete algebraic bridge and tests its limits.
