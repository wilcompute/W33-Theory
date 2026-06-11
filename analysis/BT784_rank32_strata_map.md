# BT784 — Rank-32 Strata Map

BT784 compares the BT780 rank-32 orbit alphabet with the known rank-4 count data.

Rank-32 suborbit size profile:

```text
{1:1, 3:1, 4:2, 6:2, 8:3, 12:11, 24:9, 48:3}
```

Target count profile:

```text
vertices = 4
edges = 12
faces = 16
cells = 8
one flag orbit = 96
all flags = 192
```

Exact packet matches:

```text
4   = one size-4 orbit
8   = one size-8 orbit
12  = one size-12 orbit
16  = 8 + 8, or 4 + 4 + 4 + 4
96  = 48 + 48
192 = 4 * 48
```

The key observation is that 4, 8, and 12 are primitive packet sizes in the
rank-32 alphabet, while 16 is composite.  This makes the face layer the likely
site of the bridge obstruction found in BT783.

BT783 found a binary module mismatch:

```text
cube side: 1 + 2
rank-4 side: 2 + 2
```

BT784 gives the count-level shadow:

```text
primitive packets: 4, 8, 12
composite packet: 16 = 8 + 8
```

So the next bridge should focus on the 16-face packet lift rather than the
vertex, edge, or cell packet.
