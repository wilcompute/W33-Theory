# Five followthrough gates + a determinant-resolved quantum-frame coherence witness

**2026-11-08 (US Eastern), prepared against the current W33-Theory master.** Mathematical results are distinguished from conditional field theories, numerical stress tests, existing observations, and future preregistrations throughout.

- Producer: `analysis/w33_20261108_five_followthrough_plus_coherence.py`
- Tests: `tests/test_w33_20261108_five_followthrough_plus_coherence.py`
- Certificate: `data/w33_20261108_five_followthrough_plus_coherence.json`
- Dedicated CI: `.github/workflows/w33_20261108_five_followthrough_plus_coherence.yml`

## The full evidence firewall

Nothing here demonstrates a physical TOE, quantized gravity, emergence of a 3+1 Minkowski metric, photon creation, experimental nonclassicality, a measured gauge constant, an anomaly-free Standard Model from E6, radiative strong-CP stability, new DES/KiDS cosmological inference, or a quantum hardware prototype. The calculations extend the previously merged Pass20261108 selected-null-frame exact clock construction without claiming tensor Fourier transforms as novel fundamental mathematical machinery.

## Gate 1 — A constructive globally symmetric null-frame potential with a rigorous non-unique-vacuum theorem

For the projective null cone \(\mathbb P^1(\mathbb F_p)\) there are \(n=p+1\) null directions. Introduce one real order parameter \(w_j\) per null line and the **globally permutation-invariant** quartic potential
\[
V(w)=\sum_{j=1}^{n}w_j^2(1-w_j)^2
+\kappa\left(\sum_{j=1}^{n}w_j-3\right)^2,\qquad \kappa=0.7.
\]
It is manifestly nonnegative. The global zero set comprises precisely the binary vectors with **exactly three occupied directions**, for a total of \(\binom{p+1}{3}\) minima. These three selected lines are independent as vectors in \(\operatorname{Sym}_2(\mathbb F_p)\) because no three distinct points on a nonsingular conic are collinear. For the tested prime values, the vacuum orbit degeneracies are:

| p | Distinct projective null lines | Exactly degenerate vacua | Local Hessian eigenvalues |
|---|---:|---:|---|
| 3 | 4 | 4 | \(2^3,7.6\) |
| 5 | 6 | 20 | \(2^5,10.4\) |
| 7 | 8 | 56 | \(2^7,13.2\) |
| 11 | 12 | 220 | \(2^{11},18.8\) |

Here \(2^{n-1}\) is multiplicity notation. At each minimum, the Hessian is \(2I_n+2\kappa\mathbf1\mathbf1^\top\), giving an explicit positive local radial gap. **But the symmetry does not select one unique frame**: \(\mathrm{PGL}_2(\mathbb F_p)\) is sharply 3-transitive on the projective line, so all \(\binom{p+1}{3}\) unordered triples form one orbit. Any fully invariant potential attaining one of them must attain every one. This is a finite analogue of the vacuum-selection issue: a thermodynamic state, background field, boundary condition, or dynamical symmetry-breaking phase is still needed.

The model treats the projective-frame symmetry as a **global** finite symmetry. It would be invalid to treat a local gauge-variant order parameter as an observable physical spontaneous gauge-breaking VEV; see Elitzur's theorem. Nor is an invariant order parameter on \(\mathbb P^1(\mathbb F_p)\) an experimentally acceptable Lorentz-breaking field merely because its toy Hessian is positive. Prior art for the sharp triple action: ICM 2026 discussion, DOI 10.1137/25M1805266.

## Gate 2 — Matter-coupled 27-site U(1) lattice: full nonlinear gauge invariance and continuity

The producer additionally reconstructs the original 108-edge W33 null graph and verifies that the selected 81 charged-matter links are a **strict subset of the original native edges**, not an unrelated replacement complex. Use the selected three null directions to label a periodic cubic lattice \(\mathbb F_3^3\) with **27 vertices**, **81 oriented links** and **81 oriented elementary square plaquettes**. Let \(\partial_1\) be its vertex-edge boundary and \(\partial_2\) its edge-square boundary, obeying \(\partial_1\partial_2=0\). Assign a charged complex scalar \(\psi_x\) to sites, real compact U(1) angle \(A_{xy}\) to each oriented link, and the action
\[
S[\psi,A]=\sum_{(x,y)}|\psi_y-e^{iA_{xy}}\psi_x|^2
+0.8\sum_{\square}\bigl(1-\cos[(\partial_2^\top A)_{\square}]\bigr)
+0.6\sum_x|\psi_x|^2.
\]
Under arbitrary independent site phases \(\chi_x\),
\[
\psi_x\mapsto e^{i\chi_x}\psi_x,\qquad
A_{xy}\mapsto A_{xy}+\chi_y-\chi_x.
\]
The matter covariant derivative transforms at the destination vertex and \(\partial_2^\top\partial_1^\top=0\), so the **complete nonlinear action is invariant**. Numeric desktop checks with seeded random complex fields show:
- Action invariance difference **0** at floating-point precision.
- Infinitesimal Ward-direction centered-finite-difference residual approximately **\(2.84\cdot10^{-8}\)** for step \(10^{-6}\).
- Matter Hamiltonian \(H=D^\dagger D\) is exactly Hermitian within floating-point tolerance. For its Schrödinger evolution,
\[
\dot\rho_x+(\partial_1j)_x=0,\qquad
j_e=2\,\operatorname{Im}(\bar\psi_{\mathrm{head}}e^{iA_e}\psi_{\mathrm{tail}}),
\]
with continuity residual around \(3.55\cdot10^{-15}\).
- The neutral source \(\rho_0=+1,\rho_1=-1\) is solved by a discrete Gauss field \(E=\partial_1^\top(\partial_1\partial_1^\top)^+\rho\), with residual around \(6.66\cdot10^{-16}\).

The construction is **standard scalar compact lattice electrodynamics** (cf. Kogut–Susskind, *Phys. Rev. D* **11**, 395, 1975, DOI 10.1103/PhysRevD.11.395), imported onto a W33-selected coordinate frame. It **does not derive** charge unit, spin-half electrons, measured electromagnetic coupling or a 3+1 spacetime metric. Temporal dynamics are an independent modelling choice, and radial scalar excitations need a physical mass/parameter calibration.

## Gate 3 — A robust exact 27-mode null clock with a certified Duhamel perturbation bound

Using the previously merged exact null-frame Hermitian Fourier-product Hamiltonian \(H\), let \(\Delta H\) be an arbitrary static Hermitian control error. Duhamel's identity at duration one yields the **operator inequality**
\[
\|e^{-i(H+\Delta H)}-e^{-iH}\|_{\rm op}\le\|\Delta H\|_{\rm op},
\]
hence every input-output probability changes by **at most \(2\|\Delta H\|_{\rm op}\)** (a conservative entrywise bound).

Run **48 deterministically seeded synthetic trials**: eight realizations at each of three error scales, for *onsite detuning* and *null-edge hopping errors*. The code verifies the norm and probability bounds in every trial and reports worst column-wise total variation. Selected maxima:

| Error scale | Worst intensity departure, detuning | Worst intensity departure, null-edge error |
|---|---:|---:|
| 0.005 | 0.000641 | 0.000609 |
| 0.020 | 0.002069 | 0.002621 |
| 0.060 | 0.007275 | 0.008721 |

A uniform common onsite detuning shifts every phase together and is **exactly unobservable in intensities**, providing a useful control. Randomized errors have nonzero sensitivity and increasing average deviation.

These are **not measured photonic tolerances** or fault-tolerant error thresholds. The error scale is a dimensionless Hamiltonian setting for unit-time evolution, not a hardware specification.

## Gate 4 — Native E6 cubic covariance: six Cartan directions + external SL(3), but not all 78 generators

Reconstruct all **1620 signed E6×SL3 bracket records** from `analysis/w33_e6_cubic_jacobian_rank_stratification.py`. Their underlying **45** signed E6 tritangent triples yield a \(45\times27\) incidence matrix \(T\), where \(T_{\tau i}=1\) if line \(i\) belongs to triple \(\tau\). Its exact rational rank is **21**, leaving a six-dimensional rational kernel \(Tw=0\). Thus the six toral rescalings \(X_{i\alpha}\mapsto e^{t w_i}X_{i\alpha}\) preserve **every signed cubic term**, because the three line weights sum to zero on each supported triple.

For the trilinear expression
\[
C(X)=\sum_{\mathrm{1620~records}}c_{u x o}X_{u1}X_{x2}X_{o3},
\]
verify a finite nontrivial diagonal 27-family rescaling under a rational toral generator and an independent nontrivial **external SL(3,\(\mathbb C\))** action on the external three-dimensional phase/fiber. The former invariance is termwise; the latter follows from the antisymmetric epsilon contraction. The two seeded finite-transformation relative residuals are approximately \(2.58\times10^{-16}\) and \(2.22\times10^{-16}\).

This gives a **14-dimensional** explicitly tested Lie subalgebra of the expected E6×SL3 symmetry \((78+8)\). **The remaining 72 E6 generators are not certified.** The full 78-matrix E6 representation export is absent in this clean checkout, and fitting an invariant to a torus is not a complete E6 gauge-invariance proof. The proposed scalar cubic stabilization term therefore remains a **conditional** model component; we do not claim a fully legal E6 superpotential, D/F-flat vacuum, anomaly cancellation, CKM/PMNS spectrum or protected physical \(\bar\theta\).

## Gate 5 — Cosmology evidence firewall, source replay and prospective S9

Re-read six corrected scalar-field ΛCDM nonlinear-power control cells from the committed Halofit rerun, as well as the second patched HMcode model. Compare corrected and original treatment without treating source-file arithmetic as a new likelihood. The corrected ΛCDM scalar representation agrees with standard ΛCDM at all six cells to relative error below \(3\times10^{-6}\). The previously apparent CPL-versus-fading cosmic-shear penalty **reverses** after repair, so the old S7/S8 shear evidence is withdrawn.

The parallel team has also frozen **S9**, a *prospective* prediction for future shear releases. It is **not observed new data** and may fail. This pass explicitly reads the S9 preregistration without treating it as a validation; it neither reruns raw DES/KiDS shear chains nor provides new joint evidence. It likewise checks the prior Pass12633 flavor-modulus/clock sensitivity inconsistency (over \(10^6\) in the given proxy), which requires dark/visible sequestering; the proxy remains model-dependent.

**Independent external context:** García-García, Ferreira and Wolf, *Status of single scalar field dark energy*, accepted by *Physical Review D* 29 October 2026, https://doi.org/10.1103/jkcl-g4cq, find that any preference for extensions is sensitive to surveys and priors. That article is *not* a verification of this repository's fading or KLT field. The original stock CLASS scalar-Halofit problem was reproduced upstream as https://github.com/lesgourg/class_public/issues/682 by the parallel track, not by this calculation.

## Sixth connection — determinant-resolved hidden frame decoherence

At \(p=3\) there are four distinct unordered triples of the four projective null directions. Fix an input vertex \(x\) of the original 27-element physical \(\operatorname{Sym}_2(\mathbb F_3)\). Every selected frame \(B_f\) produces an ideal Fourier output
\[
\psi_f(y|x)=27^{-1/2}\omega^{\,y^\top B_f^{-\top}B_f^{-1}x},
\qquad \omega=e^{2\pi i/3}.
\]
Hence **every frame and input has the identical uniform intensity table**:
\[
P_f(y|x)=1/27.
\]
But if the frame is unknown and sampled equally from the four wells, the output density matrix is
\[
\rho_x=\frac14\sum_{f=1}^4|\psi_f\rangle\langle\psi_f|.
\]
The Fourier characters at distinct wavevectors \(k_f=B_f^{-\top}B_f^{-1}x\) are **exactly orthogonal** and identical if the labels coincide. Consequently
\[
\boxed{\operatorname{Tr}\rho_x^2=\frac1{16}
\sum_{\text{distinct }k}\operatorname{multiplicity}(k)^2.}
\]
The producer enumerates all 27 physical vertices using **exact modular inverses**, classifies by the native determinant \(Q(x)\), and independently builds numerical 27×27 mixed density matrices for representative inputs. The complete census is:

| Physical input x | Count | Exact output purity | Character multiplicities |
|---|---:|---:|---|
| x=0 | 1 | 1 | (4) |
| x≠0, Q(x)=0 | 8 | 1/4 | (1,1,1,1) |
| Q(x)=1 | 6 | 1/4 | (1,1,1,1) |
| Q(x)=2 | 12 | 3/8 | (2,1,1) |

There is also a **simple single-input inverse-frame echo witness**, not necessarily requiring two-copy tomography. Apply the inverse Fourier transform for a specified reference frame and measure return to the original input. A device locked to that frame returns with probability **1**; a uniform four-frame mixture gives **1/4** for a nonzero \(Q=0\) input; for \(x=(0,1,0)\), which has \(Q=2\), the result is **1/4** or **1/2** depending on whether the reference frame is the singleton or duplicated Fourier-character label. The program derives these values by exact modular-character coincidence, without fitted parameters. Actual photonic optical feedback and detector efficiency remain uncalibrated.

This is a strong **negative control** for any proposed one-photon W33 apparatus: observing all 729 flat intensities does **not** certify an ordered frame, a pure quantum Fourier output, or the correct phase relation. A phase-sensitive inverse-frame interference, two-copy purity/SWAP test, or calibrated density-matrix tomography can distinguish the classes. It is a concrete frame-selection witness within ordinary quantum theory, **not** a test of whether quantum mechanics is true or a new law of gravity.

## Scientific interpretation and priorities

The shared obstacle is not one more finite coincidence. Full projective symmetry makes frame selection nonunique; adding a physical spatial lattice makes the Ward identity standard rather than emergent; the perfect clock is noise-sensitive; 14 infinitesimal cubic symmetries do not certify all 86; and a corrected cosmological pipeline must not relabel forecast as observation. The strongest new synthesis is the **exact determinant-resolved frame-decoherence census**.

Five independent next decisive experiments:

1. Use a **spatially coupled frame Potts field** with real domain-wall tension, thermodynamic limit, susceptibility and experimentally testable Lorentz anisotropy; determine whether a stable ordered phase exists at admissible couplings.
2. Quantize the **selected-frame gauge-matter theory** with a consistent Gauss constraint, fermionic chiral content and Ward–Takahashi identities; establish a controlled nontrivial 3+1 continuum without assuming its measured constants.
3. Build a full 27-mode **optical netlist plus stochastic phase-noise calibration** and test the new four-frame purity classes; require output-state tomography and independent photonic data, not only ideal simulated intensities.
4. Reconstruct or export the full **78 E6 representation generators**, test every non-Cartan generator on the exact signed cubic and the proposed scalar interaction, then evaluate symmetry-breaking vacuum moduli and CP loops.
5. Complete **corrected, fully held-out DES/KiDS survey inference** with external raw data, covariance and alternative nonlinear prescriptions; preserve prospective S9 irrespective of its later score.

### Reproduction

Run `py -3 analysis/w33_20261108_five_followthrough_plus_coherence.py` and `py -3 -m pytest -q tests/test_w33_20261108_five_followthrough_plus_coherence.py`. CI regenerates the JSON and verifies all scientific layer boundaries. The clean checkout of the connected repository carries no all-generator E6 basis export; absence is explicitly recorded, never converted to a pass.
