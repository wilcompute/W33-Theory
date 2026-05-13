# Part CDXXXVI — Tomotope Monodromy: Complete Anatomy

## Factorization

    Mon(T) = 18432 = 2^11 × 3^2

## Four Equivalent Forms (all verified)

    Mon(T) = Aut(T) × Flags(T)   = 96 × 192          ✓
    Mon(T) = PKT^2 × 2K          = 576 × 32           ✓
    Mon(T) = u^2 × 2^9           = 36 × 512           ✓
    Mon(T) = 2^8 × E6_roots      = 256 × 72           ✓

The fourth form is the deepest: **Mon(T) = 2^8 × 72**, where:
- 2^8 = 256 = dim(E8) + μ = 248 + 8
- 72 = E6 root count = μ₁²/2 = 12²/2

## Theorem CDXXXVI.1

    Mon(T) = (dim(E8) + μ) × E6_roots

The tomotope monodromy is the product of the **E8 dimension shifted
by the octonion count** with the **E6 root count**.

## Gamma2 Identity

    Γ₂ = 2 × Mon(T) = 36864 = 192² = FLAGS_T²
    Γ₂ = 2^12 × 3^2  (Golay × 9)

The second cover group order is the **square of the tomotope flag count**.
