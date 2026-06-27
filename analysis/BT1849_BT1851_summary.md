# BT1849-BT1851 summary

Executed the three requested moves after BT1846-BT1848 with repeated repo searches across antipodal gauges, K12 face words, Reye horizon completion, horizon code, primitive lowering, and actuator/covariance terms.

## Search trail

Useful repo hits included:

```text
analysis/BT1847_F12_to_K12_functor.md
analysis/bt1825_d5_coxeter_defect_involution.py
analysis/BT1826_finite_law_theorem.md
analysis/w33_reye_k12_orientable_horizon_completion.py
tests/test_w33_reye_k12_orientable_horizon_completion.py
analysis/bt1832_optical_primitive_lowering.py
analysis/BT1845_covariance_hardware_targets.md
```

## BT1849 — distance-6 antipodal gauge resolver

The only obstruction in BT1847 is the distance-6 tie in `Z/12Z`:

```text
+6 = -6
```

The six antipodal pairs are:

```text
(0,6), (1,7), (2,8), (3,9), (4,10), (5,11)
```

Resolver:

```text
one global Z2 antipodal sheet bit
bit 0: i -> i+6 for i=0,...,5
bit 1: i+6 -> i for i=0,...,5
```

Conclusion: the functor does not need six local tie bits.  It needs one global antipodal polarity, aligned with the older antipodal-involution language.

## BT1850 — face-word extractor

The older MCXCII Reye-K12 horizon completion already contains the correct face basis:

```text
16 Reye faces
28 residual faces
44 total triangular faces
132 directed edges
66 unordered edges, each appearing twice
horizon code = [72,66,6]
```

BT1850 maps every oriented face `(a,b,c)` to three F12 mesh rotations:

```text
(a,b,c) -> R_ab R_bc R_ca
```

Sample words:

```text
(0,1,11) -> R_0_1 R_1_11 R_11_0
(0,10,2) -> R_0_10 R_10_2 R_2_0
(9,10,11) -> R_9_10 R_10_11 R_11_9
```

Conclusion: the 66-edge bridge now has explicit 44 face words, so it is a face/rotation dictionary rather than only an edge count.

## BT1851 — actuator-cost covariance optimizer

BT1851 maps BT1848 covariance knobs onto BT1832 primitive families and adds modeled actuator costs.

Objective:

```text
minimize actuator cost subject to lambda_max <= 1.4
```

Selected actuator set:

```text
ring_guard_thermal_decoupler
qutrit_path_balancer
D4_parity_clock_isolator
```

Result:

```text
lambda_max start = 1.821589796573715
lambda_max after selected actuators = 1.386912
fixed 5 sigma runs start = 200
fixed 5 sigma runs after selected actuators = 156
total modeled cost = 10.5
```

Conclusion: the first hardware-control priority is not K4 phase dithering.  It is C12 ring/guard decoupling, qutrit common-drift balancing, and D4 parity clock isolation.

## Boundary

BT1849-BT1851 are exact/combinatorial/model-layer artifacts.  They do not claim a measured chip covariance, actuator power/cost, or a non-self-crossing Euclidean genus-6 polyhedron realization.
