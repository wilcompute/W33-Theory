# Five independent W33 fronts: an S5 block, loss-aware Q8 metrology, gauge action, chirality, and corrected cosmic shear

**November 9, 2026.** Independent work building on the repository's Passes 12632–12640. **Evidence levels:** exact finite-group/arithmetic statements; independently computed numerical checks; toy finite-graph candidate actions; and reanalysis of previously committed cosmological controls. None is a derived physical theory of everything, a continuum limit, an observed detection, or a new survey likelihood. Reproduce with `py -3 analysis/w33_20261109_five_fronts.py data/w33_20261109_five_fronts.json` and `py -3 -m unittest discover -s tests -p test_w33_20261109_five_fronts.py` (on other OS, use `python`). The producer does not import prior W33 math code.

## I. Pentad: the high-SOS eigenspace is nine S5 singlets

Pass 12639 identifies the five sentinel factor-swaps on the 45-dimensional two-copy symmetric space with the five star transpositions `(k 6)` in `S6`, and Pass 12640 independently identifies nine copies of the standard `(5,1)` representation. These *prior* proofs are explicitly the input, not results newly proved by this file. Here, compute the five real 5x5 star matrices from the permutation representation on six letters restricted to its zero-sum hyperplane. `R=sum_{k=1}^5 (k 6)` has spectrum `[-1,4,4,4,4]` per block. On the existing nine-copy model, the 16/9 SOS eigenspace is the `-1` eigenspace of R: **nine copies of the trivial S5 representation**. The 1/9 eigenspace is nine copies of the standard 4D S5 representation.

Explicit projectors on `Sym^2(C^9)` are `P_high=(4 I-R)/5`, `P_low=(R+I)/5`. On each 5D block `P_high` has trace one and commutes with, indeed is fixed pointwise by, all 10 `(i j)` for `1<=i<j<=5`; checked at floating error < 1e-12. The 9D high block is a **symmetry singlet**, not evidence for nine fermion generations or a physical hidden sector. The more difficult Veronese/rank-one minimization of the pentad SOS is still open here: the Hermitian 1/9 bound need not be attained by `v tensor v`.

## II. 72-unitary design: an unbiased finite-shot estimator, and an undetectable calibration failure

From the previously established three quaternion cosets in `SL(2,3)`, re-construct all 24 mutually unbiased Choi bases using explicit qutrit Clifford generators. For any *globally pure* two-qutrit input and an eight-basis coset, `C8=sum_{b,j} p_bj^2` and linear entanglement `L=1-tr(rho_A^2)=(3/2)(C8-4/3)`. At fixed `N>=2` **accepted, IID projective measurements per basis**, with observed counts `n_bj`, the unbiased collision estimator is

`c_hat_b = sum_j n_bj(n_bj-1) / [N(N-1)]`, `C_hat=sum_b c_hat_b`, `L_hat=(3/2)(C_hat-4/3)`.

Its **exact** per-basis variance, with `c=sum p_j^2`, `r=sum p_j^3`, is

`Var(c_hat)=[2(c-c^2)+4(N-2)(r-c^2)]/[N(N-1)]`.

Independent enumeration of all 729 sequences at `N=3` matches this formula within 5e-16. A 2,500-draw multinomial simulation at N=30 gives empirical/theoretical variance ratio 0.9801. Independent-basis entanglement variance multiplies the sum of these variances by 9/4. Using **disjoint paired shots** for a distribution-free Hoeffding interval, `Pr(|L_hat-L|>=epsilon) <= 2 exp(-M epsilon^2/9)` with M pairs in *each* of eight bases. At 95% and epsilon=0.1: M=3320, requiring **53,120 ideal detected preparations per coset**; all three cosets triple this to 159,360. The U-statistic typically reuses shots more efficiently than disjoint pairs.

### Calibration falsifier

Simulate the same *outcome-dependent* detector efficiency profile `e_j=0.63+0.045*j`, `j=0..8`, in every basis. Conditional on a detection, the observed frequencies are `p'_bj=e_j p_bj/(sum_k e_k p_bk)`. For the **separable product state** |00>, all three Q8 cosets yield the *same* distorted collision sum **1.3490260631** instead of the ideal **4/3**. Naively interpreting it as pure-state entanglement produces a spurious **L=0.02353909465**, while the three-coset discrepancy is **exactly zero**. Hence **agreement across cosets is necessary under the ideal model but not sufficient to detect systematic readout bias**. If the nine efficiencies are independently calibrated and stable, dividing `p'_j` by `e_j` and renormalizing recovers the ideal collision to about 1e-15.

Under global depolarization `rho_eta=eta|psi><psi|+(1-eta)I/9`, `C8-8/9` scales by `eta^2`, verified at `eta=.82` with factor `0.6724`. The pure-state inference is invalid for an arbitrary mixed input without separate characterization or a justified depolarizing model. Optical interferometers, two-qutrit entangling gates, source purity, collection efficiency, leakage and feedforward remain physical hurdles. The 72-element qutrit design and general frame-potential condition are prior art (Gross–Audenaert–Eisert 2007, arXiv:quant-ph/0611002; early 72-member qutrit designs also precede this work).

## III. A native W33 gauge action, with an exact topological warning

Independently reconstruct all 40 projective points and 40 totally isotropic lines of `W(3,3)` from `F3^4` and its alternating form. Their 4-regular bipartite Levi graph has **80 vertices, 160 edges, girth 8**, and **1,620 undirected simple 8-cycles**. Eliminating the binary edge masks of these shortest cycles shows rank **81 = E-V+1**. Thus the shortest cycles span the entire graph cycle space; there are **1,539 linear dependencies**. These counts agree with *older* repo work (`data/w33_20261013_toe59_eight_cycle_census.json`, and Pass 5044's `[1620,81,81]_2` apartment code); they must NOT be described as newly discovered.

Define a complex field `psi_v` on the 80 nodes and U(1) edge phases `theta_e` oriented from point to line. A concrete finite-graph Euclidean potential/action is

`S=sum_e |psi_p-exp(i theta_e)psi_l|^2 + 0.13 sum_{C8}(1-cos(sum_oriented theta_e)) + 0.15 sum_v |psi_v|^2 + 0.02 sum_v |psi_v|^4`.

Under `psi_v -> exp(i chi_v)psi_v`, `theta_(p,l)->theta_(p,l)+chi_p-chi_l`, **S is invariant** numerically at floating precision; the covariant graph Laplacian obeys `L(theta')=G L(theta) G†`, checked to 4e-15 on a seeded complex field. The mass and quartic couplings were arbitrary **illustrative choices**, not fixed by finite geometry. A genuinely physical model needs a temporal/causal evolution rule, gauge dynamics, a continuum family with scaling, fermions with correct chirality, and empirically matched dimensionful couplings.

If *all* 1620 octagons are glued in as independent formal 2-cells, the resulting cellular boundary map has rank 81 and `beta_2=1620-81=1539` over Q (as well as mod 2). This overcomplete 2-cell description needs a specification of higher cells/relations or an explanation of its enormous H2. It is valid to sum a 1,620-term symmetric curvature *energy*, but invalid to treat its plaquette fluxes as 1,620 independent degrees of freedom. The graph alone contains exactly 81 independent U(1) holonomies before flux constraints.

## IV. Chirality: explicit anomaly checks do not choose a handed vacuum

Independently sum one left-handed SM family `(Q,u^c,d^c,L,e^c,nu^c)` with the usual hypercharges. `SU(3)^3=0`, `SU(3)^2 U(1)=0`, `SU(2)^2 U(1)=0`, `U(1)^3=0`, mixed gravitational-U(1)=0, and there are **four** left-handed SU(2) doublets counting the three Q colors, so Witten's mod-two obstruction vanishes. The same identities hold for **every** positive number of copies, checked for one through ten. Thus anomaly cancellation **by itself** does not force three families. The older Pass 12091 statement about only ±3-family spectra is conditional on its selected E8 order-three shift, its gradings and untwisted-sector counting; this does not contradict the general arithmetic.

An even parity-symmetric double-well `V(sigma)=(sigma^2-1)^2` has equal stable minima `sigma=+1` and `-1`; a specified boundary condition, thermodynamic selection or explicit parity-breaking source is required to choose a sign. A finite example is not spontaneous symmetry breaking in the infinite-volume sense. Neither this toy potential nor a graph-orientation label establishes the observed 3+1D Weyl spectrum or fermion masses. External relevant developments: Thorngren–Preskill–Fidkowski, *JHEP* 07 (2026) 271, arXiv:2601.04304; Witten's Nov 2026 note, arXiv:2611.05051. Neither licenses bypassing anomaly/measure/mirror-sector tests.

## V. Cosmology: independent arithmetic audit, not an independent new likelihood

Read only the repo's **frozen corrected** `analysis/toe_uv/prereg_noshear.json` (`S9_shear_no_split`, 2026-11-08). The DES Y3 fixed-background control gives `Delta chi2(CPL - fading c<0)=-0.64362345`; KiDS-Legacy gives **-0.28040067**. Maximum |Delta chi2| from Lambda-CDM among the listed evolving models is **1.93525839** (DES) and **2.49287522** (KiDS). Both fit the numerical *current-control* envelope of |gap|<2 and |model-Lambda-CDM|<4, but they are neither a test of future held-out data nor significant discrimination between the two models.

The frozen S9 claim concerns **future** DES Y6, KiDS successor, HSC Y3 or Euclid DR1 data with specified survey cuts and nuisance fitting. This pass does not run CLASS, patched Halofit, HMcode, DES or KiDS covariance likelihoods anew, and cannot declare S9 confirmed/falsified. Crucially, the pre-Pass12632 scalar-field shear ranking **was withdrawn** after the Halofit Omega_m/Omega_v bookkeeping error; it must stay excluded from model selection. `analysis/PASS12632_HALOFIT_SCF_BUG.md` and `analysis/NOTE_DARK_ENERGY_EVIDENCE_20261108.md` document the retraction and patched results.

## Physical interpretation and falsification priorities

The first two fronts give exact quantum-information structure and practical metrology caveats. The third gives a gauge-invariant discrete *candidate*, not a dynamical theory. The fourth finds a genuine logical limit on inference from anomalies and chirality labels. The fifth prevents a withdrawn numerical result from reentering the evidence base. In particular, integer coincidences across W33, E6, E8, octagons, code dimensions or cosmology do not establish identification with physical fields or constants. Promotion to TOE requires **a derivation and tests of a dynamical continuum quantum theory with the observed chiral spectrum, couplings and falsifiable predictions**.

### Next five independent experiments

1. Compute the **rank-one/Veronese constrained pentad SOS minimum** and certify a strict gap above 1/9 if one exists, without mistaking the 45D operator minimum for the rank-one minimum.
2. Design an **interleaved independent readout calibration** (nine efficiencies per setting, drift model, dark counts, source-purity bound) and a loss-robust entanglement confidence interval.
3. Build a **refinement/renormalization family** of W33 incidence complexes and show, rather than assume, Lorentz-invariant, local, causal continuum propagation and gauge Ward identities.
4. Construct an **explicit Weyl regulator** and check propagator poles, mirror gaps, anomaly phase/inflow and orientation selection on a growing lattice family.
5. Run a **blinded patched CLASS/HMcode plus survey covariance** study on one new untrained shear release, with the S9 criterion fixed in advance and nuisance/prior sensitivity reported.
