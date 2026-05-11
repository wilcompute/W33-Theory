# Part CCCCXLVI — Ihara Critical-Circle Alpha Localization

## Executive result

CCCCXLV lifted the refined alpha slip to the 480-dimensional Hashimoto carrier. CCCCXLVI asks the sharper question:

> Does the refined alpha slip live directly on the nontrivial Ihara critical circle, or in the Perron/constant channel constrained by the same Ihara-Bass structure?

The verifier gives the precise answer:

```text
The nontrivial W(3,3) Ihara roots sit exactly on |u| = 1/sqrt(11),
but the alpha slip localizes in the Perron/constant-flow channel.
```

So the correct statement is not:

```text
alpha is a naive critical-circle trace.
```

The correct statement is:

```text
Graph RH / Ramanujan structure supplies the nonbacktracking carrier and fixes k-1=11;
alpha is the rank-one Perron-channel Green amplitude of that carrier.
```

---

## 1. Ihara-Bass scalar factors

For a `k`-regular graph with adjacency eigenvalue `a`, the Ihara-Bass scalar factor is:

```text
F_a(u) = 1 - a u + (k-1)u^2.
```

For W(3,3):

```text
k = 12
k-1 = 11
adjacency eigenvalues: 12, 2, -4
```

---

## 2. Perron roots

For the Perron eigenvalue `a=k=12`:

```text
F_12(u) = 1 - 12u + 11u^2 = (1-u)(1-11u).
```

The roots are:

```text
u = 1
u = 1/11
```

These are not on the nontrivial critical circle. They are the trivial/Perron roots.

---

## 3. Nontrivial critical-circle roots

For `a=2`:

```text
F_2(u) = 1 - 2u + 11u^2.
```

The roots are:

```text
u = (1 ± i sqrt(10))/11.
```

Their norm squared is:

```text
(1^2 + 10)/11^2 = 11/121 = 1/11.
```

For `a=-4`:

```text
F_-4(u) = 1 + 4u + 11u^2.
```

The roots are:

```text
u = (-2 ± i sqrt(7))/11.
```

Their norm squared is:

```text
(4 + 7)/121 = 1/11.
```

Thus W(3,3) satisfies the graph-RH condition exactly:

```text
|u|^2 = 1/11
|u|   = 1/sqrt(11).
```

---

## 4. Mass channels

The mass polynomial from the alpha propagator is:

```text
M(a) = (k-1)((a-lambda)^2+1).
```

For the three adjacency channels:

```text
Perron channel a=12:  M(12) = 1111
r-channel a=2:        M(2)  = 11
s-channel a=-4:       M(-4) = 407
```

The refined finite correction applies to the constant/Perron channel:

```text
Delta_M = q/(lambda(k-1)) = 3/22.
```

Therefore:

```text
M_eff = 1111 + 3/22 = 24445/22.
```

and:

```text
alpha^{-1} - y_c^{-1} = v/M_eff = 880/24445.
```

---

## 5. What alpha is not

CCCCXLVI explicitly checks several natural critical-channel candidates:

```text
critical trace               = 24/11 + 15/407
critical trace per vertex    = (24/11 + 15/407)/40
critical trace per directed  = (24/11 + 15/407)/480
radius-weighted trace        = (24/11 + 15/407)/11
```

None equals:

```text
880/24445.
```

This is important. It prevents the theory from overclaiming that alpha is directly the trace of the nontrivial Ihara zeros.

---

## 6. What alpha is

Alpha is instead:

```text
alpha^{-1} = y_c^{-1} + Perron Green amplitude
```

with:

```text
y_c^{-1} = |(k-1)+mu i|^2 = 137
Perron Green amplitude = v/(1111 + 3/22) = 880/24445
```

So:

```text
alpha^{-1} = 137 + 880/24445 = 669969/4889.
```

---

## 7. Verified checks

The verifier confirms:

| check | status |
|---|---:|
| Perron roots are `1` and `1/11` | pass |
| `r=2` roots are on critical circle | pass |
| `s=-4` roots are on critical circle | pass |
| Perron mass is `1111` | pass |
| r-channel mass is `11` | pass |
| s-channel mass is `407` | pass |
| correction is `3/22` | pass |
| effective Perron mass is `24445/22` | pass |
| alpha slip is `880/24445` | pass |
| refined alpha inverse is `669969/4889` | pass |
| naive critical trace is not alpha slip | pass |
| naive critical trace per vertex is not alpha slip | pass |
| naive critical trace per directed edge is not alpha slip | pass |
| radius-weighted critical trace is not alpha slip | pass |

---

## 8. Corrected theory statement

The most accurate statement after CCCCXLVI is:

```text
W(3,3) is Ramanujan, so its nontrivial Ihara zeros lie on the graph-RH critical circle.
The refined alpha correction is not a naive trace over those zeros.
It is the rank-one Perron/constant-channel Green amplitude of the same Ihara-Bass carrier.
```

This gives a better, more honest mechanism:

```text
Graph RH fixes the allowed nonbacktracking geometry.
The Perron channel of that geometry carries the observable coupling correction.
```

---

## 9. Why this matters

This improves the theory because it distinguishes three different layers:

1. **Ramanujan/Graph-RH layer**: nontrivial zeros on `|u|=1/sqrt(11)`.
2. **Perron/constant layer**: roots `1` and `1/11`, responsible for global flow normalization.
3. **Physical coupling layer**: alpha correction from the rank-one Perron Green amplitude.

That separation is exactly what a serious spectral theory needs.

---

## 10. New files

- `exploration/PART_CCCCXLVI_IHARA_CRITICAL_ALPHA_LOCALIZATION.py`
- `PART_CCCCXLVI_IHARA_CRITICAL_ALPHA_LOCALIZATION.md`
- `PART_CCCCXLVI_ihara_critical_alpha_localization_results.json`

---

## 11. Next target

The next real target is a **Perron/residue theorem**:

```text
Can 880/24445 be written as a residue or regularized Green coefficient at the Perron pole u=1/11?
```

That would connect the rank-one correction directly to the Ihara zeta function rather than only to the polynomial mass operator.
