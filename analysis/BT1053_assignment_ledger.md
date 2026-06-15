# BT1053 — Detailed 162-slot assignment ledger

BT1053 writes the explicit slot ledger for the 162-dimensional carrier from BT1038.

## Carrier factors

```text
H = C^2_chiral x C^3_generation x C^3_fiber x C^3_weakslot x C^3_color
```

The slot labels are:

```text
chirality  c in {L,R}
generation g in {0,1,2}
fiber      f in {0,1,2}
weakslot   w in {S,D1,D2}
color      k in {0,1,2}
```

Total count:

```text
2 * 3 * 3 * 3 * 3 = 162
```

## Weakslot ledger

The weakslot is split as

```text
S  = singlet slot
D1,D2 = doublet slots
```

The trace-corrected U1 generator from BT1049 acts by

```text
Y0(S)  =  2/3
Y0(D1) = -1/3
Y0(D2) = -1/3
```

## Multiplicity table

| weakslot | charge | multiplicity |
| --- | ---: | ---: |
| S | 2/3 | 2*3*3*1*3 = 54 |
| D1,D2 | -1/3 | 2*3*3*2*3 = 108 |

## Trace checks

```text
Tr_162(Y0)   = 54*(2/3) + 108*(-1/3) = 0
Tr_162(Y0^2) = 54*(4/9) + 108*(1/9) = 36
```

## Boundary

This is a slot assignment ledger. It does not yet identify physical particle names, anti-particle doubling, or left/right phenomenological assignments. Those require the final representation table.
