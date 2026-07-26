# bt1902 — Experimental Runbook: W(3,3) Substrate Discriminator

**Pre-registration ID:** bt1902  
**Depends on:** bt1901 (CF numerics), Pass 72 (defect locus D₁–D₄)  
**Target submission:** Q4 2026  
**Version:** 0.1 (draft for internal review)

---

## Abstract

This runbook specifies a photonic experiment to discriminate between the
Gaussian substrate (W(2,2) over GF(4), predicting CF = 0) and the Eisenstein
substrate (W(3,3) over GF(3), predicting CF = 1/10) using a 40-ray Witting
SIC implementation in a qutrit photonic platform. The decision variable is the
Contextual Fraction CF measured on the 4 defect rays {D₁, D₂, D₃, D₄}
identified in Pass 72.

---

## 1. Physical Platform

### 1.1 Photon Source
- **Type:** Heralded single photon via spontaneous parametric down-conversion (SPDC)
- **Wavelength:** 1550 nm (telecom C-band)
- **Heralding efficiency target:** η > 0.85
- **Repetition rate:** 80 MHz

### 1.2 Qutrit Encoding
- **Degree of freedom:** Temporal mode (time-bin)
- **Basis states:** |early⟩, |middle⟩, |late⟩ with bin separation Δt = 2 ns
- **Implementation:** Franson interferometer with two nested unbalanced
  Mach-Zehnder interferometers (MZI₁, MZI₂)
- **Visibility target:** V > 0.95 per MZI arm

### 1.3 Qutrit Hadamard Gate
The qutrit Hadamard H₃ is implemented as:

    H₃ = (1/√3) × [[1, 1, 1], [1, ω, ω²], [1, ω², ω]]

where ω = exp(2πi/3), realized via electro-optic phase modulators (EOM)
driven at 500 MHz with RF phase control to ±0.5°.

### 1.4 Controlled-X Gate (CX)
The qutrit CX gate is realized by:
- Feed-forward EOM driven by the herald photon detection signal
- Latency budget: < 50 ns
- Fidelity target: F(CX) > 0.98

---

## 2. The 40-Ray Measurement Basis

### 2.1 Circuit Structure
Each of the 40 Witting rays is prepared as:

    |ψᵢ⟩ = (CX)^{aᵢ} · H₃ · (Phase)^{bᵢ} · |0⟩

where (aᵢ, bᵢ) ∈ {0,1,2}² indexes the 9 cosets of the Heisenberg-Weyl group
on the qutrit, with an additional Clifford correction Cᵢ ∈ PSp(4,3) selecting
the specific ray. The full lookup table is generated from the Appleby
coordinates (40 rows × 6 real parameters per ray).

### 2.2 Defect Ray Settings
The 4 defect rays require specific phase settings:

| Ray | aᵢ | bᵢ | Clifford Cᵢ | Expected CF contribution |
|-----|----|----|-------------|-------------------------|
| D₁  | 0  | 1  | C₀ (identity) | 1/4 of total CF |
| D₂  | 1  | 2  | C₄ (π/3 phase) | 1/4 of total CF |
| D₃  | 2  | 0  | C₈ (2π/3 phase) | 1/4 of total CF |
| D₄  | 2  | 1  | C₁₂ (π phase) | 1/4 of total CF |

### 2.3 Non-Defect Ray Settings
The remaining 36 rays use standard H₃ + CX settings with no special phase
correction. These provide the normalization baseline for CF = 0 under the
Gaussian hypothesis.

---

## 3. Measurement Protocol

### 3.1 Run Structure
- **Total shots per run:** N = 10,000
- **Shots per ray setting:** n = 250 (40 settings × 250 = 10,000)
- **Runs per session:** 10 independent runs
- **Total photons:** 100,000

### 3.2 KS Valuation Procedure
For each shot at ray setting i:
1. Record click pattern (which of 3 time bins fired)
2. Assign binary KS value v(ψᵢ) ∈ {0,1} via the majority-vote rule on the
   3-click correlator
3. Check consistency: for each isotropic triple (i,j,k) with ω(ψᵢ,ψⱼ) = 0,
   verify v(ψᵢ) + v(ψⱼ) + v(ψₖ) ≤ 1 (KS sum rule)

### 3.3 CF Computation
After N shots:

    CF_measured = (number of rays where KS rule violated) / 40

**Decision rule:**
- If CF_measured < 1/20 (i.e. < 2 rays): fail to reject Gaussian substrate
- If CF_measured ≥ 1/10 (i.e. ≥ 4 rays): reject Gaussian at p < 0.01
  (binomial test, n=250, p₀=0, one-sided)

---

## 4. Three Independent Witnesses

The experiment records three independent quantities, all derivable from the
defect locus. Agreement of all three is required for a positive result.

### 4.1 Trace-Choi Visibility

    V(F₃) = |Tr(χ_measured · χ_theory)| / ||χ_theory||_F

**W(3,3) prediction:** V = 1/√3 ≈ 0.5774  
**Gaussian prediction:** V = 1/√4 = 0.5000  
**Required precision:** ΔV < 0.02 (achievable at N = 10,000)

### 4.2 Witting KS Budget

    Budget_measured = (number of rays with consistent classical valuation) / 40

**W(3,3) prediction:** Budget = 36/40 = 0.900  
**Gaussian prediction:** Budget = 40/40 = 1.000  
**Decision threshold:** Budget < 0.950 → reject Gaussian

### 4.3 Key-Agreement Rate (QKD sub-protocol)
Using the 40-ray SIC as a QKD alphabet between Alice (preparer) and Bob
(measurer):

    R_key = (mutual information Alice–Bob) / (40 ray settings)

**W(3,3) prediction:** R_key = 13/40 = 0.325  
**Gaussian prediction:** R_key = 15/40 = 0.375  
**Required precision:** ΔR < 0.02

---

## 5. Falsification Conditions

The W(3,3) substrate hypothesis is **falsified** if ANY of the following hold
at the stated precision after 10 independent runs:

| Witness | Falsification condition |
|---|---|
| CF | CF_measured < 1/20 across all 10 runs |
| Visibility | V_measured > 0.55 (i.e. compatible with Gaussian) |
| KS Budget | Budget_measured = 1.000 ± 0.010 |
| Key rate | R_key > 0.360 |

If falsified, the construction reverts to the Gaussian doily substrate and the
entire physical interpretation of W(3,3) as the universe's incidence geometry
must be revised.

---

## 6. Statistical Power Analysis

For N = 10,000 total shots, binomial test on CF:
- **Null hypothesis:** CF = 0 (Gaussian)
- **Alternative:** CF = 1/10 (W(3,3))
- **Significance level:** α = 0.01
- **Power:** 1 − β = 0.999 at CF = 1/10
- **Minimum detectable CF:** CF_min = 0.03 at α = 0.05

The experiment is decisively powered at the predicted signal strength.

---

## 7. Timeline

| Milestone | Target date |
|---|---|
| Runbook finalized (v1.0) | 2026-08-15 |
| Lab hardware audit | 2026-09-01 |
| Pilot run (N=1000) | 2026-09-15 |
| Full pre-registration submission | 2026-10-01 |
| Data collection complete | 2026-11-30 |
| Analysis and paper draft | 2026-12-31 |

---

## 8. Cross-References

- bt1901: CF numerical pre-registration (`artifacts/bt1901_cf_preregistration.json`)
- Pass 71: K6 bijection (`analysis/2026-07-08_pass71_k6_bijection_proofs.md`)
- Pass 72: Defect locus (`analysis/2026-07-26_pass72_CF_defect_locus.md`)
- Paper §§9.6–9.7: Smooth spectral action limit (open)
- Paper Theorem 22.16: Cyclotomic Capstone (Lean stub pending)
