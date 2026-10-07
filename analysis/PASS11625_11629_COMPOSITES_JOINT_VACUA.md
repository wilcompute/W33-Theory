# Passes11625–11629 — actual fermion pairs, joint Hesse vacua and nonlinear controls

Reservation `90099d605`; builds on the published11620–11624 packet. These are five executed investigations in supplied models, plus the user's Reye-incidence question. They do not derive a TOE or measured masses, mixing angles, Newton's constant or the cosmological constant.

Producer: `analysis/w33_pass11625_11629_composites_joint_vacua.py`.
Certificate: `data/w33_pass11625_11629_composites_joint_vacua.json`.
Independent controls: `tests/test_w33_pass11625_11629_composites_joint_vacua.py`.

The strongest constructive result is a positive degree-six **joint** flavor/Higgs potential with a complete global-zero classification. Its12 Higgs rays are four qutrit MUBs, attached to the four existing tetrahedral flavor rays. The Reye clue yields an explicit incidence lift and an exact symmetry obstruction; it does not identify those12 rays with16 spinor components.

## Ownership and intake

The11620–11624 producer/report/certificate own the136-dimensional spinor-pair Casimir,10/126 decomposition, supplied45/126 scalar action and exact297-field tree Hessian.11600 owns the normalized Hesse doublet and its CP discriminant. BT4082 already owns conditional pair hopping `2t²/Δ`: that formula is not new.11306 is a parametrized graph, not gravity;11323 records a native lapse obstruction.11307/11324 already investigate different membrane/cap constructions.11624's graviton-loop boundary remains open.

For the Reye question, BT544 owns the concrete four-triad cyclic Reye,5580–5585 own its A4 permutation-grid realization, BT5776–BT5783 own its centered rank-nine common core,1089 owns the dual-Hesse geometry, and11262 owns the four qutrit MUB completion. Those sources were read and the results themselves searched before claiming an additional connection. The existing `w33_meeting_point_c331.py` uses432 in a different arithmetic packet; `W33_REYE_ROUTING_ROBUST_FRAMES.md` concerns one-qubit controls. Neither is the432 incidence-lift enumeration below. Equal integers do not identify the objects.

Source hashes bind the relevant older producers, certificate and reports. The inherited physical boundaries are retained; no earlier certificate is superseded.

##11625 — Pauli-allowed126 pairs, and the missing parent interaction

With a supplied two-component spin factor, the actual fermionic two-particle space is

\[
\Lambda^2(\mathbb C^2\otimes\mathbb C^{16})=
\Lambda^2\mathbb C^2\otimes\mathrm{Sym}^2\mathbb C^{16}
\oplus\mathrm{Sym}^2\mathbb C^2\otimes\Lambda^2\mathbb C^{16}.
\]

The dimensions are136+360=496. An explicit496×136 isometry embeds the spin-singlet channel, with all45 Spin(10) generator intertwiners checked and the SU(2) singlet generators annihilating it. Thus the existing10+126 symmetric internal channel is Pauli-allowed for fermions once the antisymmetric spin singlet is supplied. This is a representation map; no relativistic kinetic theory is derived.

A separate exact four-mode Fock calculation tests whether ordinary attractive hopping actually generates the older swap parent. Each site has up/down modes and single-particle costU/2; empty and paired states cost zero. In the low basis `00,p0,0p,pp`, second-order Schrieffer–Wolff gives

\[
H_{\rm eff}=\begin{pmatrix}
0&0&0&0\\0&-K&-K&0\\0&-K&-K&0\\0&0&0&0
\end{pmatrix},\qquad K=2t^2/U.
\]

The off-diagonal hopping is correct, but the mixed-occupation diagonal is **not** the ferromagnetic swap parent. It is repaired, in this polarized pair-qubit restriction, only by adding

\[
2K(n_L+n_R-2n_Ln_R),
\qquad H_{\rm repaired}=K(I-\mathrm{Swap}).
\]

That adds a chemical term and an attractive neighbor density interaction. It does not generate the entire127-color occupation parent or the126 scalar effective action. Attractive-Hubbard pair hopping/pseudospin dynamics are established prior art; see [Kitamura–Aoki](https://arxiv.org/abs/1511.07890).

An extra reduced Gauss control uses only the central Z4, pair charge2 and electric link labele∈Z4. The two vertex equations `2nL+e=0`, `2nR−e=0` leave exactly `(0,0,0)` and `(1,1,2)`. Dressed creation `B_L†B_R†U_link²` connects them; an undressed single charged pair projects to zero. This is an explicit center-only gauge constraint, not continuous Spin(10) gauge dynamics.

##11626 — field-dependent one-loop inventory and a declared shell minimum

An analytic scalar Hessian is now available at arbitraryA∈45 andS∈126. At the previous tree vacuum it reproduces the entire stored297-field Hessian. Independent direct second variations and gauge-transformed backgrounds test the general Hessian and45-vector mass Gram.

The declared bosonic benchmark has tree coefficientc=.001, gaugeg²=.001, infrared shellk=.1 andUV=.5. In a Landau-background finite Euclidean shell,

\[
V_k=V_{\rm tree}+\frac1{64\pi^2}\int_{k^2}^{\Lambda^2}
 x\left[\operatorname{Tr}_{297}\log(1+H_s/x)
 +3\operatorname{Tr}_{45}\log(1+H_v/x)\right]dx.
\]

All scalar modes, including Goldstones, enter; massless vector constants drop. Fermions are absent. This is a declared cutoff/matching scheme, not an MS effective potential or physical pole-mass calculation. Goldstone infrared resummation would need an actual matched self-energy; see [Espinosa–Konstandin](https://arxiv.org/abs/1712.08068). No fictitious positive mass is inserted.

For the three-real SM-invariant background with adjoint planes `(x,x,x,y,y)` and `S=zνν`, three distinct optimization starts converge to

\[
(x,y,z)\simeq(0.989515615,\;0.009861749,\;0.896901360).
\]

The gradient norm is below10⁻⁷; the slice Hessian eigenvalues are approximately
`0.006386115,0.009272262,0.108886358`.32/64-point shell quadrature agrees well below10⁻¹⁰. The independent closed antiderivative verifies the shell integral over all modes.

At the tree point, the smallest of264 gauge-normal tree masses squared is.002 in these units. The finite shell is smooth near this orbit, so the implicit-function theorem ensures persistence of a nearby local minimum on the **full normal quotient** for a sufficiently small formal loop coefficient. This is a local existence theorem, not an explicit bound showing the chosen coefficient1 is below that threshold. The numerical benchmark certifies the three-real slice only. Global quantum minimization, all264 quantum curvatures at the benchmark, physical masses andk→0 remain open.

##11627 — a degree-six common action with exact global minima

Letu∈C² transform by the existing normalized Hesse doubletR, andh∈C³ by the qutrit Clifford generatorsG. The explicit polynomial intertwiner is

\[
D(h)=\begin{pmatrix}
h_0^2&\sqrt2h_1h_2\\h_1^2&\sqrt2h_0h_2\\h_2^2&\sqrt2h_0h_1
\end{pmatrix},\qquad
D(Gh)=\overline G D(h)R^T.
\]

Thus `D(h) conjugate(u)` transforms byGbar. Exact symbolic Fourier/phase identities and independent mixed generator words check the common action, including HeisenbergX,Z.

With independent common U(1) phases foru andh, all parent-invariant renormalizable scalar potentials depend only on `u†u` and `h†h`. Independent commutant calculations on `u⊗h`, `Sym²h` and `Sym²u` certify this inventory. In particular there is no angular quartic. An angular mixed invariant first appears at degree6:

\[
V=(u^\dagger u-1)^2+(h^\dagger h-1)^2+
\kappa\left[(u^\dagger u)(h^\dagger h)^2-
\|D(h)\overline u\|^2\right],\qquad\kappa>0.
\]

WriteK=D†D. It is positive semidefinite and `TrK=(h†h)²`, proving the last bracket nonnegative. At unit norms, a zero requiresrankD=1 andubar in its top eigenspace. Ifh has a zero coordinate, rank1 forces a coordinate ray. Otherwise it is exactly

\[
h_0^3=h_1^3=h_2^3.
\]

Therefore there are precisely3 coordinate rays and9 equal-amplitude cube-root rays forHiggs, each paired with a determined flavor ray. These are12 joint projective minima, with two independent common-phase circles each. Theu rays form the four tetrahedral vertices, each attached to one orthogonal Higgs triad. For unit coefficients and canonical complex kinetic normalization, the exact full real Hessian has spectrum

\[
0,0,1,1,2,2,2,2,4,4.
\]

The two zeros are the supplied U(1) phases. All12 joint projective minima are one parent orbit and preserve a generalized CP; the11600 discriminantW vanishes. This constructs alignment, not the generic CP-breaking vacuum or observed flavor. Degree-six and higher angular counterterms remain allowed, and coefficients/radii are inputs. The earlier degree16 one-doublet-alone obstruction is not contradicted: this is a different joint field inventory.

## Extra — the Reye clue becomes an explicit map and a symmetry test

The12 Higgs rays have **nine maximal projective lines, each containing four rays**, with exact Eisenstein arithmetic verifying all dependencies. They are the known dual Hesse `(12_3,9_4)` configuration. The four MUB triads themselves are linearly independent. Hesse SIC/MUB geometry is prior art, as in [Stacey](https://arxiv.org/abs/1404.3774); see also repo1089 and11262.

The BT544 cyclic model is independently isomorphic to the existing A4 model: its12 points are even permutationsg of four letters and its16 lines are the grid cells `(x,y)`, withincidence `g(x)=y`. The actual point-to-permutation map is stored. Its incidence matrix hasrank10 and centeredrank9. The Levi automorphism group is576, also checked by explicit graph automorphism enumeration. This is the classical Reye structure, consistent with [Monson–Pellicer–Williams, Proposition6.1](https://bmonson.ext.unb.ca/fields/tom.pdf).

Relabel the three rays independently within each of the four MUB triads and transfer BT544's16 triples. The6⁴ labelings give **432 distinct Reye incidence lifts**:

| Property | Exact result |
|---|---|
| Lifts with3 geometrically collinear Reye triples |288 |
| Lifts with6 geometrically collinear Reye triples |144 |
| Unitary Clifford orbits |6 orbits of72 |
| Stabilizer of each lift in the216-element ray action |C3 |
| Including complex conjugation |3 orbits of144, stabilizer order3 |

The last stabilizer is in the432-element extended ray action. This enumeration is exhaustive for the within-triad BT544 family; it does not assert every possible Reye labeling belongs to that family.

There is also a general obstruction beyond that enumeration. The Fourier, phase,X,Z action on these12 rays has216 distinct faithful permutations, with every generator image verified by exact Eisenstein cross-minors. If any Reye incidence on these12 labels preserved this whole group, it would embed in its576-element automorphism group. But216 does not divide576. Thus **no Reye labeling on these12 rays can retain the entire given unitary action**.

The density matrices distinguish the geometry further. The Higgs projector Gram has spectrum `4¹,1⁸,0³`, hencecenteredrank8; the Reye centered incidence Gram hasrank9. The actual joint product projectors `ρu⊗ρh` have spectrum `2¹,(2/3)³,1⁸`, hencefullrank12. None supplies the old Reye rank-nine module by simply equating12 labels.

The stabilizer calculation has a constructive CP consequence. Its unitary and CP-extended stabilizers both have order3: **none of the216 antiunitary parent transformations fixes a lift**. The six72-element unitary orbits form three CP-conjugate pairs. This refers to the declared parent; no absence of every possible accidental CP transformation in other field inventories is asserted.

An explicit interaction now realizes that structure. Add a supplied discrete incidence fieldσ taking the432 lift values. Let `(u_i,h_i)` be the12 normalized joint vacuum representatives and define

\[
f_i(u,h)=|u_i^\dagger u|^2|h_i^\dagger h|^2,
\quad C_\sigma=\sum_{\{i,j,k\}\in\sigma}f_if_jf_k,
\quad V_\sigma=V_{11627}+\lambda\left[C_\sigma-\frac{11}{243}(u^\dagger u\,h^\dagger h)^3\right]^2,
\quad\lambda>0.
\]

The added polynomial has field degree24 and is nonnegative. At each existing vacuum, `f_i=1` at its own label, zero at the other two rays of its basis, and1/9 at the other nine labels. Counting all16 triples gives `Cσ=11/243` for every lift, checked exactly over all5184 pairs. Thus the global projective zero set is exactly432×12=5184 choices, with the original phase circles. Permutingσ and the vacuum projectors together makes the potential parent-unitary and parent-CP invariant. Four stored exact Eisenstein evaluations distinguish all432 squared-defect polynomials, so the incidence is an actual coupled label, not a decoupled spectator.

Every classical zero sector breaks all generalized CP transformations in the declared parent because itsσ has no antiunitary stabilizer. This is an **engineered CP-breaking order-parameter model**, with a new432-state discrete field and a degree24 coupling. It does not derive a continuous renormalizable Spin(10) theory, choose a unique flavor phase, prove finite-volume quantum symmetry breaking or predict CKM/PMNS phases. The16-dimensional spinor and16 Reye lines still have no identified intertwiner. The CP breaking resides in the incidence field: the existing flavor doublet still hasW=0, and no sigma-dependent Yukawa operator is supplied. The coupled classical minimum classification is exact; transmitting this incidence CP asymmetry into a physical Yukawa sector is the next question.

##11628 — a nonlinear gravity/matter bracket control

A supplied spherically symmetric spatial metric is `ds³²=L²dr²+R²dΩ²`, L,R>0, with canonical pairs `(L,pL),(R,pR),(φ,p)`. Use

\[
\begin{aligned}
H={}&A\left[-p_Lp_R/R+Lp_L^2/(2R^2)\right]\\
&+B\left[RR''/L-RR'L'/L^2+R'^2/(2L)-L/2\right]\\
&+\alpha p^2/(2LR^2)+\beta R^2\phi'^2/(2L)+C LR^2,\\
D={}&p_RR'-Lp_L'+p\phi'.
\end{aligned}
\]

With compactly supported smearings or vanishing boundary variations, exact jet-Euler calculus gives

\[
\{H[N],H[M]\}=\int\frac{NM'-MN'}{L^2}
\left[AB D_{\rm grav}+\alpha\beta D_{\rm matter}\right]dr.
\]

The other brackets are ` {D[v],D[w]}=D[vw'−wv']` and `{H[N],D[v]}=−H[vN']`. Thus the usual common Dirac structure requires **αβ=AB**; a matter-speed mismatch leaves the displayed local defect. Independent Fourier-grid functional variations check both the matched and deliberately mismatched case.

This is standard continuum spherical geometrodynamics made executable alongside the native obstruction, not a new gravity theory. See [Kuchař](https://arxiv.org/abs/gr-qc/9403003). It contains one local scalar matter pair after two constraints, and **no local gravitational-wave polarization**. It does not derive this metric/action fromW33.

An exact coarse-locality negative control is already decisive: averagingL=1,2 gives `mean(1/L²)=5/8`, while `1/mean(L)²=4/9`, a defect13/72. A coarse constraint cannot retain the inverse-metric structure through meanL alone; it needs additional subcell/correlation data. No perfect nonlinear native blocking map is claimed.

##11629 — a genuine Lorentzian flux rotor and charge-compatible topology

For a supplied compact spatial slice of volumeV and compact holonomyθ∼θ+2π, the canonical model is

\[
L=\dot\theta^2/(2Ne^2V)-NV\rho,
\quad p=\dot\theta/(Ne^2V)=m\in\mathbb Z,
\quad H=NV(\rho+e^2m^2/2).
\]

Fixed endpoint holonomy defines the canonical boundary polarization; fixed flux uses its Legendre transform. The exact Lorentzian kernel is

\[
K(\theta_f,\theta_i;T)=\frac1{2\pi}\sum_m
 e^{im(\theta_f-\theta_i)-iTV(\rho+e^2m^2/2)}.
\]

The stored−8…8 free-flux restriction is exactly unitary and composes. The membrane operator `exp(iθ)` raisesm; its finite-window shift is a partial isometry, with edge loss retained instead of artificial cyclic wrapping. On a fixed background, `ρ→ρ+C` supplies a common phase. Integrating the lapse/metric also changes the constraint byVC, so this phase alone is **not** vacuum-energy sequestering.

For an Euler-conjugate flux vectorn satisfying `a·n=−χ` at fixed topology, a membrane chargeq stays in the sector precisely when **a·q=0**. One nontrivial Euler-conjugate form has no nonzero allowed jump. A distinct vacuum form and Euler form, e.g.a=(0,1),q=(1,0), admit ordinary flux transitions while preserving the Euler sector. This is an added two-form charge inventory, not a derived selection mechanism;θ/m are not the earlier rigid Euler multiplier.

The flat thin-wall bounce is checked exactly:

\[
S(R)=2\pi^2\tau R^3-\frac{\pi^2}2\Delta\rho R^4,
\quad R_*=3\tau/\Delta\rho,
\quad B=27\pi^2\tau^4/(2\Delta\rho^3),
\]

with negative radial curvature `−18π²τ²/Δρ` and `Δρ=e²(m−1/2)` for loweringm. This is the standard Brown–Teitelboim mechanism, discussed in [Hirano](https://arxiv.org/abs/1804.09985). Gravitational bounce backreaction and rates are not computed. Nothing here removes the11624 graviton terms `a1 M⁶/(2K)+a2 M⁸/K²` or selects a measured cosmological constant.

## Reproduction

```bash
OPENBLAS_NUM_THREADS=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest --noconftest -q tests/test_w33_pass11625_11629_composites_joint_vacua.py
OPENBLAS_NUM_THREADS=1 python3 analysis/w33_pass11625_11629_composites_joint_vacua.py
```

There are29 independent regression controls. The CI validates the committed certificate before regenerating the five sections plus the Reye audit. An initial run found a Sympy expanded-versus-factored equality in one test; the assertion now checks an exactly simplified zero difference. This was a representation issue, not a changed energy law. Continuity logs document each deliberate change.

## User literature leads — Reye contextuality, Witting and the coherent resource

The additional producer `analysis/w33_reye_witting_context_resource_audit.py` and its source-bound JSON turn both user-provided literature leads into concrete controls. Six independent tests are in `tests/test_w33_reye_witting_context_resource_audit.py`, making35 controls across the packet.

The Reye paper is [P.K. Aravind, *How Reye's configuration helps in proving the Bell–Kochen–Specker theorem: a curious geometrical tale*](https://users.wpi.edu/~paravind/Publications/REYE.pdf). The relevant construction uses **two** Reye configurations in four-dimensional ray space. Reconstructing the dual24-cell rays gives24 rays and24 orthogonal tetrads. For each of16 Reye lines in one half, its orthogonal mate in the other half can be deleted. The surviving18 rays lie in9 complete tetrads, with each ray appearing twice: an exactly-one assignment would count an odd number through the9 contexts and an even number through the18 rays. This reproduces the classical parity proof, not a new KS theorem. All16 such witnesses and all288 single-deletion colorings are stored.

The same producer supplies exact **adaptive Pauli measurement trees for all24 Peres contexts**. First measure a two-qubit Pauli with two rays in each outcome branch; then measure the appropriate commuting branch Pauli. The resulting rank-one projectors equal the ray projectors exactly. Thus this KS proof is compatible with stabilizer preparations and adaptive Pauli measurements. Measurement contextuality alone does not imply a coherent non-Clifford gate. The doily's sign/selection distinction is prior repo work; its historical contextual-fraction wording is not imported. BT1408/Pass1086 already state the corrected statistic boundaries.

The communications paper is [Alexander Yu. Vlasov, *Scheme of quantum communications based on Witting polytope*, arXiv:2503.18431](https://arxiv.org/html/2503.18431v1). Its coordinate realization and overlapping tetrads are reused; BT1408/BT1411 already own the communication/analyzer interface, and Pass4963 owns the exact graph identification. The useful connection to this packet is **objectwise**:

\[
h\longmapsto(h_0,h_1,h_2,0).
\]

This is an isometryC³→C⁴. The12 selected Higgs rays are exactly the12 Witting rays orthogonal to the coordinate raye3. Their four MUB triples complete with e3 to the four tetrads through it. The stored map composes this embedding with a Witting-to-F₃⁴ point labeling; every one of780 ray pairs is checked against the symplectic commutation relation. The full orthogonality graph has parameters `(40,12,2,4)` and240 edges. This corroborates the user's identification with the W33 point geometry without relying on the parameters alone.

The representations still differ: Witting rank-one projectors act onC⁴; the same finite points label projective two-qutrit Pauli operator classes onC⁹. The graph map is not a unitary map between those Hilbert spaces. The12-ray local link admits81 exactly-one colorings, one ray from each of four disjoint bases; KS uncolorability requires the larger overlapping context structure.

Vlasov's Eq7 also specifies a **coherent delayed query**,

\[
T_P=P\otimes X+(I-P)\otimes I.
\]

For `P=|11><11|` this is exactly Toffoli. More generally, for any rank-one ququartP,

\[
T_P(I\otimes Z)T_P^\dagger=(I-2P)\otimes Z,
\qquad\operatorname{Tr}(I-2P)=2.
\]

A two-qubit Pauli has trace0, or±4 for the scalar identity. Consequently the query cannot be a Clifford gate in the fixed two-data-qubit plus ancillary-qubit encoding, regardless of which rank-one ray is queried. This rank/trace proof avoids gate-fidelity or tolerance criteria. Separate computationalZ measurements destroy coherences inside the three-dimensional complement ofP; an exact binary Lüders query retains them. Acquiring a destructive yes/no statistic therefore does not certify the coherent gate.

If the computational-ray query is supplied as an actual coherent gate on arbitrary inputs, together with Clifford controls, the known Toffoli/Hadamard universality result applies with its ancillary/real-state conventions; see [Aharonov](https://arxiv.org/abs/quant-ph/0301040). This identifies a precise resource requirement. The paper's operation and the universality theorem are established prior art. No W33 Hamiltonian, physical interaction, error budget or universal device implementing that resource is derived here.

Finally, **Reye incidence itself does not force CP breaking**. The Peres realization is real and invariant under ordinary complex conjugation, yet is KS-contextual. The432-lift model above breaks the declared parent CP because of its specific complex embedding and added incidence field; its retained local Higgs MUB link is KS-colorable. CP asymmetry, contextuality and coherent universality are different properties, and the explicit maps now tell us where each enters.
