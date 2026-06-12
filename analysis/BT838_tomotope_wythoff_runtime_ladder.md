# BT838 - Tomotope Wythoff Runtime Ladder

## Summary

The Grünbaum-Coxeter/tomotope operation tables show the local tomotope
operation vertex counts:

```text
original      4
rectified     12
truncated     24
expanded      48
omnitruncated 96
```

BT838 identifies these as the holonet packet-expansion ladder, not just as
geometric variants.

## Runtime Reading

| operation | count | runtime layer |
|---|---:|---|
| original tomotope | 4 | four transversal vertex carriers, `mu` |
| rectified tomotope | 12 | local tomotope edge axes, `k` |
| truncated tomotope | 24 | full lift of the `D12` mirror-slot stabilizer, `f` |
| maximal expanded tomotope | 48 | BT814 middle packet ABI |
| omnitruncated tomotope | 96 | half-flag packet boundary |

The verified BT814 packet has 192 full flags, so:

```text
2 * omnitruncated = 2 * 96 = 192
```

The cover-lifted version is stronger:

```text
expanded slots = 48*k^3 = BT832 lifted packet capacity
full flags     = 192*k^3 = BT831 W_k order
```

## Why This Matters

The maximal expanded tomotope is the exact local packet surface already used by
the runtime.  The omnitruncated tomotope is the half-flag boundary whose doubled
base/shadow fiber gives the durable packet flags.  So the Wythoff operations act
like packet expansion stages:

```text
carrier -> edge-axis -> mirror lift -> packet ABI -> flag boundary
```

This gives a clean bridge from the Grünbaum-Coxeter tables to the engineering
architecture: the abstract tomotope operations are the compiler's packet-growth
states.

## Top 3 Next Moves

1. Build the actual adjacency/incidence graph of the 96 omnitruncated half-flags
   from the existing 48 block model and prove the base/shadow doubling map.
2. Identify whether the `W_k_order = 192*k^3` full-flag carrier has a named
   regular-cover monodromy quotient.
3. Compare the 96 half-flag boundary against the 96 vertices of the
   omnitruncated cube/octahedral packet candidates in the chart stabilizer.
