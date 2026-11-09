# Q8 cosets, 72-gate unitary designs, and two-qutrit purity measurement

*Independent continuation, November 9, 2026. Finite exact mathematics and a quantum-information protocol; not a theory of everything.*

## Relationship to the existing repository and literature

Passes 12634–12639 already established the 36/135/432 maximal-partial-spread census and the exact strong-unextendibility SOS bounds. This packet contributes an independent Q8-coset derivation of the three size-eight sets per tensor split and their connection to **unitary 2-designs and a pure-state entanglement observable**.

**Prior art boundary.** 72-element qutrit unitary 2-designs are known: see the University of Waterloo thesis (2018), https://dspacemainprd01.lib.uwaterloo.ca/server/api/core/bitstreams/f6d263c6-6441-4265-89fa-75b14c9ddcdf/content . The frame-potential criterion is Gross, Audenaert, and Eisert (2007), https://arxiv.org/abs/quant-ph/0611002 . No claim of independent priority for that known design or for the pure-state tomography technique is made.

## A: Exactly three eight-context cosets

Fix the two-qutrit split and take opposite symplectic forms on the two factors. Its 24 maximally entangled stabilizer contexts are Lagrangian graphs L_S with S in SL(2,3). Two graphs meet trivially iff det(S-T) is nonzero mod 3, equivalently det(I-S^(-1)T) != 0.

The normal quaternion subgroup Q8 of SL(2,3) comprises identity, the unique order-two element, and six order-four elements. All seven nontrivial Q8 elements have no nonzero fixed vector in F3². Every Q8 coset therefore defines eight mutually unbiased entangled bases.

The producer reconstructs the entire 24-vertex disjointness graph and **exactly** enumerates its maximal cliques: 144 of size five, 24 of size six, and **three of size eight**. The eight-cliques equal the three Q8 cosets, with no extras. Multiplying across the known 45 tensor splits gives the 135 size-eight sets already found in the corpus. The coset label is not physically selected by this theorem.

## B: Each 72-Clifford family is an exact unitary 2-design

Vectorize normalized one-qutrit unitaries as Choi states |J(U)>. Then <J(U)|J(V)> = tr(U†V)/3. Each graph context yields nine orthonormal Choi states of Clifford unitaries, and each eight-clique gives 8x9=72 gates.

For each fixed U, the fourth powers |tr(U†V)|⁴ over all 72 V have census: one 81 (itself), eight zeros (same basis), 63 ones (the seven other mutually unbiased bases). Therefore the **exact second unitary frame potential** is

\[
\mathcal F_2=\frac{81+63}{72}=2.
\]

The established criterion proves these are unitary 2-designs. One family is the projective single-qutrit Pauli translation subgroup (order 9) extended by Q8 (order 8), totaling 72. All 216 projective single-qutrit Cliffords partition into three cosets of 72. Conditional minimality: among Pauli-containing Clifford subgroups, a unitary 2-design's symplectic quotient must be transitive on the eight nonzero Pauli labels, so its cardinality is at least 9x8=72. This is **not** an absolute minimality claim for unrestricted unitary designs.

## C: Experimental collision statistic for arbitrary states

For any normalized density matrix ρ on C³⊗C³ and the 72 rank-one Choi measurement projectors from *any one* eight-MUB family, let p_j=tr(ρ E_j). The unitary 2-design twirl gives the exact identity

\[
\boxed{\sum_{j=1}^{72}p_j^2 =
1+\operatorname{tr}(\rho^2)
-\frac{\operatorname{tr}(\rho_A^2)+\operatorname{tr}(\rho_B^2)}{3}.}
\]

Since each of eight bases contributes nine probabilities summing to one,

\[
F_8=\sum_j(p_j-1/9)^2
=\operatorname{tr}(\rho^2)+1/9-
[\operatorname{tr}(\rho_A^2)+\operatorname{tr}(\rho_B^2)]/3.
\]

For a **globally pure** input, the two marginal purities coincide and therefore

\[
\boxed{1-\operatorname{tr}(\rho_A^2)=
\frac32(F_8-4/9).}
\]

Product states attain F8=4/9; maximally entangled states attain F8=8/9. Eight nine-outcome projective measurement settings suffice to determine pure-state linear entanglement entropy without full state tomography. For mixed inputs, F8 is **not** a standalone entanglement monotone. The three cosets provide exactly redundant estimates of the same quadratic statistic and thus a potential calibration cross-check.

## D: Necessary mixed-state purity ceilings, conditional on Pass 12639

With Q_B=sum_e |ee><ee| and symmetric two-copy projector Π, the exact SOS floor δ_m implies sum_B Q_B >= (m/9+δ_m)Π. Use tr[(ρ⊗ρ)Π]=(1+trρ²)/2. If an input state is unbiased to all m bases, F_m(ρ)=0 and

\[
0\ge (m/9+\delta_m)(1+\operatorname{tr}\rho^2)/2-m/9.
\]

For pentads (m,δ)=(5,1/9), necessarily trρ² <= 2/3. For size-eight sets (m,δ)=(8,4/9), necessarily trρ² <= 1/3. These are **not claimed to be sharp**.

## Machine evidence and physical scope

Independent producer: analysis/w33_20261109_q8_design_purity.py; frozen data: data/w33_20261109_q8_design_purity.json; regression: tests/test_w33_20261109_q8_design_purity.py. No imports from existing MUB implementations. Finite-group and frame-count statements are exact. Explicit Fourier/phase/Pauli matrices and **216 seeded mixed-state trials** were checked numerically on the local machine (max error 1.9984e-15); a separate implementation agreed on the server.

This demonstrates a group-theoretic **measurement primitive**, not quantum gravity, an observed constant, emergent physical time, a Maxwell field, or a unique Standard Model vacuum. Hardware implementation, loss models, statistical shot complexity, and a purity-certification mechanism remain open.
