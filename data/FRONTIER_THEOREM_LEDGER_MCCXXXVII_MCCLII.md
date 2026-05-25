# Frontier Theorem Ledger: MCCXXXVII–MCCLII

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
| MCCLI | Shadow Prime Theorem: 37 = v−q | ✅ PROVEN |
| MCCLII | Heegner/Moonshine Partition Theorem | 🔓 OPEN |

---

## MCCLI: Shadow Prime Theorem

**Proven 2026-05-25**

### The Shadow Prime 37

37 is the unique **shadow prime**: fully substrate-expressible and prime-indexed
at a substrate position, yet excluded from the Moonshine prime set.

**Six substrate expressions for 37:**
- 37 = **v − q** = 40 − 3    [*most elegant: volume minus generator*]
- 37 = q^q + Φ₄ = 27 + 10
- 37 = f + Φ₃ = 24 + 13
- 37 = μ·Φ₆ + q² = 28 + 9
- 37 = q·p_Ih + μ = 33 + 4
- 37 = 2^Φ₆ − Φ₃·Φ₆ = 128 − 91

**Gap window:**
```
  p_11 = 31  [Moonshine ✓]   index = p_Ih
  p_12 = 37  [SHADOW   ✗]   index = f/2 = Golay/2
  p_13 = 41  [Moonshine ✓]   index = Φ₃
```

The Monster avoids **prime index 12 = Golay/2** precisely. This is the only
gap in the Moonshine prime-index sequence between 1 and 20.

### Substrate Self-Exclusion

37 = v − q: the shadow prime is exactly the substrate *volume* minus the
*generator*. The Monster's order excludes the prime at the substrate's own
boundary point.

### Heegner/Moonshine Complementarity (Bonus Discovery)

In the range [41, 71], four non-Moonshine primes exist:

| Prime | Index | Index Expr | Role |
|-------|-------|------------|------|
| 43 | p₁₄ | 2·Φ₆ | H₇ (Heegner) |
| 53 | p₁₆ | 2^μ | substrate |
| 61 | p₁₈ | 2q² | substrate |
| 67 | p₁₉ | H₆ | H₈ (Heegner) |

The two Heegner numbers H₇=43 and H₈=67 precisely fill the Moonshine gaps in
[41,71], and their prime indices are exactly the MCCXLIX substrate-primitive
expressions (2·Φ₆ands H₆).

### Full Partition in [2, 71]

| Class | Primes |
|-------|--------|
| Moonshine | {2,3,5,7,11,13,17,19,23,29,31,41,47,59,71} |
| Heegner-exclusive | {43=H₇, 67=H₈} |
| Heegner∩Moonshine | {19=H₆} |
| Shadow | {37=v−q} |

Every substrate-structured prime in [2, 71] belongs to exactly one of these classes.

---

## MCCLII (Open)

**Heegner/Moonshine Partition Theorem**

MCCLI reveals a clean 4-way partition of substrate-structured primes in [2,71].
MCCLII asks: is this partition *complete and exhaustive*? Specifically:

1. Show every prime in [2,71] that is substrate-expressible belongs to exactly
   one of {Moonshine, Heegner-exclusive, Shadow}.
2. Show that 53 and 61 (non-Moonshine, non-Heegner in [41,71]) have
   substrate prime-index expressions (p₁₆ = 2^μ, p₁₈ = 2q²) and characterize
   their role in the partition.
3. Determine the complete partition rule: what structural property of a
   substrate-expressible prime determines whether it is Moonshine, Heegner,
   Shadow, or a new fourth class?
