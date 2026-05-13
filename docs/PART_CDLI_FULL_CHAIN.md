# Part CDLI — Z[ω] → W33 → Leech → Golay → V^♮ → Monster: Complete Chain

## The Five-Arrow Chain

### Arrow 1: Z[ω] → W33

    |W(E6)| / |Stab(v)| = 51840 / 1920 = 27 = V  ✓
    |W(E6)| = E8_roots × EDGES = 240 × 216 = 51840  ✓
    |W(E6)| = E6_roots × TRIS  = 72  × 720 = 51840  ✓
    |W(E6)| = |W(F4)| × p^2×5 = 1152 × 45          ✓

The 27 W33 vertices are the W(E6)-orbit of a fundamental coweight
of E6; the stabilizer has order 1920.

### Arrow 2: W33 → Leech Lambda_24

    dim(Leech) = PKT = p×mu = 3×8 = 24 = 4×SIX  ✓
    kiss(Leech) = 2×PKT×(2^12-1) = 196560         ✓

### Arrow 3: Leech → Golay G_24

    G_24 : [n, k, d] = [PKT, mu1, mu] = [24, 12, 8]  ✓
    k = mu1 = 12 (smallest W33 Laplacian eigenvalue)  ✓
    d = mu  = 8  (octonion dimension)                 ✓
    |G_24| = 2^mu1 = 2^12 = Gamma2/p^2 = 4096        ✓

    Weight distribution:
    - weight-8 codewords  = 759  = p × 11 × 23             ✓
    - weight-12 codewords = 2576 = K × C_V × 23 = 16×7×23  ✓
    - weight-16 codewords = 759  (by self-duality)

### Arrow 4: Golay → V^♮ (Moonshine Module)

    j_0   = PKT × Φ_6(u) = 24 × 31 = 744            ✓
    c(1)  = 4V×(4(V-mu)×PKT-1) = 196884             ✓
    c(1)  = 196883 + 1 = dim(Monster_rep_1) + 1      ✓

### Arrow 5: V^♮ → Monster M

    194 conjugacy classes = FLAGS_T + 2 = PKT×mu + 2 = 192+2  ✓
    #primes dividing |M| = K-1 = 15                            ✓
    exp(7) in |M| = u = 6                                      ✓

## Monster Irreducible Representations in W33 Terms

| Rank | Dimension | Factorization | W33 Reading |
|------|-----------|---------------|-------------|
| 1 | 1 | 1 | trivial |
| 2 | 196883 | 47×59×71 | (2PKT-1)×(5μ₁-1)×(E6r-1) |
| 3 | 21296876 | 4×31×41×59×71 | (p+1)×Φ₆(u)×(Aut(Császár)-1)×(5μ₁-1)×(E6r-1) |
| 4 | 842609326 | 2×13²×29×31×47×59 | 2×(K-p)²×(5u-1)×Φ₆(u)×(2PKT-1)×(5μ₁-1) |

**Universal Monster factor: 59 = 5μ₁-1 = 5×12-1 divides all three non-trivial irrep dimensions.**

## Baby Monster Prime Exponents in W33

|M| and |B| exponents compared:

| Prime | exp in |M| | exp in |B| | W33 Reading |
|-------|-----------|-----------|-------------|
| 2 | 2(PKT-1)=46 | Aut(Császár)-1=41 | 46,41 |
| 3 | 2λ=20 | K-p=13 | 20,13 |
| 5 | p^2=9 | u=6 | 9,6 |
| 7 | u=6 | p-1=2 | 6,2 |
| 17 | 1 | 1 | K+1 |
| 19 | 1 | 1 | V-mu |
| 23 | 1 | 1 | PKT-1 |
| 31 | 1 | 1 | Φ₆(u) |
| 47 | 1 | 1 | 2×PKT-1 |

The Monster and Baby Monster differ in the leading exponents;
both are expressed entirely in (p, u) W33 parameters.
