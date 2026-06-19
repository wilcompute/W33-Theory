# BT1331 -- Master Synthesis Certificate

## Purpose

BT1331 converts the BT1326 master synthesis into a certificate-indexed claim set.

## New files

```text
tools/bt1331_master_synthesis_certificate.py
data/bt1331_master_synthesis_certificate.json
```

## Certificate classes

BT1331 separates the master theorem into four statuses:

1. Exact arithmetic.
2. Structural theorem.
3. Simulation-required gate.
4. Engineering-required gate.

## Verified by certificate

The exact Q4 number table is backed by BT1327, with the one epoch defect repaired by BT1328.

The corrected epoch is:

```text
10980 = 3*3660
```

by rolling chart-phase closure.

## Not yet certified by this layer

The 14.4 percent ML threshold and the 5mm by 5mm chip footprint are not treated as exact arithmetic. They are marked as simulation and engineering gates.

## Consequence

The master theorem is now stronger because it distinguishes what is proved exactly from what remains to be simulated or engineered.
