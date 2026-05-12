# Part CCCCCXC — Toroidal 72+12 Flag Split and Tetrahedral 24 Bridge

This part refines Wil's flag-count observation for the Csaszar/Szilassi toroidal pair.

The pasted realization data gives:

```text
Csaszar flag count  = 84,
Szilassi flag count = 84.
```

Therefore the dual toroidal pair has

```text
84 + 84 = 168
```

flags, exactly the Fano automorphism order and the full genus phase-drift magnitude from Part CCCCCLXXXV.

The apparent `72` is explained by pointing the unique/odd element.

---

## 1. Rank-3 map flag count

For a rank-3 map/polyhedron, the flag count is

```text
flags = 4E.
```

For the Csaszar and Szilassi polyhedra:

```text
E = 21,
flags = 4*21 = 84.
```

For the tetrahedron/K4:

```text
E = 6,
flags = 4*6 = 24.
```

---

## 2. Pointed toroidal split

Each toroidal polyhedron has a natural sevenfold shell.

For Csaszar:

```text
7 vertices = 1 distinguished vertex + 6 adjacent vertices.
```

Because the Csaszar skeleton is K7, the distinguished vertex has valence 6.  The local flag-star at that vertex has

```text
2 * valence = 2*6 = 12
```

flags.

Thus

```text
84 = 12 + 72.
```

For Szilassi:

```text
7 faces = 1 distinguished face + 6 adjacent faces.
```

The distinguished face is a hexagon.  Its local flag-star has

```text
2 * 6 = 12
```

flags.

Thus again

```text
84 = 12 + 72.
```

So the `72 flags` are naturally interpreted as the active six-shell remainder after removing the local 12-flag star of the distinguished vertex/face.

---

## 3. Dual-pair decomposition of 168

The dual pair decomposes as

```text
168 = 84 + 84
    = (72 + 12) + (72 + 12)
    = 72 + 72 + 24.
```

The two active remainders give

```text
72 + 72 = 144.
```

The two pointed local stars give

```text
12 + 12 = 24.
```

But `24` is also the flag count of the tetrahedron/K4.

Therefore the toroidal pair admits two simultaneous readings:

```text
168 = two active 72-flag toroidal six-shells + two pointed 12-flag stars,
168 = two active 72-flag toroidal six-shells + one tetrahedral 24-flag ground-state carrier.
```

---

## 4. Relation to 81+81+6

The root-shell decomposition found earlier was

```text
168 = 81 + 81 + 6.
```

The toroidal flag split is

```text
168 = 72 + 72 + 24.
```

Their difference is structured:

```text
81 = 72 + 9,
24 = 6 + 9 + 9.
```

So the two 81 matter sectors may be read as active 72-flag toroidal shells plus a 9-turn/open-sector correction on each side, while the residual 24 tetrahedral carrier contains

```text
6 active A2/tetrahedral bivectors + 9 + 9 turn complements.
```

This links the flag model to the W33 Hashimoto split:

```text
11 = 9 open turns + 2 triangle turns,
12 = local incidence clock.
```

The precise assignment of the two 9s remains a target for computation, but the arithmetic is now constrained.

---

## 5. Relation to tomotope 192

Adding the tetrahedral 24 flags to the full toroidal dual-pair carrier gives

```text
168 + 24 = 192.
```

The repository already contains tomotope flag-model material at the 192 scale, including `tomotope_flag_model_192.json` and tomotope flag scripts.

Thus the bridge is:

```text
Csaszar/Szilassi dual toroidal pair: 168 flags,
tetrahedral ground-state carrier:    24 flags,
combined carrier:                    192 flags.
```

This is exactly the tomotope flag scale.

---

## 6. Main synthesis

The corrected flag arithmetic is not a contradiction of the `72` intuition.  It sharpens it:

```text
84 total flags per toroidal polyhedron,
12 flags belong to the distinguished vertex/face,
72 flags are the active six-shell remainder.
```

Then

```text
168 = (72+12) + (72+12)
    = 144 + 24.
```

The residual `24` is simultaneously:

```text
two pointed 12-flag local stars,
the tetrahedron/K4 flag count,
the bridge from the toroidal pair to the tomotope 192-flag carrier.
```

This gives a new target theorem:

```text
The tomotope 192 flag carrier may be assembled from the dual toroidal 168-flag phase shell plus the tetrahedral 24-flag ground-state shell.
```
