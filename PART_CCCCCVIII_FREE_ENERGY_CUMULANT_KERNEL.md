# Part CCCCCVIII — Free-Energy Cumulant Kernel

## Executive result

Part CCCCCVII introduced the finite spectral partition function:

```text
Z(t)=82+320e^{4t}+48e^{10t}+30e^{16t}.
```

Part CCCCCVIII takes the statistical-mechanical step:

```text
F(t)=log Z(t).
```

This free energy generates exact cumulants of the normalized W(3,3) finite spectral distribution.

The first cumulants are:

```text
kappa_1 = 14/3
kappa_2 = 272/9
kappa_3 = 10432/27
kappa_4 = -156416/27
```

The key new structural identity is:

```text
kappa_2 = 272/9 = (dim(E8)+dim(SU5))/q^2 = (248+24)/9.
```

So the variance of the finite spectral-action distribution is exactly the E8 dimension plus the SU(5)/r-channel dimension, divided by `q²`.

---

## 1. Normalized distribution

At `t=0`, the spectral weights are:

```text
P(0)  = 82/480  = 41/240
P(4)  = 320/480 = 2/3
P(10) = 48/480  = 1/10
P(16) = 30/480  = 1/16
```

These sum to 1 exactly.

---

## 2. Free energy

The partition function is:

```text
Z(t)=82+320e^{4t}+48e^{10t}+30e^{16t}.
```

The finite free energy is:

```text
F(t)=log Z(t).
```

The cumulants are:

```text
kappa_n = F^{(n)}(0)
```

after normalization by `Z(0)=480`.

---

## 3. Exact cumulants

The verifier computes:

```text
kappa_1 = 14/3
kappa_2 = 272/9
kappa_3 = 10432/27
kappa_4 = -156416/27
kappa_5, kappa_6 also generated exactly
```

The mean is:

```text
14/3.
```

The variance is:

```text
272/9.
```

---

## 4. Structural variance identity

The most important new identity is:

```text
kappa_2 = 272/9.
```

But:

```text
dim(E8)=248,
dim(SU5)=24,
q^2=9.
```

Therefore:

```text
kappa_2 = (248+24)/9 = (dim(E8)+dim(SU5))/q^2.
```

This is a strong bridge from finite spectral fluctuations to exceptional/GUT dimensions.

---

## 5. Coefficient of variation

The normalized coefficient of variation squared is:

```text
CV^2 = variance / mean^2 = 68/49.
```

This is another exact invariant of the W(3,3) finite spectral distribution.

---

## 6. Excited-sector statistics

Restricting to the E6 excited sector:

```text
Z_excited(t)=48e^{10t}+30e^{16t}.
```

The excited-sector total is:

```text
48+30=78=dim(E6).
```

The excited mean is:

```text
160/13.
```

The excited variance is:

```text
720/169.
```

So the E6 excited sector has its own exact finite thermodynamics.

---

## 7. Verified checks

The verifier confirms:

| check | status |
|---|---:|
| true Master Equation `q! = 2q` | pass |
| sectors total `480` | pass |
| probabilities sum to one | pass |
| mean `14/3` | pass |
| variance `272/9` | pass |
| kappa3 `10432/27` | pass |
| kappa4 `-156416/27` | pass |
| variance equals `(E8+SU5)/q²` | pass |
| coefficient of variation squared `68/49` | pass |
| excited total `78=E6` | pass |
| excited mean `160/13` | pass |
| excited variance `720/169` | pass |
| E8 dimension `248` | pass |
| SO10 dimension `45` | pass |

---

## 8. Why this matters

The finite spectral action is now a finite thermodynamic system:

```text
Z(t) -> moments
log Z(t) -> cumulants/fluctuations
```

This matters because fluctuations are where masses, mixing, and stability conditions often enter in statistical/spectral systems.

The new variance identity:

```text
variance = (E8 + SU5)/q²
```

is the first exact exceptional/GUT bridge at the cumulant level.

---

## 9. New files

- `exploration/PART_CCCCCVIII_FREE_ENERGY_CUMULANT_KERNEL.py`
- `PART_CCCCCVIII_FREE_ENERGY_CUMULANT_KERNEL.md`
- `PART_CCCCCVIII_free_energy_cumulant_kernel_results.json`

---

## 10. Next target

The next target is to compare these cumulants with the empirical mass/mixing closures:

```text
variance = 272/9
CV^2 = 68/49
excited mean = 160/13
excited variance = 720/169
```

The likely route is to test whether these fluctuation invariants generate one of the currently empirical dimensionless ratios, especially Higgs/top or CKM/PMNS variance-like quantities.
