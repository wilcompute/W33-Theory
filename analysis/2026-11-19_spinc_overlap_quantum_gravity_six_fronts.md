# Five TOE "home-run" fronts executed, plus a sixth: spin-charge topology, overlap index, vacuum ambiguity, quantum gravity and Yang-Mills force

**2026-11-19 · physics-first working note.** Reproducible, falsifiable conditional mathematics on *supplied* torus, Clifford matrices, gauge links and continuum metric proxies. **NOT a Theory of Everything, a 4D quantum gravity model, a derivation of the Standard Model, or a new experimentally verified physical law.**

## Research question, collision audit, and conceptual shift

The problem is to find a microscopic principle that **forces** spin, internal gauge transport, physical quantum states, and a dynamical 3+1 spacetime rather than treating every sector as a separately fitted construction. This effort develops the five investigations specified in the previous pass:
1. intrinsic causal spin–gauge bundle;
2. physical Dirac operator and chiral representation;
3. canonical quantum state/vacuum selection;
4. dimensional selection and genuine gravitational dynamics;
5. charge, anomaly and holonomy prediction from global structure.

A sixth, independent front tests an actual SU(2) Wilson Yang-Mills variational force rather than just local loop phases. The strongest **new-to-this-repo cross-sector observation** is a simple arithmetic constraint combining a Spin^c quotient with the *two-dimensional* Abelian gauge anomaly; we give a non-vectorlike escape family showing how little this alone predicts.

We inspected recent GitHub commits up through 1260d6c3989e93a8fccc64fbf8fb35d41c1b817d and read existing files, notably:
- analysis/2026-11-19_causal_spectral_eight_homerun_gates.md — eight earlier finite chiral, holonomy, causal vacuum, and gravity consistency gates.
- analysis/toe_20261119_spectral_exchange_seven_gates.py — Wilson versus naive Dirac and exact SM anomaly arithmetic *with supplied representations*.
- analysis/toe_20261105_causal_growth_without_background.py — transitive-percolation does not select robust dimension four from the order alone.
- analysis/toe_20261105_causal_poset_measure_correction.py — fixed-label DAG presentations bias causal histories by multiplicities 2^(R-L).
- analysis/BT1033_spectral_action_term_by_term_geometric.md and analysis/bt1140_seeley_dewitt_a4_convention_split.py — the spectral/heat-kernel route is already present, so we do not pretend to have originated a unified Dirac-squared/spectral action.
- analysis/toe_20261113_gauge_729_wilson_dirac.py — preexisting Wilson/Dirac lattice experiments.

This packet is a **new independent overlap-operator/index and global representation bridge** with explicit tests that existing scripts lacked, plus actual quantum and gauge-action counterexamples. As the literature confirms, overlap/Neuberger chirality, spin^c, anomaly sums, two-dimensional Gauss-Bonnet and Wilson gauge actions are extensive established prior art.

**Concurrent-commit collision audit (updated before publication).** Commit ff5090ff5469e1b48c3cdd467c24632a0064c1fd landed during this session. We read its full report, analysis/2026-11-19_TOE_global_toric_spin_c_causal_pure_state_gates.md. It already derives a pure-squeezed-state vacuum ambiguity and a separate Spin^c characteristic index formula on supplied CP², as well as E8 singlet, SU5 fine-tuning, causal-link nonlocality and photonic noise tests. We treat those as independent parallel corroboration, NOT our original discovery. The present packet is distinct in its **actually constructed finite 2D and 4D overlap matrices**, lattice-resolution counterexamples, the elementary *2D* Spin^c parity plus mod-8 anomaly congruence, independent GF2 cubical torus calculation, numerical Regge deficit variation, and explicit SU2 Wilson-action gradient descent. No 3-family claim or full global anomaly cancellation is inferred from either packet.

## Front I — Spin structures: cohomology is not yet an intrinsic causal spin bundle

Construct the periodic 3x3 cubical spatial torus as an honest cellular chain complex over F2. It contains V=9 vertices, E=18 edges and F=9 squares. We build both boundary matrices explicitly, confirm partial_1 partial_2=0 over F2, and compute ranks

    rank(partial_1)=8, rank(partial_2)=8,
    Betti_F2(T²)=(1,2,1).

Once an **oriented smooth torus and some base spin structure are supplied**, its spin structures form a torsor for H¹(T²,Z2)≈(Z2)^2. Thus there are **four** spin structures (periodic/antiperiodic choices on the two noncontractible cycles).

This is stronger than counting an unconstrained lattice Dirac spectrum; it checks the cohomology classifying *global spin lifts*. However, the cubical torus and orientation are supplied. The causal partial order alone does **not** select the torus, its spin lift, or the physical spin representation. This is a clear missing ingredient of the putative causal groupoid.

Source: standard spin/spin^c theory, https://en.wikipedia.org/wiki/Spin_structure ; https://georgedouzas.github.io/posts/fundamentals-of-mathematics-for-physicists/part-i-13-spinors-dirac-operator.html .

## Front II — An actual topological/chiral lattice operator, not just Wilson's doublers

Construct a Euclidean two-dimensional periodic lattice with externally specified U(1) gauge transport. In the gauge chosen here,

    U_x(x,y)=exp[-2pi i Q y / L²],
    U_y(x,L-1)=exp[2pi i Q x/L],
    U_y(x,y<L-1)=1.

Each plaquette has phase exp(2pi i Q/L²), so the discrete total magnetic flux is exactly the integer Q.

A Wilson-Dirac operator D_W is constructed with gamma_x=sigma_x, gamma_y=sigma_y, Wilson parameter r=1 and all required forward/backward gauge links. Define

    H_W = gamma5 (D_W - m0), m0=1;
    D_ov = I + gamma5 sign(H_W).

The overlap operator obeys the Ginsparg-Wilson lattice chiral identity

    gamma5 D_ov + D_ov gamma5 = D_ov gamma5 D_ov,

and has topological index

    index(D_ov) = Tr[gamma5(1-D_ov/2)]
                = -(1/2) Tr sign(H_W).

Our gamma/flux conventions give index=-Q. We construct the *entire dense matrix* and diagonalize the Hermitian kernel, rather than imposing the expected result by fiat. Results:

| L | Inserted total flux Q | Numerical index | GW Frobenius residual |
|---:|---:|---:|---:|
| 6 | 0 | 0 | 5.6e-14 |
| 6 | +1 | −1 | 5.8e-13 |
| 6 | −1 | +1 | 3.3e-13 |
| 6 | +2 | −2 | 5.4e-14 |
| 6 | −2 | +2 | 5.5e-14 |
| 8 | +3 | −3 | 6.3e-14 |
| 8 | +5 | −5 | 1.4e-13 |

The kernel has a strictly nonzero spectral gap in every tested sector (minimum 0.7442). We apply an arbitrary independently sampled U(1) frame change at **every** lattice site, verify the overlap operator conjugates covariantly to within machine tolerance, and check that a global pi winding removes zero modes from a *trivial-flux* sector without changing its index. Flux in a unit-charge background and integer charge in unit-flux background enter the same first Chern number product; our +3,+5 cases exemplify the higher-charge effect.

**Important:** This is a vectorlike Euclidean 2D overlap operator. Its exact modified chiral symmetry and integer index do NOT themselves construct an interacting 4D anomaly-free Weyl Standard Model. The 2D torus, links, gamma matrices, Wilson regulator and topological sectors were all INPUTS. A full Lorentzian causal-set operator, chiral measure and correct infrared locality remain open.

Prior art: overlap index numerical results https://doi.org/10.1143/PTP.107.163 ; Ginsparg-Wilson symmetry https://doi.org/10.1103/PhysRevD.109.014502 ; Luescher gauge-invariant anomaly-free lattice chiral construction https://doi.org/10.1016/S0550-3213(99)00115-7 ; 2026 K-theoretic index analysis https://doi.org/10.1007/s11005-026-02080-w .

## Front III — Even purity plus the exact canonical commutator cannot select a unique quantum state

The previous finite causal-set Sorkin-Johnston gate proved that positivity and the commutator alone do not identify a unique two-point state: W_SJ+epsilon I preserves the commutator. One might argue that **purity** removes the ambiguity. Here we test that explicitly and show it does not.

For one canonical bosonic mode [q,p]=i, let

    J = [[0,1],[-1,0]],
    V(r) = diag(exp(2r),exp(-2r))/2,
    W(r) = V(r) + i J/2.

For every real squeeze r, W(r) is Hermitian positive semidefinite, has fixed W-W^T=iJ, and det V=1/4, saturating the Heisenberg uncertainty bound: the state is pure. Yet the state two-point function and oscillator energy differ:

| Squeezing r | <q²> | <p²> | Energy under H=(p²+q²)/2 |
|---:|---:|---:|---:|
| 0 | 0.5000 | 0.5000 | 0.5000 |
| 0.5 | 1.3591 | 0.18394 | 0.77154 |
| 1.0 | 3.6945 | 0.06767 | 1.88110 |

Selecting a lowest-energy vacuum **does** distinguish states, but requires an external Hamiltonian and preferred time generator. For a frequency-four oscillator H_4=(p²+16q²)/2, the ground covariance is diag(1/8,2), not the unit-frequency vacuum, and has energy 2. Therefore "order + commutator + positivity + purity" cannot be a complete vacuum selection law without additional dynamics/symmetry.

This does not disprove Sorkin-Johnston (SJ): it provides a global distinguished-state prescription by additional spectral principles, and the literature has explored both uniqueness principles and ultraviolet/Hadamard subtleties. Our squeezed example is a finite canonical counterexample, not an interacting causal-set vacuum or Born-rule derivation.

Prior art: https://doi.org/10.1007/s41114-019-0023-1 ; https://arxiv.org/abs/2412.07832 ; https://doi.org/10.1088/1751-8121/ad7427 .

## Front IV — Real gravitational action and the dimension attractor: a mathematical roadblock

The 2D Regge version of Einstein-Hilbert curvature is topological by Gauss-Bonnet. We construct a periodic 3x3 triangulated torus with V=9, E=27, F=18 and randomly perturbed **shared triangle edge lengths**, such that many local curvature-deficit angles are genuinely nonzero. Still,

    sum_v delta_v = 2pi chi(T²) = 0,

with computed residual |sum delta| < 1e-14. For a tetrahedrally triangulated 2-sphere the same calculation gives sum deficit =4pi. As an invariant, the integrated scalar curvature cannot provide local, propagating 2D Einstein gravitational equations. The project must demonstrate an actual 3+1 Lorentzian Einstein/graviton limit, not infer one from a 2D spin connection or spectral curvature coefficient.

For the **unembedded causal growth** control we reran the previously implemented metric-free transitive-percolation generator at n=220, varying precursor probability p. Resulting median Myrheim-Meyer dimensions of eligible finite causal intervals:

| p | Eligible intervals in this finite run | Median reconstructed dimension |
|---:|---:|---:|
| .025 | 6 | 2.024 |
| .065 | 253 | 2.165 |
| .150 | 560 | 1.613 |

These are parameter-sensitive finite-sample outcomes; the p=.025 sample has only six eligible intervals and is not a reliable asymptotic estimate. **We do not conclude 4D can never emerge.** Rather this particular growth law has not shown robust 4D emergence. An intrinsic quantum measure over unlabeled posets with a controlled manifoldlike continuum and GR remains unconstructed.

Prior art: 2D Regge/Gauss-Bonnet https://www.physik.uni-leipzig.de/~janke/Paper/cmp9_263_2006.pdf ; causal-set emergence and nonmanifold suppression https://doi.org/10.1007/s10714-024-03281-1 ; Benincasa-Dowker action https://journals.aps.org/prresearch/abstract/10.1103/qdst-yrh6 .

## Front V — New-to-repository cross-sector filter: Spin^c charge parity meets the 2D gauge anomaly

A Spin^c(n) structure uses the quotient

    Spin^c(n)=[Spin(n) x U(1)] / { (1,1),(-1,-1) }.

Let the central -1 of Spin act as (-1)^F, and let an integer-character U(1) representation of weight q give (-1)^q on the -1 element of U(1). The representation is well defined on the **quotient** only if

    (-1)^(F+q) = +1.

Thus in this normalization elementary fermionic spinors require *odd* q, while integer-spin bosonic representations require *even* q. This is the established "spin-charge relation", **not** automatically the electromagnetic charge lattice of our universe. The 4D SM has additional global quotients, color and weak representations and differently normalized hypercharges.

Combine this parity law with the established **1+1-dimensional** chiral U(1) gauge anomaly condition

    sum_(left fermions) q_L² - sum_(right fermions) q_R² = 0.

For every odd integer q, q²=1 (mod 8). Consequently:

    0 = sum_L q_L² - sum_R q_R²
      = N_L - N_R (mod 8).

**Necessary congruence:** N_L-N_R must be divisible by 8, *assuming every Weyl fermion's integer U1 charge is odd because this U1 is the actual Spin^c quotient factor*. This is a short elementary deduction under *specific* global/2D assumptions, not a universal chiral fermion counting theorem.

Crucially the constraint is not sufficient to select or ban chiral physics. One explicit **non-vectorlike, perturbatively anomaly-free** odd-charge spectrum in two dimensions is

    Left q=(1,7) : sum q²=1+49=50
    Right q=(5,5): sum q²=25+25=50.

The left/right charge multisets are unequal but cancel their U1 gauge anomaly. They also have equal chirality counts, avoiding the perturbative 2D gravitational anomaly count. There can still be extra global, representation or dynamical restrictions. **The charges were selected, not predicted.**

This is the most speculative but focused physics connection in the current packet: global bundle quotient conditions restrict a chiral gauge anomaly cancellation problem, and the overlap index can independently check flux/chirality consistency on supplied backgrounds. An actual TOE would need a unique microscopic reason to choose the quotient, group, spectrum and physical spacetime dimension.

Sources: spin-charge relation https://andrea-cappelli.github.io/theses/villa.pdf ; 2D anomaly cancellation equation https://academic.oup.com/ptep/article/2019/7/073B02/5532742 ; chiral lattice construction https://doi.org/10.1016/S0550-3213(99)00115-7 .

## Bonus front VI — From passive Wilson loops to an actual local SU(2) Yang-Mills force

Parallel results had established that noncommuting SU2 link matrices can create nonzero plaquette curvature. That is **kinematics**. Here we additionally define the traditional *dynamical* lattice Wilson action on a periodic 3x3 network,

    S[U] = sum_plaquettes [1 - (1/2) Re Tr(U_plaquette)].

With randomly seeded nontrivial SU2 links we verify invariance under independent gauge-frame transformations at all nine sites. Then compute the finite-difference derivative of S with respect to the three Lie-algebra generators on one selected link and **actually update that link down the action gradient**:

    initial S=1.844380512762571
    one-step final S=1.828936884706812
    delta S=0.015443628055759
    local gauge-frame action error <5e-16
    magnitude of one-link Euler-Lagrange force =0.337522816512.

The link remains unitary. This demonstrates a working force/action variation rather than assuming holonomy supplies dynamics automatically. The group, lattice, Wilson action and step rule were **inserted**; we did not derive SU(2), Yang-Mills Lagrangian, the Standard Model currents or its physical coupling.

## Further executed seventh gate — genuine four-dimensional U(1) index versus lattice resolution

We extended the topological chiral test beyond the 2D Schwinger-model setting to a **4D Euclidean U(1) background** with nonzero flux through two orthogonal 2-tori. This is a considerably more demanding fermionic topology check.

We construct the full four-gamma Euclidean Clifford algebra, a 4D Wilson-Dirac operator on a periodic L^4 torus, its Hermitian gamma5 Wilson kernel and overlap index. Choose integer fluxes Q12 and Q34 inserted through the 12 and 34 planes and no flux elsewhere. The smooth continuum index/Chern-character formula on this background is

    (1/(8 pi²)) integral_(T4) F wedge F = Q12 Q34.

The resulting finite matrix dimension is 4L^4, i.e. 64 for L=2 and 324 for L=3. Rather than presupposing the continuum index, we compute the actual spectrum of gamma5(D_W-m0) with m0=1, evaluate index=-(1/2)Tr sign(H), and construct the full overlap matrix and verify Ginsparg-Wilson for the nontrivial (Q12,Q34)=(1,1), L=3 example.

| L | Q12 | Q34 | Continuum Chern product | Actual finite overlap index |
|---:|---:|---:|---:|---:|
| 2 | 1 | 1 | +1 | **0** |
| 3 | 0 | 0 | 0 | 0 |
| 3 | 1 | 0 | 0 | 0 |
| 3 | 1 | 1 | +1 | **+1** |
| 3 | 1 | −1 | −1 | **−1** |
| 3 | −1 | −1 | +1 | **+1** |
| 3 | 1 | 2 | +2 | **+1** |

For L=3, Q12=Q34=1, the full overlap matrix satisfies the Ginsparg-Wilson relation with Frobenius residual **8.46e−13**. Its Hermitian Wilson kernel has a nonzero gap, and the overlap matrix has the required topological zero mode.

**The especially useful negative result:** the L=2 double-flux case, and even the L=3 (1,2) case, **do not** obey the naive assertion that a discretized overlap index must always match the continuum Q12 Q34 product. Their flux is quantized, but the regulator is too coarse or the background too strong for the specific mass/kernel realization to reproduce the targeted continuum index. This demonstrates a finite-lattice resolution and smoothness/admissibility gate; it **does not** contradict the overlap index theorem when its assumptions and continuum limits hold. The L=3 (1,1) match is numerical evidence in this selected smooth-background test, not a proof of regulator universality.

This is directly relevant to the TOE construction: **a correct finite causal spin-gauge algebra must be benchmarked in 4D flux sectors, not merely in a zero-field Clifford model or a 2D toy.** The background here is again supplied rather than derived; the object is an *abelian U1 torus bundle*, not a dynamical nonabelian SU2 instanton or a physical chiral SM generation.

Reproduce:

    python analysis/toe_20261119_fourD_overlap_flux_threshold.py
    python -m pytest -q tests/test_toe_20261119_fourD_overlap_flux_threshold.py

File: analysis/toe_20261119_fourD_overlap_flux_threshold.py
Numerical certificate: data/toe_20261119_fourD_overlap_regulator_flux_threshold.json
Independent focused tests: 12.

Prior art on the 4D overlap topological index and the importance of lattice smoothness: https://arxiv.org/abs/hep-lat/0111060 ; https://doi.org/10.1140/epjc/s10052-020-7984-9 ; https://doi.org/10.1007/s11005-026-02080-w .

## Interpretation — What is genuinely shared, and what remains independent?

The most useful hierarchy is:

    incidence/causal order
      -> topology candidates (order complex), but not a specified spin lift
      -> choose spin lift/Spin^c quotient and U1/SU2 transport
      -> a gauge-covariant Wilson kernel, then a modified-chiral overlap operator
      -> flux sectors and index/chirality consistency conditions
      -> an action with actual variational gauge force
      -> select a physical quantum state and time generator
      -> derive rather than assume the spacetime dimension and Einstein dynamics.

This supplies multiple mathematical **consistency bridges**, but does not reduce them to one principle. The global Spin^c parity is a substantive constraint only after the group quotient is postulated. The overlap index is exact but is built on a smooth torus. The Gaussian vacuum nonuniqueness establishes why extra dynamics is needed. And 2D Regge curvature is not 4D gravity.

**No derived fundamental constants, full Standard Model chiral gauge family, Lorentzian 4D spacetime, gravity/black-hole microstates, Born rule, physical S matrix or experimental prediction.** These are independent obstructions to be solved rather than gaps silently bridged by evocative terminology.

## Reproducibility and source files

    python analysis/toe_20261119_spinc_overlap_6_homerun_gates.py
    python -m pytest -q tests/test_toe_20261119_spinc_overlap_6_homerun_gates.py

Code: analysis/toe_20261119_spinc_overlap_6_homerun_gates.py
Tests: tests/test_toe_20261119_spinc_overlap_6_homerun_gates.py
Machine-readable output: data/toe_20261119_causal_spinc_overlap_anomaly_quantum_gravity.json
Research report: analysis/2026-11-19_spinc_overlap_quantum_gravity_six_fronts.md

There are **41 new focused tests** (29 across the six original gates plus 12 for the 4D regulator extension), and a final combined regression suite of **217 passing tests**, including the independently landed parallel spin^c/E8/photonic physics tests. The new tests check six fronts, chain-complex GF2 Betti invariants, exact U1 plaquette flux and GW relation, local gauge covariance, topological zero modes, charge-parity quotient descent, 2D anomalies, purity/commutator nonuniqueness, a dynamically varying Regge deficit with fixed Euler curvature, finite causal growth controls and an actual SU2 force/energy decrease.

## Top five independent next experiments (larger upsides, sharper falsifiers)

1. **Spin/charge from unembedded causal incidence:** define Clifford generators, global Spin^c obstruction classes and a Lorentzian chiral overlap analogue intrinsically on an unlabeled causal poset; demand the index, GW relation and spectral locality without a supplied torus.
2. **A unique microscopic action/operator:** search for a local causal transport principle which *forces* the chiral/GW Dirac structure, Pauli spin-gauge curvature term, gravitational Lichnerowicz R/4 term and gauge-field action coefficients without separate inserted regulators or groups.
3. **Physical vacuum/Born selection:** formulate a covariant energetic/modular/entropic state selection principle that singles out an admissible Hadamard and positive interacting quantum state from the continuum of pure squeezed alternatives, with a microscopic time generator.
4. **True 3+1 Einstein dynamics and dimension selection:** use unlabeled causal-history measures rather than forward-edge DAG presentations; test for a robust 4D manifoldlike attractor, tensor graviton dispersion and Einstein constraints, against finite-order entropy-dominance null models.
5. **Global charge/representation predictions:** derive the global quotient of the actual 4D gauge group, its allowed spin-charge lattice, anomaly-free chiral representation content, and index/instanton sectors. Compare the derived spectrum to SM families, not toy 2D anomaly sums.

**Extra outside-the-box idea:** treat the quantum two-point state's complex structure and the spatial spin-gauge bundle's complex structure as components of a *single dynamical compatibility functional*. This is not a claim that they are the same object; a hypothetical principle would have to make both gauge holonomies and vacuum covariances stationary, while retaining Lorentz invariance and avoiding triviality. A specific computable test is whether the free massive causal commutator, overlap spectral projectors and a dynamical gauge action admit simultaneous reflection-positive, gauge-invariant stationary solutions across nontrivial flux sectors.
