# Pass 12720: unifying pseudo-Goldstone Higgs and Q + U fails in minimal form (the H̄Σ²H coupling that lifts the triplets lifts everything); a curriculum makes ternary transformers match full precision on the hard seed with 45% zeros; the SM vacuum is 2.7–4.5σ from absolute stability; qutrit codes on today's transmons are 12–49× worse per encoded bit

Claude track. **Not a theory of everything.**
- Scripts:
  - `explore_pass12720_unified.py` (≈23 min; explicit 16 spinor);
  - `explore_pass12720_curriculum.py` (≈20 min);
  - `explore_pass12720_misc.py`.
- Certificates: `data/explore_pass12720_*.json`.
- Tests: `tests/test_toe_pass12720.py`, 4 tests passing.

## (1) One pseudo-Goldstone mechanism for Higgs doublets and Q + U?
**Setup:**
- The 16 is built from the so(10) Clifford algebra: 32×32 gamma matrices, a chirality projection, and a homomorphism check. The ν^c direction is the SU(5) singlet, with B−L-generator eigenvalue +1.5i.
- Superpotential: W = (m/2)tr Σ² + (λ/4M)tr Σ⁴ + Y(H̄·H − v²) + ε·H̄S(Σ)²H.
- The vacuum (Σ along B−L, H = H̄ along ν^c) is solved numerically. Eaten modes are identified as the complexified gauge orbit; the uneaten massless modes are classified by hypercharge and SU(3)/SU(2) Casimirs on the quotient space.

| ε | \|∂W\| | zero modes | eaten | uneaten massless | content |
|---|---|---|---|---|---|
| 0 | 2×10⁻²² | 61 | 33 | **28** | (3,2)_{±1/6} ×6 each, (3̄,1)_{∓2/3} ×3 each = **Q + U**; (1,2)_{±1/2} ×2 each = **one Higgs doublet pair**; (3,1)_{±1/3} ×3 each = d^c-type triplets |
| 0.05 | 10⁻⁶ (not converged) | 33 | 36 | 18 | unreliable (an induced V_R component; classification fails) |
| **0.2** | 10⁻⁹ | 33 | 33 | **0** | everything lifted |

**What this establishes:**
- **At ε = 0 the accidental SO(10)₄₅ × U(16) (Σ sector 30 + U(16)/U(15) 31 − gauge 33) gives exactly Q + U + one doublet pair + one pair of d^c-type triplets.** This is computed, and it confirms the combined counting proposed in Pass 12719.
- **The Tavartkiladze-type coupling H̄Σ²H lifts all of them,** Q + U and the doublets included. It breaks the product symmetry to the diagonal, so nothing stays protected.
- **Why Tavartkiladze's doublets stay light (1803.11164):** he adds 45-sector terms ((tr Σ²)³, tr Σ² tr Σ⁴, tr Σ⁶) that suppress the induced V_R. Even so, the explicit H̄–Σ coupling cannot keep the Σ-sector Goldstones (our Q + U) light.
- **Consequence:** light Q + U (protected by SO(10)₄₅) and pseudo-Goldstone Higgs doublets (protected by U(16) once it is broken through Σ) **are not produced together by the minimal coupling.** Doublet–triplet splitting remains the hybrid's open problem.
- **Remaining routes:**
  - a coupling that breaks U(16) without touching SO(10)₄₅, for example through a second 45′;
  - missing-VEV splitting with a field content that avoids the Pass 12719 no-go.

## (4) A curriculum for ternary transformers (8-pair recall, the hard seed of Pass 12719)

| schedule | seed 0 | seed 1 (hard) | zero weights |
|---|---|---|---|
| plain ternary (Pass 12719) | 1.000 | 0.225 (stuck) | 45% |
| **warm start: 2-bit for 2000 steps, then ternary** | **1.000** | **1.000** | 44% |
| **annealed threshold, 0 → 0.7 over 3000 steps** | **1.000** | **1.000** | 45% |

**With either curriculum, ternary transformers escape the induction plateau and match full precision while keeping 44–45% of weights exactly zero.** The plateau is an optimisation problem, not a capacity limit of {−1, 0, +1}.

## (2) Vacuum stability with the newest inputs
Inputs: M_t = 172.80 ± 0.26 (arXiv:2603.28865), M_t^c from Pass 12709.

| α_s | scheme uncertainty | distance from stability | P(absolutely stable) |
|---|---|---|---|
| 0.1180(9) | 0 / 0.25 / 0.5 GeV | 4.2 / 3.6 / 2.7σ | 2×10⁻⁵ / 1.5×10⁻⁴ / 3×10⁻³ |
| 0.1183(7) (FLAG) | 0 / 0.25 / 0.5 GeV | 4.5 / 3.8 / 2.7σ | 3×10⁻⁶ / 9×10⁻⁵ / 3×10⁻³ |

- **The SM vacuum is metastable at 2.7–4.5σ.** The top-mass scheme uncertainty is now the only thing keeping stability at the 10⁻³ level.
- **FCC-ee:** CERN Council named it the preferred flagship on 22 May 2026, with a final decision in 2028. Its run plan (Z 4 yr, WW 2, ZH 3, then tt̄ 5) puts the threshold scan that would settle the question about 9 years after the start.

## (3) The dark-dimension DESI papers and Newton's constant
- **Bedroya–Obied–Vafa–Wu** (PRD 114, 103506, 2026):
  - The radius varies: it expands in matter domination and shrinks recently.
  - They acknowledge "observational bounds on the variations of Newton's constant" and consider either fixed total internal volume (G constant) or a partial volume change (G varying).
  - SM brane moduli are frozen.
- **Pass 12719's lunar-ranging bound** (|1 + w₀| ≲ 0.004 for a radion-driven, G-varying case) therefore applies to their varying-G branch. Their fixed-volume branch evades it.
- **Casimir quintessence (2603.19819):** the radion is the quintessence field, with R₀ = 16.4 μm. They discuss fifth-force bounds but not Ġ/G. The R₀ value is also in tension with the R ≲ 0.2 μm bound of 2610.01825 (Pass 12707).

## (5) Qutrit codes with measured hardware errors
**Data:** the best two-qutrit transmon gate is 97.3% (Goss et al. 2022), i.e. 2.7% error, against two-qubit errors of 0.3–0.6% (f = 4.5–9).

**Result for perfect [[5,1,3]] codes:** qutrits are **12–49× worse** in failure per encoded bit.

**Break-even criterion (new, simple):** failure ∝ (f·p)² and information ∝ log₂d, so a qutrit code beats a qubit code only if **f < √log₂3 = 1.26**. Today's transmons are far from that. "3 is closest to e" needs qutrit gates within 26% of qubit error rates.

## Status
- **Hybrid:**
  - Light Q + U is established (Passes 12714–12718).
  - Unification with pseudo-Goldstone doublets via H̄Σ²H fails. Doublet–triplet splitting stays open.
- **SM vacuum:** metastable at 2.7–4.5σ.
- **Ternary:**
  - transformers reach full precision with curriculum training and 45% zeros;
  - qutrit hardware needs gate errors within 1.26× of qubits.
