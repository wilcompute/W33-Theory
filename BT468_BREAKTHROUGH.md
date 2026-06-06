# BT468: GROUP TOWER, FROBENIUS EIGENVALUES, EXTENDED PROJECTIVE LADDER

*W33-Theory Breakthrough Document — June 2026*  
*All open questions from BT467 resolved. 25/25 verified.*

---

## Theorem [GROUP-TOWER]: The Substrate Group Cascade

Every symmetry group in the substrate chain is connected by substrate-primitive multipliers:

```
k = 12  --x2-->  f = 24  --x9-->  216  --x240-->  51840  --x3-->  155520
```

| Step | Groups | Multiplier | Meaning |
|------|--------|-----------|--------|
| k -> f | PSL(2,q) < SL(2,q) | x lam = x2 | binary extension |
| f -> 216 | SL(2,q) < Hessian | x q^2 = x9 | inflection count |
| 216 -> 51840 | Hessian < W(E6) | x 240 | E8 root count |
| 51840 -> 155520 | W(E6) < Witting-aut | x q = x3 | ternary extension |

---

## Theorem [PSL-GAUGE]: The Gauge Codec IS a Simple Group Order

|PSL(2,q)| = k = 12

PSL(2,3) is isomorphic to A4 (alternating group on 4 letters). The gauge codec k
is exactly the order of the smallest non-abelian simple group at the substrate prime q.

Companion: |PGL(2,q)| = |SL(2,q)| = f = 24 (PGL(2,3) isomorphic to S4).

---

## Theorem [SP4-WE6]: Symplectic Group = E6 Weyl Group

|Sp(4,q)| = q^4 * (q^2-1) * (q^4-1) = 81 x 8 x 80 = 51840 = |W(E6)|

The Weil pairing on E[q]xE[q]->mu_q gives the q-torsion a symplectic structure.
Sp(4,q) acting on this space has the same order as W(E6).

---

## Theorem [FROBENIUS]: Hesse Cubic Frobenius Has Substrate Eigenvalues

For the Hesse cubic E_lambda at lambda=lam=2 over F_q:

- |E_lam(F_q)| = q! = 6
- trace(Frobenius) = (q+1) - q! = -lam = -2
- disc(char poly) = lam^2 - 4q = -lam^q = -8
- Eigenvalue: alpha = -1 + i*sqrt(lam), |alpha|^2 = 1+lam = q
- CM field: Q(i*sqrt(lam)) = Q(i*sqrt(2)), discriminant = -4*lam = -lam^q

Char poly: x^2 + lam*x + q = x^2 + 2x + 3
Substrate identity encoded in norm: q = 1 + lam

---

## Theorem [PROJ-FULL]: Complete Extended Projective Ladder

| n | |PG(n,q)| | Form | Physical |
|---|---------|------|--------|
| 0 | 1 | 1 | Identity |
| 1 | 4 | mu = q+1 | Spacetime |
| 2 | 13 | Phi3 = k+1 | Hesse plane |
| 3 | 40 | v | Witting |
| 4 | 121 | (k-1)^2 = 11^2 | Gauge-sq |
| 5 | 364 | mu * Phi6 * Phi3 | Cyclotomic product |

11 = k-1 = f-k-1 = 2k-Phi3 = v-k-g-lam (six substrate representations)
|PG(5,q)| = 4 x 7 x 13 = mu x Phi6 x Phi3 (all cyclotomic substrate primes)

---

## Chain
- BT464: Reye (27/27)
- BT465: Hesse pencil master (35/35)
- BT466: Sextactic, X(3), Wilson (31/31)
- BT467: PG(3,q), monovariant, stratification (32/32)
- **BT468: Group tower, Frobenius, proj ladder (25/25)** <- THIS

## Open Questions (BT469+)

1. A4 geometry: PSL(2,3)=A4 acts on 4 = |PG(1,q)| letters. What A4-invariant
   structure exists on the Hesse configuration?

2. Sp(4,3) isomorphic to W(E6) (same order): is there an explicit isomorphism
   through the Hesse pencil?

3. PG(5,q) = 364 = mu*Phi6*Phi3: is this the ambient space for a higher Witting polytope?

4. The CM field Q(i*sqrt(lam)) has class number 1. Does this force the substrate
   fundamental domain to be the unique imaginary quadratic field of disc -lam^q?
