# Five independent TOE falsifiers: native qutrit three-time memory, SIC vacuum moduli, real G2, causal orientation, and calibrated SU3 loops

**2026-11-19 | Tested mathematical/quantum toy results, NOT a physical TOE.** GitHub intake was master `f287b72a87e2d8e2c1c670b3e320937d31f8b98b`, after parallel commit `0fc4aca` (engineered SU3 SIC vacuum and qubit memory) and `f287b72` (coupled H27 BPS wall with natural 1D Hessian index **one**, not three). The 3-family noncompact Pascal selector still does not solve compact chirality or anomaly inflow. Review of repo prior art also found `analysis/2026-11-19_SIC_SU3_Plucker_Hesse_baryon_selector.md` and `analysis/toe_20261118_qutrit_genuine_multitime_block_lift.py`; accordingly we do NOT claim to have invented the existing nonholomorphic SIC alignment or qubit-block qutrit embedding. This packet goes beyond both in specifically identified ways.

## 1. Genuinely three-level qutrit three-time-only quantum memory (constructive, not block embedding)

Let `d=3`, `B={|j>}` computational basis, and `C={F_3|j>}` discrete Fourier mutually unbiased basis. Define complete dephasing maps `D_B` and `D_C`. Our three channels are

    E1(rho) = (1-gamma) rho + gamma |0><0| Tr rho
    E2(rho) = D_B(rho)
    E3(rho) = D_C(rho),  0<gamma<=1.

The full 3-dimensional output space participates in both dephasings. There is no invariant spectator qubit block. All three are CPTP. The source theorem, **Beyer et al., Observation of Genuine Multi-Time Quantum Memory** arXiv:2611.17268 Supplement VI Eq. S38, applies to two MUBs in general dimension:

    W3^(d) = F2(B) + F3(C) - (1/2)||E1(I)-I||_1 >= 0

for any **single classical-memory model** explaining all three maps. Here `F2=F3=0` because the respective basis preparations remain orthogonal, while `E1(I)-I=gamma diag(2,-1,-1)` has trace norm `4gamma`. Hence

    W3^(3) = -2 gamma < 0 (gamma>0).

**All three pairs DO have explicit classical-memory explanations**:

- `(E1,E2)`: an E1 instrument with `K0=sqrt(1-gamma)I` and jumps `K_j=sqrt(gamma)|0><j|`; after K0 apply D_B; after jump j prepare `|j>`.
- `(E1,E3)`: the same E1 channel with jumps `K_j=sqrt(gamma)|0><c_j|`; after K0 apply D_C; after jump j prepare `|c_j>`.
- `(E2,E3)`: represent E2 as a uniform random unitary `Z^k/sqrt(3)`. Conditional on k, undo `Z^k` and apply D_C. This yields exactly E3.

The full 9x9 Choi matrices of all three reconstructions agree with their targets to machine precision for `gamma=.05,.36,.75`. **One common physical quantum-memory realization** also exists: use an environment of dimension 4 and extend each channel's Stinespring isometry to a 12x12 unitary `U_i`. Apply sequentially `U1`, then `U2 U1†`, then `U3 U2†` on the same S3⊗E4. Without an intermediate intervention, these reproduce exactly E1,E2,E3. 24 random density matrices at each gamma verify the actual output reductions within 1e-12, and all intertime global propagators are unitary to 1e-12. This is a finite common process construction, not just an incompatible channel list.

**Physical/H27 cross-constraint:** E2 and E3 are covariant under the qutrit Heisenberg shift X and clock Z, but E1 is necessarily not. An H27-covariant qutrit CPTP map satisfies `E(I)=I` by Schur's lemma applied to the irreducible shift/clock representation and trace preservation. Therefore its first-channel nonunitality witness `S1` vanishes. This specific witness requires H27 symmetry breaking at the first time; *other* memory witnesses may work for exact-H27 channels. This gives the W33 single-photon/time-bin architecture an explicit experimental choice between preserving exact H27 covariance and witnessing nonunital temporal memory. No actual photon device or beyond-QM prediction follows.

## 2. Gauge-invariant SIC Welch alignment: quantifying the remaining flat directions

The repository already has a positive, gauge-invariant nonholomorphic SU3 SIC alignment potential and Hesse/Pluecker baryonic line discriminator (see prior-art path above). We independently test a more universal **Welch 2-frame** functional for nine unit qutrit species:

    FP2({psi_j})=sum_(j,k)|<psi_j|psi_k>|^4 >= N^2/[d(d+1)/2] = 13.5

(the bound is established frame theory). All tested Weyl-Heisenberg SICs reach 13.5, whereas the nine rays of three mutually unbiased qutrit bases give FP2=15. Every SIC is D-flat as an equal-norm nine-fundamental frame (sum projectors=3I).

**The obstruction**: the Hesse fiducial `(0,1,-exp(it))/sqrt(2)` generates a continuous 1-parameter family of nine SIC rays, all minimizing FP2, with gauge-invariant labeled Bargmann triangle

    Tr(P_0 P_3 P_6) = -exp(-3it)/8.

The value varies with t, proving these labeled configurations are not removed merely by a common SU3 gauge rotation. A finite relabeling group cannot remove a continuous family of values. In the `(CP²)^9` projective tangent space of 36 real dimensions, the exact linear variation of the rank-2 symmetric design frame operator is a real 81-by-36 Jacobian with computed **rank 26, nullity 10** (symmetric reduced space equivalent). Eight null directions are SU3 gauge orbit directions; one additional independent, exactly integrable Hesse-family direction is verified. The tenth infinitesimal null direction might be higher-order obstructed; we do **not** claim two continuous nongauge moduli. In the full scalar field description, arbitrary individual species phases add yet more flatness unless extra interactions lock them.

Thus replacing 19 hand-chosen baryon target constants with generic nonholomorphic Welch alignment can select a class of SIC geometries over the MUB configuration but cannot by itself supply an isolated, supersymmetric, full-rank physical mass matrix. A holomorphic gauge-invariant UV potential, phase locking, E8 messenger spectrum and quantum stability are still missing.

## 3. Exact real G2 Lie algebra and the limits of the complex E6 pencil

Construct the standard seven signed Fano triples of a positive real 3-form phi on R7. The infinitesimal invariance equation `X·phi=0` has 35 independent equations for the 49 entries of a 7x7 matrix. SymPy exact rational linear algebra finds **rank 35, nullity 14**. Every generator is skew; all `C(14,2)=91` commutators close inside the 14-dimensional subspace. On the real traceless-symmetric 27 representation, generated variations `delta h=Xh+hX^T` preserve both `C0=Tr(h^3)` and `Cphi=phi phi hhh` within ~2e-8 numerical finite-difference error over random test tensors.

This independently verifies the **real G2 stabilizer subalgebra**. Grigorian, *Exceptional cubics on 7-manifolds*, arXiv:2611.21589, proves separately that the complex critical pencil at `(1±i sqrt(7))/8` has 78-dimensional complex E6 stabilizer and constructs suitable Euclidean/compact real forms after additional structure. We have NOT reconstructed that 78-dimensional stabilizer or derived a 7D charged Dirac operator, global compactification, a 4D chiral index, Einstein dynamics or particle masses. Do not confuse the action of a real 14-dimensional G2 on the original metric-mode bundle with the larger complexified exceptional symmetry.

## 4. Causal order orientation disappears under undirected Hasse and inverse Frobenius spectra

Enumerate all `2^10=1024` forward-edge presentations on 5 preordered events and take transitive closures (357 different naturally labeled closures), then identify isomorphic orders across the 120 event permutations. There are **63 nonisomorphic five-event posets**. Direct order reversal partitions them into **15 self-dual types** and **24 distinct non-self-dual pairs** (48 types). Surprisingly, these 63 types have only **14 distinct undirected Hasse graphs up to isomorphism**, and hence 14 undirected Hasse-Laplacian spectra.

For any finite poset P, the cover adjacency H(P) transposes under reversal. The undirected graph `H+H^T` is unchanged; even the *directed* previous inverse-response

    R(P)=||(mI-alpha H)^(-1)||_F^2

satisfies `R(P)=R(P^op)` exactly, because transpose commutes with inversion and preserves Frobenius norm. Verified for all 63 classes at m=1.3, alpha=.6. An explicit star with 3 minimal elements has a dual with 4 minimal elements: they are not isomorphic, yet have identical undirected Hasse and inverse responses.

This is **not** a no-go for a CPT/time-symmetric gravitational action. It is a strict information-loss result: those scalar spectra cannot themselves orient time or infer chirality. Physically directed boundary states, spin-connection/transport data and a valid Lorentzian causal structure must be provided. A new ad hoc spectral penalty is not yet an Einstein action.

## 5. SU3 four-setting interferometer calibration—and a detector-mode gauge falsifier

Let the commutator holonomy be `K=ABA†B†` and assume a balanced reference fringe

    p_theta=1/2 + (v/6) Re[exp(-i(theta+delta)) Tr K].

With two settings for target K and two for the identity holonomy I3, define

    z_target=3[(2p_target,0-1)+i(2p_target,pi/2-1)]
    z_ref=(2p_ref,0-1)+i(2p_ref,pi/2-1).

At infinite samples these satisfy `z_target=v exp(-i delta_target)Tr K`, `z_ref=v exp(-i delta_ref)`. Therefore `z_target/z_ref=exp[-i(delta_target-delta_ref)] Tr K`. An identity-loop reference cancels **common** visibility and common phase offset, but cannot remove differential drift. With v=.8, delta_ref=.4, target 10,000 accepted detections per phase and identity reference 3,000 per phase, seeded 5000-repetition Bernoulli simulations give RMS complex trace error ~**0.0573** for common phase and **0.1860** with an extra .2-radian target drift. A union-of-four-Hoeffding upper bound provides a conservative (not optimized) 99% error certificate under the IID model.

The deeper failure is *unequal internal-mode readout*. A color-weighted detector measuring `3 Tr(eta K)/Tr eta`, with fixed lab-frame `eta=diag(.4,1.0,1.6)`, can change under `K -> U K U†` even though `Tr K` cannot. Across 64 random SU3 frame rotations the maximum spurious deviation was ~**0.804**, but the identity-loop fringe was identical for every frame (the identity commutes with any eta). Thus **identity calibration alone does not restore gauge invariance when detector coupling is not proportional to I**. A genuine device must implement color/mode-insensitive detection, or transport/tomographically calibrate the detector effects in the same internal gauge frame.

All of this is conservative classical measurement theory for prescribed SU3 matrices, not an implemented photonic holonomy generator, dynamical Yang-Mills action, or distinct quantum prediction of a TOE.

## Reproduction

Run the five producers (NumPy, SciPy and SymPy):

    python analysis/toe_20261119_native_qutrit_three_time_hierarchy_v2.py
    python analysis/toe_20261119_SIC_Welch_moduli_obstruction.py
    python analysis/toe_20261119_G2_real_form_14_generator_certificate.py
    python analysis/toe_20261119_causal_Hasse_oriented_spectral_obstruction.py
    python analysis/toe_20261119_SU3_reference_calibration_gauge_frame_falsifier.py
    python -m unittest discover -s tests -p test_toe_20261119_native_qutrit_SIC_G2_causal_SU3_v2.py -v

Five JSON data certificates have the corresponding code stem names (see data/). Machine-independent formulas and externally established theorems are marked separately from new finite computations.

## Five nonsequential best next steps

1. **E8-to-SIC UV:** Replace 19 engineered baryon constants with a minimal E8-compatible gauged multiplet/superpotential whose quantum corrected F/D vacua select a SIC orbit. Use the explicit Welch nullity and species-phase test to catch unwanted massless fields; derive anomalies and masses, not only gauge-invariant polynomials.
2. **Four-dimensional causal gravity:** Derive a directed spinor/causal propagation scheme whose physically oriented observables are well defined on poset isomorphism classes while its quantum action remains appropriately time-reversal compatible. Check 4D sprinkling scaling, unitary Hilbert evolution and nonmanifold entropy, not just Hasse spectra.
3. **Actual G2/E6 charged chiral index:** Choose the Euclidean/compact real structure from Grigorian's construction, define an honest charged Dirac operator on a specified compact singular G2 manifold, and compute flux/defect index with anomaly inflow. Do not substitute 14 Lie generators for physical chiral matter.
4. **Native qutrit experiment:** Compile the exact three channels and classical pairwise instruments onto time-bin/OAM qutrit optics; implement the single S3⊗E4 memory dilation, probe true intermediate interventions, and test a nonzero W3 with calibrated SPAM/loss and an H27 symmetry-breaking control.
5. **Gauge-invariant SU3 metrology:** Design detector color-twirl/randomized measurements that eliminate `Tr(eta U K U†)` bias, incorporate interleaved target/identity calibration and phase drift statistics, and derive a finite-shot confidence certificate for actual noncommuting photon transport.
