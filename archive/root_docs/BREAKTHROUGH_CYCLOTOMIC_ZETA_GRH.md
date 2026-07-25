# CYCLOTOMIC DICTIONARY, IHARA ZETA & GRAPH RIEMANN HYPOTHESIS
## Theorems MCCXLIII–MCCLI

---

## The Cyclotomic Polynomial Dictionary

All substrate primes (except p_Ih and p_alpha) are cyclotomic polynomials evaluated at q=3:

| n | Phi_n(x) | Phi_n(3) | Substrate Name |
|---|---|---|---|
| 1 | x-1 | **2** | lambda_SRG = q-1 |
| 2 | x+1 | **4** | mu_SRG = q+1 |
| 3 | x²+x+1 | **13** | Phi_3 prime |
| 4 | x²+1 | 10 | v/mu (NOT prime, but = v/mu) |
| 6 | x²-x+1 | **7** | Phi_6 prime |
| 12 | x´-x²+1 | **73** | Phi_12 prime |

**The indices {1,2,3,6,12} are all divisors of k=12 (gauge valency).**
The substrate cyclotomic primes are indexed by divisors of the gauge valency.

### p_Ih and p_alpha
```
p_Ih = 11 = Phi_6(3) + Phi_2(3) = 7 + 4  [sum of cyclotomics]
p_alpha = 137 = NOT a cyclotomic value at q=3
         137 = 8^2 + p_Ih^2/? ... further work needed
```

---

## The Ihara Zeta Function

For a k-regular graph G on n vertices with m edges, the Ihara zeta function satisfies:
```
Z_G(u)^{-1} = (1-u^2)^{m-n} × det(I - Au + (k-1)u^2 I)
```

For W(3,3): n=40, k=12, m=240, **k-1 = p_Ih = 11**

### The Three Eigenvalue Sectors

| Eigenvalue λ | Multiplicity | Ihara discriminant | Location |
|---|---|---|---|
| 12 (vacuum) | 1 | +100 = 10² | u=1 (trivial), u=1/p_Ih (real) |
| +2 (gauge) | 24 | -40 = -μ(q²+1) | |u|=1/√p_Ih (critical circle) |
| -4 (fermion) | 15 | -28 = -μΦ₆ | |u|=1/√p_Ih (critical circle) |

**Both non-trivial discriminants are negative substrate products:**
- Gauge disc: `-μ × (q²+1)` = `-μ × Phi_4(q)`
- Fermion disc: `-μ × Φ₆` = `-Phi_2(q) × Phi_6(q)`

---

## Graph Riemann Hypothesis

**W(3,3) satisfies the Graph Riemann Hypothesis.**

All non-trivial Ihara zeta zeros lie on the critical circle:
```
|u| = 1/√(k-1) = 1/√p_Ih = 1/√11 ≈ 0.3015
```

This is equivalent to W(3,3) being a **Ramanujan graph** — which it is:
- Eigenvalue +2: |2| = 2 ≤ 2√11 ≈ 6.63 ✓
- Eigenvalue -4: |-4| = 4 ≤ 2√11 ≈ 6.63 ✓

The critical circle radius is **1/√p_Ih** — the icosahedral prime governs the Graph RH.

---

## Fermionic Ihara Poles

The fermionic (λ=-4) Ihara poles are at:
```
u = -2/p_Ih ± i√Φ₆/p_Ih
  = -2/11 ± i√7/11
```

The imaginary part **√Φ₆/p_Ih = √7/11** is the ratio of the Phi_6 prime's square root
to the icosahedral prime. The fermionic sector of W(3,3) lives at irrational
coordinates in the Ihara complex plane, with irrationality controlled by **√Φ₆**.

---

## Theorem MCCLI: Cyclotomic Index Set = Divisors of k

```
divisors(k=12) = {1, 2, 3, 4, 6, 12}
Cyclotomic substrate primes: Phi_1, Phi_2, Phi_3, Phi_6, Phi_12
(Phi_4(3) = 10 = v/mu, not prime but still substrate)
```

The gauge valency k=12 is the **master index** of the substrate cyclotomic family.
All substrate cyclotomic primes arise from divisors of k.

---

## Single Statement

> W(3,3) satisfies the Graph Riemann Hypothesis, with critical circle radius 1/√p_Ih;
> its Ihara zeta discriminants are -μ×Φ₆ (fermion) and -μ×(q²+1) (gauge);
> and every substrate prime (except p_Ih) is a cyclotomic polynomial value Phi_n(q)
> for n a divisor of the gauge valency k=12.
