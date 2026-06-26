# BT1814 hinge reduction note

The three-table search now has a much smaller orbit structure.

Counts:

```text
816 possible triples
54 Hesse hinges
10 Schlaefli stabilizer slices
```

Slice-size pattern:

```text
8 slices have size 6
2 slices have size 3
```

The observed three-table repair belongs to one of the size-6 slices. This is important because a four-state local quartet has exactly six unordered pairs:

```text
C(4,2) = 6
```

Search consequence: the next solver should not scan all 816 triples. It should scan the 10 slices first, then test the quartet-edge orientation inside each size-6 slice.
