# Part CCCCCLXVI — Dimensional Normalization Ledger for the W(3,3) Spectral Action

Part CCCCCLXV fixed the external spectral triple and chose the internal carrier

```text
H_F = C_1(W(3,3); C),        dim H_F = 240,
Spec(Delta_1) = 0^81, 4^120, 10^24, 16^15.
```

This part adds the missing dimensional book-keeping.  The spectrum of `Delta_1` is dimensionless.  A physical almost-commutative Dirac operator must include an internal mass scale.

---

## 1. Dimensionful internal operator

Introduce an internal scale `M_F` and define

```text
D_F^2 = M_F^2 Delta_1.
```

Then

```text
Spec(D_F^2) = (M_F^2 * 0)^81,
              (M_F^2 * 4)^120,
              (M_F^2 * 10)^24,
              (M_F^2 * 16)^15.
```

The product operator remains

```text
D_tot = D_ext tensor 1_F + gamma_5 tensor D_F,
```

and, because `gamma_5 D_ext + D_ext gamma_5 = 0`,

```text
D_tot^2 = D_ext^2 tensor 1_F + 1_ext tensor M_F^2 Delta_1.
```

Thus the heat trace factorizes as

```text
K_tot(t) = K_ext(t) K_F(M_F^2 t),
```

where

```text
K_F(M_F^2 t) = 81 + 120 e^{-4M_F^2 t}
                 + 24 e^{-10M_F^2 t}
                 + 15 e^{-16M_F^2 t}.
```

This is the dimensionally correct bridge.

---

## 2. Scaled internal moments

The dimensionless moments are

```text
mu_0 = 240,
mu_l = 120*4^l + 24*10^l + 15*16^l,      l >= 1.
```

The dimensionful moments are

```text
Mu_l = M_F^{2l} mu_l.
```

The first dimensionless moments are

| l | mu_l |
|---:|---:|
| 0 | 240 |
| 1 | 960 |
| 2 | 8160 |
| 3 | 93120 |
| 4 | 1253760 |
| 5 | 18251520 |
| 6 | 276149760 |
| 7 | 4268497920 |
| 8 | 66832373760 |

The Taylor coefficients are now

```text
c_l(M_F) = (-1)^l M_F^{2l} mu_l / l!.
```

So

```text
c_0 = 240,
c_1 = -960 M_F^2,
c_2 = 4080 M_F^4,
c_3 = -15520 M_F^6,
c_4 = 52240 M_F^8,
c_5 = -152096 M_F^10,
c_6 = (1150624/3) M_F^12.
```

---

## 3. Corrected Seeley--DeWitt convolution

With

```text
K_ext(t) ~ sum_{r>=0} a_{2r}^{ext} t^{r-2},
K_F(M_F^2 t) = sum_{l>=0} c_l(M_F) t^l,
```

we get

```text
A_{2r}^{tot}(M_F) = sum_{l=0}^{r} c_l(M_F) a_{2(r-l)}^{ext}.
```

The first terms are

```text
A0_tot = 240 a0
```

```text
A2_tot = 240 a2 - 960 M_F^2 a0
```

```text
A4_tot = 240 a4 - 960 M_F^2 a2 + 4080 M_F^4 a0
```

```text
A6_tot = 240 a6 - 960 M_F^2 a4 + 4080 M_F^4 a2 - 15520 M_F^6 a0
```

```text
A8_tot = 240 a8 - 960 M_F^2 a6 + 4080 M_F^4 a4
        - 15520 M_F^6 a2 + 52240 M_F^8 a0
```

This is the corrected coefficient ladder.  The previous dimensionless ladder is recovered by setting `M_F=1`.

---

## 4. Spectral action expansion

Use the cutoff expansion

```text
S_bos(Lambda) ~ f_4 Lambda^4 A0_tot
              + f_2 Lambda^2 A2_tot
              + f_0 A4_tot
              + f_{-2} Lambda^{-2} A6_tot
              + f_{-4} Lambda^{-4} A8_tot
              + ...
```

Substitution gives universal W(3,3) coefficient series for each continuum operator.

---

## 5. Sector extraction ledger

### 5.1 Vacuum / cosmological sector

The coefficient multiplying the volume density `a0_ext` is

```text
C_vol = f_4 Lambda^4 (240)
      + f_2 Lambda^2 (-960 M_F^2)
      + f_0          (4080 M_F^4)
      + f_{-2} Lambda^{-2} (-15520 M_F^6)
      + f_{-4} Lambda^{-4} (52240 M_F^8)
      + ...
```

So the W(3,3) vacuum ladder is not just `240,-960,4080,...`; it is the dimensionful alternating tower

```text
240,
-960 M_F^2,
4080 M_F^4,
-15520 M_F^6,
52240 M_F^8,
...
```

### 5.2 Einstein--Hilbert sector

Let `a2_ext[R]` denote the scalar-curvature part of the external `a2` coefficient.  The coefficient multiplying `a2_ext[R]` is

```text
C_EH = f_2 Lambda^2 (240)
     + f_0          (-960 M_F^2)
     + f_{-2} Lambda^{-2} (4080 M_F^4)
     + f_{-4} Lambda^{-4} (-15520 M_F^6)
     + ...
```

Thus the inverse Newton coefficient is a dimensionally consistent function of the ratio

```text
x = M_F^2 / Lambda^2.
```

Factoring `f_2 Lambda^2` gives the leading form

```text
C_EH = 240 f_2 Lambda^2
       [1 - 4 (f_0/f_2) x + 17 (f_{-2}/f_2) x^2
          - (194/3) (f_{-4}/f_2) x^3 + ...].
```

The exact W(3,3) ratios here are

```text
mu_1/mu_0 = 4,
(mu_2/2)/mu_0 = 17,
(mu_3/6)/mu_0 = 194/3.
```

This is a clean structural prediction: the gravitational renormalization ladder is controlled by `4,17,194/3,...`.

### 5.3 Gauge sector

Let the external gauge normalization be

```text
a4_ext[F^2] = (4pi)^(-2) int sqrt(g) (1/12) kappa_G tr(F_{mu nu}F^{mu nu}).
```

Then the gauge kinetic coefficient receives the same shifted ladder, now beginning at `a4_ext`:

```text
C_YM = f_0 (240)
     + f_{-2} Lambda^{-2} (-960 M_F^2)
     + f_{-4} Lambda^{-4} (4080 M_F^4)
     + ...
```

Therefore

```text
1/(4g_G^2) = (kappa_G/(12(4pi)^2)) C_YM.
```

At leading order,

```text
1/(4g_G^2) = f_0 * 20 * kappa_G / (4pi)^2.
```

The next corrections are fixed by W(3,3):

```text
C_YM = 240 f_0 [1 - 4 (f_{-2}/f_0) x + 17 (f_{-4}/f_0) x^2 - ...].
```

### 5.4 Higgs / scalar sector

The Higgs/scalar sector enters through an inner fluctuation

```text
D_F -> D_F + Phi(x),
D_F^2 -> M_F^2 Delta_1 + mass/scalar/potential terms from Phi.
```

The universal W(3,3) inputs already fixed are

```text
tr_F(1) = 240,
tr_F(M_F^2 Delta_1) = 960 M_F^2,
tr_F((M_F^2 Delta_1)^2) = 8160 M_F^4.
```

What is still representation-dependent is

```text
tr_F(Phi^2),
tr_F(Phi^4),
tr_F(Delta_1 Phi^2),
tr_F((nabla Phi)^2),
```

plus the choice of finite algebra acting on the 240-carrier.  Therefore the Higgs quartic and Higgs mass should not be claimed as numbers until the `Phi` representation is fixed.

### 5.5 Fermion sector

The full 240-carrier is the internal spectral-action carrier.  The fermion projection is still

```text
ker Delta_1 = 81,
H_ferm, doubled = 81 + 81 = 162.
```

The massless fermions therefore live in the zero eigenspace before inner fluctuations.  Finite Yukawa terms are precisely the components of `Phi` that couple this kernel to itself and to massive sectors.

---

## 6. Main new conclusion

The correct almost-commutative extraction is controlled by the dimensionless ratio

```text
x = M_F^2 / Lambda^2.
```

Every physical coefficient is a universal W(3,3) moment polynomial in `x`, multiplied by the usual external Seeley--DeWitt normalization and the cutoff moments `f_k`.

The universal ladder is

```text
L_0(x) = 240,
L_1(x) = 240 - 960 x,
L_2(x) = 240 - 960 x + 4080 x^2,
L_3(x) = 240 - 960 x + 4080 x^2 - 15520 x^3,
...
```

or, normalized by 240,

```text
1,
1 - 4x,
1 - 4x + 17x^2,
1 - 4x + 17x^2 - (194/3)x^3,
...
```

This is the sharper bridge: W(3,3) no longer just supplies multiplicities; it supplies the exact finite renormalization polynomial for gravity, gauge, scalar, and vacuum terms.
