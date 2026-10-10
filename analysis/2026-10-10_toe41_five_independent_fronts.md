# TOE41 — All five independent fronts executed, with exact no-go and an E6 compiler

**Date:** 10 October 2026. **Ownership:** New TOE41 code extends independently verified TOE38/TOE40, Pass11384 and Pass11869–11878. **Status:** finite algebraic certificates and a model-internal Maxwell null test, **not a TOE**. The user asked to execute five nonsequential tracks. Each is auditable below.

## 1. Fully finite Clifford-frame modular-purity gate

Producer `analysis/w33_20261010_toe41_clifford_purity_nogo.py`; certificate `data/w33_20261010_toe41_clifford_purity_no_go.json`.

Enumerate all 40 projective points of the nondegenerate symplectic 4-space over F3 and all 90 **nondegenerate 2-dimensional symplectic planes**. Every such plane defines one full one-qutrit Pauli subalgebra in the 9-dimensional two-qutrit Hilbert space (and its commutant another); its eight nonidentity Paulis define its subsystem purity.

Each nonidentity Pauli lies in **nine** of these 90 planes. Pure-state Pauli orthonormality gives sum over all 80 nonidentity Pauli expectation magnitudes squared =8. Therefore the full Clifford-frame orbit-averaged subsystem purity is identically

`(1 + 9/90*8)/3 = 3/5`

for **every pure two-qutrit state**, independent of the genus-two period matrix. Enumerated examples include separable theta, a CZ-modular shear, genuinely coupled theta, and a seeded random state. All four give 0.6. By contrast the frame-purity **variance** is 0.02986129137 for the product example and 0.00813280899 for a generic random state. That higher-order nonconstant invariant is a viable **finite Clifford-invariant mathematical potential input**, but not yet an automorphy-correct **full Siegel modular function** and not a stabilized CP-breaking vacuum. A purity-mean potential is rigorously vacuous.

## 2. Full small-k acoustic tensor and Gauss-reduced commutator

Producers `analysis/w33_20261010_toe41_maxwell_acoustic_tensor.py` and `analysis/w33_20261010_toe41_maxwell_birefringence_null.py`; frozen data certificates alongside.

Using the *existing* 1,385 genuinely closed plaquettes on the native three-deck W33 Levi cover, `P0` has rank 78, and the combined `[P0; B0^dag]` has rank 157. Hence exactly three zero-momentum harmonic edge modes. Integrate out the 78 massive P0-image directions. With the three-dimensional orthonormal harmonic basis H0 and Q an orthonormal image basis for P0:

`G_i=(I-QQ^dag) (dP/dk_i)|_0 H0` and `Acoustic(n)=sum_i,j n_i n_j G_i^dag G_j`.

The full **complex 3x3x3x3 coefficient tensor** is persisted in JSON as real and imaginary arrays; all six unit directions have one zero longitudinal eigenvalue and two positive acoustic eigenvalues. For x these are 1.9047619045 and 2.0519316020, giving phase velocities 1.3801311186 and 1.4324564922 (ratio 1.0379133351). y/z velocities are 1.3970609328 and 1.4150977488 (ratio 1.0129105435). The finite-k .015 Bloch replay closely reproduces these ratios; thus the nondegenerate splitting survives at leading k->0 for the *specified equal-weight model*.

At nonzero k the orthogonal projector `Q_T=T T^dag` to `ker B(k)^dag` has dimension 80, is Hermitian and idempotent with residuals <=1.3e-15, and defines the reduced canonical commutator `[A_i,E_j]=i(Q_T)_{ij}`. This is a well-defined *finite classical/gauge-reduced canonical algebra*, **not** a constructed physical Fock representation, QED or measured c.

## 3. Native-gauge overlap index: exact paired-spectrum obstruction

Producer `analysis/w33_20261010_toe41_w33_overlap_index_nogo.py`, certificate same stem.

Use actual W33 Levi 160 U(1) incidence link phases as a 40x40 complex M, chiral grading gamma=diag(I40,-I40), and *same-sublattice two-hop* Wilson-style regulator `r diag(M M^dag,M^dag M)-mI`, r=.1,m=1.2. The Hermitian overlap kernel is

`H=[rMM^dag-mI,M; M^dag,-rM^dag M+mI]`.

The SVD of M block-reduces H into 40 traceless 2x2 Hermitian blocks, each with eigenvalues +/-sqrt((r s²-m)²+s²). Thus the overlap index is identically `-Tr sign(H)/2=0` for **all** link gauge backgrounds, not just numerically sampled ones. The GW defect is ~3e-15; arbitrary local U(1) phase gauge covariance ~1e-15. The kernel is local in the graph (up to two-step regulator), but no growing-cover chiral topology or four-dimensional anomaly has been constructed. Other Wilson regulators can have nonzero topological index; this exact obstruction only applies to the stated paired kernel.

External checks: Hernandez/Jansen/Lüscher, *Locality properties of Neuberger's lattice Dirac operator*, Nucl. Phys. B552 (1999), https://doi.org/10.1016/S0550-3213(99)00213-8 ; *The index of lattice Dirac operators and K-theory* (2026), https://doi.org/10.1007/s11005-026-02080-w .

## 4. Actual signed 45-term E6/Albert cubic as five-layer qutrit gate network

Producer `analysis/w33_20261010_toe41_e6_45_ccz_compiler.py`, frozen full 45 signed triples in `data/w33_20261010_toe41_e6_45_ccz_compiler.json`.

Choose **standard trinification 3x3-matrix coordinates** A,B,C, nine qutrits each. The complex split-Albert cubic representative is

`N(A,B,C)=det(A)+det(B)+det(C)-Tr(ABC)`.

The three determinant parts have 18 signed squarefree triple monomials and the trace part has 27 negative monomials: **45 distinct signed triples on 27 sites**. Independent random integer checks establish equality of the two forms as polynomials in those coordinates. With qutrit number operators `n_j|x_j>=x_j|x_j>`, the declared self-adjoint commuting three-body Hamiltonian

`H=(2pi/3) sum_(i,j,k; sign) sign*n_i*n_j*n_k`

implements a diagonal unitary `U|x>=exp(2pi*i*N(x)/3)|x>` by a fixed choice of evolution sign. Every third mixed finite difference equals the corresponding signed coefficient modulo3, proving a non-Clifford cubic phase.

**Exact gate scheduling discovery and native-repo verification:** Pass10944 **already proved** the full 45-signed-CCZ phase-kickback opcode; TOE41 does **not** reclaim that result. Each of 27 qutrits participates in exactly five triples, hence five vertex-disjoint gate layers are a hard lower bound. Deterministic scheduling produces **five layers of nine disjoint CCZ interactions** in both standard Albert coordinates **and independently the repository's actual** `artifacts/canonical_su3_gauge_and_cubic.json` `d_triples`, meeting this lower bound exactly. The certificate freezes the complete **native five parallel classes of triad indices** and their signs. This is an **optimal-depth 5** no-ancilla compiler on the ideal three-body gate set, an independent scheduling improvement to Pass10944. Algebraic E6 preservation of N does not prove a unitary E6 physical symmetry, physical 3-body couplings, photonic implementation or fault tolerance.

## 5. Frozen dimensionless Maxwell-relativistic null test

Producer `analysis/w33_20261010_toe41_maxwell_birefringence_null.py` and its fixed hypothesis record.

For the **declared equal-weight W33 Hamiltonian**, impose the stringent Lorentz-isotropic photon null: the two acoustic velocities are degenerate at fixed |k| and independent of direction, tolerance 0.001. This null was written down before this six-direction numerical replay, **but TOE40 already revealed x-direction splitting**, so the test is **not blinded prospective experimental prediction**. The leading acoustic tensor produces a x-axis 3.7913% polarization-speed ratio difference and y/z 1.2911%; six directions have up to 4.03% total speed span at small finite k. **Strict untuned isotropic Maxwell interpretation is falsified.**

No renormalized mapping from abstract deck k to physical frequency, length, dimensional speed or photon-matter sector is given. It would be scientifically invalid to compare these dimensionless numbers to astrophysical vacuum-birefringence observations. The archived fixed-alpha comparison in TOE40 is already a negative control, not revived here as a new prediction. The actual experimental dimensionless prediction remains **open**.

## Scope, evidence and warnings

- Exact: 90-plane combinatorics and constant orbit mean; 40 spectral pairs and index zero for one gauge-overlap regulator; 45-term signed Albert cubic and constructive depth-five schedule.
- Numerically certified: local Maxwell 3x3 acoustic tensor with derivative and projector checks; six propagation directions.
- Not established: a full modular-invariant CP-breaking vacuum, growing-lattice chiral family, emergent Lorentz symmetry, experimental coupling, fault-tolerant E6 gate, or a Theory of Everything.
- The E6 cubic matrix representative has 27 distinct *registers*; Hilbert space dimension 3^27. The circuit is diagonal and is evaluated via sparse phase oracles, not an allocated 3^27 wavefunction.
- Reproduce via `py -3 -m pytest -q tests/test_w33_20261010_toe41_five_fronts.py`.

## Five **independent** next targets

1. Construct a full genus-two modular-invariant scalar from Igusa/Burkhardt covariants and compute a positive Hessian plus CP-distinct minima; compare its finite Clifford-frame purity variance as a candidate higher-order ingredient.
2. Optimize local W33 closed-plaquette weights subject to exact topological ranks to enforce degenerate isotropic transverse acoustic tensor; prove positivity and quantify tuning.
3. Construct a growing **four-dimensional** W33-derived cover and test a Wilson kernel with a genuine topological background that escapes the singular-value pair symmetry; verify anomalies separately.
4. Transport the five-layer 45-CCZ standard Albert compiler through the exact Pass11384 frame dictionary, then compile it into 1-/2-qutrit gates with explicit noise, magic costs and experimental resources.
5. Derive one externally testable dimensionless observable with scale, scheme and uncertainty predicted from a fixed local action, then freeze its value before obtaining experimental data; keep the internal isotropy null as a gate.
