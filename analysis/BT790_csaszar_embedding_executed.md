# BT790 — Executed Csaszar Embedding Verifier

The open BT790 question was whether W(3,3) contains seven mutually disjoint
totally isotropic lines.

The verifier has now been executed.

## Result

```text
points = 40
isotropic lines = 40
disjoint-line graph edges = 540
disjoint-line graph degree = 27
maximum mutually disjoint isotropic lines = 10
10-line spread count = 36
7-line torus subcell count = 5400
```

Therefore:

```text
Csaszar K7 embedding exists: YES
```

In fact, the result is stronger than a 7-line cell.  W(3,3) contains full
10-line spreads, and seven-line torus cells occur inside the spread geometry.

## Consequence

The toroidal transition layer is internal to the Witting/W33 substrate.  The
fractal model does not hit a hard floor at the torus interface.  The local
Csaszar-type torus is an intrinsic subcell of the same finite geometry that
supports the cube-web and tomotope packets.

## Example spread

One 10-line spread has line indices:

```text
[0, 13, 15, 21, 24, 27, 31, 33, 35, 37]
```

with point partition:

```text
[0, 1, 3, 5]
[2, 10, 24, 30]
[4, 15, 22, 33]
[6, 18, 26, 38]
[7, 14, 28, 35]
[8, 16, 29, 39]
[9, 20, 23, 32]
[11, 17, 25, 36]
[12, 19, 27, 34]
[13, 21, 31, 37]
```

## Structural reading

The open document expected a possible maximum of 4 or 5.  The executed verifier
shows maximum 10.  So the earlier hard-floor branch is eliminated.

The new local hierarchy becomes:

```text
skew pair chart  ->  7-line torus subcell  ->  10-line spread envelope
```

The spread envelope is likely the correct object for BT794-BT796 regulus and
2160 fibration work.
