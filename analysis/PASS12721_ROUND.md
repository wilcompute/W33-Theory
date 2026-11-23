# Pass 12721: the hybrid's uncoupled accidental symmetry leaves Q + U plus a complete vectorlike 5 + 5̄ (Higgs doublets + triplets) that still unifies (δ = +0.25); a second 45′ instead leaves an X-like (3,2)₅/₆ that wrecks unification; ternary language models sit between binary and 2-bit at small scale; trapped-ion qudits fail the 1.26 break-even; Casimir quintessence needs 2×10⁻⁸ tuning at R ≤ 0.2 μm

Claude track. **Not a theory of everything.**
- Scripts: `explore_pass12721_misc.py` and `explore_pass12721_charlm.py` (≈40 min).
- Certificates: `data/explore_pass12721_*.json`.
- Tests: `tests/test_toe_pass12721.py`, 4 tests passing.
- Decision table: updated snapshot in `TOE_DECISION_TABLE.md`.

## (1) Higgs splitting: the Goldstone count decides
For decoupled sectors, uneaten = Σ(broken cosets) − gauge coset (SO(10) → SM, 33). This uses the group-theory engine of Pass 12716.

| case | uneaten | content | two-loop unification (light states at 1.74 TeV, hybrid M_SS = 10¹⁰) |
|---|---|---|---|
| (a) Σ(LR) + H(SU(5)) (Pass 12716) | 18 | Q + U | δ = +0.26, M₁₂ = 4.1×10¹⁶ |
| (b) Σ(LR) + a coupled (Σ′, H) sector breaking to the SM (a second 45′ to split the Higgs) | 30 | Q + U + **(3,2)₅/₆** + c.c. | **δ = −2.15, M₁₂ = 1.3×10¹³: fails** |
| (c) Σ(LR) + H with accidental U(16), uncoupled (Pass 12720, ε = 0) | 28 | Q + U + (1,2)_{±1/2} + (3,1)_{±1/3} | **δ = +0.25, M₁₂ = 5.3×10¹⁶: unifies** |

**Results:**
- **A second 45′ that lifts the H-sector triplets fails.** Its sector eats all 33 gauge Goldstones, so all 30 of Σ's broken directions stay light, including the X-like (3,2)₅/₆ pair.
- **The uncoupled case (c) is viable for unification.** The extra light states are one Higgs doublet pair plus a d^c-type triplet pair, a **complete vectorlike 5 + 5̄** of SU(5), which shifts all three couplings equally.
- **This reverses the framing of Pass 12720.** The coupling that lifts the triplets is not needed for unification. The doublet–triplet problem becomes a **TeV-triplet problem:**
  - **Proton decay:** a 1.74 TeV triplet requires |y_qq·y_ql| ≲ 1.7×10⁻²⁵ for τ_p > 2.4×10³⁴ yr (Γ ≈ |y_qq y_ql|²·0.01·m_p⁵/(8π M_T⁴)). A symmetry, for example the Z₁₀ of Passes 12718–12719 extended, must forbid either the diquark or the leptoquark coupling.
  - **Decay:** the triplets must decay before BBN (as for Q + U, Pass 12719 item 3).
  - **A new collider signal:** a TeV vectorlike d-type quark (3,1)_{−1/3} next to Q + U.
- **Higgs:** the light doublet pair contains the SM Higgs. Its ~TeV mass needs the usual electroweak tuning for one light combination.

## (2) A ternary character-level language model on this repository's text
- **Corpus:** 121,281 characters of PASS127xx reports, vocabulary 193, unigram entropy 5.34 bits/char.
- **Model:** a 2-layer causal transformer, d = 48, context 32, 3000 Adam steps. The ternary run uses the annealed-threshold curriculum of Pass 12720.

| weights | validation bits/char | zero weights |
|---|---|---|
| fp32 | **2.97** | 0% |
| 2-bit | 3.25 | 0% |
| ternary (curriculum) | 3.42 | 45% |
| binary | 3.63 | 0% |

- **On real text, at this tiny scale, ternary closes 31% of the binary-to-fp32 gap** (3.63 → 2.97). It sits between binary and 2-bit, not at full precision.
- **This is consistent with BitNet b1.58,** whose parity with fp16 appears at multi-billion-parameter scale. Toy recall tasks (Passes 12717–12720) overstate ternary parity.

## (3) Trapped-ion qudits vs the break-even f < √log₂3 = 1.26 (Pass 12720)

| gates | qutrit error | qubit error | f | verdict |
|---|---|---|---|---|
| single-qudit (Innsbruck Clifford RB, 2109.06903) | 2×10⁻³ | ~10⁻⁴ | 20 | fails |
| two-qudit (Yb⁺ string, 92.7%, 2402.03121) | 7.3×10⁻² | ~10⁻³ | 73 | fails |

**Neither transmons (f = 4.5–9) nor ions (f = 20–73) are close to qutrit break-even today.**

## (4) Casimir quintessence at R ≤ 0.2 μm
- **The scaling problem:** the radion-Casimir dark energy of arXiv:2603.19819 uses R₀ = 16.4 μm. Since ρ_Casimir ∝ R⁻⁴, moving to the R ≤ 0.2 μm required by arXiv:2610.01825 overshoots ρ_DE by 4.5×10⁷.
- **The cost:** the Casimir coefficient would have to be tuned (or boson–fermion cancelled) to 2×10⁻⁸.
- **Consequence:** this quintessence model and the post-2610.01825 dark dimension are incompatible without a fine-tuning comparable to the one the dark dimension was meant to explain.

## Status
- **Hybrid:** the most economical version is now Q + U + a light vectorlike 5 + 5̄, all pseudo-Goldstones of the uncoupled accidental symmetry. It unifies. The open problems are a coupling-selection symmetry for the TeV triplets and their decay.
- **B′:** the dark dimension must be static, and Casimir quintessence doesn't fit it.
- **Ternary:**
  - full precision on toy attention tasks with curriculum training;
  - between binary and 2-bit for small language models;
  - qutrit hardware far from break-even.
