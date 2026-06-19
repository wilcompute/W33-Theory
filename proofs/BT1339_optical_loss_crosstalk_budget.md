# BT1339 -- Optical Loss and Crosstalk Budget

## Purpose

BT1339 upgrades BT1335 from an area-only gate to a first optical budget gate.

## Conservative scenario

```text
path length = 1.0 cm
propagation loss = 1.0 dB/cm
bends = 16 at 0.02 dB each
crossings = 20 at 0.01 dB each
phase shifters = 8 at 0.10 dB each
splitters = 4 at 0.05 dB excess loss each
pair crosstalk = -35 dB across 12 neighbors
```

Result:

```text
total loss = 2.52 dB
transmission = 0.559
aggregate crosstalk = -24.21 dB
```

This passes the conservative 3 dB loss budget and -20 dB aggregate crosstalk budget.

## Aggressive scenario

```text
total loss = 0.436 dB
transmission = 0.905
aggregate crosstalk = -34.21 dB
```

## Boundary

This is still not a foundry PDK simulation. It is a parameterized optical budget. A foundry-ready result requires routed layout extraction, wavelength-dependent S-parameters, crossing topology, thermal model, and packaging/fanout design.

## Files

```text
tools/bt1339_optical_loss_crosstalk_budget.py
data/bt1339_optical_loss_crosstalk_budget.json
```
