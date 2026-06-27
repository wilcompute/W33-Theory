# BT1845 — Covariance-Aware Hardware Target Table

BT1845 translates the BT1840 covariance matrix into primitive-family engineering targets.

## Spectral target

Current matrix budget:

```text
lambda_max = 1.821589796573715
5 sigma runs = 200
```

Target:

```text
lambda_max <= 1.4
5 sigma runs <= 159
```

## Internal family targets

```text
qutrit P family: current rho = 0.18, target rho <= 0.05
D4 G family: current rho = 0.16, target rho <= 0.05
K4 E family: current rho = 0.14, target rho <= 0.04
C12 C family: current rho = 0.20, target rho <= 0.05
```

## Cross-family targets

```text
P-G: current 0.06, target 0.03
P-E: current 0.02, target 0.02
P-C: current 0.03, target 0.02
G-E: current 0.04, target 0.02
G-C: current 0.02, target 0.02
E-C: current 0.08, target 0.03
```

## Priority order

```text
1. C12_C internal covariance
2. qutrit_P internal covariance
3. D4_G internal covariance
4. K4_E to C12_C cross covariance
5. K4_E internal covariance
```

## Hardware interpretation

The most important engineering move is not simply lowering primitive error rates; it is decorrelating the family-level drifts:

```text
C12 ring thermal drift vs phase-slip guard thresholds
qutrit path-splitter common drift
D4 parity ancilla clock coupling
K4 equality interferometer phase common-mode drift
```

Boundary: these are covariance targets derived from the model, not measured chip specifications.
