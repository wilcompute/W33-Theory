# BT1818-BT1820 fibre-law summary

Executed all three requested moves after BT1815-BT1817, continuing the fibre-law push.

## BT1818: triality gauge from old/new transport

The D4 triality gauge is fixed relative to the BT1795 transport kind.

The unique BT1816 repair has:

```text
T010: old support
T210: old support
T222: new support
```

Therefore the oriented edge is:

```text
old + old -> new
```

We choose the D4/GKP gauge where the observed edge `00--11` is the old-to-new displacement and name the nonzero endpoint `11` as the conjugate-spinor coset `c`. Triality may still rename `v,s,c`, but the invariant branch statement is now precise: the syndrome-valid edge is the one whose positive return lands in the new support sector.

## BT1819: oriented-edge tuple materializer

The tuple-table materializer separates two sections over the `12 = 3 x 4` domain:

```text
observed twisted section: 9980 tuples
untwisted F3-flat section: 9978 tuples
```

The difference is exactly the unique BT1816 oriented K4 edge law:

```text
add two 00--11 edge-pair tuples to T010
add two 00--11 edge-pair tuples to T210
remove two corresponding 00--11 edge-pair tuples from T222
```

The special edge transfer is structural and fixed; background tuples are deterministic filler pending the true accepted-tuple predicate.

## BT1820: BC-ring oriented-edge embedding

The unique oriented transfer embeds into the BC-ring model by mapping:

```text
T_i,j,s -> ring cell (phase = 3j+s, strand = i)
```

Then:

```text
T010 -> phase 3, strand 0
T210 -> phase 3, strand 2
T222 -> phase 8, strand 2
```

The two source/removal tables share phase 3 and differ by strand, while the return table shares strand 2 with T210 and sits at phase 8. The hidden quartet edge is the tetrahedral face-pair:

```text
F0--F3
```

## Current law

```text
12 = 3 x 4
3 = BC/Hesse strand coordinate
4 = D4/GKP tetrahedral K4 quartet
unique correction = old+old -> new oriented edge
observed 9980 = twisted section
repaired 9978 = untwisted F3-flat section
BC lift = F0--F3 face-pair transfer on the 30-cell ring
```

The same unique correction is now simultaneously selected by Hesse hinge symmetry, W(E6) slice geometry, D4/GKP triality gauge, F3 syndrome repair, and BC tetrahedral face-pair geometry.
