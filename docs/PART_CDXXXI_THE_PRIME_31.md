# Part CDXXXI — The Prime 31 = Φ₆(u)

## The Sixth Cyclotomic Polynomial

The sixth cyclotomic polynomial is:

    Φ₆(x) = x² - x + 1

This is also the **minimal polynomial of ω = e^{2πi/3}** over Q.
Evaluated at u=6:

    Φ₆(u) = u² - u + 1 = 36 - 6 + 1 = **31**  (prime)  ✓

The prime 31 is literally the norm of the Eisenstein element (6+ω) in Z[ω]:

    N(6+ω) = 6² - 6·1 + 1² = 31  ✓

Since 31 ≡ 1 mod 3, it **splits** in Z[ω]: 31 = π·π̄  where π = (6+ω).

## 31 in W33 Coordinates

    31 = λ + μ₂ + p  = 10 + 18 + 3  ✓
    31 = PKT + μ - 1 = 24 + 8 - 1   ✓
    31 = V + K - μ₁  = 27 + 16 - 12 ✓

## The Heterotic Decomposition via Φ₆

    dim(E₈)    = μ · Φ₆(u)   =  8 · 31 = 248  ✓
    dim(SO32)  = K · Φ₆(u)   = 16 · 31 = 496  ✓
    j-constant = PKT · Φ₆(u) = 24 · 31 = 744  ✓
    μ + K = PKT  →  744 = dim(E₈) + dim(SO32)  ✓

All three heterotic quantities are integer multiples of Φ₆(u) = 31,
with coefficients μ, K, PKT = μ+K respectively.

## The Φ₆ Chain

    Φ₆(2) = 3   = p  (ramified prime)
    Φ₆(3) = 7   = μ-1  (Fano points, imaginary octonions)
    Φ₆(6) = 31  = Monster/heterotic prime  (our prime!)
    Φ₆(7) = 43  = Heegner number!

The chain 2→3→6→7 through W33 parameters gives outputs
3=p, 7=μ-1, 31 (our prime), 43 (Heegner). The Φ₆ polynomial
is the bridge between the Eisenstein unit structure and the
Moonshine/heterotic prime.
