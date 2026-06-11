# BT826 — Photonic Mirror Middleware

BT825 proves that the photon's physical optics generate the full two-qutrit
Clifford image:

```text
|Sp(4,3)| = 51840.
```

BT815 identifies the chart-transversal bus as a `2160`-element `D12` mirror
G-set, distinct from the cyclic `C12` rectangle clock.  BT814 identifies the
local residual carrier as the `48`-block tomotope edge-face middle layer.

BT826 fuses them:

```text
|Sp(4,3)| = 24 * 2160 = 24 * 45 * 48.
```

## Meaning

The `2160` bus is not a loose count.  It is:

```text
2160 = 540 * 4   chart-transversal slots
2160 = 240 * 9   antipode slots
2160 = 45 * 48   polar-pair geography * local tomotope middle layer
```

The projective slot stabilizer is `D12`; lifting from `PSp(4,3)` to
`Sp(4,3)` doubles it to order `24 = f`.  Therefore the full optical Clifford
group factors as:

```text
full slot stabilizer * polar vacuum geography * tomotope middle carrier
    = 24 * 45 * 48
    = 51840.
```

## Architectural Reading

The photonic holonet has two different time/transport layers:

```text
C12  cyclic selector clock        rectangle side
D12  mirror/antipode bus          chart-transversal side
```

The new point is that the `D12` side is the one that lifts to the full optical
Clifford runtime.  The photon is not only clocked by the cyclic selector; it is
routed by a mirror middleware whose local carrier is the tomotope middle layer.

## Validation

Run:

```bash
python3 analysis/bt826_photonic_mirror_middleware.py
```
