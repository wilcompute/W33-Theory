# Six independent 2026-11-20 W33/TOE falsification and construction gates

**Research status:** exact representation and graph calculations, model-conditional numerical tests and a rigorous conservative measurement confidence bound. NOT an E8 ultraviolet completion, a physical singular-G2 compactification, a measured Holonet, an Einstein limit, or evidence for a new law of nature. Live GitHub intake `9c9d65d0941d373360ed197a1629fd77131d26e5`; previous assistant's baseline `9658f9ebe1040302f7acb4cf8957aecd08944cdb`. The new parallel commit `9c9d65d` provides its own genuinely MULTI-QUTRIT `[[638,81,dX=3,dZ=8]]_3` mixed Levi/repetition hypergraph-product CSS code, backed by a rank/distance proof. It is not reproduced or claimed as this packet's invention. Sources: repo `analysis/2026-11-20_mixed_levi_repetition_hgp.md`, `analysis/toe_20261120_mixed_levi_repetition_hgp.py`.

The attached Python producer builds all six finite controls deterministically. Focused unit tests, a generated JSON certificate and independent Windows replay constitute the evidence. Results are described with explicit physical boundaries.

## 1. E8 adjoint: three distinct commuting (27,3) field copies are necessary for a nonzero d×epsilon cubic of this type

The standard E8 adjoint under E6×SU3 decomposes as (78,1)+(1,8)+(27,3)+(27bar,3bar). The 27 of E6 possesses a *symmetric* cubic tensor `d_abc`; SU3 has an alternating tensor `epsilon_ijk`. The candidate trilinear on three independent commuting chiral multiplets is

    T(A,B,C)=d_abc epsilon_ijk A^a_i B^b_j C^c_k.

Because `d` is symmetric and `epsilon` antisymmetric, T(A,B,C) is alternating under exchange of *whole field copies*. Therefore T(A,A,A)=T(A,A,B)=0 identically, even when the internal triplet has several nonzero components. In particular, a single `Phi in (27,3)` does NOT produce this cubic by self-contraction. In a nonzero explicit witness, restrict the E6 27 cubic to the three diagonal entries of the Albert algebra, `N(x)=x1 x2 x3`. The fully polarized d has value `1/6` on three distinct basis vectors. With three independent (27,3) components `A_(1,1)=B_(2,2)=C_(3,3)=1`, the contraction gives **1/6**, changing sign under exchange of A and B. Random identical-copy contractions vanish numerically below 1e-12.

This does NOT prove three full E8 adjoints are sufficient to engineer the 19 H27-covariant baryon sources: these still require a precise E6/E8 representation, allowed superpotential, vacuum equations and anomaly accounting. The one-adjoint cubic obstruction appeared in earlier repo work; our increment is the explicit trilinear copy-alternation and 3-copy constructive witness.

## 2. W33: 80-dimensional known-edge noiseless subcode and an all-modes exact single-particle no-go

The W(3,3) point-line Levi graph has 80 vertices, 160 edges and `dim cycle = 160-80+1 = 81`. Its edge connectivity is **4**, independently computed here. A single particle occupying its 160 flag modes has Hilbert space `C^160`; cycle amplitudes form an 81-dimensional subspace. A known faulty edge e may suffer an arbitrary phase `U_e(theta)=I+(exp(i theta)-1)|e><e|`. Restrict to the graph cycle space after deleting e. It has exactly `dim=80`, and **every vector has zero amplitude on e**, so U_e acts as identity regardless of theta. A deterministic spanning-tree fundamental-cycle basis produces 80 integer incidence-null vectors, all zero on the deleted coordinate. For two known bad edges the dimension is 79; for all four edges incident to one vertex, the graph disconnects an isolated vertex, yielding `81-4+1=78` dimensions.

General dimension formula for a known set S of arbitrarily faulty flags:

    dim C_noiseless(S) = |E\S| - |V| + components(Levi\S).

This is the dimension of the ordinary graph cycle space after deleting S, not proof of a physically realizable unitary recovery circuit.

**General one-particle no-go, stronger than the last round:** Any code projector P of rank >=2 on `C^n` that corrects `{I,U_e(theta) : e=1,...,n}` for fixed nontrivial theta must satisfy `P |e><e| P = c_e P` for every e by Knill-Laflamme. Its left-hand side has rank at most 1, so each c_e=0. Summing over e yields P=0, contradiction. This excludes arbitrary unknown *one-mode* phase faults across all modes of a single particle; it does NOT exclude known-edge restricted errors, several particles, multiple time bins with a genuine tensor-product resource, syndromes, error flags, noisy-subsystem protection or nonunitary active recovery.

The new parallel `[[638,81,3,8]]_3` code is consistent with this impossibility because it uses **638 distinct qutrit physical subsystems**, not one photon occupying 638 optical modes. The Hilbert spaces scale as `3^638` versus at most `3*638` single-photon modes; they are physically inequivalent encodings.

## 3. Qutrit memory: noise-model-independent output-frequency witness with finite-shot confidence

Source theorem: Beyer et al., *Observation of Genuine Multi-Time Quantum Memory* (2026), arXiv:2611.17268, Supplement VI Eq. S38, https://arxiv.org/html/2611.17268. For two MUB bases B,C, the three-time classical-memory witness is

    W3 = sum_(i<j) F(E2(|bi><bi|),E2(|bj><bj|))
       + sum_(i<j) F(E3(|ci><ci|),E3(|cj><cj|))
       - S1,      S1 = .5 ||E1(I)-I||_1,

where `F` denotes *root* Uhlmann fidelity. `W3<0` rules out a *single common classical-memory* explanation of all three maps.

A projective measurement of both output states in the same chosen basis gives classical outcome probabilities `p=(p0,p1,p2)` and `q`. Quantum fidelity **cannot exceed** the classical Bhattacharyya coefficient of these outcomes, `F_quantum <= sum_j sqrt(p_j q_j)`, by data processing. Measure `E1(I/3)` with probabilities r in the computational basis; trace-distance contractivity gives `S1 >= .5 sum_j |3r_j-1|`. Therefore the *measured output frequencies themselves* supply a conservative witness upper bound. Unlike the earlier 61,300-shot estimate, this inequality does not presume an isotropic depolarization map or diagonal output density matrices. It does assume known input and measurement bases, stationarity of each channel and fair accepted-trial sampling. It is **noise-model-independent**, not device-independent.

Seven settings suffice: one maximally mixed first-channel input and the six late-channel MUB input-basis preparations. Each produces three categorical outcomes. With `N` IID accepted trials per setting, a 21-coordinate union of two-sided Hoeffding inequalities gives simultaneous radius

    t = sqrt( log(42/delta) / (2 N) ).

For each late pair, upper bound F by `sum_j sqrt(min(1,p_hat_j+t)*min(1,q_hat_j+t))`; lower bound the nonunitality by `.5 sum_j max(0,|3r_hat_j-1|-3t)`. Their difference bounds W3 above with probability at least `1-delta` regardless of output noise structure. The prospective benchmark chooses **gamma=.75, epsilon=.01** from the previous *reference model*, for which true `W3=-0.7894929399`. A rigorous *model-conditional planning* worst-case bound shows **173,884 accepted trials per setting** (1,217,188 total across seven settings) suffice for a strictly negative upper bound with 99% probability. A seeded simulation at 200,000 trials per setting returns upper `W3=-0.3657568`. The benchmark uses depolarization to forecast sample size; the estimator does not assume depolarization when applied to data.

The ideal pairwise classical decompositions already reside in previous repo code. On a real experimental device, pairwise *process* classicality would need separately certified—not automatically transferred from an ideal channel model. Loss/heralding, input calibration and drifts remain required checks. This calculation does not claim an observation.

## 4. SU3 Wilson readout: 36-setting Richardson twirl cancels detector drift through cubic order

The previous nine-Weyl twirl removes fixed detector bias; the earlier 18-exposure symmetric schedule removes linear drift, provided detector trace is time-independent. Here test `eta(t)=eta0+t eta1+t^2 eta2+t^3 eta3` with `Tr eta_i=0` for i>0. The measured biased loop character at Weyl setting W is `m_W(t)=3 Tr(eta(t) W K W†)/Tr eta(t)`.

For each W, collect four time-mirrored exposures at `+h,-h,+2h,-2h`. The Richardson estimator

    R_W=(4/3)[m_W(+h)+m_W(-h)]/2 -(1/3)[m_W(+2h)+m_W(-2h)]/2

cancels **all terms of degree 1,2,3 in t** when the trace is constant. Then average the R_W across all nine Weyl settings to cancel the remaining eta0 bias and recover `Tr K`. The test uses random noncommuting SU3 loops and positive Hermitian detector matrices: one 9-setting chronological schedule gives complex error **0.01321**, the 18-setting mirrored schedule **0.00649**, and the 36-setting polynomial-cancelled schedule error **1.11e-16**. Adding a quartic drift term gives residual **0.00339**, a deliberate falsifier.

The estimator's signed weights are not free: for identical per-exposure shot variances, the Richardson estimate has **34/9 times** the variance of a plain equal-weight four-exposure average, at equal shot allocation. No physical detector, finite-shot optical interferometer, stable reference loop, superselection analysis or setting-dependence calibration is claimed.

## 5. Exceptional charged chirality: trinification anomaly / center consistency, not a 7D index

Under `SU3_1 x SU3_2 x SU3_3`, the E6 27 decomposes as `(3,3bar,1)+(1,3,3bar)+(3bar,1,3)` (three 9-dimensional nonets). Its cubic gauge anomaly for each SU3 factor vanishes: three fundamentals from one nonet and three antifundamentals from another cancel. Hence three complete chiral 27's also have vanishing SU3^3 cubic anomalies as a representation-level statement. The central triple `(omega^2,omega,1)` acts as **omega on all three nonets**. This is precisely the central charge relevant to the repo's internal trinification H27 construction; the parallel repo already developed the conceptual representation linkage. This pass supplies its own explicit integer charge/anomaly check.

**Necessary is not sufficient:** local cubic anomaly cancellation and consistent center are not a singular G2 compactification or a physical origin of three charged chiral 27s. No 7D charged Dirac operator, defect index, inflow, flux quantization or 4D Yukawa texture is constructed. Smooth G2/round S7 chirality obstacles from earlier passes remain.

## 6. Causal continuum: nonlocal growth of the transitive-reduction link graph

Using uniform-volume sprinklings in a fixed `3+1` Minkowski Alexandrov diamond, construct causal relations R and the Hasse link matrix `L=R & not(R@R)` (a link has no intermediate event). For 40 independent seeded samples at each density, the mean number of directed links **per event** grows:

| Events n | 40 | 80 | 160 | 320 |
|---:|---:|---:|---:|---:|
| Mean links/event | 1.572 | 2.861 | 4.865 | 8.304 |

The relation fraction remains near the 4D Myrheim–Meyer expectation 0.1 across all n. This supplies a targeted falsifier for a naive W33-style **fixed finite nearest-neighbor degree** used as a universal causal dynamical law: refining a manifoldlike Lorentzian sprinkling does not keep the Hasse degree constant in these finite samples. It is not an asymptotic proof; the nonlocality of causal-set links is already established mathematical physics (Surya, *The causal set approach to quantum gravity*, Living Rev. Relativ. 2019, https://doi.org/10.1007/s41114-019-0023-1).

## Reproduction

    python analysis/toe_20261120_six_open_physics_gates.py
    python -m unittest discover -s tests -p test_toe_20261120_six_open_physics_gates.py -q

Producer, 27 focused tests, report, and frozen JSON data are all in this packet. Depend on NumPy, SciPy, NetworkX. Rebuild the JSON and report the tested commit and machine separately; no quantum-gravity or TOE status is promoted solely from algebraic count matching.

## Top five independent research gates after this pass

1. Actual E8 UV multiplet/messenger superpotential reproducing H27-covariant 19 baryon constraints with global vacuum choice and anomalies, beyond the alternating three-copy cubic.
2. Optimize and experimentally calibrate the seven-setting noise-model-independent qutrit witness; separately SDP-certify two-time classicality and handle heralding/loss.
3. Implement and compare single-photon known-edge W33 passive subcodes versus independent multi-qutrit `[[638,81,3,8]]` CSS recovery; build full finite-error physical Kraus channel and recovery circuits.
4. Optimize the 36-exposure SU3 Richardson schedule under shot noise, unequal temporal illumination and higher-order drift; test conjugation invariance of a real photonic loop.
5. Derive an actual charged singular G2/ADE Dirac index and spinorial causal action/continuum nonlocality guard; separately require anomaly inflow and cosmological dynamics.
