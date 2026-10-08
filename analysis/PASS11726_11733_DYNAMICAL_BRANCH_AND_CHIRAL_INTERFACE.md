# Passes11726–11733: clock selection, an E8 Yukawa projector and a spacetime section

Reservation **5470f3255** was pushed before computation. This packet executes
the five requested investigations and three additional probes. It constructs
interfaces and tests their compatibility; it does **not** close the physical TOE.

[Producer](w33_pass11726_11733_dynamical_branch_and_chiral_interface.py),
[certificate](../data/w33_pass11726_11733_dynamical_branch_and_chiral_interface.json),
[independent tests](../tests/test_w33_pass11726_11733_dynamical_branch_and_chiral_interface.py).

The strongest positive results are an open-coupling clock-class selector,
a nonzero symmetric E8 Yukawa projection of squared norm **1/7**, and eight
explicit E8 exceptional-field-theory section directions. A global topology
test also identifies why the proposed Higgs and chiral-index constructions
cannot simply be combined unchanged.

## Intake and prior ownership

The local and remote master were synchronized through receipt2ca529867 before
the reservation. Claude's11713–11720 reservation remains owned by that track;
no unfinished files from that range were imported. Desktop Claude.txt was
read fully and was unchanged. Prior11721–11725 was read in full, including its
certificate and branch boundaries. The forty-points paper's physics scorecard
still marks masses, mixing, couplings, gravity and vacuum energy open. This
packet preserves that boundary and does not modify the paper.

Searches covered RESULTS_INDEX, TOPICAL_ALIASES, the papers/site, Python,
Markdown and certificates, including results themselves:3875/27000,1304,
19200/76800,184 with orbit terminology,2b/3, inverse-Casimir, the explicit
bundle multidegrees and the exceptional section constraint. An integer that
is merely a pass number is not treated as prior scientific content.

- **11681** owns the actual sl9+Lambda3+dual E8 bracket and split real form.
- **11721–11725** owns the coherent parity lift, hidden-SU5 matrix units,
  principal triplet, all248 gauge masses and mixed invariant I.
- **11271**, **11293**, **11497** own the symmetric-family Yukawa operator,
  heavy-source completion and rank30 exotic-mass interface. We do not claim
  the representation decomposition or a symmetric Yukawa operator as new.
- **11301** owns the finite pointwise Leibniz obstruction; **11623** the
  linear spin2 constraint interface. The conformal graph calculation below
  does not silently inherit nonlinear ADM closure.
- **11274/11284/11289**, **11546**, **11629**, **11679** own sequestering,
  fixed-data shift tests and flux/reference boundaries; see also the complete
  [11615–11619 parent/constraint report](PASS11615_11619_PARENT_PAIRS_CONSTRAINTS.md)
  and `analysis/w33_pass11615_11619_parent_pairs_constraints.py`.
- **7154–7162** already cites E8 exceptional field theory, without constructing
  the explicit section tested here. The site already mentions coadjoint orbits
  generally;11726 supplies this particular map, stabilizer and tangent census.

Classical foundations, not novelty claims:

- [Slansky, Table53](https://doi.org/10.1016/0370-1573(81)90092-2):
  Sym2(248)=1+3875+27000 and the E6×SU3 branching of3875.
- [Hohm–Samtleben, E8 exceptional field theory, equations2.4–2.7](https://arxiv.org/abs/1406.3348):
  the3875 projector and strong section constraints. Its action and compensating
  gauge symmetry are established additional structure, not consequences of
  the finite graph. The executable coordinates below realize a section of
  that classical framework.
- [Candelas–Horowitz–Strominger–Witten](https://doi.org/10.1016/0550-3213(85)90602-9):
  the compactification reading of the internal Dirac index. Our supplied
  CP1-cubed geometry is not their Calabi–Yau solution.
- [Ó Murchadha, readings of the Lichnerowicz–York equation](https://arxiv.org/abs/gr-qc/0502055):
  the continuum conformal-constraint method. We test a graph analogue.
- [Henneaux–Teitelboim](https://doi.org/10.1016/0370-2693(89)91251-3):
  the cosmological constant as a variable conjugate to a global volume time.
  Covariance under relabelling that variable is distinct from screening at
  fixed state and boundary data.

##11726 — replace the forbidden fundamental9 by an actual equivariant orbit

For rho=|psi><psi|−I9/9, the actual E8 roots have rho-charges

    0:56; +1:8; -1:8; +2/3:28; -2/3:28; +1/3:56; -1/3:56.

Including the eight Cartans gives stabilizer Lie algebra su8+u1 of dimension64,
and a compact coadjoint orbit of real dimension184. Globally the stabilizer
is the image of S(U1×U8), not a claim that its group is a direct product.
There is a well-defined associated-bundle map

    E8 ×_(SU9/Z3) CP8 -> orbit(rho), [g,[psi]] -> Ad_g rho.

The fiber dimension16 plus base dimension168 equals184. Projective rays
descend through the Z3 center even though a charged fundamental9 does not.
An actual compact trivector transport preserves the norm and leaves the
sl9 slice; this checks the previously missing E8 directions.

There is a further quantum constraint. In the standard long-root norm2 and
hbar=1 normalization, rho has fractional coroot periods1/3 and2/3. Its
minimal integral KKS level is therefore **3**. For lambda=3rho, an explicit
positive system gives seven zero simple-root Dynkin labels and one1.
The exact120-root Weyl dimension product gives **147250**, and the quadratic
Casimir is144, agreeing with the classical Table53 index1425×60. Thus the
natural uncorrected holomorphic geometric quantization of this enlarged
orbit is a147250-dimensional E8 representation, not the original9-dimensional
state carrier. This uses a supplied symplectic/hbar normalization and does
not predict an observed particle multiplet or its energy.

This also connects the completion back to the existing material. The CP8
fiber line bundle at level3 is O(3), with section carrier Sym3(C9) of
dimension165, occurring as the SU9 highest-weight module in this E8
representation (duals depend on the Borel convention). Its nontrivial Pauli
character is3, so as a Pauli module it has five trivial characters and two
copies of every nontrivial character:165=5+2×80. Those five singlets are
**already** the dual-even-Weil/Coble cubic carrier of
[11651](PASS11651_N_QUTRIT_HESSE_SPACE.md), also connected to fermionic
triples in[11681](PASS11681_E8_FROM_TWO_QUTRITS.md). The added connection
is their place in this orbit's integral quantum completion. No147250×147250
matrices or a new intertwiner are claimed; an independent character test
uses all80 actual symmetric Weyl operators.

**Boundary:** a fully E8-invariant scalar function on this transitive orbit
is constant. The old Pauli S4 potential therefore needs additional co-moving
frame fields. This map does not by itself complete that potential or convert
the old parent fields into E8 representations.

##11727 — select the principal branch and the SM clock class

Inside the supplied hidden defining5, add a real auxiliary t with supplied
compact domain0<=t<=2 and the positive term

    ||t sum_a Phi_a²−I5||²

to the prior fuzzy-sphere residuals. A zero is a unitary SU2 representation
with scalar, nonzero Casimir. All irreducible blocks must have the same
dimension; because5 is prime, only the irreducible5 is possible. Its Casimir
is6 and t=1/6 follows. The seven partitions of5 have exact optimized
inverse-Casimir residuals5,3,2,1,1,5/7,0.

The compact auxiliary assumption matters: without it, Phi=epsilon J and
t=1/(6epsilon²) give energy60epsilon²(epsilon−1)² tending to zero at
infinite t. Unique finite zeros alone would not establish coercivity.

Now restrict U to the identity-component centralizer SU5 and U³=I. There
are exactly seven cube-root multiplicity classes. Set

    Vclock=−a(Im Tr5 U)²−b Re Tr5 U.

For **b>0 and a>2b/3**, its only minima have multiplicities(2,3,0) or(2,0,3).
They leave precisely su3+su2+u1. At a=2b/3 the identity ties, and below it
the identity wins. This is an open region of coefficients, not a single fit.

The full E8 adjoint character can express both terms without inserting a
fundamental5 field. For C=sum ad(Ja)², let P0,P2 be its spectral projectors
at eigenvalues0,2, of ranks24,33. Then

    R=(Tr_ad(P2 AdU)−3)/6 = Re Tr5 U,
    B=Tr_ad(P0 AdU)+1−R² = (Im Tr5 U)².

All seven classes agree with the actual248-coordinate operators. This
replaces11724's supplied target Tr_ad U=5 by a supplied energy whose
minimization gives that class.

**Boundary:** hidden-SU5 carrier, cubic clock constraint, connected component,
compact auxiliary domain and coupling wedge remain model inputs. The spectral
formula is a covariant branch functional; no globally polynomial off-branch
E8 action or radiative stability theorem is asserted.

##11728 — an explicit chiral index, with the actual extra modes exposed

Take the supplied spin manifold X=CP1×CP1×CP1 and split SU3 bundle

    V=O(1,1,1)+O(1,1,−2)+O(−2,−2,1).

The first Chern class is zero. With x²=y²=z²=0, integral c3(V)=6, so
ind(D_V)=3. The spin Dirac operator is Dolbeault twisted by K^(1/2); its
three summands have cohomology degree/dimension(0,1),(1,2),(2,4).
There are therefore **five positive and two negative** zero modes, not just
three positive modes. A named2×5 finite-rank smoothing map pairs two chosen
positive modes with the negative modes and leaves exactly three positive
ones. Its rank and kernels are checked exactly.

**Boundary:** this is a supplied, reducible bundle on a non-Calabi–Yau manifold.
It has abelian structure-group holonomy, not an irreducible SU3 vacuum.
The added smoothing map is E6-invariant in the declared matter interpretation;
its locality and residual abelian gauge completion are not supplied. No
ten-dimensional equations, stable-bundle conditions, local Yukawa overlaps
or observed masses follow. The familiar SM anomaly sums vanish per family;
this check is not a complete anomaly analysis of an unspecified compactification.

##11729 — a nonlinear constraint and an actual exceptional spacetime section

On the literal40-point W33 graph, solve

    8 L phi+R phi−a phi^−7+b phi^5=0, phi_i>0.

For a_i>0,b>0,R>=0 this is the gradient of

    4 phi^T L phi+(R/2)sum phi²+sum a/(6phi^6)+(b/6)sum phi^6.

The energy is coercive, diverges at the positive-domain boundary, and has
positive Hessian8L+diag(R+7a phi^−8+5b phi^4). Thus a positive solution
exists and is unique. The inhomogeneous40-coordinate witness has residual
below1e−12; permutation, constant-source and Laplacian-scale controls are
stored. The conditional continuum dictionary is b=2K²/3−2Lambda.
This is a graph constraint prototype, not a3D metric or full Einstein evolution.

The stronger algebraic connection uses the **same3875 projector as11732**.
In the actual11681 split-real coordinates, the eight vectors

    A_3i, i=0,1,2,4,5,6,7,8

satisfy all strong section constraints: invariant bilinear and brackets
vanish, and all36 symmetric pair projections onto3875 vanish. Identifying
adjoint vectors with covectors via the invariant form gives an explicit
eight-coordinate section. For distinct pairs the entire corresponding
root-pair weight sector has cross Casimir Omega=2; for a repeated root its
unique weight2alpha sector also has Omega=2.

The section is **maximal as a constant complex linear section**. Every one
of the other232 root directions fails a named constraint:1 the singlet,
57 the adjoint bracket, and174 the3875 projection, each latter witness
having squared norm1/7. The eight Cartan extension equations have rank8.
For a fixed section generator, different root coefficients produce different
total weights and cannot cancel these failures. The certificate names every
rejected root and its witness; this is stronger than an eight-direction count.

This section has a projective-ray description: span{|psi><v|:v perpendicular
to psi}, with psi=e3, the previous SM-neutral density example. Its complex
SU9 transports remain algebraic sections; arbitrary complex transports are
not assumed to preserve the chosen split-real form. A polynomial one-coordinate
vector-field commutator also checks the nonlinear Leibniz/Lie identity.

The actual Yukawa pair(A30,x013) fails the3875 constraint with squared norm
1/7. The first direction belongs to the section; the second cannot be added
as an independent coordinate derivative. This separates a tested coordinate
sector from a tested matter interaction channel without identifying all248
E8 labels as spacetime coordinates.

**Boundary:** the established EFT action, external Lorentzian3-space,
compensating gauge fields, scales, section selection and compactification
are additional inputs. We have not derived those from W33 or selected a
physical3+1-dimensional vacuum.

Compact internal E8 gauge symmetry and split E8(8) exceptional duality have
different real forms and physical roles. Sharing a complex bracket and
projector does not identify their gauge fields or inherit either action's
unitarity, kinetic terms or fermions in the other construction.

##11730 — vacuum-energy covariance must include the quantum state

A direct-sum shape Hamiltonian with volume eigenvalues2,3 provides a negative
control. Within a fixed-volume block, adding C V changes only an overall
phase. Across coherent blocks it changes the relative phase by exp(i C t),
which is observable. The producer verifies this with actual unitary evolution.

H(Lambda,C)=H0+(Lambda+C)V is covariant under Lambda->Lambda−C. That changes
the Lambda-state or boundary data; holding them fixed does not screen C.
Moreover no finite-dimensional unitary can implement Lambda->Lambda−C I
for all realC, since trace is invariant. No bounded spectrum supports all
real translations. L²(R,dLambda) supplies the usual translation representation,
but it has no translation-invariant normalizable state.

This identifies the missing state/measure condition in an attempted quantum
unimodular completion. It does not determine the cosmological constant.

##11731 — the principal Higgs and chiral bundle are globally incompatible

Use the actual family SU3 on physical levels3,4,5; it commutes with the visible
SU5 on0,1,2,7,8. The hidden defining5 restricts to its **dual3+1+1** in the
11681 matrix-unit convention. Thus W=V*+O+O has integral c3(W)=−6.

An everywhere-principal **ordered** triplet reduces the hidden-SU5 bundle to
its finite centralizer Z5. Its rational Chern classes then vanish, contradicting
c3(W)=−6. Allowing rotations of the triplet only enlarges the stabilizer to
the principal SO3 image times Z5. The five-dimensional spin2 representation
is real, with Chern roots(2u,u,0,−u,−2u), and again c3=0. Conjugating the
family convention changes the sign of6, not the obstruction.

This is a same-bundle compatibility theorem, not a retraction of11724's
finite-point Higgs construction. Potential escapes include rank-loss defects,
different Higgs representations or a different identification of the family
bundle. No escape is certified by this packet.

##11732 — the symmetric Yukawa channel survives full E8 projection

Use family SU3 on levels3,4,5. The actual E8 roots A30 and x013 are in the
same highest family component of(27,3). Their symmetric product has squared
weight4 and a **seven-dimensional** root-pair weight space. The exact cross
Casimir Omega has eigenvalues−12 once and2 six times. Therefore

    P3875=(2−Omega)/14

on this sector is an exact rank-one projector, and the normalized seed has
projected squared norm1/7. Every one of the168 nonzero root-bracket constants
used is checked against11681's original tensor bracket. Independent raising
operator tests give family highest weight(2,0), the symmetric6.

Classically3875 contains(27,6bar) and its conjugate. An E8-invariant operator

    y H_ab psi^a_alpha psi^b_beta epsilon^(alpha beta), H in3875,

thus supplies the full-group channel for11271's symmetric d_E6×family-sextet
coupling. The two-Weyl Lorentz scalar is symmetric in combined gauge/flavor
indices; it avoids the prior vanishing d×epsilon-family construction.
The explicit7×7 matrix is stored, rather than inferring the channel from dimensions.

**Boundary:** this is a classical representation completion plus an actual
nonzero projection witness. The canonical signed27 intertwiner and overall
coupling normalization are not reconstructed. A3875 scalar changes the
inventory; no chosen Higgs vev, local chiral spectrum, overlap-derived Yukawa
matrix, observed mass hierarchy or beta-function completion is certified.

##11733 — lift the eleven shape flats in the branch EFT

On the principal branch and traceless Hermitian SU5 centralizer,11725 proves

    I=1080 p2²+960 p4; p4>=7 p2²/30.

The earlier squared selector starts at fourth order in the eleven physical
shape perturbations. The **unsquared branch restriction**

    eta(I−1304 p2²)=960 eta(p4−7 p2²/30), eta>0,

is nonnegative there and gives Hessian eigenvalues19200 eta eight times
and76800 eta three times in the Tr(dSigma²) metric. The twelve gauge-orbit
directions stay zero. Retaining(p2−30)² gives the separate radial eigenvalue240.
The full24-direction Hessian is independently constructed in another basis.

**Boundary:** positivity is branch-specific. No off-branch boundedness of the
unsquared E8 invariant is claimed. These are dimensionless model curvatures,
not measured particle masses or a UV-complete scalar potential.

## What is still needed

The principal Higgs and a chiral internal bundle must coexist in one local
model. The frame-dependent vacuum action needs an actual E8 field completion.
Exceptional-section selection and Lorentzian dynamics need an action and
vacuum with the correct physical dimensions. Local overlap integrals must
determine flavor, and vacuum-energy protection must survive fixed quantum
state/boundary data. The eight certificates make these requirements explicit;
they do not replace them with matching dimensions or fitted eigenvalues.

## Validation

The final eight-section producer and maximal-section extension pass. The
combined19 new and15 prior regressions pass **34 tests in122.87s**; results
for the added Sym3 character control are retained in the receipt. Source
binding, compilation, conflict-marker checks and the forced-arithmetic
selftest pass. The final four-file intake has no guard collisions, forced
arithmetic or certified-value contradictions. RESULTS_INDEX and the separate
TOPICAL_ALIASES builder were both refreshed; aliases scanned5225 files and
1095 tokens. Local and exact-science-SHA hosted results are retained in the
publication receipts, with any later failures recorded rather than hidden.
