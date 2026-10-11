# TOE47 — Exact even-Weil cusp POVM, W33 Fisher and SPAM, Wilson-sector MUBs, magnetized flavor

**10 October 2026.** Baseline TOE46 commit 0abdc6f23f040de7e8a1366998b5a575815f69ae. Five requested fronts were experimentally/mathematically pursued, plus a 41-outcome native two-qutrit extension and one-setting d=5 purity estimator. This is a finite-dimensional mathematics and simulated quantum-device research packet, NOT a completed Standard Model or theory of everything.

## Sources reread and what is prior art

Reviewed TOE41–TOE46 Pauli-power identities, W33 incident lines, 90 virtual factor purities, ten-MUB protocols, rank-25 cusp collisions and full-rank 15D dark fibers; Pass11897–11899 Kähler even Weil-five generators and **40 cusp rays associated with W33 LINES**; Pass11900 canonical Wilson Z2 point; Pass11903 frozen 491-model local-ten census; Pass11904 Wilson theta mass unlock; Pass11905 reflection-fixed Wilson degeneracy; Pass11080 point/line ternary 13-design non-equivalence; Pass11721–11725 existing Weil coherent rays and parity projections; Holotrade's three 81D K81 carriers. At entry, W33 master matched TOE46 and Holotrade had no newer commit.

External scientific input: Cremades–Ibáñez–Marchesano, JHEP 05 (2004) 079, https://arxiv.org/abs/hep-th/0404229, established torus flux wavefunctions and theta Yukawas. Finite symplectic quadrangles, MUBs, projective 2-designs and U-statistic shadow protocols are established mathematics. The 40 Kähler cusp projective rays and Weil generators PREEXIST this work in Pass11899. Novelty claims are confined to the explicit checked synthesis and the specific measurement formulas and models below.

## Front 5 first: the **40 Kähler cusp rays** give an IC d=5 measurement

Producer: analysis/w33_20261010_toe47_cusp_even5_ic_povm.py
Certificate: data/w33_20261010_toe47_even5_cusp_ic_povm.json

Let Q:C5->C9 be the exact orthonormal even-Weil embedding derived from the existing K.even_basis() and native 2-qutrit Clifford generators. Starting with |00>, applying the seven existing generators produces precisely 40 distinct projective even-Weil rays v_L. Simultaneously transport the isotropic commuting line <Z1,Z2> by the actual symplectic generator actions. Every ray has a unique label among all 40 W33 LINES and the assignment is equivariant.

Let P_L=|v_L><v_L| in Herm(C5), and let A_line be intersection adjacency of the 40 lines. Their exact squared-overlap Gram is:

    G= (8/9) I + (2/9) A_line + (1/9) J.

Diagonal G=1; 480 ordered adjacent off-diagonal overlaps squared 1/3; 1080 ordered nonadjacent squared 1/9. The Gram spectrum is 8^1, (4/3)^24, 0^15, so its rank is 25, the entire real dimension of Herm(C5). Also:

    sum_L P_L = 8 I5,
    sum_L P_L tensor P_L = (4/3)(I25+SWAP).

Thus this 40-ray orbit is an exact **complex projective 2-design** in C5. Its 40 positive effects E_L=P_L/8 constitute an informationally complete **single POVM** in dimension five. For ANY state rho5, with p_L=Tr(rho5 P_L)/8,

    rho5 = 6 sum_L p_L P_L - I5.

Tests: projective second-moment residual 3.6e-15; 30 random full-rank reconstructions max 1.7e-15; seven generator equivariance residual <2e-15. This explicitly realizes the 25D visible **LINE-side** quotient as End(even5), correcting the rejected TOE46 shortcut Sym²(even5)=dark15. It does NOT assert an isomorphism of the point and line characteristic-three designs, which Pass11080 disproves.

### Extra: native 9D **41-outcome parity POVM**, and its information boundary

In the original two-qutrit Hilbert C9 define 40 effects E_L^9=Q P_L Qdag/8 plus E_odd=I9-Q Qdag. They are positive and sum to I9. The 40 even outcomes reconstruct only B=Qdag rho9 Q:

    p_even=sum_L Pr9(L),
    B=6 sum_L Pr9(L) P_L - p_even I5.

All 41 effects span 26 Hermitian dimensions, leaving **55 traceless C9 state directions invisible**; no full 9D tomography claim. Fifteen random 9D mixed-state inversions pass to machine precision. This is a mathematically defined POVM; implementing its 40 detectors/ancilla Naimark realization is open.

## Front 4: 40 collision summaries have Fisher rank25, but ten full MUBs rank80

Producer: analysis/w33_20261010_toe47_dark_fisher_rank.py
Certificate: data/w33_20261010_toe47_dark_fisher_information.json

The generic trace-one two-qutrit state space has 80 real Weyl coordinates mu_p=x_p+i y_p, one complex value per projective Pauli. Their squared powers are q_p=2|mu_p|² and 40 cusp-context collision probabilities obey C=(1+Nq)/9.

    dC=(4/9) N [diag(x)dx + diag(y)dy].

At every strictly full-rank state with all mu_p nonzero, rank(dC)=rank(N)=25. For ideal independent two-copy collision observations Fisher rank=25, nullity55: exactly **40 phase directions +15 W33 dark Pauli-power directions**. In contrast, ten COMPLETE commuting MUB bases have 90 outcome probabilities, 80 independent parameter directions, and their multinomial classical Fisher rank is 80. An explicit fixed-purity dark tangent has collision Fisher quadratic ~1.57e-17, while full MUB Fisher quadratic ~25.694. This is a local identifiability theorem, NOT globally optimal quantum Fisher measurement design or a complete experimental prescription.

## Front 1: calibrated four-batch quartic estimator's **exact conditional variance**

Producer: analysis/w33_20261010_toe47_spam_gap_variance.py
Certificate: data/w33_20261010_toe47_spam_gap_exact_variance.json

TOE46 used ten different MUB settings, four independent blocks A,B,C,D, q_AB,p=2 Re(mu_A,p conj(mu_B,p)) and q_CD similarly, to estimate G=(2/135)||Pminus q||² via Ghat=(2/135)(Pminus q_AB).(Pminus q_CD).

This pass injects **basis-dependent symmetric nine-outcome readout errors epsilon 4–16% and independent per-copy missing-at-random loss 4–28%**. Each surviving Pauli eigenvalue observation is corrected by 1/(1-epsilon) in its setting. The estimator is **conditionally unbiased** given all positive survivor counts and exact trusted detector epsilon.

Within a basis, the four measured Pauli observables have **correlated** multinomial samples. Let C_AB and C_CD be the exact real 40x40 covariance matrices for q_AB and q_CD (calculated from complex covariance and pseudocovariance of corrected eigenvalue averages), with t=Pminus q. The exact conditional variance is

    Var(Ghat|counts)=(2/135)^2 [
       Tr(Pminus C_AB Pminus C_CD) + t^T(C_AB+C_CD)t
    ].

For 240 seeded simulations each with 40,000 attempted state copies (1000 per each basis each block): actual true G=7.694493405e-5; calibrated average 7.643781388e-5; actual run-to-run variance 2.512636376e-10; oracle exact expected conditional variance 2.648864503e-10 (ratio0.949). Omitting readout correction gives mean 5.184980162e-5, visibly biased.

A very conservative bounded-difference radius is calculated conditional on the observed minimum valid survivor count; it is NOT an unconditional, practical, model-robust confidence interval. Unknown confusion, outcome-dependent loss and state drift remain open.

## Front 3: **four conditional qutrit MUBs** in each Wilson charge class

Producer: analysis/w33_20261010_toe47_wilson_charge_conditional_mubs.py
Certificate: data/w33_20261010_toe47_wilson_conditional_mubs.json

Pass11900's canonical ideal Wilson holonomy is two-qutrit Pauli Z2, a W33 projective point p. It has three eigenvalues and three rank-three charge eigenspaces Q_a. Exactly four maximal commuting W33 lines contain p. Restrict each line's nine joint eigenprojectors to one Q_a: each gives a 3-vector orthonormal basis. The **four restricted bases are the complete set of four mutually unbiased bases of each qutrit charge sector**, with squared cross-basis overlaps precisely 1/3.

For every two-qutrit rho and charge blocks rho_a=Q_a rho Q_a, the observed four-context collision sum obeys

    sum_{four lines L through p} sum_{nine outcomes j} Pr_L(j)^2
       = sum_{a=0..2} [Tr(rho_a²)+(Tr rho_a)^2].

For a NORMALIZED state restricted to one charge sector, it equals 1+Tr(rho²), giving an exact four-setting charge-resolved qutrit purity assay. 44 random full-rank state checks show max error ~1.1e-16.

Crucial firewall: the 491-model frozen census does not contain any model-by-model physical Wilson-holonomy matrices identifying each gauge Wilson line with this Pauli p, nor the corresponding physical Yukawa worldsheet operators. No predicted flavor selection is inferred from the pure 4:36 combinatorial count.

## Front 2: **relative Wilson displacement unlocks a single Higgs mass doublet**, not CKM

Producer: analysis/w33_20261010_toe47_relative_wilson_flux336.py
Certificate: data/w33_20261010_toe47_relative_wilson_flux336.json

TOE46: with equal left/right M=3 torus magnetic backgrounds and a fixed M=6 Higgs mode, the Yukawa overlap matrix has selection support i+j=k mod3 and symmetric offdiagonals Yij=Yji. Hence two equal singular masses.

TOE47 imposes opposite continuous gaussian-center shifts s_L=s, s_R=-s, s_H=0 with flux-weighted relation 3 s_L+3 s_R-6 s_H=0. Recomputed normalized M=3 family and M=6 Higgs wavefunctions on a 128x128 grid. Forbidden Yukawa overlaps stay below 1e-10. A SINGLE fixed Higgs now generally has unequal formerly symmetric offdiagonals Y[0,1,2] and Y[0,2,1] (absolute magnitude split):

    s       split
    0       0
    0.002   0.0050502820
    0.004   0.0101039529
    0.008   0.0202350039
    0.016   0.0406863781
    0.040   0.1054558321

Linear small-s slope ~2.525–2.529. A relative Wilson-center displacement releases the *special* equal-background single-Higgs twofold mass degeneracy. BUT the fixed-Higgs 3x3 matrix is still monomial, YYdag diagonal; so **no CKM mixing** appears without further Higgs sectors and actual dynamical alignment.

The continuous shifts form an **illustrative flat-torus overlap ansatz**, NOT a checked globally quantized D-brane background, anomaly-free chiral spectrum or physical SM fit. Pass11905's theta degeneracy at *symmetric* Wilson-line points applies to a different localised-Higgs ansatz and does not contradict this test.

## Extra 6: the one-setting even5 cusp measurement has a two-copy purity identity

Producer: analysis/w33_20261010_toe47_cusp_povm_purity.py
Certificate: data/w33_20261010_toe47_even5_single_povm_purity.json

The 5D projective 2-design guarantees

    C=sum_{r=1..40} Pr(outcome=r)^2=(1+Tr rho5²)/48.

Therefore with m independent pairs of single-POVM measurements, the collision-count estimator P_hat=48*(number of matching outcomes)/m-1 is unbiased for Tr rho5². For uniformly confused 40-outcome readout eps, C_obs=(1-eps)² C+[1-(1-eps)²]/40, invert explicitly.

At eps=.06, 6500 measured pairs per run (13,000 copies), 1200 Monte Carlo runs:
- pure true purity1; mean calibrated 0.998224, predicted single-run SE 0.13160;
- maximally mixed true purity 0.2; mean 0.195188, predicted SE 0.10520.

Useful fixed-setting protocol, but significant shot variance; no efficiency superiority or physical optical measurement implementation proven. In the original 9D device it applies only to a properly conditioned/normalized even block, not full 9D rho purity.

## Reproduce and integrity

    py -3 -m pytest -q tests/test_w33_20261010_toe47_five_plus_physics_fronts.py tests/test_w33_20261010_toe45_cusp_collisions.py

Seven TOE47 focused regression tests replay all six producers; five TOE45 checks guard previous cusp identities. Only new TOE47 named scripts, certificates, tests and this report are to be staged and pushed. Other researchers' preexisting dirty files are preserved.

The results are exact *finite matrix identities* supported by derivations and machine-precision checks, with Monte Carlo for sampling statistics. They do NOT derive a physical Kähler quantum register, anomaly cancellation, Einstein dynamics, measured gauge masses, photon loss budget, UV completion or a Theory of Everything.

## Five absolute best independent next steps

1. **Device-realistic statistics:** build plug-in confidence bounds with general 9x9 confusion calibration, missing-not-at-random photon loss, adaptive shot assignment, drift and power/loss/clock budget for the four-batch W33 quartic estimator.
2. **Full magnetized particle model:** choose a globally consistent flux/Wilson/Higgs construction, satisfy tadpole/anomaly constraints and D/F flatness, derive vacuum Higgs coefficients, kinetic metrics, actual CKM/Jarlskog and RG-evolved quark ratios; no two-parameter free fits.
3. **Compile the 41-outcome cusp POVM:** explicit Naimark ancillas, Clifford and magic gates for odd/even parity and the 40-ray measurement, with exact resource tally and leakage/error thresholds.
4. **Actually map 491 model Wilson operators:** obtain original orbifolder Wilson matrices and selection rules, check their physical relation to W33 Pauli holonomies, and test whether conditional charge-MUB contexts affect allowed Yukawa operators rather than just their W33 labels.
5. **Exact representation bridge:** compute an algebraic (cyclotomic integer/finite-field) intertwiner for 40-line permutation -> End(even5), compare nonisomorphic point/line 15D parabolics and Holotrade K81, and determine whether any dynamical coupling respects all representations.
