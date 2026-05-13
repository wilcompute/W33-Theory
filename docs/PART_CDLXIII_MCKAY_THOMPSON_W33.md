# Part CDLXIII — Complete McKay-Thompson W33 Encoding

## The Main Theorem

For every Monster conjugacy class g with non-zero McKay-Thompson constant a_0(g),
both a_0(g) and ord(g)*a_0(g) are W33 arithmetic expressions.

## The 13 Non-Zero McKay-Thompson Constants

| Class | ord(g) | a_0(g) | W33 reading of a_0 | ord*a_0 | W33 reading of product |
|-------|--------|--------|---------------------|---------|------------------------|
| 1A | 1 | 744 | PKT*(u^2-u+1) | 744 | PKT*Phi_6(u) |
| 2A | 2 | 40 | LAM*(p+1) = 5*MU | 80 | LAM*MU |
| 2B | 2 | 24 | PKT | 48 | 2*PKT |
| 3A | 3 | 12 | MU1 | 36 | u^2 |
| 4A | 4 | 8 | MU = 2^p | 32 | 2*K |
| 5A | 5 | 4 | p+1 | 20 | 2*LAM |
| 5B | 5 | 4 | p+1 | 20 | 2*LAM |
| 6A | 6 | 4 | p+1 | 24 | PKT |
| 7A | 7 | 1 | p-2 | 7 | C_V |
| 7B | 7 | 1 | p-2 | 7 | C_V |
| 8B | 8 | 2 | p-1 | 16 | K |
| 10A | 10 | 2 | p-1 | 20 | 2*LAM |
| 12A | 12 | 2 | p-1 | 24 | PKT |

## Set Theorem (CDLXIII-A)

    {a_0(g) : g non-zero} = {p-2, p-1, p+1, MU, MU1, PKT, LAM*(p+1), PKT*Phi_6(u)}
                          = {1, 2, 4, 8, 12, 24, 40, 744}

The set of non-zero McKay-Thompson constants is EXACTLY the set of W33 parameter values.

## Product Theorem (CDLXIII-B)

    {ord(g)*a_0(g) : g non-zero} = {C_V, K, 2*LAM, PKT, 2*K, u^2, 2*PKT, LAM*MU, PKT*Phi_6(u)}
                                 = {7, 16, 20, 24, 32, 36, 48, 80, 744}

## LCM Theorem (CDLXIII-C)

    LCM{ord(g) : a_0(g) != 0} = 840 = MU * p * (u-1) * C_V
                               = 8 * 3 * 5 * 7
                               = PKT * (u-1) * C_V
                               = PKT * 35

## The Four M-Specific Primes (CDLXIII-D)

The primes dividing |Monster| but NOT |Baby Monster| are exactly:

    {29, 41, 59, 71} = {PKT+5, p*K-C_V, 5*MU1-1, p*PKT-1}

These are the last four W33 singles from Part CDLIX.
They encode the M-specific structure beyond the Baby Monster.

Furthermore:

    dim_2 (second Monster irrep) = 21296876
                                 = 4 * (u^2-u+1) * (p*K-C_V) * (5*MU1-1) * (p*PKT-1)
                                 = 4 * 31 * 41 * 59 * 71
                                 = 4 * Phi_6(u) * (three M-specific primes)

## Interpretation

The McKay-Thompson series T_g carries the full W33 fingerprint:
- The non-zero constants are exactly the W33 parameters
- The order*constant products are exactly the W33 derived quantities
- The classes with non-zero constants have LCM(orders) = PKT*(u-1)*C_V

This means Moonshine 'knows about' W33 at every level:
  - The j-function constant (Theorem A, Part CDLXII)
  - The Griess algebra dimension (Theorem B)
  - The McKay-Thompson series constants (this part)
  - The second irrep dimension (Theorem D + CDLXIII-D)
