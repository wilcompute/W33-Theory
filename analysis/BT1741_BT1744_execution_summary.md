# BT1741-BT1744 execution summary

Read the new parallel commits after BT1740 and continued from the current repo frontier.

## New repo changes read first

- `0d341d72`: restored the full live-paper `docs/index.html` after the earlier stub overwrite; I avoided editing that large restored index directly.
- `1c81de1d`: added the explicit E8 Eisenstein/Witting weld and the Hesse/Mermin contextuality engine.

## BT1741: cocycle local rigidity

Added `analysis/bt1741_cocycle_local_rigidity.py`.

The script exhaustively scans all one-coordinate mutations around the BT1738 Hesse/Fano cocycle witness.  It checks 9063 mutations and retains only connected cubic `63/63/189` candidates with no 4-cycles and no 6-cycles.

Result: 222 viable no-4/no-6 candidates, but none improves the current score:

```text
8-cycles = 44
10-cycles = 73
diameter = 9
```

So the descent now needs coordinated multi-position mutation or a different cocycle parametrization.

## BT1742: E8/Hesse/atlas allocation

Added `analysis/bt1742_e8_hesse_atlas_allocation.py`.

This connects the new E8 and Hesse commits to the BT1730-BT1739 atlas laws:

```text
atlas bus = 16*3 = 48
framed flags = 16*4*3 = 192
E8 roots = 192 + 48 = 240
E8 roots = 5*48 = 240
E8 hexagons = 40, roots per hexagon = 6, so 40*6 = 240
Hesse/W33 register split = 2*9 + 10 + 12 = 40
self-frame puncture = 192 - 3 = 189
```

Boundary: this is an allocation/count theorem, not a root-level bijection.

## BT1743: channel-frame emulator

Added `analysis/bt1743_channel_frame_emulator.py`.

The emulator constructs the colored/multiflag `64/64/192` frame and punctures one self-slot to get colored degree-3 `63/63/189`.

Color collapse is a falsifier:

```text
colored punctured carrier: 189 links, degree 3
simple color collapse: 63 links, degree 1
```

So the channel-frame is a real framed carrier, but not itself the simple split-Cayley Levi graph.

## BT1744: self-frame puncture diagram

Added:

- `docs/BT1744_self_frame_puncture_diagram.svg`
- `docs/BT1744_self_frame_puncture_diagram.html`

The diagram visualizes:

```text
16-cell atlas -> 64 bit slots -> 192 colored flags -> self-frame puncture -> 63/63/189
```

I did not touch the restored 24k-line docs index.
