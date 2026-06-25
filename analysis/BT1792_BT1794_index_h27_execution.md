# BT1792--BT1794 index-driven H27 execution

## Index read: what changed the plan

The live `docs/index.html` page is not just a table of contents. Its opening theorem spine already contains the exact local rule needed here:

```text
W(3,3) = SRG(40,12,2,4)
1 + 12 + 27 local split
12 = four qutrit MUB triangles
raw 27 = nonabelian Heisenberg torsor, induced graph 8-regular
raw 27 + canonical nine-triangle central-fibre relation = GQ(2,4)
complement = Schlaefli graph
```

It also records the packet version of the same bridge: the `27` balanced packets recover the honest `H27` graph, the Schlaefli graph, the intersection graph, and the full `45 = 36 + 9` tritangent-support package. That is the crucial index lesson: do not collapse the raw 8-regular second subconstituent, the Payne-derived `GQ(2,4)`, and the balanced-packet tritangent support into one unnamed `27`. They are related by an exact transform.

## BT1792: true BT1781 tuple recovery audit

I searched the current repo surface for the real BT1781 tuple source: `BT1781`, `9980`, accepted local triples, the count vector, and the frontier notes. The repo exposes the counts and the frontier warning, but not the actual accepted tuple lists and not the acceptance predicate.

The executable result is therefore an honesty boundary, not a fabricated tuple file:

```text
raw entries = 31104
accepted entries = 9980
counts = [528,562,578,528,612,580,528,528,480,528,612,564,562,528,578,562,562,560]
actual tuple lists found = false
acceptance predicate found = false
```

BT1792 still reconstructs the correct NetworkX target geometry:

```text
raw local 27 shell: 27 vertices, 108 edges, 8-regular
Payne GQ(2,4):      SRG(27,10,1,5)
Schlaefli graph:    SRG(27,16,10,8)
H27 support:        36 old W33 triples + 9 Heisenberg fibres = 45
```

Conclusion: the BT1781 tuple file cannot be honestly recovered from the current public artifacts. The next true recovery must locate the predicate or tuple-list source; until then, the exact recoverable object is the H27/Payne projection scaffold.

## BT1793: Payne--BT1788 alignment matrix

BT1788 has 18 ternary tables indexed by nonconcurrent Hesse triples:

```text
(R_i,C_j,D_s),  with s != (j-i) mod 3.
```

The natural pair-frontier lift sends a table to three frontier points:

```text
RC(i,j), RD(i,s), CD(j,s).
```

BT1793 tests whether these 18 triples are simply 18 renamed H27 support lines. They are not.

Default labelling:

```text
nonconcurrent hits on H27 support = 2 / 18
total support hits               = 3 / 27
concurrent hits                  = 1 / 9
```

Then I searched the best independent affine relabelling of the `RD` and `CD` pair-frontier planes while holding `RC` fixed:

```text
search space = 432^2 affine maps
best nonconcurrent hits = 12 / 18
best total support hits = 15 / 27
best concurrent hits = 3 / 9
number of tied optima = 2
```

One optimum is:

```text
RD matrix      = [[2,2],[0,2]], translation = [1,1]
CD matrix      = [[0,1],[2,1]], translation = [2,2]
```

Conclusion: the missing BT1781 materialization is not coordinate renaming. There is a genuine projection/transport map between the Hesse table CSP and the H27/Payne support geometry.

## BT1794: Schlaefli/E6 lift

BT1794 takes the H27/Payne geometry all the way to the cubic-surface package.

NetworkX verifies:

```text
GQ(2,4) intersection graph = SRG(27,10,1,5)
Schlaefli skew graph       = SRG(27,16,10,8)
```

The `45` H27 support triples are exactly the `45` triangles of the intersection graph, i.e. the local tritangent-plane package.

Then the Schlaefli graph itself reconstructs the double-six layer:

```text
K6 sixers in Schlaefli graph = 72
double-sixes                 = 36
each double-six induced profile = 12 vertices, 36 Schlaefli edges, 6 cross matching edges
each cubic-surface line lies in 16 double-sixes
```

This is the clean E6 lift:

```text
27 H27 points        = 27 cubic-surface lines
45 H27 support lines = 45 tritangent planes
36 double-sixes      = cubic-surface double-six layer
Schlaefli graph      = skew-line graph
GQ(2,4)              = line-intersection / tritangent support graph
```

## Final synthesis

The index hint was exactly right and stronger than our previous framing:

```text
BT1788 27 pair-frontier
    -> H27/Payne boundary
    -> GQ(2,4) / Schlaefli dual pair
    -> cubic-surface E6 package: 27 lines, 45 tritangents, 36 double-sixes
```

But BT1793 blocks the too-easy interpretation:

```text
18 nonconcurrent Hesse ternary tables != 18 H27 support lines by relabelling.
```

So the next real breakthrough is the missing transform, not another count check. We need the materialization map that sends each ternary-table acceptance relation onto the H27/Payne/E6 support package.

## Files

- `analysis/bt1792_true_tuple_recovery_audit.py`
- `data/bt1792_true_tuple_recovery_audit.json`
- `analysis/bt1793_payne_bt1788_alignment_matrix.py`
- `data/bt1793_payne_bt1788_alignment_matrix.json`
- `analysis/bt1794_schlafli_e6_lift.py`
- `data/bt1794_schlafli_e6_lift.json`
- `analysis/BT1792_BT1794_index_h27_execution.md`
