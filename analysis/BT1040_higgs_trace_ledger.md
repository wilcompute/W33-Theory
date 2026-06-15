# BT1040 — Higgs trace ledger

BT1040 computes the raw Higgs traces for the BT1038/BT1039 representation
candidate without inserting empirical parameters.

## Weakslot scalar

The weakslot is

```text
C^3 = C_singlet + C^2_weak_doublet
```

A Higgs doublet `phi=(phi1,phi2)` acts as the Hermitian off-diagonal weakslot
matrix:

```text
Phi = [[0, phi^*], [phi, 0]]
```

Let

```text
h2 = |phi1|^2 + |phi2|^2.
```

Then on the weakslot:

```text
tr_weak(Phi^2) = 2 h2
tr_weak(Phi^4) = 2 h2^2
```

## 162-carrier traces

The multiplicity outside the weakslot is:

```text
2_chiral * 3_generation * 3_fiber * 3_color = 54
```

Therefore:

```text
tr_F(Phi^2) = 108 h2
tr_F(Phi^4) = 108 h2^2
```

## Mixed trace with Delta_1

On the harmonic 162-mode fermion projection:

```text
tr_F(Delta_1 Phi^2) = 0
```

because the projection is zero-mode. The 240-cellular extension remains pending:
one must choose how `Phi` acts on `im(d2)+heavy` before computing the mixed trace
against the full spectrum `0^81,4^120,10^24,16^15`.

## Boundary

The raw 162-carrier Higgs traces are computed. The 240-carrier mixed trace is not
fabricated; it is the next exact extension problem.

## Witnesses

```text
analysis/bt1040_higgs_trace_ledger.py
data/bt1040_higgs_trace_ledger.json
```
