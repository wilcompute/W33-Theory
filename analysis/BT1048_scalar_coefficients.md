# BT1048 — Symbolic scalar spectral coefficients

BT1048 inserts the BT1040/BT1046 scalar traces into the symbolic spectral-action
coefficient ledger.

## Minimal 240-carrier extension

```text
Tr(Phi^2)          = 54 h2
Tr(Phi^4)          = 54 h2^2
Tr(Delta_1 Phi^2) = 0
```

Core symbolic coefficients:

```text
C2_core = 54 f2 Lambda^2 h2
C4_core = 54 f0 h2^2
```

## Controlled sector ansatz

```text
Tr(Phi^2)
= 54 a0^2 h2 + 80 a4^2 h2 + 16 a10^2 h2 + 10 a16^2 h2
```

```text
Tr(Phi^4)
= 54 a0^4 h2^2 + 80 a4^4 h2^2 + 16 a10^4 h2^2 + 10 a16^4 h2^2
```

```text
Tr(Delta_1 Phi^2)
= 320 a4^2 h2 + 160 a10^2 h2 + 160 a16^2 h2
```

Uniform sector-amplitude case:

```text
C2_core = 160 f2 Lambda^2 h2 + 640 f0 h2
C4_core = 160 f0 h2^2
```

## Boundary

This is symbolic only. Cutoff moments, sign conventions, and sector amplitudes
remain explicit; no numerical physical parameter is inserted.

## Witnesses

```text
analysis/bt1048_higgs_spectral_coefficients.py
data/bt1048_scalar_coefficients.json
```
