# Passes 12217–12222: twisted 10s exist but are fermions (correcting 12208); the family triplet needs two Wilson lines

Claude track. Producer: `analysis/w33_pass12217_to_12222_twisted_tens_are_fermions.py`. Drivers:

- `analysis/search_drivers_12217/` (`exhaust10.py`, `exhaust10_full.py`, `build_candidates.py`)
- `analysis/search_drivers_12218/roots2751.py`
- `analysis/search_drivers_12219/sym_asym.py`

## 12217: the exhaustive twisted-10 analysis, and a correction

**Scope.** One A4-type second Wilson line W = (λ, μ) over 7 bases × 864 λ × 6561 μ, with the admissibility of 12161. That
gives 231,124 admissible configurations.

**Necessary condition, checked before any projection phase.** A twisted massless 10 needs |P|² = 4/3 and an SU(5)-projection
norm of 6/5.

- The first E8 alone does not exclude it: hits occur with |P1|² = 4/3, and with 11/9 in Witten-twisted cosets.
- With the second-E8 class included (P2 = 0, resp. |P2|² = 1/9), **exactly 405** configurations admit a twisted 10-type
  vector.

**As models in the engine.**

- 153 of the 405 load; the other 252 fail the engine's consistency conditions.
- All 153 are SU(5)×U(1) and tachyon-free.
- **All 153 carry twisted 10s: 918 fields, every one a fermion in a Witten-twisted sector. Twisted scalar 10s: 0.**

**Correction.** 12208's "no twisted 10 of either statistics" held only for its 163-model sample. The class has density
0.17%; the 1616-configuration sample of 12212 would expect about 2.8 hits and saw 0. Those paragraphs are now corrected in
the paper.

**What is true on this scope:** no scalar 10 exists in any sector. Untwisted, this is theorem 12170. Twisted, the only 10s
are fermions.

## 12218: why the family-triplet parent cannot interpolate

The unbroken roots of SM_2751:

| Wilson lines | roots | A2 factors |
|---|---|---|
| actual | A1 + A2 + A2 + A4 | 2 (colour + family) |
| W5 = 0 | A1³ + A2 + A3 + A5 | 1 |
| W6 = 0 | A2 + A4 + D5 | 1 |
| W6 = W5 | A2 + A4 + D5 | 1 |
| both = 0 | A2 + D5 + E6 | 1 |

The base gives E6 × SU(3)_family. Keeping the family SU(3) while breaking E6 to the Standard Model needs two independent
order-2 Wilson lines, which is exactly the absence of a symmetric direction.

## 12219: symmetric versus asymmetric Z3

Results on the native II(2,2):

| twist | order-2 translations | invariant moduli |
|---|---|---|
| asymmetric (g1 or g2 alone) | 2 | 0 |
| symmetric (g1 g2, g1 g2⁻¹; det(1 − g) = 9) | 0 | 2 |

**A twisted plane carries a translation or a running radius, never both.**

## 12220 and 12221

- **12220:** the 12214 note has had no reply yet.
- **12221:** the paper now cites Theorems 7.5–7.6 in three places: the Section 9 key idea, scorecard entry 8, and Section 11
  open problem 1.
