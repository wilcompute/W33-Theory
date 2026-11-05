# Passes 12616–12620: complete multiplets, brane terms, E/N, brane instantons, posterior predictive

Claude track. Continues `PASS12613_12615_ORBIFOLD_ROUTE.md` and `PASS12593_12602_SINGLE_ACTION_TESTS.md`. Producer: `analysis/w33_pass12616_to_12620_five_items.py`. Test: `tests/test_w33_pass12616_to_12620.py`.

**Not a theory of everything.** One retraction (12620), one new candidate (12616).

## 12616: trinification gives complete multiplets

`pq_complete_multiplets.py`, `trin_gates.py`. In SU(3)³, (3,3̄,1) = (3,2,⅙) + (3,1,−⅓). In flipped SU(5), a vectorlike 10 + 10̄ gives the same plus a singlet. So pairs of these are complete multiplets, with no splitting problem. My Pass 12605 scan stopped at three coloured multiplets and never tested them. Two-loop, all three couplings meeting:

| Vectorlike (3,3̄,1) | M_X (GeV) | M_U (GeV) | 1/α_U | τ (yr) | E/N with N_DW = 1 |
|---:|---:|---:|---:|---:|---|
| 1 | no solution | | | | |
| 2 | 8.2×10⁸ | 3.6×10¹⁶ | 34.6 | 2.7×10³⁸ | none |
| **3** | **2.9×10¹¹** | **3.5×10¹⁶** | 34.6 | **2.4×10³⁸** | **8/3** or −4/3 |

**Three copies:** proton safe by four orders, beyond Hyper-K, so that falsifier is lost. With N_DW = 1 and E/N = 8/3, the coupling sits on the GUT line of arXiv:2511.21830, so the orbifold axion tension of 12615 does not apply.

σ stability with 27 colour components (common y) holds only for f ≳ 7×10¹² GeV, so **m_a ≲ 0.8 μeV**, y_Q ≈ 0.03, and the axion is pre-inflationary. Current haloscopes do not reach below a few μeV. I recall lumped-element searches aiming at DFSZ there, without having checked their reach. Gaps: the trinification GUT itself, its Higgs sector, and why three copies, are not built. In flipped SU(5), α₂ = α₃ alone meets at about 3×10¹⁶ GeV for any threshold.

## 12617: the orbifold at two loops, with brane terms

`orbifold_twoloop.py`. Two loops below 1/R, KK towers at one loop above. **Control:** ΛR = 1 reproduces the 4D two-loop result to all printed digits.

| ΛR | M_X (GeV) | 1/R (GeV) | τ, matter on the SU(5) brane |
|---:|---:|---:|---:|
| 1 | 2.7×10¹⁰ | 4.0×10¹⁵ | 3.5×10³⁴ |
| 3 | 1.3×10¹⁰ | 2.6×10¹⁵ | 6.0×10³³ |
| 10 | 6.3×10⁹ | 1.6×10¹⁵ | 6.3×10³² |

**So matter must sit on the SM brane**, where tree-level X exchange is absent. The Hyper-K prediction of 12610 then becomes loop-suppressed and is lost for the orbifold version.

Brane kinetic terms: d ln M_X/dδ = (1.5, −2.7, 1.2) per unit of non-universal δ_i. With random non-universal terms of ±0.5, ±1, ±2, ±4, M_X stays in 10⁹ to 2×10¹¹ in 100, 82, 45 and 25 percent of draws. The orbifold numbers are order-of-magnitude unless brane terms are known.

## 12618: E/N separates the embeddings

`en_discriminator.py`. **Controls:** a single (3,1,−⅓) gives ⅔ and a single (3,1,⅔) gives 8/3, by E/N = 6Y². The search tool's summary in Pass 12603 had these swapped, and the formula settles it. A complete SU(5) 5 or 10 gives 8/3.

| Measured E/N | g/g_KSVZ | Relative to the GUT line | Points to |
|---|---:|---|---|
| ⅔ | 0.65 | above | Model A, N_DW = 1: 4D with tuned splitting |
| 22/15 | 0.24 | below | Model A, N_DW = 5: pre-inflation, compatible with the orbifold |
| 8/3 | 0.39 | on | trinification, complete SU(5) |
| −4/3 | 1.69 | above | trinification, other charge choice |

So Model A with all-positive charges escapes the orbifold bound, at the cost of N_DW = 5.

## 12619: brane instantons, an argument only

Pass 12615 estimated the needed suppression as K e^(−S) ≲ 10⁻⁷⁷ and guessed K ~ 10⁻⁴⁸ from Yukawa closure. **That guess ignored B+L.** In the SM the electroweak θ is unphysical, because the anomalous B+L rotates it away. A single SU(2) instanton's 't Hooft vertex, QQQL per generation, cannot close into a vacuum diagram without a further source of B+L violation, such as the seesaw's lepton-number violation, which adds suppression by small Majorana-related factors. So electroweak brane instantons likely give a far smaller axion potential than 12615 assumed. U(1)_Y effects need a UV completion (monopole loops) and were not assessed. **[I]**: not computed, and it weakens the 12615 tension without removing it. Agrawal et al treat chiral suppression from added brane fermions; this B+L argument is mine and unchecked against their section 5.

## 12620: posterior-predictive cross-validation, and a retraction

`class_ppd.py`. Each model's training posterior (Fisher at the lowest-training-χ² fit from Pass 12597, held probe masked) sampled with 24 draws. Score: elpd = ln⟨e^(−χ²_held/2)⟩. Dovekie.

| Model | elpd, SN held | elpd, BAO held | Total |
|---|---:|---:|---:|
| ΛCDM | −817.59 | −11.47 | −829.07 |
| CPL | −816.70 | −6.88 | −823.58 |
| fading, Fisher posterior | −815.65 | −7.37 | −823.02 |
| fading, c and c′ block ×2 | −816.59 | −11.15 | −827.74 |

**Retraction.** Pass 12597 said fading beats CPL by 7.4 to 22.6 in χ². That compared best-fit points. CPL trained without SN has a broad posterior whose better draws predict SN well (16th percentile χ² 1631.1), so the posterior predictive is a **tie**: 0.56 in elpd, well within the noise of 24 draws. Both evolving models beat ΛCDM out of sample by about 5.5 to 6 in elpd with the Fisher posterior. Fading's lead falls to 1.3 with its c, c′ block widened, and in that variant 10 of 24 BAO draws failed in CLASS, so it is less reliable. The exponential comparator was still running at this writing.

Limits: Gaussian posteriors; 24 draws, with elpd dominated by the best draws; two folds; Dovekie only; not blind.

## Parallel work

Parallel `6fdfcfefb` independently gave the two-loop single-Q threshold, 2.1189×10⁷ against 2.1220×10⁷ here. No newer parallel commits at this writing.

## Sources

arXiv:2511.21830, 1705.05370, hep-ph/9902423, hep-ph/0103125, 1307.3536. Trinification decomposition: standard; not re-read.
