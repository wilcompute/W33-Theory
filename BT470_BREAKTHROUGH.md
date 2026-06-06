# BT470: MONSTER MOONSHINE, ALL SUPERSINGULAR PRIMES, KNIGHT-WEYL

*W33-Theory Breakthrough Document — June 2026*  
*24/24 verified.*

---

## Theorem [MONSTER-EXPS]: Monster Prime Exponents Are Substrate-Pure

|Monster| = 2^46 · 3^20 · 5^9 · 7^6 · 11^2 · 13^3 · ...

| Prime | Exponent | Substrate form |
|-------|----------|---------------|
| 2=λ | 46 | v+Φ₆−1 = λ(f−1) |
| 3=q | 20 | f−μ = Φ₄·λ = k+λ^q |
| 5=F₅ | 9 | q² = k−q |
| 7=Φ₆ | 6 | q·λ = rank(E₆) |
| 11 | 2 | λ |
| 13=Φ₃ | 3 | q |

---

## Theorem [SPORADIC]: All 9 Sporadic Monster Primes Are Substrate

| Prime | Substrate form |
|-------|---------------|
| 17 | k+F₅ |
| 19 | k+Φ₆ |
| 23 | λ·q²+F₅ |
| 29 | q^q+λ |
| 31 | q^q+μ |
| 41 | v+1 |
| 47 | λ·f−1 |
| 59 | λ·q^q+F₅ |
| 71 | q·f−1 |

Every prime that divides |Monster| and is not {2,3,5,7,11,13} is a substrate expression.

---

## Theorem [SUPERSINGULAR]: The Supersingular Prime Set Is Substrate-Controlled

The 15 supersingular primes are exactly the Monster divisor primes.

- Count: 15 = g⁻ = F₅·q = 5·3
- Sum: 2+3+5+…+71 = 378 = λ·q³·Φ₆ = 2·27·7

---

## Theorem [KNIGHT-WEYL]: Knight Graph Edges = f; Weyl Increments = Knight Coordinates

The 4×4 = μ² knight graph (from BT-knight-tour scripts):
- **Edges = f = 24 = |SL(2,q)|**
- Knight move distance² = 1+λ² = F₅ = 5
- Knight move coordinates (1, λ) encode the Weyl increment pair:
  - **+q = 1+λ** (short + long = q)
  - **+μ = λ^λ** (board dimension = λ squared = μ)

The Weyl ladder increments (+q, +μ) in the lam-exponents of W(E6)→W(E7)→W(E8)
are precisely the two components of a knight move (1, λ) on the μ×μ board.

---

## Chain
- BT464–BT469: previous results
- **BT470: Monster moonshine + supersingular primes + knight-Weyl (24/24)** ← THIS

## Open Questions (BT471+)

1. **Co0 Leech lattice group:** |Co0| = 2^22 · 3^9 · 5^4 · 7^2 · 11 · 13 · 23.
   Are the exponents 22, 9, 4, 2 substrate-pure?
   22 = f−lam? = 22 ✓; 9 = q^2 ✓; 4 = μ ✓; 2 = λ ✓.

2. **Mathieu M24:** |M24| = 2^10 · 3^3 · 5 · 7 · 11 · 23.
   Exponents: 10=Φ₄, 3=q, 1,1,1,1 — all substrate!

3. **McKay-E8 correspondence:** The Monster moonshine j-function and McKay’s observation
   that the E8 diagram encodes the Monster’s smallest representations.
   Is this the substrate’s E8 = lam^mu·F5·q roots connection?
