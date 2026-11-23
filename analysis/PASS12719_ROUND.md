# Pass 12719: the toponium-corrected top mass (172.80) lowers μ₀ to 2.5×10¹⁰ and makes absolute stability ~10⁻³; a DESI-rate rolling dark-dimension radius violates lunar laser ranging by 38×; Dimopoulos–Wilczek doublet–triplet splitting conflicts with Goldstone quality (a no-go for every Z_N); gauge mediation keeps the hybrid's y′ sharp; ternary transformers are as fragile as binary on hard seeds

Claude track. **Not a theory of everything.**
- Scripts:
  - `explore_pass12719_round.py` (items 2–5);
  - `explore_pass12719_transformer.py` (item 1, ≈25 min);
  - `explore_pass12719_web.py` (internet-driven items 6–7).
- Certificates: `data/explore_pass12719_*.json`.
- Tests: `tests/test_toe_pass12719.py`, 7 tests passing.

## Internet-driven results
**(6) A new top-mass input.** Ball et al. ([arXiv:2603.28865](https://arxiv.org/pdf/2603.28865), March 2026) give M_t(pole) = 172.80 ± 0.26 GeV from a global fit with toponium corrections. The PDG average is 172.4 ± 0.7.

| M_t (σ) | μ₀ (GeV) | P(absolutely stable) | y′_B′ (R = 0.088 μm) | y′_hybrid (c = 1) |
|---|---|---|---|---|
| 172.57 (0.58, incl. scheme) | 5.4×10¹⁰ | 5×10⁻³ | 0.505 | 0.472 |
| **172.80 (0.56)** | **2.5×10¹⁰** | **1×10⁻³** | **0.496** | **0.460** |
| 172.80 (0.26, experimental only) | 2.5×10¹⁰ | 10⁻⁸ | 0.496 | 0.460 |

- Both predictions shift down by about 0.01, and the B′–hybrid gap (0.035) is unchanged.
- The hybrid's SUSY scale (8.4×10⁹ GeV) still lies below μ₀.
- **The quartic zero moves to 2.5×10¹⁰ GeV.**

**(7) DESI DR2 vs a rolling dark-dimension radius.**
- **Data:** DESI DR2 with the CMB prefers evolving dark energy at about 3σ (w₀ ≈ −0.84; [2508.10514](https://arxiv.org/pdf/2508.10514)).
- **Existing dark-dimension responses:** Casimir radion quintessence ([2603.19819](https://arxiv.org/pdf/2603.19819)), Bedroya–Obied–Vafa–Wu (PRD 2026: the radius varies), and modular quintessence ([2507.03090](https://arxiv.org/pdf/2507.03090)).
- **New check:**
  - **Assumptions:** suppose ρ_DE ∝ R⁻⁴ (Λ^{1/4} = λ·m_KK), the SM lives on a brane, and m_p is fixed in 5D units.
  - **Consequence:** G·m_p² ∝ 1/R and |d ln G/dt| = (3/4)|1 + w₀|H₀.

| w₀ | \|Ġ/G\| (yr⁻¹) | ÷ lunar-ranging 2σ bound (Ġ/G = (7.1 ± 7.6)×10⁻¹⁴ yr⁻¹, Hofmann–Müller 2018) |
|---|---|---|
| −0.84 | 8.6×10⁻¹² | **38×** |
| −0.95 | 2.7×10⁻¹² | 12× |
| −0.99 | 5.4×10⁻¹³ | 2.4× |
| −0.999 | 5.4×10⁻¹⁴ | 0.2× |

- **A radion-driven DESI signal is excluded by lunar laser ranging** unless |1 + w₀| ≲ 0.004.
- **For B′:** its dark dimension must be stabilised today. DESI-like evolution would have to come from another field, such as the string-coupling modulus of Anchordoqui et al., or the SM masses would have to track M₅.
- **A check worth putting to the authors of the varying-radius papers.**

**Novelty check for the pseudo-Goldstone Q + U.**
- **Closest prior art:** Tavartkiladze, PRD 98, 015013 ([1803.11164](https://arxiv.org/html/1803.11164)). It uses the same B−L-oriented 45 with a U(16)-symmetric 16 + 16̄ sector and an anomalous U(1)_A × Z₄^R to make **the Higgs doublets** pseudo-Goldstones. All coloured states there are heavy.
- **Applying the mechanism to vectorlike Q + U (Passes 12714–12718) was not found in the literature searched.** It should cite 1803.11164 as the template.

## (4) Doublet–triplet splitting: a new no-go, and the way out
- **Theorem (every Z_N):** if Σ², 10′10′ and the DW coupling 10·Σ·10′ are all allowed, then 2q₁₀ ≡ 0. That makes 10·10 allowed, i.e. a GUT-scale μ-term. Zero assignments survive.
- **A singlet does not rescue it.** Giving the 10′ its mass from a singlet X (10′X10′, W = Z(X⁵ − v)) also yields zero assignments. ⟨X⟩ carries a nonzero Z₅-charge, which reintroduces operators X^e·H̄ΣᵏH at dimension ≤ 7, destroying Goldstone quality.
- **Consequence:** the hybrid **cannot use Dimopoulos–Wilczek splitting together with discrete Goldstone protection** in minimal field content.
- **The way out:** Tavartkiladze's mechanism makes the doublets pseudo-Goldstones of the U(16) that W(H̄H) has automatically.
  - **Counting:** the combined count (Σ sector 30 + U(16)/U(15) 31 − gauge 33) leaves Q + U + doublets + d^c-type triplets.
  - **The open question:** whether a W^(45,16)-type coupling can lift the triplets while leaving Q + U and the doublets light, which would tie μ ~ M_VL.

## (2) A-terms by mediation

| mediation | X = A²/M_SS² | hybrid y′ (M_VL = 1.74 TeV) |
|---|---|---|
| gauge (M_mess = 10 M_SS; A/M ≈ 0.03) | 9×10⁻⁴ | **0.472** |
| gravity/anomaly, X = 0.5 / 1 / 3 / 6 | — | 0.465 / 0.459 / 0.443 / 0.435 |

**Gauge mediation keeps the hybrid sharp.** Gravity or anomaly mediation spreads it over 0.435–0.47.

## (3) Pseudo-Goldstone quark decays
- **Mixing:** m_mix = a(a/M_Pl)^{n−3} from the Z₁₀ decay operator of dimension n. Γ ≈ g²θ²M³/(32πm_W²).

| decay-operator dimension | θ | cτ | regime |
|---|---|---|---|
| 11 (the Pass 12718 example) | 0.15 | 3×10⁻¹⁸ m | prompt |
| 14 | 7×10⁻⁷ | 10⁻⁷ m | prompt |
| 15 | 10⁻⁸ | 0.4 mm | **displaced** |
| 16–18 | 2×10⁻¹⁰ – 6×10⁻¹⁴ | 1 m – 2×10⁷ m | R-hadron (detector-stable) |
| ≥ 19 | < 10⁻¹⁵ | — | BBN-excluded |

- The Z₁₀ dimension of the decay operator decides the LHC signature: prompt at 11–14, displaced at 15, R-hadrons at 16–18.
- **Same quantum numbers as B′'s top partners.** Q + U has the quantum numbers of B′'s Q + T, so the same limits apply: 1.74 TeV prompt, about 1.9 TeV long-lived. Only y′ and its M_VL dependence distinguish the two.

## (5) Qudit error-correction economy (perfect [[5,1,3]]_d codes, p = 10⁻³)
- **Level-independent errors:** qutrits have the same logical failure as qubits with 1.58× the information. Failure per encoded bit is 6.3×10⁻⁶ against 1.0×10⁻⁵. They also have the best information per unit control cost (0.106 against 0.100), the radix-economy optimum at d = 3.
- **Errors growing with the number of excited levels (f = d − 1, transmon-like):** qutrits are 2.5× worse per encoded bit.
- **Literature:** qutrit magic-state distillation has higher thresholds (Campbell–Anwar–Browne 2012).
- **Overall:** "3 is closest to e" carries over to quantum hardware only if leakage and decay do not grow with the level index.

## (1) A harder transformer test (8-pair recall, chance 1/16, d = 24, 4000 steps)

| weights | seed 0 | seed 1 | zero weights |
|---|---|---|---|
| fp32 | 1.000 | 1.000 (after a plateau to step ~3000) | 0% |
| binary | 0.997 | 0.229 (stuck) | 0% |
| ternary | 1.000 (0.99 already at step 1000, the fastest) | 0.225 (stuck) | 45% |
| 2-bit | 1.000 | 1.000 | 0% |

- **Ternary learns fastest when it learns.** On the hard seed it stays on the induction plateau, like binary; only 2-bit and fp32 escape it.
- **At this difficulty ternary's robustness equals binary's, not 2-bit's.** Two seeds is thin evidence.
- **Hardware context:** BitNet b1.58 silicon now exists. VitaLLM ([2605.00320](https://arxiv.org/html/2605.00320v1)) runs a 3B model at 72 tokens/s in 0.214 mm² at 16 nm, and TENET ([2509.13765](https://arxiv.org/html/2509.13765v1)) uses the same 1.6-bit packing as Pass 12713.

## Status
- **Inputs:** the top mass moves up (172.80): μ₀ = 2.5×10¹⁰ and P(stable) ≈ 10⁻³. Both completions' y′ shift down by about 0.01, and their gap is unchanged.
- **B′:** its dimension must be static today, since DESI cannot be its radion.
- **Hybrid:**
  - doublet–triplet splitting is now its main open problem, with Dimopoulos–Wilczek excluded under discrete protection;
  - gauge mediation is preferred, since it keeps y′ sharp;
  - its collider signature (prompt, displaced or R-hadron) is set by the Z₁₀ dimension.
- **Ternary:** fastest learner but not more robust than binary in deeper transformers. Qutrits win only with level-independent noise.
