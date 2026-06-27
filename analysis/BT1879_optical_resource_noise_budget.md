# BT1879 — Optical Resource/Noise Budget for BT1876

BT1879 combines the BT1876 five-round measurement schedule with the older BT1831/BT1832 optical budget anchors.

## Anchors

BT1831 baseline:

```text
resource count = 15
survival probability = 0.9704163817442235
erasure probability = 0.02958361825577649
surviving-shot syndrome error union bound = 0.00872
```

BT1832 primitive lowering:

```text
connected component graph = 33 nodes, 39 edges
12 ring bins
12 ring detectors
21 phase shifters
```

## BT1876 schedule

```text
rounds = 5
X face checks = 44
Z vertex-star checks = 12
total checks = 56
edge/check touches = 264
payload edges = 66
```

## Conservative pass model

Count both payload edges and check ancillas as active resources:

```text
active resources = 66 + 56 = 122
per-resource loss = 0.002
survival = 0.7832962313857886
erasure = 0.21670376861421137
```

Scale the BT1831 surviving-shot syndrome union rate per resource:

```text
0.00872 / 15 = 0.0005813333333333333
56 checks -> 0.03255466666666667
```

Combined conservative bound:

```text
unconditional error-or-erasure bound = 0.24925843528087804
effective postselected success rate = 0.7577962836717681
```

## Lighter ancilla-only scenario

If only the 56 active check ancillas are counted as loss-critical in a reused payload path:

```text
survival = 0.8939439964545421
erasure = 0.10605600354545786
unconditional error-or-erasure bound = 0.13861067021212453
effective postselected success rate = 0.8648419476312967
```

## Interpretation

The protected-code schedule is much heavier than the BT1831 15-resource syndrome demo.  In the conservative model, erasure dominates.  The first engineering priority is therefore not decoding sophistication; it is loss reduction and syndrome-round reuse.

Boundary: scaled union-bound budget only.  This is not a calibrated noise model, decoder threshold, or hardware feasibility proof.
