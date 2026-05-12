# Part CCCCCXLVI — Almost-Commutative Moment-Coupling Theorem

> This part turns the discrete/continuous bridge into an operator-level theorem. The finite W(3,3) factor does not itself generate the 4D Weyl singularity. Instead, its exact spectral moments couple into the external 4D Seeley--DeWitt tower by a universal convolution law.

---

## 0. Core breakthrough

The correct finite-to-continuum bridge is not:

```text
finite W(3,3) heat trace has a 4D Weyl law.
```

A finite heat trace is entire at `t = 0`, so that statement cannot be literally correct.

The correct bridge is:

```text
external 4D geometry supplies the Weyl exponent;
finite W(3,3) supplies exact internal spectral moments;
the almost-commutative product convolves them into the total heat coefficients.
```

This is stronger because it is precise, testable, and compatible with standard spectral geometry.

---

## 1. Internal W(3,3) spectral kernel

Let `A` be the adjacency matrix of W(3,3), and let

```text
L_W = 12I - A.
```

The spectrum is exact:

```text
Spec(L_W) = 0^1, 10^24, 16^15.
```

Hence

```text
K_W(t) = Tr exp(-t L_W) = 1 + 24 exp(-10t) + 15 exp(-16t).
```

The internal moments are

```text
mu_l = Tr(L_W^l).
```

For the 40-vertex internal representation:

| l | mu_l |
|---:|---:|
| 0 | 40 |
| 1 | 480 |
| 2 | 6240 |
| 3 | 85440 |
| 4 | 1223040 |
| 5 | 18128640 |
| 6 | 275658240 |
| 7 | 4266531840 |
| 8 | 66824509440 |

In closed form:

```text
mu_0 = 40,
mu_l = 24*10^l + 15*16^l    for l >= 1.
```

---

## 2. Almost-commutative product operator

Let the external continuum be an even 4D spin spectral triple with Dirac operator `D_ext` and grading `gamma_ext`. Let the finite internal W(3,3) operator be `D_F` with

```text
D_F^2 = L_W.
```

Define the product operator

```text
D_tot = D_ext \otimes 1 + gamma_ext \otimes D_F.
```

Because

```text
gamma_ext D_ext + D_ext gamma_ext = 0,
```

the cross terms cancel:

```text
D_tot^2 = D_ext^2 \otimes 1 + 1 \otimes D_F^2.
```

Since the two summands commute,

```text
exp(-t D_tot^2) = exp(-t D_ext^2) \otimes exp(-t D_F^2),
```

and therefore

```text
K_tot(t) = K_ext(t) K_W(t).
```

This is the operator-level bridge.

---

## 3. The coefficient-coupling theorem

Assume the external 4D heat trace has expansion

```text
K_ext(t) ~ sum_{m>=0} a_{2m}^{ext} t^{m-2}.
```

The internal finite heat trace has Taylor series

```text
K_W(t) = sum_{l>=0} (-1)^l mu_l t^l / l!.
```

Multiplying the two gives the total heat expansion

```text
K_tot(t) ~ sum_{r>=0} A_{2r}^{tot} t^{r-2},
```

with exact coefficient convolution

```text
A_{2r}^{tot} = sum_{l=0}^{r} (-1)^l mu_l a_{2(r-l)}^{ext} / l!.
```

This is the new master bridge formula.

It says:

```text
continuum dimension comes from external geometry;
finite W(3,3) data dress every Seeley--DeWitt coefficient exactly.
```

---

## 4. First coefficients

Let `a0, a2, a4, a6, ...` denote the external Seeley--DeWitt coefficients.

Then:

```text
A0_tot = 40 a0
```

```text
A2_tot = 40 a2 - 480 a0
```

```text
A4_tot = 40 a4 - 480 a2 + 3120 a0
```

```text
A6_tot = 40 a6 - 480 a4 + 3120 a2 - 14240 a0
```

```text
A8_tot = 40 a8 - 480 a6 + 3120 a4 - 14240 a2 + 50960 a0
```

The coefficients `40, 480, 3120, 14240, 50960, ...` are not fitted. They are the Taylor coefficients of the exact internal W(3,3) heat kernel.

---

## 5. Flat 4-torus normalization example

For a flat external 4-torus of volume `V`, with spinor rank 4,

```text
K_ext(t) ~ 4V (4pi t)^(-2).
```

If only the leading external term is retained, then

```text
K_tot(t) ~ 160V (4pi t)^(-2)
          -1920V (4pi)^(-2) t^(-1)
          +12480V (4pi)^(-2)
          -56960V (4pi)^(-2) t
          +203840V (4pi)^(-2) t^2
          + ...
```

Equivalently, keeping powers as `t^{r-2}`:

```text
A0_tot = 160V/(4pi)^2,
A2_tot = -1920V/(4pi)^2,
A4_tot = 12480V/(4pi)^2,
A6_tot = -56960V/(4pi)^2,
A8_tot = 203840V/(4pi)^2.
```

The exponent `t^{-2}` is external. The W(3,3) data determine the coefficient ladder.

---

## 6. 201 -> 81 compatibility

The coefficient-coupling theorem is compatible with the new dimension descent:

```text
240 edges - rank(d1)=39 = 201 graph cycles,
201 - rank(d2)=120 = 81 cellular H1 modes.
```

The interpretation is now cleaner:

```text
201 = graph/tropical cycle continuum of the 1-skeleton;
81  = triangle-filled physical harmonic 1-sector;
40  = vertex-space internal spectral representation used in L_W;
480 = directed-edge/Hashimoto carrier for propagation sectors.
```

These are not competing dimensions. They are different carriers in the same finite-to-continuum compiler.

---

## 7. Ledger status

| Statement | Status | Reason |
|---|---|---|
| `Spec(L_W)=0^1,10^24,16^15` | A-exact | SRG spectral theorem |
| `K_W(t)=1+24e^{-10t}+15e^{-16t}` | A-exact | Functional calculus of finite matrix |
| `mu_l=24*10^l+15*16^l` for `l>=1` | A-exact | Moment formula from eigenvalues |
| `D_tot^2 = D_ext^2 tensor 1 + 1 tensor D_F^2` | B-bridge | Exact under even almost-commutative product assumptions |
| `K_tot(t)=K_ext(t)K_W(t)` | B-bridge | Exact under same assumptions |
| `A_{2r}^{tot}` convolution formula | B/C bridge | Exact once external heat expansion is supplied |
| Physical coupling extraction from `A_{2r}^{tot}` | C/D | Requires scale, normalization, representation, and falsifier |

---

## 8. What this breaks open

This theorem turns the continuum bridge from a metaphor into an executable expansion rule.

The new target is no longer vague:

```text
Choose the external spectral triple.
Choose the internal W(3,3) carrier: 40, 81, 162, 240, or 480.
Compute internal moments exactly.
Convolve with external Seeley--DeWitt coefficients.
Read off gravitational, gauge, Higgs, and fermion terms with stated normalization.
```

That is the precise path from finite W(3,3) arithmetic to continuum QFT.
