# Five-front TOE follow-up: chirality, detector-space qutrit QEC, volume geometry, SU(3) Ramsey, and multi-time memory

**2026-11-20 | tested baseline:** `wilcompute/W33-Theory` `f9685d73c897f1fde12b15667aff5defb388ea37`. All computations in this packet are **exact algebra, classical simulations, or conditional probability bounds**, not a complete physical theory, hardware experiment, real singular-G2 index, proof of fault-tolerant threshold, or established Standard Model. The user asked to execute all five fronts; the impossible physical completion and missing experimental input are stated rather than presumed.

**Prior art reviewed:** recent W33 mixed Levi/repetition code, adjustable-length HGP code, and H27/SU(3) center quotient; latest `analysis/toe_20261120_levi_css_h27_color_center_certificate.py` single-qudit check; `analysis/toe_20261120_four_physics_controls.py` for E6 anomaly, causal conformal, reference Wilson, and worst-case accepted data. Our additions are a **time-resolved detector dictionary**, explicit chiral toy index, inverse *calibrated density* experiment, drift-insensitive quadrature bound, separate finite-shot efficiency calibration, and a classical marginal-gluing test. All underlying mathematics has known precedents; do not characterize them as new physical laws.

## Gate 1: chiral fermion index and why smooth closed geometry is insufficient

Study the first-order operator on the real line

\[
D=\frac{d}{dx}+\tanh x,\qquad D^\dagger=-\frac{d}{dx}+\tanh x.
\]

The normalized zero mode is `u=sech(x)/sqrt(2)`, which satisfies `Du=0` and has unit L² norm. The adjoint's formal null solution `cosh(x)` is **not** square-integrable, so the Fredholm index of this 1D toy is `1-0=+1`; reversing the wall reverses the index. A seeded 24,001-point centered finite difference of `Du` gives maximum interior residual `1.80e-7` (the null mode is also analytically exact). On a **periodic smooth circle**, solving the first-order ODE shows both `ker D` and `ker D†` are one-dimensional if the integrated mass is zero; otherwise both vanish. In either case the index is **zero**. Tested with `m(x)=sin x` and `m(x)=1`.

Important physical conclusion: a wall/boundary/singularity can support net chirality in an index-bearing toy, while the naive periodic version cannot. A direct sum of `N` identical walls has index `N` for *any* `N`: this alone does not explain three generations. Likewise, each complete E6 `27=16_1 +10_-2 +1_4` has vanishing U(1)ψ and mixed anomalies, and any number of such complete multiplets remains anomaly-free in those channels. The actual missing calculation is a **charged 7D singular-G2/ADE Dirac problem**, its index/inflow, local anomaly cancellation at each defect, the compactification's spectrum, vacuum selection, and physical Yukawa matrices. **None was constructed.** Literature: Acharya/Witten analyses of conical G2 singularities, anomaly inflow and charged chirality, e.g. [hep-th/0109152](https://arxiv.org/abs/hep-th/0109152) and [anomalies in singular G2](https://www.sciencedirect.com/science/article/abs/pii/S0550321303007399).

## Gate 2: repeated-syndrome detector model for the qutrit [[1833,81,8]] code

Rebuild the W(3,3) 80-vertex 160-edge Levi graph directly from F₃ projective symplectic isotropic lines; reconstruct the two sparse stabilizer matrices over F₃. For repetition length `L=8`:

- `H_X` has shape `(632, 1833)`; `H_Z` has shape `(1120, 1833)`; the product `H_X H_Z^T` vanishes over F₃ and `K=1833-632-1120=81`.
- For `T=3` noisy extraction rounds and a **perfect final boundary syndrome**, form `d_t=s_t-s_{t-1}`. A data error `a e_j` beginning at time `t` induces the signed column `aH[:,j]` in detector round `t`. A measurement fault of amplitude `a` on row `i` in round `t` produces `+a` in detector `(t,i)` and `−a` in `(t+1,i)`. These are discrete spacetime **coboundary signatures**.
- The X-error channel uses `H_Z`, yielding `3×2×(1833+1120)=17,718` distinct one-fault signatures. The Z-error channel uses `H_X`, yielding `3×2×(1833+632)=14,790` distinct one-fault signatures. The code exhaustively enumerates both dictionaries, checks injectivity, and tests actual detector labels. **This is a one-fault lookup decoder**, not a multi-fault, circuit-level decoder.
- **Load-bearing boundary falsifier:** remove the perfect final readout. On the X-error channel (`H_Z`) there are **320** degree-one data-check columns; on the Z-error channel (`H_X`) there are **32**. At the final measurement round, a data fault on one such column and a measurement fault on its incident row produce **identical observed detector records**. This gives **640 X-channel** and **64 Z-channel** indistinguishable fault labels (counting the two nonzero F₃ amplitudes), even though every signature had been unique with a perfect endpoint. Thus neither a literal always-on decoder nor an actual non-ideal final measurement can inherit the earlier uniqueness guarantee without extra assumptions, longer windows, priors or a boundary-condition model. This corrects the tempting overstatement that the bare code is already fault-tolerant.
- Deterministic bipartite conflict-free edge scheduling needs **6 interaction layers for X-check circuits and 7 for Z-check circuits** when considered separately. This is a parallel-interaction resource bound, not a safe qutrit SUM gate ordering or extraction circuit.
- A *specific* assumed fault mechanism propagating an ancilla Pauli to a suffix of qudits within one check can be shortened **modulo that check stabilizer** to at most `floor(w/2)` data-site support: ≤3 for an X check of weight 6 and ≤2 for a Z check of weight 4. This is solely a check-support bound, not a gate-channel hook enumeration.
- A full length-eight edge-fiber X logical splits into two distinct weight-four error vectors with **identical** `H_Z` syndromes. Thus distance eight guarantees correction up to three arbitrary data errors in ideal decoding but does *not* guarantee arbitrary weight-four correction.

At iid fault probability `p` **per modeled fault location** (data and measurement locations in one Pauli channel), the probability of zero or one faults in `M=3(N+r)` locations is `(1-p)^M + Mp(1-p)^(M-1)`. At `p=1e-4` this one-fault-guaranteed subset has probability about **0.7776** (X channel) and **0.8304** (Z channel). These are deliberately **not logical error rates** or even bounds on an optimal decoder; they quantify why the completed one-fault lookup is nowhere near a tested fault-tolerance threshold. The immediate next implementation must include **correlated two-qudit SUM errors, ancilla preparation/readout, repeated syndrome with temporal decoding, hook order, leakage, and logical-failure Monte Carlo**. Prior work: [Fast Fault-Tolerant Decoders for Hypergraph Product and Lifted-Product Codes, arXiv:2608.31040](https://arxiv.org/abs/2608.31040), and [QLDPC decoder under circuit-level noise](https://www.nature.com/articles/s41534-026-01292-1).

## Gate 3: spacetime curvature from *additional* calibrated volume data

Keep the fixed-order causal example of `g_a=exp(2a x²)(−dt²+dx²)` on a known coordinate rectangle. The causal order and light cones do not change with `a`. Its origin curvature changes as `R(0)=−4a`. Suppose **independently** that physical sprinkling intensity per spacetime volume is uniform and the coordinate chart is known. Then the observed spatial coordinate density is

\[
p_a(x)=\frac{\exp(2a x^2)}{\int_{-1}^{1}\exp(2a y^2)dy},\quad
\mathbb{E}_a[x^2]=\frac{\int_{-1}^{1}x^2\exp(2a x^2)dx}{\int_{-1}^{1}\exp(2a x^2)dx}.
\]

The moment is strictly increasing in `a` because its derivative is `2 Var_a(x²) > 0`; hence with those *extra assumptions*, it identifies `a`. An inverse solver and seeded rejection sprinkling at `a=.25` estimate approximately `0.2318`, `0.3129`, and `0.2433` using 500, 2,000 and 10,000 events, respectively. Convergence need not be monotone across independent random samples. Inverting a **given** coordinate-sampling measure is **not** an intrinsic metric reconstruction from a naked causal set. Next requirement: a diffeomorphism-invariant volume estimator derived from interval cardinalities, then a renormalized curvature/action test and continuum response to matter. Standard causal-set work uses *order plus counting* and interval actions, not order alone; see [higher-order causal-set curvature](https://doi.org/10.1140/epjp/s13360-023-04202-y) and [causal sets and emerging continuum](https://doi.org/10.1007/s10714-024-03281-1).

## Gate 4: non-Abelian center holonomy with differential Ramsey quadratures

For SU(3) qutrit shift/clock, `ZX=ωXZ`, `ω=exp(2πi/3)`. The commutator `K=ZXZ†X†=ωI₃`; its adjoint character is **8**, exactly the identity's. A bare color-center gauge transformation is not itself a measurable physical operation on gauge-invariant color-singlet states. The existing repo Pass5709 and H27 quotient work already made that distinction; the test here instead quantifies **what a physical coherent reference would have to provide**.

If a realizable reference-controlled fundamental Wilson operation exists, measure two complementary Ramsey quadratures of both identity and center arms. Under a common unknown phase `θ`, the mean complex signals are `m_I=V_I e^{iθ}` and `m_K=V_K e^{i(θ+2π/3+Δ)}`. Their complex ratio cancels the common phase and exposes the center offset plus *relative* phase drift Δ. For visibility at least `V_min=.8`, independently bounded relative drift `|Δ|≤.12 rad`, and IID binary ±1 observations, a four-coordinate union-Hoeffding bound with `δ=.01` gives **209 accepted shots for each of four quadratures (836 accepted events total)** as a conservative sufficient condition for identifying the phase nearest to `0` versus `2π/3`. More precisely, `t=sqrt(2 log(8/δ)/N)`, each complex mean has error ≤`sqrt(2)t`, and the total phase uncertainty is bounded by `|Δ|+2asin(sqrt(2)t/V_min)<π/3`. Seeded binomial tests at 250, 1,000, 4,000 shots show finite sampling noise.

**Physical obstacle:** neither a gauge-invariant controlled-Wilson interferometer, nor its charged reference sector, detector efficiency, relative-drift calibration, nor a photonic loop Hamiltonian has been demonstrated. Treat `836` as an idealized four-setting accepted-shot planning bound, **not** a field-theory or hardware claim.

## Gate 5: calibrate both acceptance and multi-time output counts

Beyer et al. [arXiv:2611.17268](https://arxiv.org/html/2611.17268), Supplement VI equation S38, prove the qudit three-time witness `W3 = sum of pairwise root fidelities in two mutually unbiased bases - (1/2)||E1(I)-I||1`. A **negative** witness rules out one common three-time classical-memory model. Critically, it does **not** show the three *pairwise* channel combinations are individually classically simulable; that demands separate decompositions or a suitable pairwise SDP.

The earlier repo scripts assumed an already certified common acceptance lower bound `η`; here its **statistical estimation** is included. For seven preparation settings with `M` attempted shots each, observe accepted count `N_j` and accepted three-outcome frequency vectors. Allocate total confidence error `δ=.01` equally: `δ_eff=.005` for the seven one-sided binomial efficiency bounds and `δ_out=.005` for the 21 two-sided accepted-output coordinates. Define

\[
\eta_{\min}=\min_j(N_j/M)-\sqrt{\frac{\ln(7/\delta_{\rm eff})}{2M}},\quad
 t=\sqrt{\frac{\ln(42/\delta_{\rm out})}{2\min_j N_j}}.
\]

Then for each output coordinate the true (completion-inclusive) distribution obeys `p_true ≤ min(1,eta_min*min(1,p_hat+t)+(1-eta_min))`, without assuming a model for rejected trials. Upper-bound each quantum root fidelity by the corresponding classical Bhattacharyya coefficient and lower-bound first-time nonunitality as `S1≥max(0,3eta_min*max(0,r_hat0−t)−1)`. The resulting `W3_upper` has **simultaneous 99% statistical coverage**, conditional on IID attempts and accepted outputs, preparation and measurement validity, stationary channel, and the calibration protocol's acceptance assumptions. This correctly includes uncertainty of the *efficiency calibration itself*.

Prospective reference **not physical data**: `γ=.75`, late-channel depolarization `ε=.01`, efficiency `.995`. For perfect expected output frequencies and attempted shots per setting of 500,000; 1,000,000; 2,000,000; 5,000,000, the conservative witness upper is approximately `+0.02889; -0.07295; -0.14855; -0.21857`. A seeded binomial/multinomial demonstration at 2 million attempted per setting gives `W3_upper≈−0.14510`; at 5 million gives `−0.21705`. The **negative mathematical certificate is conditional on that illustrative snapshot model**; it is not a measured non-Markovian device or an actual joint physical process. Losses and rejected trials may be state-dependent; the conservative completion guard does not replace verifying that the observed snapshots arise from one stationary physical dynamics. Pairwise classicality remains separately unverified.

## Independent outside-the-box gate: marginal gluing versus global memory

There is a clean **classical** obstruction reminiscent of the compatibility issue in the new quantum-memory paper. Let A, B, C be bits with individually fair marginals. Prescribe each pair to disagree with probability `q`. Every pair's 2×2 distribution is individually legitimate for every `q∈[0,1]`. But for a single assignment of three bits the number of disagreeing pairs among AB, AC, BC is either 0 or 2; it is never 3. Thus a global joint distribution would obey `3q≤2`, i.e. `q≤2/3`. A linear program over all eight bit assignments verifies global compatibility for `q=.5,.6,2/3` and infeasibility for `q=.75,1`. This is an exact **marginal gluing / contextuality analogy**, not a proof that the specific three qutrit channels each admit a compatible classical-memory instrument. It suggests a practical independent SDP workbench for the actual quantum time-channel compatibility problem without conflating pairwise tests with triple tests.

## What is *not* closed and how to reproduce

No compact singular G2 index, no E8 UV Lagrangian or three-family prediction, no logical error threshold, no gauge-invariant physical SU3 loop, no Einstein continuum action, no actual measured quantum memory, and no pairwise classical process decomposition. These remain research gates. The exact and model-conditional workbench is reproducible with NumPy, SciPy, and NetworkX:

```bash
python analysis/toe_20261120_fivefront_hardware_gravity_index.py
python -m unittest discover -s tests -p test_toe_20261120_fivefront_hardware_gravity_index.py -v
```

The executable generates `data/toe_20261120_fivefront_hardware_gravity_index.json`, which freezes all numerical targets, assumptions and proofs for independent replay. The test file checks ten geometry/physics assertions plus an eleventh classical-gluing compatibility gate. Temporal-detector coboundaries and classical marginal gluing are promising **mathematical analogies** with the broader IS architecture, not evidence that spacetime causality or quantum context is literally constructed from these codes.
