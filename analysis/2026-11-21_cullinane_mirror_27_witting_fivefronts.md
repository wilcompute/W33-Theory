# Seven executed fronts: 27 five-chart Witting readouts, full Hermitian–Pauli symmetry, physical channel limits, and Cullinane's recovered site

**21 November 2026 — executed, audited finite mathematics and ideal-quantum simulation.**
Producer `analysis/toe_20261121_27decks_fivefronts.py`;
frozen certificate `data/toe_20261121_fivefront_27decks.json`;
offline tests `tests/test_toe_20261121_27decks_fivefronts.py`.

## Sources recovered and read; source-priority firewall

**The inaccessible address** `https://finitegeometry.org/sc/map.html` consistently timed out in the previous pass, including a 12-second Windows direct request. Its author Steven H. Cullinane has an **accessible full site-map mirror** at:

**https://m759.github.io/map.html**

The actual HTML was fetched successfully from the authorized Windows workstation (HTTP 200, 42,216 bytes). A deterministic standard-library HTML parser extracted and froze **190 distinct link targets**, both local and external, in the certificate. This is a link inventory, NOT a claim that all 190 targets or every paper have been read. Some historical external links may be broken.

The site has a versioned snapshot (35.8 MB) at **https://zenodo.org/records/1038121**, and public source at **https://github.com/finite-geometry/galois**. The accessible mirror includes, among others:
- Cullinane, *Geometry of the 4x4 Square*, https://m759.github.io/16/geometry.html : 35 affine plane-partitions of AG(4,2), MOG/PG(3,2), and AGL(4,2) order322560.
- *The Geometry of Qubits*, https://m759.github.io/gen/geoqubits.html : Saniga's matrix-ring M2(F2), two-qubit GQ(2,2), Veldkamp context, references to N-qudit Pauli geometries.
- *The Miracle Octad Generator*, https://m759.github.io/24/MOG.html : 35 paired partitions, 759 Golay octads, M24.
- *The Klein Correspondence, Penrose Space-Time, and a Finite Model*, https://m759.github.io/64/KleinCorr.html : 35 lines of PG(3,2), Q+(5,2), Conwell heptads and a distinct complex twistor comparison.
- *Finite Relativity*, https://m759.github.io/16/finiterelat.html : finite reference-frame invariance and affine group, not the Einstein field equations.
- *Configurations and Squares*, https://m759.github.io/gen/configs.html : Hesse, Möbius–Kantor, Pappus configurations.

The recovered site is valuable but **Cullinane's Q+(5,2) Klein geometry and two-qubit W(3,2) are NOT identical to our odd-characteristic two-qutrit W(3,3) or to a physical Lorentzian metric.** Distinguish mathematical analogy from an explicit map.

Frans Marcelis's independently relevant website is at https://fgmarcelis.wordpress.com/ ; his Witting/Penrose and E8 geometry belong to this provenance, not to new discoveries in our code. Other principal literature: Vlasov, *Scheme of quantum communications based on Witting polytope*, https://arxiv.org/abs/2503.18431 ; Waegell–Aravind, Witting/Penrose in CP3, https://arxiv.org/abs/1701.06512 ; classical H(3,4)=GQ(4,2) and PGU4(2)≅PSp4(3).

**Explicit repository precedents:** `analysis/2026-10-15_toe90_vlasov_witting_research.md` and TOE91–93 own the 40 Witting ququart ray projective 2-design, physical entanglement witness and full 25920 projective unitary ray action; `scripts/w33_witting_deck_control_audit.py` owns 36 ten-rank spread decks; `scripts/w33_witting_packet_quotient_geometry_audit.py` already constructs the 45/27 GQ quotient via a different packet route; `analysis/w33_pass9961_9984_the_unitary_branch.py` owns E8/2E8→H(3,4) and 45/27/135 refinement; `analysis/toe_20261120_octonion_mereology_radon.py` owns 45 Pauli tensor frames; and our first new package `analysis/toe_20261121_hermitian45_pauli_sic_bridge.py` owns the explicit 45 isotropic-point-to-double-SIC supports. We claim **an additional explicit 27-schedule optical equivalence and its further tests**, not discovery of these basic groups or incidence counts.

## Front 1: The 27 Hermitian lines give 27 five-setting Witting POVMs

Starting with GF(4)=F2[a]/(a²+a+1), Hermitian H(3,4) has 45 isotropic points and 27 isotropic lines; each line has five points and each point lies on three lines. For each Hermitian point z the prior bridge associates eight nonisotropic projective points S_z, precisely one K(4,4) double-SIC chart of the complex 40-ray Witting system.

**New explicit exhaustive test:** for EVERY Hermitian line L={z1,…,z5}, its five chart supports S_z are **pairwise disjoint** and their union is all 40 rays. Thus each of the 27 Hermitian lines defines a *complete five-setting 8-outcome quantum measurement schedule*.

Let P_i=|r_i><r_i|. At each chart z, implement the POVM \(\{P_i/2:i\in S_z\}\). Pick one of the five z on a fixed L uniformly. Then the **unlabeled** 40-outcome marginal effect is
\[
 E_i = \tfrac15 \tfrac12 P_i = P_i/10,\quad i=1,\dots,40.
\]
Exactly the same effect follows from randomly selecting one of the 40 original four-outcome orthonormal Witting tetrads, since every ray occurs in four tetrads. This is a reduction of **setting count 40→5**, but increases output ports/context 4→8. Context labels, latency, noise, security and hardware resources remain different.

Disjoint chart pairs are EXACTLY collinear point pairs in H(3,4); its chart-disjointness graph is SRG(45,12,3,3). On the 27 isotropic lines, declare two lines adjacent iff disjoint: the resulting skew-line graph is SRG(27,16,10,8), the Schläfli graph. The 27 five-chart schedules are frozen as explicit lists of Hermitian-point IDs.

The 45-chart adjacency graph's ordinary positive Laplacian has spectrum 0^(1), 9^(20),15^(24); it does **not** supply a Lorentzian timelike direction or a continuum.

## Front 2: Full exceptional group-equivariant 40→45→27 dictionary

Construct seven explicit GF4 Hermitian unitary generators: three coordinate swaps, three cubic-field diagonal phase multiplications, and the GF4 matrix J+I (zero diagonal, one off diagonal). All preserve the Hermitian form.

BFS closure of their **projective 40-point permutations** contains exactly **25920** elements. On 45 Hermitian isotropic points, and on the induced 27 Hermitian lines, the image groups each also have order25920. For each of the seven generators verify all 45 polar neighborhoods are transported to the corresponding neighborhoods and each of 27 lines maps to another line.

Independently, construct five F3 symplectic transvections in the W(3,3) coordinates already mapped explicitly to the Witting rays. Their closure on 40 labels has exactly25920 elements and, **as a literal set of permutations**, equals the GF4 Hermitian group. The exceptional PGU(4,2)≅PSp(4,3) symmetry has therefore been checked not merely as group orders but on the same concrete 40-point representation, with consistent 45- and 27-object actions. The abstract exceptional isomorphism and earlier full group action are published/repo precedents; this verifies our particular 27-schedule measurement dictionary is equivariant.

## Front 3: 45 real Naimark-compatible 8-output optical settings

For each of the 45 double-SIC charts, assemble the 8x4 matrix \(V_z\) whose rows are \(\langle r_i|/\sqrt2\). The exact POVM normalization gives \(V_z^\dagger V_z=I_4\). Extend the four columns to an 8x8 unitary \(U_z\) via orthonormal completion, and embed a ququart amplitude \(\psi\) as \((\psi,0,0,0,0)\). Measuring computational output modes of \(U_z(\psi\oplus0)\) produces probabilities \(|\langle r_i|\psi\rangle|^2/2\). All 45 unitary completions pass numerical unitarity/POVM checks with residual below 10^-11.

For Alice/Bob sharing arbitrary two-ququart rho and choosing the same one of any fixed five-chart schedule, Alice uses P_i/2 and Bob its complex conjugate. The *unconditioned* average matching operator is
\[
 C_{\rm SIC}=\frac{I_{16}+4|\Phi_4\rangle\langle\Phi_4|}{10}.
\]
Its ideal maximally entangled matching value is 1/2; all separable states satisfy \(P_{\rm match}\le1/5\). Compare Vlasov's four-outcome *projective* scheme: ideal value1, separable threshold2/5. The factor2 difference is from the nonprojective local POVMs; no improvement in entanglement visibility follows. Setting-dependent and outcome-informed loss can invalidate conditional statistics. No realistic eight-rail optical BOM/calibration or QKD proof follows from matrix existence.

## Front 4: A genuine CPTP ququart→two-qutrit channel AND an exact covariance no-go

**Constructive, but entanglement-breaking:** let \(E_i=P_i/10\) be the forty input Witting effects. Via the full verified 40-label graph mapping, let \(W_i\) denote one nontrivial two-qutrit Weyl order-three class representative, \(\Pi_i=(I+W_i+W_i^\dagger)/3\) its rank3 +1 eigenspace projector, and \(\sigma_i=\Pi_i/3\) a density matrix in C9. Then define
\[
 \mathcal E(\rho)=\sum_{i=1}^{40}\operatorname{Tr}(E_i\rho)\,\sigma_i.
\]
This is an explicit **completely positive trace-preserving** quantum channel, realized by measuring the four-mode Witting POVM and preparing one of 40 nine-dimensional Pauli eigenspace states. Its Choi operator \(\sum_i E_i^T\otimes\sigma_i\) was verified positive and trace-preserving. It is **entanglement-breaking**, so cannot realize coherent two-qutrit computation or have an exact CPTP inverse.

Nonetheless it is **injective on ququart density operators**: the 40 output \(\sigma_i\) have Hilbert-Schmidt Gram \(1/3\) on the diagonal and \(1/9\) off diagonal, and for all traceless Hermitian Δ the channel is HS-isotropic:
\[
 \|\mathcal E(\Delta)\|_2^2=\|\Delta\|_2^2/225.
\]
All fifteen independent traceless ququart directions were tested with an explicit orthonormal Hermitian basis. This gives a precise, if fragile, *physical measurement-and-preparation interface* and a clear distinction between **informational injection** and **reversible quantum encoding**.

**Strict limit for coherent covariance:** for any rank4 orthogonal projector P in C9, Weyl twirling gives
\[
 \frac1{81}\sum_{W\in{\rm Weyl}_9}WPW^\dagger =\frac49 I_9.
\]
Consequently average leakage from this subspace under the 80 nonidentity Weyl unitaries, and equally under 40 projective pairs, is exactly \(9/16\). Checked on three independent rank4 isometries and explicitly on the forty projective reps. No 4D subspace is invariant under the full two-qutrit Pauli group. This is an application of standard irreducibility, not an impossibility of ALL CPTP 4→9 channels.

## Front 5: A minimal, externally powered two-ray chart selector

One input Witting pure ray belongs to nine charts and gives no unique frame. All 240 orthogonal ray pairs belong to three charts each; all 540 nonorthogonal pairs belong to exactly one chart. A source-dependent classical potential \(V(z)=-\lambda({\bf1}_{a\in S_z}+{\bf1}_{b\in S_z})\) therefore has a unique minimizer for a prescribed nonorthogonal pair (frozen example rays 0 and 5).

The eight chart-outcome Shannon entropy for a pure ray equals \((1+\log_2 6)/2\) bits in its nine containing charts and \(\log_2 6\) bits in the other 36; all 45 cases were checked. These are context-dependent ideal measurement entropies, not universal free-energy laws.

An unforced *fully* PSp4(3)-invariant scalar on the transitive set of 45 charts is constant, so it cannot uniquely select one chart. The two-ray potential **explicitly introduces a physical source/spurion** and is not spontaneous selection by a derived fundamental Hamiltonian. This strengthens earlier repo symmetry-selection no-gos while giving a minimal testable control handle.

## Front 6: Multitime qutrit quantum memory with a genuine causal break

Use the 12 eigenstates of the four standard qutrit Weyl MUBs \(Z,X,XZ,XZ^2\), a complex projective 2-design. Prepare each state on system S with environment E in |0>. SWAP S↔E, **discard and reprepare** S in |0> at the intermediate slot (causal break), then SWAP S↔E again and measure output overlap with input.

- Ideal coherent environment memory: average survival **1**.
- Any entanglement-breaking (measure-and-prepare) qutrit storage: average design fidelity at most **2/(3+1)=1/2**.
- Complete computational-basis dephasing: average **1/2**.
- Fixed-state memoryless reset: average **1/3**.

Numerically checked all 12 states, mutual unbiasedness, complete 2-design operator identity and exact SWAP/partial-trace causal-break circuit. A trusted physical test above 1/2 would witness non-entanglement-breaking temporal quantum memory in a known time ordering. It does **not** establish literal photon self-entanglement, retrocausality, or gravity, and requires a real instrument and SPAM/loss controls.

## Front 7: Site restoration audit

The original domain still times out; **the full site map is now directly readable on the mirror** at https://m759.github.io/map.html . The frozen 190-link census is available in the certificate; a versioned zip is at https://zenodo.org/records/1038121 . Some linked historical papers are available via modern DOI/arXiv repositories; an accessible page title or link is not proof its cited PDF is accessible or has been read.

## Reproduction

```powershell
python analysis/toe_20261121_hermitian45_pauli_sic_bridge.py
python analysis/toe_20261121_27decks_fivefronts.py
python -m pytest -q tests/test_toe_20261121_27decks_fivefronts.py
```

The producer regenerates every calculation and recrawls only the public mirror's site-map HTML. The regression uses frozen site results and is offline. All reports distinguish established GQ/Steiner/Witting facts, new finite computational synthesis, an actual but entanglement-breaking quantum channel, a declared classical selection model, and a toy temporal experiment; none is a completed theory of everything.

## Five independent next experiments

1. Build an instrument-calibrated eight-output integrated-photonics chart analyzer (8-mode Naimark mesh), and compare loss and phase sensitivity against the older 40 four-output PVMs.
2. Apply full \(PGU(4,2)\) group action to the complete 27*5 **physical pulse scheduler**, and prove exactly which time/switch-cost resource objectives are invariant rather than assume group symmetry lowers hardware costs.
3. Characterize the Choi spectrum, accessible information and EB quantum capacity (zero) of the explicit Witting-to-two-qutrit channel; attempt ancilla/coherent assistance and bound the resources required to escape the no-go.
4. Find a microscopically motivated local two-photon interaction or environment coupling which favors exactly the observed nonorthogonal-pair chart minimizer, while quantifying external symmetry-breaking control.
5. Replace the two-SWAP ideal memory model with an event-ready, multi-slot process-tensor experiment and demand a separate continuum gravitational falsifier (nondegenerate causal cones, Lorentz signature, Ward/Einstein equations).
