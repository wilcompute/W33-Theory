# Five TOE physics closures: E8 anomaly factorization, Yukawa gap, orbifold multiplicities, signed causal layers, honest Bell tests

**Date: 2026-11-19. Scientific status:** Five executable, independently checked *conditional* consistency tests; one novel-to-repository two-channel anomaly factorization and one signed causal-layer cancellation. **NOT a complete anomaly-free G2/M-theory vacuum, a derived quantum gravity action, or a Theory of Everything.**

## Collision audit and literature

Reviewed current `wilcompute/W33-Theory` master `d5edaa9a0`, which has `analysis/2026-11-19_five_deep_physics_gates_global_uniqueness_report.md`: hypercharge nonuniqueness, gauge-center SU2, KMS noise, causal history entropy and topological cone; `4ea5ae0ad` renormalizable messenger vacuum; `cb1a66717` original balanced E8 point sources and exact strict bulk-cup obstruction; `ff5090ff5` toric singlet model and causal-link counts; and `21e8ff606` true 4D overlap index. We did not silently claim earlier mathematical results as original.

Recent literature checked on the web: [Local d'Alembertian for causal sets, Phys. Rev. D 113 (2026) 024046](https://doi.org/10.1103/np89-qzjp), which challenges any blanket assertion that convergent causal-set differential operators MUST be nonlocal; [Benincasa–Dowker–Glaser actions by quantum counting (May 2026)](https://doi.org/10.1103/qdst-yrh6); [Five-dimensional SU5 x U1PQ GUT (2025)](https://doi.org/10.1140/epjc/s10052-025-14320-9), which actually builds triplet/octet boundary zero modes and full two-loop running; [General orbifold vacuum stability (2025)](https://doi.org/10.1103/PhysRevD.111.095013) and [experimental indefinite causal order (2026)](https://doi.org/10.1126/sciadv.aee2912). The latter is quantum-optical prior art, not evidence for a novel TOE.

## Gate I: Original E8 spectrum needs at least TWO Green–Schwarz shift directions

The E8 source `sector_census()` has precisely 3 chiral Spin10 16s, 5 real 10 multiplets, and 8 charged singlets, with three Abelian Cartan charges. We independently sum the full *original* chiral fermion anomaly coefficients (DO NOT add artificial cancelling mirror fields). In the source's integral charge basis:

```
A_4Dgrav-U1 = (20,10,10) = 10 (2,1,1),
A_Spin10²-U1 (T(10)=1) = (2,1,1).
```

For formal commuting Abelian field-strength variables a,b,c, the cubic tensor gives polynomial

```
P(a,b,c) = 2(10a³+6a²b+6a²c+9ab²+18abc+15ac²+8b³-3b²c+11c³).
```

In the simplest 4D Green–Schwarz realization with ONE axion that shifts by a vector s under U1 gauge transformations, the linear gravitational and Spin10 anomaly terms require **s parallel to (2,1,1)**. The reducible U1³ anomaly must then factor as `P=(2a+b+c) Q2(a,b,c)` for some quadratic Q2. But a direct symbolic restriction gives

```
P(a=-(b+c)/2,b,c)=(3/2)(b-5c)(b+c)(5b-c) != 0.
```

**Conditional one-axion no-go:** the cubic anomaly is NOT divisible by the only shift direction compatible with the linear anomalies. One Green–Schwarz shift field with a standard quadratic topological coupling cannot cancel all three families of anomalies in this spectrum by itself. No automatic salvation follows from Higgsing all three U1 factors, nor from the three newly introduced vectorlike messenger pairs (which have zero net perturbative anomaly).

**Constructive two-axion polynomial decomposition.** Let `L1=2a+b+c`, `L2=b-5c`. Exact polynomial division gives

```
P = L1 * (20a²+2ab+2ac+17b²+34bc+29c²)/2
  + L2 * 3(b+c)(5b-c)/2.
```

So two *independent integral* axionic gauge-shift vectors `s1=(2,1,1), s2=(0,1,-5)` are algebraically enough to span the cubic anomaly polynomial; the grav/Spin10 mixed anomaly can be assigned to s1. This is a **necessary algebraic factorization certificate, NOT a complete anomaly cancellation**. The 6D anomaly-polynomial normalizations, local counterterms, quantized WZ/GS couplings, spin/gravity global anomalies, supersymmetric axion supermultiplets, generalized Chern–Simons counterterms, and higher-dimensional inflow all still need a common derivation. Other chiral charged fields or separate defect inflow can change the minimum.

**Possible crack:** Three broken Abelian phases already exist in the singlet Higgs vacuum, suggesting a place to seek Wess–Zumino/axion couplings; their coefficients must be *computed from UV physics*, not invented to fit this polynomial.

## Gate II: A full-rank formal Yukawa texture still does not explain charged mass hierarchies

The exact previous 19-field messenger SUSY vacuum has three source-allowed operators

```
16_1² 10_34 S12conj/M,
16_2² 10_34 S12/M,
16_3² 10_24 S13/M.
```

The code imports their actual nonzero singlet VEVs and checks that, if all three physical overlaps and weak-Higgs projections are set to the same value, their mass spurion ratio is only **1.4422** (roughly). A target family mass hierarchy of `10^5` (illustrative top/up order of magnitude, not a same-renormalization-scale fit) requires the actual overlap times light-doublet-Higgs projections to differ by at least **69337.5** across the three. This bound is just `(required physical ratio)/(supplied maximum spurion ratio)`, not proof against topological flavor localization.

Two different Spin10 10s appear (10_34 vs 10_24); a genuinely common Standard Model Higgs doublet must arise from an explicitly derived light-Higgs mixing/projection. Neither gauge permission nor having nonzero F/D-flat condensates makes a physical Yukawa integral nonzero. The original punctured S3 ordinary bulk relative cup is *exactly zero* in the strict source model; boundary/defect/M2 terms or changed source topology remain necessary.

## Gate III: The orbifold GUT solves one splitting but not the next

For two boundary parities `P0=I5`, `Ppi=diag(1,1,1,-1,-1)`, one bulk adjoint `24_F` projects the 12 off-block X/Y generators out of zero modes but retains **one SU2 triplet, one SU3 octet, and one singlet**. Two identically assigned 24_F retain **two triplets AND two octets**, not the desired two triplets and *one* octet. Thus additional mass matrices, distinct boundary assignments or brane couplings are still necessary. The 2025 5D SU5+PQ article already provides a more elaborate precedent, including doublet multiplets and two-loop matching.

We also test a toy pure KK spectral-sum issue. The massive (+,+) tower has energies `n*pi/L`, the (+,-) tower `(n+1/2)*pi/L`. The raw unweighted relative logarithmic sum through level N is exactly

```
S_N=sum_{n=1}^N ln((n+1/2)/n)
   =ln Gamma(N+3/2)-ln Gamma(3/2)-ln Gamma(N+1)
   ~ (1/2)ln N + ln(2/sqrt(pi)).
```

It is **not cutoff-independent**. This is not itself a physical unification correction: complete 5D gauge/fermion/scalar beta coefficients, threshold matching conventions, 5D brane-localized counterterms and regulator dependence must be included; the sum merely prevents an unqualified claim that zero-mode projection automatically predicts unique low-energy couplings. Unification, proton decay and KK stability are still open.

## Gate IV: signed 3+1 causal layer combinations remove the lightcone divergence at expectation level

The previous 3+1 Poisson sprinkling future cone (0<t<1) has an expected number of direct causal links from its origin growing `pi sqrt(6)*sqrt(rho)` at density rho. That divergence does NOT prove all causal differential operators have to be nonlocal; a 2026 PRD paper constructs a distinct convergent local operator.

**New-to-this-repo constructive cancellation:** Let `L_k` be the number of events above a fixed origin with *exactly k intervening sprinkled events*, for k=0,1,2. Their expected values are

```
E[L_k]=pi*rho int_0^1 ds exp[-rho*pi*s²/24] (rho*pi*s²/24)^k/k!
    * g(s),
g(s)=sqrt(1-s)-s ln[(1+sqrt(1-s))/sqrt(s)].
```

Individually each expectation is O(sqrt(rho)). Expanding `g(s)=1+s[(ln s)/2-ln2-1/2]+O(s²)` gives leading coefficients `sqrt(6*pi)*Gamma(k+1/2)/k!` and a common subleading log(rho) contribution per layer. The integer weights

```
(w0,w1,w2)=(1,-5,4)
```

satisfy BOTH `sum_k w_k Gamma(k+1/2)/k! =0` and `sum_k w_k=0`. The exact rational 2×3 moment matrix has rows `(1,1/2,3/8)` and `(1,1,1)`, a one-dimensional nullspace, and its primitive integer generator is uniquely `(1,-5,4)` up to overall sign/scale. The remaining finite term is an exact constant,

```
lim_(rho->infty) E[L0-5L1+4L2]
 = pi/(8*(pi/24))*(psi(1)-5psi(2)+4psi(3))
 = 3.
```

Numerical integration: rho=40 ->4.0903, 160 ->3.3629, 2560 ->3.07619, 163840 ->**3.00913**, approaching 3 as predicted.

This is a **finite signed expectation**, NOT finite physical graph valency, cost, a constructed d'Alembertian or dynamical Einstein tensor. Signed weights can enforce cancellations in an operator that still touches many events. Geometry and sprinkling are supplied; no intrinsic quantum path measure or scale-setting is derived. But it gives a concrete example of how a divergence in raw causal adjacency can coexist with bounded expectation of a geometrically structured, signed operator.

## Gate V: a local hidden-variable system can fake CHSH=4 under setting-dependent postselection

A proposed single-/two-photon TOE experimental test must distinguish standard quantum predictions from both experimental artifacts and adversarial classical hidden-variable descriptions. We construct a **fully local deterministic** model with a shared random hidden variable `lambda=(x_target,y_target)` uniformly sampled over the four setting pairs. Alice's detector clicks only when her locally chosen setting equals x_target, Bob's only for y_target. At the detected pair, choose output products `(+1,+1,+1,-1)` for (00,01,10,11). There is no dependence of a local output or local detection on the other party's actually chosen setting.

Each setting pair has joint detection fraction **1/4**, but after discarding undetected trials, the four correlations yield

```
S_CHSH_postselected = 1+1+1-(-1)=4.
```

This exceeds the ordinary quantum Tsirelson bound 2sqrt2, **without** any nonlocal dynamics. With settings chosen independently *after* a trusted event-ready herald, the accepted hidden-variable ensemble cannot be chosen differently for each setting and a local deterministic CHSH bound 2 is restored. Full detection-loophole closure still matters. This is a standard detection-loophole construction, not a new loophole or new quantum prediction.

**Interpretation:** A spectacular Bell statistic is not a TOE signature unless operational constraints, heralding/efficiency, setting independence and a quantitative nonstandard physical prediction are specified.

## Independent reproducible deliverables

```powershell
python analysis/toe_20261119_two_GS_axions_causal_layer_and_Bell_gates.py
python -m unittest discover -s tests -p test_toe_20261119_two_GS_axions_causal_layer_and_Bell_gates.py -v
```

Output data: `data/toe_20261119_anomaly_GS_signed_causal_orbifold_chsh.json`. Producer independently calls the original sector census and the previous renormalizable messenger model, then computes exact anomaly polynomials, conditional Yukawa deficit, exact KK gamma product, Poisson layer integrals, and enumerates the four deterministic local hidden-variable states. New assertions verify each gate. The original paper's local causal d'Alembertian is a separate construction; do not misrepresent this simple signed layer operator as reproducing its proof.

## Top five best orthogonal next experiments

1. **Physical anomaly inflow:** realize the TWO explicit shift vectors and the polynomial quadratic GS coefficients from genuinely quantized chiral axion/defect fields in a compact E8/G2 construction; derive supersymmetric Wess–Zumino couplings, global anomaly cancellation and all zero-mode content simultaneously.
2. **Real charged masses:** solve the matter/Higgs Dirac localization and M2/defect Yukawa integrals for all three source spinors in one compact background; generate the actual factor >10^4–10^5 hierarchy *without inserting it as coupling constants* and reduce to one light electroweak Higgs.
3. **Complete orbifold GUT:** choose complete boundary parities for two triplets and one octet, calculate KK power/log corrections in a consistent regulator, include all 5D gauge/scalar/matter content, and compute proton decay and two-loop unification; compare its naturalness to the 4D three-adjoint solution.
4. **Derive Lorentzian causal gravity:** test a signed-layer operator against independent 2026 local d'Alembertian convergence benchmarks (constant, linear, quadratic fields, boosted frames); establish positivity/no extra poles, causal constraint closure and a 3+1 dynamical Einstein continuum. Include actual per-event computation costs, not just signed expectation.
5. **Design an event-ready beyond-QM falsifier:** specify a candidate microscopic modification to an operational multi-time process tensor, predict a numerical deviation with a conserved complete photon/reference budget, require blind registered trials and a valid classical/quantum null including setting-independent heralding.

No TOE has been solved; the nearest new constraints are the two-direction E8 anomaly requirement and the causal signed-layer cancellation mechanism.
