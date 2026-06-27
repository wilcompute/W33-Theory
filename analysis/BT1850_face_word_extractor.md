# BT1850 — Face-Word Extractor

BT1850 extracts the 44 triangular face words from the existing MCXCII Reye-K12 orientable horizon completion and maps each triangle back to three `F12` mesh rotations.

## Repo anchors searched

The decisive anchor is:

```text
analysis/w33_reye_k12_orientable_horizon_completion.py
```

The test suite already verifies the core invariants:

```text
V = 12
E = 66
F = 44
Reye triangles = 16
Residual triangles = 28
directed edge count = 132
unordered edge profile = {2: 66}
horizon code = [72,66,6]
```

## Face-word rule

For an oriented triangle

```text
(a,b,c)
```

emit the mesh word

```text
R_ab R_bc R_ca
```

and the K12 edge word

```text
{a,b} {b,c} {c,a}
```

## Extracted packet

The committed JSON stores:

```text
16 Reye face words
28 residual face words
44 total face words
```

and sample mesh words such as:

```text
(0,1,11) -> R_0_1 R_1_11 R_11_0
(0,10,2) -> R_0_10 R_10_2 R_2_0
(9,10,11) -> R_9_10 R_10_11 R_11_9
```

## Interpretation

This is the first explicit bridge from topological face words to optical mesh operations:

```text
one triangular face = three F12 two-mode rotations
```

Boundary: the face basis is the existing MCXCII abstract orientable completion.  No Euclidean non-self-crossing polyhedron is asserted.
