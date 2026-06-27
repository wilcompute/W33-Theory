# BT1841 — Numeric F12 Phase Table Generator

BT1838 gave the mesh schedule count for the C12 winding analyzer:

```text
F12: 66 two-mode rotations + 12 output phases
```

BT1841 materializes the numeric Givens phase table.

## Generator

Use complex Givens nullification on the normalized Fourier matrix

```text
F12[j,k] = exp(2*pi*i*j*k/12) / sqrt(12).
```

For each column, sweep bottom-to-top and zero the current subdiagonal entry using a two-row unitary.  Each rotation record stores:

```text
rows
zeroed column
theta = atan2(|b|,|a|)
phase_a = arg(a)
phase_b = arg(b)
```

## Verification

```text
rotations = 66
output phases = 12
Frobenius reconstruction error = 2.351156386898407e-15
offdiagonal norm after nullification = 5.625739853018683e-15
```

The full numeric table is in:

```text
data/bt1841_f12_phase_table.json
```

Boundary: hardware sign conventions can change displayed phase labels, but the unitary reconstruction check fixes the schedule.
