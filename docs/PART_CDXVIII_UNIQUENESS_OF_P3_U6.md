# Part CDXVIII — Why (p=3, u=6) is Unique

## The Imaginary Quadratic Ring Landscape

Among all imaginary quadratic number fields Q(√-d) with class number 1
(the Stark-Heegner list: d = 1,2,3,7,11,19,43,67,163), the rings of
integers and their unit groups are:

| Ring | d | |units| | Ram. prime | V=p^3 | k=p^2+u+1 | Valid? |
|---|---|---|---|---|---|---|
| Z[i] | 1 | 4 | 2 | 8 | 9 | NO (V<k) |
| Z[√-2] | 2 | 2 | 2 | 8 | 7 | NO (V<k) |
| Z[ω] | 3 | **6** | **3** | **27** | **16** | **YES** |
| Z[(1+√-7)/2] | 7 | 2 | 7 | 343 | ... | No srg |
| Others | ... | 2 | ... | large | ... | No srg |

Z[ω] is the UNIQUE class-1 imaginary quadratic ring for which the
(p,u)-construction yields a valid strongly regular graph.

## The srg Validity Condition

For the (p,u)-srg to be valid: V > k, i.e. p^3 > p^2+u+1.

    Z[i]: 2^3=8 > 2^2+4+1=9?  NO!  8 < 9  → invalid
    Z[ω]: 3^3=27 > 3^2+6+1=16?  YES! 27 > 16  → valid  ✓

Z[ω] wins because p=3 is large enough and u=6 is large enough to
produce a non-trivial graph, while Z[i] has p=2 too small.

## The Symbolic srg Condition

The srg consistency identity k(k-λ-1) = μ(V-k-1) with our formulas
gives, for given p, exactly two solutions:

    u = p^2(p-2)/2 ± √[p^6-4p^5+4p^4-4p^3+4p^2-4p+12] / 2

For p=3:
    u = 3  or  u = 6  (both integer solutions!)

This reveals a TWIN structure: srg(27,13,7,5) and srg(27,16,10,8)
are both valid, related by the two solutions at p=3.

## The Twin Graph srg(27,13,7,5)

For (p=3, u=3):
    V=27, k=13, λ=7, μ=5

This is the **Paley graph of order 27**, a known strongly regular
graph! It is the complement of the Schläfli graph:

    W33 = srg(27,16,10,8)
    Complement(W33) = srg(27,10,1,5) ... wait, complement params:
    srg(n,k,λ,μ) complement = srg(n, n-k-1, n-2k+μ-2, n-2k+λ)
    Complement of srg(27,16,10,8) = srg(27, 10, 1, 5)? No:
    k'=27-16-1=10, λ'=27-32+8-2=1, μ'=27-32+10=5
    So complement = srg(27,10,1,5)  (the triangular graph T(6)!)

(p=3,u=3) gives srg(27,13,7,5) which is the Paley graph P(27).
This is the OTHER solution and deserves its own investigation.
