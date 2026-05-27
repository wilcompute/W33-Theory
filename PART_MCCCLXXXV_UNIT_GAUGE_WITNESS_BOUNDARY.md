# Part MCCCLXXXV — Unit-Gauge Witness Boundary

This part reconciles the local legacy measured-constants hint with the stricter
MCCCLXXXIV packet.

The arithmetic is kept.  The universal headline is not.  Dimensionful SI
mantissas are promoted only as unit-gauge witnesses unless a separate
dimensionless ratio or scale map fixes the physical unit gauge.

## Reconciled Legacy Hints

| Legacy hint | Strict witness | Integer | Status |
|---|---:|---:|---|
| `G` | Newtonian constant `G` | `667430` | CODATA measured rounded mantissa |
| `g0` | standard gravity `g0` | `980665` | conventional exact |
| `1 atm` | standard atmosphere | `101325` | conventional exact |
| `m_p` in rounded keV | proton mass energy equivalent | `938272` | CODATA measured rounded mantissa |
| Faraday `F` | Faraday constant | `9648533` | SI-derived exact rounded mantissa |

All five legacy arithmetic witnesses match the strict MCCCLXXXIV packet.

## Strict Extra Closure

MCCCLXXXIV adds one witness missing from the legacy hint:

```text
molar gas constant: R*10^6 rounded = 8314463
8314463 = (F5*Phi3 + r*Phi6*Phi12) * (Phi6*L_eff - 2^Phi6)
        = (5*13 + 2*7*73) * (7*1111 - 128)
```

So the strict six-witness orbit is:

```text
5 legacy overlaps + 1 molar-gas alpha-volume lock = 6 unit-gauge witnesses
```

## Boundary Theorem

The six witnesses split evenly into three status classes:

```text
2 CODATA measured rounded mantissas
2 conventional exact standards
2 SI-derived exact rounded mantissas
```

This is the executable boundary:

```text
unit-scaled decimal witness layer = true
dimensionless prediction layer    = false
unsafe universal headline         = false
```

The result is stronger than a retraction.  It keeps every exact integer
identity that survived verification, adds the molar-gas closure, and removes
the category error that would treat an SI-unit mantissa as a unit-independent
prediction.

## Verification

Run:

```bash
python3 analysis/w33_MCCCLXXXV_unit_gauge_witness_boundary.py
python3 -m pytest --noconftest -q tests/test_w33_MCCCLXXXV_unit_gauge_witness_boundary.py
```

The verifier checks 12 conditions, including the legacy overlap, the strict
extra witness, the balanced status classes, and the non-promotion boundary.
