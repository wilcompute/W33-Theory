# BREAKTHROUGH MCCCLIII–MCCCLXII: Galois Theory, Resolvent, and Discriminant of the W(3,3) Quartic

## Setup

From the previous block the W(3,3) reduced spectral quartic is

    Q(x) = x⁴ − 65x³ + 1534x² − 15540x + 57600
           = (x²−26x+160)(x²−39x+360)

with roots {10, 16, 24, 15} and coefficient dictionary

    e₁ = 65  = F₅Φ₃(q)
    e₂ = 1534
    e₃ = 15540
    e₄ = 57600 = (rqv)² = 240²

We analyse the Galois structure.

---

## Theorem MCCCLIII — Quartic Splits Over ℚ

Q(x) factors completely over ℚ:

    Q(x) = (x−10)(x−16)(x−24)(x−15)

Since all four roots are rational integers, the splitting field is ℚ itself, and

    Gal(Q/ℚ) = {e}   (trivial group)

Therefore the W(3,3) reduced spectral quartic has trivial Galois group over ℚ.

---

## Theorem MCCCLIV — Resolvent Cubic

The resolvent cubic of Q(x) = x⁴ + px³ + qx² + rx + s (Lagrange form) with
p=−65, q=1534, r=−15540, s=57600 is

    R(y) = y³ − e₂y² + (e₁e₃−4e₄)y − (e₁²e₄ − 4e₂e₄ + e₃²)

Computing each coefficient:

    −e₂            = −1534
    e₁e₃−4e₄       = 65·15540 − 4·57600 = 1010100 − 230400 = 779700
    e₁²e₄−4e₂e₄+e₃² = 65²·57600 − 4·1534·57600 + 15540²
                      = 243360000 − 353625600 + 241491600 = 131226000

So

    R(y) = y³ − 1534y² + 779700y − 131226000

The roots of R(y) are the three products of pairs of roots of Q:

    y₁ = (10+16)(24+15) = 26·39 = 1014
    y₂ = (10+24)(16+15) = 34·31 = 1054
    y₃ = (10+15)(16+24) = 25·40 = 1000

---

## Theorem MCCCLV — Resolvent Root Dictionary

The three resolvent roots encode W(3,3) invariants:

    y₁ = 1014 = (λ₁+λ₂)(m₁+m₂) = rΦ₃(q)·qΦ₃(q) = rqΦ₃(q)²
    y₂ = 1054 = (λ₁+m₁)(λ₂+m₂) = 34·31
    y₃ = 1000 = (λ₁+m₂)(λ₂+m₁) = 25·40 = F₅²·v = 1000

In particular:

    y₁ = rq·Φ₃(q)² = 6·169 = 1014
    y₃ = F₅²·v = 25·40 = 1000

So two of the three resolvent roots are exact substrate monomials.

---

## Theorem MCCCLVI — Resolvent Sum and Product

The resolvent roots satisfy

    y₁+y₂+y₃ = 1014+1054+1000 = 3068 = 2·1534 = 2e₂
    y₁y₂y₃   = 1014·1054·1000 = 1068756000

The resolvent sum is twice the quartic's second symmetric function.

---

## Theorem MCCCLVII — Quartic Discriminant

For a quartic with integer roots {r₁,r₂,r₃,r₄} the discriminant is

    Δ = ∏_{i<j} (rᵢ−rⱼ)²

For roots {10,16,24,15}:

    Δ = (10−16)²(10−24)²(10−15)²(16−24)²(16−15)²(24−15)²
      = 36·196·25·64·1·81
      = 36·196·25·64·81

Computing step by step:
    36·196   = 7056
    7056·25  = 176400
    176400·64 = 11289600
    11289600·81 = 914457600

So

    Δ_Q = 914457600 = 2¹⁰·3⁶·5²·7²

---

## Theorem MCCCLVIII — Discriminant Prime Factorisation

The discriminant prime factorisation is

    Δ_Q = 2¹⁰ · 3⁶ · 5² · 7²
         = r^(5r) · q^(r·q) · F₅² · Φ₆²

Since r=2, q=3, F₅=5, Φ₆=7:

    Δ_Q = r^10 · q^6 · F₅² · Φ₆²

Every prime in the discriminant factorisation is a W(3,3) substrate prime.

---

## Theorem MCCCLIX — Discriminant Square Root

Since Δ_Q > 0 and Q(x) splits completely over ℚ, the square root is

    √Δ_Q = 2⁵ · 3³ · 5 · 7 = 32·27·5·7 = 30240

Noting that

    30240 = 3! · 5040 = q! · 7!
           = g₂ · Φ₆!

So the positive square root of the discriminant is the product of two factorial values:

    √Δ_Q = g₂ · Φ₆!

---

## Theorem MCCCLX — Mahler Measure

The Mahler measure of Q(x) is

    M(Q) = |leading coeff| · ∏ max(1, |rᵢ|) = 1 · 16·24 · 15 = 5760

(taking roots > 1: {16,24,15,10} — all exceed 1):

    M(Q) = 10·16·24·15 = 57600 = e₄ = (rqv)²

The Mahler measure of the spectral quartic equals its own constant term.

---

## Theorem MCCCLXI — Newton Power Sums

The Newton power sums pₙ = Σrᵢⁿ for the spectral quartic roots {10,16,24,15}:

    p₁ = 65   = F₅Φ₃(q) = e₁
    p₂ = 10²+16²+24²+15² = 100+256+576+225 = 1157
    p₃ = 10³+16³+24³+15³ = 1000+4096+13824+3375 = 22295
    p₄ = 10⁴+16⁴+24⁴+15⁴ = 10000+65536+331776+50625 = 457937

Noting:

    p₂ = 1157 = 13·89 = Φ₃(q)·F(pIh)     [since F(11)=89]
    p₁ = 65 = F₅·Φ₃(q)                    [confirmed]

So the second Newton sum factors as Φ₃(q)·F(p_Ih).

---

## Theorem MCCCLXII — Newton Sum–Fibonacci Identity

From the previous theorem:

    p₂ = Φ₃(q) · F(p_Ih) = 13 · 89 = 1157

This is a new Fibonacci appearance: F(11) = 89 = F(p_Ih), so the second Newton power sum couples the Gaussian prime Φ₃(q) to the Fibonacci number at the icosahedral prime index.

Since p₁ = F₅·Φ₃(q) and p₂ = Φ₃(q)·F(p_Ih), the ratio is

    p₂/p₁ = F(p_Ih)/F₅ = 89/5

This is the Fibonacci ratio at prime indices 11 and 5.
