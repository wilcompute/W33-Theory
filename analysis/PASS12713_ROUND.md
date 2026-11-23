# Pass 12713: no missing-partner splitting through a 24, 75 or 200 leaves exactly Q + u^c light (correcting Pass 12712); a realistic Belle II reach tests only 17–83% of B′; ternary weights sit on the energy–accuracy front at 48 pJ per weight; balanced ternary cuts the longest carry chain 3.5×; an FCC y′ fixes the dark-dimension size to a factor ~2–3

Claude track. **Not a theory of everything.**
- Script: `explore_pass12713_round.py` (≈5 s).
- Certificate: `data/explore_pass12713_round.json`.
- Tests: `tests/test_toe_pass12713.py`, 5 tests passing.

**Correction to Pass 12712.** That pass said the generalised missing-partner mechanism (2308.11705) keeps Q + U light. It does the reverse.
- Its partner, the 40, contains Q and U partners but no e^c partner.
- So **e^c-type states stay light** and the coloured components are heavy (at about 10¹⁶ GeV).

## (2) The missing-partner no-go for a light Q + u^c (computed)
- **Method:** a Freudenthal weight-multiplicity engine for Aₙ, checked against the Weyl dimension formula, decomposes Φ ⊗ 10 into SU(5) irreps. Each irrep is then branched to the SM. The 10 itself comes out as Q + u^c + e^c with the correct hypercharges, as a check.
- **Rule:** a partner irrep R gives mass to exactly the components of the 10 that it contains.

| Φ | R ⊂ Φ ⊗ 10 | partner contains | light from the 10 |
|---|---|---|---|
| 24 | 10, 175 | Q, U, E | none |
| 24 | **40** | Q, U | **e^c** (the GMPM) |
| 24 | 15 | Q | u^c, e^c |
| 75 | 10, 175, 315 | Q, U, E | none |
| 75 | 40, 210 | Q, U | e^c |
| 200 (from Φ²/M) | 175, 1215 | Q, U, E | none |
| 200 | 450 | Q, U | e^c |
| 200 | 160 | Q | u^c, e^c |

Dimension totals check: 240, 750 and 2000.

- **Result:** in every case, any partner containing an e^c partner also contains partners for both Q and U. **No partner, and no combination of partners, leaves exactly Q + u^c light.** Combining partners can only add massive components.
- **Consequence for the hybrid:** its light Q + U cannot come from a missing-partner mechanism with the SU(5) adjoints 24 or 75, nor with the 200 that a Φ²/M term would supply. The remaining options are:
  - a pseudo-Goldstone mechanism;
  - a symmetry outside SU(5), for example SU(6) or SU(3)³ ⊂ E₆;
  - the tuning of Pass 12705, at a cost of about 10⁻²⁷ in the evidence.
- **The hybrid's best-case evidence of Pass 12710 (0.1–0.75) now needs a mechanism no one has exhibited.**

## (3) Belle II vs B′, with the exclusive fraction (corrects Pass 12712's "100%")
Searches target exclusive two-body modes (ψΛ, ψp, …). The fraction f of B′'s required inclusive rate that lands in them was taken log-uniform in [1%, 10%].

| exclusive reach | fraction of B′ tested |
|---|---|
| 10⁻⁷ | **17%** |
| 10⁻⁸ | 83% |
| 10⁻⁹ | 100% |

- The median exclusive BR B′ needs is 3×10⁻⁸.
- **Fully excluding B′ needs about 10⁻⁹ exclusive sensitivity**, or an inclusive B → baryon + missing-energy search.

## (1) End-to-end inference energy (Horowitz 45 nm numbers)

| weights | bits | memory-bound (DRAM), pJ/weight | on-chip (SRAM), pJ/weight | accuracy (Pass 12712 task) |
|---|---|---|---|---|
| fp32 | 32 | 965 | 9.7 | 0.562 |
| int8 | 8 | 240 | 1.5 | ≈0.562 (assumed) |
| 2-bit | 2 | 60 | 0.40 | 0.552 |
| **ternary** | **1.6** (5 trits per byte, 99.1% packing efficiency) | **48** | **0.27** | **0.538** |
| binary | 1 | 30 | 0.19 | 0.523 |

- **Pareto front:** binary → ternary → 2-bit → int8, with ternary on the front.
- **Why ternary is cheap:** in memory-bound inference (batch-1 decoding) energy is set by the bits moved, so ternary is 5× cheaper than int8 and 20× cheaper than fp32. Its 44% zeros help only the arithmetic.

## (4) Balanced ternary vs binary carries (same numeric range)

| range | digits | longest carry chain (mean), binary / balanced ternary | P(carry) per digit |
|---|---|---|---|
| 16-bit | 11 trits | 5.2 / 1.7 | 0.47 / 0.25 |
| 32-bit | 21 trits | 7.5 / 2.2 | 0.49 / 0.25 |
| 64-bit | 41 trits | 9.8 / **2.8** | 0.49 / 0.25 |

- **Carries are much rarer.** A balanced-ternary carry happens with probability 1/4 per digit, against nearly 1/2 in binary. The longest chain is 3.5× shorter.
- **Two effects compound:** there are 1.58× fewer digits, and carries are generated half as often.
- **Implication:** a ripple-carry ternary adder's typical delay is much shorter. Whether the slower multi-level gates eat that gain depends on the technology (see Pass 12712's 2.5× energy penalty).

## (5) Inverting an FCC y′ into the size of the dark dimension
- **Flat dimension:** dy′/d ln R ≈ 0.0053–0.0059.
  - With σ(y′) = 0.005 ⊕ 0.0036 (parametric), FCC measures **R to a factor of 2.8–3.2**.
  - With σ_meas = 0.002 it improves to a factor of 2.0–2.2.
  - Equivalently, M₅ ∝ R^{−1/3} to a factor of about 1.4.
- **Warped dimension (UV brane, m_KK = 1 eV):** dy′/dkL ≈ −0.004 to −0.008, so σ(kL) ≈ 0.8–1.7.
- **Interpretation:** a single collider measurement of a Yukawa coupling would size an extra dimension to within a factor of 3, provided B′ is the right model and the dimension is flat.

## Status
- **Hybrid:** has no known mechanism for exactly-light Q + U. Missing-partner via 24, 75 or 200 is excluded here.
- **B′:** a Belle II search at 10⁻⁸–10⁻⁹ in exclusive modes, or an inclusive search, is needed to settle it. FCC would size its dimension to a factor of about 3.
- **Ternary:**
  - wins in memory-bound neural-network inference (ternary weights on the energy–accuracy front);
  - wins in links (PAM3);
  - wins in carry statistics;
  - loses in logic energy per bit.
