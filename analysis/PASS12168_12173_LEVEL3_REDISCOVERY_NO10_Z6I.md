# Passes 12168–12173: level-3 mass formulas (a rediscovery, cited), the untwisted no-10_H theorem, exact onsets, Z6-I with many Witten shifts

Claude track. Producer: `analysis/w33_pass12168_to_12173_level3_rediscovery_no10_z6i.py`. Drivers and frozen outputs:
`analysis/search_drivers_12168/`.

## Rediscovery notice (read first)

Passes **11115, 11136 and 11139** already established the following.

| pass | result |
|---|---|
| 11139 | the Wilson-line duality group is **Γ₀(3)**; the Fricke involution T → −1/(3T) is only approximate (0.34%, K-independent) |
| 11136 | the Witten-sector levels Δ = −½ + p_R²/2 in closed form, in three classes (below) |
| 11115 | an approximate Fricke duality in the levels; model 77's onset ≈ √3/2 |

The three 11136 classes:

| class | p_R² | tachyon domain |
|---|---|---|
| √3 | (b² + y²)/(√3y) | onset √3 |
| golden | (b² + y²)/(√3y) + 1/(3√3y) | top √3/2 + √(5/12) = 1.5115; disk at the Fricke point i/√3 |
| charged | (c² + y² + 1/12)/(√3y) + 1/3 | disk at the elliptic point (3 + i√3)/6, tangent to B = 0 at i/√3 |

**What this covers.** Passes 12140, 12149, 12152, part of 12158, and this round's mass formula re-derive these results
for S002, T115 and the crossed models. They are cited here, not claimed. In particular, S002's massless multiplet at
i/√3 (12149) is 11136's charged level at the tangency point. That rediscovery was caught late, by a grep for "Fricke",
and is now recorded in memory.

## What is new

### 12168: the formulas hold exactly on the e6+a2 route

- S002's lowest Witten level equals (√3y − 1)²/(6√3y), the 11136 charged form at B = 0. The match is 5·10⁻¹⁶ at 18
  axis points.
- T115's levels are Δ = y/(2√3) − ½, the 11136 √3 form. Its onset is exactly √3.

### 12169: why 11139's Fricke deviation is K-independent

The duality maps level **values** exactly but permutes **multiplicities** (272 ↔ 104 in S002, 12158). So it relates a
model to a partner, not to itself. The partner is not W → −W, W → 2W, a single-torus flip, or V1 → −V1 (12164).

### 12171: a third exact class

**p_R² = 2y/√3**, so Δ = y/√3 − ½, with onset √3/2. It covers model 77 and the crossed models A8SM_10006/16222, where
11115 had only "≈ √3/2".

With the 11107 enumerator at root ∓ 0.002, models 2 (√3), 10 (√3/2 + √(5/12)) and 77 (√3/2) are each tachyon-free just
above the root and tachyonic just below. The Δ values match −0.002 × (slope) exactly. **11107's certified radii 1.73,
1.512 and 0.87 are these exact numbers.**

### 12170: THEOREM — no untwisted 10_H

Checked on all 7 e6+a2 bases × all 864 A4-type second Wilson lines (6048 models):

- the untwisted first-E8 scalars form only SU(5) 5s and singlets;
- untwisted 10s occur only as fermions (288 per base: the generation 10s).

The 10 sits in the SO(10) 16, which is odd under the split parity. Twisted sectors remain a sample (0/185).

### 12172: Z6-I with eight Witten shifts per base

Pass 11100 used one shift per base. Here: 58 bases × 8 V0 = 464 shifts and 27,840 Wilson-line draws.

| result | count |
|---|---|
| tachyon-free | 10,986 (39%) |
| SM-like | 4 |
| SM-like **and** tachyon-free | **0** |

All 4 SM-like draws come from Witten shifts whose base is already tachyonic (6 tachyonic fields). **On Z6-I the SM-like
Witten shifts are exactly the tachyonic ones.** 11100's conclusion holds at 8× the V0 sample.

### 12173: synthesis

The closure of 12167 stands, now with an untwisted theorem for the missing 10_H and a much larger Z6-I sample. The
level-3 structure of the Wilson-line modulus belongs to 11115/11136/11139.
