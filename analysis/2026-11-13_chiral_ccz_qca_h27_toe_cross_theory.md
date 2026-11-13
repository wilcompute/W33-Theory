# November 13, 2026 — independent cross-theory research: the chiral cone gate is one qutrit CCZ

**Status:** a new exact circuit classification and reproducible algebraic compatibility/causality/entanglement audits, NOT a complete physical theory or experimental TOE. This follows the pushed parent commit b2a1c15f48d49fdd3fe6283b1c9f721d02e12482.

## Repository-search and novelty ledger

The investigation used multiple independent passes over the current master: cubic/Clifford/CCZ gate scripts; causal-set/automata/continuum scripts; holographic error-correction code implementations; Heisenberg and E6 cubic connections; five-qubit Pauli-MUB exhaustive-rank codes. Important parents:
- analysis/toe_20261113_chiral_null_order3_gate.py and _chiral_null_wigner_magic.py — already prove exact rational order-3 U, non-Clifford Wigner magic, three-qutrit rank profile 3/2/3; not new here.
- analysis/w33_20261108_null_orbit_chirality.py, analysis/w33_20260924_null_history_spectral_clock.py and Pass11549 — already know 27 rank-one cone and positive/negative orbit split.
- analysis/w33_20261010_toe41_e6_45_ccz_compiler.py — already compiles the **distinct 27-coordinate E6 cubic** as 45 commuting CCZ terms, not the present 27-dimensional **single three-qutrit clock gate**.
- analysis/w33_pass10941_qutrit_universal_instruction_bridge.py — already has qutrit Clifford/T ports, with honest magic-state requirements; no assumption of free non-Clifford resources.
- analysis/toe_20261105_causal_poset_measure_correction.py and analysis/2026_11_03_causal_set_dimension_nulls.py — already test poset measures/dimensions; the present four-microstep unrolling is a different construction.
- analysis/w33_e6_cubic_diagonal_phase_weld.py and analysis/w33_pass10975_e6_cubic_reynolds_clock_weld.py — establish H27 phase normal form and four six-point E6 fibres; the nine-state partial commuting bridge here should not be mistaken for their full E6 cubic weld.
- Pass12649–12653, analysis/w33_five_qubit_size8_dlx.py and analysis/w33_five_qubit_floor24.py — eight five-qubit bases remain unresolved; no negative proof is claimed.

## Exact theorem: one Clifford-conjugated CCZ is the entire 27-state clock

Let D=T-T^T be the oriented Cayley matrix on Sym2(F3), with four forward null steps 100,001,111,121 and U=(18I+3D+D²)/18.

In Fourier coordinates k=(a,b,c), U has diagonal eigenvalue omega^(f(k)), omega=e^(2pi i/3). Direct finite-field character evaluation gives f(k)=0 for 19 k, +1 for four and -1 for four. The unique polynomial representing f as a function on F3³ is

\[
f(a,b,c)=(a+c)(1-ac-b^2).
\]

In F3 the Frobenius identity (a+c)^3=a+c implies

\[
\boxed{f(a,b,c)=(a+c)(a-c-b)(a-c+b)}.
\]

The linear transformation

\[
L=\begin{pmatrix}1&0&1\\1&-1&-1\\1&1&-1\end{pmatrix}
\pmod3
\]

has determinant 1 in F3. Define P_L|k>=|Lk>, F[x,k]=omega^(k dot x)/sqrt(27), CCZ|u,v,w>=omega^(uvw)|u,v,w>. Then

\[
\boxed{U=F P_L^\dagger CCZ P_L F^\dagger.}
\]

The proof certificate computes all 27 Fourier eigenvalues in Z[omega], using the exact relation omega²=-1-omega and the integer matrix M=9U; no numerical eigenvalue fitting occurs. A separate complex-matrix reconstruction agrees to <5e-16. Every single-coordinate finite difference of f is quadratic, giving U in level three of the qutrit Clifford hierarchy. A genuine cubic term shows U is not Clifford. One CCZ is therefore both sufficient and resource-count optimal when arbitrary Clifford circuits are free (zero CCZ would be Clifford). This **does not** imply minimal total optical cost, fault-tolerant transversality, hardware feasibility, or universality by U alone.

The factorization provides an exact, unambiguous **trilinear phase**. It invites comparison with twisted finite gauge theories/group-cohomology cup products; it does NOT by itself construct a topological action, a 3-cocycle on group-valued spacetime cochains, anomaly cancellation or a chiral Standard Model.

## Microcausal two-layer distinction: spatially cyclic clock, acyclic computation

The internal Cayley graph has directed cycles: q repetitions of a nonzero displacement return to the same finite-field site. Thus its edge relation is not a causal partial order. A physical causal-set candidate cannot simply use that relation.

Each of the four commuting factors exp[t(T_v-T_v^-1)] has support on just x,x+v,x-v for every x. If these factors are **scheduled sequentially** in four strictly advancing temporal slices, the reachable spatial support from one history grows 1->3->9->27->27. The five-layer DAG has 135 layer-labelled events and 324 forward interlayer arrows, no directed temporal cycles. The composed circuit equals the exact U (numerical error bounded in the producer). This reconciles finite internal clock reversibility with causal ordering of *operations*, conditional on an externally chosen schedule. There is NO preferred time direction, proper Lorentz cone, gravity or spontaneous causal growth derived here.

The relevant literature separates these assumptions: D'Ariano/Perinotti's QCA explicitly imposes local homogeneous unitary updates and derives an IR Dirac regime on an appropriate unbounded lattice; Surya's causal-set review requires a locally finite **partial order**. Our finite gate is neither a substitute for a QCA continuum nor a causal set by itself.

## Entanglement versus holographic perfect-tensor requirements

For the pure state U|000>, exact integer Gram matrices give reduced densities (each numerator divided by nine)

\[
\rho_A=\rho_C=\frac19\begin{pmatrix}4&-1&1\\-1&2&0\\1&0&3\end{pmatrix},\qquad
\rho_B=\frac19\begin{pmatrix}5&-1&-1\\-1&2&2\\-1&2&2\end{pmatrix}.
\]

Single-qutrit purities are (11/27,5/9,11/27), Schmidt ranks (3,2,3); none equals I/3. The output is therefore not an absolutely maximally entangled three-party state / 1-uniform three-leg tensor. For any **pure three-party state**, tripartite information I3 is identically zero, so this particular output does not nontrivially test a holographic negative-tripartite-information criterion. This does NOT disprove holographic coding using this gate plus ancillary modes, nor test six-leg Choi tensor perfection.

Cree et al. 2021 prove severe transversal non-Clifford restrictions for **certain holographic stabilizer codes under specified correctability/locality assumptions**. Since U is Clifford-conjugate to CCZ, implementing it as a protected logical gate will require a protocol consistent with these restrictions, such as magic-state injection or suitable code switching; we have **not** proved that any particular W33 code satisfies the relevant hypotheses.

## E6/H27 partial commuting bridge: order nine, not 27

The current Heisenberg normal form is (a,b,c)(A,B,C)=(a+A,b+B,c+C-bA). Set v=c+ab. For right action,

\[
(a,b,v)(A,B,C)=(a+A,b+B,v+C+aB+AB).
\]

When B=0, the last coordinate is translated by C, and the nine-member subgroup H0={(A,0,C)} acts by standard commuting translations on each of three b-labelled fibres. All 729 right actions were checked exactly. The center contains three elements, and each of 24 noncentral elements has a centralizer of size nine. There are exactly four maximal abelian subgroups of order nine, all meeting in the center. Hence no full faithful commuting 27-translation subgroup can be contained in H27.

This is a maximal **partial** equivariance result, not a signed E6 cubic automorphism nor an E6 mass/Yukawa calculation. It repairs the earlier mistaken hope of simply equating the two 27-element carriers.

## Five-qubit 8-versus-9 maximal Pauli MUB frontier

Rechecked the already certified nine-basis seven-matrix witness, whose code indices are 980,30085,20322,22520,4690,21838,7411. Exhaustive five-by-five binary symmetric matrix enumeration gives 13,888 nonsingular candidates; no candidate extends the full nine-set. For each of its seven single deletions (leaving an eight-set with the two fixed Lagrangians), the numbers of candidate extensions are exactly 40,36,40,36,40,40,44, respectively. These punctures are not maximal, even though their parent is. This is a bounded exact witness-family census, **not** an exhaustive exclusion of all eight-sets. The prior eight-set DLX attempt explored 4.31 million nodes, timed out on all eight stabilizer orbits, and remains undecided. The minimum known interval is still 8 or 9.

## External research compared, without conflating mathematical models

- D'Ariano & Perinotti (2014), *Derivation of the Dirac Equation from Principles of Information Processing*, Phys Rev A 90 062106: https://doi.org/10.1103/PhysRevA.90.062106 . Key missing W33 ingredient: Lorentz-compatible long-wavelength dispersion on an extensible local lattice.
- Sumati Surya (2019), *The causal set approach to quantum gravity*, Living Rev Relativ 22 article 5: https://doi.org/10.1007/s41114-019-0023-1 . Missing ingredient: partial-order growth and an action/measure; directed internal clock cycles are not enough.
- S Carlip (2024), *Causal sets and an emerging continuum*: https://doi.org/10.1007/s10714-024-03281-1 . Even random causal sets face manifold-likeness selection.
- Pastawski, Yoshida, Harlow, Preskill (2015), HaPPY holographic QECC, JHEP 06(2015)149: https://doi.org/10.1007/JHEP06(2015)149 . Missing ingredient: a tensor-network encoder with verified correctability, geometry and entanglement structure.
- Cree, Dolev, Calvera, Williamson (2021), fault-tolerant holographic gates: https://doi.org/10.1103/PRXQuantum.2.030337 . Non-Clifford gates cannot be assumed transversal under their hypotheses.
- Jacobson (2016), entanglement equilibrium and Einstein equation, Phys Rev Lett 116 201101: https://doi.org/10.1103/PhysRevLett.116.201101 . Missing ingredient: horizon area/entropy variation, metric, energy tensor; three-qutrit output entropy is not Einstein gravity.
- Lorentzian Barrett-Crane group-field-theory condensate cosmology (2022): https://doi.org/10.1088/1475-7516/2022/01/050 . Missing W33 ingredient: many-body continuum phase and relational dynamical observables.
- 2026 *Clifford Hierarchy Stabilizer Codes: Transversal Non-Clifford Gates and Magic States*: https://doi.org/10.1103/j2q4-bnc6 . Twisted finite gauge theory demonstrates what a genuine topological/cup-product framework needs; the CCZ polynomial is only a candidate algebraic input.

## Executable sources and strict scope

- analysis/toe_20261113_ccz_clifford_normalform.py
- analysis/toe_20261113_h27_maximal_translation_bridge.py
- analysis/toe_20261113_clock_causal_holographic_firewall.py
- analysis/toe_20261113_mub_nine_puncture_census.py
- tests/test_toe_20261113_ccz_causal_h27.py
- Corresponding structured outputs under data/toe_20261113_*.json

**Top five independent follow-ups:** (1) experimentally viable qutrit CCZ synthesis/measurement and per-gate error models; (2) signed E6-cubic-preserving dynamics on maximal commuting H27 nine-sectors and their cocycle gluing; (3) causal-set/Dirac-QCA continuum derived without imposing a background geometry; (4) a genuine holographic QECC with confirmed complementary recovery plus nontransversal CCZ gate injection; (5) complete independently checkable size-eight Pauli MUB search (SAT/DRAT or verified exact-cover) or a positive eight-set witness.

The actual new deliverable is exact circuit resource classification (single CCZ), not an inference that W33 has solved the physical theory of everything.

## Parallel-commit reconciliation at publication

While this packet was being tested, another assistant pushed 1a26ceb031211ad8d25862fd2d7b96064bcdd097 to master. Its commit message reports an S3 symmetry merging eight O(5) second-matrix orbits into two equivalence classes for the five-qubit size-eight search; the exhaustive search was still in progress. We did **not** independently verify that orbit-collapse theorem or incorporate its status into the exact puncture census, which remains a separate, modest calculation. This release sits atop the latest parallel master and preserves all unrelated local modifications.

## Exact SUM synthesis addendum

A separate executable exhaustive Dijkstra run enumerates all 11,232 elements of GL(3,3) under 18 generators: twelve signed SUM row additions of unit cost, three coordinate swaps and three local x->2x rescalings at zero cost. The exact minimum SUM-count histogram for linear maps is (cost:count) 0:48, 1:576, 2:3600, 3:6336, 4:672. Our target L has minimum cost four. A concrete all-positive four-SUM sequence is 2->0, 0->2, 1->2, 2->1. Consequently the complete U=F P_L^dag CCZ P_L F^dag circuit can be realized using six single-qutrit Fourier gates, eight SUMs and one CCZ. This is optimal in CCZ count with freely available Cliffords and optimal for the *individual L* within the stated linear+free-monomial model; neither claim establishes a globally minimal optical circuit with arbitrary Clifford gates, ancillas or measurements. Reproduction: analysis/toe_20261113_ccz_sum_optimal.py, its JSON certificate, and tests/test_toe_20261113_ccz_sum_optimal.py.
