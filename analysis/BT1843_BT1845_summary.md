# BT1843-BT1845 summary

Executed the three requested moves after BT1840-BT1842, including Wil's proposed 66-edge genus connection.

## BT1843 — multivariate covariance SPRT

BT1842 compressed the BT1840 covariance matrix to its largest eigenvalue.  BT1843 uses the full 12-dimensional inverse covariance in the likelihood ratio.

```text
uniform-direction variance inflation = 1.763333333333333
aggregate sigma = 5.656481204831619
delta^T Sigma^{-1} delta = 0.12635807264797333
LLR drift under section A = 0.06317903632398666
LLR sd per run = 0.3554688068564854
fixed 5 sigma budget = 200 runs
adaptive median stop = 99 runs
adaptive mean stop = 111.886 runs
adaptive p95 stop = 224 runs
wrong decisions = 3 / 5000
```

## BT1844 — F12/genus-6 edge bridge

Read the repo's oscillator/genus trail and tested the proposed 66-edge connection.

The result is exact at the complete-pair incidence level:

```text
F12 mesh rotations = C(12,2) = 66
Csaszar genus-6 K12 edges = C(12,2) = 66
Szilassi genus-6 complete face adjacencies = C(12,2) = 66
```

Csaszar side:

```text
v = 12
h = (v-3)(v-4)/12 = 6
E = v(v-1)/2 = 66
F = 44
```

Szilassi side:

```text
f = 12
h = (f-4)(f-3)/12 = 6
E = f(f-1)/2 = 66
V = 44
```

Verdict: the connection is real as an incidence-schedule equivalence, not as a proof that a geometric non-self-crossing genus-6 Csaszar/Szilassi polyhedron exists.

## BT1845 — covariance-aware hardware targets

Translated the BT1840 covariance matrix into primitive-family targets.

```text
current lambda_max = 1.821589796573715
target lambda_max <= 1.4
current 5 sigma budget = 200 runs
target 5 sigma budget <= 159 runs
```

Internal covariance targets:

```text
qutrit P: current 0.18 -> target 0.05
D4 G: current 0.16 -> target 0.05
K4 E: current 0.14 -> target 0.04
C12 C: current 0.20 -> target 0.05
```

Priority order:

```text
1. C12_C internal covariance
2. qutrit_P internal covariance
3. D4_G internal covariance
4. K4_E to C12_C cross covariance
5. K4_E internal covariance
```

The key engineering conclusion is that covariance suppression, especially ring/guard common drift and qutrit path common drift, is now the highest-value hardware target.
