# PARTS MCD–MCDV: Fifth Root of Unity, Q(ζ₅), and W(3,3)

## Background: The Paper

Amaral et al., *"Quantum Gravity at the Fifth Root of Unity"* (arXiv:1903.10851,
SciPost Phys. 2021) considers spin foam models with deformation parameter
q = e^{2πi/5}, a complex fifth root of unity.

At this value, SU(2)_q has exactly **4 unitary irreps** (spin 0, 1/2, 1, 3/2)
with quantum dimensions **1, φ, φ, 1** where φ = (1+√5)/2 is the golden ratio.

---

## MCD: p_Ih = √Φ₅(q)

The 5th cyclotomic polynomial evaluated at q = 3:

```
Φ₅(3) = 3⁴ + 3³ + 3² + 3 + 1 = 81 + 27 + 9 + 3 + 1 = 121 = 11² = p_Ih²
```

Therefore:
```
p_Ih = √Φ₅(q)
```

**The icosahedral prime is the square root of the 5th cyclotomic polynomial evaluated at the field size.**

This has a norm interpretation: Φ₅(3) = N_{Q(ζ₅)/Q}(3 − ζ₅), the algebraic
norm of (3 − ζ₅) in the 5th cyclotomic field.

---

## MCDI: All Major Constants are Cyclotomic Values at q

| Cyclotomic polynomial | Value at q=3 | W(3,3) constant |
|---|---|---|
| Φ₁(3) = 3−1 | **2** | q−1 (small eigenvalue r) |
| Φ₂(3) = 3+1 | **4** | **χ = q+1** |
| Φ₃(3) = 3²+3+1 | **13** | Φ₃ (the 13-prime) |
| **Φ₄(3) = 3²+1** | **10** | **E₁** |
| **Φ₅(3) = 3⁴+…+1** | **121 = p_Ih²** | **p_Ih²** |
| **Φ₆(3) = 3²−3+1** | **7** | **Φ₆ = 7** |

The Laplacian eigenvalue E₁, the Euler characteristic χ, and the substrate
prime Φ₆ are **literally cyclotomic polynomial values** at q.

---

## MCDII: [Q(ζ₅) : Q] = χ

The degree of the 5th cyclotomic field over Q:
```
[Q(ζ₅) : Q] = φ(5) = 4 = χ(W(3,3))
```

The Galois group Gal(Q(ζ₅)/Q) ≅ (ℤ/5ℤ)* has order **4 = χ**.

The field tower:
```
Q ⊂ Q(√5) ⊂ Q(ζ₅)
```
- Q(√5) is the **real subfield**, containing φ = (1+√5)/2
- [Q(√5):Q] = 2 = q−1
- [Q(ζ₅):Q(√5)] = 2 = q−1

The norm N_{Q(√5)/Q}(3−φ) = (3−φ)(3−φ') = **5**, the prime at the center
of Q(√5). So q=3 is at algebraic distance 5 from the golden ratio.

---

## MCDIII: D²(SU(2)_{ζ₅}) = χ + 2φ

The total quantum dimension squared of the ζ₅ spin foam:
```
D² = Σ d(j)² = 1² + φ² + φ² + 1² = 2 + 2φ² = 2 + 2(φ+1) = 4 + 2φ = χ + 2φ
```

Since φ² = φ+1 (golden ratio identity), and χ = 4 = q+1.

---

## MCDIV: The Central Identity D² · √5 = E₁ · φ

```
D² · √5 = (4 + 2φ)·√5 = 4√5 + 2φ√5 = 4√5 + (√5 + 5) = 5√5 + 5 = 5(1+√5) = 10φ = E₁·φ
```

Therefore:

$$\boxed{D^2(\mathrm{SU}(2)_{\zeta_5}) \cdot \sqrt{5} = E_1(W(3,3)) \cdot \varphi}$$

Numerically: 7.2361 × 2.2361 = 10 × 1.6180 = **16.1803** ✓

This is the **central identity** linking:
- The total quantum dimension of the fifth-root-of-unity spin foam
- The first Laplacian eigenvalue of W(3,3)
- The golden ratio

Equivalently: **D² = E₁·φ/√5**, and φ/√5 = lim F(n)/F(n+1) (Binet denominator).

---

## MCDV: The Fibonacci Convergent Chain

The ratios of successive W(3,3) constants form the **Fibonacci convergents to φ**:

| Ratio | Value | Fibonacci form |
|---|---|---|
| g₂/χ | 6/4 = **3/2** | F(4)/F(3) |
| E₁/g₂ | 10/6 = **5/3** | F(5)/F(4) |
| E₂/E₁ | 16/10 = **8/5** | F(6)/F(5) |
| → | → | → **φ** (limit) |

The sequence 3/2 → 5/3 → 8/5 → … → φ is exactly the **Fibonacci rational
approximants** to the golden ratio. The three core energy constants (g₂, E₁, E₂)
from the super-axiom chain are spaced by **consecutive Fibonacci denominators**.

This chain terminates at F(6)/F(5) = 8/5 because:
- E₂ = 16 = 2·F(6) = 2·8 is the last Fibonacci-indexed constant
- The next ratio g₁/E₂ = 21/16 breaks the pattern (21 = F(8), not F(7))
- F(7) = 13 does not appear in W(3,3)'s constant table — it is **skipped**

---

## Complete Q(ζ₅) ↔ W(3,3) Dictionary

| Quantity | Q(ζ₅) spin foam | W(3,3) | Value |
|---|---|---|---|
| [Q(ζ₅):Q] | 4 | χ = q+1 | 4 |
| \|Gal\| | 4 | χ | 4 |
| # unitary irreps | 4 | # eigenspaces+1 | 4 |
| Quantum dim spin-½ | φ | m_r/m_s ≈ φ | 8/5 (Fib approx) |
| Total D² | 4+2φ | χ+2φ | 7.236 |
| D²·√5 | 16.180 | E₁·φ | 16.180 |
| N(3−φ) | 5 | F(5) = resonance index | 5 |
| Φ₅(3) = N(3−ζ₅) | 121 | p_Ih² | 121 |
| Resonance index | F(5) = 5 | q+2 = 5 | 5 |
| χ(Hilb^{q+2}) | C(10,5)=252 | central binomial | 252 |

---

## The Algebraic Meaning

The field Q(ζ₅) is the **minimal field containing all fifth roots of unity**.
Its subfield Q(√5) contains φ. The prime 5 is the **ramified prime** of
Q(√5)/Q, and 11 is an **inert prime** (Φ₅(3) = 121 = 11² reflects the
fact that 11 ramifies or splits in a specific way in Z[ζ₅]).

The icosahedral symmetry group I ≅ A₅ has order 60 = 4·15 = χ·m_s, and
its double cover 2I has order 120 = 5! = (q+2)! — another instance of the
resonance index q+2 = 5 appearing in the icosahedral context.

All of this traces back to the unique fact that q = 3 satisfies:
- q! = 2q (factorial axiom)
- q+2 = F(5) (Fibonacci resonance)
- Φ₅(q) = p_Ih² (cyclotomic/icosahedral identity)
- [Q(ζ₅):Q] = q+1 = χ (field degree = Euler characteristic)
