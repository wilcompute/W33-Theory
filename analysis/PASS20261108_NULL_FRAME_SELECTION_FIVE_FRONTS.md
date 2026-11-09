# A selected null frame simultaneously solves static exact mixing and produces a two-transverse-mode spatial Maxwell scaffold

**2026-11-08, 20:xx US Eastern (2026-11-09 UTC)**. Scientific status: **exact finite-dimensional construction + conditional field-theory/engineering examples**. Not a completed Theory of Everything, physical Lorentz emergence, verified E6 vacuum or observational dark-energy discovery.

Files:
- Producer: `analysis/w33_20261108_null_frame_selection_five_fronts.py`
- Regressions: `tests/test_w33_20261108_null_frame_selection_five_fronts.py`
- Machine certificate: `data/w33_20261108_null_frame_selection_five_fronts.json`
- Focused CI: `.github/workflows/w33_20261108_null_frame_selection_five_fronts.yml`

## Prior-art and compatibility audit

This starts from the native \(\operatorname{Sym}_2(\mathbb F_p)\) history carrier, \(Q(a,b,c)=ac-b^2\), originally \(p=3\). It is an explicitly **symmetry-reduced extension** of PASS20261108_LORENTZ_CHIRP_ESCAPE and PASS20261108_PRIMEFIELD_PHOTON_FIVE_FRONTS, not a contradiction: the earlier no-go excludes exact flat mixing for **time-independent, translation-invariant, full SL2-congruence-covariant** strictly null-supported generators at \(p\ge5\), whereas the Hamiltonian below is **inhomogeneous**, and singles out three null directions. Our previous complex homogeneous 24-parameter \(p=5\) search (MSE \(1.1358\cdot10^{-5}\)) did not include this family.

Tensor-product Fourier transforms, their polynomial Hermitian logarithms and cubic-lattice electrodynamics are standard tools. The contribution is an **explicit reuse of one three-null-direction frame on the native finite quadratic carrier**, the exact locus of symmetry breaking, optical resource counts, and a machine-verifiable comparison to the earlier obstructions. We claim no priority or novelty for the elementary Fourier factorization itself.

## Front 1: exact homogeneous-obstruction escape with ONE static Hamiltonian

The three chosen, linearly independent, projectively null vectors are
\[
d_1=(1,0,0),\quad d_2=(1,1,1),\quad d_3=(0,0,1),\qquad Q(d_i)=0.
\]
They give an invertible chart
\[
(a,b,c)\ \mapsto\ a d_1+b d_2+c d_3=(a+b,b,b+c)
\]
on the \(p^3\) native points. Denote the unitary discrete Fourier matrix by
\[
(F_p)_{j,k}=p^{-1/2}\zeta_p^{jk},\quad \zeta_p=e^{2\pi i/p}.
\]
Its eigenvalues belong to \(\{1,i,-1,-i\}\), since \(F_p^4=I\). The spectral projectors and one explicit Hermitian matrix logarithm are
\[
P_\lambda={1\over4}\sum_{r=0}^{3}\lambda^{-r}F_p^r,\qquad
h_p=0P_1-{\pi\over2}P_i+\pi P_{-1}+{\pi\over2}P_{-i}.
\]
Directly, \(h_p^\dagger=h_p\) and \(e^{-ih_p}=F_p\).

Construct the **single constant Hamiltonian**
\[
\boxed{H_p=h_p\otimes I\otimes I+I\otimes h_p\otimes I+I\otimes I\otimes h_p.}
\]
Each off-diagonal term connects only two points whose coordinate labels differ in **one** of the three selected null directions. Therefore **all nonzero off-diagonal couplings satisfy \(Q(x-y)=0\)**. Because the three tensor summands commute,
\[
\boxed{e^{-iH_p}=F_p^{\otimes3}},\quad
\left|(e^{-iH_p})_{x,y}\right|^2=p^{-3}\quad\forall x,y.
\]
No sequential time-dependent switching is required: it is an exact **static** null-local mixer. Crucially, at \(p=3\) the producer also imports the original native 27-point/108-edge graph (`analysis/w33_20261108_s4_harmonic_qdual.py`) and independently certifies that the **81 active hopping edges are an exact subset of its 108 edges**. It is not an unrelated replacement graph. The code reconstructs the full \(p^3\times p^3\) matrix for \(p=3,5,7\), checks Hermiticity and every off-null matrix entry, and certifies all amplitudes to machine tolerance.

| Prime p | Modes | Off-diagonal null-couplings used | Target probability |
|---|---:|---:|---:|
| 3 | 27 | 81 | 1/27 |
| 5 | 125 | 750 | 1/125 |
| 7 | 343 | 3,087 | 1/343 |

**Exact noncontradiction:** \(h_p\) is not invariant under even a unit coordinate shift. The program certifies a nonzero translation commutator. Consequently \(H_p\) does **not** possess the homogeneous translation covariance that previous no-go theorems assumed. There is no claim of full SL2 or GL2 congruence symmetry, homogeneous causal physics, speed of light, or physically determined Hamiltonian energy.

### How much symmetry is deliberately sacrificed?

The projectivized isotropic cone has \(p+1\) null directions, with natural \(\operatorname{PGL}_2(\mathbb F_p)\) action on \(\mathbb P^1(\mathbb F_p)\). An unordered triple of distinct projective null directions constitutes a basis. PGL2 is sharply 3-transitive on ordered triples, giving
\[
\binom{p+1}{3}\text{ equivalent unordered frames},\qquad
|\mathrm{Stab}_{GL_2(p)}(\{d_1,d_2,d_3\})|=6(p-1).
\]
The producer **enumerates every GL2 matrix** at \(p=3,5,7\), independently recovering frame orbit sizes **4, 20, 56** and stabilizers **12, 24, 36**. The frame is an extra symmetry-breaking datum. The Hamiltonian can break the remaining setwise symmetries further. **Selection by the physical vacuum remains completely unexplained.**

## Front 2: Maxwell's two transverse branches, only after explicitly adding physical space and time

Use the **same selected three null-frame coordinates** as a **three-dimensional spatial cubic lattice**, spacing \(1/p\) on a unit 3-torus, and explicitly **introduce an independent continuous time coordinate** and a positive Maxwell electric/magnetic action. The three spatial edge fields give the exact Bloch curvature
\[
a_j(k)=e^{2\pi i k_j/p}-1,\qquad
K(k)=\|a(k)\|^2 I_3-a(k)a(k)^\dagger.
\]
For each \(k\ne0\), this is Hermitian positive semidefinite with eigenvalues
\[
\boxed{0,\;\|a(k)\|^2,\;\|a(k)\|^2.}
\]
The zero is longitudinal pure gauge, leaving **two transverse modes** after Gauss reduction. Three uniform Wilson loops remain at zero spatial momentum. Compare with the prior **unprojected** \(p+1\) null-edge channel model, which had \(p\) transverse branches per nonzero \(k\): choosing a frame removes the extra carriers.

The lattice oscillator frequencies (with explicitly assumed unit wave speed) satisfy
\[
\omega_p(k)^2=4p^2\sum_{j=1}^3\sin^2(\pi k_j/p)
\longrightarrow (2\pi)^2\|k\|^2
\]
for fixed integer lattice momentum \(k\) as \(p\to\infty\). The one-axis squared-frequency relative error at \(p=31\) is **0.00341870**.

**Physical boundary:** This is **standard 3+1 lattice Maxwell added as a model**, not its derivation from the native finite determinant. The latter has a 2+1 Lorentzian quadratic analogy. We have **not** derived a dynamical metric, continuous time, absolute speed \(c\), physical gauge coupling, charged matter, Lorentz invariance of full interactions, or a ground-state mechanism selecting the null frame. It is a mathematical *existence proof under explicit extra assumptions*, not an unconditional W33 derivation.

## Front 3: a native cubic anchor has insufficient information to stabilize E6

The earlier trial quartic \(V_0(\Xi)=\lambda\operatorname{Tr}[(\Xi^\dagger\Xi-v^2 I_3)^2]\) on \(\Xi\in\mathbb C^{81\times3}\) admits the complex Stiefel \(V_3(\mathbb C^{81})\), **477** real flat tangent dimensions. We reconstruct all **1620** signed native alternating cubic records and the associated generic 81-state mass matrix of rank **78**. The three-spurion bilinear completion reaches rank **81**.

Define the *candidate* native alternating contraction
\[
C(\Xi)=\sum_{(u,x,o,c)\ {\rm native\ record}}c\,\Xi_{u1}\Xi_{x2}\Xi_{o3}.
\]
Consider augmenting the potential by **one complex cubic-anchor constraint**
\[
V=V_0+\kappa|C(\Xi)-C_0|^2
\]
for one specified regular value \(C_0\). At a reproducible, full-rank orthonormal minimum \(\Xi_0\) with \(C_0=C(\Xi_0)\), the code constructs two independent **real tangent** changes of \(C\): column phase rotation (changes its phase) and an orthogonal-column deformation (changes magnitude). The complex constraint has local Jacobian real rank **two**. The regular minimum-level manifold hence retains
\[
477-2=475
\]
real dimensions. Even were the full **78** E6 gauge generators to act freely and remove that many tangent directions, at least
\[
\boxed{475-78=397}
\]
gauge-inequivalent flat directions remain. Two relative column rephasings, e.g. \((+\theta,-\theta,0)\), also leave **both** Gram and \(C\) exactly unchanged.

**Crucial conditional:** We have **not** verified that this particular signed-81-index contraction is invariant under all actual E6 generators on the adopted 81 representation; until its covariance is proven, it is only a *candidate interaction*. The count is a conditional model falsifier, not a physically allowed stabilized GUT vacuum. Nor are the native rank lift or an unconstrained determinant phase equivalent to SM fermion masses or radiative strong-CP protection. A genuine F/D-term potential and anomaly/one-loop calculation remains necessary.

## Front 4: optics and independent phase/loss diagnostics

For \(p=3\), the Fourier product on 27 single-photon modes can be implemented as **three families of nine parallel 3-mode DFT blocks**, one family per selected null coordinate. A generic 3×3 interferometer needs at most \(3\) two-mode mixing couplers plus phase shifts. A naive triangular interferometer synthesis therefore uses at most
\[
\boxed{3\times9\times3=81}
\]
two-mode mixing couplers, before layout optimization or insertion loss. This matches the number of supported undirected edge couplings in the static Hermitian implementation but is **not** proof that a chip exists or uses exactly that many physical components.

We derive two deliberately distinct calibration controls:

- **Relative-phase echo:** Insert a phase \(\delta=\pi/3\) on one of three equiprobable addresses and undo the preparation transform. The ideal return probability is
\[
P_{\rm echo}=\left|{2+e^{i\delta}\over3}\right|^2=\boxed{7/9}.
\]
Raw computational-basis intensities before interference would not reveal the phase; a calibrated Fourier-referenced echo does.
- **Rail-dependent loss:** Assign intensity transmissions \((0.98,1,1)\) to the first three equiprobable branches. Their mean survival is \(0.993333\ldots\), and the renormalized output distribution has a **nonzero** total-variation distance from uniform. A uniform attenuation of \(0.98\) across every branch lowers detection rate but leaves the **conditional** distribution exactly uniform.

The model reports these predictions explicitly and does not invent measured chip loss, source heralding, gate fidelity, detector efficiency, error thresholds or scalable multi-photon entanglement. **Single-photon factorization still requires \(3^n\) orthogonal modes for \(n\) independent logical qutrits.** Experimentally, Imany et al., *npj Quantum Information* **5, 59** (2019), DOI 10.1038/s41534-019-0173-8, demonstrated deterministic SUM logic within one photon in time/frequency modes but did not solve scalable photon–photon interactions.

## Front 5: corrected nonlinear dark-energy evidence and an independent flavor-clock filter

The producer independently re-reads the source-committed **six CLASS/Halofit scalar-field ΛCDM controls**, which reproduce ordinary ΛCDM within \(3\times10^{-6}\) relative error. It replays **six finite \((z,k)\) cells** of both patched Halofit and HMcode fading/CPL nonlinear-boost ratios, and the corrected DES Y3/KiDS **fixed-background** chi-square differences. At \(z=0.01,k=1\,h/{\rm Mpc}\), the patched fading-vs-CPL boost differences are approximately **+0.6% (Halofit) and +1.9% (HMcode)**. These are forward-model controls, **not** a new shear likelihood or physical calibration of interacting-dark-matter nonlinear evolution.

The old prepatch S7/S8 held-out shear rankings remain **withdrawn** after PASS12632. New refits, raw shear chains, cross-survey covariance or genuine parameter Bayes factors were **not executed** in this pass; the producer has an explicit `False` flag for independent held-out inference. It reads the revised fixed-background DES/KiDS scores with the previously reported sign reversal, without claiming either model wins statistically.

A new parallel Pass12633 tests whether dark energy can itself be a level-3 A4 flavor modulus. Its native mathematical texture has minimum modeled mass-ratio sensitivity \(S\approx4.225\) per \(M_P\) and atomic-clock proxy slope bound \(2.5017\times10^{-6}\). Under an assumed **linear inherited coupling**, its rolling-flavor admixture must obey
\[
|\epsilon| \lesssim {2.5017\times10^{-6}\over4.225}\approx5.92\times10^{-7}.
\]
The associated visible-to-dark coupling requirement, taking \(0.05\) for the illustrative dark coupling, is below \(5.01\times10^{-5}\). This is a **conditional proxy budget**, not a fitted or independently observed mixing angle; complete particle-mass dependence and cancellation mechanisms are not derived. Sources: `analysis/PASS12633_FLAVOUR_MODULUS_CLOCK.md` and `analysis/PASS12632_HALOFIT_SCF_BUG.md`.

## Sixth connection: one selected frame controls both dynamics and polarization

Choosing **three independent null directions** does something unexpectedly useful twice:

1. **Quantum clock:** it provides a strictly null-supported *static* Hermitian generator that reaches a perfect flat Fourier mixing in one unit of evolution.
2. **Spatial Maxwell scaffold:** it removes the growing \(p\)-channel surplus of the natural full-null orbit, giving exactly **two transverse modes** per nonzero momentum **when independent continuous time and a cubic spatial metric are supplied**.

This symmetry-breaking frame is not derived, unique, or necessarily preserved by interactions. In fact GL2 acts transitively on all \(\binom{p+1}{3}\) such unordered frames, and even the Fourier Hamiltonian breaks the residual homogeneous translation symmetry. There is no physical sense in which the standard Fp³ Fourier tensor factorization constitutes a new fundamental force. It is, however, a **precise falsifiable research direction**: derive a dynamical selection mechanism for this frame without spoiling its exact gauge/clock structure, and demonstrate a 3+1 continuum rather than merely declaring the finite quadratic space physical spacetime.

## Five orthogonal next steps

1. Derive a **dynamical E6/finite-Lorentz frame order parameter** that selects one null triple, with an actual bounded stable potential and mass gap; quantify explicit Lorentz-symmetry breaking and experimental constraints.
2. Solve a **time-continuum and Ward-identity problem**, adding charged matter to the 3-axis gauge scaffold and proving decoupling of all unwanted sectors under p→∞ at fixed physical scales.
3. Test **robustness of the inhomogeneous flat-mixer**: constrained controls, clock precision, sparse optical control schedule, and noise budgets; distinguish exact mathematical unitary from engineered error thresholds.
4. Certify E6 covariance of the **actual 81-index cubic tensor**, then construct F/D-term stabilization, CP/anomaly cancellation and RG-robust vacuum selection; the toy cubic anchor is currently conditional.
5. Run completely corrected DES/KiDS raw likelihoods across **both Halofit and HMcode** with cross-survey covariance and an interacting-dark-matter nonlinear uncertainty budget, while maintaining the Pass12632 withdrawals.

**Reproduce:** `py -3 analysis/w33_20261108_null_frame_selection_five_fronts.py` then `py -3 -m pytest -q tests/test_w33_20261108_null_frame_selection_five_fronts.py`. The focused GitHub Actions workflow separately regenerates the certificate and tests essential scientific claim boundaries.
