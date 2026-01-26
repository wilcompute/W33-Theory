# W33 Quick Reference

## The Construction (one page)

```
V = F₃⁴ + symplectic ω
        ↓
    W(3,3) GQ
   40 pts, 40 lines
        ↓
W33 = SRG(40,12,2,4)
Aut = W(E₆) = 51840
        ↓
   A² ≡ 0 (mod 2)
  [40, 24, 6] code
  240 weight-6 gens
        ↓
   H = F₂⁸ (dim O)
  120 nonsingular
 SRG(120,56,28,24)
        ↓
  Gauge fix → Q
     Q ≅ W33 ←───┐
        │        │
        └────────┘
      (bootstrap)
```

## Key Numbers

| n | Meaning | Factors |
|---|---------|---------|
| 3 | field | prime |
| 8 | dim(H) | 2³ = dim(O) |
| 40 | points | 8×5 |
| 81 | cycles | 3⁴ |
| 88 | core | 8×11 |
| 90 | vacuum | 2×3²×5 |
| 120 | roots/2 | 8×15 |
| 240 | roots | 2⁴×3×5 |
| 248 | E₈ | 8×31 |

## SRG Parameters

W33: SRG(40, 12, 2, 4), spectrum 12¹ 2²⁴ (-4)¹⁵
120-shell: SRG(120, 56, 28, 24), spectrum 56¹ 8³⁵ (-4)⁸⁴

## Physical Predictions

α⁻¹ = 81 + 56 + 40/1111 ≈ 137.036
sin²θ_W = 40/173 ≈ 0.2312
Generations = 81/27 = 3
Ω_DM/Ω_b = 27/5 = 5.4
m_t = v√(40/81) ≈ 173 GeV
m_H = v√(81/312) ≈ 125 GeV

## Vacuum Modes (90 = 45 + 45)

S=+1: 1 + 24 + 20 = 45
S=-1: 15 + 30 = 45

## Tetrahedra (9450 total)

J≠0: 3008 = 64×47
  J=1: 1512 = 8×27×7
  J=2: 1496 = 8×11×17
J=0: 6442

## Gauge/Matter Split

Gauge: Aut(W33) = W(E₆), 240 roots
Matter: H₃ = Z₃⁸⁹ = 88D core ⊕ 1D
Vacuum: 90 non-iso lines
Sources: J = dF on tetrahedra

## Bootstrap Equation

Q = W33 (self-reference)
