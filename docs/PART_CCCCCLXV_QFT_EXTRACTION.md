# Part CCCCCLXV — Choosing the Spectral Triple and Extracting QFT Sectors

> This part executes the four-step prescription: choose the external spectral triple, choose the W(3,3) internal carrier, compute exact internal moments, convolve with external Seeley--DeWitt coefficients, and identify the gravity/gauge/Higgs/fermion sectors with explicit normalization conventions.

---

## 0. Choice summary

### External spectral triple

We choose the standard compact Euclidean 4D spin spectral triple with gauge and scalar inner fluctuations:

```text
A_ext = C^infty(M)
H_ext = L^2(M,S)
D_ext = D_M^A
```

where:

- `M` is a compact oriented 4D Riemannian spin manifold,
- `S` is the spinor bundle,
- `D_M^A = gamma^mu (nabla_mu^S + A_mu)` is the gauge-covariant Dirac operator,
- `gamma_5` is the external grading.

The external heat trace is written in the normalized form

```text
K_ext(t) ~ sum_{r>=0} a_{2r}^{ext} t^{r-2}.
```

This external factor supplies the continuum Weyl exponent `t^{-2}`.

### Internal W(3,3) carrier

We choose the **240-dimensional cellular 1-chain carrier**:

```text
H_F = C_1(W(3,3); C),       dim H_F = 240.
```

Reason: this is the smallest carrier that simultaneously contains:

```text
81  = cellular H1 zero modes / physical harmonic 1-sector,
120 = triangle-boundary / local gauge-exact sector,
24  = r=2 W(3,3) sector,
15  = s=-4 W(3,3) sector.
```

The internal operator is the cellular 1-Hodge Laplacian

```text
Delta_1 = d1^* d1 + d2 d2^*.
```

Its exact spectrum is

```text
Spec(Delta_1) = 0^81, 4^120, 10^24, 16^15.
```

This carrier is better than the 40-vertex carrier for QFT extraction because the 40-carrier sees the adjacency/Laplacian theorem kernel, but the 240-carrier sees the physical `81` H1 sector and the `120` triangle-boundary sector at the same time.

---

## 1. Product spectral triple

Let

```text
D_F^2 = Delta_1.
```

The almost-commutative product operator is

```text
D_tot = D_ext \otimes 1_F + gamma_5 \otimes D_F.
```

Since `gamma_5 D_ext + D_ext gamma_5 = 0`, the cross terms cancel:

```text
D_tot^2 = D_ext^2 \otimes 1_F + 1_ext \otimes Delta_1.
```

Therefore

```text
K_tot(t) = Tr exp(-t D_tot^2)
         = K_ext(t) K_F(t).
```

This is the operator-level discrete/continuous bridge.

---

## 2. Exact internal moments

The internal heat trace is

```text
K_F(t) = 81 + 120 e^{-4t} + 24 e^{-10t} + 15 e^{-16t}.
```

Define exact moments

```text
mu_l = Tr(Delta_1^l).
```

Then

```text
mu_0 = 240,
mu_l = 120*4^l + 24*10^l + 15*16^l,   l >= 1.
```

First moments:

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

The Taylor coefficients of `K_F(t)` are

```text
c_l = (-1)^l mu_l / l!.
```

So:

| l | c_l |
|---:|---:|
| 0 | 240 |
| 1 | -960 |
| 2 | 4080 |
| 3 | -15520 |
| 4 | 52240 |
| 5 | -152096 |
| 6 | 1150624/3 |
| 7 | -17785408/21 |
| 8 | 34808528/21 |

---

## 3. Seeley--DeWitt convolution

With

```text
K_ext(t) ~ sum_{r>=0} a_{2r}^{ext} t^{r-2},
K_F(t)   = sum_{l>=0} c_l t^l,
```

we get

```text
K_tot(t) ~ sum_{r>=0} A_{2r}^{tot} t^{r-2},
```

where

```text
A_{2r}^{tot} = sum_{l=0}^{r} c_l a_{2(r-l)}^{ext}.
```

For the 240-carrier:

```text
A0_tot = 240 a0
```

```text
A2_tot = 240 a2 - 960 a0
```

```text
A4_tot = 240 a4 - 960 a2 + 4080 a0
```

```text
A6_tot = 240 a6 - 960 a4 + 4080 a2 - 15520 a0
```

```text
A8_tot = 240 a8 - 960 a6 + 4080 a4 - 15520 a2 + 52240 a0
```

This is the exact coefficient ladder for the chosen QFT bridge.

---

## 4. Sector extraction with normalization conventions

The bosonic spectral action is written as

```text
S_bos(Lambda) = Tr f(D_tot^2 / Lambda^2)
              ~ f_4 Lambda^4 A0_tot
               + f_2 Lambda^2 A2_tot
               + f_0 A4_tot
               + f_{-2} Lambda^{-2} A6_tot
               + ...
```

The `f_k` are moments of the cutoff function `f`. The external coefficients are normalized using the Laplace-type convention

```text
P = -(g^{mu nu} nabla_mu nabla_nu + E),
```

with

```text
a0_ext = (4pi)^(-2) int_M sqrt(g) tr(1),

a2_ext = (4pi)^(-2) int_M sqrt(g) tr(E + R/6),

a4_ext = (4pi)^(-2)/360 int_M sqrt(g) tr(
  60 R E + 180 E^2 + 30 Omega_{mu nu} Omega^{mu nu}
  + (5R^2 - 2|Ric|^2 + 2|Riem|^2) 1
),
```

up to total derivatives. This convention fixes all signs and factors for the extraction ledger.

### 4.1 Cosmological / vacuum sector

The volume term receives contributions from every convolved order:

```text
S_Lambda,vol ~ int sqrt(g) [
  f_4 Lambda^4 (240 a0_unit)
+ f_2 Lambda^2 (-960 a0_unit)
+ f_0          (4080 a0_unit)
+ ...
].
```

So the internal 1-chain carrier renormalizes the vacuum coefficient by the exact ladder

```text
240, -960, 4080, -15520, 52240, ...
```

### 4.2 Einstein--Hilbert sector

Let `a2_ext[R]` denote the coefficient of the scalar-curvature term in `a2_ext`. Then the leading gravitational coefficient is

```text
S_EH ~ [f_2 Lambda^2 * 240 - f_0 * 960 + f_{-2} Lambda^{-2} * 4080 - ...] a2_ext[R].
```

Equivalently, the inverse Newton coefficient is not a single free number; it is a cutoff-weighted W(3,3) moment series.

### 4.3 Gauge sector

Assume the external Dirac operator is twisted by a gauge connection with curvature `F_{mu nu}`, and choose the convention

```text
a4_ext[F^2] = (4pi)^(-2) int sqrt(g) (1/12) kappa_G tr(F_{mu nu}F^{mu nu}).
```

Then the leading Yang--Mills kinetic coefficient is

```text
1/(4 g_G^2) = f_0 * 240 * kappa_G / (12 (4pi)^2)
            = f_0 * 20 * kappa_G / (4pi)^2.
```

Thus relative gauge coupling predictions are controlled by the representation trace normalization `kappa_G`; the W(3,3) carrier contributes the universal exact multiplicity `240`.

The carrier split suggests the sector dictionary:

```text
0^81   -> harmonic matter/generation modes,
4^120  -> gauge/local-boundary excitations,
10^24  -> r-sector heavy/GUT correction,
16^15  -> s-sector heavy/adjoint correction.
```

### 4.4 Higgs / scalar sector

Introduce a finite inner fluctuation scalar field

```text
Phi(x) in End(H_F),
D_F -> D_F + Phi(x).
```

In the external `a2` and `a4` coefficients, the scalar sector has the schematic normalized form

```text
S_H ~ int sqrt(g) tr_F(
  C_kin (nabla Phi)^2
+ C_2 Phi^2
+ C_4 Phi^4
+ C_R R Phi^2
),
```

where the constants `C_kin, C_2, C_4, C_R` are fixed once the precise Laplace-type sign convention and representation of `Phi` are selected. The W(3,3) input is exact:

```text
tr_F(1) = 240,
tr_F(Delta_1) = 960,
tr_F(Delta_1^2) = 8160.
```

So the Higgs mass/quartic extraction reduces to computing `tr_F(Phi^2)`, `tr_F(Phi^4)`, and mixed traces with `Delta_1` in the chosen internal representation. No empirical parameter should be inserted before those traces are fixed.

### 4.5 Fermionic sector

The fermionic action is

```text
S_ferm = <psi, D_tot^{A,Phi} psi>.
```

The internal carrier decomposes as

```text
H_F = ker Delta_1  direct_sum  im(d2)  direct_sum  coexact/heavy sectors
    = 81           +           120    + 24 + 15.
```

The 81 zero modes are the natural massless matter/generation carrier. If a real/chiral fermion representation is required, use the doubled carrier

```text
H_ferm = H1_cell^+ direct_sum H1_cell^- ,    dim = 162,
```

which is the fermion-only projection of the 240-sector QFT carrier. The full 240-carrier is therefore the bosonic/internal spectral carrier, while the 162-carrier is the fermionic chiral projection.

---

## 5. Why this is the current best bridge

The previous 40-vertex carrier gives the cleanest adjacency theorem kernel:

```text
Spec(12I-A) = 0^1, 10^24, 16^15.
```

But the 240-carrier gives the QFT sector kernel:

```text
Spec(Delta_1) = 0^81, 4^120, 10^24, 16^15.
```

This is the first choice that simultaneously sees:

- the physical 81-dimensional H1 sector,
- the triangle-boundary/gauge sector,
- the W(3,3) r/s heavy sectors,
- the exact discrete-to-continuum Seeley--DeWitt convolution.

So the extraction chain is now:

```text
External triple: compact 4D spin manifold with gauge connection.
Internal carrier: C1(W(3,3)), dim 240.
Internal operator: cellular 1-Hodge Laplacian Delta_1.
Moments: mu_l = 120*4^l + 24*10^l + 15*16^l.
Convolution: A_{2r}^{tot} = sum c_l a_{2(r-l)}^{ext}.
Physics: gravity/gauge/Higgs/fermions are read off from A0,A2,A4 plus the fermionic action.
```

That is the concrete QFT bridge.
