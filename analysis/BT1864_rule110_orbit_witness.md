# BT1864 — Rule-110 Orbit Witness

BT1864 runs the BT1861 transition rule on the BT1858 length-30 tape seed.

## Rule

```text
T((a,h_a),(b,h_b),(c,h_c)) = (rule110(a,b,c), h_b + 1 mod 6)
```

where the gap track uses `S=0`, `L=1`, and the hole track uses `Z/6Z`.

## Run

```text
length = 30
steps = 120
first full-state repeat = none found
first gap-track repeat = none found
```

## Statistics

```text
ones_min = 9
ones_max = 24
max cyclic transitions = 24
hole track coverage at every sampled step = {0,1,2,3,4,5}
```

## Selected snapshots

```text
t=0:
S0 L1 S2 S3 L4 S5 L0 S1 L2 S3 S4 L5 S0 L1 S2 L3 S4 L5 S0 S1 L2 S3 L4 S5 S0 L1 S2 S3 L4 S5
```

```text
t=30:
L0 S1 L2 L3 S4 L5 L0 L1 S2 L3 S4 L5 L0 L1 L2 L3 S4 L5 L0 L1 S2 S3 S4 S5 L0 L1 L2 S3 L4 L5
```

Gap-track checkpoints:

```text
t=0   SLSSLSLSLSSLSLSLSLSSLSLSSLSSLS
t=30  LSLLSLLLSLSLLLLLSLLLSSSSLLLSLL
t=60  LLLSLLLSLLSLLLLLSSSLLLSLLLSSSS
t=90  LLSSSSLLLSLLLSLLSLLLLLSSSLLLSL
t=120 SLLLSLLLSSSSLLLSLLLSLLSLLLLLSS
```

## Verdict

The BT1858 tape seed does not collapse under the BT1861 rule through 120 steps.  It shows nontrivial symbolic dynamics, preserves all six hole symbols, and has no observed repeat in either the full 12-symbol state or the binary gap track.

Boundary: finite orbit witness only; no full universality proof or physical implementation proof is claimed.
