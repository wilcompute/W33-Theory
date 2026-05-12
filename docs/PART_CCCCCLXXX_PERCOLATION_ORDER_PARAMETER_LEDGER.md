# Part CCCCCLXXX — Percolation Order-Parameter Ledger

Part CCCCCLXXIX connected the genus oscillator to quantum/topological percolation. This part fixes the order parameters every executable experiment must report.

## 1. Occupied bridge model

For incidence atoms `a`, define Bernoulli occupation

```text
omega_a in {0,1},       P(omega_a=1)=p.
```

The occupied bridge is

```text
Y_p = sum_a omega_a w_a Y_a.
```

The quantum transport Hamiltonian and matter visibility operator are

```text
H_p = Delta_internal + Y_p + Y_p^*,
C_H(p) = Y_p Y_p^* restricted to K=H1.
```

## 2. Core scalar order parameters

Given eigenvalues `lambda_i >= 0` of `C_H(p)`, define

```text
R(p) = rank C_H(p),
T1(p)= Tr C_H(p),
T2(p)= Tr C_H(p)^2,
D(p) = T1(p)^2 / T2(p)       if T2(p)>0,
D(p) = 0                     if T2(p)=0.
```

`D(p)` is the effective visible dimension. It equals 81 for a perfectly isotropic full-rank 81-sector and drops when the spectrum concentrates.

## 3. Threshold definitions

```text
p_geom  = first p with giant occupied incidence component,
p_H1    = first p with R(p)>0,
p_full  = first p with R(p)=81,
p_split = first p with stable nontrivial spectral splitting of C_H(p).
```

The hierarchy is expected to satisfy

```text
p_geom <= p_H1 <= p_full
```

only in favorable cases. Quantum localization may delay `p_H1` or `p_full` beyond classical geometric connectivity.

## 4. Spectral split counter

For sorted positive eigenvalues of `C_H(p)`, group values within tolerance `eps`. Define

```text
S(p) = number of positive eigenvalue clusters.
```

Then:

```text
S(p)=0  no matter visibility,
S(p)=1  isotropic visible sector,
S(p)>1  split/hierarchical visible sector.
```

## 5. Betti order parameters

For the occupied incidence subcomplex, also record

```text
B(p) = (beta_0(p), beta_1(p), beta_2(p), ...).
```

The topological transition is then compared against the quantum visibility transition:

```text
beta_1(p)>0       versus       R(p)>0,
large component   versus       rank C_H(p)=81.
```

## 6. Meaning

This separates four notions that can be conflated:

```text
geometric percolation  = connectivity,
homological percolation = nontrivial cycles,
quantum percolation     = coherent transport through occupied disorder,
W33 matter visibility   = full or partial rank of C_H(p) on H1.
```

The next script should accept a sampled `C_H(p)` spectrum and occupied-complex Betti data, then emit this ledger for every `p`.
