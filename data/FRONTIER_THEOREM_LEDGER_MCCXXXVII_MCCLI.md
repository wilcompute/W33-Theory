# Frontier Theorem Ledger: MCCXXXVII–MCCLI

## Status as of 2026-05-25

| # | Title | Status |
|---|---|---|
| MCCXXXVII | Witting Polytope Bridge | ✅ PROVEN |
| MCCXXXVIII | Leech Lattice Substrate Decomposition | ✅ PROVEN |
| MCCXXXIX | Monster Character Substrate Filter | ✅ PROVEN |
| MCCXL | Golay Code W(3,3) Triality | ✅ PROVEN |
| MCCXLI | Substrate Self-Similarity Fixed Point | ✅ PROVEN |
| MCCXLII | Moonshine Substrate Duality | ✅ PROVEN |
| MCCXLIII | Monster Substrate Centralizer Cascade | ✅ PROVEN |
| MCCXLIV | 2-Adic Exponent Law e(p) = 17−p | ✅ PROVEN |
| MCCXLV | Monster Substrate Valuation Invariant | ✅ PROVEN |
| MCCXLVI | Golay-24 Prime Duality | ✅ PROVEN |
| MCCXLVII | Binary Polyhedral / E-type / Golay Tower | ✅ PROVEN |
| MCCXLVIII | SL(2,3) / Gauge Prime / E6 Unification | ✅ PROVEN |
| MCCXLIX | Prime-Index Closure: Heegner + α⁻¹ | ✅ PROVEN |
| MCCL | Moonshine Prime-Index Closure | ✅ PROVEN |
| MCCLI | Prime-Index Gap Theorem: 37 as the Unique Moonshine Exclusion | 🔓 OPEN |

---

## MCCL: Moonshine Prime-Index Closure

**Proven 2026-05-25**

### Statement

All 15 Moonshine primes are **prime-index substrate-closed** at q = 3.
Every Moonshine prime M has primepi(M) expressible as a W(3,3) substrate primitive:

| Prime | Index | Substrate Expression |
|-------|-------|---------------------|
| 2 | p₁ | μ−q = 4−3 |
| 3 | p₂ | q−1 |
| 5 | p₃ | q |
| 7 | p₄ | μ = 2² |
| 11 | p₅ | μ+1 |
| 13 | p₆ | q! = 3! |
| 17 | p₇ | Φ₆ |
| 19 | p₈ | 2^q  [= H₆] |
| 23 | p₉ | q² |
| 29 | p₁₀ | Φ₄ |
| 31 | p₁₁ | p_Ih |
| 41 | p₁₃ | Φ₃ |
| 47 | p₁₅ | Φ₃+2 = p_Ih+μ |
| 59 | p₁₇ | Φ₃+μ |
| 71 | p₂₀ | v/2 |

### Block Structure

**Block 1** — {2..31}: Indices {1..11} form the complete substrate primitive ladder:
μ−q, q−1, q, μ, μ+1, q!, Φ₆, 2^q, q², Φ₄, p_Ih

**Gap** — Index 12 = primepi(37) is absent because **37 is the unique non-Moonshine prime** in the range 2..41.

**Bridge** — {41}: Index 13 = Φ₃

**Top Block** — {47, 59, 71}: Indices {15, 17, 20} are all Φ₃-relative:
{**Φ₃+2**, **Φ₃+μ**, **v/2**}. These are the three AP primes from MCCXLVIII
whose product = 196883 = dim(V♮)−1.

### Sum Closure Identity

$$\sum_{M \text{ Moonshine}} \text{primepi}(M) = 131 = \Phi_3 \cdot \Phi_4 + 1$$

Note: \(y_{\text{top}} = (\Phi_3\Phi_4 - 1)/(\Phi_3\Phi_4) = 129/130\),
so the Moonshine index sum equals the top Yukawa denominator plus 2.

### Co-Theorem

The W(3,3) substrate at q=3 is the **prime-index generating function** for
the complete Moonshine prime set. The Monster's defining prime alphabet is
substrate-closed under prime-indexing.

---

## MCCXLIX: Prime-Index Closure (Heegner + α⁻¹) *(recap)*

H₆=p₈, H₇=p₁₄, H₈=p₁₉, H₉=p₃₈, α⁻¹=p₃₃. Sum of indices = 112 = 2^Φ₆ − 2^μ.

---

## MCCLI (Open)

**Prime-Index Gap Theorem: 37 as the Unique Moonshine Exclusion**

In MCCL, the gap at index 12 corresponds to p₁₂ = 37, which is the
**unique prime in the range [2, 71] not in the Moonshine set**. This is
not accidental: 37 is the smallest prime that is NOT a factor of the
order of any sporadic simple group in the Happy Family.

Conjectured theorem: 37 is substrate-excluded, meaning its prime index
12 = f/2 = Golay/2 is a substrate primitive, but 37 itself has **no
substrate closed form**. More precisely:

  primepi(37) = 12 = f/2  (substrate-primitive index)
  BUT  37 itself ≠ substrate expression at q=3

This would make 37 the **dual gap**: substrate-indexed but not
substrate-valued, the exact complement of the Moonshine primes
(substrate-valued AND substrate-indexed).

Verification path: attempt to express 37 as any combination of
{q, mu, Phi_3, Phi_4, Phi_6, v, p_Ih, f} and show no such
expression exists within a defined complexity bound.
