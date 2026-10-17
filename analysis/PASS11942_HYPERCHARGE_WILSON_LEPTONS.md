# Pass 11942: a hypercharge Wilson line on the 5̄ torus fixes the lepton ratios from the quark fit

> **Scope and convention (added after the intake).**
> * **Scope.** z_e = 6·z_d assumes the 5̄ Wilson line lies along pure SU(5) hypercharge. TOE55 shows Y + t(B−L) is
>   anomaly-free for every t. Along that direction z_e/z_d = X(e^c)/X(Q) = 6(1+t)/(1+2t). The band of Pass 11943 and the
>   exclusion of Pass 11945 are statements at t = 0.
> * **CP convention.** The CP-orientation convention of Pass 11941 applies here too.

> **Corrected by Pass 11943.** A fifth chain (branch B, seed 7) excludes the data. The claim "near the centre of every
> chain's band" is withdrawn. Over the quark-acceptable region the rule gives m_μ/m_τ ≈ 0.029–0.081 and
> m_e/m_μ ≈ 0.002–0.017: this contains the data and excludes minimal SU(5), but it is a band, not a sharp prediction.

Producer: `analysis/w33_pass11942_hypercharge_wilson_leptons.py`
Certificate: `data/w33_pass11942_hypercharge_wilson_leptons.json`
Regression: `tests/test_w33_pass11942.py`
Track: Claude. Answers the open question of Pass 11941: why the P-odd Wilson lines sit only in the down sector.

## The rule

**Setting.** The SU(5) Yukawas are level-3 theta nulls on near-product homes.
* The up coupling 10·10·H_u lives on two 10 factors.
* The down coupling 10·5̄·H_d lives on (10 factor, 5̄ factor).
* The lepton coupling is Y_e = Y_dᵀ in SU(5).

**Where the Wilson line goes.** Put a hypercharge Wilson line a **only on the 5̄ factor**. This matches the F-theory
practice of keeping hypercharge flux off the 10 curve. On that factor the theta argument collects the 5̄ matter field and
H_d. By hypercharge conservation their sum is minus the hypercharge of the 10 field in the coupling:

| coupling | Wilson argument |
|---|---|
| down, Q d^c H_d | z_d = (Y_dc + Y_Hd)·a = −Y_Q·a = −a/6 |
| lepton, e^c L H_d | z_e = (Y_L + Y_Hd)·a = −Y_ec·a = −a |

So **z_e = 6·z_d**.

**The up coupling.** It has no 5̄ factor, so it stays Wilson-free. That is exactly what Pass 11941 needed to keep the
Weber law and the neutrino relation of Passes 11938–11940.

## Results

**1. Quark fit.** With Wilson lines only on the 5̄ factor (10 real parameters), all eight quark observables (masses, CKM,
J) are reproduced within 0.4%.
* There are two branch classes, A and B, related by the frame τ_d → τ_d − 1.
* Both have the 5̄ factor in its cusp regime (Im τ_d ≈ 0.017) and |ε_d| ≈ 0.02.

**2. Lepton ratios at the best fits, with no lepton parameter.** Data at M_Z: m_μ/m_τ = 0.0588, m_e/m_μ = 0.00474.

| rule z_e/z_d | A: m_μ/m_τ, m_e/m_μ | B: m_μ/m_τ, m_e/m_μ |
|---|---|---|
| 1 (minimal SU(5), Y_e = Y_dᵀ) | 0.0185, 0.0504 | 0.0185, 0.0504 |
| 0 (matter − Higgs) | 0.0092, 0.207 | 0.221, 0.00022 |
| −3/2 (matter only) | 0.0865, 0.00177 | 0.190, 0.00034 |
| **6 (gauge-invariant)** | **0.0532, 0.00523** | **0.0449, 0.00706** |

For rule 6, y_b/y_τ = 1.22 (A) and 1.18 (B), with the quasi-periodic Wilson-line normalisation included.

**3. Posterior (frozen search record).**
* **Method.** Metropolis MCMC over the 10 parameters, with χ² from the quark data errors: masses 5–20%, V_us 0.3%,
  V_cb 2.5%, V_ub and J 5%. Four chains of 4000 steps, local to the two branch classes; median χ² 4.0–5.0.
* **Predictions under rule 6.**

| chain | m_μ/m_τ median [90%] | m_e/m_μ median [90%] | y_b/y_τ median |
|---|---|---|---|
| A1 | 0.0547 [0.036, 0.076] | 0.00484 [0.0022, 0.012] | 1.23 |
| A2 | 0.0571 [0.038, 0.081] | 0.00448 [0.0021, 0.009] | 1.25 |
| B1 | 0.0530 [0.039, 0.067] | 0.00513 [0.0028, 0.010] | 1.22 |
| B2 | 0.0521 [0.041, 0.071] | 0.00504 [0.0027, 0.008] | 1.22 |

* **Against the data.** Both measured lepton ratios lie near the centre of every chain's band.

## Reading

**Why minimal SU(5) fails here.** Theta-null Yukawas with Y_e = Y_dᵀ fail for leptons exactly as minimal SU(5) does,
by factors of 3 and 10.

**What repairs it.** The hypercharge Wilson line that the CKM needs (Pass 11941), under the gauge-invariant charge
rule, repairs both lepton ratios to Georgi–Jarlskog quality. For comparison, GJ's factors 3 and 1/9 give 0.0555 and
0.0056. No 45-Higgs and no lepton parameter is used.

**One background, two jobs.** The same background that generates the Cabibbo angle also fixes m_μ/m_τ and m_e/m_μ.

## Scope

* **Rules tried.** Three non-trivial rules were compared against the minimal baseline (look-elsewhere factor 3). Rule 6
  is the one fixed by gauge invariance, and the only one that works.
* **Posterior is local.** It explores two branch classes found by multistart; other classes may exist. The earlier
  boundary-pinned fits (Im τ_d ≥ 0.03, |ε_d| ≤ 0.03) give 0.034 and 0.017, but miss V_us by about 5σ.
* **Scale.** The comparison uses M_Z ratios. y_b/y_τ ≈ 1.2 is a statement about the Yukawa matrices and needs running
  before it can be compared with b–τ unification.
* **Prior art.** That hypercharge flux splits lepton from down Yukawas in F-theory local models is known qualitatively
  (Aparicio–Font–Ibáñez–Marchesano 2011; Font–Ibáñez–Marchesano–Regalado 2013). The new step is the theta-null
  realisation with the charge rule z_e = 6·z_d tied to the CKM fit.
