# BT1043 — Phi extension to the 240 cellular QFT carrier

BT1043 chooses a non-fabricated extension of the Higgs scalar to the 240-cellular
QFT carrier.

## Carrier split

```text
ker Delta_1      = 81
im(d2)           = 120
r-sector         = 24
s-sector         = 15
total            = 240
```

## Extension choice

The extension is **minimal harmonic-only**:

```text
Phi acts on the harmonic 81-sector as left multiplication on HS(K)
Phi acts as zero on im(d2)+heavy until a nonzero sector action is derived
```

This is deliberately conservative: it does not invent Higgs couplings on sectors
where the action has not been derived.

## Traces

Let

```text
h2 = |phi1|^2 + |phi2|^2.
```

Then for the 240-carrier minimal extension:

```text
tr_240(Phi^2)          = 54 h2
tr_240(Phi^4)          = 54 h2^2
tr_240(Delta_1 Phi^2) = 0
```

## Boundary

The zero mixed trace is a consequence of the minimal harmonic-only extension, not
a universal claim. A nonzero `im(d2)+heavy` Higgs action must be derived before
changing the mixed trace.

## Witnesses

```text
analysis/bt1043_phi_240_extension.py
data/bt1043_phi_240_extension.json
```
