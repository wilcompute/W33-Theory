# Nine native investigations: topology, cubic actions, dynamics and networks

This continuation executes the five investigations following
`2026-11-02_native_knight_clifford_cover_bridge.md`, then follows the results
into twisted quantum doubles, network-capacity auditing and a recent
entanglement-to-geometry proposal, then audits the actual orthogonal group
following the user's further steering. Nine producers provide explicit maps and
certificates. They establish finite mathematics and declared quantum models;
they do not establish a complete physical TOE.

## Results and provenance

| Investigation | Verified result | Producer stem after `w33_20261102_` |
|---|---|---|
| Cover symmetry | Regular C2³ deck group; four meridians 1,2,4,7 | `deck_monodromy_network` |
| Same native cubic, changed action | Explicit nonmonomial27 action of the46080 linear Clifford group | `clifford_native_cubic_repair` |
| Preserve the old local action | Explicit324-coordinate induced cubic carrier and common cover of order46080·2^60 | `induced_cubic_common_cover` |
| Declared quantum dynamics | Exact256-dimensional quartet Hamiltonian; second/third-order effective operators | `quantized_native_tetrahedron` |
| Real structures and circuits | Five signature cases, antiunitary obstruction, optimal1-CNOT and8-CNOT realizations | `real_clifford_gate_synthesis` |
| Deck-group quantum topology | Supplied type-III twist:22 anyons, dimension-squared64, explicit CCZ resource | `deck_twisted_quantum_double` |
| Bell-resource capacity | Single Q4 serves at most6 of8 antipodal requests; constructive6 and capacity-two8 routes | `hypercube_switch_capacity` |
| Information geometry audit | Full-rank, positive-MI counterexample to a proposed metric implication | `entanglement_metric_axiom_audit` |
| Actual orthogonal image | Signed rotational B6 group, not the equal-order W(D6) | `spin6_rotation_group_audit` |

Each stem names an `analysis/*.py` producer and corresponding `data/*.json`
certificate. `w33_20261102_extended_native_validation.py` replays all nine,
then the new tests and21 connected prior tests. The independent tests are in
`tests/test_w33_20261102_six_native_fronts.py`; its historical filename now
covers the additional investigations too.

The latest parallel report
`PASS12518_12525_HYPEROVAL_FLOOR_HESSE_DICTIONARY.md` was read in full. Its
explicit Hesse SIC/MUB maps, B4 point-stabilizer identification and convention
correction are distinct results. This packet does not claim those maps or
replace its CP-SAT proof status with an independently checked proof.

Existing hypercube networking is substantial. In particular,
`BT3308_BT3319_knight_hypercube_gauge_closure.md` already supplies a typed
controller, exact routing dilation/congestion bounds and a two-board Q5
interpretation. The May29 Clifford/Pascal/knight report owns that basic
identification. These are reused, not rediscovered. Earlier numerical
coincidence language in `w33_BREAKTHROUGH_282_hypercube_interconnect_network.py`
is not used as a proof of spacetime or hardware performance.

## 1. The native cover is a regular C2³ cover

On the existing Z4² triangulation, the eight maps are

```
(x,y) -> (-1)^e (x,y)+(2a,2b),   e,a,b in F2.
```

Every map preserves all oriented faces and all actual native projector labels.
All have order dividing two and commute. A deck map is determined by its image
on one base triangle; that triangle has exactly eight preimages. The eight
constructed maps therefore exhaust the deck group. Independent colored-graph
automorphism enumeration also tests exhaustiveness, retaining only maps of
the oriented face set.

The producer transports sheets along the **dual edges**, rather than assigning
monodromy by count. Four based loops around the tetrahedron's target vertices
give four commuting fixed-point-free involutions of eight sheets. Each has
cycle type2^4, their product is identity, and the first three freely generate
C2³. In the exported address basis they are **1,2,4,7**.

Every source vertex has stabilizer order two. This is the earlier degree-eight
cover with16 simple ramification points, not an unbranched eightfold torus
cover. The translation subgroup gives the familiar factorization through an
unbranched fourfold torus quotient followed by a branched double cover of a
sphere, the pillowcase construction. Intermediate quotient cells need not
form an abstract simplicial complex: multiple edges can occur.

## 2. The triangulated carrier is the Shrikhande graph

The literal edge set is the Cayley graph on Z4² with steps
±(1,0), ±(0,1), ±(1,1). This is the standard Shrikhande graph, with

```
A²=4I+2J, spectrum 6^1,2^6,(-2)^9.
```

All32 graph triangles are exactly the chosen torus faces. This identifies the
native covering carrier with an established graph, not a new SRG.

Pass75 (`w33_pass75_zeta_equidistribution.py`) already owns the Shrikhande/rook
cospectral comparison and the link distinction C6 versus two disjoint K3s;
Pass76 reuses it. Pass4762 identifies **rook** grids inside a different W33
construction. Here exact chain matrices add the carrier comparison:

| Two-dimensional complex | V,E,F | Rational Betti numbers |
|---|---|---|
| Shrikhande's32 triangle faces | 16,48,32 | 1,2,1 |
| Rook graph's triangle2-skeleton | 16,48,32 | 1,9,8 |

The rook graph's **full** clique complex also has eight tetrahedra; the table
deliberately compares two-dimensional complexes. Equal adjacency spectra,
cell counts and local degrees do not select a surface topology.

There is also an operational difference between the cube routing subgraph
and its triangular thickening. Let G be the ordinary grid adjacency, K the
knight adjacency and D the diagonal adjacency. At the stipulated time π/2:

```
exp(-i*pi*G/2)=exp(-i*pi*K/2)=C,
exp(-i*pi*(G+D)/2)=-I,
exp(-i*pi*(G+2D)/2)=C,
```

where C sends `(x,y)` to `(x+2,y+2)`. Thus equal diagonal weights turn
antipodal perfect transfer into a revival. **Doubling the diagonal coupling
repairs transfer without deleting the triangular surface edges.** More
generally even integer diagonal weights give C and odd integer weights give
−I at that time.

For equal weights there is no vertex-to-vertex perfect state transfer at
*any* time. The exact eigenprojector P2 has diagonal3/8 and off-diagonal±1/8,
excluding strong cospectrality of distinct vertices. With z=exp(−4it), the
adjacent transition amplitude is exp(2it)(z−1)(z+3)/16 and the nonadjacent one
is exp(2it)(z−1)²/16. Their maximum probabilities are **1/12 and1/16**.
These are ideal single-excitation Hamiltonians with chosen coupling units,
not an experiment or a quantum-switch universality theorem.

## 3. Two explicit repairs of the representation problem

The old signed27 module and the spinor4 module already require a61440 common
cover. The old signed module cannot simply be regarded as a representation
of the spinor1920 quotient: the previously exported kernel acts nontrivially.
This packet supplies a concrete word whose spinor matrix is I4 but whose
old signed27 trace is **3**. Any action factoring through that spinor matrix
has trace27 on the same word. No basis change removes the mismatch.

For prescribed **support-permutation** maps factoring through projective
Clifford, there is another obstruction. Its Pauli16 subgroup is contained in
the old960, and its centralizer in the enlarged11520 is precisely Pauli16.
A normal kernel disjoint from old960 would centralize Pauli16 and hence be
trivial. The extension would therefore have to be injective into the native
support automorphism group, of order51840, but11520 does not divide51840.
This excludes that specified class of extensions. It is not a no-go for all
larger common covers or all nonmonomial cubic actions.

### Repair A: retain27 coordinates and change the embedding

Use the standard SL6 model

```
C(A,u,v)=Pf(A)+u^T A v,
A in Lambda²(C6), u,v in dual(C6).
```

The repo already has exact Pfaffian/E6 coordinate restrictions in
`w33_pfaffian_doily_e6_cubic_bridge.py` and all36 sections in
`w33_all36_pfaffian_double_six_sections.py`. The standard representation
theory also predates this work; see [Manivel, Configurations of lines and
models of Lie algebras](https://arxiv.org/abs/math/0507118).

The new certificate identifies **all45 signed terms** with the current
signed native cubic by an explicit coordinate permutation and signs. For an
actual spinor U, let B=diag(U,I2), then act by

```
A -> B A B^T, u -> B^(-T) u, v -> B^(-T) v.
```

The producer checks exact polynomial equality, in native coordinates, for
each of the six old generators and the new gate. Independent tests transform
every entry of the polarized27×27×27 tensor. The enlarged linear group has
order**46080**: its projective image is11520, determinant restricts the
scalar kernel to μ4, and the exported old word for P together with U²=iP
exhibits iI. All four scalars therefore occur.

The Lambda²(C4) component has dimension six and carries the invariant
`chi^T J (psi wedge eta)`, with the explicit symmetric epsilon pairing J.
This is a concrete covariant replacement for a single fixed symplectic
bilinear. It sits inside the new27 action. It does not make the new action
equivalent to the old signed27 action, or select a physical Yukawa coupling.

### Repair B: retain the old local action and enlarge the carrier

The index of old projective960 in11520 is twelve. The producer constructs an
explicit Schreier transversal and twelve27-coordinate blocks. Each enlarged
generator permutes blocks, applying an actual old signed-cubic symmetry
inside each block. The sum of the twelve native cubics is invariant.

On reference block0, all six old generators restrict **exactly** to the old
signed27 generators, paired with the original spinor matrices. Thus the old
coupled action is recovered on this block of its stabilizer. This repairs
the compatibility problem by using a324-coordinate global scalar carrier;
it does not supply an unchanged global27 representation.

The group order is computed, not guessed. All69,121 non-tree Cayley relations
over11520 projective states are reduced to diagonal signs and scalar μ4
phases. Binary elimination gives the full **60-dimensional sign kernel**;
the paired kernel over projective Clifford has order2^62. Consequently the
constructed common cover has order

```
46080 * 2^60 = 53126622932283508654080.
```

The independent relation witnesses are rechecked modulo17, separately from
the producer's characteristic1009 computation. Exact projective covariance
and determinant one restrict each scalar ratio to μ4, so its injective
finite-field image determines it exactly. This is a finite construction,
**not a minimality claim**. Its large independent kernel makes compression a
substantive next question. The twelve algebraic cosets are not the eight
sheets of the surface covering; the dimension324 also is not an identification
with the earlier KO6 construction.

## 4. A declared quantum chiral model and its controlled tunneling

Freeze one actual native quartet and use its four labels as a supplied
ququart basis at each site. Let H0 count oriented faces that fail the actual
native positive-completion rule. Add the specified local driver

```
H(h)=H0-h sum_v A(K4)_v.
```

This is a new model choice, not a quantization uniquely forced by the
projectors. On the tetrahedral surface the full Hilbert dimension is256.
There are twelve classical zero-energy states. The exact effective operator
on those states has second-order coefficient −4I12. Its third-order
coefficient has spectrum

```
(-8)^1, (-8/3)^9, 0^2.
```

Thus E0=−4h²−8h³+O(h⁴), and the first gap is
`(16/3)h³+O(h⁴)`. Direct eigensolutions at five h values include residuals,
ground-sector weights and single-site entropies. At h=.01 the energy is
approximately−0.00040824648 and the gap5.55284e−6.

For any finite number of sites and h>0, the configuration graph of single-site
K4 changes is connected and all off-diagonal Hamiltonian entries are
nonpositive. Perron–Frobenius therefore gives a unique positive finite-volume
ground state for this declared model. This is not a proof of a thermodynamic
gap or a selected cosmological vacuum.

On the16-site native torus, the twelve quartet-sector classical ground
colorings have pairwise Hamming distances12 or16. Consequently a single-site
driver cannot connect distinct such states before perturbative order12.
This is a **first-possible-order bound**, not a computed nonzero order12
amplitude or proof of topological protection. Diagonal energy selection
between all810 native quartets and the full120-level quantum problem remain
outside this restricted-sector calculation.

## 5. Real signatures and two different circuit costs

The actual gamma matrices give the following real-algebra structures with p
positive and q negative generator squares:

| p,q | Real algebra | Commuting antiunitary square | Minimum real module |
|---|---|---:|---:|
| 4,0 | Mat2(H) | −1 | 8 |
| 3,1 | Mat4(R) | +1 | 4 |
| 2,2 | Mat4(R) | +1 | 4 |
| 1,3 | Mat2(H) | −1 | 8 |
| 0,4 | Mat2(H) | −1 | 8 |

This is standard Clifford classification, checked on the fixed matrices; see
[Canonical bases for real representations of Clifford algebras](https://arxiv.org/abs/math-ph/0401014).
The binomial grade row does not select a signature. The old unitary subgroup
has a quaternionic antiunitary, but the enlarged group has no commuting
antiunitary on C4. Its explicit iI already forbids one by antilinearity.
The supplied doubled representation U⊕U* has the usual realification. This
constrains an unchanged Majorana interpretation; it does not rule out complex
internal matter or provide a physical Lorentz action.

In the fixed basis, P=−Y⊗Y and U=exp(−iπY⊗Y/4). An exhaustive weighted
Clifford search exhibits an ideal circuit with **one CNOT** and eight local
H/S gates. Entanglement of U|00> proves a local-only circuit impossible.

The same unsigned mask map, implemented as a permutation of the computational
basis of **four** qubits, instead needs **eight CNOTs** in the all-to-all
CNOT-only model. A full GL4(2) BFS produces the circuit; independent
forward-radius3 and backward-radius4 searches exclude every circuit of at
most seven gates. The16 blades label operators of the two-qubit spinor;
they are not sixteen spinor amplitudes. These are distinct hardware tasks.

## 6. From actual deck holonomy to a supplied twisted quantum double

Take the certified deck group C2³ as a possible gauge group. Untwisted
D(C2³) has64 Abelian sectors. The supplied normalized cocycle

```
omega(a,b,c)=(-1)^(a0*b1*c2)
```

satisfies all4096 cocycle equations. The slant cocycle in flux g is
`alpha_g(x,y)=omega(g,x,y)omega(x,y,g)/omega(x,g,y)`.
The zero-flux twisted group algebra has eight1-dimensional irreducibles.
Each nonzero flux has radical{0,g}; its two central blocks are M2(C).
This gives **eight dimension-one and fourteen dimension-two anyons**, with
dimension-squared64 and spin multiplicities `(1,-1,i,-i)=(14,6,1,1)`.
These are established type-III data, not new anyon theory; compare the
[published twisted-double classification](https://link.aps.org/accepted/10.1103/PhysRevB.91.035134).
The repo's `w33_anyons_from_2T.py` concerns a different gauge group.

An independent closed-manifold check evaluates the cocycle on T³: among512
triples,344 contribute+1 and168 contribute−1. Dividing by the gauge-group
order gives **Z(T³)=22=dim H(T²)**. This dimension distinction matters;
one must not substitute a two-dimensional gauge-theory class count for a
three-dimensional quantum-double torus state space.

The local phase is literally CCZ on the selected three binary components.
The exact witness `CCZ X0 CCZ = X0 CZ12` excludes a Pauli image. The normalized
Pauli fourth moment of CCZ|+++> is11/32. Thus the chosen twist includes an
explicit non-Clifford phase resource, unlike the previous added Clifford
gate. It is supplied, not derived from native dynamics.

Recent work on [Clifford-hierarchy stabilizers and twisted quantum doubles](https://arxiv.org/abs/2610.00464)
gives a relevant framework for separating stabilizer levels, preparation
phases and code-switching resources. Its stated type-III realization result
for odd primes should not be silently substituted for our qubit case.
Moreover, [Etingof, Rowell and Witherspoon](https://arxiv.org/abs/math/0703274)
prove finite braid images for twisted finite-group doubles. Non-Abelian
sectors here therefore do not establish braid-only universality, a gapped
native phase or3+1D gravity.

## 7. A concrete limit on a recent network-switch claim

[Universal Nested Quantum Switch](https://arxiv.org/html/2603.00236v1),
submitted February2026, distinguishes a degree-(2d−1) nested resource from
its degree-d hypercube subgraph. Its Theorem1 states universality restricted
to one hypercube layer; the proof discusses odd d and then invokes two copies
for arbitrary d. That single-layer restriction fails at d=4.

For k edge-disjoint antipodal paths in Q4, at least4k edges are used. At each
of the2k terminals the used degree is odd, hence at most3; at the other
vertices it is at most4. At most32−k edges can be used, so **5k≤32** and
**k≤6**. An explicit six-path witness attains the bound. Eight explicit paths
work with two Bell pairs per edge, with maximum load two.

This does not refute the paper's larger nested graph or two-layer provision.
It prevents importing single-layer universality into our16-node router from
a graph-name match. Independent Bell swapping resources also differ from
the coherent single-excitation perfect-transfer Hamiltonian in section2.

## 8. Testing a recent entanglement-to-geometry implication

The July2026 proposal [Quantum Gravity from Fractal Entanglement Geometry](https://arxiv.org/html/2607.26035v1)
section2 claims that strong subadditivity guarantees a metric triangle
inequality for raw distances `d(A,B)=-log(I(A:B)/I0)`. A four-qubit
counterexample tests this implication without adopting or rejecting every
other part of that research program.

Partition the qubits as A={0}, B={1,2}, C={3}. Let psi be a product of Bell
pairs01 and23, and let GHZ be the four-qubit GHZ state. Use the rational matrix

```
rho = (89/100)|psi><psi|+(1/100)|GHZ><GHZ|+I16/160.
```

It is full rank since rho≥I/160. All three pairwise mutual informations are
strictly positive, so the distances are finite. Partial traces give
`I(A:B)=I(B:C)≈1.01998874` nats and `I(A:C)≈0.0000500008334` nats. Strong
subadditivity holds. Nevertheless, for I0=4ln2,

```
d(A,C)-d(A,B)-d(B,C) ≈ 8.92327262 > 0.
```

The certificate gives the exact rational density matrix and exact AC marginal;
independent tensor partial traces and high-precision logarithms verify it.
A shortest-path closure can supply a metric, but changes the raw pairwise
distance and adds a construction. Additional restrictions or a different
information distance are needed before this implication can support a
continuum geometry. No Lorentzian metric or Einstein equation follows from
this finite audit alone.

## 9. The actual six-dimensional group is not W(D6)

A further server-side exact enumeration suggested a useful false lead to
test: two groups of order23040 need not be the same. The producer now builds
the actual intertwiner from our spinor matrices. The six skew forms are
`i Omega, gamma_1 Omega,...,gamma_5 Omega`; they have Gram matrix4I and
transform by `B -> U B U^T`. Each old generator and the new gate act by an
explicit real signed permutation matrix of determinant+1.

Their closure is all23040 determinant-one signed6×6 permutations, the
rotational hyperoctahedral group. It has **631 involutions**. W(D6) instead
requires an even number of sign flips, independent of permutation parity,
and has **751 involutions**. The complete element-order histograms differ,
so the groups are not isomorphic. Independent direct involution enumeration
and the literal matrix intertwiner are tested.

The exact chain is therefore linear Clifford46080, then its six-form image
23040 with kernel±I4, then the projective quotient11520. The scalar iI4 maps
to−I6. This is the standard internal Spin6/SU4 relation realized on the actual
matrices, not a six-dimensional spacetime or an E7/E8 embedding. The older
`w33_exceptional_weyl_trident.py` gives correct group-order arithmetic for
W(D6); that arithmetic does not identify it with this representation image.

## Boundaries and next investigations

The native surface geometry is still externally specified. The quartet
quantization, gauge theory, cocycle and network couplings are explicit model
choices. The native two-qutrit projector Hilbert space, the internal spinor4,
the supplied ququart site basis and the sixteen-dimensional blade space
remain different carriers. Only the maps actually constructed here connect
them. The complete past-week commit audit and full215-page PDF reading remain
unfinished; neither is claimed completed by this packet.

Five independent investigations follow: compress the induced common cover;
establish thermodynamic quantum phases; derive or exclude a native cocycle
selection mechanism; test resource-aware networks under calibrated noise;
construct a state-restricted information metric with a controlled continuum
limit.
