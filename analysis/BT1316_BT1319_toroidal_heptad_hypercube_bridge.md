# BT1316-BT1319 Toroidal Heptad / Q4 Holonet Bridge

## Summary

This packet closes the toroidal-polyhedra data loop and connects it to the
local Q4 packet router used by the holonet architecture.

## BT1316 - Authoritative Data Lock

The verified dual data are:

```text
Csaszar:  V,E,F = 7,21,14
Szilassi: V,E,F = 14,21,7
```

The shared invariant is `E=21`; duality swaps vertices and faces.  The older
DXXXII table that duplicated the Csaszar row onto Szilassi was stale and is now
explicitly corrected.

## BT1317 - Pipeline Consolidator

The same heptad carrier is visible across the existing artifacts:

```text
raw TXT heptad -> CCCCXXI Fano bridge -> 168/192 tomotope packet
              -> 42 oriented transports -> 168 weighted transports
              -> 7+1 Markov split -> 21/16 Fourier source
```

The moment ladder is exact:

```text
21/16 * 16 = 21
21 * 2 = 42
42 * 4 = 168
```

## BT1318 - C2 Axis Assignment

The abstract Csaszar map has automorphism group order `42` with order profile:

```text
{1:1, 2:7, 3:14, 6:14, 7:6}
```

There are exactly seven involutions, each fixing one Csaszar vertex.  Current
metric coordinates do not distinguish the five Csaszar and two Szilassi
realizations as those seven involutions.  They prove a more specific boundary:

```text
five Csaszar metrics -> one vertex-axis C2 fixing vertex 6
two Szilassi metrics -> one dual face-axis C2 fixing face 4
```

So the realization-to-involution bijection remains unproved in the current
labels.

## BT1319 - 4x4 Toroidal Square = Q4 Packet Router

The ordinary 4x4 knight graph is not Q4:

```text
ordinary edges = 24
degree profile = 2^4, 3^8, 4^4
```

The toroidal boundary is exactly the missing operation.  With wraparound the
4x4 knight graph becomes:

```text
16 vertices
32 edges
4-regular
Q4
```

The existing toroidal knight tour is a Gray Hamilton cycle on Q4, with each
hypercube dimension contributing eight edges.

## Tomotope / Hypercube Interface

The flag-codec identity is:

```text
tetrahedron + Csaszar + Szilassi = (2 + 7 + 7) codecs = 16 codecs
16 codecs * 12 flags/codec = 192 tomotope flags
```

Thus the Q4 vertices are not decoration: they are the sixteen local 12-flag
codec slots.  The Q4 square faces give the tetrahedron flags:

```text
faces_2(Q4) = C(4,2) * 2^2 = 24
```

The protected router lift keeps the 16 Q4 states but encodes them as the
extended Hamming / RM(1,3) `[8,4,4]` code, so one Q4 bit flip lifts to a
distance-4 protected transition.

## 14641 Boundary

The tetrahedral Pascal row is:

```text
(1,4,6,4,1)
```

Evaluating at `Phi_4=10` gives:

```text
1 + 4*10 + 6*10^2 + 4*10^3 + 10^4 = 14641 = 11^4 = (k-1)^mu
```

This is the correct status of the "14641 tetrahedron Clifford algebra" clue:
it is a verified tetrahedral Pascal/Ihara scale marker.  It is not yet a proof
of a complete `11^4` Clifford algebra object unless a future construction
provides the objectwise generators, multiplication, and representation action.

## Holonet Placement

The Q4 router is local.  The holonet also has:

```text
540 Q3 chart routers
540 * 4 = 2160 chart-transversal slots
2160 D12 mirror-bus slots
```

So the local-to-global placement is:

```text
4x4 toroidal square -> Q4 packet router -> 16 tomotope codec slots
                    -> local protected [8,4,4] router lift
                    -> 540-chart / 2160-slot holonet bus
```

This does not replace the global Q3 atlas and does not upgrade the known Q4
subsystem distance boundary.

## Verification

```text
python3 analysis/bt1316_toroidal_authoritative_data_lock.py
python3 analysis/bt1317_toroidal_tomotope_pipeline_consolidator.py
python3 analysis/bt1318_toroidal_c2_axis_assignment.py
python3 analysis/bt1319_toroidal_q4_hypercube_holonet_bridge.py
python3 tests/test_bt1316_bt1319_toroidal_heptad_hypercube_bridge.py
python3 -m py_compile analysis/bt1316_toroidal_authoritative_data_lock.py analysis/bt1317_toroidal_tomotope_pipeline_consolidator.py analysis/bt1318_toroidal_c2_axis_assignment.py analysis/bt1319_toroidal_q4_hypercube_holonet_bridge.py tests/test_bt1316_bt1319_toroidal_heptad_hypercube_bridge.py
python3 -m json.tool data/bt1316_toroidal_authoritative_data_lock.json
python3 -m json.tool data/bt1317_toroidal_tomotope_pipeline_consolidator.json
python3 -m json.tool data/bt1318_toroidal_c2_axis_assignment.json
python3 -m json.tool data/bt1319_toroidal_q4_hypercube_holonet_bridge.json
```
