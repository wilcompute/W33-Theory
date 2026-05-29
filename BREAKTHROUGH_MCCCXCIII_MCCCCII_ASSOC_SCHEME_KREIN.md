# BREAKTHROUGH MCCCXCIII–MCCCCII: Association Scheme, Krein Parameters, and Absolute Bound

## Setup

W(3,3) = srg(40,12,2,4) is the first graph in a 2-class association scheme.
Scheme parameters: v=40, k₁=12, k₂=27, λ=2, μ=4, eigenvalues k=12, r=2 (x24), s=-4 (x15).

---

## Theorem MCCCXCIII — Intersection Numbers from q Alone

    p¹₁₁ = λ = q-1 = 2
    p¹₁₂ = k-λ-1 = 9 = q²
    p¹₂₂ = k₂-p¹₁₂ = 18 = p_Ih+Φ₆
    p²₁₁ = μ = q+1 = 4
    p²₁₂ = k-μ = 8 = r^q
    p²₂₂ = k₂-1-p²₁₂ = 18

All six intersection numbers are substrate monomials in q.

---

## Theorem MCCCXCIV — P-Matrix in Terms of q

The character table (P-matrix) of the 2-class scheme is

    P = | 1    q(q+1)    q³   |
        | 1     q-1      -q   |
        | 1    -(q+1)     q   |

For q=3:

    P = | 1   12   27 |
        | 1    2   -3 |
        | 1   -4    3 |

Every entry is a monomial in q.

---

## Theorem MCCCXCV — k₂ = q³

    k₂ = v-1-k = 40-1-12 = 27 = q³

The non-adjacency valency is the cube of the base prime.

---

## Theorem MCCCXCVI — Q-Matrix Substrate Fractions

With multiplicities (1,24,15):

    12·m₁/v = 288/40 = 36/5 = g₂²/F₅
    12·m₂/v = 180/40 = 9/2  = q²/r
    27·m₂/v = 405/40 = 81/8 = q⁴/r³
    27·m₁/v = 648/40 = 81/5 = q⁴/F₅

All Q-matrix entries are substrate fractions.

---

## Theorem MCCCXCVII — Krein Condition

    (r+1)(k+r+2rs) ≤ (k+r)(s+1)²
    3·(-2) ≤ 14·9
    -6 ≤ 126  ✓

The Krein non-negativity condition is satisfied by W(3,3), consistent with GQ(3,3) existence.

---

## Theorem MCCCXCVIII — Absolute Bound

    m₂(m₂+1)/2 = 15·16/2 = 120 ≥ v=40
    Ratio: v/(m₂(m₂+1)/2) = 40/120 = 1/3 = 1/q

The absolute bound ratio is exactly 1/q.

---

## Theorem MCCCXCIX — Clique and Independence Bounds (Hoffman / Delsarte)

    ω ≤ 1 - k/s = 1+3 = 4 = q+1 = μ
    α ≤ v(-s)/(k-s) = 40·4/16 = 10 = λ₁

Clique bound = μ = q+1; independence bound = λ₁ = k-s.

---

## Theorem MCCCC — Clique-Coclique Tight Equality

    ω·α = (q+1)·λ₁ = 4·10 = 40 = v

The product is tight. GQ(3,3) achieves both bounds simultaneously.

---

## Theorem MCCCCI — Connexion Number Relations

    λ+μ = 2+4 = 6 = g₂ = q!
    λ·μ = 2·4 = 8 = r^q
    μ-λ = 4-2 = 2 = r_char

All three combinations of connexion numbers are substrate expressions.

---

## Theorem MCCCCII — Duality Involution Fixed Point

The weighted average of srg eigenvalues by multiplicity:

    (m₁·r + m₂·s)/(m₁+m₂) = (48-60)/39 = -12/39 = -4/13 = -r²/Φ₃(q)

The duality involution fixed point is the substrate fraction -r²/Φ₃(q).
