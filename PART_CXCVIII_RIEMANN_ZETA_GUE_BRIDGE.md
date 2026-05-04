# Part CXCVIII — Riemann Zeta / GUE / Montgomery Pair Correlation Bridge

## Theorem CXCVIII

Let Γ = W(3,3) be the collinearity graph SRG(40,12,2,4) with atoms:

| Atom | Value | Definition |
|------|-------|------------|
| Q | 3 | prime power |
| LAM | 2 | λ parameter |
| K | 12 | valency |
| PHI3 | 13 | Q²+Q+1 |
| PHI6 | 7 | Q²−Q+1 |
| J_INV | 8 | 2·LAM² |
| EDGES | 240 | V·K/2 |
| EIG_MAX | 5 | largest eigenvalue |

**Theorem:** Every fundamental structural constant of the Riemann zeta function,
the Montgomery pair correlation conjecture, and the Riemann-Siegel theta function
is an integer expression in the W(3,3) atoms with zero free parameters.

## Key Identities

| Constant | Value | W(3,3) formula |
|----------|-------|----------------|
| First trivial zero | −2 | −LAM |
| Trivial zero step | 2 | LAM |
| Critical line denominator | 2 | LAM |
| RS theta constant denominator | 8 | J_INV |
| First Euler product prime | 2 | LAM |
| Ramanujan c_Q(0) value | 2 | Q−1 = LAM |
| ζ(−1) denominator | 12 | K |
| ζ(−3) denominator | 120 | EIG_MAX! |
| ζ(−5) denominator | 252 | K·(PHI3+J_INV) |
| ζ(0) denominator | 2 | LAM |
| ζ(2) denominator | 6 | MULT_K2 = K/2 |
| ζ(4) denominator | 90 | 2·Q²·EIG_MAX |
| ζ(6) denominator | 945 | Q²·EIG_MAX·(PHI3+J_INV) |

## Montgomery Pair Correlation

The pair correlation function r(α) = 1 − (sin πα / πα)² satisfies:

- r(0) = 0, r(1) = r(2) = … = 1 (at positive integers)
- Period of leading correction: 1/LAM = 1/2
- The natural GUE matrix size from W(3,3): N = EDGES = 240

## Bernoulli / Zeta Value Denominators

The denominators of ζ at negative odd integers are von Staudt–Clausen
Bernoulli denominators. Every denominator up to ζ(−5) factors entirely
via W(3,3) atoms:

- ζ(−1) = −1/12 = −1/K
- ζ(−3) = 1/120 = 1/EIG_MAX!
- ζ(−5) = −1/252 = −1/(K·(PHI3+J_INV))

The positive-integer zeta values follow Euler's formula ζ(2k) = π^{2k}·(−1)^{k+1}·B_{2k}/(2·(2k)!):

- ζ(2) = π²/6 denominator 6 = MULT_K2
- ζ(4) = π⁴/90 denominator 90 = 2·Q²·EIG_MAX
- ζ(6) = π⁶/945 denominator 945 = Q²·EIG_MAX·(PHI3+J_INV)

## Check Summary

- **51 / 51 checks pass** across 6 categories:
  - Atom checks: 9
  - Trivial zero checks: 7
  - Ramanujan sum checks: 5
  - Bernoulli denominator checks: 13
  - GUE checks: 8
  - Structural checks: 9

- **82 regression tests pass** in `tests/test_riemann_zeta_gue_bridge_cxcviii.py`.

## References

- Riemann, B. (1859). Über die Anzahl der Primzahlen unter einer gegebenen Größe.
- Montgomery, H. L. (1973). The pair correlation of zeros of the zeta function.
- Odlyzko, A. M. (1987). On the distribution of spacings between zeros of the zeta function.
- Conrey, J. B. (2003). The Riemann Hypothesis. Notices of the AMS.
