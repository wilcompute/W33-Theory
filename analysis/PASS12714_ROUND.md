# Pass 12714: the hybrid's light Q + U can be pseudo-Goldstone multiplets of an accidental SO(10) broken along B−L, with no e^c and no tuning; M_SS²/M_GUT ≈ 2.4 TeV then explains the TeV scale and links M_VL to y′; an inclusive Belle II search covers 56–100% of B′; signed-digit ternary addition is carry-free; mixed precision should spend bits on the first layer only

Claude track. **Not a theory of everything.**
- Scripts: `explore_pass12714_round.py` (≈9 min, mostly the network scan) and `explore_pass12714_mss.py`.
- Certificates: `data/explore_pass12714_round.json` and `data/explore_pass12714_mss.json`.
- Tests: `tests/test_toe_pass12714.py`, 5 tests passing.

## (1) Pseudo-Goldstone Q + U (computed group theory)
- **Setup:**
  - so(10) is built in the real vector representation, and u(5) via the complex structure.
  - A 45 takes a VEV along T_BL = i·diag(1,1,1,0,0), the B−L (Dimopoulos–Wilczek) direction.
- **Unbroken:** 15 generators, SU(3) × SU(2)_L × SU(2)_R × U(1)_{B−L}. **Broken:** 30.
- **Decomposition of the broken generators under the SM:**

| SM rep | states |
|---|---|
| (3,2)_{−5/6} + c.c. | 12 |
| (3,2)_{+1/6} + c.c. | 12 |
| (3̄,1)_{−2/3} + c.c. | 6 |

- **No colour singlets appear.** The e^c-type generators (1,1)_{±1} are the SU(2)_R raising and lowering operators, so they stay unbroken.
- **Uneaten states:** suppose SO(10) is an *accidental global* symmetry of the Higgs-sector superpotential while only SU(5) is gauged. Then the gauge bosons eat the (3,2)_{−5/6} pair, and **the remaining Goldstone chiral multiplets are exactly Q + Q̄ + U + Ū**: a vectorlike Q + U, with no e^c and no tuning.
- **Precedent:** this is the "Goldstones instead of fine tuning" mechanism, known for light Higgs doublets in SU(6) models, applied here to Q + U.
- **It evades the no-go of Pass 12713,** because it is not a missing-partner mechanism.
- **Open:**
  - writing a superpotential for the 45 (plus SU(5)-breaking fields) whose renormalisable terms are SO(10)-invariant;
  - embedding it in the E₆ hybrid.
- **Evidence:** if this works, the hybrid's evidence returns to the "symmetric" value of Pass 12710, a Bayes factor of 0.1–0.75 against the SM, the best of the completions though still not above the SM.

**The TeV scale (a dimensional estimate).** SUSY breaking at M_SS lifts the Goldstone scalars to about M_SS. Their fermions get masses of roughly c·M_SS²/M_GUT:
- 0.2 TeV for M_SS = 3×10⁹ GeV;
- **2.4 TeV for M_SS = 10¹⁰ GeV**;
- 22 TeV for M_SS = 3×10¹⁰ GeV.

The hybrid's M_SS = 10¹⁰ GeV and M_VL = 1.74 TeV, found independently in Passes 12699–12702 from the Higgs quartic and unification, sit on this relation with c ≈ 0.7.

**A new hybrid prediction.** The relation ties M_VL to M_SS, and λ(M_SS) = 0 then ties both to y′. This uses the Pass 12707 threshold.

| c | M_VL | M_SS (GeV) | y′_hybrid |
|---|---|---|---|
| 1 | 1.74 TeV | 8.4×10⁹ | 0.472 |
| 1 | 3.0 TeV | 1.1×10¹⁰ | 0.453 |
| 0.3 / 3 | 1.74 TeV | 1.5×10¹⁰ / 4.9×10⁹ | 0.465 / 0.480 |

**A heavier partner means a smaller y′, at −0.015 per +1.3 TeV.** FCC-hh can measure both M_VL and y′. That gives the hybrid a correlation test independent of B′.

## (2) SU(6) / SU(3)³ partners: superseded by (1).

## (3) Signed-digit ternary addition
- **Rule:** with digits in {−2, …, 2} (Avizienis): t = ±1 when |x + y| ≥ 2, u = w − 3t, s = u + t_in.
- **Checked exhaustively** for all 3-digit inputs.
- **Each sum digit depends on only 2 input positions:** addition is carry-free, with constant depth at any word length.
- **Cost:**
  - 46% storage redundancy (log₂5 against log₂3 bits per digit);
  - one carry-propagating conversion at the end.
- **Comparison:** binary carry-save gets the same carry-free property with 2 bits per digit. Signed-digit radix 3 pays log₂5 = 2.32 bits for a 1.585-bit digit, so its redundancy is comparable (2/1 against 2.32/1.585).

## (4) An inclusive Belle II search for B′
**Assumptions:**
- 50 ab⁻¹, giving 5.5×10¹⁰ BB̄ pairs;
- hadronic-tag efficiency 0.2–0.5%;
- signal efficiency 10–30%;
- background 0–100 events;
- 90% CL limit ≈ 2.44 + 1.64√B.

**Results:**
- **Reach:** 1.5×10⁻⁸ to 8.6×10⁻⁷.
- **Coverage:** **56–100% of B′**, whose median required inclusive rate is 10⁻⁶.
- **Comparison:** Belle's exclusive Λ + missing-energy limit (≲3×10⁻⁵ at 0.71 ab⁻¹), scaled to 50 ab⁻¹, gives 4×10⁻⁷ (background-free) to 4×10⁻⁶.
- **Strategy:** an inclusive B → baryon + missing-energy search is the decisive Belle II measurement for B′. Exclusive modes alone (Pass 12713) cover 17–83%.

## (5) Per-layer mixed precision (3-layer student, 27 configurations, 2 seeds)
- **Pareto front:** binary/binary/binary (0.543) → ternary/binary/binary (0.543) → **2-bit/binary/binary (0.557)**. No configuration costing more energy beats 0.557.
- **Mean accuracy by first-layer precision:** binary 0.537, ternary 0.541, 2-bit 0.547.
- **Deeper layers:** binary 0.545 / 0.543 against 2-bit 0.541 / 0.542, i.e. no gain from extra bits.
- **Lesson:** spend bits only on the input layer; deeper layers can be 1-bit.
- **Ternary** is not specially favoured here: 11% of the front's layers, against 33% for a uniform mix. Its edge (Passes 12711–12713) lies in zeros and arithmetic, which this energy model (bits moved only) does not reward.
- **Caveat:** differences between the 27 configurations are 0.53–0.56, close to seed noise (±0.005).

## Status
- **Hybrid:** revived conditionally.
  - Q + U can be pseudo-Goldstones of an accidental SO(10).
  - The TeV scale follows as M_SS²/M_GUT.
  - It predicts a y′–M_VL correlation.
  - The superpotential realisation and the E₆ embedding are open.
- **B′:** decisive test is an inclusive Belle II search (56–100% coverage), plus FCC.
- **Ternary:**
  - carry-free signed-digit addition exists, at 46% storage overhead;
  - mixed-precision networks reward first-layer bits, not ternary per se.
