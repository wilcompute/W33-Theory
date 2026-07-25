# BREAKTHROUGH 413-420
## Electroweak Crossing Lattice, Threshold Reciprocity, and Low-Energy Alpha Closure

### BT413 — THE PAIRWISE CROSSING LATTICE

BT387's literal one-loop script does not close alpha. The correct positive
result is sharper: the observed one-loop pairwise crossing scales form a
near-substrate ladder, and the W33 seesaw scale lands at the substrate-weighted
center of the first two crossings.

Using GUT-normalized U(1), SU(2), and SU(3) couplings at M_Z:

| Crossing | Scale |
|---|---:|
| M12: alpha1 = alpha2 | 1.245073e13 GeV |
| M13: alpha1 = alpha3 | 3.126086e14 GeV |
| M23: alpha2 = alpha3 | 1.407818e17 GeV |

The ratios are substrate-clean to sub-percent accuracy:

| Ratio | Value | Substrate target | Error |
|---|---:|---:|---:|
| M13/M12 | 25.107656 | F5^2 = 25 | 0.43% |
| M23/M13 | 450.345265 | (f - q!) F5^2 = 18*25 = 450 | 0.077% |
| M23/M12 | 11307.113884 | 11250 | 0.508% |

The W33 scale is not a triple unification point. It is the weighted geometric
center:

```text
sqrt(M12*M13) = 6.238753e13 GeV
M_W33 / sqrt(M12*M13) = 0.801442
mu/F5 = 4/5 = 0.800000
(mu/F5)*sqrt(M12*M13) = 4.991002e13 GeV
```

So:

```text
M_W33 ~= (mu/F5) * sqrt(M12*M13)
```

with 0.1803% error. The remaining electroweak proof target is therefore not
"find another alpha identity"; it is derive the finite W33 threshold vector at
this scale.

At M_W33, the one-loop inverse couplings are:

```text
alpha1^-1 = 41.819335
alpha2^-1 = 43.427188
alpha3^-1 = 38.581247
spread = 4.845942
```

No triple unification is claimed.

---

### BT414 — THRESHOLD RECIPROCITY AND THE HIGGS QUARTIC

BT414 supplies the scalar-side mirror of the BT413 gauge-side placement.

Gauge side:

```text
M_W33 / sqrt(M12*M13) ~= mu/F5 = 4/5
```

Scalar side:

```text
lambda_H(seed) = 1/v(W33) = 1/40
lambda_H(EW) = F5/40 = 5/40 = 1/8 = 2^-q
```

Then the Higgs mass relation gives:

```text
m_H = sqrt(2*lambda_H) * v_H
    = sqrt(2*(1/8)) * v_H
    = v_H / 2
    = 123.109820 GeV
```

Compared with m_H = 125.25 GeV, this is a 1.7087% mass error. The Higgs quartic
itself is:

```text
lambda_H(pred) = 0.125000
lambda_H(obs)  = 0.129384
error = 3.3883%
```

The exact reciprocity identity is:

```text
(gauge scale weight) * (scalar quartic lift)
  = (mu/F5) * F5
  = mu
  = 4
```

This is the new bridge target: derive one W33 threshold mechanism that both
lowers the gauge crossing center by 4/5 and raises the scalar vertex coupling
by 5, producing the four-dimensional spacetime factor.

### Status

BT413 and BT414 are executable and verified. They do not close alpha, and they
do not derive the Higgs VEV. They replace the overclaimed BT387 alpha result
with a precise threshold problem:

```text
W33 finite threshold vector at M_W33
  -> alpha/theta normalization
  -> Higgs quartic lift
  -> four-dimensional reciprocity
```

---

### BT415 — THE TRACE-ZERO THRESHOLD VECTOR

BT415 extracts the actual electroweak threshold direction. At the W33 scale,
the centered inverse-coupling vector is:

```text
(alpha1^-1, alpha2^-1, alpha3^-1) - mean
  = (0.543411755, 2.151264963, -2.694676718)
```

This is within 0.1714% of the substrate trace-zero direction:

```text
(1, mu, -F5) = (1, 4, -5)
```

Solving for exact collinearity gives:

```text
M_trace = 5.027507e13 GeV
M_trace / M_W33 = 1.005501317
c = 0.538066062092
exp(q!*c) = 25.239150307 ~= F5^2 = 25
```

The scale is only 0.5501% above W33, and the amplitude is within 0.9566% of
the same F5^2 ladder found in BT413.

---

### BT416 — QUTRIT-SHEET CARRIER OF THE VECTOR

BT416 derives the vector from the finite selector stack:

```text
selected qutrit phase sheet + boundary lines - closure
  = 1 + 4 - 5
  = (1, mu, -F5)
```

The support arithmetic is exact:

```text
selected sheet supports = 108 = mu*q^3
ordered failures        = 864 = mu*q^3*2^q
incident sheets/support = 8   = mu*lambda = 2^q
selected Z20 edges      = 54  = lambda*q^3
active cross pairs      = 4   = mu
inactive same-side pairs= 2   = lambda
```

So the threshold vector is not a fitted direction. It is the closure ledger of
the self-entangled qutrit correction mechanism.

---

### BT417 — LORENTZ-DISTRIBUTED CLOSURE AMPLITUDE

BT417 tests the coefficient:

```text
c0 = log(F5^2) / q!
   = log(25) / 6
   = 0.536479304145
```

Interpretation: the fivefold closure is squared into 25 closure states and
distributed over the six Lorentz bivectors.

Comparison:

```text
BT415 exact-trace c = 0.538066062092  error = 0.2958%
W33-scale c         = 0.538615599904  error = 0.3982%
```

---

### BT418 — FINITE ELECTROWEAK BOUNDARY PREDICTION

BT418 uses only finite W33 boundary data:

```text
mean inverse coupling = q*k + F5 = 41
threshold direction   = (1, mu, -F5)
coefficient           = log(F5^2)/q!
scale                 = M_W33 = 5e13 GeV
```

Running this boundary down to M_Z gives:

| Observable | Prediction | Repo target | Error |
|---|---:|---:|---:|
| alpha_em^-1(M_Z) | 128.147302 | 128.900000 | 0.5839% |
| sin^2(theta_W) | 0.230383209 | 0.231220000 | 0.3619% |
| alpha_s(M_Z) | 0.121895367 | 0.118100000 | 3.2137% |

No observed couplings are used as high-scale boundary inputs.

---

### BT419-BT420 — LOW-ENERGY ALPHA CLOSURE

BT419 adds the finite low-energy threshold:

```text
Delta alpha^-1(M_Z -> 0)
  = lambda^mu * F5 / q^2
  = 16*5/9
  = 80/9
```

Then:

```text
alpha^-1(0)
  = 128.147302195 + 8.888888889
  = 137.036191084
```

Against the repo target 137.036, the absolute error is 0.000191084 and the
relative error is 0.000139%.

BT420 identifies the 80/9 carrier:

```text
16 = lambda^mu  = BT385 line stabilizers in common
5  = F5         = BT416 qutrit-sheet closure
9  = q^2        = color-generation averaging grid
```

The remaining open work is the continuum interpretation: realize this finite
80/9 carrier as the actual charged-sector M_Z-to-zero decoupling operator.
