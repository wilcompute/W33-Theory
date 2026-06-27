# BT1875-BT1877 summary

Executed the three requested moves after BT1872-BT1874.

## BT1875 — all-weight subsystem distance proof

Parent code from BT1872:

```text
[[66,13,3]]_3
```

Subsystem candidate from BT1873:

```text
[[66,8,>=3;5]]_3
```

BT1875 proves the distance for the chosen finite symplectic gauge-pair model.

Proof strategy:

```text
To prove distance 3, rule out dressed logicals of weight 1 and 2, then exhibit one dressed logical of weight 3.
```

The BT1872 parent has no weight-1/2 logicals.  Adding five gauge-pair commutation constraints shrinks the logical centralizer, so no new weight-1/2 dressed logical can appear.

Surviving weight-3 dressed logical:

```text
edge(0,1) + 2*edge(0,3) + edge(1,3)
```

Result:

```text
[[66,8,3;5]]_3
```

Boundary: exact finite symplectic-matrix distance result for the chosen gauge model; no optical decoder or hardware threshold is claimed.

## BT1876 — optical measurement schedule for [[66,13,3]]_3

Compiled the parent CSS code into a finite optical syndrome schedule.

Checks:

```text
44 X face checks
12 Z dual vertex-star checks
66 F12/K12 edge payload rotations
```

Touch counts:

```text
44 * 3  = 132 X edge touches
12 * 11 = 132 Z edge touches
264 total edge/check touches per full cycle
```

Five-round schedule:

```text
X0_Reye_faces:          16 checks, 48 touches
X1_residual_faces_A:    14 checks, 42 touches
X2_residual_faces_B:    14 checks, 42 touches
Z0_even_vertex_stars:    6 checks, 66 touches
Z1_odd_vertex_stars:     6 checks, 66 touches
```

Rank dependencies:

```text
X rows measured = 44, X rank = 42, dependencies = 2
Z rows measured = 12, Z rank = 11, dependencies = 1
```

Boundary: compiler-level optical measurement schedule only.

## BT1877 — glider phase-class extractor

Classified the BT1874 packet velocities by the `Z/6Z` hole phase.

Phase evolution along a velocity-v diagonal:

```text
h_t = h_0 + (v+1)t mod 6
```

Velocity classes:

```text
v = 0:     six-phase clock packet
v = -4:    antipodal two-phase packet
v = 3:     three-phase chiral packet
v = 10:    six-phase reverse packet
v = -11:   three-phase reverse/alias packet
```

Active-ring survival:

```text
N=78:  v=0, v=-4, v=3
N=204: v=0, v=-4, v=3, v=10
```

Interpretation:

```text
Z6 hole phase = gauge/clock layer, not stabilizer protection itself
```

This now matches the code side: the six-distance/hole layer is the gauge/clock layer in both the quantum-code construction and the Rule-110 tape dynamics.

## Boundary

BT1875 is an exact finite symplectic-matrix result for the chosen gauge model, BT1876 is a compiler-level optical schedule, and BT1877 is a finite phase-class extractor.  No optical decoder, hardware threshold, infinite glider theorem, or physical implementation is claimed.
