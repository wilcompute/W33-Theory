# BT1801--BT1803 nullspace, fibre search, and W(E6) orbit handoff

## BT1801 — full double-six matrix and linear kernels

BT1801 rebuilds the Schläfli/E6 double-six incidence around the BT1795 transported 18-line set.

The matrix is:

```text
18 transported Hesse table-lines x 36 double-six checks
```

with row labels:

```text
T001 T002 T010 T012 T020 T021 T100 T101 T111 T112 T120 T122 T200 T202 T210 T211 T221 T222
```

The matrix has:

```text
row sum set    = {24}
column sum set = {12}
rank_F2 = 16
rank_F3 = 13
left nullity/right nullity over F2 = 2 / 20
left nullity/right nullity over F3 = 5 / 23
```

The committed script `analysis/bt1801_double_six_matrix_nullspaces.py` writes the full matrix and all left/right kernel bases to:

```text
data/bt1801_double_six_matrix_nullspaces_full.json
```

The compact result file keeps the explicit row labels, ranks, dimensions, and left-kernel bases.

## BT1802 — structured 12-symbol fibre search

BT1802 tests whether the `9980` count vector can be explained by simple structured fibre rules above the BT1795 transport.

Counts:

```text
[528,562,578,528,612,580,528,528,480,528,612,564,562,528,578,562,562,560]
```

Total:

```text
9980
```

Test results:

```text
12 = 3 x 4 uniform residue lift: fail (not all counts multiple of 64)
12 = 2 x 6 uniform binary lift: fail (not all counts multiple of 216)
coarse binary/quartic lift:      fail (not all counts multiple of 8)
point-additive H27 potential:    fail (unique left relation dot counts = 164)
F2 double-six syndrome:          pass, but only because all counts are even
F3 double-six syndrome:          fail with evaluations [0,2,1,1,1]
```

Conclusion: the missing BT1781 rule is not H27 support membership, not old/new support kind, not a uniform residue lift, not point-additive on H27, and not a pure F3 double-six syndrome. It must be a nonuniform 12-symbol fibre rule above the transport.

## BT1803 — W(E6) orbit handoff

BT1798 already disproved literal uniqueness with NetworkX:

```text
source automorphism order = 216
first 1000 transports -> 504 distinct support images
```

BT1803 commits the right handoff rather than pretending NetworkX can finish the full E6 orbit problem. It creates:

```text
analysis/bt1803_we6_orbit_handoff.py
analysis/bt1803_we6_orbit_handoff.gap
data/bt1803_we6_orbit_handoff.json
```

The GAP handoff asks for:

```text
Aut(Schläfli), expected order 51840 = W(E6)
action on 45 tritangent support lines
orbit and stabilizer of the BT1795 18-line image
orbit classes grouped by old/new count and double-six syndrome ranks
```

BT1803's honest status is `handoff_prepared_not_full_orbit_computed`.

## Bottom line

```text
BT1801: double-six syndrome matrix is now executable with kernel data.
BT1802: the 9980 vector forces a genuinely nonuniform 12-symbol fibre layer.
BT1803: full transport canonicalization is a W(E6) orbit problem, not a NetworkX-only job.
```
