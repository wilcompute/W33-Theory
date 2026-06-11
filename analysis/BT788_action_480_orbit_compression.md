# BT788 - 480 Action Orbit Compression

BT785 proved the arithmetic identity:

```text
480 = 10 * 48
```

BT788 tests whether that survives the actual cube-chart stabilizer action.

## Result

Under the 48-element stabilizer of a cube chart, the raw action on directed
W33 edges is not ten free 48-orbits.  The micro-orbit profile is:

```text
48^5 + 24^8 + 16^2 + 8^2 = 480
```

The same profile occurs on oriented triangle-corners.

This compresses to ten local packets by the unique size pattern:

```text
5 packets:  [48]
4 packets:  [24 + 24]
1 packet:   [16 + 16 + 8 + 8]
```

So the corrected theorem is:

```text
480 is ten local 48-packets after stabilizer micro-orbit compression.
```

## Five Carriers

The verifier applies the real stabilizer action to:

```text
2E  directed edges              actual orbit computation
3T  oriented triangle-corners    actual orbit computation
Tr(A^2) closed 2-walks           same carrier as directed edges
Tr(L0) degree trace              same carrier as directed incidences
6*80 curvature integral          ten spectral-gap 48-channels
```

The first two are independent 480-point carriers and both have the same
micro-orbit compression signature.

## Interpretation

This is better than a bare count.  The failure of "ten raw 48-orbits" exposes
the real local packet grammar:

```text
48, 24+24, 16+16+8+8
```

That grammar is exactly the scale at which the cube side and tomotope side
can exchange data without pretending the local stabilizer action is free.

## Validation

Run:

```bash
python3 analysis/bt788_action_480_orbit_compression.py
```
