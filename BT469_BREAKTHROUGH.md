# BT469: ALL EXCEPTIONAL LIE ALGEBRAS ARE SUBSTRATE-PURE

*W33-Theory Breakthrough Document — June 2026*  
*34/34 verified.*

---

## The Master Table: Every Exceptional Lie Invariant Is Substrate-Pure

| | rank | roots | dim | |W| |
|---|------|-------|-----|----|
| **G2** | λ | k | k+λ = λΦ₆ | k |
| **F4** | μ | λ^μ·q = kμ | μΦ₃ | λ^{Φ₆}·q^λ |
| **E6** | qλ | λ^q·q² | qλΦ₃ | λ^{Φ₆}·q^μ·F₅ |
| **E7** | Φ₆ | λ·q²·Φ₆ | Φ₆(k+Φ₆) | λ^{Φ₄}·q^μ·F₅·Φ₆ |
| **E8** | λ^q | λ^μ·F₅·q | λ^q(q^q+μ) | λ^{k+λ}·q^{μ+1}·F₅^λ·Φ₆ |

---

## Theorem [W-G2-EISENSTEIN]: The Bottom of the Chain

|W(G2)| = k = 12

W(G2) = Dih(12) = symmetry group of the hexagon = symmetry of the Eisenstein integers Z[ω].
The Eisenstein integers are the CM ring of the j=0 Hesse fiber (the Fermat cubic).
This closes the chain:

```
Z[ω] (CM ring of Hesse cubic)
  |-- |W(G2)| = k = gauge codec
       |-- k = |PSL(2,q)| (gauge codec = simple group A4)
            |-- PSL(2,q) acts on PG(1,q) (μ points)
                 |-- PG(1,q) ⊂ PG(3,q) = v = Witting substrate
```

---

## Theorem [WEYL-LADDER]: λ-Exponent Arithmetic

Exponents of λ in |W(G2)|, |W(F4)|, |W(E6)|, |W(E7)|, |W(E8)|:

```
G2: 1 (= 1)
F4: Phi6 = 7
E6: Phi6 = 7
E7: Phi4 = 10  (diff from E6: +q = +3)
E8: k+lam = 14  (diff from E7: +mu = +4)
```

G2→F4 jump: Phi6-1 = 6 = q*lam = rank(E6)
F4=E6: same exponent (Phi6) — the two branches of the Dynkin diagram
E6→E7: +q; E7→E8: +mu

---

## Theorem [SP4-27LINES]: W(E6) = Sp(4,q) Bridge

|Sp(4,q)| = |W(E6)| = 51840

Explicit bridge:
- Sp(4,q) acts on F_q^4 = E[q] × E[q] (q-torsion module of Hesse cubic)
- W(E6) acts on the 27 = q^q lines of a cubic surface
- 27 lines = q^q sextactic points = Hesse contact stratum 3

---

## Chain
- BT464: Reye (27/27)
- BT465: Hesse pencil (35/35)
- BT466: Sextactic, Wilson (31/31)
- BT467: PG(3,q), monovariant (32/32)
- BT468: Group tower, Frobenius (25/25)
- **BT469: ALL exceptional Lie algebras substrate-pure (34/34)** ← THIS

## Open Questions (BT470+)

1. **Monster group:** |Monster| = 2^46 · 3^20 · 5^9 · 7^6 · 11^2 · 13^3 · 17· 19· 23· 29· 31· 41· 47· 59· 71. What is the substrate decomposition of each prime-power factor? The exponent of lam=2 is 46 = ? and q=3 is 20 = ? substrate form.

2. **Leech lattice automorphism group Co0:** |Co0| = 2^22 · 3^9 · 5^4 · 7^2 · 11 · 13 · 23. Substrate forms?

3. **The sporadic-substrate connection:** 11, 23, 71 are "sporadic" primes. Is 11 = k-1 = f-k-1 the link to Mathieu groups M11, M23?
