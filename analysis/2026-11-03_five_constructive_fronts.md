# Five constructive continuations: interactions, vacuum, receiver, tunneling and interfaces

This packet executes the five investigations proposed after `60ae56bf3`.
It constructs explicit mathematical objects and conditional field-theory models;
it does not solve the theory of everything. The original homogeneous native
cubic still has its previously established vacuum-selection/ADS problem.
The new stabilized example changes its superpotential and supplies a mass scale.

The five producers are `w33_20261103_changed_embedding_matter_completion.py`,
`w33_20261103_native_singlet_stabilization.py`,
`w33_20261103_native_qutrit_feedforward.py`,
`w33_20261103_kagome_tunneling_bounds.py`, and
`w33_20261103_deck_twist_interfaces.py`, under `analysis/`, with matching
certificates under `data/`. The fixture-free test module and validation producer
carry the same `five_constructive` prefix.
The additional sixth producer, `w33_20261103_native_quantum_vacuum_displacement.py`,
continues the stabilized model to an exact algebraic critical curve in a
declared holomorphic effective theory.

## Intake, ownership and research

Master was reviewed through `60ae56bf3`, including the previously read parallel
Fox-tricoloring/parafermion and hyperoval results `6d6432fe0`, and four-bit IC /
eiconal results `422708cc0`. No newer commit was present at initial intake.
The prior unchanged-embedding cubic obstruction remains valid: per
decision-33f7cdf6-0810-403c-a4bd-e977fa33eb8c [source CLI, cite:d918f9], its
published packet and parent artifacts are frozen. Here the mixed interactions
use the **changed** embedding already supplied by the Nov2 native-cubic repair.
They do not evade a theorem while keeping its hypotheses.

Result searches covered the existing result index, source, reports and docs for
kagome/cuboctahedral geometry, feedforward, singlet stabilization, the120/127
interface, and graph/spanning-tree integrals. These are bounded searches, not
proofs of novelty. Earlier applicable owners were read:

* Nov2 native-cubic repair: actual signed coordinate map and epsilon mixed tensor.
* Nov2 conditional symplectic vacuum and Nov3 effective quantum audit: F-flat
  branch, charged null modes, Sp(2) Nf=1 ADS obstruction.
* Nov3 postselected qutrit holonomy: actual projectors and selected generators.
* Nov3 all-quartet tunneling:9720 palettes, adjacency degree320, spectral
  difference216, and the exact4x4 coefficient.
* Nov2 deck monodromy and Nov3 cocycle selection: actual deck maps, meridians,
  and the A4-invariant classes120/127.
* October22 all-five report: feedforward questions on a different large CSS
  carrier; it does not establish the present native rank3 receiver.
* Pass11957–11961: earlier explicitly supplied multiplier stabilization in a
  different gauge model. Multiplier stabilization is not claimed as a new method.
* BT1331 kagome note: a different proposed W33 embedding. Its unverified folding,
  code-distance and hardware assertions are not inputs to this packet.

External primary research checked during execution:

* [Intriligator–Pouliot, hep-th/9505006](https://arxiv.org/abs/hep-th/9505006):
  Sp SQCD superpotentials, mass deformations and pure-gauge vacua. These are
  conditional dynamical inputs, not deductions from a finite group order.
* [Oi,1402.1104](https://arxiv.org/abs/1402.1104): general degenerate-projection
  holonomies. The general method is prior art.
* [Bullivant–Hu–Wan,1706.03611](https://arxiv.org/abs/1706.03611): subgroup and
  two-cochain boundary data for twisted quantum doubles.
* [Warman, AlgebrasTQD,2610.36029v1](https://arxiv.org/html/2610.36029v1),
  posted26 October2026: exact algebra/interface computations, subgroup
  trivializations, and the need to quotient algebra data by equivalence.
  AppendixA.1's full coboundary equation is checked directly here. The package
  itself is not installed or claimed to have validated these certificates.

Internet searches for the graph integral did not establish a priority claim.
The elementary derivation below is included so it can be assessed directly.
The original full-week patch-reading and full-PDF-reading audit remains
incomplete; this packet does not represent it as completed.

## 1. The changed embedding permits exactly one mixed cubic, and its matter must be anomaly-free

Use the existing `Pf6(A)+u^T A v` realization of the same signed native cubic,
with `B=diag(U4,I2)`. Its27-dimensional SU4 representation is

`6 + 2*4 + 2*dual4 + 5*1`.

For a tensor linear in one27 scalar and bilinear in two fundamental4 fields,
the central `iI4` permits only the six scalar coordinates `chi=A|C4`.
There are96 coefficients. The seven actual finite Clifford generators impose
672 equations; their reduction at `i=4,sqrt2=6` over F17 has rank95. All rational
denominators are inverted in the field. A nonzero exact epsilon witness supplies
the remaining dimension, proving characteristic-zero nullity exactly1.
It is alternating in the two4 indices; the symmetric tensor space is zero.
The witness itself, `chi^T J(psi wedge eta)`, is credited to the Nov2 producer.

At `chi=t Omega`, the resulting8-by8 chiral Hessian has full rank and all
singular values `|yt|`. However, two new fundamental chiral multiplets have
SU4 cubic anomaly+2 in fundamental units. The explicit anomaly-free extension
adds two antifundamentals and

`Wext=y chi^T J(psi wedge eta)+ytilde psi_tilde^T chi eta_tilde`.

Its added anomaly is zero. The two8-dimensional blocks have masses `|yt|`
and `|ytilde*t|`. These are supplied internal gauge multiplets; identifying
their four components with spacetime fermion spin is not justified.

The extra matter changes the UV beta coefficient9 to7. Before decoupling the
new masses, the unbroken Sp(2) theory has Nf=3 and coefficient6. Standard
holomorphic matching gives, up to nonzero convention-dependent constants,

`Lambda_Nf3^6 ~ Lambda_SU4^7/t`,
`Lambda_Nf1^8 ~ y*ytilde*t*Lambda_SU4^7`.

The reversed power of `t` relative to the old matter inventory matters.
Adding massive spectators changes the effective dynamics. This extension
alone does not stabilize the remaining native-sector ADS runaway.

## 2. An explicit29-field deformation removes every physical classical flat direction locally

This is a separate model: native27 plus two SU4-singlet chiral fields S,T.
It does not assume the extra16 fields of the preceding matter extension.
Write `p_i=A_i4,q_i=A_i5`, with indices0 through3, and add

`DeltaW=sum_i(u_i*p_i+2*u_i*q_i+3*v_i*p_i+5*v_i*q_i)`
`       +u5*v4+S*(u4-1)+T*(v5-1)`.

Units are supplied: the quadratic coefficients and multiplier kappas have
mass dimension1, and `1` in the constraints is a chosen nonzero VEV scale.
The example uses a common unit and mass matrix `[[1,2],[3,5]]`.
Every new term is SU4 invariant; all15 infinitesimal sl4 variations vanish
identically. Thus the actual seven finite Clifford generators preserve it.

At `A02=A13=u4=v5=1`, all other fields zero:

* all29 F terms and W vanish exactly;
* D vanishes because `chi*chi-dagger=I4` and u4,v5 are gauge singlets;
* the29-by29 superpotential Hessian has rank24;
* the charged16-by16 block has determinant256 and full rank;
* the five Hessian zero directions are exactly the complexified gauge orbit.

Consequently the classical chiral vacuum is locally isolated modulo gauge,
with unbroken USp4. This is stronger than merely lifting one radial modulus.
Unbroken gauge multiplets are still present, and other global vacua have not
been classified. F=D=0 gives a nonnegative supersymmetric scalar potential;
no tachyon is being hidden by the holomorphic Hessian terminology.

Under the additional weak-coupling hierarchy in which all matter masses and
the Higgs scale exceed the strong scale, the low-energy theory is pure USp4,
with dual Coxeter number3. Standard gaugino condensation has three branches.
Local holomorphic nondegeneracy permits small nonperturbative displacements
of the isolated classical solution in this regime. The explicit effective
calculation below constructs these displacements. Global finite-coupling UV
dynamics remain unclassified.

A separate mass-deformed mesonic benchmark displays the mechanism:

`W=2*sqrt(Lambda_low^8/M)+m*M+X*(t-v)`.

For nonzero inputs the stationary mesons obey
`M^3=Lambda_low^8/m^2`, giving three finite roots, with
`W_MM=3m/(2M)` nonzero. X balances the t derivative. This uses an added tree
mass and constraint; it is not a property of the undeformed pure cubic.

### Additional investigation: solve the effective quantum stationarity equations

The entire charged16-coordinate Hessian admits an exact flavor factorization.
In the SU4-singlet ansatz
`chi=t*Omega, A45=z, u4=r, v5=q, u5=l, v4=k`, replace the two dual4 fields
by Omega times fundamentals. The charged Hessian becomes `Mflavor tensor Omega`,
where the4-by4 antisymmetric flavor matrix has upper-triangle entries

`(M01,M02,M03,M12,M13,M23)=(t,1+k,3-r,2+q,5-l,t)`.

Its Pfaffian is

`P=t^2-(1+k)*(5-l)+(2+q)*(3-r)`.

The full charged Hessian determinant is exactly `P^8`; at the classical vacuum
P=2, recovering256. Before decoupling this matter the Sp(2) theory has Nf=2
and beta coefficient7. Holomorphic Higgs and mass matching therefore give

`Lambda_pure^9=C*Lambda_SU4^9*P/t^2`.

The standard threshold normalization C is nonzero and absorbed in epsilon.
In the common input mass units the effective superpotential is

`W_eff=z*(r*q-l*k-t^2)+l*k+S*(r-1)+T*(q-1)+3*epsilon*(P/t^2)^(1/3)`.

This yields an exact parametrized solution of all eight effective F equations.
For parameter b define

`t^2=1+5*b^2`, `r=q=1`, `l=5*b`, `k=-b`,
`R=2*(1+5*b)/(1+5*b^2)`,
`A=b*(1+5*b^2)/(1-2*b-5*b^2)`,
`z=A*(1-R)`, `S=3*A-z`, `T=-2*A-z`.

The scale relation is

`4*b^3*(1+5*b)^2*(1+5*b^2)^4`
`   -epsilon^3*(1-2*b-5*b^2)^3=0`.

This polynomial has degree13 in b. Every effective F equation is checked as
an exact symbolic identity on the curve, with epsilon assigned a consistent
cube-root branch. The massive Higgs patch excludes t=0, P=0 and the displayed
denominator's zeros. Algebraic roots outside the weak patch are not counted
as additional physical vacua.

For `c=2^(-2/3)`, the weak branch has `b=c*epsilon+O(epsilon^2)` and

`(delta t,delta z,delta r,delta q,delta l,delta k,delta S,delta T)`
`   =c*epsilon*(0,-1,0,0,5,-1,4,-1)+O(epsilon^2)`.

The radial modulus first shifts at second order:
`t=1+(5/2)*c^2*epsilon^2+O(epsilon^3)`.
All eight F equations through second order are separately verified using
derivative tensors, and independent numeric checks evaluate the full effective
gradients at three finite parameter values. The three gaugino branches act
by the cube roots of unity on epsilon near the classical point. D flatness
persists on this singlet ansatz. This is exact stationarity in the stated
holomorphic EFT, with an explicit controlled local expansion; its applicability
still depends on the supplied gauge theory and a heavy-scale hierarchy.

## 3. All81 branches give deterministic ideal qutrit Clifford gates

For each of the three prior generators, measure in the order Pc, Pb, P0,
retaining all27 triples `(rC,rB,rA)`. Each branch has probability1/27,
independent of the encoded logical state. The final output code can vary.

The exported lookup table specifies an exact physical correction:

1. Align the final code with `I3 tensor X^(-rA)`.
2. Apply the inverse logical Pauli `(X^a Z^b)^dagger` from the outcome table.

All corrected Kraus maps equal the intended gate times a branch phase divided
by `sqrt27`. Exact integer equalities in `Q(sqrt3,i)` certify unitarity and
the Pauli relation for every branch. An independent test composes the full
9-dimensional physical projectors and corrections and checks the Choi matrix
of each resulting channel, including coherences with an external reference.

This removes the prior1/27 postselection cost in the ideal control model.
The deterministic projective gate group is the same216-element qutrit Clifford
group. Physical Pauli control and classical feedforward are supplied resources.
This is not measurement-only universality or an experimental receiver.

An additional readout-only error calculation assumes each reported trit is
wrong independently with probability epsilon, each alternative epsilon/2.
For all three gates, the counts of outcome/report pairs that retain the ideal
logical operation with k wrong trits are `[27,0,54,0]`. Thus

`F_ent(epsilon)=(1-epsilon)^3 + epsilon^2*(1-epsilon)/2`.

The code-leak probability is epsilon because an incorrect final-code trit
aligns to an orthogonal code. The quadratic correction term reflects canceling
errors in the intermediate outcomes. Detector loss, noisy controls, actual
fault tolerance and non-Clifford resources remain unmodeled.

## 4. The tunneling sector is kagome; a tree integral bounds the leading term

On an even m-by-n torus with N=mn, two nearest ground palettes agree on one
parity class. The other `k=3N/4` sites form a4-regular kagome graph G.
For4x4 it is exactly the cuboctahedron `L(Q3)`. This connects the hypercube
through a different construction from the toroidal knight graph.

For a binary hybrid S of these two palettes, the exact face excitation cost is

`E(S)=(3/2)*|cut_G(S)|`.

A face with two active vertices contributes its cut edge; a face with three
contributes half its cut-edge count. Each active edge meets one of each type.
The native unique-quartet completion rule excludes an accidentally maximal
mixed face. The corresponding projected Hamiltonian is the ferromagnetic
transverse-field Ising form

`Hhybrid=(3/4)*sum_edges(1-Z_i Z_j)-h*sum_i X_i`.

The full120-state driver does not preserve this binary subspace; the reduction
is exact for the shortest tunneling paths, not for its complete spectrum.
Every one of the9720 palettes is replayed against the native completion table
on both tori. Exact subset dynamic programming gives

| torus | active sites / leading order | exact leading off-diagonal coefficient |
|---|---|---|
|4x4|12|19657590887/45916502400000|
|4x6|18|23259766347797390440995449137/2645785072959855023554560000000000|

The first matches the prior certificate. The second sums all18! shortest
orders through a262144-subset recurrence, using integer scaling and one final
rational reduction. An independent V8 **server-side** coordinate construction
and modular recurrence corroborate the second coefficient at primes1000000007
and1000000009. This ran while local validation used Remote Desktop Commander;
the local executors share the same physical machine, not separate extra CPUs.
The modular residues are checks, not by themselves a uniqueness proof.

There is a useful general integral representation for a connected graph with
positive edge weights w:

`c_G = integral_(t_root=0) exp(-sum_edges w_uv*|t_u-t_v|) d^(k-1)t`.

Partition relative event times by their total order and use consecutive
positive spacings. The exponent becomes `sum_j E(S_j)*spacing_j`, with unit
Jacobian. Integrating each spacing yields exactly the path denominators.
Dropping all edges outside a spanning tree increases the integral. Rooted
tree edge differences have determinant+-1, so each integral is `2/w_e`.
For the present weight3/2,

`c_G <= (4/3)^(k-1)`.

Thus the leading amplitude is bounded by
`h*(4h/3)^(3N/4-1)`, and the leading gap term by216 times that expression.
Every unlabeled tree through seven vertices is checked exactly. This is a
uniform exponential bound on the **leading term** for h<3/4, not a uniform
perturbative convergence radius or a proof of the full fixed-h thermodynamic
gap. The earlier small finite-volume isolation condition is not replaced.

There is also a decisive protection limitation: the span of the classical
ground product states has **quantum distance1**. A one-site projector has
expectation1 in one palette and0 in another. Hence `P O_site P` is not scalar,
violating Knill–Laflamme local indistinguishability. Extensive classical Hamming
separation is therefore compatible with immediate local quantum dephasing.
At h=0 a supplied symmetry-breaking field selects a palette within the ground
manifold with splitting at least `3*epsilon*N/4`; this is explicit bias, not
a proof of spontaneous thermodynamic order.

## 5. A noninvertible interface preserves exactly the free deck translations

The two non-Abelian A4-invariant bulk classes are120 and127. Their ratio is
code7, the sum of the three type-I cocycles. Define

`chi(g)=g0+g1+g2 mod2`, `H=ker chi={0,3,5,6}`.

Write `a=(x xor y,x,y)`, `b=(u xor v,u,v)` in H. The explicit cochain

`beta(a,b)=i^(x*v)*(-1)^(x*y*u+y*u*v)`

satisfies `delta beta=omega120/omega127` on all64 triples of H. It defines
the diagonal-H twisted group algebra in the folded pointed category for
`G x G`. Its underlying algebra has dimension4; its Lagrangian full center
in the folded bulk has dimension64. These are different categorical objects.

Every g outside H has ratio `omega(g,g,g)=-1`. A normalized U1 coboundary
on the cyclic subgroup generated by g has value+1 on that triple. Thus no
larger diagonal subgroup is permitted. The full native deck permutation set
is checked: H is the free translation V4, while each of the four branch
inertia elements1,2,4,7 has four fixed vertices. The interface's admissible
subgroup therefore coincides exactly with the unramified deck subgroup.

A further equivalence audit prevents overcounting. Multiplying beta by
`zeta(a,b)=(-1)^(x_a*y_b)` gives the other H2(V4,U1) choice. These are distinct
under cochain gauge alone. But ambient folded-group twisted conjugation by
`(1,0)` multiplies beta by a slant cocycle in precisely this nontrivial class.
An explicit normalized1-cochain identifies the slant/zeta ratio. Consequently
there are **six diagonal-subgroup/cochain-gauge data, but five classes after
ambient equivalence**: the two maximal-H choices become equivalent.
This is a restricted diagonal-subgroup classification, not the classification
of every subgroup of the folded group or every interface.

The two bulk topological-spin multisets differ, excluding a ribbon equivalence
and hence an invertible topological interface. The constructed gapped interface
is noninvertible. A4-invariant bulk classes and an A4-stable H do not supply
the higher coherence of an A4-equivariant interface; that remains open.
Neither bulk topological action has been derived from the strictly acting
native projector deck maps.

## Validation and remaining boundary

The validation script regenerates all six producers in three local workers,
checks frozen input hashes, and runs isolated pytest with legacy root conftest
disabled. The certificate retains actual outputs. An initial replay passed
all five producers and25 tests; one wording-only test failed and was replaced
with a substantive symbolic scale-gradient check. Early finite-field and
torus-return-contract implementation errors were repaired before certificates
were accepted. Configured guards and their failures/timeouts are recorded in
the publication audit rather than represented as universally green.

Additional executed ideas include the anomaly/mass threshold audit, readout
noise polynomial, spanning-tree integral, distance-one obstruction, independent
server modular replay, and ambient-conjugation correction. The usable progress
is constructive: an ideal deterministic receiver, an explicitly deformed locally
isolated vacuum with an algebraic effective quantum critical curve, a leading
tunneling theorem and an explicit interface. A common
physical action, experimentally selected parameters, spacetime/gravity and
global quantum vacuum remain unresolved.

Five independent next investigations:

1. Establish a volume-uniform quantum contour/remainder bound for the full120-state Hamiltonian.
2. Build A4-equivariant coherence data for the explicit translation interface and calculate its anyon transmission map.
3. Determine canonically normalized quantum masses and the domain of validity of the native29 effective critical curve.
4. Find a native non-Clifford control resource and test the deterministic receiver with physical loss and readout errors.
5. Derive the supplied stabilizing mass matrix and VEV scale from a common anomaly-free dynamical model.
