# Part CDLXX — One-Parameter Collapse

## The Master Dictionary

Every constant in the theory derives from **p = 3** alone:

| Constant | Expression in p | Value |
|----------|-----------------|-------|
| u (six-kernel) | 2p | 6 |
| r (eigenvalue) | p+1 | 4 |
| PKT (24-packet) | (p+1)*2p = r*u | 24 |
| K (valency) | (p+1)^2 = r^2 | 16 |
| V (vertices) | p^3 | 27 |
| LAM (λ) | C(p+2,2) = C(r+1,2) | 10 |
| MU (μ) | 2(p+1) = 2r | 8 |
| MU1 (μ₁) | p(p+1) = r(r-1) | 12 |
| C_V | 2p+1 | 7 |
| C_E | (2p+1)p | 21 |
| h(E₆) | p(p+1) = MU1 | 12 |
| h(E₇) | 2p² | 18 |
| h(E₈) | 2p(p+2) = PKT+u | 30 |
| E₆ roots | 2p²(p+1) = p·PKT | 72 |
| E₈ roots | LAM·PKT | 240 |
| triangles(W33) | (2p)! = u! | 720 |
| Leech min-norm | u!·p·(2p+1)·(p²+p) | 196560 |
| Gap (17×19) | (r²+1)(2r+r(r-1)/r+1) | 323 |

## W33 Complement

    W33 complement = srg(27, 10, 1, 5)
    Triangles in complement = p²(p+2) = 45

## Csaszár Toroid in W33

    V = C_V = 2p+1 = 7
    E = C_E = (2p+1)p = 21
    F = 2*C_V = 14
    Euler: V - E + F = 7 - 21 + 14 = 0  (torus)

The Csaszár toroid is the W33 vertex/edge parametric object living inside the same arithmetic.
