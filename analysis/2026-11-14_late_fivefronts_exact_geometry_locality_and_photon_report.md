# Five independent TOE follow-throughs: full F8 tangent geometry, protected KK tower, exact H27 no-go, thermodynamic W33 frame selector, calibrated photon witness

**Research:** 2026-11-14 Eastern. **Scope:** exact finite/dynamical conditional mathematics, numerical crosschecks at an exact algebraic six-qubit witness, and a synthetic calibrated-readout model. **Not** a completed TOE, no Einstein-equation derivation from W33, no observed photonic or gravitational data.

Reproducer: `analysis/toe_20261114_fivefronts_late_independent.py`

Machine-readable certificate: `data/toe_20261114_fivefronts_late_independent_certificates.json`

Independent regression: `tests/test_toe_20261114_fivefronts_late_independent.py`

This pass checks existing master and distinguishes prior owners:
- Prior exact F8 witness: Pass12671 \`analysis/w33_f8_exact_witness.py\`, \`data/w33_f8_exact_witness.json\`. Parallel Pass12672, addendum \`b73225a42d53\`, established a global order-nine Clifford symmetry and a numerically tight degree-six SOS bound **on an eight-dimensional code space**. Its C4 subspace reductions do **not** establish a global C64 lower bound.
- Previous five-front passes \`056c4fc9f348\` and \`071fbdaa5024\` already established the original D9 unequal-flux branch, H27 four-pulse cursor, W33 1,620-frame fluctuations, and idealized five-setting optical witness.
- Existing W33 apartment/framing: Pass4474 and October TOE23. This pass contributes an explicitly **hypothetical thermodynamic interaction**, not the apartments or the finite frame Hamiltonian.
- The original F8 SDP/PPT bounds from other tracks are not overwritten.

## 1. F8: full 126-real-dimensional projective Hessian at exact pure witness

From Pass12671's **exact rank-one density matrix** in \`Q(2cos(2π/9),sqrt3,i)\`, reconstruct its normalized eigenvector \`psi\` to double precision. Independently enumerate the 567 distinct nonidentity Hermitian Pauli observables in the nine F8-regulus MUB classes. Define on the unit sphere

\`c8(psi)=sum_{P in C} <psi|P|psi>^2\`, exact witness value \`(47-32 cos(2π/9))/9≈2.498508646688078\`.

For real tangent \`v\` orthogonal to both \`psi\` and the global-phase vector \`i psi\`, the constrained Hessian quadratic form (i.e., the geodesic second derivative at 0) is

\`H(v,v)=8 sum_P (Re<v|P|psi>)^2 +4 <v|(sum_P r_P P)|v> -4 c8 ||v||^2\`,
with \`r_P=<psi|P|psi>\`.

The full 126x126 real symmetric Hessian (not merely eight-dimensional code-space directions) has **124 eigenvalues >1e-6, two numerically null, zero negative**. The third-smallest eigenvalue is approximately \`1.85951599137\`, and the largest about \`74.9221952661\`. The full stationarity residual is \`1.7e-14\`. Seven random finite-difference directional checks of the Hessian agree within \`1.1e-6\` (step \`2e-4\`). **These are numerical certificates; the eigenvalues have not been converted to exact algebraic positivity proofs.**

### New finding: two flat modes form a fourth-order perfect square and candidate straight lines of equal-value states

Let \`e0,e1\` span the numerically flat tangent kernel. For any \`v=cos(theta)e0+sin(theta)e1\`, integrate out all 124 positive-Hessian tangent modes \`w\` at order \`t^2\`, minimizing the quartic energy using the Hessian pseudoinverse. The resulting homogeneous fourth-order form on the unit circle is numerically

\`Qeff(theta)=A+B cos(4theta)+C sin(4theta)\`,
\`A≈2.241475335793096, B≈0.630806251270658, C≈-2.150882412947448\`.

Its discriminant \`A²-B²-C²≈-3.55e-15\` vanishes to numerical precision. Hence it behaves like a nonnegative **perfect square** with two perpendicular zero rays. Null angle \`theta≈0.4640186734023375\` radians and its translate by \`π/2\`. Numerically \`Qeff≈0\` and forcing onto the remaining flat kernel is <5e-15.

Surprisingly, the relaxation correction vector \`w\` for these two null rays has Euclidean norm \`~4.85e-15\`, so it is numerically **zero**. The simpler \`psi(t)∝psi+t v\` yields **the same c8** within ~1e-15 across \`t=0.025,0.05,0.1,0.25,0.5,1,2\`, including well outside the infinitesimal regime.

This was checked more strongly than point sampling. For \`a(t)=psi+t v+t²w\`, every Pauli expectation numerator \`a(t)^† P a(t)\` and squared norm \`||a(t)||²\` has degree ≤4. The identity

\`sum_{P in C} [a(t)^† P a(t)]² - c8 ||a(t)||⁴=0\`

is a polynomial of degree ≤8. **All nine coefficients were independently computed by convolution** (each Pauli term independently evaluated) and the maximum absolute coefficient residual is approximately \`2.7e-15\`. This is striking numerical evidence for **positive-dimensional, crossing equal-value projective state families** through the exact witness. It is **not an exact algebraic proof** since \`v\` comes from a floating-point Hessian and may hide algebraic coefficients. The next step is algebraically recover \`v\` and verify the 9 polynomial coefficients in the exact field.

A local flat-family observation **does not** prove the global lower bound \`c8≥(47-32cos(2π/9))/9\`. Existing competing state searches and global SOS bounds remain relevant.

## 2. D9 Einstein–Maxwell: protected spin-2 KK tower and uniform Maxwell vector

Assume exactly the previously verified 9D action \`R-F²/4\` on \`AdS5 x S²(r1) x S²(r2)\` with unequal quantized magnetic flux, \`t=r1²/r2²>0\`. The previous pass proved the unique positive-radius charge branch and homogeneous radion masses.

The complete **decoupled external transverse-traceless spin-2** sector follows from scalar harmonics on the compact product. The KK Fierz–Pauli mass is

\`m²L_AdS² = 20 [ell1(ell1+1)+t ell2(ell2+1)]/(1+t)\`

with harmonic multiplicity \`(2ell1+1)(2ell2+1)\`, for all nonnegative integers \`ell1,ell2\`. The unique \`(0,0)\` mode is massless. All other spin-2 modes are strictly positive, with first gap \`40min(1,t)/(1+t)\` that tends to zero at extreme flux anisotropy. The numerical verifier exhaustively checks a finite 9×9 index window \`0≤ell_i≤8\` with summed harmonic degeneracy **6561**, and the symbolic formula covers the full tower.

There is additionally a spatially constant internal harmonic of the abelian gauge fluctuation \`δA_mu(x)\`, with no internal field strength \`δF_{mu a}=0\`; its 5D Maxwell equation yields a protected **massless U(1) vector** in this unwarped classical ansatz. This does not by itself include the isometry-derived graviphoton sectors.

**Remaining open:** mixed Einstein–Maxwell scalar/vector harmonics, gauge constraints, BF-dangerous coupled modes, flux backreaction at nonlinear level, quantum scales, and any E6 exceptional-field-theory embedding. For prior full product-manifold fluctuation analysis, see Brown–Dahlen, *Phys. Rev. D* 90 (2014), arXiv:1310.6360: https://arxiv.org/abs/1310.6360. Their general theory is not rederived here.

## 3. H27 local Hamiltonian: exact long-range-hop obstruction for any continuous-time logarithm of an isolated cursor cycle

The prior 108-state H27 reversible cursor has nine disjoint 12-cycles. Take **one isolated 12-cycle** with directed shift \`S|j>=|j+1>\` and unit-tick evolution \`exp(-iH)=S\` for time-independent Hermitian \`H\`.

Since \`H\` commutes with \`exp(-iH)=S\` and the 12 eigenvalues of a single cycle \`S\` are simple, H must be **circulant**, diagonal in the exact Fourier eigenbasis of S. Its 12 eigenphases must have the form

\`h_k = -2πk/12 + 2π n_k\`, \`n_k∈Z\` (or the opposite sign according to shift orientation).

The matrix entry connecting opposite sites is the alternating Fourier coefficient:

\`H_{j,j+6}= 1/12 Σ_k (-1)^k h_k = (π/12)(1+2m)\`, \`m∈Z\`, up to overall Fourier sign.

Therefore **\`|H_{j,j+6}|≥π/12\` for every exact time-independent Hermitian logarithm of a single directed 12-cycle shift**. Its principal logarithm saturates the bound. This is an exact elementary integer-parity proof, not merely numerical evidence. A real-symmetric H is additionally impossible, since its propagator is symmetric but a directed shift is not. The producer independently enumerates 100 random spectral branches and checks the formula.

**Scope:** This theorem rules out exact single-tick evolution by an *isolated* short-range Hamiltonian on each twelve-site clock cycle. It does **not** exclude a multicycle/cross-channel Hamiltonian, stroboscopic driven circuit, extra ancillas, or approximations. The general chiral information-flow obstruction for one-dimensional quantum walks is related to Gross–Nesme–Vogts–Werner, *Commun. Math. Phys.* 310 (2012), arXiv:0910.3675: https://arxiv.org/abs/0910.3675.

## 4. W33 symmetry and frame selection: a **conditional** thermodynamic transition

Prior W33 work establishes 1,620 projective symplectic apartment frames, each carrying four signed coordinate axes and eight nearest-neighbor generators on 81 affine addresses. Prior finite hopping models fail to select a frame spontaneously. Simply choosing one frame by hand is not a physical derivation.

Construct a **new specified many-copy toy interaction** among M copies choosing one of q=1620 apartment labels:

\`H_M= -J/(2M) Σ_{a,b=1}^M 1[sigma_a=sigma_b]\`, \`J>0\`.

It is invariant under **all permutations** of the 1620 labels and therefore PSp(4,3)-invariant; no particular frame is explicitly favored. The thermodynamic mean-field free-energy functional is \`F(p)=Σ_i p_i ln p_i -(βJ/2)Σ_i p_i²\`.

At the **first-order coexistence point**

\`βJ_c=2(q-1)ln(q-1)/(q-2)≈14.7882621026\`,

the uniform state \`p_i=1/q\` and q ordered states \`p_dominant=(q-1)/q\`, \`p_other=1/[q(q-1)]\` have exactly equal free energy and satisfy the stationary equations. The uniform local spinodal is \`βJ=q=1620\` and so lies far above the coexistence threshold. This is the established Curie–Weiss–Potts transition in our normalization (the model is **not a novel Potts theorem**): see https://link.springer.com/article/10.1007/s10955-026-03571-9 ; https://www.cambridge.org/core/journals/advances-in-applied-probability/article/on-approximating-the-potts-model-with-contracting-glauber-dynamics/8E47C85A421D23D07DE50860487744B9 .

For every **finite M**, Gibbs equilibrium is symmetric and there is no exact spontaneous frame selector. In the \`M→infinity\` thermodynamic limit, choosing an ordered pure phase gives one apartment and hence a sparse eight-neighbor *Euclidean address* graph; no Lorentzian spacetime or gravity follows. Crucially the all-to-all ferromagnetic Potts alignment was **inserted as a toy interaction**, not deduced from the W33 exchange laws.

## 5. Sixteen-mode photonic GHZ: calibrated per-rail confusion and asymmetric parity flips

The project encodes four **virtual/internal qubits** in one 16-rail photon. A trusted five-setting witness gives \`F_GHZ=(p0+p15+A)/2\`, \`A=(1/4)Σ_{j=0}³(-1)^j <M(jπ/4)^⊗4>\`. The previous code verifies this identity on arbitrary density matrices and rejects a false-positive \`X^⊗4\` signal.

Here use a full **16×16 column-stochastic readout confusion matrix**, for each true rail \`x\`:

\`C_{y|x}=(1-εR-εL-d) δ_{y,x} + εR δ_{y,x+1} + εL δ_{y,x-1} +d/16\` (mod 16),

with hypothetical \`εR=.023, εL=.017, d=.006\`. Solve the **conditioned inverse readout vector** \`w=C^{-T}(e0+e15)\`, so \`E[w_(reported)]=p0+p15\`. Its 1-norm matrix condition number is approximately **1.098**.

For equatorial parity, plus-to-minus flip \`ε+=.025\` and minus-to-plus \`ε-=.018\` give gain \`g=1-ε+-ε-=.957\`, bias \`b=ε-−ε+=-.007\`. Correct each parity estimator as \`μ=(μ_reported-b)/g\`.

Set **12,000 accepted Z detections** and **8,000 accepted events at each of four equatorial settings**; draw frozen independent synthetic clicks. The five simultaneous two-sided Hoeffding inequalities, union bound α=.01, give a statistical fidelity width ~**0.030662**. Assume, *in addition*, a bound **0.002** on each actual confusion-matrix column's ℓ1 deviation and **0.002** on each actual parity flip rate's absolute error. The worst-case calibration contribution is ~**0.005209** by triangle inequality and the inverse readout weights.

The synthetic fidelity estimate is **0.965911**, yielding the conservative **99%-confidence one-sided bound 0.930040** after statistical and systematic allowances. Nominal raw launch expectation is **54,438** at 98% transmission per traversed optical layer and 93% detection efficiency. These are NOT actual laboratory results and the raw count is a model expectation, not a high-probability launch guarantee.

A fidelity >1/2 under trusted internal factorization certifies multipartite entanglement of those **virtual qubit subsystems**, **not** four space-like separated entangled photons or device-independent Bell violation.

## Cross-front conclusion, limitations, and next experiments

The most surprising result is the *numerical polynomial identity* in the F8 flat sector: apparent Hessian zero modes can encode **entire straight equal-value pure-state curves**, not merely quartic-soft fluctuations. An exact field certificate, independent derivation of the tangent vectors and rigorous global minimum are still missing.

The KK calculation finishes **only the decoupled external spin-2 tower** (plus a protected vector zero mode), not the mixed Maxwell-gravitational sectors. The H27 theorem prohibits a particular continuous-time implementation but offers testable alternatives with ancillas or time-dependent gates. The Potts model gives a conditional thermodynamic symmetry-breaking mechanism and isolates the still-missing derivation of native interactions. The photon protocol has explicit model-dependent calibration and loss controls but no physical device data.

**Commands (Windows checkout):**
\`\`\`powershell
py -3 analysis/toe_20261114_fivefronts_late_independent.py
py -3 -m pytest tests/test_toe_20261114_fivefronts_late_independent.py -q
\`\`\`

The finite proof and numerical claims remain separately labeled in the JSON certificate. No result in this packet purports to derive the complete Standard Model, physical c, a Lorentzian metric or quantum gravity from the W33 finite geometry.
