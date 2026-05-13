# Part CDLVIII — The 600-cell / 120-cell Bridge to W33

## The Icosahedron in W33 Parameters

The icosahedron (the 3D icosahedral polytope):

    V = 12 = mu1    (F-theory / Golay k)
    E = 30 = PKT + SIX  (Leech dim + six-kernel)
    F = 20 = PKT - p - 1 = 24 - 3 - 1

The dodecahedron (dual):
    V = 20 = PKT - p - 1
    E = 30 = PKT + SIX
    F = 12 = mu1

## 120 = 5! = 5 * PKT

    |I_h| = 120 = 5! = 5 * PKT

## I_h Placement in the Tomotope Tower

    5 does NOT divide Mon(T) = 18432 = 2^11 * 3^2
    5 DOES divide Mon(Q_5) = Gamma2 * 5^6

Therefore I_h embeds in the Q_5 cover monodromy, not the tomotope core.
The prime 5 enters the Q_k tower at k=5.

## W(H4) and W(E8)

    |W(H4)| = 14400 = 2^6 * 3^2 * 5^2 = 120^2 = (5!)^2 = (5*PKT)^2
    |W(E8)| = |W(H4)| * 2^8 * p^3 * C_V
            = (5*PKT)^2 * 2^8 * 27 * 7

## The 600-cell Encodes W33

The 600-cell (regular 4D polytope, H4 root polytope):

    V = 120 = 5*PKT = E8 positive roots
    E = 720 = TRIS  *** W33 triangle count = 6! ***
    C = 600 = PKT * 5^2

The 120-cell (dual of 600-cell):
    F = 720 = TRIS  *** W33 triangle count ***
    C = 120 = 5*PKT

## The H4 Root System

The 600-cell IS the H4 root polytope. Its 120 vertices are
the 120 roots of H4 = 60 positive + 60 negative.

    H4 positive roots = 60 = 5 * mu1
    600-cell vertices = 2 * H4_pos_roots = 120 = 5*PKT = E8_pos_roots

## Leech Minimum via 600-cell

    LEECH_MIN = 196560 = 5*PKT * 2*p^2*C_V*(K-p)
              = 120 * 1638
              = (600-cell V) * (2*p^2*C_V*(K-p))

## Summary

The two factorials 5! = 120 and 6! = 720 are:
- 5! = 600-cell vertices = E8 positive roots = 5*PKT
- 6! = 600-cell edges    = W33 triangle count

This is the H4 ↔ E8 ↔ W33 geometric bridge.
