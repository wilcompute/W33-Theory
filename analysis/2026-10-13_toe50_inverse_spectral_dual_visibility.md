# TOE50 — Inverse-acoustic spectral fingerprint and exact even-Weil/spread dual decoder

**13 October 2026**. Baseline TOE49 final master merge bfd7fc4cc7e000679345580d0ff62b4629a869ac; current initial W33 head 2eabdc92fdcd0131623066e1c1016a6459946648. Approximately **127 intervening commits** including many repetitive Pass398 formula-index updates, multiple distinct science passes through 11961, hosted replay receipts, and an explicit retraction. Holotrade's current visible head remains b0264880d7c5fd24c6af932b892324247ab57808 (no changes since prior packet).

This is a focused *semantic* audit, not a dishonest assertion that all 127 patches, thousands of historical files or three large flagship papers received line-by-line manual review. Examined the full newest scientific reports Pass11949, Passes11950–11951, Passes11952–11956, Passes11957–11961; respective source dependencies including native Maxwell kinetic weight solver, SU5 threshold and gauged Z12 quality producer, charged-neutrino Clebsch fitter, TOE47 40 cusp even-Weil geometry, Pass3694–3700 spread ETF, and the 36-spread/40-line bridge. Searched old reports and current code for rediscovery before claiming a new bridge. Reviewed the most recent 36-spread suspension **retraction** and its replacement proof. The new packet adds two independently generated checks in entirely separate physics/mathematics fronts.

## Incoming results and necessary firewalls

- **Pass11949 retracts the axiflavon QCD-axion claim** because the epsilon² spurion violates PQ quality many orders above QCD. The new color-threshold / vectorlike-sector alternatives are *proposed models*, not completed strong-CP solutions.
- **11950–11951**: the up theta determinant has a cubic zero at the separating divisor. A regular holomorphic color gauge factor cannot make a nonzero globally phase-safe analytic product across that divisor; a pole z^-3 or separate Nelson–Barr mass architecture is required. The latter can reconstruct (not predict) input quark masses/mixing with real full 4x4 determinant and weak CP. Full loop/gauge matching is open.
- **11952–11956**: conditional native Maxwell electric weights select exactly two isotropic acoustic modes at omega²=2|k|², using a proved positive local root, while gravity is not obtained. A selected singlet sector is tree-positive, but a light singlet <=4.72 GeV at Lambda1e16 cannot automatically withstand TeV soft breaking.
- **11957–11959**: a declared SU5_color→SU3_color Higgs threshold supplies a *local* z^-3 holomorphic pole, not an E6 embedding or global modular completion; an E6×U1X×U1Z model plus spectator Z2 suppresses specified holomorphic leakage, but soft/Kähler terms remain. Fermion-box loops misalign equal portals. The most optimistic fixed-modulus benchmark upper-block leakage (~1.78e-12) is only an example envelope, not a proof of strong CP safety.
- **11960**: corrects physical CKM conjugation convention in the Clebsch/neutrino fit, preserving input J=+3.08e-5. Two real charged Clebsch coefficients and two further real Majorana offdiagonals *fit* lepton comparison targets, yielding multiple, mutually incompatible CP phases (~281°, 113°, 57°). This is flexibility, not prediction.
- **11961**: continuum ADM-class ansatz requires lambda=1/2 and ab=2 to match the supplied matter cone, but the discrete-native 160-link electric weights still have 154 local microscopic directions yielding the same six leading Gram coefficients. Existing non-Leibniz, dynamical-gravity and continuum-limit obstructions are not solved.
- **Latest retraction**: the 36-state spread fibre base is NOT the set of 40 rung-9 line-complement regions. Their stabilizers 720 versus 648 forbid an equivariant identification. The spectral bound on 36-point regions remains, but no map from hypervisor base to 36 retained points was built. This exact distinction is maintained below.

## TOE50 Front A: genuinely different microscopic geometry with EXACTLY the same light cone

Producer: analysis/w33_20261013_toe50_inverse_acoustic_spectral_trace.py.
Certificate: data/w33_20261013_toe50_inverse_acoustic_spectral_trace.json.

Build from the existing native marked W33 Maxwell 160-edge geometry. Let W=diag(w_e)>0 be the electric link weights and P(k) the **fixed native magnetic plaquette/commutator matrix**. The six independent entries of the Gauss-reduced weighted harmonic kinetic matrix G(w) are exact acoustic observables. Pass11956 proves there is a positive local root G=I3/2; Pass11961 proves its Jacobian has rank6 and therefore a local 154-dimensional level set. Those results are **prior repo facts**, not rediscoveries.

The new question: are those 154 microscopic directions physically invisible to all frequencies, or only to the leading acoustic tensor?

Use an independent higher-band observable at Bloch k=0:

    T(w)=Tr[W^-1 P(0)^dag P(0)]
        = Σ_e [P(0)^dag P(0)]_ee / w_e.

This equals the sum of all generalized squared magnetic normal-mode frequencies (including zero modes) in the pencil Pdag P u = omega² W u. Its differential is exact:

    dT/dw_e = - [Pdag P]_ee / w_e²,

while the Gauss-harmonic envelope theorem gives

    dG_ij/dw_e = h_ei h_ej.

Project the T gradient orthogonally off the six-dimensional span of G gradients. The projected tangent lives in the 154-dimensional kernel of DG. The result is **nonzero**: dT/dt≈1135.8275524, relative logarithmic slope≈0.10003249 (t is unit Euclidean link-weight perturbation).

For five displacements t=-.030,-.015,0,.015,.030, **nonlinearly adjust the original six free link weights** so G=I/2 exactly to machine precision at every t. All 160 weights stay >1/8. The trace changes:

| t | gapped spectral trace | max |G−I/2| |
|---:|---:|---:|
| -0.030 | 11321.0914123 | 2.3e-16 |
| -0.015 | 11337.6964435 | 1.2e-16 |
| 0 | 11354.5863762 | 8.4e-14 |
| +0.015 | 11371.7766095 | 3e-18 |
| +0.030 | 11389.2838350 | 1.2e-16 |

This **constructively proves local non-identifiability from the leading light cone but identifiability of at least one additional microscopic direction from a gapped spectral trace** for the supplied finite model. More precisely, the Jacobian rank of (G,T) is at least seven here. It does not identify all 160 link weights or imply physical gravity.

Relevance to physics: long-wavelength effective-medium matching erases microstructure; dispersive/band observables can retrieve additional information. This is an instance of inverse homogenization, which has substantial prior literature, e.g. [Dehomogenization of spectral measures](https://doi.org/10.1088/0266-5611/24/6/065008) and [Electromagnetic metamaterial parameter retrieval](https://doi.org/10.1103/PhysRevE.71.036617). **Novelty claimed only for this exact W33 Maxwell native construction and its frozen data**.

## TOE50 Front B: exact perfect complementary 40-line decoder from cusp operators and spread incidence

Producer: analysis/w33_20261013_toe50_dual_cusp_spread_decoder.py.
Certificate: data/w33_20261013_toe50_dual_cusp_spread_decoder.json.

Existing committed facts: TOE47 has the 40 even-Weil cusp rank-one projectors P_L on C5, indexed by W33 **LINES**, with Hilbert-Schmidt Gram

    G_cusp = (8 I+2 A_line+J)/9,

eigenspaces 8^1+(4/3)^24+0^15, real rank25. Independently, Pass3694–3700 and older point-line-spread bridge have **36 spreads**, each ten disjoint lines; every line lies in nine spreads. Let B be 40x36 line-by-spread membership. Existing spectral decomposition gives rank(B)=16, visible 1+15 and kernel24. These previous results belong to earlier repo authors.

New exact simultaneous identity on the COMMON 40 labelled W33 LINES:

    B B^T = 6 I -3 A_line +3 J.

Eliminating A_line yields the integer identity

    36 I = 3(9 G_cusp)+2 B B^T -9 J,

or

    **I40 = (3/4) G_cusp + (1/18) B B^T - (1/4) J.**

Let P0=J/40. A more revealing *positive orthogonal projector* decomposition is

    I = P0 + (3/4)(G_cusp -8 P0) + (1/18)(BB^T-90 P0).

The terms are mutually orthogonal projectors on dimensions **1,24,15**, respectively. Centered orthogonality is checked by pure integer arithmetic:

    [5(9G_cusp)-9J] [4BB^T-9J] = 0.

This is an exact Parseval-like *complementary visibility theorem*: given an arbitrary real 40-line signal y, its cusp Hermitian synthesis operator X=Σ_L y_L P_L, spread totals B^T y, and global sum determine y **uniquely** via the boxed identity. The combined readout rank is40. Fifty random real line-signal inversions gave maximum error 5.05e-15; exact integer identity and 36-spread cover were checked independently. It neither identifies 36 spreads with 36-point regions (retracted) nor implies extra physical measurements on an unknown two-qutrit density matrix. It unifies the older 1+24 cusp operator quotient with the prior 1+15 spread ETF in a single exact reconstructing frame on line-indexed data.

## Strong-CP / gravity / particle-physics status

The latest declared sectors remain separate EFT models. The color pole has not been derived from a compactified colored threshold spectrum; the Z12 singlet has unsolved soft stability, PMNS fit parameters and phases are selected rather than predicted, and finite lattice Maxwell light-cone data do not yield general relativity. This TOE50 packet adds two structural connections but **does not solve a Theory of Everything**. Retraction, prior-art boundaries, and observational/provenance restrictions are maintained. The principal physics opportunity is experimentally accessible *spectral discrimination* of otherwise acoustically indistinguishable geometries, and a principled exact multi-carrier measurement/intertwiner architecture.

## Verification

    py -3 -m pytest -q tests/test_w33_20261013_toe50_spectral_and_dual_decoder.py tests/test_w33_pass11957_11961_selection_completion.py tests/test_w33_pass11950_11951_strong_cp_completion.py

TOE50 tests regenerate both own certificates, check positivity/kinetic matching, exact cardinalities/ranks/decoder errors. Prior physics tests protect the most recent strong-CP and kinetic model dependencies. Stage only TOE50 named source, JSON and report; other agents have substantial unrelated tracked dirty changes and untracked research scratch files that must NEVER be included.

## Five best INDEPENDENT next steps

1. **Inverse-spectral W33 tomography:** add higher Bloch spectral moments at 3D wavevectors, rigorously determine rank increments beyond the six leading Gram entries, quantify shot/resolution/noise required to separate microscopic classes, and find any residual isospectral gauge freedoms.
2. **Build a genuinely physical vectorlike strong-CP completion:** embed the SU5_color z^-3 matching and parity-safe E6 sector into one UV and string-consistent model, include light singlet sequestering, all colored thresholds, soft/gluino phases and neutron EDM bounds.
3. **Derive rather than fit charged and neutral flavor:** demand a single stable scalar vacuum, anomaly-consistent Clebsch coefficients, neutrino Yukawas and Majorana textures; use real PMNS CP and neutrinoless double-beta constraints to distinguish branches.
4. **Formalize the dual decoder as a covariant compiler:** prove the 1+24+15 orthogonal projectors over the rational integral W33 line module, map the 25D even-Weil cusp operator channel and 36 spread channel into Holotrade's existing K81 carrier without conflating point/line objects, and compile physical optical error/coupler budgets if realizable.
5. **Native dynamical-gravity closure:** couple electric and magnetic link geometries to specified conjugate momenta, check discrete hypersurface-deformation brackets, constraints and continuum scaling before deriving any metric/graviton or a speed-of-light constant from W33.
