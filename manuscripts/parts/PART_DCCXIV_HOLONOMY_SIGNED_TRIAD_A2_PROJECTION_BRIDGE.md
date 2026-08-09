# Part DCCXIV - Holonomy Signed-Triad A2 Projection Bridge

## Why this part exists

`Part DCCXI` found the first welded-coherence defect:

```text
[[6561, 0], [0, -6561]].
```

The recent tomotope/Clifford review sharpened the interpretation of the recurring six-shell:

```text
primitive six-shell = signed Clifford triad
projected six-shell = A2 root hexagon
```

So the six should not be identified with A2 by fiat. A2 is the charge projection of a more primitive signed three-axis object.

## Exact lift

Use the three Clifford bivector axes:

```text
B23, B31, B12.
```

With orientation signs this gives six channels:

```text
{+B23, -B23, +B31, -B31, +B12, -B12}.
```

The DCCXI packet magnitude splits evenly:

```text
6561 / 3 = 2187,
6 * 2187 = 13122.
```

So the signed-diagonal support is exactly three positive packet axes against three negative packet axes.

## A2 projection

Project the primitive axes by:

```text
B23 -> ( 1,-1, 0)
B31 -> ( 0, 1,-1)
B12 -> (-1, 0, 1)
```

The three projected positive roots sum to zero and have norm `2`. Adding signs gives six distinct roots with dot spectrum:

```text
{-2, -1, 1, 2}.
```

That is the A2 root hexagon.

## QEC ouroboros link

The public "snake eats its tail" picture should now be read as a protected finite cycle, not a cyclic `Z40` shortcut:

```text
480 = 40 * 12
12 = 6 + 6.
```

The local turn alphabet is six signed Clifford channels plus six projected A2/Weyl return channels on the 480 directed Hashimoto/fusion carrier. The `H1=81` QEC payload is preserved by the return, rather than collapsed by a global cyclic Cayley action.

## Executable artifact

Verifier:

```text
verify_dccxiv_holonomy_signed_triad_a2_projection_bridge.py
```

Tests:

```text
tests/test_dccxiv_holonomy_signed_triad_a2_projection_bridge.py
```

Generated summary:

```text
data/dccxiv_holonomy_signed_triad_a2_projection_bridge.json
```

---
*W33-Theory | Part DCCXIV | the primitive six-shell is the signed Clifford triad; A2 is the charge projection, and the QEC ouroboros local alphabet is the resulting 6+6 return law.*
