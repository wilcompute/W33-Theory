# Part MMCCCLXXI: Bridge-Line Affine Cayley Cube

## Claim

The `27` bridge lines in the golden-selector failure carrier are an explicit
affine qutrit cube. They are not merely counted by `3^3`.

Fix the anchor line. For each bridge line and each of the four anchor points,
the generalized-quadrangle axiom gives a unique off-anchor line through that
point meeting the bridge. This gives a natural word

```text
(x0, x1, x2, x3) in F3^4.
```

The `27` bridge words are exactly the affine subspace

```text
x0 + x1 + 2*x2 + x3 = 0  over F3.
```

Every projection deleting one coordinate is a bijection onto `F3^3`.

## Cayley Model

Using the first three word coordinates, the bridge-line intersection graph is
the 8-regular Cayley graph

```text
Cay(F3^3, {+/-e1, +/-e2, +/-e3, +/-(1,1,1)})
```

up to the explicit `GL(3,3)` coordinate change

```text
[[0, 1, 1],
 [1, 0, 1],
 [2, 2, 2]].
```

The spectrum is therefore the corrected Part CDIV affine-cube spectrum:

```text
{8^1, 2^12, -1^8, -4^6}.
```

The common-neighbor profile is:

```text
adjacent:    {1: 108}
nonadjacent: {2: 162, 4: 81}
```

## Reading

Part MMCCCLXX showed that the unique golden failures are

```text
K2,2 x F3^3 = 108.
```

This part identifies the shared `F3^3` factor itself. It is the same affine
qutrit cube already seen in the local `AG(3,3)` shell and in the Part CDIV
Cayley graph.

## Boundary

This identifies the `27`-line bridge carrier and its spectrum. It still does
not identify the four `K2,2` cross-pair copies with explicit `O^-(6,2)/A5`
cosets.

## Verification

Run:

```bash
python3 analysis/w33_bridge_line_affine_cayley_cube.py
```

Expected result: `12/12` checks verified.
