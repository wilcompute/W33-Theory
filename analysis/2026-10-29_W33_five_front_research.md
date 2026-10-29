# W33 five-front continuation: exact code distance, F9, finite E8, photonic and dynamics falsifiers

**2026-10-29.** Follows commit 4b93784c1. Results below distinguish finite certificates, conditional extensions, and physical obstructions. Nothing here establishes a theory of everything or predicts a fundamental constant. Executable producers regenerate JSON.

## 1. Extension-field test

The file analysis/w33_20261029_F9_extension_field_rank.py constructs 820 points and 820 totally isotropic lines over the genuine field F9=F3[t]/(t²+1), **not** integer residues modulo 9.

- Exact binary ranks: rank(N)=451 and rank(A)=370, summing to 821.
- A²=0 and AN=J over F2; the even-line span has rank 450, exactly dim ker(A).
- The adjacency CSS code has n=820, k=80, d<=18. Exact distance remains open.

The odd-q incidence 2-rank formula is prior art (repo Passes 238/266, including q=9). This extension independently checks the even-line/adjacency kernel bridge. The base incidence identities hold for all odd prime powers; general equality requires the known rank law.

## 2. Exact q=5 minimum distance, partial q=7

analysis/w33_20261029_adjacency_css_distance_falsifier.py reconstructs adjacency syndromes. It defines a deterministic linear projection F2^n -> F2^64 by assigning one fixed SHA256-derived 64-bit coefficient to each syndrome coordinate and XORing those present. The cryptographic collision-resistance of SHA256 is NOT assumed.

**Exact collision lemma.** If every projected syndrome of a d-subset of distinct points is distinct, there is no nonzero even kernel word of weight <=2d. If a kernel word has support S of even weight 2s<=2d, choose a d-subset T meeting S in exactly s elements; then T and T symmetric-difference S have size d and equal full syndromes, hence equal projected syndromes. Such a T exists for n>=2d.

- q=5: all C(156,4)=23,738,715 projected four-point sums are distinct (zero collisions). Every nonzero kernel word has weight >=10; a symmetric difference of intersecting lines is a weight-10 logical outside im(A). **[[156,24,10]] exactly.**
- q=7: all C(400,3)=10,586,800 projected three-point sums are distinct. No nonzero kernel word has weight <=6. An intersecting-line word outside im(A) has weight 14. Thus **[[400,48,d]] with 8<=d<=14**, not an exact distance assertion.

The produced JSON contains deterministic SHA256 fingerprints of sorted projected sums. The absence of collisions under *any deterministic linear projection* is rigorous evidence of absence of full collisions; no probabilistic assumption is used.

## 3. Concrete E8/2E8 quadratic isometry, with complete projective group closure

analysis/w33_20261029_explicit_mod2_E8_isometry.py builds H=ker(A)/im(A), a hyperbolic basis, and an explicit isometry into the E8 simple-root lattice modulo 2, using Q(v)=sum_i v_i + sum_{i~j} v_i v_j.

- All 256/256 classes preserve Q.
- Full Weyl reflection enumeration yields 240 integral E8 roots and 120 distinct classes modulo 2; the 120 nonsingular H classes map exactly to them.
- Seven explicit symplectic transvections induce orthogonal 8x8 binary matrices. Full generator closure gives **25,920 distinct projective W33 permutations and 25,920 distinct orthogonal matrices**, checking composition consistency: a faithful PSp(4,3) action in the finite E8/2E8 coordinates.

This is basis-dependent: it is NOT a canonical integral E8 Weyl-lattice lift, an eight-label permutation representation, or a physical Hamiltonian. Prior repo work already identified the abstract O8+(2) carrier; the novelty claimed is the directly executable coordinate and group-action certificate.

## 4. Photonic code feasibility and photon-loss falsifier

analysis/w33_20261029_photonic_dynamics_boundaries.py establishes specific resource constraints.

- One photon across m mutually orthogonal modes spans an m-dimensional Hilbert space. Eight logical qubits need dimension 256; 40 and 240 single-photon modes cannot carry the entire [[40,8,6]] logical state space. Four logical qubits need 16 dimensions and do fit inside 40 modes dimensionally; this does not prove a fault-tolerant implementation.
- For uniform total photon loss L_eta(rho)=eta*rho+(1-eta)|vac><vac|, two orthogonal one-photon inputs have output trace distance eta instead of 1. Contractivity forbids deterministic exact recovery from that output alone for eta<1. Heralded success, additional photons and quantum ancillas, or matter memory are not excluded.
- A 40-physical-qubit CSS block is not the same thing as one photon in 40 modes. An optical implementation must specify an encoding, ancillas, a physically realizable syndrome extraction, recovery, and fault analysis. A 2026 PRX Quantum no-go also restricts implementing the full multi-logical-qubit Clifford group by transversal constructions.

Sources: Knill–Laflamme 1997 https://doi.org/10.1103/PhysRevA.55.900 ; Moyano-Fernandez & Garcia-Escartin 2017 https://doi.org/10.1016/j.optcom.2016.07.085 ; Chakraborty & Gottesman 2026 https://doi.org/10.1103/y14y-7kp3 . The statements above follow from specified elementary models; do not generalize the no-go to architectures with quantum redundancy or postselection.

## 5. Finite-geometry symmetry does not uniquely determine dynamics

The W33 point adjacency graph has the exact integer identity A²=8I-2A+4J and eigenvalues 12 (once), 2 (24), -4 (15). Two different Hamiltonians H1=A and H2=A+J/40 commute with every W33 automorphism. At t=pi (fixed arbitrary energy units):

    exp(-i*pi*H1) = I
    exp(-i*pi*H2) = I - 2J/40

The on-site return probabilities differ: 1 versus 361/400. Thus identical geometry and symmetry can give physically distinguishable evolution. Finite symmetry alone cannot determine a unique Hamiltonian, mass scale, gravity or clock rate. A TOE must add an independently justified dynamical/action selection principle and deliver parameter-free falsifiable predictions.

## Commands

    python analysis/w33_20261029_F9_extension_field_rank.py
    python analysis/w33_20261029_adjacency_css_distance_falsifier.py
    python analysis/w33_20261029_explicit_mod2_E8_isometry.py
    python analysis/w33_20261029_photonic_dynamics_boundaries.py
    python -m unittest discover -s tests -p test_w33_20261029_five_fronts.py -v

Only the distance search requires NumPy (for sorting large uint64 vectors); other producers use Python standard library. The local worktree is isolated from pre-existing user changes.
