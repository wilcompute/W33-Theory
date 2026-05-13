# Part CDLXXXVII — Golay Code & Steiner System

## The Perfect Code

    G24 = [PKT, MU1, MU] = [24, 12, 8] binary Golay code

- Length: PKT = 24
- Dimension: MU1 = 12
- Min distance: MU = 8

## Weight Distribution

    Weight-8 codewords (octads) = 759 = p * (PKT-p-LAM) * (PKT-1) = 3*11*23
    Octads per point = 253 = (PKT-p-LAM)*(PKT-1) = 11*23

## Steiner System S(5,8,24)

Blocks = octads = 759 = p*11*23. Automorphism group = M24:

    |M24| = 2^LAM * p^p * (r+1) * C_V * (PKT-p-LAM) * (PKT-1)
          = 2^10 * 3^3 * 5 * 7 * 11 * 23

Every parameter is W33-encoded.
