# BT813 — The Vacuum Transition Matrix

The complete relative-position table between the five vacua (BT812):
for each ordered pair of maximal classes, the orbit partition of one
acting on the other's coset space (GAP-witnessed).

```text
            G/27        G/36       G/40line   G/40point  G/45
  M27    [1,10,16]    [16,20]      [40]       [40]      [5,40]
  M36    [12,15]      [1,15,20]    [10,30]    [40]      [15,30]
  M40l   [27]         [9,27]       [1,12,27]  [4,36]    [18,27]
  M40p   [27]         [36]         [4,36]     [1,12,27] [9,36]
  M45    [3,24]       [12,24]      [16,24]    [8,32]    [1,12,32]
```

## Theorems

1. **Double-coset symmetry** holds throughout (orbit counts match
   transposed entries), and all rows sum correctly.
2. **The diagonals are the classical intersection geometries**: the 27
   icosahedral registers carry the Schläfli line-intersection structure
   [1,10,16] (meet 10 / skew 16); the 36 spreads carry the double-six
   ranks [1,15,20]; the 45 polar pairs the tritangent ranks [1,12,32].
   The BT810 dictionary is confirmed at the orbit level, not just by
   counting.
3. **Every W(3,3) line lies in exactly 9 regular spreads**
   (36 x 10 = 40 x 9; the [9,27] entry), while every POINT is in
   uniform position to all 36 spreads (the [36]-transitive entry) —
   spreads are line-structured, point-blind.
4. **The off-diagonal entries speak substrate**:
   - icosahedral vacuum sees the 45 tritangents as [5, 40]: five = F5
     distinguished polar pairs per register;
   - a polar pair sees the 27 registers as [3, 24]: three = q
     distinguished registers per tritangent;
   - icosahedral <-> spread: [16, 20] (the mu^2 = 16 register cells +
     20 BC rings) and [12, 15] (k + g);
   - spread <-> polar: [15, 30] (g + h(E8)) and [12, 24] (k + f).

## Reading

The five vacua are not isolated readings: the transition matrix is the
complete "moduli interaction" of the substrate, every entry a substrate
primitive, every diagonal a classical cubic-surface geometry.  Combined
with BT742 (Steinberg), BT744 (building), BT777 (chart atlas), and
BT810 (Schläfli dictionary), PSp(4,3)'s subgroup geometry is now mapped
end to end: objects, stabilizers, vacua, and transitions.

## Boundary

Open: the [5,40] icosa-tritangent pentad (which five? an A5-orbit of
polar pairs = a pentagonal structure on the register); the [3,24]
triad's relation to the q = 3 generations; and lifting the transition
matrix to the Hecke algebra level (structure constants, not just orbit
counts).
