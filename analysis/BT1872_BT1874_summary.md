# BT1872-BT1874 summary

Executed the three requested moves after BT1869-BT1871.

## BT1872 — dual-face Z-check construction

BT1869 showed the global-clock-only CSS skeleton was not protected.  BT1872 replaces the failed six distance-row Z layer with the actual local dual-face layer.

Construction:

```text
X checks = 44 oriented K12 triangular face rows
Z checks = 12 signed vertex-star rows, i.e. Szilassi-dual face checks
field = GF(3)
```

For edge `i<j`, the signed vertex-star convention is:

```text
vertex i coefficient = +1
vertex j coefficient = -1 = 2 mod 3
```

Exact result:

```text
rank(HX) = 42
rank(HZ) = 11
rank(HX HZ^T) = 0
nonzero entries in HX HZ^T = 0
n = 66
k = 66 - 42 - 11 = 13
d_X = 3
d_Z = 3
```

Therefore the finite matrix model gives:

```text
[[66,13,3]]_3
```

This is the first bona fide finite CSS matrix code in the K12/F12 chain.

## BT1873 — subsystem paired-gauge construction

BT1873 reuses the five distance contrasts correctly.

Starting parent:

```text
BT1872 stabilizer parent = [[66,13,3]]_3
```

The five distance contrasts from the BT1865 commutation defect become gauge refinements:

```text
5 Z-gauge distance contrasts
5 X-gauge partners from independent face-row combinations
symplectic pair rank = 5
```

Subsystem accounting:

```text
n = 66
parent k = 13
gauge qudits r = 5
logical after gauge accounting = 8
```

Candidate notation:

```text
[[66,8,>=3;5]]_3
```

The `>=3` remains conditional on a full all-weight subsystem-distance proof.  The key correction is that BT1872 fixes the weight-2 defect; the five distance contrasts are gauge refinements, not the primary protection mechanism.

## BT1874 — larger-ring Rule-110 glider catalog

Extended the BC/Sturmian rings to `16N` steps.

```text
N=48,  steps=768:  repeat 120 -> 216, period 96
N=78,  steps=1248: no repeat
N=126, steps=2016: repeat 759 -> 766, period 7
N=204, steps=3264: no repeat
```

All rings see all eight Rule-110 neighborhoods.

Recurring candidate packet velocities:

```text
v = 0
v = -4
v = 3
v = 10 / -11 aliases
```

Interpretation:

```text
finite-box locks: N=48, N=126
nonrepeating active rings: N=78, N=204
```

The N=126 period-7 lock is a traveling-wave/glider-lock regime with very long diagonal packets, not a uniform collapse.  N=78 and N=204 are the better active test beds.

## Boundary

BT1872 is an exact finite GF(3) CSS matrix-code construction.  BT1873 is a finite symplectic subsystem-gauge construction whose full gauge-distance proof remains open.  BT1874 is a finite larger-ring dynamical catalog.  No physical implementation, hardware threshold, or infinite Rule-110 universality proof is claimed.
